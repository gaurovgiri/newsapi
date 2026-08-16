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
        seen_urls = set()
        
        try:
            items = soup.select('.half-more-news > div')
            
            for i, item in enumerate(items):
                try:
                    title_el = item.select_one('span.titles a, .titles a, .titles')
                    if not title_el:
                        continue
                    
                    title = self.clean_text(title_el.get_text())
                    if not title:
                        continue
                    
                    # Get link
                    link_el = item.select_one('span.titles a, figure a, a')
                    source_url = link_el.get('href', '').strip() if link_el else ''
                    if not source_url or source_url.startswith('javascript:'):
                        continue
                    
                    if source_url in seen_urls:
                        continue
                    seen_urls.add(source_url)
                    
                    # Get image
                    img_el = item.select_one('figure img, img')
                    image_url = ''
                    if img_el:
                        image_url = (img_el.get('data-src') or img_el.get('src') or '').strip()
                    
                    # Get description / full text
                    summary = ''
                    if source_url:
                        detail_soup = self.fetch_page(source_url, timeout=5)
                        if detail_soup:
                            paras = []
                            for p in detail_soup.select('.editor-box p, .detail-box p, .news-content p'):
                                txt = self.clean_text(p.get_text())
                                if txt and len(txt) > 10 and not txt.startswith('©') and not txt.startswith('Site by'):
                                    paras.append(txt)
                            if paras:
                                summary = '\n\n'.join(paras)
                    
                    # Fallback to listing description or title
                    if not summary:
                        desc_el = item.select_one('.description')
                        summary = self.clean_text(desc_el.get_text()) if desc_el else ''
                    if not summary:
                        summary = title
                    
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
