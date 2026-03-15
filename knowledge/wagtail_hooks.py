from wagtail_modeladmin.options import (
    ModelAdmin, modeladmin_register
)
from .models import ResourceCategory, KnowledgeResource

class ResourceCategoryAdmin(ModelAdmin):
    """Resource Category admin"""
    model = ResourceCategory
    menu_label = "Resource Categories"
    menu_icon = "list-ul"
    menu_order = 500
    add_to_settings_menu = True
    list_display = ("name", "slug", "sort_order")
    list_filter = ("name",)
    search_fields = ("name", "description")

class KnowledgeResourceAdmin(ModelAdmin):
    """Knowledge Resource admin"""
    model = KnowledgeResource
    menu_label = "Knowledge Resources"
    menu_icon = "doc-full"
    menu_order = 510
    add_to_settings_menu = True
    list_display = ("title", "resource_type", "category", "is_featured", "publication_date")
    list_filter = ("resource_type", "category", "is_featured")
    search_fields = ("title", "summary", "authors")

# Register admins
modeladmin_register(ResourceCategoryAdmin)
modeladmin_register(KnowledgeResourceAdmin)