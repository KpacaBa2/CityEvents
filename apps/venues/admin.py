from django.contrib import admin

from apps.venues.models import Amenity, Venue, VenuePhoto


class VenuePhotoInline(admin.TabularInline):
    model = VenuePhoto
    extra = 1


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'capacity')
    list_filter = ('city',)
    search_fields = ('name', 'address')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [VenuePhotoInline]
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'city', 'address')}),
        ('Details', {'fields': ('capacity', 'description', 'map_url', 'amenities', 'cover')}),
    )


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(VenuePhoto)
class VenuePhotoAdmin(admin.ModelAdmin):
    list_display = ('venue', 'caption', 'created_at')
    search_fields = ('venue__name', 'caption')
