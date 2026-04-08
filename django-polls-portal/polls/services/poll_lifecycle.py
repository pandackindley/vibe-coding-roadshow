from polls.models import Poll, PollOption, PollStatus


def create_draft(creator_user_id: str, question_text: str, options: list[str], opens_at, closes_at) -> Poll:
    poll = Poll.objects.create(
        creator_user_id=creator_user_id,
        question_text=question_text,
        opens_at=opens_at,
        closes_at=closes_at,
    )
    for idx, option in enumerate(options, start=1):
        PollOption.objects.create(poll=poll, option_text=option.strip(), option_order=idx)
    return poll


def publish_poll(poll: Poll) -> Poll:
    options = list(poll.options.values_list("option_text", flat=True))
    distinct_options = {o.strip().lower() for o in options if o and o.strip()}
    if len(distinct_options) < 2:
        raise ValueError("Poll requires at least two unique options")
    poll.status = PollStatus.PUBLISHED
    poll.save(update_fields=["status", "updated_at"])
    return poll
