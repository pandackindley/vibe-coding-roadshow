from django.utils import timezone

from polls.models import PollReview, PollResponse


def enforce_retention() -> dict[str, int]:
    now = timezone.now()
    deleted_responses, _ = PollResponse.objects.filter(retention_delete_after__lte=now).delete()
    deleted_reviews, _ = PollReview.objects.filter(retention_delete_after__lte=now).delete()
    return {"responses": deleted_responses, "reviews": deleted_reviews}
