import hashlib
from datetime import timedelta

from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
from django.utils import timezone


def _cipher() -> Fernet:
    secret = settings.TOKEN_SIGNING_SECRET.encode("utf-8")
    key = hashlib.sha256(secret).digest()
    token_key = __import__("base64").urlsafe_b64encode(key)
    return Fernet(token_key)


def issue_token() -> str:
    payload = f"anon:{timezone.now().timestamp()}".encode("utf-8")
    return _cipher().encrypt(payload).decode("utf-8")


def validate_token(token: str) -> bool:
    try:
        _cipher().decrypt(token.encode("utf-8"), ttl=60 * 60 * 24 * 365)
        return True
    except InvalidToken:
        return False


def token_hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def cooldown_expiry() -> timezone.datetime:
    return timezone.now() + timedelta(seconds=settings.POLL_COOLDOWN_SECONDS)
