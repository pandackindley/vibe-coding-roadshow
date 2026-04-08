import pytest
from django.urls import reverse
from django.utils import timezone

from polls.models import Poll, PollStatus


@pytest.mark.django_db
def test_results_hidden_for_open_poll(client):
    poll = Poll.objects.create(
        creator_user_id="creator",
        question_text="Q",
        status=PollStatus.PUBLISHED,
        opens_at=timezone.now() - timezone.timedelta(minutes=1),
        closes_at=timezone.now() + timezone.timedelta(hours=1),
    )
    response = client.get(reverse("api_poll_results", kwargs={"poll_id": poll.id}))
    assert response.status_code == 423
