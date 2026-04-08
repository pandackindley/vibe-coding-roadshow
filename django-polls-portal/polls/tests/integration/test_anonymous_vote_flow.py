import pytest
from django.urls import reverse
from django.utils import timezone

from polls.models import Poll, PollOption, PollStatus


@pytest.mark.django_db
def test_anonymous_vote_success(client):
    poll = Poll.objects.create(
        creator_user_id="creator",
        question_text="Q",
        status=PollStatus.PUBLISHED,
        opens_at=timezone.now() - timezone.timedelta(minutes=1),
        closes_at=timezone.now() + timezone.timedelta(hours=1),
    )
    option = PollOption.objects.create(poll=poll, option_text="A", option_order=1)
    response = client.post(reverse("api_submit_response", kwargs={"poll_id": poll.id}), data={"optionId": str(option.id)}, content_type="application/json")
    assert response.status_code == 201
