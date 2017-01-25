from django.contrib import admin
from .models import ShortUrl


class ShortUrlAdmin(admin.ModelAdmin):
    actions = None
    list_display = ['pk', 'short_url', 'full_url', 'visit_count', 'date_created']
    search_fields = ['short_url', 'full_url']
    list_filter = ['visit_count']

    def has_add_permission(self, request):
        """Disable admin from creating(adding) short urls."""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Disable admin from deleting short urls."""
        return False

admin.site.register(ShortUrl, ShortUrlAdmin)