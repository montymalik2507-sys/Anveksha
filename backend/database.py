import sqlite3
import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional

DB_PATH = Path(__file__).resolve().parent / "anveksha.db"

def get_db_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Runs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS runs (
        id TEXT PRIMARY KEY,
        created_at TEXT NOT NULL,
        model_name TEXT NOT NULL,
        model_hash TEXT NOT NULL,
        dataset_a_name TEXT NOT NULL,
        dataset_b_name TEXT NOT NULL,
        is_demo INTEGER NOT NULL DEFAULT 0,
        outcome TEXT NOT NULL, -- 'Valid comparison' or 'Blocked (NO-GO)'
        status TEXT NOT NULL,  -- 'completed', 'failed', 'running'
        threshold REAL NOT NULL DEFAULT 0.50,
        count_unit TEXT NOT NULL DEFAULT 'image',
        metrics_json TEXT,
        compatibility_json TEXT,
        data_checks_json TEXT,
        settings_json TEXT
    );
    """)

    # Datasets registry
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS datasets (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        source TEXT NOT NULL,
        label_type TEXT NOT NULL,
        access TEXT NOT NULL,
        status TEXT NOT NULL,
        images_count INTEGER NOT NULL DEFAULT 0,
        positive_count INTEGER NOT NULL DEFAULT 0,
        negative_count INTEGER NOT NULL DEFAULT 0,
        is_demo INTEGER NOT NULL DEFAULT 0,
        metadata_json TEXT
    );
    """)

    # Models registry
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS models (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        trained_task TEXT NOT NULL,
        trained_on TEXT NOT NULL,
        file_hash TEXT NOT NULL,
        version TEXT NOT NULL,
        status TEXT NOT NULL,
        documentation TEXT,
        preprocessing_json TEXT
    );
    """)

    conn.commit()
    conn.close()

init_db()
