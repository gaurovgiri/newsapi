# Quick Start Guide - Nepali News API & Dataset

Get up and running with the **Nepali News API** and **Nepali News Dataset** in minutes.

## 🚀 For API Consumers (No Installation Required)

Access live Nepali news feeds directly in your applications — no API keys or backend setup needed.

### 1. Get Today's Aggregated News

**Using cURL:**
```bash
curl https://raw.githubusercontent.com/thegauravgiri/newsapi/refs/heads/master/data/today.json
```

**Using JavaScript / TypeScript:**
```javascript
fetch('https://raw.githubusercontent.com/thegauravgiri/newsapi/refs/heads/master/data/today.json')
  .then(res => res.json())
  .then(data => {
    console.log(`Loaded ${data.total_articles} articles from ${data.sources.join(', ')}`);
  });
```

**Using Python:**
```python
import requests

data = requests.get('https://raw.githubusercontent.com/thegauravgiri/newsapi/refs/heads/master/data/today.json').json()
print(f"Total articles today: {data['total_articles']}")
for article in data['articles'][:5]:
    print(f"[{article['source']}] {article['title']}")
```

---

### 2. Access Historical Daily News Datasets

Replace `YYYY-MM-DD` with your desired date:

```bash
# Example: January 23, 2026
curl https://raw.githubusercontent.com/thegauravgiri/newsapi/refs/heads/master/data/2026-01-23.json
```

---

## 🔧 For Developers & Contributors (Local Scraper Setup)

### 1. Clone the Repository
```bash
git clone https://github.com/thegauravgiri/newsapi.git
cd newsapi
```

### 2. Create Virtual Environment & Install Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the Scrapers Locally
```bash
python main.py
```

Results will be saved to `data/today.json` and `data/YYYY-MM-DD.json`.

➡️ For full documentation, see [API_USAGE.md](./API_USAGE.md) and [CONTRIBUTING.md](./CONTRIBUTING.md).
