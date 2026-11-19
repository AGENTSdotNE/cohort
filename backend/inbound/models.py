from django.db import models
from django.db.models import F


class InboundItem(models.Model):
    reference = models.CharField(max_length=50, unique=True)
    received_raw = models.CharField(max_length=100, blank=True)
    received_at = models.DateTimeField(null=True, blank=True)
    channel = models.CharField(max_length=50)
    sender = models.CharField(max_length=200, blank=True)
    subject = models.CharField(max_length=300, blank=True)
    message = models.TextField(blank=True)
    logged_by = models.CharField(max_length=100, blank=True)

    class Meta:
        # Items with an unknown date come first because they need a human to check them.
        ordering = [F('received_at').desc(nulls_first=True), 'reference']

    def __str__(self):
        return self.reference
