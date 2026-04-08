from django.utils import timezone

from polls.models import PollResponse, PollStatus


def can_accept_response(poll, token_hash_value: str) -> tuple[bool, str]:
    now = timezone.now()
    if poll.status != PollStatus.PUBLISHED or now < poll.opens_at or now > poll.closes_at:
        return False, "inactive_poll"

    existing = PollResponse.objects.filter(poll=poll, participant_token_hash=token_hash_value).first()
    if existing:
        if existing.cooldown_expires_at > now:
            return False, "cooldown_violation"
        return False, "duplicate_response"

    return True, "ok"
