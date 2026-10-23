from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_api_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["app"] == "ANVEKSHA"
    assert "Not clinically validated" in data["disclaimer"]

def test_api_compatibility_check():
    payload = {
        "model": {"task": "Pulmonary TB screening"},
        "dataset_a": {
            "label_task": "Pulmonary TB screening",
            "source": "Montgomery County CXR",
            "label_method": "Microbiological culture & expert consensus",
            "population": "De-identified outpatient cohort",
            "equipment": "Standard digital radiography",
            "setting": "Outpatient clinic",
            "positive_count": 58,
            "negative_count": 80
        },
        "dataset_b": {
            "label_task": "Pulmonary TB screening",
            "source": "Indian Hospital Evaluation Cohort",
            "label_method": "GeneXpert & clinical diagnosis",
            "population": "Adult screening survey",
            "equipment": "Mobile digital X-ray unit",
            "setting": "District hospital",
            "positive_count": 45,
            "negative_count": 75
        },
        "mapping_confirmed": True
    }
    response = client.post("/api/compatibility/check", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["can_run"] is True
    assert "GO" in res["verdict"]

def test_api_compatibility_nogo_mismatch():
    payload = {
        "model": {"task": "Pulmonary TB screening"},
        "dataset_a": {"label_task": "Pulmonary TB screening", "positive_count": 20, "negative_count": 20},
        "dataset_b": {"label_task": "Normal vs Abnormal", "positive_count": 20, "negative_count": 20},
        "mapping_confirmed": True
    }
    response = client.post("/api/compatibility/check", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["can_run"] is False
    assert res["verdict"] == "NO-GO"
