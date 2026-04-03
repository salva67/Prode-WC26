from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from apps.groups.models import PrivateGroup
from apps.matches.models import Match
from apps.predictions.models import Prediction

class HomeView(TemplateView):
    template_name = "home.html"

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        ctx["upcoming_matches"] = Match.objects.select_related("home_team", "away_team", "venue").open_for_predictions()[:10]
        ctx["my_groups"] = PrivateGroup.objects.for_user(user)[:10]
        ctx["pending_predictions"] = Match.objects.pending_for_user(user)[:10]
        ctx["my_prediction_count"] = Prediction.objects.filter(user=user).count()
        return ctx
