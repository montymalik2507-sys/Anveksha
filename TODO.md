# ANVEKSHA: Master Build Checklist (TODO.md)

This checklist tracks every screen, component, rule, done gate, and acceptance criterion for ANVEKSHA.
Items are ticked `[x]` ONLY when concrete evidence exists (test name, command output, or screenshot path).

---

## 1. Non-Negotiable Scientific Integrity Rules
- [ ] `RULE-01`: Research evaluation disclaimer on every report ("Research evaluation. Not clinically validated."). Never diagnose or claim safe/unsafe/approved/certified.
- [ ] `RULE-02`: NO-GO enforcement: Any critical compatibility or data-quality check failure stops prediction/charts/headline. Shows reason and fix instead.
- [ ] `RULE-03`: Separation of measured findings and possible explanations (hypotheses). No causal words ("because", "due to").
- [ ] `RULE-04`: Conditional headlines: Strong headlines appear only when numbers and 95% CIs support it; otherwise "No clear difference found" or "Not enough evidence".
- [ ] `RULE-05`: Demo data banner: Visible amber banner on any demo/sample screen ("Demo data. Numbers on this screen are examples, not an actual evaluation."). Never shown on real runs.
- [ ] `RULE-06`: Model invariance: Unchanged model runs on both datasets. Zero retraining or fine-tuning in codebase.
- [ ] `RULE-07`: Truth in metrics: Never fabricate metrics, counts, or CIs. Show "Not available" with explanation if not computable.
- [ ] `RULE-08`: Truth in checks: Never claim an automatic check that is not implemented. Use status "Not verified" instead.
- [ ] `RULE-09`: Data privacy: Only permitted, de-identified data. Privacy information displayed at upload.

---

## 2. Design System & Tokens
- [ ] `DS-01`: Dark and Light token definitions (CSS variables) matching section 4.1 exactly.
- [ ] `DS-02`: Surface rules: Background triple soft radial glows (teal top-left, saffron top-right, blue bottom 12-16% opacity). Top bar gradient to #15476E with 3px tri-color line (teal, blue, saffron).
- [ ] `DS-03`: Cards & Verdict styling: radius 12, 1px border, 4px rotating top gradient strip (teal->blue, blue->teal, saffron->red). Verdict boxes left border 6px with tinted background.
- [ ] `DS-04`: Button styling: Primary gradient teal-to-blue (radius 10, min height 44, glow shadow). Secondary transparent with 1px border. Focus ring 2px outline with 2px offset.
- [ ] `DS-05`: Logo assets: SVG and transparent PNG of navy hexagon with teal-and-orange "A", pulse line, two small bars (40px bar, 84px home, 160px splash). Live wordmark ANVEKSHA (weight 800, letter spacing 0.14em) and tagline ("Beyond Accuracy." teal, "Across Population." saffron).
- [ ] `DS-06`: Icons & Status language: Lucide icons with stroke 2 rounded. Exact 4 statuses: "Pass" (check, green), "Warning" (exclamation, amber), "Fail" (cross, red), "Not verified" (question mark, neutral grey). Never renamed!
- [ ] `DS-07`: Accessibility: WCAG 2.2 AA contrast >= 4.5:1 (large text 3:1). Reduced-motion support and in-app setting. Accessible icon names and touch targets >= 44px.
- [ ] `DS-08`: Token audit script: Verifies no hard-coded colors outside token definitions.

---

## 3. Global Navigation & Layout
- [ ] `NAV-01`: Desktop sticky top bar: Logo + wordmark + tagline, navigation links (Home, New test, Results, History, Learn), Language button, Settings gear, Profile avatar.
- [ ] `NAV-02`: Mobile responsive layout (< 700px): Compact top bar + bottom tab bar (Home, New test, Results, History, Settings, 44px tall, sticky, blurred background, 3px top active line).
- [ ] `NAV-03`: Workflow stepper: 5 steps (Add data, Check data, Compatibility, Run model, Results) with done, current, next states, clickable completed steps, mobile step summary ("Step 2 of 5: Check data").
- [ ] `NAV-04`: Language selector dropdown: 10 Indian languages (English, Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Kannada, Malayalam, Punjabi) with checkmark, keyboard operable, escape/outside click close.
- [ ] `NAV-05`: Beginner/Expert mode switch: Simple / Detailed view toggle remembered in local state.

---

## 4. Screens Implementation (Desktop & Mobile, All States: Loading, Empty, Error, Success)
- [ ] `UI-01`: Screen 6.1 Intro (Splash): Hexagon pop-in (scale 0.4, 20deg rotation, 1.2s), soft glow loop, wordmark rises (0.8s), tagline fades (1.4s), 160px gradient loading line (1.8s over 1.6s), skippable, respects reduced-motion.
- [ ] `UI-02`: Screen 6.2 Sign In & Create Account: Split layout, left brand panel with tagline "Measure it. Do not assume it.", research disclaimer. Form with validation on blur/submit, role selection, de-identification confirmation checkbox.
- [ ] `UI-03`: Screen 6.3 Home: Hero section, headline "Does your medical AI work on Indian data?", one-line explanation, "Start a new test" & "See an example result" buttons, 3 step cards, trust statement, research footer.
- [ ] `UI-04`: Screen 6.4 Add Your Data (Step 1): Dropzone (drag & drop, browse, paste link), supported file chips (PNG, JPG, DICOM, ZIP, CSV, XLSX, JSON, ONNX, PT), file list with type badge, role dropdown (Foreign data, Indian data, Model), status, problem expansion, privacy panel with immediate file deletion.
- [ ] `UI-05`: Screen 6.5 Describe Your Datasets (Step 1b): Two dataset cards (Foreign vs Indian) with metadata fields, column matching selector (picture ID, label column, positive value), label preview table with missing value flags, required mapping confirmation checkbox.
- [ ] `UI-06`: Screen 6.6 Data Check (Step 2): Headline "Is the Indian data clean?", large verdict, plain-language checklist with statuses & counts, problem images strip with reasons, actions (Remove bad pictures & re-check, Upload fixed data, Download issue list), no proceed anyway button, folded "Why do we check first?".
- [ ] `UI-07`: Screen 6.7 Compatibility (Step 3): Headline "Can we compare these datasets?", GO/NO-GO verdict, cards for 6 compatibility checks with status, reason, evidence, and Next action. Produces Invalid comparison report on NO-GO.
- [ ] `UI-08`: Screen 6.8 Check the Model (Step 4, Part 1): Model verification checklist, settings (positive class, threshold default 0.50, counting unit: image or patient), required no-retraining checkbox, model hash & preprocessing config, folded failure recovery panel.
- [ ] `UI-09`: Screen 6.9 Running (Step 4, Part 2): 5-stage progress table (load data, check labels, run predictions, calculate metrics, build report), progress bar, sample counters, elapsed time, cancel/resume, failure table. Settings saved before run.
- [ ] `UI-10`: Screen 6.10 Result (Step 5): Model name, Data check passed tag, Demo tag if sample data. Simple view (conditional verdict, 3 metric cards with delta bars, chart card, What this means 3-line box, download/new test buttons). Detailed view (full metric table with 95% Wilson/bootstrap CIs, two confusion matrices, disease share note, run record).
- [ ] `UI-11`: Chart Card Component: 5 chart types (Bar, Dot, Line, Radar, Pie), accessibility table/summary, legend, label editing, PNG and SVG export, remembered chart selection. NO-GO hides charts completely.
- [ ] `UI-12`: Screen 6.11 Reports: Valid report (header, sources, compatibility result, findings table, hypotheses in dashed amber box, limitations, recommendations, export PDF/CSV/JSON in neutral print styles). Invalid comparison report (red banner, checks table, remediation guide, buttons).
- [ ] `UI-13`: Screen 6.12 History: Past runs table with date, model, datasets, outcome, report links, search & filter, row checkboxes, side-by-side comparison modal, export selected, rename, delete. Empty state with action.
- [ ] `UI-14`: Screen 6.13 Library: Tabbed library of verified Datasets and Models with metadata, access status, verification badges, add/edit/delete functionality.
- [ ] `UI-15`: Screen 6.14 Learn (Method & Limits): Plain-language guide on measured findings vs hypotheses, known domain shift risks, scope, project guide references (Musa et al., WHO, ICMR IN-CXR), glossary of terms.
- [ ] `UI-16`: Screen 6.15 Settings: Tabs for Profile, Appearance (Light, Dark, System previews, motion toggles), Accessibility (text size, high contrast, status display), Data & Privacy (retention, delete all files, download archive), Account.

---

## 5. Backend Engine & Services
- [ ] `BE-01`: FastAPI application with CORS, user isolation directory management, and SQLite database for runs, datasets, and models.
- [ ] `BE-02`: Data loader service: Format inspection by magic bytes/content, ZIP decompression, DICOM parser (strips PHI metadata and checks for leaks), CSV/XLSX/JSON label parser.
- [ ] `BE-03`: Data quality & validation service: Unreadable/corrupt detection, empty files, missing/invalid labels, body part/view heuristic filter, image quality (blur/exposure checks), perceptual hashing (imagehash) for exact and near-duplicates, patient-level multi-image detection, class counts.
- [ ] `BE-04`: Compatibility checker engine: Evaluates task match, user mapping confirmation, training independence, duplicate/leakage overlap, class sample sizes, and metadata completeness. Issues deterministic GO or NO-GO with evidence.
- [ ] `BE-05`: Inference engine: ONNX runtime integration for real chest X-ray models (ResNet/DenseNet TB screening classifier). Reproducible preprocessing, deterministic random seeds, model SHA-256 hash logging.
- [ ] `BE-06`: Evaluation & statistical engine: Accuracy, Sensitivity (finds sick patients), Specificity (clears healthy patients), Precision, F1, AUC, Confusion matrix. Wilson score 95% confidence intervals for proportions, bootstrap 95% intervals for AUC/F1. Relative and absolute difference calculations.
- [ ] `BE-07`: Report generation service: ReportLab PDF exporter with theme-neutral styling, research disclaimers, findings vs hypotheses blocks, plus CSV and JSON exporters.
- [ ] `BE-08`: Data deletion & privacy enforcement: Full purge of user folder, runs, predictions, cached thumbnails upon user request.

---

## 6. Real Medical Datasets & Test Models
- [ ] `DATA-01`: Verified real chest X-ray TB sample dataset A (foreign baseline: e.g. Montgomery County / Shenzhen de-identified open CXR) with valid TB labels.
- [ ] `DATA-02`: Verified real chest X-ray Indian sample dataset B (ICMR IN-CXR format / Indian clinical sample) with mapped TB labels.
- [ ] `DATA-03`: Real working ONNX TB screening model for inference.
- [ ] `DATA-04`: Curated test dataset with intentional flaws (corrupt image, duplicate image, blank/blurred image, missing label) for dirty data check verification.
- [ ] `DATA-05`: Curated test dataset with incompatible labels (e.g., normal/abnormal vs TB-positive/negative) for compatibility NO-GO verification.

---

## 7. Testing, Auditing & Done Gates (Section 12)
- [ ] `GATE-01`: Every screen in section 6 exists, works with real files, and has loading, empty, error, and success states.
- [ ] `GATE-02`: Dark is default. Light and System work. Theme persists. No screen has individual theme toggle.
- [ ] `GATE-03`: Colors, gradients, icons, motion match section 4. Token audit finds no hardcoded colors outside token file.
- [ ] `GATE-04`: Full workflow runs end-to-end on real permitted datasets and ONNX model, producing report.
- [ ] `GATE-05`: Incompatible pair triggers NO-GO, displays invalid report, produces zero performance charts.
- [ ] `GATE-06`: Deliberately dirty dataset detected, prediction refused, all issues itemized with explanations.
- [ ] `GATE-07`: All numbers computed with 95% CIs and sample sizes. Unit test validates against hand-computed reference values. Rerun gives identical results.
- [ ] `GATE-08`: Chart types (Bar, Dot, Line, Radar, Pie) render, switch correctly, have accessible labels, and export SVG/PNG.
- [ ] `GATE-09`: PDF, CSV, and JSON exports match on-screen numbers, containing run ID, report version, model hash, language, and disclaimers.
- [ ] `GATE-10`: Language switching updates workflow, labels, status words, and exports (English & Hindi full, others partial fallback).
- [ ] `GATE-11`: Playwright responsive screenshots at 390px, 768px, and 1280px in both Dark and Light themes with no overflow/clipping.
- [ ] `GATE-12`: Axe accessibility audit reports zero serious or critical issues. Keyboard-only navigation works end-to-end.
- [ ] `GATE-13`: Demo banner shows on sample data and never on real runs (enforced by test).
- [ ] `GATE-14`: Banned phrases audit: Zero instances of banned words ("safe", "unsafe", "certified", "approved for use", "proves", "because of", "caused by", "AI diagnoses", "any file works").
- [ ] `GATE-15`: Documentation complete: README.md, TODO.md, PROGRESS.md, DECISIONS.md. Final audit passes with zero issues -> `ANVEKSHA_DONE`.
