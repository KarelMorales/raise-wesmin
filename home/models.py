from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images.models import Image
from wagtail.images.widgets import AdminImageChooser

class HomePage(Page):
    # Hero Section
    hero_title = models.CharField(
        max_length=200, 
        blank=True,
        default="AANR Knowledge Hub"
    )
    hero_subtitle = RichTextField(
        blank=True,
        default="Empowering communities through knowledge sharing and technological advancement in Agriculture, Aquatic, and Natural Resources sectors."
    )
    hero_quote = models.TextField(
        blank=True,
        default="Harnessing knowledge to sustain Agriculture, Aquatic, and Natural Resources— empowering communities, preserving nature, and driving innovation for a resilient future."
    )
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    # Features Section
    features_title = models.CharField(
        max_length=200,
        blank=True,
        default="Knowledge Hub Features"
    )
    features_subtitle = models.CharField(
        max_length=200,
        blank=True,
        default="Discover the powerful tools and resources available to help you advance your work in the AANR sector"
    )
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
            FieldPanel('hero_quote'),
            FieldPanel('hero_image', widget=AdminImageChooser),  # Updated this line
        ], heading="Hero Section"),
        
        MultiFieldPanel([
            FieldPanel('features_title'),
            FieldPanel('features_subtitle'),
        ], heading="Features Section"),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        # Try to get FAQs if the faqs app exists
        try:
            from faqs.models import FAQ
            context['latest_faqs'] = FAQ.objects.all().order_by('-created_at')[:5]
        except:
            context['latest_faqs'] = []
        return context