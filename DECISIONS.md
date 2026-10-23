# ANVEKSHA: Engineering & Design Decisions (DECISIONS.md)

This document records architectural, algorithmic, and design decisions made during the project according to Section 2 of AGENTS.md.

### DEC-001: Architecture & Project Structure
- **Decision:** Split into a modern Vite + React + TypeScript front-end (`frontend/`) and a Python FastAPI back-end (`backend/`).
- **Rationale:** Ensures clean separation of concerns: heavy scientific computations, ONNX inference, DICOM parsing, image hashing, Wilson score interval statistics, and PDF report generation occur on the Python backend; UI rendering, interactive Recharts/SVG charts, internationalization, and accessibility are handled cleanly on the React frontend.

### DEC-002: Statistical Confidence Intervals (Wilson Score & Bootstrap)
- **Decision:** Use Wilson score confidence interval without continuity correction for binomial proportions (accuracy, sensitivity, specificity, precision). Use percentile bootstrap (1,000 iterations, fixed random seed) for composite metrics (F1 score and ROC AUC).
- **Rationale:** Required by Section 9 of AGENTS.md. Wilson score interval prevents impossible bounds (< 0 or > 1) even on small sample sizes.

### DEC-003: Model Storage & Checksumming
- **Decision:** Models are evaluated via standard ONNX runtime (`onnxruntime`). The SHA-256 hash of the `.onnx` model file is computed upon registration and stored in SQLite to guarantee auditability and repeatability.
- **Rationale:** Guarantees scientific integrity (Rule 6: same unchanged model runs on both datasets, zero fine-tuning).

### DEC-004: Internationalization and Script Handling
- **Decision:** Use `i18next` and `react-i18next` supporting 10 languages: English (en), Hindi (hi), Bengali (bn), Tamil (ta), Telugu (te), Marathi (mr), Gujarati (gu), Kannada (kn), Malayalam (ml), Punjabi (pa). English and Hindi have complete translations; other languages fall back to English with a visible notice ("Partly translated").
- **Rationale:** Strictly mandated by Section 5, 6, and 11.1.
