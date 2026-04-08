import pytest
from django.urls import reverse
from django.utils import timezone

from polls.models import Poll


@pytest.mark.django_db
def test_reviews_require_auth(client):
    poll = Poll.objects.create(creator_user_id="creator", question_text="Q", opens_at=timezone.now(), closes_at=timezone.now() + timezone.timedelta(hours=1))
    response = client.get(reverse("api_poll_reviews", kwargs={"poll_id": poll.id}))
    assert response.status_code in {401, 403}
