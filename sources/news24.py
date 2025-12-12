"""
News24 Nepal scraper.
"""
import logging
import html
from typing import List
from news_source import NewsSource, Article

logger = logging.getLogger(__name__)


class News24Source(NewsSource):
    """News scraper for News24Nepal."""
    
    @property
    def source_name(self) -> str:
        return "News24"
    
    @property
    def language(self) -> str:
        return "np"
    
    def scrape(self) -> List[Article]:
        """Scrape news from News24Nepal."""
        url = 'https://www.news24nepal.com/news-1'
        soup = self.fetch_page(url)
        
        if not soup:
            return []
        
        articles = []
        
        try:
            headings = soup.select('.half-more-news > div > div > span:nth-child(1)')
            links = soup.select('.half-more-news > div > div > span > a')
            images = soup.select('.half-more-news > div > figure > a > img')
            
            for i, heading in enumerate(headings):
                try:
                    # Get text and decode HTML entities
                    title_text = html.unescape(heading.get_text().strip())
                    # Remove first 6 characters if they exist
                    title = title_text[6:].strip() if len(title_text) > 6 else title_text
                    
                    # Get link
                    source_url = links[i].get('href', '') if i < len(links) else ''
                    
                    # Get image
                    image_url = ''
                    if i < len(images):
                        image_url = images[i].get('data-src', '') or images[i].get('src', '')
                    
                    # Use title as summary if no separate summary
                    summary = title
                    
                    if title:
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
