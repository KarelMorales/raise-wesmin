from wagtail_modeladmin.options import (
    ModelAdmin, modeladmin_register
)
from .models import FAQTopic, FAQ

class FAQTopicAdmin(ModelAdmin):
    """FAQ Topic admin"""
    model = FAQTopic
    menu_label = "FAQ Topics"
    menu_icon = "tag"
    menu_order = 200
    add_to_settings_menu = True
    list_display = ("name", "slug", "sort_order")
    list_filter = ("name",)
    search_fields = ("name", "description")

class FAQAdmin(ModelAdmin):
    """FAQ admin"""
    model = FAQ
    menu_label = "FAQs"
    menu_icon = "help"
    menu_order = 210
    add_to_settings_menu = True
    list_display = ("question", "topic", "is_featured", "sort_order")
    list_filter = ("topic", "is_featured")
    search_fields = ("question", "answer")

# Register both admins
modeladmin_register(FAQTopicAdmin)
modeladmin_register(FAQAdmin)