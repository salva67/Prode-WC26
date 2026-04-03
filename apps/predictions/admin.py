from django.contrib import admin
from .models import Prediction, LeaderboardEntry

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ("user", "match", "home_score", "away_score", "points_awarded")
    list_filter = ("match__tournament",)
    search_fields = ("user__username", "match__home_team__name", "match__away_team__name")

@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ("group", "user", "points_total", "exact_hits", "correct_outcomes")
