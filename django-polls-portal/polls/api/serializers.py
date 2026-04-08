from rest_framework import serializers

from polls.models import Poll, PollOption, PollResponse, PollReview


class PollOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollOption
        fields = ["id", "option_text", "option_order"]


class PollSerializer(serializers.ModelSerializer):
    options = PollOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ["id", "question_text", "status", "opens_at", "closes_at", "options"]


class CreatePollSerializer(serializers.Serializer):
    questionText = serializers.CharField(max_length=500)
    options = serializers.ListField(child=serializers.CharField(max_length=200), min_length=2)
    opensAt = serializers.DateTimeField()
    closesAt = serializers.DateTimeField()


class SubmitResponseSerializer(serializers.Serializer):
    optionId = serializers.UUIDField()


class PollResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollResponse
        fields = ["id", "poll_id", "option_id", "submitted_at"]


class CreateReviewSerializer(serializers.Serializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)
    comments = serializers.CharField(required=False, allow_blank=True)


class PollReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollReview
        fields = ["id", "poll_id", "reviewer_user_id", "rating", "comments", "created_at"]
