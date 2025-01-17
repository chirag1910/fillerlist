from django.contrib import admin
from analytics.models import Analytic

@admin.register(Analytic)
class AnalyticAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'time')
    search_fields = ('ip_address',)
    list_filter = ('time',)
    ordering = ('-time',)
    date_hierarchy = 'time'
    list_per_page = 50
