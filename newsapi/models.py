from django.db import models
from django.utils import timezone


class News(models.Model):
    """Model representing a news article."""
    
    title = models.TextField(help_text="The title of the news article")
    summary = models.TextField(help_text="A brief summary of the news article")
    source = models.CharField(max_length=100, help_text="The news source name")
    language = models.CharField(
        max_length=3, 
        choices=[
            ('en', 'English'),
            ('np', 'Nepali'),
        ],
        default='en',
        help_text="Language of the article"
    )
    source_url = models.URLField(max_length=500, help_text="URL to the original article")
    image_url = models.URLField(
        max_length=500, 
        null=True, 
        blank=True, 
        help_text="URL to the article's featured image"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this record was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When this record was last updated"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "News Article"
        verbose_name_plural = "News Articles"

    def __str__(self):
        return f"{self.title[:50]}... ({self.source})"


