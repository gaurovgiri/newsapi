# Quick Start Guide

Get up and running with Nepali News API in minutes.

## 🚀 For API Users (No Installation)

If you just want to use the API to get news data, no installation is required!

### Get Today's News

**Using cURL:**
```bash
curl https://raw.githubusercontent.com/gaurovgiri/newsapi/refs/heads/master/data/today.json
```

**Using JavaScript:**
```javascript
fetch('https://raw.githubusercontent.com/gaurovgiri/newsapi/refs/heads/master/data/today.json')
  .then(res => res.json())
  .then(data => console.log(data));
```

**Using Python:**
```python
import requests
data = requests.get('https://raw.githubusercontent.com/gaurovgiri/newsapi/refs/heads/master/data/today.json').json()
print(data)
```

### Get News from Specific Date

Replace `YYYY-MM-DD` with your desired date:

```bash
# Example: December 12, 2024
curl https://raw.githubusercontent.com/gaurovgiri/newsapi/refs/heads/master/data/2024-12-12.json
```

### What You Get

A JSON response containing:
- List of articles from multiple Nepali news sources
- Article titles, links, descriptions
- Source information and language
- Scrape timestamp

**That's it!** No API keys, no registration, no limits. 

➡️ For more details, see [API_USAGE.md](./API_USAGE.md)

---

## 🔧 For Contributors (Local Setup)

If you want to run the scraper locally or contribute to the project:

### 1. Prerequisites

- Python 3.11 or higher
- Git
- pip (Python package manager)

### 2. Clone the Repository

```bash
git clone https://github.com/gaurovgiri/newsapi.git
cd newsapi
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies installed:**
- `requests` - HTTP client
- `beautifulsoup4` - HTML parsing
- `lxml` - XML/HTML parser (faster than default)

### 4. Run the Scraper

```bash
python main.py
```

**What happens:**
1. Scrapes articles from all configured news sources
2. Saves results to `data/YYYY-MM-DD.json`
3. Copies results to `data/today.json`

### 5. View Results

```bash
# View today's data
cat data/today.json

# Pretty print with jq (if installed)
cat data/today.json | jq .

# View specific date
cat data/2024-12-12.json
```

### 6. Run on Schedule (Optional)

**Linux/macOS (Cron):**
```bash
# Edit crontab
crontab -e

# Add: Run daily at 6 AM
0 6 * * * cd /path/to/newsapi && /usr/bin/python3 main.py
```

**Windows (Task Scheduler):**
```powershell
schtasks /create /tn "News Scraper" /tr "python C:\path\to\newsapi\main.py" /sc daily /st 06:00
```

➡️ For automation details, see [AUTOMATION.md](./AUTOMATION.md)

---

## 📁 Project Structure

```
newsapi/
├── main.py              # Main entry point
├── news_source.py       # Base class for scrapers
├── requirements.txt     # Python dependencies
├── sources/             # News source scrapers
│   ├── news24.py
│   ├── kathmandu_post.py
│   ├── ekantipur.py
│   └── nagarik_news.py
└── data/                # Generated JSON files
    ├── today.json       # Always current
    └── YYYY-MM-DD.json  # Historical data
```

---

## 📰 Available News Sources

| Source | Language | URL |
|--------|----------|-----|
| News24 | Nepali | [news24nepal.tv](https://news24nepal.tv) |
| Kathmandu Post | English | [kathmandupost.com](https://kathmandupost.com) |
| Ekantipur | Nepali | [ekantipur.com](https://ekantipur.com) |
| Nagarik News | Nepali | [nagariknews.nagariknetwork.com](https://nagariknews.nagariknetwork.com) |

---

## 🔥 Quick Examples

### Filter by Source

```python
import requests

data = requests.get('https://raw.githubusercontent.com/gaurovgiri/newsapi/refs/heads/master/data/today.json').json()

# Get only Kathmandu Post articles
kp_articles = [a for a in data['articles'] if a['source'] == 'Kathmandu Post']
print(f"Found {len(kp_articles)} Kathmandu Post articles")
```

### Filter by Language

```javascript
const data = await fetch('https://raw.githubusercontent.com/gaurovgiri/newsapi/refs/heads/master/data/today.json')
  .then(res => res.json());

// Get only Nepali articles
const nepaliNews = data.articles.filter(a => a.language === 'ne');
console.log(`Found ${nepaliNews.length} Nepali articles`);
```

### Search by Keyword

```python
import requests

data = requests.get('https://raw.githubusercontent.com/gaurovgiri/newsapi/refs/heads/master/data/today.json').json()

# Search for keyword in titles
keyword = "काठमाडौं"
results = [a for a in data['articles'] if keyword in a['title']]
print(f"Found {len(results)} articles about {keyword}")
```

---

## 🛟 Troubleshooting

### Can't access the API?
- Check your internet connection
- Verify the URL is correct
- GitHub may be down (check [status.github.com](https://status.github.com))

### Getting 404 for historical date?
- Data only exists for dates when the scraper ran
- The project may not have been running on that date

### Scraper fails locally?
```bash
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Run with verbose logging
python main.py
```

---

## 📚 Next Steps

- **Using the API?** → See [API_USAGE.md](./API_USAGE.md)
- **Adding sources?** → See [CONTRIBUTING.md](./CONTRIBUTING.md)
- **Setting up automation?** → See [AUTOMATION.md](./AUTOMATION.md)

---

## 💡 Quick Tips

✅ **No rate limiting** - Use freely, but be considerate  
✅ **Updates every 4 hours** - No need to poll more frequently  
✅ **Cache locally** - Save bandwidth, improve speed  
✅ **Free forever** - No API keys, no payments  

---

**Ready to build something awesome? Start coding! 🚀**
