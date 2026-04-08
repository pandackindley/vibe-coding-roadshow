from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Poll",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("creator_user_id", models.CharField(max_length=150)),
                ("question_text", models.CharField(max_length=500)),
                ("status", models.CharField(choices=[("draft", "Draft"), ("published", "Published"), ("closed", "Closed"), ("archived", "Archived")], default="draft", max_length=16)),
                ("opens_at", models.DateTimeField()),
                ("closes_at", models.DateTimeField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="PollOption",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("option_text", models.CharField(max_length=200)),
                ("option_order", models.PositiveIntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("poll", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="options", to="polls.poll")),
            ],
            options={"unique_together": {("poll", "option_order")}},
        ),
        migrations.CreateModel(
            name="PollReview",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("reviewer_user_id", models.CharField(max_length=150)),
                ("rating", models.PositiveSmallIntegerField()),
                ("comments", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("retention_delete_after", models.DateTimeField()),
                ("poll", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reviews", to="polls.poll")),
            ],
        ),
        migrations.CreateModel(
            name="PollResponse",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("participant_token_hash", models.CharField(max_length=128)),
                ("submitted_at", models.DateTimeField(auto_now_add=True)),
                ("cooldown_expires_at", models.DateTimeField()),
                ("retention_delete_after", models.DateTimeField()),
                ("option", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="responses", to="polls.polloption")),
                ("poll", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="responses", to="polls.poll")),
            ],
        ),
    ]
