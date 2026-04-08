import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_create_poll_requires_auth(client):
    response = client.post(reverse("api_create_poll"), data={}, content_type="application/json")
    assert response.status_code in {401, 403}
