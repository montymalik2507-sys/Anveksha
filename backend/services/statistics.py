import math
import numpy as np
from typing import Dict, Any, List, Tuple, Optional

def wilson_score_interval(successes: int, total: int, confidence: float = 0.95) -> Tuple[float, float]:
    """
    Computes Wilson score confidence interval for a binomial proportion without continuity correction.
    Section 9: Wilson for proportions.
    """
    if total <= 0:
        return 0.0, 0.0
    
    p = successes / total
    # z for 95% confidence is ~1.95996
    z = 1.959963984540054
    z2 = z * z
    n = total
    
    denominator = 1 + z2 / n
    center = (p + z2 / (2 * n)) / denominator
    spread = z * math.sqrt((p * (1 - p) + z2 / (4 * n)) / n) / denominator
    
    lower = max(0.0, center - spread)
    upper = min(1.0, center + spread)
    if successes == total:
        upper = 1.0
    if successes == 0:
        lower = 0.0
    return float(lower), float(upper)

def bootstrap_metric_ci(
    y_true: List[int],
    y_scores: List[float],
    metric_fn,
    n_iterations: int = 1000,
    seed: int = 42
) -> Tuple[float, float]:
    """
    Percentile bootstrap 95% confidence interval with fixed random seed for reproducibility.
    Section 9: bootstrap for AUC and F1. Rerunning with same manifest must give identical predictions.
    """
    if len(y_true) < 2:
        return 0.0, 0.0
    
    rng = np.random.RandomState(seed)
    y_true_arr = np.array(y_true)
    y_scores_arr = np.array(y_scores)
    n = len(y_true_arr)
    
    scores = []
    for _ in range(n_iterations):
        indices = rng.randint(0, n, size=n)
        sample_y = y_true_arr[indices]
        sample_scores = y_scores_arr[indices]
        # Check if both classes are present in sample for ROC or metric
        if len(np.unique(sample_y)) < 2 and metric_fn.__name__ == 'calculate_auc':
            continue
        try:
            val = metric_fn(sample_y, sample_scores)
            if not math.isnan(val):
                scores.append(val)
        except Exception:
            continue
            
    if len(scores) < 10:
        return 0.0, 0.0
        
    scores.sort()
    lower_idx = int(0.025 * len(scores))
    upper_idx = int(0.975 * len(scores))
    return float(scores[lower_idx]), float(scores[upper_idx])

def calculate_auc(y_true: np.ndarray, y_scores: np.ndarray) -> float:
    """Computes Area Under ROC curve using Mann-Whitney U rank statistic."""
    y_true = np.asarray(y_true)
    y_scores = np.asarray(y_scores)
    
    pos = y_scores[y_true == 1]
    neg = y_scores[y_true == 0]
    
    n_pos = len(pos)
    n_neg = len(neg)
    if n_pos == 0 or n_neg == 0:
        return float('nan')
        
    # Vectorized rank sum
    rank_sum = 0
    for p in pos:
        rank_sum += np.sum(p > neg) + 0.5 * np.sum(p == neg)
        
    return float(rank_sum / (n_pos * n_neg))

def calculate_f1(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    tp = np.sum((y_true == 1) & (y_pred == 1))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    if (2 * tp + fp + fn) == 0:
        return 0.0
    return float((2.0 * tp) / (2.0 * tp + fp + fn))

def evaluate_dataset_performance(
    y_true: List[int],
    y_prob: List[float],
    threshold: float = 0.50
) -> Dict[str, Any]:
    """
    Evaluates predictions against ground truth labels and computes all required metrics with 95% CIs.
    """
    total = len(y_true)
    if total == 0:
        raise ValueError("Cannot evaluate an empty dataset.")
        
    y_pred = [1 if p >= threshold else 0 for p in y_prob]
    
    tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 1)
    tn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 0)
    fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 1)
    fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 0)
    
    positives = tp + fn
    negatives = tn + fp
    predicted_positives = tp + fp
    
    # 1. Overall Correct (Accuracy)
    correct = tp + tn
    acc = correct / total if total > 0 else 0.0
    acc_ci = wilson_score_interval(correct, total)
    
    # 2. Finds sick patients (Sensitivity / Recall)
    sens = tp / positives if positives > 0 else 0.0
    sens_ci = wilson_score_interval(tp, positives) if positives > 0 else (0.0, 0.0)
    
    # 3. Clears healthy patients (Specificity)
    spec = tn / negatives if negatives > 0 else 0.0
    spec_ci = wilson_score_interval(tn, negatives) if negatives > 0 else (0.0, 0.0)
    
    # 4. Precision
    prec = tp / predicted_positives if predicted_positives > 0 else 0.0
    prec_ci = wilson_score_interval(tp, predicted_positives) if predicted_positives > 0 else (0.0, 0.0)
    
    # 5. F1 Score
    f1 = calculate_f1(np.array(y_true), np.array(y_pred))
    f1_ci = bootstrap_metric_ci(
        y_true, 
        y_pred, 
        lambda yt, yp: calculate_f1(yt, (yp >= threshold).astype(int)),
        n_iterations=500
    )
    
    # 6. AUC (Area under ROC curve)
    auc_val = calculate_auc(np.array(y_true), np.array(y_prob))
    auc_ci = bootstrap_metric_ci(
        y_true,
        y_prob,
        lambda yt, yp: calculate_auc(yt, yp),
        n_iterations=500
    )
    
    disease_share = positives / total if total > 0 else 0.0

    return {
        "sample_size": total,
        "positive_count": positives,
        "negative_count": negatives,
        "disease_share": round(disease_share, 4),
        "confusion_matrix": {
            "tp": tp,
            "tn": tn,
            "fp": fp,
            "fn": fn
        },
        "accuracy": {
            "value": round(acc, 4),
            "ci_lower": round(acc_ci[0], 4),
            "ci_upper": round(acc_ci[1], 4),
            "name": "Overall correct (accuracy)"
        },
        "sensitivity": {
            "value": round(sens, 4),
            "ci_lower": round(sens_ci[0], 4),
            "ci_upper": round(sens_ci[1], 4),
            "name": "Finds sick patients (sensitivity)"
        },
        "specificity": {
            "value": round(spec, 4),
            "ci_lower": round(spec_ci[0], 4),
            "ci_upper": round(spec_ci[1], 4),
            "name": "Clears healthy patients (specificity)"
        },
        "precision": {
            "value": round(prec, 4),
            "ci_lower": round(prec_ci[0], 4),
            "ci_upper": round(prec_ci[1], 4),
            "name": "Precision"
        },
        "f1": {
            "value": round(f1, 4),
            "ci_lower": round(f1_ci[0], 4),
            "ci_upper": round(f1_ci[1], 4),
            "name": "F1 Score"
        },
        "auc": {
            "value": round(auc_val, 4) if not math.isnan(auc_val) else None,
            "ci_lower": round(auc_ci[0], 4) if not math.isnan(auc_val) else None,
            "ci_upper": round(auc_ci[1], 4) if not math.isnan(auc_val) else None,
            "name": "ROC AUC"
        }
    }

def compare_dataset_performances(
    res_a: Dict[str, Any],
    res_b: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Compares Dataset A (foreign baseline) with Dataset B (Indian data).
    Calculates absolute difference (percentage points) and relative change.
    Rule 4: A strong headline appears only when numbers and their uncertainty support it.
    Otherwise says 'No clear difference found' or 'Not enough evidence'.
    """
    metrics = ['accuracy', 'sensitivity', 'specificity', 'precision', 'f1']
    comparison = {}
    
    has_clear_drop = False
    has_clear_increase = False
    
    for m in metrics:
        val_a = res_a[m]["value"]
        val_b = res_b[m]["value"]
        ci_a = (res_a[m]["ci_lower"], res_a[m]["ci_upper"])
        ci_b = (res_b[m]["ci_lower"], res_b[m]["ci_upper"])
        
        abs_diff_pp = round((val_b - val_a) * 100, 2)
        rel_change_pct = round(((val_b - val_a) / val_a * 100) if val_a > 0 else 0.0, 2)
        
        # Check if 95% confidence intervals overlap
        intervals_overlap = not (ci_b[1] < ci_a[0] or ci_a[1] < ci_b[0])
        
        if not intervals_overlap:
            if val_b < val_a:
                has_clear_drop = True
                verdict_status = "clear drop"
            else:
                has_clear_increase = True
                verdict_status = "clear increase"
        else:
            verdict_status = "no clear difference"
            
        comparison[m] = {
            "metric": m,
            "name": res_a[m]["name"],
            "dataset_a": val_a,
            "dataset_a_ci": ci_a,
            "dataset_b": val_b,
            "dataset_b_ci": ci_b,
            "abs_diff_pp": abs_diff_pp,
            "rel_change_pct": rel_change_pct,
            "intervals_overlap": intervals_overlap,
            "status": verdict_status
        }
        
    # Formulate conditional headline (Section 1.4 & Rule 4)
    if has_clear_drop:
        headline = "Model shows measurable lower performance on Indian dataset"
        headline_detail = "The 95% confidence intervals for key metrics do not overlap between datasets, confirming an observed performance gap."
        status = "Warning"
    elif has_clear_increase:
        headline = "Model shows measurable higher performance on Indian dataset"
        headline_detail = "The 95% confidence intervals indicate higher observed scores on the Indian dataset."
        status = "Pass"
    else:
        headline = "No clear difference found between datasets"
        headline_detail = "Observed differences are within expected statistical uncertainty (overlapping 95% confidence intervals)."
        status = "Pass"
        
    return {
        "headline": headline,
        "headline_detail": headline_detail,
        "status": status,
        "metrics": comparison
    }
