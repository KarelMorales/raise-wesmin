from wagtail_modeladmin.options import (
    ModelAdmin, modeladmin_register
)
from .models import CommodityCategory, Commodity

class CommodityCategoryAdmin(ModelAdmin):
    """Commodity Category admin"""
    model = CommodityCategory
    menu_label = "Commodity Categories"
    menu_icon = "list-ul"
    menu_order = 600
    add_to_settings_menu = True
    list_display = ("name", "slug", "color", "sort_order")
    list_filter = ("name",)
    search_fields = ("name", "description")

class CommodityAdmin(ModelAdmin):
    """Commodity admin"""
    model = Commodity
    menu_label = "Commodities"
    menu_icon = "site"
    menu_order = 610
    add_to_settings_menu = True
    list_display = ("name", "category", "resource_count", "is_featured", "is_recently_updated")
    list_filter = ("category", "is_featured", "is_recently_updated")
    search_fields = ("name", "scientific_name", "summary")

# Register admins
modeladmin_register(CommodityCategoryAdmin)
modeladmin_register(CommodityAdmin)