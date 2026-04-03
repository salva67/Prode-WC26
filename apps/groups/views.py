from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, FormView, ListView, View
from .forms import CreateGroupForm, JoinGroupForm
from .models import GroupMembership, PrivateGroup
from apps.predictions.models import LeaderboardEntry

class GroupListView(LoginRequiredMixin, ListView):
    template_name = "groups/list.html"
    context_object_name = "groups"

    def get_queryset(self):
        return PrivateGroup.objects.for_user(self.request.user).select_related("tournament", "owner")

class GroupDetailView(LoginRequiredMixin, DetailView):
    model = PrivateGroup
    slug_field = "slug"
    slug_url_kwarg = "slug"
    template_name = "groups/detail.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.memberships.filter(user=self.request.user).exists():
            raise Http404("No pertenecés a este grupo.")
        return obj

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["leaderboard"] = LeaderboardEntry.objects.filter(group=self.object).select_related("user").order_by("-points_total", "-exact_hits", "user__username")
        return ctx

class GroupCreateView(LoginRequiredMixin, FormView):
    template_name = "groups/create.html"
    form_class = CreateGroupForm

    def form_valid(self, form):
        group = form.save(owner=self.request.user)
        GroupMembership.objects.get_or_create(group=group, user=self.request.user, defaults={"role": "owner"})
        messages.success(self.request, "Grupo creado correctamente.")
        return redirect("group_detail", slug=group.slug)

class GroupJoinView(LoginRequiredMixin, FormView):
    template_name = "groups/join.html"
    form_class = JoinGroupForm

    def form_valid(self, form):
        group = get_object_or_404(PrivateGroup, invite_code=form.cleaned_data["invite_code"])
        GroupMembership.objects.get_or_create(group=group, user=self.request.user, defaults={"role": "member"})
        messages.success(self.request, "Te uniste al grupo.")
        return redirect("group_detail", slug=group.slug)

class GroupJoinByCodeView(LoginRequiredMixin, View):
    def post(self, request, code):
        group = get_object_or_404(PrivateGroup, invite_code=code.upper())
        GroupMembership.objects.get_or_create(group=group, user=request.user, defaults={"role": "member"})
        messages.success(request, "Te uniste al grupo.")
        return redirect("group_detail", slug=group.slug)
