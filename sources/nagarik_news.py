"""
Nagarik News scraper.
"""
import re
import logging
import html
from typing import List
from news_source import NewsSource, Article

from urllib.parse import urljoin

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
        seen_urls = set()
        
        try:
            cards = soup.select('article')
            
            for i, card in enumerate(cards):
                try:
                    title_el = card.select_one('h1 a, h2 a, h3 a, h4 a, h1, h2, h3, h4')
                    if not title_el:
                        continue
                    
                    title_text = title_el.get_text()
                    title_text = re.sub(r'(?:\n|\t| {2,})', ' ', title_text).strip()
                    title = self.clean_text(title_text)
                    if not title:
                        continue
                    
                    # Get link
                    link_el = card.select_one('h1 a, h2 a, h3 a, h4 a, figure a, a')
                    href = link_el.get('href', '').strip() if link_el else ''
                    if not href or href == '#' or href.startswith('javascript:'):
                        continue
                    
                    source_url = urljoin('https://nagariknews.nagariknetwork.com', href)
                    if source_url in seen_urls:
                        continue
                    seen_urls.add(source_url)
                    
                    # Get summary / full description
                    summary = ''
                    if source_url:
                        detail_soup = self.fetch_page(source_url, timeout=5)
                        if detail_soup:
                            paras = []
                            for p in detail_soup.select('.subscriber-content-check p, #news-content p, .text p'):
                                txt = self.clean_text(p.get_text())
                                if txt and len(txt) > 10 and 'नागरिक अभिलेखालय' not in txt and 'Facebook' not in txt and 'javascript' not in txt.lower():
                                    paras.append(txt)
                            if paras:
                                summary = '\n\n'.join(paras)
                    
                    if not summary:
                        p_el = card.select_one('.text > p, p')
                        if p_el:
                            content_text = p_el.get_text()
                            content_text = re.sub(r'(?:\n|\t| {2,})', ' ', content_text).strip()
                            summary = self.clean_text(content_text)
                            
                    if not summary:
                        summary = title
                    
                    # Get image
                    img_el = card.select_one('figure img, img')
                    image_url = ''
                    if img_el:
                        img_src = (img_el.get('data-src') or img_el.get('src') or '').strip()
                        if img_src:
                            image_url = urljoin('https://nagariknews.nagariknetwork.com', img_src)
                    
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
