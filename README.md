# Nepali News API 🇳🇵

> **Free and Open Source API for Nepali News Sources** - Scrape, aggregate, and access Nepali news articles in JSON format with automatic updates every 4 hours.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Automated Updates](https://img.shields.io/badge/updates-every%204%20hours-green.svg)](https://github.com/gaurovgiri/newsapi/actions)

## 📰 About

**Nepali News API** is a free, open-source news aggregation service that scrapes top Nepali news sources and provides clean, structured JSON data. Perfect for developers building news apps, researchers analyzing Nepali media, or anyone needing programmatic access to Nepali news content.

### Why This API?

- 🆓 **100% Free** - No API keys, no rate limits, no subscriptions
- 🔄 **Auto-Updated** - Fresh news every 4 hours via GitHub Actions
- 🌐 **Open Source** - Transparent, extensible, and community-driven
- 📱 **Easy Integration** - Simple JSON endpoints for quick implementation
- 🇳🇵 **Unicode Support** - Proper Nepali text encoding (UTF-8)
- 🔌 **Plug & Play** - No backend setup required for API consumers

## 🚀 Quick Start

### Get Today's News (No Installation)

Access the API directly - no authentication required:

```bash
# Get today's aggregated news
curl https://raw.githubusercontent.com/gaurovgiri/newsapi/refs/heads/master/data/today.json

# Get news from a specific date (format: YYYY-MM-DD)
curl https://raw.githubusercontent.com/gaurovgiri/newsapi/refs/heads/master/data/2024-12-12.json
```

**JavaScript:**
```javascript
fetch('https://raw.githubusercontent.com/gaurovgiri/newsapi/refs/heads/master/data/today.json')
  .then(res => res.json())
  .then(data => console.log(`${data.total_articles} articles from ${data.sources.length} sources`));
```

**Python:**
```python
import requests
data = requests.get('https://raw.githubusercontent.com/gaurovgiri/newsapi/refs/heads/master/data/today.json').json()
print(f"{data['total_articles']} articles available")
```

➡️ **See [Quick Start Guide](docs/QUICK_START.md) for more examples**

### Run Locally (For Contributors)

```bash
git clone https://github.com/gaurovgiri/newsapi.git
cd newsapi
pip install -r requirements.txt
python main.py
```

## 📊 API Response Format

```json
{
  "scrape_date": "2024-12-12",
  "scrape_time": "06:00:15",
  "total_articles": 156,
  "sources": ["News24", "Kathmandu Post", "Ekantipur", "Nagarik News"],
  "articles": [
    {
      "title": "Article Title in Nepali or English",
      "link": "https://example.com/article",
      "description": "Article summary or excerpt",
      "published_date": "2024-12-12T10:30:00",
      "source": "News24",
      "language": "ne"
    }
  ]
}
```

➡️ **See [API Usage Guide](docs/API_USAGE.md) for detailed documentation and examples**

## 📰 Supported News Sources

| Source | Language | Website |
|--------|----------|---------|
| **News24** | Nepali | [news24nepal.tv](https://news24nepal.tv) |
| **Kathmandu Post** | English | [kathmandupost.com](https://kathmandupost.com) |
| **Ekantipur** | Nepali | [ekantipur.com](https://ekantipur.com) |
| **Nagarik News** | Nepali | [nagariknews.nagariknetwork.com](https://nagariknews.nagariknetwork.com) |

**Want to add more sources?** See [Contributing Guide](docs/CONTRIBUTING.md)

## 🏗️ Project Structure

```
newsapi/
├── main.py                 # Main scraper orchestrator
├── news_source.py          # Abstract base class for scrapers
├── requirements.txt        # Python dependencies
├── run_scraper.sh          # Shell script for automation
├── sources/                # Modular news source scrapers
│   ├── __init__.py
│   ├── _template.py       # Template for new sources
│   ├── news24.py
│   ├── kathmandu_post.py
│   ├── ekantipur.py
│   └── nagarik_news.py
├── data/                   # Generated JSON files
│   ├── today.json         # Latest scrape (always current)
│   └── YYYY-MM-DD.json    # Historical date-stamped files
└── .github/
    └── workflows/
        └── scrape-news.yml # Automated scraping workflow
```

## 🔧 Features

✅ **Modular Architecture** - Each news source in a separate, maintainable module  
✅ **Template-Based** - Easy-to-use template for adding new sources  
✅ **Date-Stamped Archives** - Historical data preserved with date-based filenames  
✅ **Automated Updates** - GitHub Actions runs scraper every 4 hours  
✅ **Error Handling** - Graceful failures with detailed logging  
✅ **Unicode Support** - Proper UTF-8 encoding for Nepali Devanagari script  
✅ **No Database Required** - Lightweight JSON file storage  
✅ **GitHub-Hosted** - Free hosting and CDN via GitHub Raw

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Quick Start](docs/QUICK_START.md) | Get up and running in minutes |
| [API Usage Guide](docs/API_USAGE.md) | Complete API documentation with examples |
| [Contributing Guide](docs/CONTRIBUTING.md) | How to add new news sources |
| [Automation Guide](docs/AUTOMATION.md) | Set up automated scraping |

## 📝 Use Cases

- 📱 **News Apps** - Build mobile or web applications with real-time Nepali news
- 📊 **Data Analysis** - Research Nepali media trends and content patterns
- 🤖 **Chatbots** - Integrate news feeds into AI assistants
- 📧 **News Digests** - Create automated news summary emails
- 🔔 **Alert Systems** - Monitor specific topics or keywords
- 📚 **Archive Projects** - Build historical news databases

## 🤝 Contributing

Contributions are welcome! Whether you want to add a new news source, fix bugs, or improve documentation:

1. 📰 **Add News Sources** - See [Contributing Guide](docs/CONTRIBUTING.md)
2. 🐛 **Report Bugs** - Open an [issue](https://github.com/gaurovgiri/newsapi/issues)
3. 💡 **Suggest Features** - Share your ideas in [discussions](https://github.com/gaurovgiri/newsapi/discussions)
4. ⭐ **Star the Repo** - Show your support!

## 📄 License

See [LICENSE](LICENSE) for full details.

## 📞 Support & Community

- 🐛 **Issues**: [GitHub Issues](https://github.com/gaurovgiri/newsapi/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/gaurovgiri/newsapi/discussions)
- 📖 **Documentation**: [docs/](docs/)

## 🙏 Acknowledgments

Special thanks to:
- All Nepali news sources for providing accessible content
- The open-source community for inspiration and tools
- Contributors who help expand and improve this project

---

<div align="center">

**Made with ❤️ for the Nepali developer community**

[⭐ Star on GitHub](https://github.com/gaurovgiri/newsapi) · [📖 Documentation](docs/) · [🐛 Report Bug](https://github.com/gaurovgiri/newsapi/issues)

</div>