from django.contrib import admin
from .models import TrafficLog

# Register your models here.

@admin.register(TrafficLog)
class TrafficLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'service_name', 'method', 'path', 'status_code', 'remote_ip', 'execution_duration')
    list_filter = ('service_name', 'method', 'status_code')
    search_fields = ('path', 'remote_ip','service_name')

    readonly_fields = ('timestamp','service_name', 'method', 'path', 'status_code', 'remote_ip', 'execution_duration','payload')