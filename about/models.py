from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images.widgets import AdminImageChooser  # Use this import

class AboutPage(Page):
    # Hero Section
    hero_title = models.CharField(
        max_length=200,
        blank=True,
        default="RAISE Western Mindanao"
    )
    hero_subtitle = models.CharField(
        max_length=300,
        blank=True,
        default="Empowering agricultural communities through innovation, sustainability, and knowledge sharing"
    )
    
    # Knowledge Hub Section
    knowledge_hub_title = models.CharField(
        max_length=200,
        blank=True,
        default="Knowledge Hub"
    )
    knowledge_hub_subtitle = models.CharField(
        max_length=200,
        blank=True,
        default="Project Foundation"
    )
    knowledge_hub_description = models.TextField(
        blank=True,
        default="Understanding the core purpose and goals that drive our mission forward"
    )
    
    # Program Rationale Section
    rationale_title = models.CharField(
        max_length=200,
        blank=True,
        default="Program Rationale"
    )
    rationale_content = RichTextField(blank=True)
    
    # Program Objectives
    objectives_title = models.CharField(
        max_length=200,
        blank=True,
        default="Program Objectives"
    )
    general_objective_title = models.CharField(
        max_length=100,
        blank=True,
        default="General:"
    )
    general_objective = models.TextField(blank=True)
    specific_objectives_title = models.CharField(
        max_length=100,
        blank=True,
        default="Specific:"
    )
    specific_objectives = RichTextField(
        blank=True,
        help_text="Enter each objective on a new line"
    )
    
    # Organizational Structure
    org_title = models.CharField(
        max_length=200,
        blank=True,
        default="Organizational Structure"
    )
    org_description = models.CharField(
        max_length=200,
        blank=True,
        default="Our streamlined structure ensures efficient implementation across all project components"
    )
    org_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Upload the organizational structure image"
    )
    
    # RAISE Projects Section
    projects_title = models.CharField(
        max_length=200,
        blank=True,
        default="RAISE Projects"
    )
    projects_description = models.TextField(
        blank=True,
        default="Discover our innovative agricultural research initiatives and collaborative projects that are transforming the future of farming and rural development"
    )
    projects_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Upload the projects image"
    )
    
    content_panels = Page.content_panels + [
        # Hero Section
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
        ], heading="Hero Section"),
        
        # Knowledge Hub Section
        MultiFieldPanel([
            FieldPanel('knowledge_hub_title'),
            FieldPanel('knowledge_hub_subtitle'),
            FieldPanel('knowledge_hub_description'),
        ], heading="Knowledge Hub Section"),
        
        # Program Rationale
        MultiFieldPanel([
            FieldPanel('rationale_title'),
            FieldPanel('rationale_content'),
        ], heading="Program Rationale"),
        
        # Program Objectives
        MultiFieldPanel([
            FieldPanel('objectives_title'),
            FieldPanel('general_objective_title'),
            FieldPanel('general_objective'),
            FieldPanel('specific_objectives_title'),
            FieldPanel('specific_objectives'),
        ], heading="Program Objectives"),
        
        # Organizational Structure
        MultiFieldPanel([
            FieldPanel('org_title'),
            FieldPanel('org_description'),
            FieldPanel('org_image', widget=AdminImageChooser),  # Fixed this line
        ], heading="Organizational Structure"),
        
        # RAISE Projects
        MultiFieldPanel([
            FieldPanel('projects_title'),
            FieldPanel('projects_description'),
            FieldPanel('projects_image', widget=AdminImageChooser),  # Fixed this line
        ], heading="RAISE Projects"),
    ]