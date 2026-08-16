"""
Ekantipur scraper.
"""
import logging
from typing import List
from news_source import NewsSource, Article

from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class EkantipurSource(NewsSource):
    """News scraper for Ekantipur."""
    
    @property
    def source_name(self) -> str:
        return "Ekantipur"
    
    @property
    def language(self) -> str:
        return "np"
    
    def scrape(self) -> List[Article]:
        """Scrape news from Ekantipur."""
        url = 'https://ekantipur.com/'
        soup = self.fetch_page(url)
        
        if not soup:
            return []
        
        articles = []
        seen_urls = set()
        
        try:
            items = soup.select('.news-section, article, .normal')
            
            for i, item in enumerate(items):
                try:
                    h_tag = item.select_one('h1, h2, h3, h4, h5')
                    a_tag = h_tag.select_one('a') if h_tag else item.select_one('a')
                    if not a_tag or not h_tag:
                        continue
                    
                    title = self.clean_text(h_tag.get_text())
                    href = a_tag.get('href', '').strip()
                    if not href or not title or href.startswith('javascript:'):
                        continue
                    
                    source_url = urljoin('https://ekantipur.com', href)
                    if source_url in seen_urls:
                        continue
                    seen_urls.add(source_url)
                    
                    # Summary / full description
                    summary = ''
                    if source_url:
                        detail_soup = self.fetch_page(source_url, timeout=5)
                        if detail_soup:
                            paras = []
                            for p in detail_soup.select('.news-inner-wrapper p, .news-section-wrap > p, .normal p'):
                                txt = self.clean_text(p.get_text())
                                if txt and len(txt) > 10 and not txt.startswith('©') and 'Facebook' not in txt:
                                    paras.append(txt)
                            if paras:
                                summary = '\n\n'.join(paras)
                    
                    if not summary:
                        p_tag = item.select_one('p')
                        summary = self.clean_text(p_tag.get_text()) if p_tag else ''
                    
                    if not summary:
                        summary = title
                    
                    # Image
                    image_url = ''
                    img_tag = item.select_one('img')
                    if not img_tag:
                        # Find corresponding anchor with image on page
                        for matching_a in soup.find_all('a', href=href):
                            candidate_img = matching_a.select_one('img')
                            if candidate_img:
                                img_tag = candidate_img
                                break
                    if not img_tag and item.parent:
                        img_tag = item.parent.select_one('img')
                    
                    if img_tag:
                        src = img_tag.get('data-src') or img_tag.get('src') or ''
                        if src.startswith('//'):
                            image_url = 'https:' + src
                        elif src.startswith('/'):
                            image_url = urljoin('https://ekantipur.com', src)
                        elif src.startswith('http'):
                            image_url = src
                    
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
