from celery import shared_task
from .services import recalculate_match_and_groups

@shared_task
def recalculate_match_leaderboard_task(match_id):
    recalculate_match_and_groups(match_id)
