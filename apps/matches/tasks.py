from celery import shared_task
from django.utils import timezone
from .models import Match

@shared_task
def lock_due_matches():
    Match.objects.filter(status="scheduled", lock_at__lte=timezone.now()).update(status="locked")

@shared_task
def mark_live_matches():
    now = timezone.now()
    Match.objects.filter(status="locked", kickoff_at__lte=now, result__isnull=True).update(status="live")
