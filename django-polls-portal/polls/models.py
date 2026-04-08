import uuid
from datetime import timedelta

from django.db import models
from django.utils import timezone


class PollStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    PUBLISHED = "published", "Published"
    CLOSED = "closed", "Closed"
    ARCHIVED = "archived", "Archived"


class Poll(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator_user_id = models.CharField(max_length=150)
    question_text = models.CharField(max_length=500)
    status = models.CharField(max_length=16, choices=PollStatus.choices, default=PollStatus.DRAFT)
    opens_at = models.DateTimeField()
    closes_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self) -> None:
        if self.closes_at <= self.opens_at:
            raise ValueError("closes_at must be later than opens_at")
        if not self.question_text or not self.question_text.strip():
            raise ValueError("question_text cannot be empty")


class PollOption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poll = models.ForeignKey(Poll, related_name="options", on_delete=models.CASCADE)
    option_text = models.CharField(max_length=200)
    option_order = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("poll", "option_order")


class PollResponse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poll = models.ForeignKey(Poll, related_name="responses", on_delete=models.CASCADE)
    option = models.ForeignKey(PollOption, related_name="responses", on_delete=models.CASCADE)
    participant_token_hash = models.CharField(max_length=128)
    submitted_at = models.DateTimeField(auto_now_add=True)
    cooldown_expires_at = models.DateTimeField()
    retention_delete_after = models.DateTimeField()

    @staticmethod
    def retention_deadline() -> timezone.datetime:
        return timezone.now() + timedelta(days=365)


class PollReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poll = models.ForeignKey(Poll, related_name="reviews", on_delete=models.CASCADE)
    reviewer_user_id = models.CharField(max_length=150)
    rating = models.PositiveSmallIntegerField()
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    retention_delete_after = models.DateTimeField(default=PollResponse.retention_deadline)
