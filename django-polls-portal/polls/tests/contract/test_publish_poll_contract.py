import pytest
from django.urls import reverse

from polls.models import Poll


@pytest.mark.django_db
def test_publish_poll_requires_auth(client, django_user_model):
    poll = Poll.objects.create(creator_user_id="creator", question_text="Q", opens_at="2026-01-01T00:00:00Z", closes_at="2026-01-02T00:00:00Z")
    response = client.post(reverse("api_publish_poll", kwargs={"poll_id": poll.id}))
    assert response.status_code in {401, 403}
