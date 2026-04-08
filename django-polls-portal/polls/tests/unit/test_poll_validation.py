import pytest
from django.utils import timezone

from polls.models import Poll


@pytest.mark.django_db
def test_poll_question_must_not_be_empty():
    poll = Poll(
        creator_user_id="creator",
        question_text="",
        opens_at=timezone.now(),
        closes_at=timezone.now() + timezone.timedelta(hours=1),
    )
    with pytest.raises(ValueError):
        poll.clean()
