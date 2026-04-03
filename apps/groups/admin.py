from django.contrib import admin
from .models import PrivateGroup, GroupMembership

class GroupMembershipInline(admin.TabularInline):
    model = GroupMembership
    extra = 0

@admin.register(PrivateGroup)
class PrivateGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "tournament", "owner", "invite_code")
    search_fields = ("name", "invite_code", "owner__username")
    inlines = [GroupMembershipInline]
