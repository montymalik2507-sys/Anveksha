import pytest
import math
from backend.services.statistics import (
    wilson_score_interval,
    calculate_auc,
    calculate_f1,
    evaluate_dataset_performance,
    compare_dataset_performances
)

def test_wilson_score_hand_computed():
    """Validates Wilson score interval against hand-calculated values."""
    # 6 successes out of 8 trials: center ~0.6689, lower ~0.4093, upper ~0.9285
    lower, upper = wilson_score_interval(6, 8)
    assert math.isclose(lower, 0.4093, abs_tol=1e-3)
    assert math.isclose(upper, 0.9285, abs_tol=1e-3)

def test_wilson_score_boundary_conditions():
    # 0 out of 10
    lower_zero, upper_zero = wilson_score_interval(0, 10)
    assert lower_zero == 0.0
    assert upper_zero > 0.0

    # 10 out of 10
    lower_full, upper_full = wilson_score_interval(10, 10)
    assert lower_full < 1.0
    assert upper_full == 1.0

def test_evaluate_dataset_performance_metrics():
    y_true = [1, 1, 1, 1, 0, 0, 0, 0]
    y_prob = [0.9, 0.8, 0.7, 0.4, 0.6, 0.2, 0.1, 0.3]
    # At threshold 0.5:
    # y_pred = [1, 1, 1, 0, 1, 0, 0, 0]
    # TP=3, FN=1, FP=1, TN=3
    res = evaluate_dataset_performance(y_true, y_prob, threshold=0.50)
    
    assert res["sample_size"] == 8
    assert res["positive_count"] == 4
    assert res["negative_count"] == 4
    assert res["confusion_matrix"]["tp"] == 3
    assert res["confusion_matrix"]["fn"] == 1
    assert res["confusion_matrix"]["fp"] == 1
    assert res["confusion_matrix"]["tn"] == 3
    
    assert math.isclose(res["accuracy"]["value"], 0.75, abs_tol=1e-4)
    assert math.isclose(res["sensitivity"]["value"], 0.75, abs_tol=1e-4)
    assert math.isclose(res["specificity"]["value"], 0.75, abs_tol=1e-4)
    assert math.isclose(res["precision"]["value"], 0.75, abs_tol=1e-4)
    assert math.isclose(res["f1"]["value"], 0.75, abs_tol=1e-4)

def test_deterministic_bootstrap():
    """Ensures identical inputs yield strictly identical bootstrap intervals."""
    y_true = [1, 1, 0, 0, 1, 0, 1, 0] * 5
    y_prob = [0.9, 0.8, 0.2, 0.1, 0.7, 0.3, 0.85, 0.15] * 5
    
    res1 = evaluate_dataset_performance(y_true, y_prob, threshold=0.5)
    res2 = evaluate_dataset_performance(y_true, y_prob, threshold=0.5)
    
    assert res1["f1"]["ci_lower"] == res2["f1"]["ci_lower"]
    assert res1["f1"]["ci_upper"] == res2["f1"]["ci_upper"]
    assert res1["auc"]["ci_lower"] == res2["auc"]["ci_lower"]
    assert res1["auc"]["ci_upper"] == res2["auc"]["ci_upper"]

def test_compare_dataset_performances_conditional_headline():
    res_a = {
        "accuracy": {"value": 0.95, "ci_lower": 0.90, "ci_upper": 0.98, "name": "Accuracy"},
        "sensitivity": {"value": 0.94, "ci_lower": 0.88, "ci_upper": 0.97, "name": "Sensitivity"},
        "specificity": {"value": 0.96, "ci_lower": 0.91, "ci_upper": 0.99, "name": "Specificity"},
        "precision": {"value": 0.95, "ci_lower": 0.90, "ci_upper": 0.98, "name": "Precision"},
        "f1": {"value": 0.94, "ci_lower": 0.89, "ci_upper": 0.97, "name": "F1 Score"},
    }
    
    # Dataset B has a statistically significant drop (non-overlapping CIs)
    res_b = {
        "accuracy": {"value": 0.70, "ci_lower": 0.62, "ci_upper": 0.77, "name": "Accuracy"},
        "sensitivity": {"value": 0.65, "ci_lower": 0.55, "ci_upper": 0.74, "name": "Sensitivity"},
        "specificity": {"value": 0.75, "ci_lower": 0.67, "ci_upper": 0.82, "name": "Specificity"},
        "precision": {"value": 0.72, "ci_lower": 0.63, "ci_upper": 0.80, "name": "Precision"},
        "f1": {"value": 0.68, "ci_lower": 0.59, "ci_upper": 0.76, "name": "F1 Score"},
    }
    
    comp = compare_dataset_performances(res_a, res_b)
    assert comp["status"] == "Warning"
    assert "lower performance" in comp["headline"]
    assert comp["metrics"]["accuracy"]["abs_diff_pp"] == -25.0
