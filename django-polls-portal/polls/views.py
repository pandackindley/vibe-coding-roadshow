from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from polls.models import Poll, PollStatus


def home(request):
    return redirect("poll_list")


def poll_list(request):
    polls = Poll.objects.all().order_by("-created_at")
    return render(request, "polls/poll_list.html", {"polls": polls, "now": timezone.now()})


def create_poll_page(request):
    return render(request, "polls/create_poll.html")


def respond_poll_page(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    return render(request, "polls/respond_poll.html", {"poll": poll})


def results_page(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    show_results = poll.status == PollStatus.CLOSED or timezone.now() > poll.closes_at
    return render(request, "polls/results.html", {"poll": poll, "show_results": show_results})


def review_poll_page(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    return render(request, "polls/review_poll.html", {"poll": poll})
