from datetime import timedelta

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from polls.api.errors import ERRORS
from polls.api.serializers import (
    CreatePollSerializer,
    CreateReviewSerializer,
    PollReviewSerializer,
    PollSerializer,
    PollResponseSerializer,
    SubmitResponseSerializer,
)
from polls.audit import audit_event
from polls.models import Poll, PollOption, PollResponse, PollReview, PollStatus
from polls.permissions import is_creator, is_reviewer
from polls.services.poll_lifecycle import create_draft, publish_poll
from polls.services.token_identity import cooldown_expiry, issue_token, token_hash, validate_token
from polls.services.vote_guard import can_accept_response


class CreatePollView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if not is_creator(request.user):
            return Response({"detail": "Creator role required."}, status=status.HTTP_403_FORBIDDEN)

        serializer = CreatePollSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        poll = create_draft(
            creator_user_id=str(request.user),
            question_text=data["questionText"],
            options=data["options"],
            opens_at=data["opensAt"],
            closes_at=data["closesAt"],
        )
        audit_event(str(request.user), "create_poll", str(poll.id))
        return Response(PollSerializer(poll).data, status=status.HTTP_201_CREATED)


class PublishPollView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, poll_id):
        if not is_creator(request.user):
            return Response({"detail": "Creator role required."}, status=status.HTTP_403_FORBIDDEN)
        poll = get_object_or_404(Poll, id=poll_id)
        try:
            publish_poll(poll)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        audit_event(str(request.user), "publish_poll", str(poll.id))
        return Response(PollSerializer(poll).data)


class SubmitResponseView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, poll_id):
        poll = get_object_or_404(Poll, id=poll_id)
        serializer = SubmitResponseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        raw_token = request.COOKIES.get("poll_token") or issue_token()
        if not validate_token(raw_token):
            raw_token = issue_token()
        token_value = token_hash(raw_token)

        allowed, reason = can_accept_response(poll, token_value)
        if not allowed:
            code = status.HTTP_423_LOCKED if reason == "inactive_poll" else status.HTTP_409_CONFLICT
            return Response({"detail": ERRORS[reason]}, status=code)

        option = get_object_or_404(PollOption, id=serializer.validated_data["optionId"], poll=poll)
        response_obj = PollResponse.objects.create(
            poll=poll,
            option=option,
            participant_token_hash=token_value,
            cooldown_expires_at=cooldown_expiry(),
            retention_delete_after=timezone.now() + timedelta(days=365),
        )
        payload = PollResponseSerializer(response_obj).data
        resp = Response(payload, status=status.HTTP_201_CREATED)
        resp.set_cookie("poll_token", raw_token, httponly=True, samesite="Lax", max_age=60 * 60 * 24 * 365)
        return resp


class ResultsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, poll_id):
        poll = get_object_or_404(Poll, id=poll_id)
        if poll.status != PollStatus.CLOSED and timezone.now() <= poll.closes_at:
            return Response({"detail": "Results are hidden while poll is open."}, status=status.HTTP_423_LOCKED)

        breakdown = []
        for option in poll.options.all().order_by("option_order"):
            breakdown.append({"optionId": str(option.id), "count": option.responses.count()})
        return Response(
            {"pollId": str(poll.id), "totalResponses": poll.responses.count(), "optionBreakdown": breakdown},
            status=status.HTTP_200_OK,
        )


class ReviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, poll_id):
        if not is_reviewer(request.user):
            return Response({"detail": "Reviewer role required."}, status=status.HTTP_403_FORBIDDEN)
        poll = get_object_or_404(Poll, id=poll_id)
        serializer = CreateReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = PollReview.objects.create(
            poll=poll,
            reviewer_user_id=str(request.user),
            rating=serializer.validated_data["rating"],
            comments=serializer.validated_data.get("comments", ""),
            retention_delete_after=timezone.now() + timedelta(days=365),
        )
        audit_event(str(request.user), "review_poll", str(poll.id))
        return Response(PollReviewSerializer(review).data, status=status.HTTP_201_CREATED)

    def get(self, request, poll_id):
        if not is_reviewer(request.user):
            return Response({"detail": "Reviewer role required."}, status=status.HTTP_403_FORBIDDEN)
        poll = get_object_or_404(Poll, id=poll_id)
        reviews = poll.reviews.all().order_by("-created_at")
        return Response(PollReviewSerializer(reviews, many=True).data)
