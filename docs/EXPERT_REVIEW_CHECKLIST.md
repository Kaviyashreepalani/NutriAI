# NutriAI – Expert Review & Clinical Validation Checklist

> **CRITICAL NOTICE**: Before NutriAI is deployed in a live pilot, clinical trial, or public community intervention, this checklist must be reviewed, executed, and signed off by qualified subject-matter experts.

---

## 1. Clinical & Medical Safety Sign-Off (Physician / Haematologist)
- [ ] **Haemoglobin Cut-Offs**: Validate severity cut-offs (< 7.0 g/dL severe, 7.0–9.9 moderate, 10.0–11.9 mild for adolescent girls and non-pregnant women) against latest ICMR and WHO guidelines.
- [ ] **Pregnancy Thresholds**: Validate 11.0 g/dL threshold for pregnant users.
- [ ] **Non-Iron Anaemia Safeguards**: Review logic flagging low MCV with normal/elevated Ferritin (prevention of inappropriate iron loading in thalassaemia minor or anaemia of chronic disease).
- [ ] **Red-Flag Escalation**: Verify that severe symptoms or critical lab anomalies unconditionally trigger medical referral and block prototype formulation generation.
- [ ] **Medical Disclaimers**: Confirm all disclaimers adequately convey that NutriAI provides nutritional support, not medical treatment or diagnosis.

---

## 2. Nutritional Biochemistry & Formulations Sign-Off (Nutritionist / Dietitian)
- [ ] **IFCT 2017 Data Import**: Replace all `data_status='draft'` entries with verified assays from the Indian Food Composition Tables (NIN-ICMR).
- [ ] **Nutrient Reference Values (RDA)**: Verify energy, protein, elemental iron, folate, vitamin B12, vitamin C, and calcium RDAs for girls aged 10–12, 13–15, 16–18, and women 19–35, 36–49.
- [ ] **Bioavailability Calculations**: Review enhancer (ascorbic acid) to iron molar ratios and phytate/tannin inhibitor penalty factors.
- [ ] **HFSS Avoidance**: Validate maximum permissible thresholds for added sugar (< 10% energy), saturated fat (< 10% energy), and sodium (< 100 mg/serving) in prototypes.
- [ ] **Serving Sizes**: Confirm that serving sizes (e.g. 35g bar, 40g laddoo, 30g mix) are practical for daily consumption.

---

## 3. Food Processing & Shelf-Life Sign-Off (Food Technologist)
- [ ] **Formulation Feasibility**: Review ingredient percentages to ensure physical cohesion (binder constraints, moisture levels).
- [ ] **Processing & Storage Instructions**: Audit preparation and storage directions for safe shelf-life in Indian ambient temperatures.
- [ ] **Sensory & Organoleptic Palatability**: Ensure high-iron ingredients (e.g. garden cress seeds, moringa) are balanced with pleasant masking agents (dates, jaggery, cardamom).

---

## 4. Multilingual Translation Sign-Off (Linguistic Reviewers)
- [ ] **Medical Glossary**: Review Tamil (ta), Hindi (hi), Telugu (te), and Malayalam (ml) terms for Haemoglobin, Ferritin, Anaemia, and Bioavailability.
- [ ] **Machine Draft Review**: Verify and transition all `machine_draft` status strings to `expert_reviewed`.

