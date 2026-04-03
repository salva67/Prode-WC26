from django.db import models
from django.db.models import Exists, OuterRef
from django.utils import timezone

class MatchQuerySet(models.QuerySet):
    def open_for_predictions(self):
        return self.select_related("home_team", "away_team", "venue", "stage", "tournament").filter(lock_at__gt=timezone.now(), status="scheduled").order_by("kickoff_at")

    def pending_for_user(self, user):
        from apps.predictions.models import Prediction
        subquery = Prediction.objects.filter(user=user, match=OuterRef("pk"))
        return self.open_for_predictions().annotate(has_prediction=Exists(subquery)).filter(has_prediction=False)
