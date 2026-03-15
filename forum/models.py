from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

class Category(models.Model):
    """Forum topic categories (Rice, Eggplant, Fish, etc.)"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, default="chat")
    thread_count = models.IntegerField(default=0)
    sort_order = models.IntegerField(default=0)
    
    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('description'),
        FieldPanel('icon'),
        FieldPanel('thread_count'),
        FieldPanel('sort_order'),
    ]
    
    def __str__(self):
        return self.name
    
    def update_thread_count(self):
        self.thread_count = self.threads.count()
        self.save()
    
    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name_plural = "Categories"

class Thread(ClusterableModel):  # Changed: Now inherits from ClusterableModel
    """Discussion thread/question"""
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='threads'
    )
    title = models.CharField(max_length=300)
    content = RichTextField()
    created_by_name = models.CharField(max_length=100, blank=True)
    created_by_email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    is_pinned = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    
    panels = [
        FieldPanel('category'),
        FieldPanel('title'),
        FieldPanel('content'),
        FieldPanel('created_by_name'),
        FieldPanel('created_by_email'),
        FieldPanel('is_pinned'),
        FieldPanel('is_closed'),
    ]
    
    def __str__(self):
        return self.title
    
    def reply_count(self):
        return self.replies.count()
    
    class Meta:
        ordering = ['-is_pinned', '-created_at']

class Reply(models.Model):  # No change needed here
    """Reply to a thread"""
    thread = ParentalKey(
        Thread,  # Now Thread is ClusterableModel, so this works
        on_delete=models.CASCADE,
        related_name='replies'
    )
    content = RichTextField()
    created_by_name = models.CharField(max_length=100, blank=True)
    created_by_email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    panels = [
        FieldPanel('content'),
        FieldPanel('created_by_name'),
        FieldPanel('created_by_email'),
    ]
    
    def __str__(self):
        return f"Reply to {self.thread.title} by {self.created_by_name}"
    
    class Meta:
        ordering = ['created_at']

class ForumIndexPage(Page):
    """Main forum page listing all categories and recent threads"""
    intro = RichTextField(blank=True)
    hero_title = models.CharField(max_length=200, blank=True, default="AANR Knowledge Community Forum")
    hero_subtitle = models.CharField(max_length=300, blank=True, default="Join the conversation and grow your knowledge in Agriculture, Aquatic, and Natural Resources!")
    
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
        ], heading="Hero Section"),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        
        # Get all categories
        context['categories'] = Category.objects.all()
        
        # Get filter from URL
        category_slug = request.GET.get('category', '')
        context['current_category'] = category_slug or 'all'
        
        # Base queryset for threads
        threads = Thread.objects.all()
        
        # Apply category filter
        if category_slug and category_slug != 'all':
            threads = threads.filter(category__slug=category_slug)
        
        context['threads'] = threads
        context['total_threads'] = threads.count()
        
        return context