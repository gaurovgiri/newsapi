# API Usage Guide

Complete guide to using the Nepali News API for developers and applications.

## 📍 API Endpoints

### Base URL
```
https://raw.githubusercontent.com/gaurovgiri/newsapi/refs/heads/master/data/
```

### Available Endpoints

| Endpoint | Description | Example |
|----------|-------------|---------|
| `today.json` | Latest aggregated news | Always returns current day's data |
| `YYYY-MM-DD.json` | Historical news by date | `2024-12-12.json` |

## 🔗 Direct Access

### Get Today's News
```bash
curl https://raw.githubusercontent.com/gaurovgiri/newsapi/refs/heads/master/data/today.json
```

### Get News from Specific Date
```bash
# Format: YYYY-MM-DD.json
curl https://raw.githubusercontent.com/gaurovgiri/newsapi/refs/heads/master/data/2024-12-12.json
```

## 📊 Response Format

### Success Response

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

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `scrape_date` | string | Date when scraping was performed (YYYY-MM-DD) |
| `scrape_time` | string | Time when scraping was performed (HH:MM:SS) |
| `total_articles` | integer | Total number of articles scraped |
| `sources` | array | List of news sources included |
| `articles` | array | Array of article objects |
| `articles[].title` | string | Article headline |
| `articles[].link` | string | Full URL to the article |
| `articles[].description` | string | Article summary or excerpt |
| `articles[].published_date` | string | When the article was published (ISO 8601) |
| `articles[].source` | string | Name of the news source |
| `articles[].language` | string | Language code (`ne` for Nepali, `en` for English) |

## 💻 Code Examples

### JavaScript / Node.js

```javascript
// Using Fetch API (Browser/Node 18+)
async function getTodayNews() {
  const response = await fetch(
    'https://raw.githubusercontent.com/gaurovgiri/newsapi/refs/heads/master/data/today.json'
  );
  const data = await response.json();
  
  console.log(`Total articles: ${data.total_articles}`);
  data.articles.forEach(article => {
    console.log(`${article.title} - ${article.source}`);
  });
}

getTodayNews();
```

```javascript
// Using Axios
const axios = require('axios');

axios.get('https://raw.githubusercontent.com/gaurovgiri/newsapi/refs/heads/master/data/today.json')
  .then(response => {
    const data = response.data;
    console.log(`Found ${data.total_articles} articles`);
  })
  .catch(error => console.error('Error:', error));
```

### Python

```python
import requests
from datetime import datetime

# Get today's news
def get_today_news():
    url = 'https://raw.githubusercontent.com/gaurovgiri/newsapi/refs/heads/master/data/today.json'
    response = requests.get(url)
    data = response.json()
    
    print(f"Total articles: {data['total_articles']}")
    print(f"Sources: {', '.join(data['sources'])}")
    
    for article in data['articles']:
        print(f"\n{article['title']}")
        print(f"Source: {article['source']} | Link: {article['link']}")

# Get news from specific date
def get_news_by_date(date_str):
    url = f'https://raw.githubusercontent.com/gaurovgiri/newsapi/refs/heads/master/data/{date_str}.json'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Example usage
get_today_news()
news = get_news_by_date('2024-12-12')
```

### PHP

```php
<?php
// Get today's news
$url = 'https://raw.githubusercontent.com/gaurovgiri/newsapi/refs/heads/master/data/today.json';
$json = file_get_contents($url);
$data = json_decode($json, true);

echo "Total articles: " . $data['total_articles'] . "\n";

foreach ($data['articles'] as $article) {
    echo $article['title'] . " - " . $article['source'] . "\n";
}
?>
```

### Ruby

```ruby
require 'net/http'
require 'json'

# Get today's news
url = URI('https://raw.githubusercontent.com/gaurovgiri/newsapi/refs/heads/master/data/today.json')
response = Net::HTTP.get(url)
data = JSON.parse(response)

puts "Total articles: #{data['total_articles']}"

data['articles'].each do |article|
  puts "#{article['title']} - #{article['source']}"
end
```

### Go

```go
package main

import (
    "encoding/json"
    "fmt"
    "io/ioutil"
    "net/http"
)

type NewsData struct {
    ScrapeDate    string    `json:"scrape_date"`
    TotalArticles int       `json:"total_articles"`
    Sources       []string  `json:"sources"`
    Articles      []Article `json:"articles"`
}

type Article struct {
    Title         string `json:"title"`
    Link          string `json:"link"`
    Description   string `json:"description"`
    PublishedDate string `json:"published_date"`
    Source        string `json:"source"`
    Language      string `json:"language"`
}

func main() {
    url := "https://raw.githubusercontent.com/gaurovgiri/newsapi/refs/heads/master/data/today.json"
    
    resp, err := http.Get(url)
    if err != nil {
        panic(err)
    }
    defer resp.Body.Close()
    
    body, _ := ioutil.ReadAll(resp.Body)
    
    var data NewsData
    json.Unmarshal(body, &data)
    
    fmt.Printf("Total articles: %d\n", data.TotalArticles)
    for _, article := range data.Articles {
        fmt.Printf("%s - %s\n", article.Title, article.Source)
    }
}
```

### cURL Advanced Examples

```bash
# Get today's news and pretty print
curl -s https://raw.githubusercontent.com/gaurovgiri/newsapi/refs/heads/master/data/today.json | jq .

# Get only article titles
curl -s https://raw.githubusercontent.com/gaurovgiri/newsapi/refs/heads/master/data/today.json | jq -r '.articles[].title'

# Filter by source
curl -s https://raw.githubusercontent.com/gaurovgiri/newsapi/refs/heads/master/data/today.json | jq '.articles[] | select(.source == "News24")'

# Count articles by source
curl -s https://raw.githubusercontent.com/gaurovgiri/newsapi/refs/heads/master/data/today.json | jq -r '.articles | group_by(.source) | .[] | "\(.[0].source): \(length)"'
```

## 🔍 Filtering and Searching

### Filter by Language

```javascript
// Get only Nepali articles
const nepaliArticles = data.articles.filter(article => article.language === 'ne');

// Get only English articles
const englishArticles = data.articles.filter(article => article.language === 'en');
```

### Filter by Source

```python
# Get articles from specific source
kathmandu_post = [a for a in data['articles'] if a['source'] == 'Kathmandu Post']
```

### Search by Keywords

```javascript
// Search articles by keyword in title
function searchArticles(keyword) {
  return data.articles.filter(article => 
    article.title.toLowerCase().includes(keyword.toLowerCase())
  );
}

const covidNews = searchArticles('covid');
```

## 📝 Common Use Cases

### 1. News Feed Widget

```javascript
async function createNewsFeed() {
  const response = await fetch('https://raw.githubusercontent.com/gaurovgiri/newsapi/refs/heads/master/data/today.json');
  const data = await response.json();
  
  const newsContainer = document.getElementById('news-feed');
  
  data.articles.slice(0, 10).forEach(article => {
    const newsItem = document.createElement('div');
    newsItem.innerHTML = `
      <h3><a href="${article.link}" target="_blank">${article.title}</a></h3>
      <p>${article.description}</p>
      <small>${article.source} - ${article.published_date}</small>
    `;
    newsContainer.appendChild(newsItem);
  });
}
```

### 2. News Notification Bot

```python
import requests
import time

def check_for_new_articles(last_count):
    url = 'https://raw.githubusercontent.com/gaurovgiri/newsapi/refs/heads/master/data/today.json'
    response = requests.get(url)
    data = response.json()
    
    current_count = data['total_articles']
    
    if current_count > last_count:
        new_articles = current_count - last_count
        print(f"🔔 {new_articles} new articles available!")
        return current_count
    
    return last_count

# Monitor every 30 minutes
last_count = 0
while True:
    last_count = check_for_new_articles(last_count)
    time.sleep(1800)  # 30 minutes
```

### 3. Historical Data Analysis

```python
from datetime import datetime, timedelta
import requests
import pandas as pd

def get_week_data():
    articles = []
    
    for i in range(7):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        url = f'https://raw.githubusercontent.com/gaurovgiri/newsapi/refs/heads/master/data/{date}.json'
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                articles.extend(data['articles'])
        except:
            continue
    
    # Create DataFrame for analysis
    df = pd.DataFrame(articles)
    print(f"Total articles in last 7 days: {len(df)}")
    print(df.groupby('source').size())
    
    return df

df = get_week_data()
```

## ⚡ Performance Tips

1. **Cache Responses**: Store JSON locally and refresh periodically
2. **Use CDN**: GitHub's CDN ensures fast global access
3. **Minimize Requests**: today.json updates every 4 hours, no need to poll more frequently
4. **Filter Client-Side**: Download full data once, filter as needed
5. **Handle 404s**: Historical dates may not exist, implement error handling

## 🚫 Limitations

- No real-time updates (4-hour refresh cycle)
- No pagination (all articles in single file)
- No authentication required (public access)
- No rate limiting (but please be considerate)
- Historical data availability depends on when scraping started

## 📞 Support

Need help? [Open an issue](https://github.com/gaurovgiri/newsapi/issues) on GitHub.
