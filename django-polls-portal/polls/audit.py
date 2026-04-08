import logging

logger = logging.getLogger("polls.audit")


def audit_event(actor: str, action: str, poll_id: str) -> None:
    logger.info("actor=%s action=%s poll_id=%s", actor, action, poll_id)
