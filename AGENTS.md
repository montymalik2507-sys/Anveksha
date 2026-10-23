# ANVEKSHA: Master Build and Polish Prompt (Loop Mode)

For Antigravity or Cursor. Paste this whole document as the first message, or save it as AGENTS.md in the repo root. Also put IndiHealth_AI_Project_Guide.pdf in /docs and read it first. The visual reference is the design canvas: https://claude.ai/artifact/A63sdzacF8Ama5MH4c5QGP

## 0. Role and mission
You are a senior product designer, senior front-end engineer, ML-evaluation engineer and QA lead in one. Build ANVEKSHA (tagline: Beyond Accuracy. Across Population.), a research tool that tests whether an existing medical AI model (first case: chest X-ray TB screening) still works when the data comes from a different setting, such as Indian hospital data.

The product must work end to end with real files. A screen that only looks right but does nothing is a failure.

## 1. Non-negotiable rules (scientific integrity)
These override every other instruction.
1. Never say a model is safe, unsafe, approved, certified or suitable for clinical use. Never diagnose. Every report says: Research evaluation. Not clinically validated.
2. If any critical compatibility or data-quality check fails, the result is NO-GO: no performance chart, no score, no headline. Show the reason and the fix instead.
3. Keep measured findings and possible explanations in separate visual blocks. Causes (equipment, population, labels) are hypotheses unless separate evidence exists. Use no causal words such as because or due to about results.
4. A strong headline (for example the model scores lower on Indian data) appears only when the numbers and their uncertainty support it. Otherwise say no clear difference found or not enough evidence.
5. Demo or sample numbers must always carry a visible banner: Demo data. Numbers on this screen are examples, not an actual evaluation. Real runs never show this banner. Demo and real data never mix.
6. The same unchanged model runs on both datasets. No retraining or fine-tuning anywhere in the code.
7. Never fabricate a metric, count, confidence interval or file result. If something cannot be computed, show Not available and say why.
8. Never claim an automatic check that is not implemented. Use the status Not verified instead.
9. Only permitted, de-identified data. Show privacy information at upload.

## 2. Loop protocol (work until done)
Do not stop after one pass. Work in a loop until every gate in section 12 is green.
1. Read /docs/IndiHealth_AI_Project_Guide.pdf and this file fully.
2. Plan. Create TODO.md : a numbered checklist, one line per screen, component, rule and acceptance criterion in this document. Give each a stable ID (for example UI-07 , RULE-03 ). Create PROGRESS.md for the log.
3. Pick the next unchecked item. Implement only that item.
4. Verify it. Run lint, type-check, unit tests and build. Open the screen in a browser at 390, 768 and 1280 px, in dark and light mode. Take a screenshot of each. Compare against the spec in this document.
5. Fix and re-verify until the item passes. Allow at most 5 attempts per item. After that, write the blocker in PROGRESS.md and move on. Come back to it before finishing.
6. Tick the item in TODO.md only when evidence exists (test name, screenshot path, command output). Never tick on belief.
7. Log one line in PROGRESS.md : ID, what changed, evidence.
8. Repeat from step 3.
9. When all items are ticked, run the final audit (section 13). Fix everything it finds, then rerun the audit. Repeat until the audit finds zero issues.
10. Print ANVEKSHA_DONE only after the audit passes with zero issues. Never print it earlier.

Ask the user a question only if you are blocked by something you cannot create yourself (for example a private key or a missing licence). Otherwise decide, record the decision in DECISIONS.md , and continue. Do not invent placeholder text, fake data or lorem ipsum. Do not delete a test to make it pass.

## 3. Tech stack (default, change only with a written reason)
- Front end: React + TypeScript + Vite. Styling with CSS variables for tokens (plus Tailwind if wanted). Charts: Recharts or hand-written SVG. Icons: lucide-react . Router with one route per screen. i18n: i18next .
- Back end: Python FastAPI. onnxruntime for inference, pandas for tables, Pillow and pydicom for images, imagehash for near-duplicates, reportlab or weasyprint for PDF, SQLite for runs and history.
- Tests: Vitest, Playwright (screenshots and flows), axe-core for accessibility, pytest for the back end.
- Everything runs locally with one command ( npm run dev and uvicorn ). Provide a README.md with setup.

## 4. Design system

### 4.1 Theme
Dark is the default. Settings offers Light, Dark and System. The choice is saved and applies to the whole app, including charts and exported reports. There is no theme switch on individual screens.

Dark tokens: bg #07121F , card #0E2035 , text #EAF3F8 , text-2 #BCCDDA , muted #93A9BA , line #1E3753 , line-2 #193048 , line-3 #4B6A86 , header #0F2B4A , accent teal #3EF0DC , blue #5AA9FF , saffron #F28C1E , button text #06202B . Success bg #0F4A3F text #8FF3D8 . Warning bg #5A3A0B text #FFD08A . Error bg #5A1D1A text #FFC2BB , error line #F0786E .

Light tokens: bg #F4F8FA , card #FFFFFF , text #0D2038 , text-2 #2E4256 , muted #4B6073 , line #D3DEE6 , line-2 #E4ECF1 , line-3 #93A7B6 , header #0D2038 , accent teal #0B7F76 , blue #1D5FA8 , saffron #D97706 , button text #FFFFFF . Success bg #CFF1E6 text #0A4A38 . Warning bg #FDE2B5 text #6B3D00 . Error bg #FAD4D0 text #7A1810 , error line #B3261E .

All text must meet WCAG AA contrast (4.5:1, large text 3:1) in both themes. Check with a script.

### 4.2 Colour and surface rules
- Page background is never flat. Use three soft radial glows: teal at top-left, saffron at top-right, blue at bottom, each about 12 to 16 percent opacity over the bg colour.
- Top bar: gradient from header colour to #15476E , with a 3 px bottom line that runs teal, blue, saffron.
- Cards: radius 12, 1 px line border, soft shadow, a 4 px gradient strip on top. Strip colours rotate by position: teal to blue, blue to teal, saffron to red.
- Primary button: gradient teal to blue, radius 10, min height 44, glow shadow. Secondary button: transparent with a 1 px accent border. Hover lifts 2 px. Focus shows a 2 px accent outline with 2 px offset.
- Hero panel (Home): gradient of teal, blue and saffron mixed 14 to 18 percent into the card colour, with two blurred floating circles and a slow teal glow on the logo. The key phrase uses a teal-to-saffron text gradient.
- Verdict boxes: left border 6 px, a soft tint of the status colour. Amber for warning, red for fail, green for pass.
- Motion: bars grow in 1.1 s, cards lift 3 px on hover, icons scale 1.1 on hover. Honour prefers-reduced-motion and the in-app Reduce motion setting: turn all animation off.

### 4.3 Type and spacing
System UI font stack. Body 15 to 16 px, line height 1.5. Headings 28 (page), 22 to 24 (verdict), 17 to 20 (card). Small text never below 13 px. Spacing scale 4, 8, 12, 16, 20, 24, 32, 48. Page max width 1100 px (900 px for form pages).

### 4.4 Status language (never colour alone)
Every status shows an icon, a word and a colour: Pass (check, green), Warning (exclamation, amber), Fail (cross, red), Not verified (question mark, neutral grey). These four words are used everywhere and are never renamed.

### 4.5 Logo
Use the supplied logo: a navy hexagon with a teal-and-orange "A", a pulse line and two small bars. Provide a transparent-background PNG and SVG of the hexagon (about 40 px in the bar, 84 px on Home, 160 px on the intro). Draw the wordmark ANVEKSHA (weight 800, letter spacing 0.14 em) and the tagline as live text so they follow the theme. Tagline colours: Beyond Accuracy. teal, Across Population. saffron. Alt text: ANVEKSHA logo. Never stretch or recolour the hexagon.

### 4.6 Icons (lucide, stroke 2, rounded)
Sizes: nav 20, mobile tab 22, card header 24, drop zone 30. Each icon has an accessible name. Hover: move up 2 px and scale 1.15 (nav) or rotate 60 degrees (Settings gear only). Active nav item: filled soft background and a 3 px teal underline.
Mapping:
- Home: House
- New test: CirclePlus
- Results: ChartColumn
- History: History
- Learn: BookOpen
- Settings: Settings
- Language: Globe
- Upload: Upload
- Remove: X
- Pass: Check
- Warning: TriangleAlert
- Fail: X
- Not verified: CircleHelp
- Privacy: ShieldCheck
- Dataset: Database
- Model: Cpu
- Report: FileText
- Download: Download
- Compare: GitCompare
- Library: Library
- Re-check: RefreshCw
- Delete: Trash2
- Info: Info

## 5. Global layout and navigation
- Desktop top bar (sticky): logo + wordmark + tagline on the left; links Home, New test, Results, History, Learn in the middle (each icon + label); on the right a language button (globe + code, for example EN), a Settings gear and a profile circle. Exactly one navigation pattern on every screen. No duplicates.
- Mobile (under 700 px): the bar keeps logo, language, gear and avatar. A bottom tab bar shows Home, New test, Results, History, Settings (icon above label, 44 px tall, sticky, blurred background). Active tab: accent colour and a 3 px top line.
- Stepper on every workflow screen: Add data, Check data, Compatibility, Run model, Results. Each step shows done (check), current (gradient, glow) or next (outline). Desktop shows labels. Mobile shows circles plus one line: Step 2 of 5: Check data. Completed steps can be clicked to go back. The current page also shows the eyebrow Step N of 5 and one primary next action.
- Demo banner (amber strip under the bar) on any screen showing sample data.
- Language menu: a dropdown with English, हिन्दी , বাংলা , தமிழ் , తెలుగు , मराठी , ગુજરાતી , ಕನ್ನಡ , മലയാളം , ਪੰਜਾਬੀ . Current language shows a check. Closes on Escape or outside click, and is keyboard operable.
- Beginner and expert views: wherever technical numbers exist, a Simple / Detailed switch (default Simple) shows or hides the advanced block. The choice is remembered.

## 6. Screens (build all, at desktop and mobile)
For every screen provide: loading, empty, error and success states. All copy is plain language. Use the words in section 10.
- 6.1 Intro (splash)
- 6.2 Sign in and Create account
- 6.3 Home
- 6.4 Add your data (Step 1)
- 6.5 Describe your datasets (Step 1b)
- 6.6 Data check (Step 2)
- 6.7 Compatibility (Step 3)
- 6.8 Check the model (Step 4, part 1)
- 6.9 Running (Step 4, part 2)
- 6.10 Result (Step 5)
- 6.11 Reports (Valid report & Invalid comparison report)
- 6.12 History
- 6.13 Library
- 6.14 Learn (Method and limits)
- 6.15 Settings

## 7. Data loader
- Accept the formats in 6.4 (PNG, JPG, DICOM, ZIP; CSV, XLSX, JSON; ONNX, PT). Detect type by content, not only by extension. Reject the rest with a reason.
- Chunked, resumable uploads with progress, cancel and resume.
- Read ZIP and DICOM. Strip or ignore any patient metadata. Warn if identifying fields are found.
- Validation, with exact counts and affected items: unreadable or corrupt files, unsupported formats, empty files, missing or invalid labels, label values outside the declared set, wrong view or body part (heuristic, marked as such), poor quality (blur, blank, over or under exposure), duplicates and near-duplicates (perceptual hash), same-patient multiple images (only when patient IDs exist), class imbalance and class counts.
- Column mapping is configurable and saved with the dataset. Show a label preview before confirming.

## 8. Compatibility checker rules
- Result is one of GO or NO-GO. NO-GO if any check is Fail. Warnings allow GO but are carried into the report. Not verified is shown as a limitation and never as a pass.
- Task match: the model's declared task must equal the label meaning of both datasets. TB-positive or negative is never treated as equal to normal or abnormal.
- Sample size: minimum positives and negatives per dataset are configurable (default provided, shown on screen). Below minimum is a Warning that marks the result low-confidence, or a Fail if zero.
- Every check stores: status, reason, evidence, next action, timestamp. This feeds the check report.

## 9. Inference and evaluation engine
- Run the model unchanged on both datasets with the same preprocessing and threshold. Store model hash, version, preprocessing config, threshold, positive class, dataset versions, count unit, and the random seed if used. Rerunning with the same manifest must give identical predictions.
- Metrics: accuracy, sensitivity, specificity, precision, F1, confusion matrix, and AUC when probabilities exist. Each with sample size and a 95 percent confidence interval (Wilson for proportions, bootstrap for AUC and F1). Show the absolute difference in percentage points and the relative change separately. A difference is described as clear only if intervals support it.
- Count unit is image or patient. With several images per patient, patient-level is the default and the choice is shown.
- Handle: unsupported model, crash, invalid output, out of memory, timeout. Save partial progress and allow resume. Never show a score computed from missing labels.

## 10. Words to use (plain language)
- Overall correct (accuracy)
- Finds sick patients (sensitivity)
- Clears healthy patients (specificity)
- Foreign data and Indian data in beginner views (Dataset A and B in detailed views)
- Pictures, not images, in beginner copy
- Banned phrases: safe, unsafe, certified, approved for use, proves, because of, caused by (for results), AI diagnoses, any file works.

## 11. Cross-cutting requirements
- 11.1 Languages: i18n for English, Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Kannada, Malayalam, Punjabi. Complete English & Hindi. Fallback notice for partial translations. Numbers formatted by locale.
- 11.2 Accessibility: WCAG 2.2 AA. Keyboard navigation, visible focus ring, aria-live errors, touch targets >= 44px, skip link, contrast >= 4.5:1.
- 11.3 Privacy & Security: Isolated per-user storage, retention period, delete all files works, server-side validation.
- 11.4 Quality: Zero console errors, zero typescript errors, fast load.

## 12. Done gates (all must be green)
1. Every screen in section 6 exists, works with real files, and has loading, empty, error and success states.
2. Dark is the default. Light and System work. The theme persists, and no screen has its own theme switch.
3. Colours, gradients, icons and motion match section 4. A token audit finds no hard-coded colours outside the token file.
4. The full workflow runs end to end on a pair of real, permitted datasets and one real ONNX model, and produces a report.
5. A deliberately incompatible pair (for example TB labels versus normal or abnormal) triggers NO-GO and produces no chart.
6. A deliberately dirty dataset (corrupt, mislabelled, duplicate, wrong-view images) is detected, the model refuses to predict, and each problem is explained.
7. All numbers are computed, with intervals and sample sizes. A unit test checks the metrics against hand-computed values. Rerunning the same manifest reproduces identical results.
8. Chart types Bar, Dot, Line, Radar and Pie all render, are labelled, switch correctly, and export.
9. PDF, CSV and JSON exports match the on-screen numbers and carry run ID, report version, model hash and language.
10. Language switching changes the whole workflow and the exports.
11. Playwright screenshots exist for every screen at 390, 768 and 1280 px in both themes, with no overflow, clipping or overlap.
12. axe reports zero serious or critical issues. Keyboard-only run through the whole flow succeeds.
13. The demo banner shows on all sample data and never on real runs. A test enforces it.
14. No banned phrase from section 10 appears anywhere in the code or exports (a test greps for them).
15. README, TODO.md (all ticked with evidence), PROGRESS.md and DECISIONS.md are complete.

## 13. Final audit (run, fix, repeat)
Adversarial check of every flow and edge case. Stop only when a full audit finds zero issues, then print ANVEKSHA_DONE and a one-page summary.
