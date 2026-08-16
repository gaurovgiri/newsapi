# API Usage Guide - Nepali News API & Dataset

Complete reference guide to using the **Nepali News API** and **Nepali News Dataset** for developers, researchers, and applications.

---

## 📍 API Endpoints

### Base URL
```
https://raw.githubusercontent.com/thegauravgiri/newsapi/refs/heads/master/data/
```

*or via jsDelivr CDN:*
```
https://cdn.jsdelivr.net/gh/thegauravgiri/newsapi@master/data/
```

### Available Endpoints

| Endpoint | Description | Example |
|---|---|---|
| `today.json` | Latest real-time aggregated news (updated every 4h) | `.../data/today.json` |
| `YYYY-MM-DD.json` | Historical news snapshot by date | `.../data/2026-01-23.json` |

---

## 📊 Response Format & Schema

```json
{
  "scraped_at": "2026-08-16T13:52:17.276123",
  "date": "2026-08-16",
  "total_articles": 260,
  "sources": [
    "News24",
    "KathmanduPost",
    "Ekantipur",
    "NagarikNews"
  ],
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

### Field Descriptions

| Field | Type | Description |
|---|---|---|
| `scraped_at` | string | ISO-8601 timestamp of when the news scrape executed |
| `date` | string | Publication date in `YYYY-MM-DD` format |
| `total_articles` | integer | Total count of deduplicated articles in this snapshot |
| `sources` | array | List of active news source portals included in the file |
| `articles[].title` | string | Complete article headline |
| `articles[].summary` | string | Entire multi-paragraph article body / description |
| `articles[].source` | string | Name of news organization (`Ekantipur`, `NagarikNews`, `KathmanduPost`, `News24`) |
| `articles[].language` | string | 2-letter language code (`np` for Nepali, `en` for English) |
| `articles[].source_url` | string | Direct link to original online publication |
| `articles[].image_url` | string | High-resolution thumbnail image URL |

---

## 💻 Code Examples

### JavaScript / Node.js
```javascript
async function fetchNepaliNews() {
  const url = 'https://raw.githubusercontent.com/thegauravgiri/newsapi/refs/heads/master/data/today.json';
  const response = await fetch(url);
  const data = await response.json();
  
  console.log(`Total: ${data.total_articles}`);
  data.articles.forEach(article => {
    console.log(`- [${article.source}] ${article.title}`);
  });
}

fetchNepaliNews();
```

### Python
```python
import requests

url = 'https://raw.githubusercontent.com/thegauravgiri/newsapi/refs/heads/master/data/today.json'
data = requests.get(url).json()

print(f"Total articles: {data['total_articles']}")
for article in data['articles']:
    print(f"[{article['source']}] {article['title']}")
```

### cURL with jq
```bash
# Extract only titles
curl -s https://raw.githubusercontent.com/thegauravgiri/newsapi/refs/heads/master/data/today.json | jq -r '.articles[].title'

# Filter by portal
curl -s https://raw.githubusercontent.com/thegauravgiri/newsapi/refs/heads/master/data/today.json | jq '.articles[] | select(.source == "Ekantipur")'
```

---

## 🤝 Questions & Support
Need help or want to request a new feature? [Open an Issue](https://github.com/thegauravgiri/newsapi/issues) on GitHub.
