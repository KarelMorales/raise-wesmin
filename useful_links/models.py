from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index

class LinkCategory(models.Model):
    """Category for organizing useful links"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, default="link")
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
        verbose_name = "Link Category"
        verbose_name_plural = "Link Categories"

class UsefulLink(models.Model):
    """Individual useful link"""
    title = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        LinkCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='links'
    )
    icon = models.CharField(max_length=50, blank=True, help_text="Bootstrap icon class (e.g., bi-file-pdf)")
    is_featured = models.BooleanField(default=False)
    opens_in_new_tab = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    panels = [
        FieldPanel('title'),
        FieldPanel('url'),
        FieldPanel('description'),
        FieldPanel('category'),
        FieldPanel('icon'),
        FieldPanel('is_featured'),
        FieldPanel('opens_in_new_tab'),
        FieldPanel('sort_order'),
    ]
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['sort_order', 'title']

class UsefulLinksIndexPage(Page):
    """Main page for displaying useful links"""
    intro = RichTextField(blank=True)
    featured_title = models.CharField(max_length=200, blank=True, default="Useful Links")
    featured_subtitle = models.CharField(max_length=200, blank=True, default="Curated collection of external resources and partner organizations")
    
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        MultiFieldPanel([
            FieldPanel('featured_title'),
            FieldPanel('featured_subtitle'),
        ], heading="Featured Section"),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        # Get all categories with their links
        context['categories'] = LinkCategory.objects.all()
        context['total_links'] = UsefulLink.objects.count()
        context['featured_links'] = UsefulLink.objects.filter(is_featured=True)
        
        # Get filter from URL
        category_slug = request.GET.get('category', '')
        search_query = request.GET.get('q', '')
        
        # Base queryset
        links = UsefulLink.objects.all()
        
        # Apply category filter
        if category_slug and category_slug != 'all':
            links = links.filter(category__slug=category_slug)
            context['current_category'] = category_slug
        else:
            context['current_category'] = 'all'
        
        # Apply search filter
        if search_query:
            links = links.filter(
                models.Q(title__icontains=search_query) |
                models.Q(description__icontains=search_query) |
                models.Q(url__icontains=search_query)
            )
            context['search_query'] = search_query
        
        context['links'] = links
        return context