import pytest
from django.utils import timezone

from polls.models import Poll, PollReview
from polls.services.retention import enforce_retention


@pytest.mark.django_db
def test_retention_deletes_expired_reviews():
    poll = Poll.objects.create(
        creator_user_id="creator",
        question_text="Q",
        opens_at=timezone.now(),
        closes_at=timezone.now() + timezone.timedelta(hours=1),
    )
    review = PollReview.objects.create(
        poll=poll,
        reviewer_user_id="reviewer",
        rating=4,
        comments="ok",
        retention_delete_after=timezone.now() - timezone.timedelta(days=1),
    )
    enforce_retention()
    assert not PollReview.objects.filter(id=review.id).exists()
