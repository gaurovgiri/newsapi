import logging
import re
from itertools import cycle
from typing import List, Dict, Optional

import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import News
from .serializers import NewsSerializer

logger = logging.getLogger(__name__)


class NewsScrapingConfig:
    """Configuration for news scraping from different websites."""
    
    WEBSITES = [
        {
            'url': 'https://www.news24nepal.com/news-1',
            'head_selector': '.half-more-news > div > div > span:nth-child(1)',
            'content_selector': '.half-more-news > div > div > span:nth-child(1)',
            'link_selector': '.half-more-news > div > div > span > a',
            'image_selector': '.half-more-news > div > figure > a > img',
            'source': 'News24',
            'language': 'np'
        },
        {
            'url': 'https://www.kathmandupost.com',
            'head_selector': 'article > h3',
            'content_selector': 'article > p',
            'link_selector': 'article > h3 > a',
            'image_selector': '.pull-right .img-responsive',
            'source': 'KathmanduPost',
            'language': 'en'
        },
        {
            'url': 'https://ekantipur.com/',
            'head_selector': 'div.teaser > h2',
            'content_selector': 'div.teaser > p',
            'link_selector': 'div.teaser > h2 > a',
            'image_selector': '.listLayout img',
            'source': 'Ekantipur',
            'language': 'np'
        },
        {
            'url': 'https://nagariknews.nagariknetwork.com/',
            'head_selector': '#politics h1 a',
            'content_selector': '.text > p',
            'link_selector': '.text > h1 > a',
            'image_selector': 'article.list-group-item > div.image.default > figure > a > img',
            'source': 'NagarikNews',
            'language': 'np'
        }
    ]


class NewsScraperService:
    """Service class for scraping news from various websites."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def clean_text(self, text: str, source: str) -> str:
        """Clean and format text based on source-specific patterns."""
        if source == 'NagarikNews':
            # Remove extra whitespace and newlines
            return re.sub(r'(?:\n|\t| {2,})', '', text).strip()
        elif source == 'News24':
            # Remove first 6 characters if they exist
            return text[6:].strip() if len(text) > 6 else text.strip()
        return text.strip()
    
    def get_link_url(self, element, source: str, base_url: str) -> str:
        """Extract and format URL based on source requirements."""
        if source == 'NagarikNews':
            href = element.get('href', '')
            return f"https://nagariknews.nagariknetwork.com{href}" if href else ''
        elif source == 'KathmanduPost':
            href = element.get('href', '')
            return f"https://kathmandupost.com{href}" if href else ''
        else:
            return element.get('href', '')
    
    def get_image_url(self, element, source: str) -> str:
        """Extract image URL based on source requirements."""
        if source == 'EtajaKhabar':
            return element.get('src', '')
        else:
            return element.get('data-src', '') or element.get('src', '')
        return ''
    
    def scrape_website(self, config: Dict) -> List[Dict]:
        """Scrape news from a single website based on configuration."""
        articles = []
        
        try:
            response = self.session.get(config['url'], timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html5lib')
            
            # Get all elements
            headings = soup.select(config['head_selector'])
            contents = soup.select(config['content_selector'])
            links = soup.select(config['link_selector'])
            images = soup.select(config['image_selector'])

            # Process articles
            for i, heading in enumerate(headings):
                try:
                    title = self.clean_text(heading.get_text(), config['source'])
                    
                    # Get summary if available
                    summary = ''
                    if i < len(contents):
                        content_text = contents[i].get_text()
                        # Skip News24 content that starts with newline and https
                        if not re.match(r'\nhttps:+', content_text):
                            summary = content_text.strip()
                    
                    # Get source URL
                    source_url = ''
                    if i < len(links):
                        source_url = self.get_link_url(links[i], config['source'], config['url'])
                    
                    # Get image URL
                    image_url = ''
                    if i < len(images):
                        image_url = self.get_image_url(images[i], config['source'])
                    
                    if title and summary:  # Only add if we have both title and summary
                        articles.append({
                            'title': title,
                            'summary': summary,
                            'source': config['source'],
                            'language': config['language'],
                            'source_url': source_url,
                            'image_url': image_url
                        })
                        
                except Exception as e:
                    logger.warning(f"Error processing article {i} from {config['source']}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping {config['url']}: {e}")
        
        return articles
    
    def scrape_all_news(self) -> List[Dict]:
        """Scrape news from all configured websites."""
        all_articles = []
        
        for config in NewsScrapingConfig.WEBSITES:
            logger.info(f"Scraping news from {config['source']}...")
            articles = self.scrape_website(config)
            all_articles.extend(articles)
            logger.info(f"Found {len(articles)} articles from {config['source']}")
        
        return all_articles


class NewsListAPIView(generics.ListAPIView):
    """API view to list all news articles."""
    
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    
    def get_queryset(self):
        """Filter queryset based on query parameters."""
        queryset = super().get_queryset()
        
        source = self.request.query_params.get('source')
        language = self.request.query_params.get('language')
        
        if source:
            queryset = queryset.filter(source__iexact=source)
        if language:
            queryset = queryset.filter(language=language)
            
        return queryset


@api_view(['POST'])
def refresh_news(request):
    """API endpoint to refresh news data by scraping websites."""
    try:
        scraper = NewsScraperService()
        articles = scraper.scrape_all_news()
        
        if not articles:
            return Response(
                {'error': 'No articles were scraped'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Clear existing news and save new ones
        News.objects.all().delete()
        
        created_count = 0
        for article_data in articles:
            try:
                News.objects.create(**article_data)
                created_count += 1
            except Exception as e:
                logger.error(f"Error saving article: {e}")
                continue
        
        return Response({
            'message': f'Successfully refreshed news data',
            'articles_created': created_count,
            'total_scraped': len(articles)
        })
        
    except Exception as e:
        logger.error(f"Error refreshing news: {e}")
        return Response(
            {'error': 'Failed to refresh news data'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def trigger_news_refresh(request):
    """Web view to trigger news refresh and redirect to API."""
    try:
        scraper = NewsScraperService()
        articles = scraper.scrape_all_news()
        
        if articles:
            News.objects.all().delete()
            for article_data in articles:
                try:
                    News.objects.create(**article_data)
                except Exception as e:
                    logger.error(f"Error saving article: {e}")
                    continue
        
        return redirect('/api')
        
    except Exception as e:
        logger.error(f"Error in trigger_news_refresh: {e}")
        return redirect('/api')


# Legacy compatibility (deprecated)
class all_news(APIView):
    """Legacy API view - use NewsListAPIView instead."""
    
    def get(self, request):
        news_all = News.objects.all()
        serializer = NewsSerializer(news_all, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        return Response(
            {'error': 'POST method not supported'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
