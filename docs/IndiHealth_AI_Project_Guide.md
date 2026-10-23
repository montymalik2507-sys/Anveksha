# IndiHealth AI: Improving the Reliability of Medical AI Across Indian Healthcare Settings
*Problem Definition, Existing Approaches, Proposed Solution and Hackathon Roadmap*

**STATUS:** Concept document for a research and evaluation prototype. Not clinically validated; not a diagnostic or certification tool. Prepared from the source document "IndiHealth AI: SIH-Style Problem Statement and Hackathon Roadmap".

---

## 1. Executive Overview
IndiHealth AI is a proposed research and evaluation tool. It helps people check whether an existing medical AI model still performs reliably when tested on data from a different healthcare setting, and whether such a comparison is valid in the first place.

**An analogy:** A student who has studied from one textbook may do very well on that textbook's questions. That does not, by itself, show how they will do on an exam written by a different board. A medical AI model is similar: it learns patterns from the data it was developed on, and those patterns may not transfer equally well to another hospital, region or population.

- **The problem:** Medical AI models are developed and evaluated on data gathered under particular clinical, demographic and technical conditions. In a different healthcare setting their reliability may be uncertain, because the new data can differ in patient characteristics, disease prevalence, imaging characteristics and labelling practices.
- **The proposed solution:** An accessible, evidence-oriented Medical AI Reliability Assessment System. It evaluates an existing model across compatible datasets, identifies measurable performance differences, detects limitations that make comparisons unreliable, and generates a clear report of findings and the further validation required.
- **Intended users:** Medical AI researchers; hospital innovation and clinical evaluation teams; medical AI developers.
- **Core prototype:** Two verified, compatible datasets; one suitable existing model; reproducible predictions and appropriate metrics; at least one meaningful compatibility rule; a clear comparison; a report with findings, limitations and recommended further validation; and an end-to-end demonstration using real, permitted data.
- **Provisional first application:** Pulmonary tuberculosis (TB) screening on chest X-rays is a candidate, not a confirmed choice. It proceeds only if a compatible dataset pairing and a model able to produce valid predictions can be obtained.
- **What it will not do:** Declare a model safe, unsafe or suitable for clinical deployment; diagnose patients; certify models; make patient-care decisions; or connect to live hospital systems.

---

## 2. Background and Unmet Need
A model learns patterns from the data it is trained on. When it meets data from a different hospital, region or population, those patterns may not transfer equally well.

Two chest X-ray datasets can differ in:
1. **Patient characteristics:** Age distribution, underlying conditions and other population characteristics.
2. **Disease distribution:** Frequency and types of conditions represented.
3. **Image acquisition:** Imaging equipment, positioning, image processing and image quality.
4. **Data labelling:** Criteria used to classify a scan as normal, abnormal or disease-positive.
5. **Clinical setting:** Screening populations versus patients already suspected of having a disease.

### Key terms in plain language
- **Label:** The "right answer" attached to an example (e.g., normal, abnormal, TB-positive).
- **Metadata:** Information about the data: where it came from, how labels were assigned, equipment, population, access conditions.
- **Internal testing:** Checking a model on held-out data from the same dataset it was developed on.
- **External validation:** Checking a model on an independent dataset that was not part of its development.
- **Domain shift:** A difference between the data a model was built on and the data it is later used on.
- **Sensitivity:** Of the people who truly have the condition, the share the model correctly flags.
- **Specificity:** Of the people who truly do not have the condition, the share the model correctly clears.
- **Headline accuracy:** One overall score. It can look stable while sensitivity or specificity change underneath it.

---

## 3. Formal Problem Statement
Medical AI models are often developed and evaluated using datasets collected under particular clinical, demographic and technical conditions. When these models are considered for use in different healthcare settings, their reliability may be uncertain because the target data can differ from the development data in patient characteristics, disease prevalence, imaging characteristics and labelling practices.

Currently, evaluating such differences requires suitable datasets, compatible labels, appropriate evaluation methods and expertise in interpreting the results. Comparing headline accuracy scores alone may conceal clinically important changes in sensitivity, specificity or other performance measures.

Develop an accessible, evidence-oriented Medical AI Reliability Assessment System that enables users to evaluate an existing model across compatible datasets, identify measurable performance differences, detect limitations that make comparisons unreliable, and generate a clear report describing the findings and additional validation required.

---

## 4. Initial Clinical Application & Core Decisions
- **Candidate:** Pulmonary tuberculosis (TB) screening using chest X-rays.
- **Caution:** Labels must match the task. Normal vs. Abnormal is NOT equal to TB-positive vs TB-negative.
- **Rule:** Keep measured findings and possible explanations in separate visual blocks. Causes are hypotheses unless separate evidence exists. Avoid causal words like "because" or "due to".

---

## 5. Five-Stage Hackathon Roadmap & Acceptance Criteria
1. **Stage 1: Validate the experiment:** Confirm one workable experiment. Two compatible datasets, one existing model.
2. **Stage 2: Build the evaluation engine:** Reproducible predictions, proper metrics with 95% confidence intervals (Wilson score interval for proportions, bootstrap for AUC/F1).
3. **Stage 3: Implement compatibility checks:** Prevent invalid comparisons. Clear GO / NO-GO decisions.
4. **Stage 4: Build the dashboard and report:** Communicate evidence clearly.
5. **Stage 5: Test and prepare the demonstration:** End-to-end reproducible flow with real data.

### Prototype Acceptance Criteria (from Section 10)
1. Team can explain clinical problem and intended prediction task.
2. Data sources, labels, access conditions and limitations are documented.
3. Model produces predictions for selected evaluation data.
4. Evaluation metrics are calculated correctly and reproducibly.
5. Dashboard identifies genuine dataset-compatibility issue or demonstrates valid cross-dataset comparison.
6. Report distinguishes measured findings from hypotheses and unsupported conclusions.
7. Demonstration clearly states why result matters and what further validation is needed.

---

## 6. References
1. Musa, A., Prasad, R. and Hernández, M. (2025). Addressing cross-population domain shift in chest X-ray classification through supervised adversarial domain adaptation. *Scientific Reports*, 15, 11383. DOI: 10.1038/s41598-025-95390-3
2. World Health Organization (2021). *Ethics and governance of artificial intelligence for health: WHO guidance*. ISBN 9789240029200.
3. ICMR–National Institute for Research in Tuberculosis. IN-CXR: An Open Dataset of Chest Radiography. https://nirt.res.in/incxr
