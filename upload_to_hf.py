#!/usr/bin/env python3
"""
CLI script to migrate/upload all dataset files and Dataset Card to Hugging Face Hub.

Usage:
    python upload_to_hf.py --token <HF_TOKEN> --repo-id thegauravgiri/nepali-news-dataset
    
Or set environment variables:
    export HF_TOKEN="hf_..."
    export HF_REPO_ID="thegauravgiri/nepali-news-dataset"
    python upload_to_hf.py
"""

import argparse
import logging
import os
import sys
from pathlib import Path

from hf_sync import (
    upload_folder_to_hf,
    upload_dataset_card,
    build_parquet_from_json_files,
    DEFAULT_REPO_ID,
    get_hf_token,
    get_hf_repo_id
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Upload Nepali News Dataset to Hugging Face Hub.")
    parser.add_argument(
        "--token",
        type=str,
        default=None,
        help="Hugging Face User Access Token (with Write permission). Alternatively set HF_TOKEN env var."
    )
    parser.add_argument(
        "--repo-id",
        type=str,
        default=None,
        help=f"Hugging Face Dataset Repo ID (default: {DEFAULT_REPO_ID})"
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default="data",
        help="Directory containing JSON dataset files (default: 'data')"
    )

    args = parser.parse_args()

    token = args.token or get_hf_token()
    repo_id = args.repo_id or get_hf_repo_id()
    data_dir = Path(args.data_dir)

    if not token:
        logger.error("Error: No Hugging Face token provided. Pass --token or set HF_TOKEN environment variable.")
        sys.exit(1)

    if not data_dir.exists() or not data_dir.is_dir():
        logger.error("Error: Data directory '%s' does not exist.", data_dir)
        sys.exit(1)

    logger.info("=" * 60)
    logger.info("Starting Nepali News Dataset Migration to Hugging Face")
    logger.info("Target Dataset: https://huggingface.co/datasets/%s", repo_id)
    logger.info("Source Directory: %s", data_dir.resolve())
    logger.info("=" * 60)

    # 1. Build Unified Parquet Dataset
    parquet_path = data_dir / "train.parquet"
    logger.info("Step 1: Building unified Parquet dataset at '%s'...", parquet_path)
    build_parquet_from_json_files(data_dir, parquet_path)

    # 2. Upload Dataset Card (README.md)
    logger.info("Step 2: Uploading Dataset Card (README.md)...")
    card_success = upload_dataset_card(repo_id=repo_id, token=token)
    if not card_success:
        logger.warning("Failed to upload dataset card; continuing with data folder upload...")

    # 3. Upload Data Folder
    logger.info("Step 3: Uploading dataset archive to 'data/' folder...")
    folder_success = upload_folder_to_hf(
        data_dir=data_dir,
        repo_id=repo_id,
        token=token,
        commit_message="📦 Update complete dataset with unified train.parquet and daily JSON archives"
    )

    if folder_success:
        logger.info("=" * 60)
        logger.info("🎉 Dataset Migration Completed Successfully!")
        logger.info("Explore your dataset at: https://huggingface.co/datasets/%s", repo_id)
        logger.info("=" * 60)
    else:
        logger.error("Migration failed. Please check error logs above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
