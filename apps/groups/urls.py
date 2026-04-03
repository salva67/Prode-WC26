from django.urls import path
from .views import GroupListView, GroupDetailView, GroupCreateView, GroupJoinView, GroupJoinByCodeView

urlpatterns = [
    path("", GroupListView.as_view(), name="group_list"),
    path("create/", GroupCreateView.as_view(), name="group_create"),
    path("join/", GroupJoinView.as_view(), name="group_join"),
    path("invite/<str:code>/", GroupJoinByCodeView.as_view(), name="group_join_code"),
    path("<slug:slug>/", GroupDetailView.as_view(), name="group_detail"),
]
