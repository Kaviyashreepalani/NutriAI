"""Seed data for Recommended Dietary Allowances (RDA) reference values across life stages.

Tagged status='draft' with source_document='PLACEHOLDER_DEMO' until validated by a licensed nutritionist.
"""
from datetime import date

NUTRIENT_REFERENCES_SEED = [
    # 1. Adolescent Girls 10-12 years
    {"nutrient_code": "energy", "life_stage": "girl_10_12", "value": 2060.0, "unit": "kcal"},
    {"nutrient_code": "protein", "life_stage": "girl_10_12", "value": 33.0, "unit": "g"},
    {"nutrient_code": "iron", "life_stage": "girl_10_12", "value": 16.0, "unit": "mg"},
    {"nutrient_code": "folate", "life_stage": "girl_10_12", "value": 170.0, "unit": "ug"},
    {"nutrient_code": "vit_c", "life_stage": "girl_10_12", "value": 50.0, "unit": "mg"},
    {"nutrient_code": "calcium", "life_stage": "girl_10_12", "value": 850.0, "unit": "mg"},
    {"nutrient_code": "b12", "life_stage": "girl_10_12", "value": 1.2, "unit": "ug"},

    # 2. Adolescent Girls 13-15 years
    {"nutrient_code": "energy", "life_stage": "girl_13_15", "value": 2400.0, "unit": "kcal"},
    {"nutrient_code": "protein", "life_stage": "girl_13_15", "value": 43.0, "unit": "g"},
    {"nutrient_code": "iron", "life_stage": "girl_13_15", "value": 22.0, "unit": "mg"},
    {"nutrient_code": "folate", "life_stage": "girl_13_15", "value": 225.0, "unit": "ug"},
    {"nutrient_code": "vit_c", "life_stage": "girl_13_15", "value": 65.0, "unit": "mg"},
    {"nutrient_code": "calcium", "life_stage": "girl_13_15", "value": 1000.0, "unit": "mg"},
    {"nutrient_code": "b12", "life_stage": "girl_13_15", "value": 2.2, "unit": "ug"},

    # 3. Adolescent Girls 16-18 years
    {"nutrient_code": "energy", "life_stage": "girl_16_18", "value": 2500.0, "unit": "kcal"},
    {"nutrient_code": "protein", "life_stage": "girl_16_18", "value": 46.0, "unit": "g"},
    {"nutrient_code": "iron", "life_stage": "girl_16_18", "value": 26.0, "unit": "mg"},
    {"nutrient_code": "folate", "life_stage": "girl_16_18", "value": 270.0, "unit": "ug"},
    {"nutrient_code": "vit_c", "life_stage": "girl_16_18", "value": 65.0, "unit": "mg"},
    {"nutrient_code": "calcium", "life_stage": "girl_16_18", "value": 1050.0, "unit": "mg"},
    {"nutrient_code": "b12", "life_stage": "girl_16_18", "value": 2.2, "unit": "ug"},

    # 4. Women of Reproductive Age 19-35 years
    {"nutrient_code": "energy", "life_stage": "woman_19_35", "value": 2130.0, "unit": "kcal"},
    {"nutrient_code": "protein", "life_stage": "woman_19_35", "value": 46.0, "unit": "g"},
    {"nutrient_code": "iron", "life_stage": "woman_19_35", "value": 29.0, "unit": "mg"},
    {"nutrient_code": "folate", "life_stage": "woman_19_35", "value": 220.0, "unit": "ug"},
    {"nutrient_code": "vit_c", "life_stage": "woman_19_35", "value": 65.0, "unit": "mg"},
    {"nutrient_code": "calcium", "life_stage": "woman_19_35", "value": 1000.0, "unit": "mg"},
    {"nutrient_code": "b12", "life_stage": "woman_19_35", "value": 2.2, "unit": "ug"},

    # 5. Women of Reproductive Age 36-49 years
    {"nutrient_code": "energy", "life_stage": "woman_36_49", "value": 2130.0, "unit": "kcal"},
    {"nutrient_code": "protein", "life_stage": "woman_36_49", "value": 46.0, "unit": "g"},
    {"nutrient_code": "iron", "life_stage": "woman_36_49", "value": 29.0, "unit": "mg"},
    {"nutrient_code": "folate", "life_stage": "woman_36_49", "value": 220.0, "unit": "ug"},
    {"nutrient_code": "vit_c", "life_stage": "woman_36_49", "value": 65.0, "unit": "mg"},
    {"nutrient_code": "calcium", "life_stage": "woman_36_49", "value": 1000.0, "unit": "mg"},
    {"nutrient_code": "b12", "life_stage": "woman_36_49", "value": 2.2, "unit": "ug"},
]

