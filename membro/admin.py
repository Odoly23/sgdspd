from django.contrib import admin
from .models import *

# ================================
# BASE ADMIN
# ================================
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

    def delete_model(self, request, obj):
        obj.soft_delete(request.user)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(deleted_at__isnull=True)


# ================================
# INLINE (RELATION DI MEMBRU)
# ================================
class ContactInline(admin.StackedInline):
    model = ContactInfo
    extra = 0

class LocationInline(admin.StackedInline):
    model = LocationTL
    extra = 0

class AddressInline(admin.StackedInline):
    model = AddressOrigin
    extra = 0

class PhotoInline(admin.StackedInline):
    model = Photo
    extra = 0

class PositionInline(admin.StackedInline):
    model = MembroPosition
    extra = 0

class EducationInline(admin.TabularInline):
    model = FormalEducation
    extra = 0


# ================================
# MEMBRU ADMIN (MAIN)
# ================================
@admin.register(Membru)
class MembruAdmin(BaseAdmin):
    list_display = (
        'nu_id',
        'name',
        'sex',
        'status',
        'year',
        'get_municipality',
        'age'
    )

    search_fields = ('nu_id', 'name')
    list_filter = ('sex', 'status', 'year')

    inlines = [
        ContactInline,
        LocationInline,
        AddressInline,
        PhotoInline,
        PositionInline,
        EducationInline
    ]

    def get_municipality(self, obj):
        if hasattr(obj, 'locationtl') and obj.locationtl:
            return obj.locationtl.municipality
        return "-"
    get_municipality.short_description = "Municipiu"


# ================================
# CONTACT
# ================================
@admin.register(ContactInfo)
class ContactAdmin(BaseAdmin):
    list_display = ('membro', 'email', 'phone')
    search_fields = ('membro__name', 'email', 'phone')


# ================================
# LOCATION
# ================================
@admin.register(LocationTL)
class LocationAdmin(BaseAdmin):
    list_display = ('membro', 'municipality', 'administrativepost', 'village', 'aldeia')
    list_filter = ('municipality', 'administrativepost', 'village')
    search_fields = ('membro__name',)


# ================================
# ADDRESS
# ================================
@admin.register(AddressOrigin)
class AddressAdmin(BaseAdmin):
    list_display = ('membro', 'city', 'address')
    search_fields = ('membro__name', 'city')


# ================================
# PHOTO
# ================================
@admin.register(Photo)
class PhotoAdmin(BaseAdmin):
    list_display = ('membro', 'image')


# ================================
# EDUCATION
# ================================
@admin.register(FormalEducation)
class EducationAdmin(BaseAdmin):
    list_display = ('membro', 'educationlevel', 'university', 'graduation_year', 'is_active')
    list_filter = ('educationlevel', 'is_active')
    search_fields = ('membro__name',)


# ================================
# MEMBER USER
# ================================
@admin.register(MembroUser)
class MemberUserAdmin(BaseAdmin):
    list_display = ('membro', 'user', 'created_at')
    search_fields = ('membro__name', 'user__username')


# ================================
# POSITION
# ================================
@admin.register(MembroPosition)
class PositionAdmin(BaseAdmin):
    list_display = ('membro', 'estructure', 'position')
    list_filter = ('estructure', 'position')
    search_fields = ('membro__name',)