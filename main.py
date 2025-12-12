"""
News Scraper - Main script to scrape news from multiple sources
and save to JSON files.

Usage:
    python scrape_news.py

The script will:
1. Scrape news from all configured sources
2. Save results to data/YYYY-MM-DD.json
3. Also save a copy to data/today.json
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import List

from news_source import Article
from sources import (
    News24Source,
    KathmanduPostSource,
    EkantipurSource,
    NagarikNewsSource
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class NewsScraper:
    """Main scraper that orchestrates scraping from all sources."""
    
    def __init__(self, output_dir: str = 'data'):
        """
        Initialize the news scraper.
        
        Args:
            output_dir: Directory to save JSON files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize all news sources
        self.sources = [
            News24Source(),
            KathmanduPostSource(),
            EkantipurSource(),
            NagarikNewsSource()
        ]
    
    def scrape_all(self) -> List[Article]:
        """
        Scrape news from all sources.
        
        Returns:
            List of all scraped Article objects
        """
        all_articles = []
        
        logger.info("Starting news scraping from %d sources...", len(self.sources))
        
        for source in self.sources:
            logger.info("Scraping from %s...", source.source_name)
            try:
                articles = source.scrape()
                all_articles.extend(articles)
                logger.info("Successfully scraped %d articles from %s", 
                          len(articles), source.source_name)
            except Exception as e:
                logger.error("Failed to scrape from %s: %s", 
                           source.source_name, e)
                continue
        
        logger.info("Total articles scraped: %d", len(all_articles))
        return all_articles
    
    def _load_existing_articles(self, file_path: Path) -> tuple[List[dict], str]:
        """
        Load existing articles from a JSON file.
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            Tuple of (list of existing article dictionaries, date string from file)
        """
        if not file_path.exists():
            return [], ""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('articles', []), data.get('date', '')
        except (json.JSONDecodeError, IOError) as e:
            logger.warning("Could not load existing articles from %s: %s", file_path, e)
            return [], ""
    
    def _merge_articles(self, existing: List[dict], new_articles: List[Article]) -> List[dict]:
        """
        Merge new articles with existing ones, avoiding duplicates.
        
        Duplicates are identified by matching title and source.
        
        Args:
            existing: List of existing article dictionaries
            new_articles: List of new Article objects
            
        Returns:
            List of merged article dictionaries
        """
        # Convert new articles to dicts
        new_dicts = [article.model_dump() for article in new_articles]
        
        # Create a set of (title, source) tuples for existing articles
        existing_keys = {(article.get('title', ''), article.get('source', '')) 
                        for article in existing}
        
        # Filter out duplicates from new articles
        unique_new = []
        duplicate_count = 0
        for article in new_dicts:
            key = (article.get('title', ''), article.get('source', ''))
            if key not in existing_keys:
                unique_new.append(article)
                existing_keys.add(key)  # Prevent duplicates within new articles too
            else:
                duplicate_count += 1
        
        if duplicate_count > 0:
            logger.info("Skipped %d duplicate articles", duplicate_count)
        
        # Combine existing and unique new articles
        return existing + unique_new
    
    def save_to_json(self, articles: List[Article]) -> None:
        """
        Save articles to JSON files, appending new articles to existing data.
        
        Creates/updates two files:
        1. data/YYYY-MM-DD.json - Date-stamped file (always appends for same date)
        2. data/today.json - Overwrites if date changed, appends if same date
        
        New articles are checked for duplicates (by title + source) before appending.
        
        Args:
            articles: List of Article objects to save
        """
        if not articles:
            logger.warning("No articles to save")
            return
        
        # Get current date
        today = datetime.now()
        date_str = today.strftime('%Y-%m-%d')
        timestamp = today.isoformat()
        
        # Process date-stamped file - always append for the same date
        date_file = self.output_dir / f"{date_str}.json"
        existing_date, _ = self._load_existing_articles(date_file)
        merged_date = self._merge_articles(existing_date, articles)
        
        # Prepare data structure for date file
        date_output = {
            'scraped_at': timestamp,
            'date': date_str,
            'total_articles': len(merged_date),
            'sources': list(set(article['source'] for article in merged_date)),
            'articles': merged_date
        }
        
        with open(date_file, 'w', encoding='utf-8') as f:
            json.dump(date_output, f, ensure_ascii=False, indent=2)
        
        new_count = len(merged_date) - len(existing_date)
        logger.info("Saved %d articles to %s (%d new, %d total)", 
                   new_count, date_file, new_count, len(merged_date))
        
        # Process today.json file - overwrite if date changed, append if same date
        today_file = self.output_dir / "today.json"
        existing_today, existing_date_str = self._load_existing_articles(today_file)
        
        # Check if the date has changed
        if existing_date_str and existing_date_str != date_str:
            # Date changed - overwrite with new data
            logger.info("Date changed from %s to %s - overwriting today.json", 
                       existing_date_str, date_str)
            articles_dict = [article.model_dump() for article in articles]
            merged_today = articles_dict
            new_count_today = len(articles)
        else:
            # Same date - append new articles
            merged_today = self._merge_articles(existing_today, articles)
            new_count_today = len(merged_today) - len(existing_today)
        
        # Prepare data structure for today file
        today_output = {
            'scraped_at': timestamp,
            'date': date_str,
            'total_articles': len(merged_today),
            'sources': list(set(article['source'] for article in merged_today)),
            'articles': merged_today
        }
        
        with open(today_file, 'w', encoding='utf-8') as f:
            json.dump(today_output, f, ensure_ascii=False, indent=2)
        
        logger.info("Saved %d articles to %s (%d new, %d total)", 
                   new_count_today, today_file, new_count_today, len(merged_today))
    
    def run(self) -> None:
        """Run the complete scraping process."""
        logger.info("=" * 60)
        logger.info("News Scraper Started")
        logger.info("=" * 60)
        
        try:
            # Scrape all sources
            articles = self.scrape_all()
            
            # Save to JSON
            self.save_to_json(articles)
            
            logger.info("=" * 60)
            logger.info("News Scraper Completed Successfully")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error("Scraping failed: %s", e)
            sys.exit(1)


def main():
    """Main entry point."""
    scraper = NewsScraper()
    scraper.run()


if __name__ == '__main__':
    main()
