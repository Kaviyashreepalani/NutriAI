"""Epidemiological statistics seed data adhering to honesty policy:
Only verified rows with real citations have numeric values; unverified metrics are seeded with status='pending' and value=None.
"""

STATISTICS_SEED = [
    {
        "metric_name": "Anaemia Prevalence in Adolescent Girls (15–19 years)",
        "value": 59.1,
        "unit": "%",
        "population_group": "Adolescent Girls (15–19)",
        "survey_name": "NFHS-5 (National Family Health Survey)",
        "survey_year": "2019-21",
        "definition": "Percentage of adolescent girls with haemoglobin levels below 12.0 g/dL (adjusted for altitude and smoking).",
        "citation": "International Institute for Population Sciences (IIPS) and ICF. 2021. National Family Health Survey (NFHS-5), India Report.",
        "status": "verified",
    },
    {
        "metric_name": "Anaemia Prevalence in Women of Reproductive Age (15–49 years)",
        "value": 57.0,
        "unit": "%",
        "population_group": "Women (15–49)",
        "survey_name": "NFHS-5 (National Family Health Survey)",
        "survey_year": "2019-21",
        "definition": "Proportion of all women aged 15–49 years with haemoglobin concentration < 12.0 g/dL (non-pregnant) or < 11.0 g/dL (pregnant).",
        "citation": "Ministry of Health and Family Welfare (MoHFW), Government of India. NFHS-5 Compendium.",
        "status": "verified",
    },
    {
        "metric_name": "Anaemia in Pregnant Women (15–49 years)",
        "value": 52.2,
        "unit": "%",
        "population_group": "Pregnant Women (15–49)",
        "survey_name": "NFHS-5",
        "survey_year": "2019-21",
        "definition": "Percentage of pregnant women with haemoglobin below 11.0 g/dL.",
        "citation": "NFHS-5 National Factsheet, MoHFW.",
        "status": "verified",
    },
    # Pending verification metrics (No fabricated numbers)
    {
        "metric_name": "Dietary Iron Intake Adequacy among Rural Adolescent Girls",
        "value": None,
        "unit": "%",
        "population_group": "Rural Adolescents (10–19)",
        "survey_name": "ICMR-NIN Diet & Nutritional Status of Urban and Rural Population",
        "survey_year": "2023",
        "definition": "Percentage of adolescent girls meeting at least 50% of the recommended dietary allowance (RDA) for iron.",
        "citation": "ICMR-National Institute of Nutrition (Awaiting official release extraction)",
        "status": "pending",
    },
    {
        "metric_name": "Adherence Rate to Weekly Iron-Folic Acid Supplementation (WIFS)",
        "value": None,
        "unit": "%",
        "population_group": "School-Going Adolescent Girls",
        "survey_name": "MoHFW Anemia Mukt Bharat Dashboard",
        "survey_year": "2024",
        "definition": "Reported 4-week compliance with school-based supervised WIFS blue tablet distribution.",
        "citation": "MoHFW Anemia Mukt Bharat Quarterly Monitoring (Pending verification)",
        "status": "pending",
    },
    {
        "metric_name": "Global Prevalence Comparison – South Asian Regional Anaemia Burden",
        "value": None,
        "unit": "%",
        "population_group": "Women of Reproductive Age",
        "survey_name": "WHO Global Health Observatory",
        "survey_year": "2023",
        "definition": "Regional comparative burden of moderate-to-severe nutritional anaemia.",
        "citation": "World Health Organization Data Repository (Pending administrative review)",
        "status": "pending",
    },
]

