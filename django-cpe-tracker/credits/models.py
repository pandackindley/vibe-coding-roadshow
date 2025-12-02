from django.db import models


from django.conf import settings


class CPEExperience(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	title = models.CharField(max_length=200, default="Untitled Experience")
	details = models.TextField()
	credit_hours = models.DecimalField(max_digits=4, decimal_places=2)
	date_accomplished = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user.username}: {self.title} ({self.credit_hours} hrs)"
