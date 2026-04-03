from django.contrib import admin
from .models import Team, Venue, Match, MatchResult

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "fifa_code", "group_code")
    search_fields = ("name", "fifa_code")

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "country", "timezone")
    search_fields = ("name", "city", "country")

class MatchResultInline(admin.StackedInline):
    model = MatchResult
    extra = 0

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("number", "tournament", "stage", "home_team", "away_team", "kickoff_at", "status")
    list_filter = ("tournament", "stage", "status")
    search_fields = ("home_team__name", "away_team__name")
    inlines = [MatchResultInline]
