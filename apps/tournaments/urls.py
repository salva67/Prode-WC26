from django.urls import path
from .views import TournamentListView, TournamentDetailView

urlpatterns = [
    path("", TournamentListView.as_view(), name="tournament_list"),
    path("<slug:slug>/", TournamentDetailView.as_view(), name="tournament_detail"),
]
