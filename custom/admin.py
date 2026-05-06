from django.contrib import admin
from .models import *

# ================================
# BASE ADMIN (REUSABLE)
# ================================
def soft_delete_selected(modeladmin, request, queryset):
    for obj in queryset:
        obj.soft_delete(request.user)
soft_delete_selected.short_description = "Soft Delete Selected"


class BaseAdmin(admin.ModelAdmin):
	actions = [soft_delete_selected]
	list_per_page = 25
	readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at', 'deleted_by', 'deleted_at')

	def save_model(self, request, obj, form, change):
		if not obj.pk:
			obj.created_by = request.user
		else:
			obj.updated_by = request.user
		obj.save()

	def get_queryset(self, request):
		return super().get_queryset(request).filter(deleted_at__isnull=True)

# ================================
# SIMPLE MASTER DATA
# ================================
@admin.register(Estructure)
class EstructureAdmin(BaseAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


@admin.register(Position)
class PositionAdmin(BaseAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(EducationLevel)
class EducationLevelAdmin(BaseAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Country)
class CountryAdmin(BaseAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


@admin.register(Municipality)
class MunicipalityAdmin(BaseAdmin):
    list_display = ('code', 'name', 'hckey')
    search_fields = ('code', 'name')
    list_filter = ('hckey',)


@admin.register(AdministrativePost)
class AdministrativePostAdmin(BaseAdmin):
    list_display = ('name', 'municipality')
    search_fields = ('name',)
    list_filter = ('municipality',)


@admin.register(Village)
class VillageAdmin(BaseAdmin):
    list_display = ('name', 'administrativepost')
    search_fields = ('name',)
    list_filter = ('administrativepost',)


@admin.register(SubVillage)
class SubVillageAdmin(BaseAdmin):
    list_display = ('name', 'village')
    search_fields = ('name',)
    list_filter = ('village',)


@admin.register(University)
class UniversityAdmin(BaseAdmin):
    list_display = ('name', 'country')
    search_fields = ('name',)
    list_filter = ('country',)


@admin.register(Faculty)
class FacultyAdmin(BaseAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(StudyProgram)
class StudyProgramAdmin(BaseAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Area)
class AreaAdmin(BaseAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Year)
class YearAdmin(BaseAdmin):
    list_display = ('year', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('year',)


@admin.register(Language)
class LanguageAdmin(BaseAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Status)
class StatusAdmin(BaseAdmin):
    list_display = ('name',)
    search_fields = ('name',)