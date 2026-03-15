from wagtail_modeladmin.options import (
    ModelAdmin, modeladmin_register
)
from .models import Category, Thread, Reply

class CategoryAdmin(ModelAdmin):
    """Category admin"""
    model = Category
    menu_label = "Forum Categories"
    menu_icon = "list-ul"
    menu_order = 400
    add_to_settings_menu = True
    list_display = ("name", "slug", "thread_count", "sort_order")
    list_filter = ("name",)
    search_fields = ("name", "description")

class ThreadAdmin(ModelAdmin):
    """Thread admin"""
    model = Thread
    menu_label = "Forum Threads"
    menu_icon = "chat"
    menu_order = 410
    add_to_settings_menu = True
    list_display = ("title", "category", "created_by_name", "created_at", "reply_count")
    list_filter = ("category", "is_pinned", "is_closed")
    search_fields = ("title", "content")

class ReplyAdmin(ModelAdmin):
    """Reply admin"""
    model = Reply
    menu_label = "Forum Replies"
    menu_icon = "comment"
    menu_order = 420
    add_to_settings_menu = True
    list_display = ("thread", "created_by_name", "created_at")
    search_fields = ("content",)

# Register admins
modeladmin_register(CategoryAdmin)
modeladmin_register(ThreadAdmin)
modeladmin_register(ReplyAdmin)