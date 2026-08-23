# 🇳🇵 Nepali News API & Dataset

> **The #1 Free & Open-Source Nepali News API and NLP Dataset Corpus** — Scrape, stream, and download 14,000+ full-text Nepali and English news articles in clean JSON format. Hosted natively on **Hugging Face Datasets** and automatically updated every 4 hours via GitHub Actions.

[![Hugging Face Dataset](https://img.shields.io/badge/🤗%20Hugging%20Face-Dataset-yellow.svg)](https://huggingface.co/datasets/thegauravgiri/nepali-news-dataset)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Automated Updates](https://img.shields.io/badge/Updates-Every%204%20Hours-brightgreen.svg)](https://github.com/thegauravgiri/newsapi/actions)
[![Dataset Size](https://img.shields.io/badge/Dataset-14%2C000%2B%20Articles-orange.svg)](https://huggingface.co/datasets/thegauravgiri/nepali-news-dataset)
[![Encoding](https://img.shields.io/badge/Unicode-UTF--8%20Devanagari-purple.svg)](https://huggingface.co/datasets/thegauravgiri/nepali-news-dataset)

---

## 📌 Table of Contents
- [🌟 Why Nepali News API & Dataset?](#-why-nepali-news-api--dataset)
- [⚡ Free Zero-Config API Endpoints](#-free-zero-config-api-endpoints)
- [🤗 Hugging Face `datasets` Python Library Usage](#-hugging-face-datasets-python-library-usage)
- [📊 Dataset Specifications & Schema](#-dataset-specifications--schema)
- [💻 Integration Code Examples](#-integration-code-examples)
  - [Python (Requests & Pandas)](#python-requests--pandas)
  - [JavaScript / TypeScript (Fetch & Node.js)](#javascript--typescript-fetch--nodejs)
  - [cURL & CLI (jq)](#curl--cli-jq)
  - [PHP](#php)
  - [Go](#go)
- [📰 Supported News Portals](#-supported-news-portals)
- [🧠 Machine Learning & NLP Applications](#-machine-learning--nlp-applications)
- [🏗️ Project Architecture & Automated Sync](#️-project-architecture--automated-sync)
- [⚙️ Setup & Configuration](#️-setup--configuration)
- [❓ Frequently Asked Questions (FAQ)](#-frequently-asked-questions-faq)
- [🤝 Contributing & Adding Sources](#-contributing--adding-sources)
- [📄 License](#-license)

---

## 🌟 Why Nepali News API & Dataset?

The **Nepali News API & Dataset** project solves the lack of open, clean, and reliable media data in Nepal. Whether you are building a real-time Nepali news mobile application, training Natural Language Processing (NLP) models in Devanagari, or conducting sentiment analysis on Nepali digital media, this repository provides:

- 🆓 **100% Free & Unlimited** — No registration, no API keys, no rate limits, no subscriptions.
- 🤗 **Hosted on Hugging Face Hub** — Explore, preview, and load directly with `datasets.load_dataset("thegauravgiri/nepali-news-dataset")`.
- 📦 **Massive NLP Dataset** — 14,000+ historical articles across 250+ daily JSON snapshots.
- 🔄 **Real-Time Automated Updates** — Cron-based GitHub Actions scrapers run every 4 hours and push directly to Hugging Face.
- 📝 **Full-Text Article Content** — Complete multi-paragraph news bodies, not just short summaries.
- 🇳🇵 **Native Devanagari UTF-8** — Clean Unicode text with zero character corruption.
- ⚡ **Global High-Speed CDN Delivery** — Direct access via Hugging Face raw endpoints and Dataset Server REST API.

---

## ⚡ Free Zero-Config API Endpoints

Access live Nepali news directly in your frontend or backend applications without setting up databases, servers, or authentication:

### 1. Today's Live News (Updated Every 4 Hours)
```http
GET https://huggingface.co/datasets/thegauravgiri/nepali-news-dataset/raw/main/data/today.json
```
*or permanent resolve URL:*
```http
GET https://huggingface.co/datasets/thegauravgiri/nepali-news-dataset/resolve/main/data/today.json
```

### 2. Historical Daily News Archive (`YYYY-MM-DD.json`)
```http
GET https://huggingface.co/datasets/thegauravgiri/nepali-news-dataset/raw/main/data/2026-08-23.json
```

### 3. Serverless Dataset Query API (REST & Pagination)
```http
GET https://datasets-server.huggingface.co/rows?dataset=thegauravgiri%2Fnepali-news-dataset&config=default&split=train&offset=0&limit=100
```

---

## 🤗 Hugging Face `datasets` Python Library Usage

You can load and filter the dataset directly in Python using the official Hugging Face `datasets` package:

```bash
pip install datasets
```

### Load Today's News
```python
from datasets import load_dataset

# Load today's live feed
dataset = load_dataset(
    "thegauravgiri/nepali-news-dataset",
    data_files="data/today.json",
    field="articles"
)

print(dataset["train"])
print(dataset["train"][0]["title"])
```

### Load Entire Historical Corpus
```python
from datasets import load_dataset

# Load all 250+ daily archives (14,000+ articles)
dataset = load_dataset(
    "thegauravgiri/nepali-news-dataset",
    field="articles"
)

print(f"Total articles in corpus: {len(dataset['train'])}")

# Filter only Nepali language articles
nepali_articles = dataset["train"].filter(lambda x: x["language"] == "np")
print(f"Total Nepali articles: {len(nepali_articles)}")
```

---

## 📊 Dataset Specifications & Schema

Each JSON archive contains structured, validated schema data:

```json
{
  "scraped_at": "2026-08-23T16:53:43.675123",
  "date": "2026-08-23",
  "total_articles": 380,
  "sources": ["News24", "KathmanduPost", "Ekantipur", "NagarikNews"],
  "articles": [
    {
      "title": "दीपंकर बुद्धदेखि शुरु भएको पञ्चदान, दान पारमिताको सम्बन्ध",
      "summary": "काठमाडौँ । प्रत्येक वर्ष भाद्र कृष्ण पञ्चमीका दिन मनाइने पञ्चदान पर्व बौद्ध धर्मावलम्बीहरूले विशेष महत्वका साथ मनाएका छन्...",
      "source": "News24",
      "language": "np",
      "source_url": "https://www.news24nepal.com/detail/13516",
      "image_url": "https://www.news24nepal.com/uploads/posts/400X300/example.jpg"
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

# 1. Fetch Today's News from Hugging Face
url = "https://huggingface.co/datasets/thegauravgiri/nepali-news-dataset/raw/main/data/today.json"
response = requests.get(url)
data = response.json()

print(f"Total articles today: {data['total_articles']}")
print(f"Active sources: {', '.join(data['sources'])}")

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
  const url = 'https://huggingface.co/datasets/thegauravgiri/nepali-news-dataset/raw/main/data/today.json';
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
curl -s https://huggingface.co/datasets/thegauravgiri/nepali-news-dataset/raw/main/data/today.json | jq -r '.articles[].title'

# Filter articles by specific source (e.g., Ekantipur)
curl -s https://huggingface.co/datasets/thegauravgiri/nepali-news-dataset/raw/main/data/today.json | jq '.articles[] | select(.source == "Ekantipur")'
```

### PHP

```php
<?php
$json = file_get_contents('https://huggingface.co/datasets/thegauravgiri/nepali-news-dataset/raw/main/data/today.json');
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
	resp, _ := http.Get("https://huggingface.co/datasets/thegauravgiri/nepali-news-dataset/raw/main/data/today.json")
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

## 🏗️ Project Architecture & Automated Sync

```
newsapi/
├── main.py                 # Orchestrator, deduplication engine & HF uploader
├── hf_sync.py              # Hugging Face Hub sync & Dataset Card generator
├── upload_to_hf.py         # Standalone migration CLI utility
├── news_source.py          # Abstract base class & Pydantic models
├── requirements.txt        # Dependencies (huggingface_hub, requests, beautifulsoup4)
├── sources/                # Modular scraper plugins
│   ├── __init__.py
│   ├── ekantipur.py       # Ekantipur scraper
│   ├── kathmandu_post.py  # Kathmandu Post scraper
│   ├── nagarik_news.py    # Nagarik News scraper
│   ├── news24.py          # News24 Nepal scraper
│   └── _template.py       # Developer template for adding new sources
├── data/                   # Local staging directory (git-ignored)
└── .github/workflows/
    └── scrape-news.yml    # Automated GitHub Actions workflow (Every 4h)
```

```
┌─────────────────────────┐       ┌──────────────────────────────┐
│  GitHub Actions Runner  │ ────> │   Scrape Portals & Merge     │
│  (Cron every 4 hours)   │       │   (Ekantipur, Nagarik, etc.) │
└─────────────────────────┘       └──────────────┬───────────────┘
                                                 │
                                                 ▼
                                  ┌──────────────────────────────┐
                                  │ Push directly via HfApi to   │
                                  │ 🤗 Hugging Face Dataset      │
                                  └──────────────┬───────────────┘
                                                 │
                   ┌─────────────────────────────┴─────────────────────────────┐
                   ▼                                                           ▼
       ┌───────────────────────────┐                               ┌───────────────────────────┐
       │ Free Direct API Endpoints │                               │ datasets.load_dataset()   │
       │ (today.json, YYYY-MM-DD)  │                               │ (Python NLP Pipelines)    │
       └───────────────────────────┘                               └───────────────────────────┘
```

---

## ⚙️ Setup & Configuration

### 1. Configure GitHub Actions Secret
To enable automated updates from GitHub Actions to Hugging Face:
1. Go to your GitHub Repository **Settings** > **Secrets and variables** > **Actions**.
2. Click **New repository secret**.
3. Name: `HF_TOKEN`
4. Value: Your Hugging Face user access token (with **Write** permissions).
5. *(Optional)* Add Repository Variable `HF_REPO_ID` with value `thegauravgiri/nepali-news-dataset`.

### 2. Running Scraper Locally

```bash
# Clone repository
git clone https://github.com/thegauravgiri/newsapi.git
cd newsapi

# Set up Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run scraper (uploads to Hugging Face if HF_TOKEN is set, or saves locally)
export HF_TOKEN="hf_..."
python main.py
```

### 3. Migrating or Uploading Dataset to Hugging Face

```bash
python upload_to_hf.py --token <YOUR_HF_TOKEN> --repo-id thegauravgiri/nepali-news-dataset
```

---

## ❓ Frequently Asked Questions (FAQ)

### What is the best free Nepali News API?
The **Nepali News API** by Gaurav Giri is the most comprehensive free and open-source Nepali news aggregation API and dataset. It provides Devanagari Unicode JSON feeds updated every 4 hours from top media outlets including Ekantipur, Nagarik News, News24 Nepal, and The Kathmandu Post.

### Where can I download the Nepali News Dataset for NLP?
You can directly download over 14,000+ structured Nepali and English news articles from the [Hugging Face Dataset repository](https://huggingface.co/datasets/thegauravgiri/nepali-news-dataset) or load it directly in Python using `datasets.load_dataset("thegauravgiri/nepali-news-dataset", field="articles")`.

### Is there any rate limit or API key requirement?
No. The endpoints are hosted via Hugging Face Hub's global CDN, meaning there are **no API keys, no registration, and no rate limits** for standard programmatic usage.

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

[🤗 Hugging Face Dataset](https://huggingface.co/datasets/thegauravgiri/nepali-news-dataset) · [⭐ Star on GitHub](https://github.com/thegauravgiri/newsapi) · [🐛 Report Issue](https://github.com/thegauravgiri/newsapi/issues)

</div>