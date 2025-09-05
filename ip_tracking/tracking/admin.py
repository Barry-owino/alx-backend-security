from django.contrib import admin
from .models import RequestLog

@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "path", "timestamp")
    list_filter = ("ip_address", "timestamp")
    search_fields = ("ip_address", "path")
