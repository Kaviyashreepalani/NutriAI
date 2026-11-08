# NutriAI – Medical Safety Framework & Safety Gate

## 1. Core Principles
1. **Nutrition Support Only**: NutriAI is an AI-assisted nutrition platform for dietary formulation. It is **not** a diagnostic device, clinical decision support software, medical prescription, or therapeutic treatment.
2. **Prohibited Vocabulary**:
   - Strictly forbidden in UI and API output: *"treats", "cures", "diagnoses", "prescribes", "medication", "dosage", "clinical remedy"*.
   - Mandated vocabulary: *"supports", "may help meet nutrient needs", "dietary supplement context", "food-based formulation", "laboratory reference range"*.
3. **Prototype Product Notice**: Every product, cart, checkout, and order view must prominently feature the label:
   > **"Prototype product – demo checkout"**
4. **Mandatory Disclaimers**: Displayed on all formulation results, lab reviews, progress tracking, and chatbot conversations:
   > *"NutriAI provides food-based dietary formulations designed to support nutritional adequacy. It does not replace medical advice, diagnosis, or treatment. Changes in laboratory parameters must not be attributed solely to NutriAI products and should be evaluated by a qualified healthcare professional."*

---

## 2. Safety Gate Classification

The safety gate evaluates raw extracted laboratory parameters and user health history before any formulation is attempted.

### Age Boundary
- **Target Population**: Adolescent girls (10–19 years) and women of reproductive age (20–49 years).
- **Out of Range (< 10 or > 49 years)**: Generation is **BLOCKED** with a message directing the user to general nutritional resources or age-appropriate healthcare providers.

### Haemoglobin (Hb) Cut-Offs (Non-Pregnant)
- **Severe (< 7.0 g/dL)**: Action: **`blocked`**. Product generation is halted immediately. A high-priority medical referral alert is presented, instructing immediate consultation with a physician.
- **Moderate (7.0 – 9.9 g/dL)**: Action: **`refer_to_doctor`** (or `caution`). Medical referral guidance provided. Formulation permitted only if `ALLOW_GENERATION_WITH_REFERRAL=true`.
- **Mild (10.0 – 11.9 g/dL)**: Action: **`caution`**. Food-based support recommendation enabled with standard dietary guidance.
- **Normal (>= 12.0 g/dL)**: Action: **`ok`**. Standard maintenance nutrient target (iron 4–5 mg/serving).

### Haemoglobin (Hb) Cut-Offs (Pregnant Women)
- **Severe (< 7.0 g/dL)**: Action: **`blocked`**. Urgent referral.
- **Moderate (7.0 – 9.9 g/dL)**: Action: **`refer_to_doctor`**.
- **Mild (10.0 – 10.9 g/dL)**: Action: **`caution`**.
- **Normal (>= 11.0 g/dL)**: Action: **`ok`**.

---

## 3. Non-Iron Anaemia and Differential Safeguards
Haemoglobin alone cannot establish iron deficiency. NutriAI enforces differential logic:
1. **Low Hb + Normal/High Ferritin (> 150 ng/mL)**:
   - Possible Anaemia of Chronic Disease, inflammation, or haemoglobinopathy (e.g. Thalassaemia minor).
   - **Safeguard**: Iron supplementation target is dampened; warning issued: *"Your ferritin levels suggest iron stores are not depleted. Additional iron may not be indicated; consultation with a haematologist is recommended."*
2. **Low B12 (< 200 pg/mL) or Low Folate (< 4.0 ng/mL)**:
   - Macrocytic anaemia pattern.
   - **Safeguard**: Elevate Vitamin B12 and Folate delivery in formulation targets; note that iron alone will not address megaloblastic patterns.
3. **Low MCV (< 80 fL) with Normal Ferritin**:
   - Suspected haemoglobinopathy trait. High-dose iron is contraindicated.

---

## 4. Hard Allergen Filter Policy
- **Layer 1 (Database Query)**: `WHERE NOT (i.allergens && :user_allergens)`
- **Layer 2 (Linear Programming Solver)**: Allergenic ingredient upper bounds set to `0.0`.
- **Layer 3 (Independent Validator)**: Inspects final ingredient array against active user allergies. Any violation triggers immediate rejection (`ValidationFailure: AllergenDetected`).

