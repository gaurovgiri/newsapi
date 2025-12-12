"""
Nagarik News scraper.
"""
import re
import logging
import html
from typing import List
from news_source import NewsSource, Article

logger = logging.getLogger(__name__)


class NagarikNewsSource(NewsSource):
    """News scraper for Nagarik News."""
    
    @property
    def source_name(self) -> str:
        return "NagarikNews"
    
    @property
    def language(self) -> str:
        return "np"
    
    def scrape(self) -> List[Article]:
        """Scrape news from Nagarik News."""
        url = 'https://nagariknews.nagariknetwork.com/'
        soup = self.fetch_page(url)
        
        if not soup:
            return []
        
        articles = []
        
        try:
            headings = soup.select('#politics h1 a')
            contents = soup.select('.text > p')
            links = soup.select('.text > h1 > a')
            images = soup.select('article.list-group-item > div.image.default > figure > a > img')
            
            for i, heading in enumerate(headings):
                try:
                    # Clean text with special handling for NagarikNews and decode HTML entities
                    title_text = heading.get_text()
                    title_text = re.sub(r'(?:\n|\t| {2,})', '', title_text).strip()
                    title = html.unescape(title_text)
                    
                    # Get summary
                    summary = ''
                    if i < len(contents):
                        content_text = contents[i].get_text()
                        content_text = re.sub(r'(?:\n|\t| {2,})', '', content_text).strip()
                        summary = html.unescape(content_text)
                    
                    # Get link
                    source_url = ''
                    if i < len(links):
                        href = links[i].get('href', '')
                        source_url = f"https://nagariknews.nagariknetwork.com{href}" if href else ''
                    
                    # Get image
                    image_url = ''
                    if i < len(images):
                        image_url = images[i].get('data-src', '') or images[i].get('src', '')
                    
                    if title and summary:
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
