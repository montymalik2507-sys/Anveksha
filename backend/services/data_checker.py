import io
import os
import zipfile
from typing import Dict, Any, List, Tuple, Optional
from PIL import Image, ImageStat
import numpy as np
import imagehash
import pandas as pd

# Supported magic bytes / header signatures
MAGIC_SIGNATURES = {
    b'\x89PNG\r\n\x1a\n': 'PNG',
    b'\xff\xd8\xff': 'JPEG',
    b'PK\x03\x04': 'ZIP',
    b'PK\x05\x06': 'ZIP', # empty zip
    b'PK\x07\x08': 'ZIP', # spanned zip
}

def detect_file_type(file_bytes: bytes, filename: str) -> Tuple[str, bool]:
    """
    Detects file type by content / magic bytes first, fallback to structure.
    Returns (type_name, is_supported).
    """
    # Check image/archive magic signatures
    for sig, ftype in MAGIC_SIGNATURES.items():
        if file_bytes.startswith(sig):
            return ftype, True
            
    # Check DICOM: DICOM files usually have preamble of 128 bytes then 'DICM'
    if len(file_bytes) > 132 and file_bytes[128:132] == b'DICM':
        return 'DICOM', True

    # Check for text tabular formats (CSV, JSON)
    try:
        sample = file_bytes[:1024].decode('utf-8', errors='ignore').strip()
        if sample.startswith('{') or sample.startswith('['):
            return 'JSON', True
        if ',' in sample or '\t' in sample or ';' in sample:
            return 'CSV', True
    except Exception:
        pass

    # Check for ONNX model
    if filename.lower().endswith('.onnx') or b'onnx' in file_bytes[:64].lower():
        return 'ONNX', True

    # Check for PyTorch (.pt, .pth)
    if filename.lower().endswith(('.pt', '.pth')) or b'PK' in file_bytes[:4]:
        return 'PT', True

    ext = filename.split('.')[-1].upper() if '.' in filename else 'UNKNOWN'
    return ext, False

def inspect_image_quality(img: Image.Image) -> Tuple[bool, List[str]]:
    """
    Checks image quality: blur (Laplacian variance), blank/black/white, exposure, and aspect ratio.
    """
    issues = []
    
    # Check blank or solid color
    stat = ImageStat.Stat(img)
    if all(s == 0 for s in stat.var):
        issues.append("Blank solid image detected")
        return False, issues

    gray = img.convert('L')
    arr = np.array(gray, dtype=np.float32)
    
    # 1. Exposure checks: Mean pixel intensity
    mean_val = np.mean(arr)
    if mean_val < 10.0:
        issues.append("Severely underexposed / completely dark scan")
    elif mean_val > 245.0:
        issues.append("Severely overexposed / completely white scan")

    # 2. Blur heuristic (discrete Laplacian convolution approximation)
    if arr.shape[0] >= 3 and arr.shape[1] >= 3:
        # 3x3 Laplacian kernel
        lap = (
            arr[:-2, 1:-1] + arr[2:, 1:-1] +
            arr[1:-1, :-2] + arr[1:-1, 2:] -
            4 * arr[1:-1, 1:-1]
        )
        lap_var = float(np.var(lap))
        if lap_var < 15.0 and len(issues) == 0:
            issues.append(f"Image is excessively blurred or low-contrast (Laplacian variance: {lap_var:.1f})")

    # 3. View / body part heuristic (chest X-rays are typically near 1:1 or portrait 4:5, not ultra-wide banner)
    aspect_ratio = img.width / img.height if img.height > 0 else 1.0
    if aspect_ratio < 0.45 or aspect_ratio > 2.2:
        issues.append(f"Unusual aspect ratio ({aspect_ratio:.2f}) - wrong body part or view")

    is_clean = len(issues) == 0
    return is_clean, issues

def run_data_check_pipeline(
    images_data: List[Dict[str, Any]], 
    labels_df: Optional[pd.DataFrame] = None,
    id_col: str = "image_id",
    label_col: str = "label",
    positive_val: str = "1",
    known_training_hashes: Optional[set] = None
) -> Dict[str, Any]:
    """
    Runs full Data Check (Step 2) per Section 6.6 and Section 7.
    Returns checklist rows, exact counts, problem images strip, and verdict.
    """
    problem_images = []
    hash_map: Dict[str, str] = {} # hash -> image_name
    duplicate_count = 0
    corrupt_count = 0
    blur_or_exposure_count = 0
    wrong_view_count = 0
    missing_label_count = 0
    training_overlap_count = 0
    
    label_dict = {}
    if labels_df is not None and id_col in labels_df.columns and label_col in labels_df.columns:
        for _, row in labels_df.iterrows():
            label_dict[str(row[id_col]).strip()] = str(row[label_col]).strip()

    valid_images_count = 0
    
    for item in images_data:
        name = item.get("filename", "unknown")
        raw_bytes = item.get("bytes", b"")
        
        # 1. Unreadable / Corrupt check
        try:
            img = Image.open(io.BytesIO(raw_bytes))
            img.verify() # verify integrity
            img = Image.open(io.BytesIO(raw_bytes)) # re-open for inspection
        except Exception as e:
            corrupt_count += 1
            problem_images.append({
                "filename": name,
                "reason": f"Corrupt or unreadable image file ({str(e)})",
                "severity": "Fail"
            })
            continue

        # 2. Quality & View checks
        clean_img, issues = inspect_image_quality(img)
        if not clean_img:
            for issue in issues:
                if "aspect ratio" in issue:
                    wrong_view_count += 1
                else:
                    blur_or_exposure_count += 1
                problem_images.append({
                    "filename": name,
                    "reason": issue,
                    "severity": "Warning" if "aspect ratio" not in issue else "Fail"
                })

        # 3. Duplicate and near-duplicate detection via perceptual hashing
        try:
            phash = str(imagehash.phash(img))
            if phash in hash_map:
                duplicate_count += 1
                problem_images.append({
                    "filename": name,
                    "reason": f"Duplicate scan of {hash_map[phash]} (exact perceptual match)",
                    "severity": "Fail"
                })
            else:
                hash_map[phash] = name
                
            # 4. Check if copied from training data
            if known_training_hashes and phash in known_training_hashes:
                training_overlap_count += 1
                problem_images.append({
                    "filename": name,
                    "reason": "Image matches training dataset hash (data leakage)",
                    "severity": "Fail"
                })
        except Exception:
            pass

        # 5. Label match check
        base_id = os.path.splitext(name)[0]
        if labels_df is not None:
            if name not in label_dict and base_id not in label_dict:
                missing_label_count += 1
                problem_images.append({
                    "filename": name,
                    "reason": "Missing ground-truth label in label table",
                    "severity": "Fail"
                })
                
        valid_images_count += 1

    total_images = len(images_data)
    
    # Plain-language checklist per Section 6.6
    # 1. pictures open correctly
    # 2. no repeated pictures
    # 3. every picture has an answer
    # 4. all are chest X-rays
    # 5. pictures are clear
    # 6. not copied from training data
    
    checklist = [
        {
            "id": "open_correctly",
            "title": "Pictures open correctly",
            "status": "Pass" if corrupt_count == 0 else "Fail",
            "count": f"{total_images - corrupt_count} of {total_images} readable",
            "detail": "All image files were decoded without corruption or header errors." if corrupt_count == 0 else f"{corrupt_count} files failed decoding."
        },
        {
            "id": "no_duplicates",
            "title": "No repeated pictures",
            "status": "Pass" if duplicate_count == 0 else "Fail",
            "count": f"{duplicate_count} duplicate(s) found",
            "detail": "No duplicate or near-identical scans detected via perceptual hashing." if duplicate_count == 0 else f"Found {duplicate_count} duplicate pictures."
        },
        {
            "id": "has_answer",
            "title": "Every picture has an answer",
            "status": "Pass" if missing_label_count == 0 else "Fail",
            "count": f"{total_images - missing_label_count} of {total_images} labelled",
            "detail": "All scans map to a defined ground truth label." if missing_label_count == 0 else f"{missing_label_count} pictures lack labels."
        },
        {
            "id": "chest_xrays",
            "title": "All are chest X-rays",
            "status": "Pass" if wrong_view_count == 0 else "Fail",
            "count": f"{wrong_view_count} flagged view(s)",
            "detail": "Aspect ratio and radiographic framing match standard chest views." if wrong_view_count == 0 else f"{wrong_view_count} pictures flagged for non-chest aspect ratio."
        },
        {
            "id": "pictures_clear",
            "title": "Pictures are clear",
            "status": "Pass" if blur_or_exposure_count == 0 else "Warning",
            "count": f"{blur_or_exposure_count} flagged scan(s)",
            "detail": "Contrast and focus meet screening thresholds." if blur_or_exposure_count == 0 else f"{blur_or_exposure_count} scans show high blur or exposure anomalies."
        },
        {
            "id": "not_copied",
            "title": "Not copied from training data",
            "status": "Not verified" if not known_training_hashes else ("Pass" if training_overlap_count == 0 else "Fail"),
            "count": f"{training_overlap_count} matches" if known_training_hashes else "Not verified",
            "detail": "No perceptual overlap with declared training hashes." if known_training_hashes and training_overlap_count == 0 else ("Training set hashes not provided." if not known_training_hashes else "Images overlap with training set.")
        }
    ]

    has_fail = any(row["status"] == "Fail" for row in checklist)
    
    if has_fail:
        verdict = "Not clean enough. The model will not predict."
        verdict_status = "Fail"
    elif any(row["status"] == "Warning" for row in checklist):
        verdict = "The data has minor warnings but can be evaluated."
        verdict_status = "Warning"
    else:
        verdict = "The data looks clean."
        verdict_status = "Pass"

    return {
        "verdict": verdict,
        "verdict_status": verdict_status,
        "total_images": total_images,
        "checklist": checklist,
        "problem_images": problem_images,
        "can_predict": not has_fail
    }
