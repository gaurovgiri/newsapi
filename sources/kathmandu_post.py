"""
The Kathmandu Post scraper.
"""
import logging
from typing import List
from news_source import NewsSource, Article

logger = logging.getLogger(__name__)


class KathmanduPostSource(NewsSource):
    """News scraper for The Kathmandu Post."""
    
    @property
    def source_name(self) -> str:
        return "KathmanduPost"
    
    @property
    def language(self) -> str:
        return "en"
    
    def scrape(self) -> List[Article]:
        """Scrape news from The Kathmandu Post."""
        url = 'https://www.kathmandupost.com'
        soup = self.fetch_page(url)
        
        if not soup:
            return []
        
        articles = []
        
        try:
            headings = soup.select('article > h3')
            contents = soup.select('article > p')
            links = soup.select('article > h3 > a')
            images = soup.select('.pull-right .img-responsive')
            
            for i, heading in enumerate(headings):
                try:
                    title = self.clean_text(heading.get_text())
                    
                    # Get summary
                    summary = ''
                    if i < len(contents):
                        summary = self.clean_text(contents[i].get_text())
                    
                    # Get link
                    source_url = ''
                    if i < len(links):
                        href = links[i].get('href', '')
                        source_url = f"https://kathmandupost.com{href}" if href else ''
                    
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
