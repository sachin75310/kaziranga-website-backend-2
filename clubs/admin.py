from django.contrib import admin
from .models import Community


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'head', 'member_count', 'status', 'theme', 'created_on']
    list_filter = ['status', 'theme', 'created_on']
    search_fields = ['name', 'head', 'description']
    ordering = ['-created_on']
    readonly_fields = ['created_on', 'updated_on']
