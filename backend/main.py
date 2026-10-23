import os
import uuid
import json
import datetime
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel

from backend.database import get_db_connection, init_db
from backend.services.statistics import (
    evaluate_dataset_performance,
    compare_dataset_performances
)
from backend.services.compatibility import evaluate_compatibility
from backend.services.data_checker import run_data_check_pipeline

app = FastAPI(
    title="ANVEKSHA Medical AI Reliability Assessment API",
    description="Research evaluation platform testing medical AI generalization across healthcare settings.",
    version="1.0.0"
)

# Enable CORS for Vite frontend (http://localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database schema
init_db()

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "app": "ANVEKSHA",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "disclaimer": "Research evaluation. Not clinically validated."
    }

@app.get("/api/runs")
def list_runs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, created_at, model_name, dataset_a_name, dataset_b_name, is_demo, outcome, status FROM runs ORDER BY created_at DESC")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"runs": rows}

@app.get("/api/runs/{run_id}")
def get_run_details(run_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM runs WHERE id = ?", (run_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Run not found")
        
    data = dict(row)
    if data.get("metrics_json"):
        data["metrics"] = json.loads(data["metrics_json"])
    if data.get("compatibility_json"):
        data["compatibility"] = json.loads(data["compatibility_json"])
    if data.get("data_checks_json"):
        data["data_checks"] = json.loads(data["data_checks_json"])
    if data.get("settings_json"):
        data["settings"] = json.loads(data["settings_json"])
        
    return data

@app.delete("/api/runs/{run_id}")
def delete_run(run_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM runs WHERE id = ?", (run_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted", "id": run_id}

@app.post("/api/compatibility/check")
def check_compatibility(payload: Dict[str, Any]):
    model = payload.get("model", {})
    ds_a = payload.get("dataset_a", {})
    ds_b = payload.get("dataset_b", {})
    mapping_confirmed = payload.get("mapping_confirmed", False)
    
    result = evaluate_compatibility(
        model_metadata=model,
        dataset_a=ds_a,
        dataset_b=ds_b,
        mapping_confirmed_by_user=mapping_confirmed,
        training_hashes_provided=payload.get("training_hashes_provided", False),
        overlap_count=payload.get("overlap_count", 0),
        patient_ids_available=payload.get("patient_ids_available", False)
    )
    return result

@app.post("/api/data-check/run")
def check_data(payload: Dict[str, Any]):
    images = payload.get("images", [])
    # Run data checker pipeline
    result = run_data_check_pipeline(images_data=images)
    return result

@app.post("/api/privacy/purge")
def purge_all_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM runs WHERE is_demo = 0")
    cursor.execute("DELETE FROM datasets WHERE is_demo = 0")
    cursor.execute("DELETE FROM models WHERE id NOT LIKE 'demo-%'")
    conn.commit()
    conn.close()
    return {
        "status": "purged",
        "message": "All user uploaded datasets, prediction records, and temporary files have been permanently erased."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
