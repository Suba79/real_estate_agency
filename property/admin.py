from django.contrib import admin

from .models import Complaint, Flat, Owner


@admin.register(Flat)
class FlatAdmin(admin.ModelAdmin):
    search_fields = (
        'town',
        'address',
        'owners__full_name',
        'owners__phonenumber',
        'owners__pure_phone',
    )
    readonly_fields = ('created_at',)

    list_display = (
        'address',
        'price',
        'new_building',
        'construction_year',
        'town',
    )
    list_editable = ('new_building',)
    list_filter = ('new_building',)
    raw_id_fields = ('liked_by',)


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    raw_id_fields = ('flats',)


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', 'flat')