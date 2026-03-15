from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images.widgets import AdminImageChooser  # Changed from ImageChooserPanel
from wagtail.search import index
from django.db.models import Q

class ResourceCategory(models.Model):
    """Category for knowledge resources (Publications, News, Events, etc.)"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, default="file-text")
    sort_order = models.IntegerField(default=0)
    
    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('description'),
        FieldPanel('icon'),
        FieldPanel('sort_order'),
    ]
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name_plural = "Resource Categories"

class KnowledgeResource(models.Model):
    """Individual knowledge resource item"""
    RESOURCE_TYPES = [
        ('publication', 'Publication'),
        ('news', 'News'),
        ('event', 'Event'),
        ('project', 'Project'),
        ('technology', 'Technology'),
        ('training', 'Training/Seminar'),
        ('webinar', 'Webinar'),
        ('policy', 'Policy'),
        ('map', 'Map'),
        ('media', 'Media'),
        ('product', 'Product'),
        ('info_system', 'Information System/Website'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=300)
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPES, default='publication')
    category = models.ForeignKey(
        ResourceCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resources'
    )
    summary = models.TextField(blank=True, help_text="Brief description of the resource")
    content = RichTextField(blank=True)
    
    # File upload or external link
    file = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    external_url = models.URLField(blank=True, help_text="Link to external resource if no file")
    
    # Metadata
    authors = models.CharField(max_length=300, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    organization = models.CharField(max_length=200, blank=True)
    
    # Image/thumbnail
    thumbnail = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    # Status
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    panels = [
        FieldPanel('title'),
        FieldPanel('resource_type'),
        FieldPanel('category'),
        FieldPanel('summary'),
        FieldPanel('content'),
        MultiFieldPanel([
            FieldPanel('file'),
            FieldPanel('external_url'),
        ], heading="Resource File/Link"),
        MultiFieldPanel([
            FieldPanel('authors'),
            FieldPanel('publication_date'),
            FieldPanel('organization'),
        ], heading="Metadata"),
        FieldPanel('thumbnail', widget=AdminImageChooser),  # Fixed here
        MultiFieldPanel([
            FieldPanel('is_featured'),
            FieldPanel('is_published'),
            FieldPanel('sort_order'),
        ], heading="Status"),
    ]
    
    def __str__(self):
        return self.title
    
    def get_resource_url(self):
        """Return either the file URL or external URL"""
        if self.file:
            return self.file.url
        return self.external_url
    
    class Meta:
        ordering = ['-is_featured', 'sort_order', '-created_at']

class KnowledgeIndexPage(Page):
    """Main page for knowledge resources"""
    hero_title = models.CharField(max_length=200, blank=True, default="AANR Knowledge Resources")
    hero_subtitle = models.TextField(blank=True, default="Explore our comprehensive collection of resources in Agriculture, Aquatic, and Natural Resources sectors.")
    intro = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
        ], heading="Hero Section"),
        FieldPanel('intro'),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        
        # Get all categories
        context['categories'] = ResourceCategory.objects.all()
        
        # Get filter from URL
        category_slug = request.GET.get('category', '')
        resource_type = request.GET.get('type', '')
        search_query = request.GET.get('q', '')
        
        context['current_category'] = category_slug or 'all'
        context['current_type'] = resource_type
        
        # Base queryset - only published resources
        resources = KnowledgeResource.objects.filter(is_published=True)
        
        # Apply category filter
        if category_slug and category_slug != 'all':
            resources = resources.filter(category__slug=category_slug)
        
        # Apply resource type filter
        if resource_type:
            resources = resources.filter(resource_type=resource_type)
        
        # Apply search
        if search_query:
            resources = resources.filter(
                Q(title__icontains=search_query) |
                Q(summary__icontains=search_query) |
                Q(authors__icontains=search_query)
            )
            context['search_query'] = search_query
        
        context['resources'] = resources
        context['total_resources'] = resources.count()
        context['featured_resources'] = KnowledgeResource.objects.filter(is_published=True, is_featured=True)[:3]
        
        # Get unique resource types for filter dropdown
        context['resource_types'] = KnowledgeResource.RESOURCE_TYPES
        
        return context