import pytest
from django.utils import timezone

from polls.models import Poll, PollOption, PollStatus
from polls.services.poll_lifecycle import publish_poll


@pytest.mark.django_db
def test_creator_publish_flow_changes_status():
    poll = Poll.objects.create(
        creator_user_id="creator",
        question_text="Question",
        opens_at=timezone.now(),
        closes_at=timezone.now() + timezone.timedelta(hours=1),
    )
    PollOption.objects.create(poll=poll, option_text="A", option_order=1)
    PollOption.objects.create(poll=poll, option_text="B", option_order=2)
    publish_poll(poll)
    poll.refresh_from_db()
    assert poll.status == PollStatus.PUBLISHED
