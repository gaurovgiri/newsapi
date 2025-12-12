"""
Abstract base class for news sources with Pydantic models.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
import requests
from bs4 import BeautifulSoup
import logging
import html
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class Article(BaseModel):
    """Pydantic model for a news article."""
    title: str = Field(..., min_length=1, description="Article title")
    summary: str = Field(..., min_length=1, description="Article summary or description")
    source: str = Field(..., min_length=1, description="Name of the news source")
    language: str = Field(..., pattern=r'^[a-z]{2}$', description="Two-letter language code (e.g., 'en', 'np')")
    source_url: str = Field(default="", description="URL to the original article")
    image_url: str = Field(default="", description="URL to the article image")
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "title": "Breaking News Title",
                "summary": "This is a summary of the article",
                "source": "NewsSource",
                "language": "en",
                "source_url": "https://example.com/article",
                "image_url": "https://example.com/image.jpg"
            }
        }


class NewsSource(ABC):
    """
    Abstract base class for news sources.
    Each news source must implement the scrape method.
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    @property
    @abstractmethod
    def source_name(self) -> str:
        """Return the name of the news source."""
        pass
    
    @property
    @abstractmethod
    def language(self) -> str:
        """Return the language code (e.g., 'en', 'np')."""
        pass
    
    @abstractmethod
    def scrape(self) -> List[Article]:
        """
        Scrape news articles from the source.
        
        Returns:
            List of Article objects
        """
        pass
    
    def fetch_page(self, url: str, timeout: int = 10) -> Optional[BeautifulSoup]:
        """
        Fetch and parse a web page.
        
        Args:
            url: URL to fetch
            timeout: Request timeout in seconds
            
        Returns:
            BeautifulSoup object or None if fetch fails
        """
        try:
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            # Set encoding to UTF-8 to handle Nepali text properly
            response.encoding = 'utf-8'
            return BeautifulSoup(response.text, 'html5lib')
        except Exception as e:
            logger.error("Error fetching %s: %s", url, e)
            return None
    
    def clean_text(self, text: str) -> str:
        """
        Clean text by removing extra whitespace and decoding HTML entities.
        
        Args:
            text: Text to clean
            
        Returns:
            Cleaned text
        """
        # Decode HTML entities (e.g., &#2352; -> proper Unicode)
        text = html.unescape(text)
        # Remove extra whitespace
        return ' '.join(text.split()).strip()
