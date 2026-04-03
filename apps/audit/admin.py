from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "actor", "method", "path", "status_code")
    list_filter = ("status_code", "method")
    search_fields = ("path", "actor__username")
