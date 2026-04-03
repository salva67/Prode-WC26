from django.conf import settings
from django.db import models
from apps.matches.models import Match, Team
from apps.groups.models import PrivateGroup

class Prediction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="predictions")
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="predictions")
    home_score = models.PositiveSmallIntegerField()
    away_score = models.PositiveSmallIntegerField()
    penalty_winner = models.ForeignKey(Team, on_delete=models.PROTECT, null=True, blank=True)
    points_awarded = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "match")
        ordering = ("match__kickoff_at",)

    def __str__(self):
        return f"{self.user} -> {self.match}"

class LeaderboardEntry(models.Model):
    group = models.ForeignKey(PrivateGroup, on_delete=models.CASCADE, related_name="leaderboard_entries")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="leaderboard_entries")
    points_total = models.IntegerField(default=0)
    exact_hits = models.PositiveIntegerField(default=0)
    correct_outcomes = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("group", "user")

    def __str__(self):
        return f"{self.group} - {self.user}"
