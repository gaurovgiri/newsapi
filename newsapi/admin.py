from django.contrib import admin
from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """Admin interface for News model."""
    
    list_display = ('title', 'source', 'language', 'created_at')
    list_filter = ('source', 'language', 'created_at')
    search_fields = ('title', 'summary', 'source')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Article Information', {
            'fields': ('title', 'summary', 'source', 'language')
        }),
        ('URLs', {
            'fields': ('source_url', 'image_url')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
