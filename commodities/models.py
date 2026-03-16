from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images.widgets import AdminImageChooser
from django.db.models import Q

class CommodityCategory(models.Model):
    """Category for commodities (Agriculture, Aquatic, Natural Resources)"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=20, blank=True, help_text="Category color (e.g., '#4CAF50' or 'green')")
    icon = models.CharField(max_length=50, blank=True, default="tree")
    sort_order = models.IntegerField(default=0)
    
    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('description'),
        FieldPanel('color'),
        FieldPanel('icon'),
        FieldPanel('sort_order'),
    ]
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name_plural = "Commodity Categories"

class Commodity(models.Model):
    """Individual commodity item"""
    name = models.CharField(max_length=200)
    scientific_name = models.CharField(max_length=200, blank=True, help_text="Scientific name if applicable")
    category = models.ForeignKey(
        CommodityCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='commodities'
    )
    summary = models.TextField(help_text="Brief description of the commodity")
    description = RichTextField(blank=True)
    
    # Images
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Main commodity image"
    )
    icon_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Small icon/image for cards"
    )
    
    # Details
    growing_seasons = models.CharField(max_length=200, blank=True)
    harvest_period = models.CharField(max_length=200, blank=True)
    market_value = models.CharField(max_length=100, blank=True, help_text="e.g., '₱50-80/kg'")
    
    # Stats
    resource_count = models.IntegerField(default=0, help_text="Number of resources available")
    is_featured = models.BooleanField(default=False)
    is_recently_updated = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    panels = [
        FieldPanel('name'),
        FieldPanel('scientific_name'),
        FieldPanel('category'),
        FieldPanel('summary'),
        FieldPanel('description'),
        MultiFieldPanel([
            FieldPanel('main_image', widget=AdminImageChooser),
            FieldPanel('icon_image', widget=AdminImageChooser),
        ], heading="Images"),
        MultiFieldPanel([
            FieldPanel('growing_seasons'),
            FieldPanel('harvest_period'),
            FieldPanel('market_value'),
        ], heading="Commodity Details"),
        MultiFieldPanel([
            FieldPanel('resource_count'),
            FieldPanel('is_featured'),
            FieldPanel('is_recently_updated'),
            FieldPanel('sort_order'),
        ], heading="Status"),
    ]
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name_plural = "Commodities"

class CommodityIndexPage(Page):
    """Main page for commodities"""
    hero_title = models.CharField(max_length=200, blank=True, default="AANR Commodities")
    hero_subtitle = models.TextField(blank=True, default="Explore our collection of Agriculture, Aquatic, and Natural Resources commodities. Find detailed information, market insights, and best practices for each commodity.")
    
    # Background image for hero
    hero_background = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Background image for hero section"
    )
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
            FieldPanel('hero_background', widget=AdminImageChooser),
        ], heading="Hero Section"),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        
        # Get all categories
        context['categories'] = CommodityCategory.objects.all()
        
        # Get filter from URL
        category_slug = request.GET.get('category', '')
        search_query = request.GET.get('q', '')
        
        context['current_category'] = category_slug or 'all'
        
        # Base queryset
        commodities = Commodity.objects.all()
        
        # Apply category filter
        if category_slug and category_slug != 'all':
            commodities = commodities.filter(category__slug=category_slug)
        
        # Apply search
        if search_query:
            commodities = commodities.filter(
                Q(name__icontains=search_query) |
                Q(scientific_name__icontains=search_query) |
                Q(summary__icontains=search_query)
            )
            context['search_query'] = search_query
        
        context['commodities'] = commodities
        context['total_commodities'] = commodities.count()
        context['featured_commodities'] = Commodity.objects.filter(is_featured=True)[:4]
        
        return context