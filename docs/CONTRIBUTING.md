# Contributing to Nepali News API

Thank you for considering contributing to Nepali News API! This guide will help you add new news sources to the project.

## 🤝 How to Contribute

Contributions are welcome in many forms:

1. 📰 **Add News Sources** - Add scrapers for new Nepali news websites
2. 🐛 **Report Bugs** - Found a broken scraper? Let us know
3. 💡 **Suggest Features** - Have ideas for improvements?
4. 📖 **Improve Documentation** - Fix typos or add examples
5. 🧪 **Write Tests** - Help us maintain quality

## 📰 Adding a New News Source

### Prerequisites

- Python 3.11 or higher
- Basic understanding of HTML and web scraping
- Familiarity with BeautifulSoup4

### Step-by-Step Guide

#### Step 1: Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/newsapi.git
cd newsapi

# Install dependencies
pip install -r requirements.txt
```

#### Step 2: Create Your Scraper File

Copy the template to create a new scraper:

```bash
cp sources/_template.py sources/your_source.py
```

**Naming Convention**: Use lowercase with underscores. Examples:
- `the_himalayan_times.py`
- `online_khabar.py`
- `setopati.py`

#### Step 3: Implement the Scraper

Edit `sources/your_source.py` and implement the required methods:

```python
import logging
from typing import List
from datetime import datetime
from news_source import NewsSource, Article

logger = logging.getLogger(__name__)


class YourSourceName(NewsSource):
    """
    Scraper for [Your News Source Name].
    
    Website: https://your-news-source.com
    Language: Nepali/English
    """
    
    @property
    def source_name(self) -> str:
        """Return the display name of this news source."""
        return "Your Source Name"
    
    @property
    def language(self) -> str:
        """
        Return the primary language code.
        'ne' for Nepali, 'en' for English
        """
        return "ne"
    
    def scrape(self) -> List[Article]:
        """
        Scrape articles from the news source.
        
        Returns:
            List of Article objects
        """
        articles = []
        
        try:
            # 1. Fetch the webpage
            url = 'https://your-news-source.com'
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # 2. Parse HTML
            soup = self.parse_html(response.text)
            
            # 3. Find article containers
            # Adjust the selector based on the website structure
            article_elements = soup.find_all('article', class_='news-item')
            
            # 4. Extract data from each article
            for element in article_elements:
                try:
                    # Extract title
                    title_elem = element.find('h2', class_='title')
                    if not title_elem:
                        continue
                    title = title_elem.text.strip()
                    
                    # Extract link
                    link_elem = element.find('a')
                    if not link_elem:
                        continue
                    link = link_elem.get('href', '')
                    
                    # Make absolute URL if necessary
                    if link.startswith('/'):
                        link = f'https://your-news-source.com{link}'
                    
                    # Extract description (optional)
                    desc_elem = element.find('p', class_='description')
                    description = desc_elem.text.strip() if desc_elem else ''
                    
                    # Extract published date (optional)
                    date_elem = element.find('time')
                    published_date = None
                    if date_elem:
                        date_str = date_elem.get('datetime') or date_elem.text
                        published_date = self.parse_date(date_str)
                    
                    # Create Article object
                    article = Article(
                        title=title,
                        link=link,
                        description=description,
                        published_date=published_date,
                        source=self.source_name,
                        language=self.language
                    )
                    
                    articles.append(article)
                    
                except Exception as e:
                    logger.warning(f"Failed to parse article: {e}")
                    continue
            
            logger.info(f"Successfully scraped {len(articles)} articles from {self.source_name}")
            
        except Exception as e:
            logger.error(f"Error scraping {self.source_name}: {e}")
        
        return articles
```

#### Step 4: Register Your Source

Add your scraper to `sources/__init__.py`:

```python
from .news24 import News24Source
from .kathmandu_post import KathmanduPostSource
from .ekantipur import EkantipurSource
from .nagarik_news import NagarikNewsSource
from .your_source import YourSourceName  # Add this line

__all__ = [
    'News24Source',
    'KathmanduPostSource',
    'EkantipurSource',
    'NagarikNewsSource',
    'YourSourceName',  # Add this line
]
```

#### Step 5: Add to Main Scraper

Update `main.py` to include your source:

```python
from sources import (
    News24Source,
    KathmanduPostSource,
    EkantipurSource,
    NagarikNewsSource,
    YourSourceName  # Add this import
)

class NewsScraper:
    def __init__(self, output_dir: str = 'data'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize sources
        self.sources = [
            News24Source(),
            KathmanduPostSource(),
            EkantipurSource(),
            NagarikNewsSource(),
            YourSourceName(),  # Add this line
        ]
```

#### Step 6: Test Your Scraper

```bash
# Run the scraper
python main.py

# Check the output
cat data/today.json

# Verify your source appears and has articles
cat data/today.json | jq '.sources'
cat data/today.json | jq '.articles[] | select(.source == "Your Source Name")'
```

#### Step 7: Submit Your Contribution

```bash
# Create a new branch
git checkout -b feat/add-your-source

# Add your changes
git add sources/your_source.py sources/__init__.py main.py

# Commit with a descriptive message
git commit -m "Add YourSourceName scraper

- Scrapes articles from https://your-source.com
- Extracts title, link, description, and date
- Supports Nepali/English language"

# Push to your fork
git push origin feat/add-your-source
```

Then create a Pull Request on GitHub!

## 🎯 Best Practices

### 1. Respect Robots.txt

Always check the website's `robots.txt` file:

```python
# Good practice
response = self.session.get('https://example.com/robots.txt')
# Check if scraping is allowed
```

### 2. Handle Errors Gracefully

```python
try:
    # Scraping logic
    pass
except requests.RequestException as e:
    logger.error(f"Network error: {e}")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
```

### 3. Use Appropriate Selectors

```python
# Prefer specific selectors
article = soup.find('article', class_='news-card')

# Use fallbacks
title = article.find('h2') or article.find('h3') or article.find('h1')
```

### 4. Validate Data

```python
# Ensure required fields exist
if not title or not link:
    logger.warning("Missing required fields, skipping article")
    continue

# Clean data
title = title.strip()
link = link.strip()
```

### 5. Set Reasonable Timeouts

```python
response = self.session.get(url, timeout=30)
```

### 6. Add Logging

```python
logger.info(f"Starting scrape for {self.source_name}")
logger.info(f"Found {len(articles)} articles")
logger.error(f"Failed to fetch page: {e}")
```

## 🧪 Testing Checklist

Before submitting your PR, verify:

- [ ] Scraper runs without errors
- [ ] At least one article is successfully scraped
- [ ] Article titles are properly extracted
- [ ] Links are valid and absolute URLs
- [ ] Source name appears in the output
- [ ] Language code is correct (`ne` or `en`)
- [ ] No sensitive or personal data is included
- [ ] Code follows Python conventions (PEP 8)
- [ ] Logging statements are appropriate

## 📝 Pull Request Guidelines

### Title Format
```
Add [SourceName] scraper
```

### Description Template
```markdown
## Description
Adds scraper for [Source Name] from [URL].

## Details
- **Language**: Nepali/English
- **Articles per scrape**: ~XX articles
- **Special features**: Any unique aspects

## Testing
- [x] Tested locally
- [x] Generated valid JSON
- [x] Verified article data quality

## Screenshots (optional)
<!-- Add sample output if helpful -->
```

## 🚫 What NOT to Scrape

Please avoid scraping:

- ❌ Paywalled content
- ❌ Content requiring login
- ❌ Sites that explicitly prohibit scraping
- ❌ Personal data or sensitive information
- ❌ Copyrighted images (text/links only)

## 🔧 Helper Methods

The `NewsSource` base class provides useful methods:

### `parse_html(html: str) -> BeautifulSoup`
Parse HTML string into BeautifulSoup object.

### `parse_date(date_str: str) -> Optional[str]`
Parse various date formats into ISO 8601 string.

```python
# Handles formats like:
# "2024-12-12"
# "12 Dec 2024"
# "2024-12-12T10:30:00"
date = self.parse_date("12 Dec 2024")
```

### `session: requests.Session`
Reusable HTTP session with headers.

## 📚 Common Patterns

### Pattern 1: List Page Scraping

```python
def scrape(self) -> List[Article]:
    articles = []
    url = 'https://example.com/news'
    response = self.session.get(url)
    soup = self.parse_html(response.text)
    
    for item in soup.select('.article-list .article'):
        article = self._parse_article(item)
        if article:
            articles.append(article)
    
    return articles
```

### Pattern 2: RSS Feed Parsing

```python
import feedparser

def scrape(self) -> List[Article]:
    articles = []
    feed = feedparser.parse('https://example.com/feed')
    
    for entry in feed.entries:
        article = Article(
            title=entry.title,
            link=entry.link,
            description=entry.summary,
            published_date=self.parse_date(entry.published),
            source=self.source_name,
            language=self.language
        )
        articles.append(article)
    
    return articles
```

### Pattern 3: API Endpoint Scraping

```python
def scrape(self) -> List[Article]:
    articles = []
    url = 'https://example.com/api/news'
    response = self.session.get(url)
    data = response.json()
    
    for item in data['articles']:
        article = Article(
            title=item['title'],
            link=item['url'],
            description=item.get('description', ''),
            published_date=item.get('date'),
            source=self.source_name,
            language=self.language
        )
        articles.append(article)
    
    return articles
```

## 🐛 Common Issues

### Issue: 403 Forbidden Error
**Solution**: Update User-Agent header in `NewsSource.session`

### Issue: Empty Results
**Solution**: Check if selectors match website structure (use browser inspector)

### Issue: Encoding Problems
**Solution**: Ensure response encoding is correct: `response.encoding = 'utf-8'`

### Issue: Relative URLs
**Solution**: Convert to absolute URLs:
```python
from urllib.parse import urljoin
absolute_url = urljoin(base_url, relative_url)
```

## 📞 Getting Help

- **Questions**: Open a [Discussion](https://github.com/gaurovgiri/newsapi/discussions)
- **Bugs**: Open an [Issue](https://github.com/gaurovgiri/newsapi/issues)
- **Chat**: Comment on your PR for specific help

## 🙏 Thank You!

Every contribution helps make Nepali news more accessible to developers and researchers. Thank you for being part of this open-source project!
