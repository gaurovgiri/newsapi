"""
Template for creating a new news source scraper.

To add a new news source:
1. Copy this file to sources/your_source_name.py
2. Rename the class to YourSourceName (use PascalCase)
3. Update source_name and language properties
4. Implement the scrape() method with your scraping logic
5. Add the import to sources/__init__.py
6. Add an instance to scrape_news.py

Example:
    from sources import YourSourceSource
    
    # In NewsScraper.__init__:
    self.sources = [
        ...,
        YourSourceSource()
    ]
"""
import logging
from typing import List
from news_source import NewsSource, Article

logger = logging.getLogger(__name__)


class TemplateSource(NewsSource):
    """News scraper template - replace with your source name."""
    
    @property
    def source_name(self) -> str:
        """Return the name of the news source (e.g., 'MyNewsSource')."""
        return "TemplateName"
    
    @property
    def language(self) -> str:
        """Return the language code (e.g., 'en' for English, 'np' for Nepali)."""
        return "en"
    
    def scrape(self) -> List[Article]:
        """
        Scrape news from your source.
        
        Returns:
            List of Article objects with validated fields:
            - title: Article title (required)
            - summary: Article summary (required)
            - source: Source name (auto-filled from self.source_name)
            - language: Language code (auto-filled from self.language)
            - source_url: URL to original article (optional, defaults to empty string)
            - image_url: URL to article image (optional, defaults to empty string)
        """
        url = 'https://example.com'
        soup = self.fetch_page(url)
        
        if not soup:
            return []
        
        articles = []
        
        try:
            # Example: Select elements using CSS selectors
            headings = soup.select('article h2')
            contents = soup.select('article p')
            links = soup.select('article a')
            images = soup.select('article img')
            
            for i, heading in enumerate(headings):
                try:
                    # Extract and clean title
                    title = self.clean_text(heading.get_text())
                    
                    # Extract summary
                    summary = ''
                    if i < len(contents):
                        summary = self.clean_text(contents[i].get_text())
                    
                    # Extract link
                    source_url = ''
                    if i < len(links):
                        href = links[i].get('href', '')
                        # Add base URL if needed
                        source_url = f"https://example.com{href}" if href.startswith('/') else href
                    
                    # Extract image
                    image_url = ''
                    if i < len(images):
                        # Try data-src first (lazy loading), then src
                        image_url = images[i].get('data-src', '') or images[i].get('src', '')
                    
                    # Only add if we have required fields
                    if title and summary:
                        # Create Article object with Pydantic validation
                        article = Article(
                            title=title,
                            summary=summary,
                            source=self.source_name,
                            language=self.language,
                            source_url=source_url,
                            image_url=image_url
                        )
                        articles.append(article)
                        
                except (IndexError, AttributeError) as e:
                    logger.warning("Error processing article %d from %s: %s", i, self.source_name, e)
                    continue
                    
        except Exception as e:
            logger.error("Error scraping %s: %s", self.source_name, e)
        
        logger.info("Scraped %d articles from %s", len(articles), self.source_name)
        return articles
