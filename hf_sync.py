"""
Hugging Face Hub synchronization module for Nepali News Dataset.
Handles downloading existing daily snapshots, uploading updated JSON and Parquet files,
and publishing dataset metadata/card to Hugging Face.
"""

import os
import logging
from pathlib import Path
from typing import Optional, List
from datetime import datetime, timezone
import json

from huggingface_hub import HfApi, hf_hub_download
from huggingface_hub.utils import EntryNotFoundError, RepositoryNotFoundError, HfHubHTTPError

logger = logging.getLogger(__name__)

DEFAULT_REPO_ID = "thegauravgiri/nepali-news-dataset"


def get_hf_token() -> Optional[str]:
    """Retrieve the Hugging Face token from environment variables."""
    return (
        os.environ.get("HF_TOKEN")
        or os.environ.get("HUGGINGFACE_TOKEN")
        or os.environ.get("HUGGING_FACE_HUB_TOKEN")
    )


def get_hf_repo_id() -> str:
    """Retrieve the Hugging Face dataset repository ID."""
    return (
        os.environ.get("HF_REPO_ID")
        or os.environ.get("HF_DATASET_REPO")
        or DEFAULT_REPO_ID
    )


def ensure_hf_repo(repo_id: Optional[str] = None, token: Optional[str] = None) -> bool:
    """
    Ensure the dataset repository exists on Hugging Face Hub.
    Creates it if it does not exist.
    """
    repo_id = repo_id or get_hf_repo_id()
    token = token or get_hf_token()

    if not token:
        logger.warning("No Hugging Face token provided; skipping repo verification/creation.")
        return False

    try:
        api = HfApi(token=token)
        api.create_repo(
            repo_id=repo_id,
            repo_type="dataset",
            private=False,
            exist_ok=True
        )
        logger.info("Hugging Face dataset repository '%s' verified/created.", repo_id)
        return True
    except Exception as e:
        logger.error("Error verifying/creating Hugging Face repo '%s': %s", repo_id, e)
        return False


def download_hf_file(
    filename: str,
    target_path: Path,
    repo_id: Optional[str] = None,
    token: Optional[str] = None
) -> bool:
    """
    Download an existing file from the Hugging Face dataset repository to a local path.
    Used by scrapers to retain daily history on ephemeral runners (e.g. GitHub Actions).
    """
    repo_id = repo_id or get_hf_repo_id()
    token = token or get_hf_token()

    try:
        logger.info("Checking Hugging Face for existing '%s' in %s...", filename, repo_id)
        downloaded_path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            repo_type="dataset",
            token=token
        )
        
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with open(downloaded_path, "rb") as src, open(target_path, "wb") as dst:
            dst.write(src.read())
        
        logger.info("Successfully fetched '%s' from Hugging Face -> %s", filename, target_path)
        return True
    except EntryNotFoundError:
        logger.info("File '%s' does not exist yet on Hugging Face dataset '%s'.", filename, repo_id)
        return False
    except RepositoryNotFoundError:
        logger.warning("Repository '%s' not found on Hugging Face.", repo_id)
        return False
    except Exception as e:
        logger.warning("Could not download '%s' from Hugging Face: %s", filename, e)
        return False


def build_parquet_from_json_files(data_dir: Path, output_file: Path) -> Optional[Path]:
    """
    Build a unified Parquet file from all daily JSON files in data_dir.
    This provides instant streaming and clean Hugging Face Dataset Viewer UI.
    """
    import pandas as pd

    all_rows = []
    for p in sorted(data_dir.glob("20*.json")):
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
                date = data.get("date", p.stem)
                scraped_at = data.get("scraped_at", "")
                for art in data.get("articles", []):
                    all_rows.append({
                        "title": str(art.get("title", "")).strip(),
                        "summary": str(art.get("summary", "")).strip(),
                        "source": str(art.get("source", "")).strip(),
                        "language": str(art.get("language", "np")).strip(),
                        "source_url": str(art.get("source_url", "")).strip(),
                        "image_url": str(art.get("image_url", "")).strip(),
                        "date": str(date),
                        "scraped_at": str(scraped_at)
                    })
        except Exception as e:
            logger.warning("Error reading %s for parquet build: %s", p, e)

    if not all_rows:
        logger.warning("No articles found to build parquet.")
        return None

    df = pd.DataFrame(all_rows)
    df = df.drop_duplicates(subset=["title", "source", "date"])
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_file, index=False)
    logger.info("Built Parquet dataset at %s with %d articles.", output_file, len(df))
    return output_file


def update_parquet_dataset(
    articles: List[dict],
    date_str: str,
    scraped_at: str,
    parquet_path: Path,
    repo_id: Optional[str] = None,
    token: Optional[str] = None
) -> Optional[Path]:
    """
    Append new articles to the Parquet dataset and deduplicate.
    Downloads train.parquet from HF Hub if not available locally.
    """
    import pandas as pd
    repo_id = repo_id or get_hf_repo_id()
    token = token or get_hf_token()

    if not parquet_path.exists():
        download_hf_file("data/train.parquet", parquet_path, repo_id, token)

    existing_df = None
    if parquet_path.exists():
        try:
            existing_df = pd.read_parquet(parquet_path)
        except Exception as e:
            logger.warning("Could not read existing parquet file: %s", e)

    new_rows = []
    for art in articles:
        new_rows.append({
            "title": str(art.get("title", "")).strip(),
            "summary": str(art.get("summary", "")).strip(),
            "source": str(art.get("source", "")).strip(),
            "language": str(art.get("language", "np")).strip(),
            "source_url": str(art.get("source_url", "")).strip(),
            "image_url": str(art.get("image_url", "")).strip(),
            "date": str(art.get("date", date_str)),
            "scraped_at": str(art.get("scraped_at", scraped_at))
        })
    
    new_df = pd.DataFrame(new_rows)
    if existing_df is not None and not existing_df.empty:
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        combined_df = new_df

    combined_df = combined_df.drop_duplicates(subset=["title", "source", "date"])
    parquet_path.parent.mkdir(parents=True, exist_ok=True)
    combined_df.to_parquet(parquet_path, index=False)
    logger.info("Updated parquet dataset at %s (%d total articles)", parquet_path, len(combined_df))
    return parquet_path


def upload_files_to_hf(
    files: List[Path],
    repo_id: Optional[str] = None,
    token: Optional[str] = None,
    commit_message: Optional[str] = None
) -> bool:
    """
    Upload specific files to the Hugging Face dataset repository.
    """
    repo_id = repo_id or get_hf_repo_id()
    token = token or get_hf_token()

    if not token:
        logger.warning("HF_TOKEN not found. Skipping upload to Hugging Face.")
        return False

    if not files:
        logger.warning("No files specified for Hugging Face upload.")
        return False

    try:
        api = HfApi(token=token)
        ensure_hf_repo(repo_id, token)

        if not commit_message:
            timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            commit_message = f"🗞️ Update news data - {timestamp}"

        logger.info("Uploading %d file(s) to Hugging Face dataset '%s'...", len(files), repo_id)

        for file_path in files:
            if not file_path.exists():
                logger.warning("File '%s' does not exist locally; skipping.", file_path)
                continue
            
            if "data" in file_path.parts:
                idx = file_path.parts.index("data")
                path_in_repo = "/".join(file_path.parts[idx:])
            else:
                path_in_repo = f"data/{file_path.name}"

            api.upload_file(
                path_or_fileobj=str(file_path),
                path_in_repo=path_in_repo,
                repo_id=repo_id,
                repo_type="dataset",
                commit_message=commit_message
            )
            logger.info("Uploaded '%s' -> '%s' on Hugging Face.", file_path.name, path_in_repo)

        logger.info("Hugging Face upload completed successfully!")
        return True
    except Exception as e:
        logger.error("Failed to upload files to Hugging Face '%s': %s", repo_id, e)
        return False


def upload_folder_to_hf(
    data_dir: Path,
    repo_id: Optional[str] = None,
    token: Optional[str] = None,
    commit_message: Optional[str] = None
) -> bool:
    """
    Upload the entire data directory to the Hugging Face dataset repository.
    """
    repo_id = repo_id or get_hf_repo_id()
    token = token or get_hf_token()

    if not token:
        logger.error("HF_TOKEN is required to upload dataset to Hugging Face.")
        return False

    if not data_dir.exists():
        logger.error("Directory '%s' does not exist.", data_dir)
        return False

    try:
        api = HfApi(token=token)
        ensure_hf_repo(repo_id, token)

        if not commit_message:
            timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            commit_message = f"📦 Sync news dataset archive - {timestamp}"

        logger.info("Uploading folder '%s' to Hugging Face dataset '%s'...", data_dir, repo_id)
        api.upload_folder(
            folder_path=str(data_dir),
            path_in_repo="data",
            repo_id=repo_id,
            repo_type="dataset",
            commit_message=commit_message
        )
        logger.info("Successfully uploaded folder '%s' to Hugging Face dataset '%s'!", data_dir, repo_id)
        return True
    except Exception as e:
        logger.error("Failed to upload folder to Hugging Face: %s", e)
        return False


def get_dataset_card_content(repo_id: str) -> str:
    """Generate rich README.md content (Dataset Card) for Hugging Face."""
    return f"""---
annotations_creators:
- no-annotation
language:
- ne
- en
license:
- mit
multilinguality:
- multilingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
- summarization
- feature-extraction
task_ids:
- topic-classification
- news-articles-summarization
- news-articles-headline-generation
pretty_name: Nepali News Dataset & Corpus
tags:
- news
- nepali
- nlp
- corpus
- devanagari
- ekantipur
- kathmandu-post
- nagarik-news
- news24
configs:
- config_name: default
  data_files:
  - split: train
    path: "data/train.parquet"
---

# 🇳🇵 Nepali News Dataset & NLP Corpus

> **The comprehensive, open-access Nepali & English News Dataset for NLP and Machine Learning**, automatically aggregated and updated every 4 hours.

- **Repository**: [{repo_id}](https://huggingface.co/datasets/{repo_id})
- **Total Articles**: 15,000+ full-text articles and growing
- **Update Frequency**: Every 4 hours via automated GitHub Actions pipelines
- **Languages**: Nepali (`np` / `ne`) and English (`en`) in clean UTF-8 Devanagari encoding
- **License**: MIT License

---

## ⚡ Free Zero-Config API Endpoints

You can directly fetch real-time and historical news via Hugging Face raw endpoints with no authentication or rate limits:

### 1. Today's Live News (Updated Every 4 Hours)
```http
GET https://huggingface.co/datasets/{repo_id}/raw/main/data/today.json
```

### 2. Historical Daily Archive (`YYYY-MM-DD.json`)
```http
GET https://huggingface.co/datasets/{repo_id}/raw/main/data/2026-08-23.json
```

### 3. Serverless Dataset Query API
```http
GET https://datasets-server.huggingface.co/rows?dataset={repo_id.replace('/', '%2F')}&config=default&split=train&offset=0&limit=100
```

---

## 💻 Usage with Hugging Face `datasets` Library

```python
from datasets import load_dataset

# Load entire corpus out of the box
dataset = load_dataset("{repo_id}")

# View the dataset structure
print(dataset)
print(dataset["train"][0])
```

### Filter Nepali Articles
```python
nepali_news = dataset["train"].filter(lambda row: row["language"] == "np")
print(f"Total Nepali articles: {{len(nepali_news)}}")
```

---

## 📊 Dataset Schema

Each row contains:

| Field | Type | Description |
|---|---|---|
| `title` | `string` | Headline of the news article (Nepali Devanagari or English) |
| `summary` | `string` | Full multi-paragraph body text of the article |
| `source` | `string` | News portal (`Ekantipur`, `KathmanduPost`, `NagarikNews`, `News24`) |
| `language` | `string` | Language code (`np` for Nepali, `en` for English) |
| `source_url` | `string` | Original canonical link to the article |
| `image_url` | `string` | Featured thumbnail / photo URL |
| `date` | `string` | Publication snapshot date (`YYYY-MM-DD`) |
| `scraped_at` | `string` | ISO timestamp of when the article was scraped |

---

## 📰 Supported News Portals

| Portal | Language | Frequency | Website |
|---|---|---|---|
| **Ekantipur (कान्तिपुर)** | Nepali (`np`) | Every 4 Hours | [ekantipur.com](https://ekantipur.com) |
| **Nagarik News (नागरिक दैनिक)** | Nepali (`np`) | Every 4 Hours | [nagariknews.nagariknetwork.com](https://nagariknews.nagariknetwork.com) |
| **The Kathmandu Post** | English (`en`) | Every 4 Hours | [kathmandupost.com](https://kathmandupost.com) |
| **News24 Nepal (न्युज २४)** | Nepali (`np`) | Every 4 Hours | [news24nepal.com](https://news24nepal.com) |

---

## 📄 License
This dataset is published under the [MIT License](https://opensource.org/licenses/MIT).
"""


def upload_dataset_card(
    repo_id: Optional[str] = None,
    token: Optional[str] = None
) -> bool:
    """
    Generate and upload the dataset README.md (Dataset Card) to Hugging Face.
    """
    repo_id = repo_id or get_hf_repo_id()
    token = token or get_hf_token()

    if not token:
        logger.warning("HF_TOKEN missing; skipping dataset card upload.")
        return False

    try:
        api = HfApi(token=token)
        ensure_hf_repo(repo_id, token)
        content = get_dataset_card_content(repo_id)

        api.upload_file(
            path_or_fileobj=content.encode("utf-8"),
            path_in_repo="README.md",
            repo_id=repo_id,
            repo_type="dataset",
            commit_message="📝 Update Dataset Card README with schema and Parquet config"
        )
        logger.info("Dataset card README.md uploaded successfully to '%s'!", repo_id)
        return True
    except Exception as e:
        logger.error("Failed to upload dataset card: %s", e)
        return False
