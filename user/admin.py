from django.contrib import admin
from .models import AuditLogin


@admin.register(AuditLogin)
class AuditLoginAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_time', 'id')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    list_filter = ('login_time',)
    ordering = ('-login_time',)

    readonly_fields = ('id', 'user', 'login_time')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False