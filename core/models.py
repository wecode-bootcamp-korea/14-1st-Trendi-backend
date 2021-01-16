from django.db import models

class TimeStampedModel(models.Model):
    models.DurationField
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, editable=True)

    class Meta:
        abstract = True
