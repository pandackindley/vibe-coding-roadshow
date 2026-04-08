import pytest
from django.urls import reverse
from django.utils import timezone

from polls.models import Poll, PollStatus


@pytest.mark.django_db
def test_results_visible_after_close(client):
    poll = Poll.objects.create(
        creator_user_id="creator",
        question_text="Q",
        status=PollStatus.CLOSED,
        opens_at=timezone.now() - timezone.timedelta(days=1),
        closes_at=timezone.now() - timezone.timedelta(hours=1),
    )
    response = client.get(reverse("api_poll_results", kwargs={"poll_id": poll.id}))
    assert response.status_code == 200
