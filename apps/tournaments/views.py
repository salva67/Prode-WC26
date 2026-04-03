from django.views.generic import DetailView, ListView
from .models import Tournament

class TournamentListView(ListView):
    model = Tournament
    template_name = "tournaments/list.html"

class TournamentDetailView(DetailView):
    model = Tournament
    slug_field = "slug"
    slug_url_kwarg = "slug"
    template_name = "tournaments/detail.html"
