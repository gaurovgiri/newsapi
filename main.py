"""
News Scraper - Main script to scrape news from multiple sources,
deduplicate articles, save JSON snapshots, and push to Hugging Face Hub.

Usage:
    python main.py

The script will:
1. Fetch existing daily snapshot from Hugging Face if not available locally
2. Scrape news from all configured sources
3. Deduplicate and merge articles with existing day data
4. Save results locally to data/YYYY-MM-DD.json and data/today.json
5. Automatically push updated files to Hugging Face Hub (if HF_TOKEN is set)
"""

import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Tuple

from news_source import Article
from sources import (
    News24Source,
    KathmanduPostSource,
    EkantipurSource,
    NagarikNewsSource
)
from hf_sync import (
    download_hf_file,
    upload_files_to_hf,
    update_parquet_dataset,
    get_hf_token,
    get_hf_repo_id
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
    """Main scraper that orchestrates scraping, deduplication, and Hugging Face sync."""
    
    def __init__(self, output_dir: str = 'data'):
        """
        Initialize the news scraper.
        
        Args:
            output_dir: Directory to save JSON files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.hf_token = get_hf_token()
        self.hf_repo_id = get_hf_repo_id()
        
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
    
    def _load_existing_articles(self, file_path: Path, repo_relative_path: str = "") -> Tuple[List[dict], str]:
        """
        Load existing articles from a JSON file.
        If file doesn't exist locally, attempts to fetch from Hugging Face Hub.
        
        Args:
            file_path: Path to the local JSON file
            repo_relative_path: Path inside HF dataset repo (e.g., 'data/today.json')
            
        Returns:
            Tuple of (list of existing article dictionaries, date string from file)
        """
        if not file_path.exists() and repo_relative_path:
            # Attempt to pull previous state from Hugging Face
            download_hf_file(
                filename=repo_relative_path,
                target_path=file_path,
                repo_id=self.hf_repo_id,
                token=self.hf_token
            )

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
        new_dicts = [article.model_dump() for article in new_articles]
        
        # Create a set of (title, source) tuples for existing articles
        existing_keys = {(article.get('title', ''), article.get('source', '')) 
                        for article in existing}
        
        unique_new = []
        duplicate_count = 0
        for article in new_dicts:
            key = (article.get('title', ''), article.get('source', ''))
            if key not in existing_keys:
                unique_new.append(article)
                existing_keys.add(key)
            else:
                duplicate_count += 1
        
        if duplicate_count > 0:
            logger.info("Skipped %d duplicate articles", duplicate_count)
        
        return existing + unique_new
    
    def save_to_json(self, articles: List[Article]) -> List[Path]:
        """
        Save articles to JSON files, appending new articles to existing data.
        
        Creates/updates two files:
        1. data/YYYY-MM-DD.json - Date-stamped file (always appends for same date)
        2. data/today.json - Overwrites if date changed, appends if same date
        
        Returns:
            List of modified file paths
        """
        if not articles:
            logger.warning("No articles to save")
            return []
        
        today = datetime.now()
        date_str = today.strftime('%Y-%m-%d')
        timestamp = today.isoformat()
        
        # 1. Process date-stamped file - always append for the same date
        date_file = self.output_dir / f"{date_str}.json"
        existing_date, _ = self._load_existing_articles(date_file, f"data/{date_str}.json")
        merged_date = self._merge_articles(existing_date, articles)
        
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
        
        # 2. Process today.json file - overwrite if date changed, append if same date
        today_file = self.output_dir / "today.json"
        existing_today, existing_date_str = self._load_existing_articles(today_file, "data/today.json")
        
        if existing_date_str and existing_date_str != date_str:
            logger.info("Date changed from %s to %s - refreshing today.json", 
                       existing_date_str, date_str)
            articles_dict = [article.model_dump() for article in articles]
            merged_today = articles_dict
            new_count_today = len(articles)
        else:
            merged_today = self._merge_articles(existing_today, articles)
            new_count_today = len(merged_today) - len(existing_today)
        
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
        
        modified_files = [date_file, today_file]

        # 3. Update Parquet dataset
        parquet_file = self.output_dir / "train.parquet"
        try:
            update_parquet_dataset(
                articles=merged_today,
                date_str=date_str,
                scraped_at=timestamp,
                parquet_path=parquet_file,
                repo_id=self.hf_repo_id,
                token=self.hf_token
            )
            if parquet_file.exists():
                modified_files.append(parquet_file)
        except Exception as e:
            logger.warning("Could not update parquet dataset: %s", e)

        return modified_files
    
    def sync_to_huggingface(self, modified_files: List[Path]) -> None:
        """
        Push updated JSON files to Hugging Face Dataset repository.
        
        Args:
            modified_files: List of file Paths to upload
        """
        if not self.hf_token:
            logger.info("HF_TOKEN environment variable not found. Skipping Hugging Face upload.")
            return

        logger.info("Syncing updated files to Hugging Face dataset: %s...", self.hf_repo_id)
        now_str = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        commit_message = f"🗞️ Update news data - {now_str}"
        
        success = upload_files_to_hf(
            files=modified_files,
            repo_id=self.hf_repo_id,
            token=self.hf_token,
            commit_message=commit_message
        )
        
        if success:
            logger.info("Successfully pushed updates to Hugging Face: https://huggingface.co/datasets/%s", self.hf_repo_id)
        else:
            logger.warning("Failed to sync some files to Hugging Face.")
    
    def run(self) -> None:
        """Run the complete scraping and sync process."""
        logger.info("=" * 60)
        logger.info("Nepali News Scraper Started")
        logger.info("=" * 60)
        
        try:
            # 1. Scrape all sources
            articles = self.scrape_all()
            
            # 2. Save to JSON
            saved_files = self.save_to_json(articles)
            
            # 3. Push to Hugging Face
            if saved_files:
                self.sync_to_huggingface(saved_files)
            
            logger.info("=" * 60)
            logger.info("Nepali News Scraper Completed Successfully")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error("Scraping process failed: %s", e)
            sys.exit(1)


def main():
    """Main entry point."""
    scraper = NewsScraper()
    scraper.run()


if __name__ == '__main__':
    main()
