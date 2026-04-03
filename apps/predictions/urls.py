from django.urls import path
from .views import MyPredictionsView, SavePredictionView

urlpatterns = [
    path("mine/", MyPredictionsView.as_view(), name="my_predictions"),
    path("save/<int:match_id>/", SavePredictionView.as_view(), name="save_prediction"),
]
