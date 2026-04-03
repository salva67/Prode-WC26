from django.db import models
from django.utils import timezone
from apps.tournaments.models import Tournament, Stage
from .managers import MatchQuerySet

class Team(models.Model):
    name = models.CharField(max_length=120)
    short_name = models.CharField(max_length=40)
    fifa_code = models.CharField(max_length=3, unique=True)
    group_code = models.CharField(max_length=2, blank=True)
    flag_emoji = models.CharField(max_length=8, blank=True)
    flag_image = models.CharField(max_length=255, blank=True, help_text="Ruta estática o URL")

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

class Venue(models.Model):
    name = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    timezone = models.CharField(max_length=50, default="UTC")
    address = models.CharField(max_length=255, blank=True)
    capacity = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("country", "city", "name")

    def __str__(self):
        return f"{self.name} - {self.city}"

class Match(models.Model):
    STATUS_CHOICES = (
        ("scheduled", "Programado"),
        ("locked", "Bloqueado"),
        ("live", "En vivo"),
        ("finished", "Finalizado"),
    )
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="matches")
    stage = models.ForeignKey(Stage, on_delete=models.PROTECT, related_name="matches")
    group_code = models.CharField(max_length=2, blank=True)
    number = models.PositiveIntegerField()
    home_team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name="home_matches")
    away_team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name="away_matches")
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT, related_name="matches")
    kickoff_at = models.DateTimeField()
    lock_at = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="scheduled")

    objects = MatchQuerySet.as_manager()

    class Meta:
        ordering = ("kickoff_at",)
        unique_together = ("tournament", "number")

    def __str__(self):
        return f"#{self.number} {self.home_team} vs {self.away_team}"

    @property
    def can_predict(self):
        return self.lock_at > timezone.now() and self.status == "scheduled"

class MatchResult(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE, related_name="result")
    home_score = models.PositiveSmallIntegerField()
    away_score = models.PositiveSmallIntegerField()
    home_score_et = models.PositiveSmallIntegerField(null=True, blank=True)
    away_score_et = models.PositiveSmallIntegerField(null=True, blank=True)
    home_penalties = models.PositiveSmallIntegerField(null=True, blank=True)
    away_penalties = models.PositiveSmallIntegerField(null=True, blank=True)
    winner = models.ForeignKey(Team, on_delete=models.PROTECT, related_name="won_results", null=True, blank=True)
    published_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Resultado {self.match}"
