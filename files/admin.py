from django.contrib import admin

from . import models


@admin.register(models.Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ["file_url", "params", "create_at"]
    list_display_links = ["file_url", "params", "create_at"]
