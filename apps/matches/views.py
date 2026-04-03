from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, redirect, render
from .forms import MatchResultForm
from .models import Match, MatchResult
from apps.scoring.tasks import recalculate_match_leaderboard_task

class FixtureListView(ListView):
    model = Match
    template_name = "matches/fixture.html"
    paginate_by = 50

    def get_queryset(self):
        qs = Match.objects.select_related("home_team", "away_team", "venue", "stage", "tournament")
        stage_code = self.request.GET.get("stage")
        if stage_code:
            qs = qs.filter(stage__code=stage_code)
        return qs

@staff_member_required
def publish_result(request, pk):
    match = get_object_or_404(Match.objects.select_related("home_team", "away_team"), pk=pk)
    result, _ = MatchResult.objects.get_or_create(match=match)
    if request.method == "POST":
        form = MatchResultForm(request.POST, instance=result)
        if form.is_valid():
            form.save()
            match.status = "finished"
            match.save(update_fields=["status"])
            recalculate_match_leaderboard_task.delay(match.id)
            messages.success(request, "Resultado publicado y scoring encolado.")
            return redirect("fixture")
    else:
        form = MatchResultForm(instance=result)
    return render(request, "matches/publish_result.html", {"match": match, "form": form})
