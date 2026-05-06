from django.contrib import admin
from .models import *

# =========================
# BASE ADMIN
# =========================
class BaseAdmin(admin.ModelAdmin):
    list_per_page = 25
    readonly_fields = (
        'created_by','created_at',
        'updated_by','updated_at',
        'deleted_by','deleted_at'
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        obj.save()

    def get_queryset(self, request):
        return super().get_queryset(request).filter(deleted_at__isnull=True)

    def delete_model(self, request, obj):
        obj.soft_delete(request.user)


# =========================
# STATUS VOTE
# =========================
@admin.register(status_vote)
class StatusVoteAdmin(BaseAdmin):
    list_display = ('data_lg', 'is_open', 'is_close', 'date_loke', 'date_close')
    list_filter = ('is_open', 'is_close', 'data_lg')
    search_fields = ('data_lg__year',)


# =========================
# VOTING PLACE
# =========================
@admin.register(VotingPlace)
class VotingPlaceAdmin(BaseAdmin):
    list_display = ('name', 'municipality', 'administrativepost', 'village', 'aldeia', 'code')
    list_filter = ('municipality', 'administrativepost', 'village')
    search_fields = ('name', 'code')


# =========================
# INLINE ATTACHMENT
# =========================
class VotingAttachmentInline(admin.TabularInline):
    model = VotingAttachment
    extra = 1


# =========================
# VOTING RESULT (MAIN)
# =========================
@admin.register(VotingResult)
class VotingResultAdmin(BaseAdmin):
    list_display = (
        'membro',
        'voting_place',
        'total_votes',
        'latitude',
        'longitude',
        'submitted_at'
    )

    list_filter = ('voting_place', 'submitted_at')
    search_fields = ('membro__name', 'voting_place__name')
    readonly_fields = ('uuid', 'submitted_at')

    inlines = [VotingAttachmentInline]


# =========================
# ATTACHMENT (OPTIONAL VIEW)
# =========================
@admin.register(VotingAttachment)
class VotingAttachmentAdmin(BaseAdmin):
    list_display = ('voting_result', 'image')
    search_fields = ('voting_result__membro__name',)