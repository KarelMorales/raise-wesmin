from wagtail_modeladmin.options import (
    ModelAdmin, modeladmin_register
)
from .models import LinkCategory, UsefulLink

class LinkCategoryAdmin(ModelAdmin):
    """Link Category admin"""
    model = LinkCategory
    menu_label = "Link Categories"
    menu_icon = "folder"
    menu_order = 300
    add_to_settings_menu = True
    list_display = ("name", "slug", "sort_order")
    list_filter = ("name",)
    search_fields = ("name", "description")

class UsefulLinkAdmin(ModelAdmin):
    """Useful Link admin"""
    model = UsefulLink
    menu_label = "Useful Links"
    menu_icon = "link"
    menu_order = 310
    add_to_settings_menu = True
    list_display = ("title", "category", "is_featured", "sort_order")
    list_filter = ("category", "is_featured")
    search_fields = ("title", "description", "url")

# Register both admins
modeladmin_register(LinkCategoryAdmin)
modeladmin_register(UsefulLinkAdmin)