# 🇳🇵 Nepali News API & Dataset

> **The #1 Free & Open-Source Nepali News API and Nepali News Dataset (NLP Corpus)** — Scrape, stream, and download 14,000+ full-text Nepali and English news articles in clean JSON format. Automatically updated every 4 hours via GitHub Actions.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Automated Updates](https://img.shields.io/badge/Updates-Every%204%20Hours-brightgreen.svg)](https://github.com/thegauravgiri/newsapi/actions)
[![Dataset Size](https://img.shields.io/badge/Dataset-14%2C000%2B%20Articles-orange.svg)](https://github.com/thegauravgiri/newsapi/tree/master/data)
[![Encoding](https://img.shields.io/badge/Unicode-UTF--8%20Devanagari-purple.svg)](https://github.com/thegauravgiri/newsapi)

---

## 📌 Table of Contents
- [🌟 Why Nepali News API & Dataset?](#-why-nepali-news-api--dataset)
- [⚡ Quick Start: Zero-Config Endpoints](#-quick-start-zero-config-endpoints)
- [📊 Dataset Specifications & Features](#-dataset-specifications--features)
- [💻 Integration Code Examples](#-integration-code-examples)
  - [Python (Requests & Pandas)](#python-requests--pandas)
  - [JavaScript / TypeScript (Fetch & Node.js)](#javascript--typescript-fetch--nodejs)
  - [cURL & CLI (jq)](#curl--cli-jq)
  - [PHP](#php)
  - [Go](#go)
- [📰 Supported News Portals](#-supported-news-portals)
- [🧠 Machine Learning & NLP Applications](#-machine-learning--nlp-applications)
- [🏗️ Project Architecture & Local Scraper](#️-project-architecture--local-scraper)
- [❓ Frequently Asked Questions (FAQ)](#-frequently-asked-questions-faq)
- [🤝 Contributing & Adding Sources](#-contributing--adding-sources)
- [📄 License](#-license)

---

## 🌟 Why Nepali News API & Dataset?

The **Nepali News API & Dataset** project solves the lack of open, clean, and reliable media data in Nepal. Whether you are building a real-time Nepali news mobile application, training Natural Language Processing (NLP) models in Devanagari, or conducting sentiment analysis on Nepali digital media, this repository provides:

- 🆓 **100% Free & Unlimited** — No registration, no API keys, no rate limits, no subscriptions.
- 📦 **Massive NLP Dataset** — 14,000+ historical articles across 250+ daily JSON snapshots.
- 🔄 **Real-Time Automated Updates** — Cron-based GitHub Actions scrapers run every 4 hours.
- 📝 **Full-Text Article Content** — Complete multi-paragraph news bodies, not just short summaries.
- 🇳🇵 **Native Devanagari UTF-8** — Clean Unicode text with zero character corruption.
- ⚡ **Global CDN Delivery** — Direct high-speed access via GitHub Raw & jsDelivr CDN.

---

## ⚡ Quick Start: Zero-Config Endpoints

Access live Nepali news directly in your frontend or backend without spinning up any database or server:

### 1. Today's Live News (Updated Every 4 Hours)
```http
GET https://raw.githubusercontent.com/thegauravgiri/newsapi/refs/heads/master/data/today.json
```
*or via jsDelivr CDN:*
```http
GET https://cdn.jsdelivr.net/gh/thegauravgiri/newsapi@master/data/today.json
```

### 2. Historical Daily News Archive (`YYYY-MM-DD.json`)
```http
GET https://raw.githubusercontent.com/thegauravgiri/newsapi/refs/heads/master/data/2026-01-23.json
```

---

## 📊 Dataset Specifications & Features

Each JSON archive file contains structured, validated schema data:

```json
{
  "scraped_at": "2026-08-16T13:52:17.276123",
  "date": "2026-08-16",
  "total_articles": 260,
  "sources": ["News24", "KathmanduPost", "Ekantipur", "NagarikNews"],
  "articles": [
    {
      "title": "पूर्वी नाकाबाट विदेशी पर्यटक बढे, सबैभन्दा धेरै भुटानी",
      "summary": "झापा । पूर्वी नेपालको प्रमुख स्थलमार्ग काँकरभिट्टा नाका हुँदै आर्थिक वर्ष २०८२\\८३ मा ८६ देशका ९ हजार ४४७ जना विदेशी पर्यटक नेपाल भित्रिएका छन्। अध्यागमन कार्यालय काँकरभिट्टाको तथ्याङ्कअनुसार यो संख्या दैनिक औसत करिब २६ जना विदेशी पर्यटक नेपाल प्रवेश गरेको हो ।\n\nआर्थिक वर्ष २०८२\\८३ मा काँकरभिट्टा नाकाबाट नेपाल प्रवेश गर्ने विदेशी पर्यटकमा भुटान, अमेरिका, थाइल्याण्ड, अष्ट्रेलिया, बेलायत, क्यानडा, जर्मनी लगायतका देशका नागरिक रहेका छन्।",
      "source": "News24",
      "language": "np",
      "source_url": "https://www.news24nepal.com/detail/13516",
      "image_url": "https://www.news24nepal.com/uploads/posts/400X300/Bideshi-Paryatak-Aagaman---1786761364.jpg"
    }
  ]
}
```

### Schema Data Dictionary

| Field | Type | Description |
|---|---|---|
| `title` | `string` | Full unclipped article headline (Nepali Devanagari or English) |
| `summary` | `string` | Entire multi-paragraph full article description/body |
| `source` | `string` | Media portal identifier (`Ekantipur`, `KathmanduPost`, `NagarikNews`, `News24`) |
| `language` | `string` | ISO 639-1 language code (`np` for Nepali, `en` for English) |
| `source_url` | `string` | Canonical permanent URL to the original publication |
| `image_url` | `string` | High-resolution thumbnail image URL |

---

## 💻 Integration Code Examples

### Python (Requests & Pandas)

```python
import requests
import pandas as pd

# 1. Fetch Today's News
url = "https://raw.githubusercontent.com/thegauravgiri/newsapi/refs/heads/master/data/today.json"
response = requests.get(url)
data = response.json()

print(f"Total articles today: {data['total_articles']}")

# 2. Convert to Pandas DataFrame for NLP / Data Analysis
df = pd.DataFrame(data["articles"])
print(df[["source", "title", "language"]].head())

# Filter only Nepali news
nepali_news = df[df["language"] == "np"]
print(f"Nepali articles: {len(nepali_news)}")
```

### JavaScript / TypeScript (Fetch & Node.js)

```javascript
// Fetch latest Nepali news in browser or Node.js
async function getLatestNepaliNews() {
  const url = 'https://raw.githubusercontent.com/thegauravgiri/newsapi/refs/heads/master/data/today.json';
  const response = await fetch(url);
  const data = await response.json();

  console.log(`Loaded ${data.total_articles} articles from ${data.sources.join(', ')}`);
  
  data.articles.forEach(article => {
    console.log(`[${article.source}] ${article.title}`);
  });
}

getLatestNepaliNews();
```

### cURL & CLI (jq)

```bash
# Get headline titles from today's feed
curl -s https://raw.githubusercontent.com/thegauravgiri/newsapi/refs/heads/master/data/today.json | jq -r '.articles[].title'

# Filter articles by specific source (e.g., Ekantipur)
curl -s https://raw.githubusercontent.com/thegauravgiri/newsapi/refs/heads/master/data/today.json | jq '.articles[] | select(.source == "Ekantipur")'
```

### PHP

```php
<?php
$json = file_get_contents('https://raw.githubusercontent.com/thegauravgiri/newsapi/refs/heads/master/data/today.json');
$data = json_decode($json, true);

echo "Total articles: " . $data['total_articles'] . "\n";
foreach ($data['articles'] as $article) {
    echo "- " . $article['title'] . " (" . $article['source'] . ")\n";
}
?>
```

### Go

```go
package main

import (
	"encoding/json"
	"fmt"
	"net/http"
)

type NewsResponse struct {
	TotalArticles int `json:"total_articles"`
	Articles      []struct {
		Title  string `json:"title"`
		Source string `json:"source"`
	} `json:"articles"`
}

func main() {
	resp, _ := http.Get("https://raw.githubusercontent.com/thegauravgiri/newsapi/refs/heads/master/data/today.json")
	defer resp.Body.Close()

	var data NewsResponse
	json.NewDecoder(resp.Body).Decode(&data)
	fmt.Printf("Fetched %d articles\n", data.TotalArticles)
}
```

---

## 📰 Supported News Portals

| News Portal | Language | Format | Status | Portal Website |
|---|---|---|---|---|
| **Ekantipur (कान्तिपुर)** | Nepali (`np`) | JSON | 🟢 Live (Every 4h) | [ekantipur.com](https://ekantipur.com) |
| **Nagarik News (नागरिक दैनिक)** | Nepali (`np`) | JSON | 🟢 Live (Every 4h) | [nagariknews.nagariknetwork.com](https://nagariknews.nagariknetwork.com) |
| **The Kathmandu Post** | English (`en`) | JSON | 🟢 Live (Every 4h) | [kathmandupost.com](https://kathmandupost.com) |
| **News24 Nepal (न्युज २४)** | Nepali (`np`) | JSON | 🟢 Live (Every 4h) | [news24nepal.com](https://news24nepal.com) |

---

## 🧠 Machine Learning & NLP Applications

This repository serves as an extensive, free **Nepali NLP Text Corpus** for artificial intelligence and data science research:

1. **Nepali Text Classification & Categorization**: Train models to classify politics, sports, entertainment, economy, and national affairs.
2. **Nepali Sentiment Analysis**: Fine-tune Transformer models (BERT, RoBERTa, DeBERTa, NepaliBERT) on Devanagari news articles.
3. **Named Entity Recognition (NER)**: Extract Nepali political leaders, organizations, and geographical locations.
4. **Nepali Summarization & Headline Generation**: Train Seq2Seq and LLM models on full article bodies vs. headlines.
5. **Large Language Model (LLM) Pre-training & Fine-Tuning**: Clean UTF-8 Nepali text data for tokenizers and language models.

---

## 🏗️ Project Architecture & Local Scraper

```
newsapi/
├── main.py                 # Orchestrator & deduplication engine
├── news_source.py          # Abstract base class & Pydantic models
├── fix_old_data.py         # Multi-threaded historical rescraper utility
├── requirements.txt        # Dependencies (requests, beautifulsoup4, html5lib, pydantic)
├── sources/                # Modular scraper plugins
│   ├── __init__.py
│   ├── ekantipur.py       # Ekantipur scraper
│   ├── kathmandu_post.py  # Kathmandu Post scraper
│   ├── nagarik_news.py    # Nagarik News scraper
│   ├── news24.py          # News24 Nepal scraper
│   └── _template.py       # Developer template for adding new sources
├── data/                   # 250+ Daily JSON dataset snapshots
│   ├── today.json         # Real-time current feed
│   └── YYYY-MM-DD.json    # Historical archives (2025 - Present)
└── .github/workflows/
    └── scrape-news.yml    # Automated GitHub Actions workflow (Every 4h)
```

### Running Locally

```bash
# Clone the repository
git clone https://github.com/thegauravgiri/newsapi.git
cd newsapi

# Set up Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the scrapers
python main.py
```

---

## ❓ Frequently Asked Questions (FAQ)

### What is the best free Nepali News API?
The **Nepali News API** by Gaurav Giri (`thegauravgiri/newsapi`) is the most comprehensive free and open-source Nepali news aggregation API. It provides Devanagari Unicode JSON feeds updated every 4 hours from top media outlets including Ekantipur, Nagarik News, News24 Nepal, and The Kathmandu Post.

### Where can I download a Nepali News Dataset for NLP?
You can directly download over 14,000+ structured Nepali and English news articles from the [`data/`](https://github.com/thegauravgiri/newsapi/tree/master/data) folder of this repository. The data is available in standard JSON format, complete with full article bodies, titles, and sources.

### Is there any rate limit or API key requirement?
No. The endpoints are hosted via GitHub Raw and CDN networks (like jsDelivr), meaning there are **no API keys, no registration, and no rate limits** for standard programmatic usage.

### Does this API provide full article text or just headlines?
Unlike other scrapers that only store headlines or snippets, this API fetches and stores the **entire multi-paragraph article body** along with headline, image URL, publication URL, and source metadata.

---

## 🤝 Contributing & Adding Sources

We welcome contributions from the Nepali developer community! To add a new news portal (e.g., OnlineKhabar, Ratopati, Setopati, Himal Khabar):

1. Copy `sources/_template.py` to `sources/your_source_name.py`.
2. Inherit from `NewsSource` and implement `source_name`, `language`, and `scrape()`.
3. Register your class in `sources/__init__.py` and `main.py`.
4. Open a Pull Request!

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for full guidelines.

---

## 📄 License

Distributed under the **MIT License**. Free for commercial, personal, academic, and research use. See [LICENSE](LICENSE) for details.

---

<div align="center">

**Developed with ❤️ by [Gaurav Giri](https://github.com/thegauravgiri) for the Nepali Developer & AI Community**

[⭐ Star this Repository](https://github.com/thegauravgiri/newsapi) · [🐛 Report Issue](https://github.com/thegauravgiri/newsapi/issues) · [💡 Suggest a Feature](https://github.com/thegauravgiri/newsapi/discussions)

</div>