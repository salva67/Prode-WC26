from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, View
from apps.matches.models import Match
from .forms import PredictionForm
from .models import Prediction

class MyPredictionsView(LoginRequiredMixin, ListView):
    template_name = "predictions/my_predictions.html"
    context_object_name = "predictions"

    def get_queryset(self):
        return Prediction.objects.filter(user=self.request.user).select_related("match", "match__home_team", "match__away_team", "match__result")

class SavePredictionView(LoginRequiredMixin, View):
    def post(self, request, match_id):
        match = get_object_or_404(Match, pk=match_id)
        if not match.can_predict:
            messages.error(request, "El partido ya está bloqueado.")
            return redirect("fixture")

        instance = Prediction.objects.filter(user=request.user, match=match).first()
        form = PredictionForm(request.POST, instance=instance, match=match)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.match = match
            obj.save()
            messages.success(request, "Pronóstico guardado.")
        else:
            messages.error(request, "No se pudo guardar el pronóstico.")
        return redirect("fixture")
