"""
The Kathmandu Post scraper.
"""
import logging
from typing import List
from news_source import NewsSource, Article

from urllib.parse import urljoin

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
        seen_urls = set()
        
        try:
            cards = soup.select('article')
            
            for i, card in enumerate(cards):
                try:
                    title_el = card.select_one('h1 a, h2 a, h3 a, h4 a, h1, h2, h3, h4, .title a, .title')
                    if not title_el:
                        continue
                    
                    title = self.clean_text(title_el.get_text())
                    if not title:
                        continue
                    
                    # Get link
                    link_el = card.select_one('h1 a, h2 a, h3 a, h4 a, a')
                    href = link_el.get('href', '').strip() if link_el else ''
                    if not href or href == '#' or href.startswith('javascript:'):
                        continue
                    
                    source_url = urljoin('https://kathmandupost.com', href)
                    if source_url in seen_urls:
                        continue
                    seen_urls.add(source_url)
                    
                    # Get summary / full description
                    summary = ''
                    if source_url:
                        detail_soup = self.fetch_page(source_url, timeout=5)
                        if detail_soup:
                            paras = []
                            for p in detail_soup.select('.story-section p, .subscribe-content p'):
                                txt = self.clean_text(p.get_text())
                                if txt and len(txt) > 10 and not txt.startswith('Published at') and not txt.startswith('Updated at'):
                                    paras.append(txt)
                            if paras:
                                summary = '\n\n'.join(paras)
                    
                    if not summary:
                        p_el = card.select_one('p')
                        summary = self.clean_text(p_el.get_text()) if p_el else ''
                        
                    if not summary:
                        summary = title
                    
                    # Get image
                    img_el = card.select_one('img')
                    image_url = ''
                    if img_el:
                        src = (img_el.get('data-src') or img_el.get('src') or '').strip()
                        if src:
                            image_url = urljoin('https://kathmandupost.com', src)
                    
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
