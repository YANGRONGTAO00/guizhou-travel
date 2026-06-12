from django.contrib import admin

from .models import Feature, Region, ScenicSpot, SpotProfile


class SpotProfileInline(admin.StackedInline):
    model = SpotProfile
    extra = 0


@admin.register(ScenicSpot)
class ScenicSpotAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "category", "ticket_price", "rating", "is_world_heritage")
    list_filter = ("region", "category", "is_world_heritage", "features")
    search_fields = ("name", "address", "short_description")
    filter_horizontal = ("features",)
    inlines = [SpotProfileInline]


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(SpotProfile)
class SpotProfileAdmin(admin.ModelAdmin):
    list_display = ("spot", "best_season", "suggested_hours")

# Register your models here.
