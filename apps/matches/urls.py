from django.urls import path
from .views import FixtureListView, publish_result

urlpatterns = [
    path("fixture/", FixtureListView.as_view(), name="fixture"),
    path("<int:pk>/publish-result/", publish_result, name="publish_result"),
]
