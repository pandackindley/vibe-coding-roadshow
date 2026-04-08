import pytest
from django.utils import timezone

from polls.models import Poll, PollStatus
from polls.services.vote_guard import can_accept_response


@pytest.mark.django_db
def test_reject_inactive_poll():
    poll = Poll.objects.create(
        creator_user_id="creator",
        question_text="Q?",
        status=PollStatus.DRAFT,
        opens_at=timezone.now(),
        closes_at=timezone.now() + timezone.timedelta(hours=1),
    )
    allowed, reason = can_accept_response(poll, "token")
    assert not allowed
    assert reason == "inactive_poll"
