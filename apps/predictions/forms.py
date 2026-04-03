from django import forms
from .models import Prediction

class PredictionForm(forms.ModelForm):
    class Meta:
        model = Prediction
        fields = ("home_score", "away_score", "penalty_winner")

    def __init__(self, *args, **kwargs):
        match = kwargs.pop("match", None)
        super().__init__(*args, **kwargs)
        self.fields["home_score"].widget.attrs.update({"min": 0})
        self.fields["away_score"].widget.attrs.update({"min": 0})
        if match:
            self.fields["penalty_winner"].queryset = match.home_team.__class__.objects.filter(pk__in=[match.home_team_id, match.away_team_id])
