from django.contrib import admin
from .models import Tournament, Stage

class StageInline(admin.TabularInline):
    model = Stage
    extra = 0

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "starts_at", "ends_at")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [StageInline]
