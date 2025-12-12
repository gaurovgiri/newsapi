# News Scraper

A standalone Python script to scrape news articles from multiple Nepali news sources and save them to JSON files.

**No Django required!** This is a simple, standalone scraper with a clean modular architecture.

## Features

- **Modular Architecture**: Each news source in its own file in the `sources/` directory
- **Easy to Extend**: Template provided for adding new sources
- **Multiple News Sources**: News24, Kathmandu Post, Ekantipur, Nagarik News
- **JSON Output**: Date-stamped files + `today.json`
- **Automation Ready**: Run via cron jobs or GitHub Actions
- **Proper Unicode Support**: Nepali text correctly stored

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the scraper
python scrape_news.py
```

## Project Structure

```
newsapi/
├── scrape_news.py          # Main script
├── news_source.py          # Abstract base class
├── sources/                # One file per news source
│   ├── __init__.py
│   ├── _template.py       # Template for new sources
│   ├── news24.py
│   ├── kathmandu_post.py
│   ├── ekantipur.py
│   └── nagarik_news.py
└── data/                   # Generated JSON files
    ├── today.json
    └── YYYY-MM-DD.json
```

## Adding New Sources

See [ADDING_SOURCES.md](ADDING_SOURCES.md) for a complete guide.

**Quick steps:**
1. Copy `sources/_template.py` to `sources/your_source.py`
2. Implement the scraper
3. Add to `sources/__init__.py`
4. Add to `scrape_news.py`

## Documentation

- [QUICK_START.md](QUICK_START.md) - Quick reference guide
- [ADDING_SOURCES.md](ADDING_SOURCES.md) - How to add new sources

## Automation

Run daily via cron:
```bash
0 6 * * * cd /path/to/newsapi && python scrape_news.py
```

Or use GitHub Actions - see [ADDING_SOURCES.md](ADDING_SOURCES.md) for workflow example.
