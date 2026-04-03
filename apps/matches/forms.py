from django import forms
from .models import MatchResult

class MatchResultForm(forms.ModelForm):
    class Meta:
        model = MatchResult
        fields = (
            "home_score",
            "away_score",
            "home_score_et",
            "away_score_et",
            "home_penalties",
            "away_penalties",
            "winner",
        )
