from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
import csv
from datetime import datetime
from .models_brochure import BrochureDownload

@admin.register(BrochureDownload)
class BrochureDownloadAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'email', 'phone', 'course', 'downloaded_at', 'ip_address')
    list_filter = ('course', 'downloaded_at')
    search_fields = ('user_name', 'email', 'phone')
    date_hierarchy = 'downloaded_at'
    readonly_fields = ('downloaded_at', 'ip_address')
    actions = ['export_as_csv']
    list_per_page = 50  # Number of records per page
    list_select_related = ('course', 'brochure')  # Optimize queries
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']  # Remove delete action
        return actions

    def export_as_csv(self, request, queryset):
        if not request.user.is_superuser:
            raise PermissionDenied
            
        meta = self.model._meta
        field_names = ['user_name', 'email', 'phone', 'course', 'brochure', 'ip_address', 'downloaded_at']
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=brochure_downloads_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = [
                obj.user_name,
                obj.email,
                obj.phone,
                obj.course.name,
                obj.brochure.title,
                obj.ip_address,
                obj.downloaded_at.strftime("%Y-%m-%d %H:%M:%S")
            ]
            writer.writerow(row)
        
        return response
    
    export_as_csv.short_description = "Export selected downloads as CSV"

    def has_view_permission(self, request, obj=None):
        # Only superusers can view the records
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return False  # Make entries read-only

    def has_module_permission(self, request):
        # Only superusers can see this module in admin
        return request.user.is_superuser