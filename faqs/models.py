from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index

class FAQTopic(models.Model):
    """Topic/Category for FAQs"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, default="tag")
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
        verbose_name = "FAQ Topic"
        verbose_name_plural = "FAQ Topics"

class FAQ(models.Model):
    """Individual FAQ item"""
    question = models.CharField(max_length=500)
    answer = RichTextField()
    topic = models.ForeignKey(
        FAQTopic,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='faqs'
    )
    is_featured = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    panels = [
        FieldPanel('question'),
        FieldPanel('answer'),
        FieldPanel('topic'),
        FieldPanel('is_featured'),
        FieldPanel('sort_order'),
    ]
    
    def __str__(self):
        return self.question
    
    class Meta:
        ordering = ['sort_order', '-created_at']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

class FAQIndexPage(Page):
    """Main FAQ page that lists all FAQs"""
    intro = RichTextField(blank=True)
    featured_title = models.CharField(max_length=200, blank=True, default="Frequently Asked Questions")
    featured_subtitle = models.CharField(max_length=200, blank=True, default="Browse through our comprehensive FAQ collection")
    
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        MultiFieldPanel([
            FieldPanel('featured_title'),
            FieldPanel('featured_subtitle'),
        ], heading="Featured Section"),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        # Get all topics
        context['topics'] = FAQTopic.objects.all()
        context['total_faqs'] = FAQ.objects.count()
        
        # Get filter from URL
        topic_slug = request.GET.get('topic', '')
        search_query = request.GET.get('q', '')
        
        # Base queryset
        faqs = FAQ.objects.all()
        
        # Apply topic filter
        if topic_slug and topic_slug != 'all':
            faqs = faqs.filter(topic__slug=topic_slug)
            context['current_topic'] = topic_slug
        else:
            context['current_topic'] = 'all'
        
        # Apply search filter
        if search_query:
            faqs = faqs.filter(
                models.Q(question__icontains=search_query) |
                models.Q(answer__icontains=search_query)
            )
            context['search_query'] = search_query
        
        context['faqs'] = faqs
        return context