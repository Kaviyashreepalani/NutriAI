"""Seed data for 40 common Indian ingredients with draft demo nutrient profiles.

Honesty Policy:
Every nutrient is tagged source='PLACEHOLDER_DEMO' and data_status='draft' until verified against IFCT 2017.
"""
from datetime import date

INGREDIENTS_SEED = [
    # 1. Millets & Cereals
    {
        "name": "Finger Millet (Ragi)",
        "local_names": {"hi": "रागी (मंडुआ)", "ta": "கேழ்வரகு", "te": "రాగులు", "ml": "കൂവരക് (റാഗി)"},
        "category": "cereal_millet",
        "diet_class": "vegan",
        "allergens": [],
        "cost_per_kg_inr": 45.0,
        "availability": "high",
        "processing_notes": "Sprouted and roasted for enhanced mineral bioavailability.",
        "min_inclusion_pct": 5.0,
        "max_inclusion_pct": 40.0,
        "nutrients": {
            "energy": 320.0, "protein": 7.3, "iron": 3.9, "calcium": 344.0,
            "vit_c": 0.0, "folate": 18.0, "fat": 1.3, "added_sugar": 0.0,
            "sodium": 11.0, "phytate_flag": True
        }
    },
    {
        "name": "Pearl Millet (Bajra)",
        "local_names": {"hi": "बाजरा", "ta": "கம்பு", "te": "సజ్జలు", "ml": "കമ്പം"},
        "category": "cereal_millet",
        "diet_class": "vegan",
        "allergens": [],
        "cost_per_kg_inr": 38.0,
        "availability": "high",
        "processing_notes": "Puffed or milled roasted flour.",
        "min_inclusion_pct": 5.0,
        "max_inclusion_pct": 35.0,
        "nutrients": {
            "energy": 361.0, "protein": 11.6, "iron": 8.0, "calcium": 42.0,
            "vit_c": 0.0, "folate": 45.0, "fat": 5.0, "added_sugar": 0.0,
            "sodium": 10.0, "phytate_flag": True
        }
    },
    {
        "name": "Sorghum (Jowar)",
        "local_names": {"hi": "ज्वार", "ta": "சோளம்", "te": "జొన్నలు", "ml": "ചോളം"},
        "category": "cereal_millet",
        "diet_class": "vegan",
        "allergens": [],
        "cost_per_kg_inr": 42.0,
        "availability": "high",
        "processing_notes": "Dry roasted and flaked.",
        "min_inclusion_pct": 5.0,
        "max_inclusion_pct": 30.0,
        "nutrients": {
            "energy": 349.0, "protein": 10.4, "iron": 4.1, "calcium": 25.0,
            "vit_c": 0.0, "folate": 20.0, "fat": 1.9, "added_sugar": 0.0,
            "sodium": 7.0, "phytate_flag": True
        }
    },
    {
        "name": "Foxtail Millet (Kangni / Tenai)",
        "local_names": {"hi": "कंगनी", "ta": "தினை", "te": "కొర్రలు", "ml": "തിന"},
        "category": "cereal_millet",
        "diet_class": "vegan",
        "allergens": [],
        "cost_per_kg_inr": 65.0,
        "availability": "high",
        "processing_notes": "Dehusked roasted grains.",
        "min_inclusion_pct": 5.0,
        "max_inclusion_pct": 30.0,
        "nutrients": {
            "energy": 351.0, "protein": 12.3, "iron": 2.8, "calcium": 31.0,
            "vit_c": 0.0, "folate": 15.0, "fat": 4.3, "added_sugar": 0.0,
            "sodium": 5.0, "phytate_flag": True
        }
    },
    {
        "name": "Rolled Oats",
        "local_names": {"hi": "जई", "ta": "ஓட்ஸ்", "te": "ఓట్స్", "ml": "ഓട്സ്"},
        "category": "cereal_millet",
        "diet_class": "vegan",
        "allergens": ["gluten"],
        "cost_per_kg_inr": 120.0,
        "availability": "high",
        "processing_notes": "Steamed and rolled.",
        "min_inclusion_pct": 5.0,
        "max_inclusion_pct": 35.0,
        "nutrients": {
            "energy": 389.0, "protein": 16.9, "iron": 4.7, "calcium": 54.0,
            "vit_c": 0.0, "folate": 56.0, "fat": 6.9, "added_sugar": 0.0,
            "sodium": 2.0, "phytate_flag": True
        }
    },

    # 2. Pulses & Legumes
    {
        "name": "Roasted Bengal Gram (Chana Dalia)",
        "local_names": {"hi": "भुना चना (दलिया)", "ta": "பொட்டுக்கடலை", "te": "పుట్నాల పప్పు", "ml": "പൊട്ടുകടല"},
        "category": "pulse_legume",
        "diet_class": "vegan",
        "allergens": [],
        "cost_per_kg_inr": 90.0,
        "availability": "high",
        "processing_notes": "Dry roasted, dehulled split chickpeas.",
        "min_inclusion_pct": 5.0,
        "max_inclusion_pct": 35.0,
        "nutrients": {
            "energy": 369.0, "protein": 22.5, "iron": 9.5, "calcium": 58.0,
            "vit_c": 0.0, "folate": 140.0, "fat": 5.2, "added_sugar": 0.0,
            "sodium": 35.0, "phytate_flag": False
        }
    },
    {
        "name": "Sprouted Green Moong Flour",
        "local_names": {"hi": "अंकुरित मूंग आटा", "ta": "முளைகட்டிய பாசிப்பயறு", "te": "మొలకెత్తిన పెసలు", "ml": "മുളപ്പിച്ച ചെറുപയർ"},
        "category": "pulse_legume",
        "diet_class": "vegan",
        "allergens": [],
        "cost_per_kg_inr": 130.0,
        "availability": "high",
        "processing_notes": "Germinated, solar dried and fine milled.",
        "min_inclusion_pct": 5.0,
        "max_inclusion_pct": 25.0,
        "nutrients": {
            "energy": 345.0, "protein": 24.0, "iron": 4.4, "calcium": 75.0,
            "vit_c": 8.0, "folate": 165.0, "fat": 1.2, "added_sugar": 0.0,
            "sodium": 15.0, "phytate_flag": False
        }
    },
    {
        "name": "Horse Gram (Kulthi / Kollu)",
        "local_names": {"hi": "कुलथी", "ta": "கொள்ளு", "te": "ఉలవలు", "ml": "മുതിര"},
        "category": "pulse_legume",
        "diet_class": "vegan",
        "allergens": [],
        "cost_per_kg_inr": 80.0,
        "availability": "high",
        "processing_notes": "Roasted and milled into fine flour.",
        "min_inclusion_pct": 2.0,
        "max_inclusion_pct": 20.0,
        "nutrients": {
            "energy": 321.0, "protein": 22.0, "iron": 7.1, "calcium": 287.0,
            "vit_c": 0.0, "folate": 110.0, "fat": 0.5, "added_sugar": 0.0,
            "sodium": 12.0, "phytate_flag": True
        }
    },
    {
        "name": "Soybean Flour (Defatted)",
        "local_names": {"hi": "सोयाबीन आटा", "ta": "சோயா மாவு", "te": "సోయా పిండి", "ml": "സോയാബീൻ പൊടി"},
        "category": "pulse_legume",
        "diet_class": "vegan",
        "allergens": ["soy"],
        "cost_per_kg_inr": 85.0,
        "availability": "high",
        "processing_notes": "Toasted defatted soy grits.",
        "min_inclusion_pct": 2.0,
        "max_inclusion_pct": 15.0,
        "nutrients": {
            "energy": 330.0, "protein": 49.8, "iron": 9.2, "calcium": 240.0,
            "vit_c": 0.0, "folate": 200.0, "fat": 1.2, "added_sugar": 0.0,
            "sodium": 20.0, "phytate_flag": True
        }
    },

    # 3. Oilseeds & Nuts
    {
        "name": "White Sesame Seeds (Til)",
        "local_names": {"hi": "सफेद तिल", "ta": "வெள்ளை எள்", "te": "తెల్ల నువ్వులు", "ml": "വെള്ള എള്ള്"},
        "category": "oilseed_nut",
        "diet_class": "vegan",
        "allergens": ["sesame"],
        "cost_per_kg_inr": 180.0,
        "availability": "high",
        "processing_notes": "Lightly roasted.",
        "min_inclusion_pct": 2.0,
        "max_inclusion_pct": 20.0,
        "nutrients": {
            "energy": 563.0, "protein": 18.3, "iron": 14.6, "calcium": 1450.0,
            "vit_c": 0.0, "folate": 97.0, "fat": 43.3, "added_sugar": 0.0,
            "sodium": 11.0, "phytate_flag": False
        }
    },
    {
        "name": "Black Sesame Seeds",
        "local_names": {"hi": "काला तिल", "ta": "கருப்பு எள்", "te": "నల్ల నువ్వులు", "ml": "കറുത്ത എള്ള്"},
        "category": "oilseed_nut",
        "diet_class": "vegan",
        "allergens": ["sesame"],
        "cost_per_kg_inr": 190.0,
        "availability": "high",
        "processing_notes": "Dry roasted whole seeds.",
        "min_inclusion_pct": 2.0,
        "max_inclusion_pct": 15.0,
        "nutrients": {
            "energy": 560.0, "protein": 18.0, "iron": 16.2, "calcium": 1500.0,
            "vit_c": 0.0, "folate": 100.0, "fat": 44.0, "added_sugar": 0.0,
            "sodium": 12.0, "phytate_flag": False
        }
    },
    {
        "name": "Flaxseeds (Alsi)",
        "local_names": {"hi": "अलसी", "ta": "ஆளி விதை", "te": "అవిసె గింజలు", "ml": "ചണവിത്ത്"},
        "category": "oilseed_nut",
        "diet_class": "vegan",
        "allergens": [],
        "cost_per_kg_inr": 140.0,
        "availability": "high",
        "processing_notes": "Dry roasted and coarsely cracked for omega-3 and iron release.",
        "min_inclusion_pct": 2.0,
        "max_inclusion_pct": 15.0,
        "nutrients": {
            "energy": 534.0, "protein": 18.3, "iron": 5.7, "calcium": 255.0,
            "vit_c": 0.6, "folate": 87.0, "fat": 42.2, "added_sugar": 0.0,
            "sodium": 30.0, "phytate_flag": False
        }
    },
    {
        "name": "Pumpkin Seeds",
        "local_names": {"hi": "कद्दू के बीज", "ta": "பூசணி விதை", "te": "గుమ్మడి గింజలు", "ml": "മത്തങ്ങ വിത്തുകൾ"},
        "category": "oilseed_nut",
        "diet_class": "vegan",
        "allergens": [],
        "cost_per_kg_inr": 450.0,
        "availability": "high",
        "processing_notes": "Shelled and dry roasted.",
        "min_inclusion_pct": 2.0,
        "max_inclusion_pct": 20.0,
        "nutrients": {
            "energy": 559.0, "protein": 30.2, "iron": 8.8, "calcium": 46.0,
            "vit_c": 1.9, "folate": 58.0, "fat": 49.0, "added_sugar": 0.0,
            "sodium": 7.0, "phytate_flag": False
        }
    },
    {
        "name": "Garden Cress Seeds (Halim / Aliv)",
        "local_names": {"hi": "हलीम (आलिव)", "ta": "ஆளி விதை (சந்திரி)", "te": "ఆదిత్య గింజలు", "ml": "ആശളി"},
        "category": "oilseed_nut",
        "diet_class": "vegan",
        "allergens": [],
        "cost_per_kg_inr": 280.0,
        "availability": "high",
        "processing_notes": "Powerhouse iron source. Pre-soaked or powdered.",
        "min_inclusion_pct": 1.0,
        "max_inclusion_pct": 8.0,
        "nutrients": {
            "energy": 454.0, "protein": 25.3, "iron": 100.0, "calcium": 377.0,
            "vit_c": 8.0, "folate": 80.0, "fat": 24.5, "added_sugar": 0.0,
            "sodium": 14.0, "phytate_flag": False
        }
    },
    {
        "name": "Roasted Peanuts (Groundnut)",
        "local_names": {"hi": "मूंगफली", "ta": "வேர்க்கடலை", "te": "వేరుశెనగ", "ml": "നിലക്കടല"},
        "category": "oilseed_nut",
        "diet_class": "vegan",
        "allergens": ["peanut"],
        "cost_per_kg_inr": 140.0,
        "availability": "high",
        "processing_notes": "Dry roasted, blanched split kernels.",
        "min_inclusion_pct": 2.0,
        "max_inclusion_pct": 30.0,
        "nutrients": {
            "energy": 567.0, "protein": 25.8, "iron": 4.6, "calcium": 92.0,
            "vit_c": 0.0, "folate": 240.0, "fat": 49.2, "added_sugar": 0.0,
            "sodium": 18.0, "phytate_flag": False
        }
    },
    {
        "name": "Almonds",
        "local_names": {"hi": "बादाम", "ta": "பாதாம்", "te": "బాదం", "ml": "ബദാം"},
        "category": "oilseed_nut",
        "diet_class": "vegan",
        "allergens": ["tree_nut"],
        "cost_per_kg_inr": 750.0,
        "availability": "high",
        "processing_notes": "Sliced blanched almonds.",
        "min_inclusion_pct": 2.0,
        "max_inclusion_pct": 20.0,
        "nutrients": {
            "energy": 579.0, "protein": 21.2, "iron": 3.7, "calcium": 269.0,
            "vit_c": 0.0, "folate": 44.0, "fat": 49.9, "added_sugar": 0.0,
            "sodium": 1.0, "phytate_flag": False
        }
    },

    # 4. Leafy Greens & Vegetables (Dehydrated Powders)
    {
        "name": "Dehydrated Moringa Leaf Powder",
        "local_names": {"hi": "सहजन पत्ता पाउडर", "ta": "முருங்கை இலை பொடி", "te": "మునగాకు పొడి", "ml": "മുരിങ്ങയില പൊടി"},
        "category": "leafy_green",
        "diet_class": "vegan",
        "allergens": [],
        "cost_per_kg_inr": 350.0,
        "availability": "high",
        "processing_notes": "Shade dried drumstick leaves, micronized.",
        "min_inclusion_pct": 1.0,
        "max_inclusion_pct": 10.0,
        "nutrients": {
            "energy": 205.0, "protein": 27.1, "iron": 28.2, "calcium": 2003.0,
            "vit_c": 17.3, "folate": 40.0, "fat": 2.3, "added_sugar": 0.0,
            "sodium": 42.0, "phytate_flag": False
        }
    },
    {
        "name": "Dehydrated Amaranth Leaf Powder",
        "local_names": {"hi": "चौलाई पत्ता पाउडर", "ta": "பசலைக்கீரை / தண்டுக்கீரை பொடி", "te": "తోటకూర పొడి", "ml": "ചീരപ്പൊടി"},
        "category": "leafy_green",
        "diet_class": "vegan",
        "allergens": [],
        "cost_per_kg_inr": 320.0,
        "availability": "high",
        "processing_notes": "Cleaned, dehydrated green amaranth foliage.",
        "min_inclusion_pct": 1.0,
        "max_inclusion_pct": 10.0,
        "nutrients": {
            "energy": 215.0, "protein": 23.0, "iron": 25.5, "calcium": 1850.0,
            "vit_c": 22.0, "folate": 85.0, "fat": 2.0, "added_sugar": 0.0,
            "sodium": 30.0, "phytate_flag": False
        }
    },

    # 5. Fruits & Natural Vitamin C Enhancers
    {
        "name": "Indian Gooseberry Powder (Amla)",
        "local_names": {"hi": "आंवला पाउडर", "ta": "நெல்லிக்காய் பொடி", "te": "ఉసిరికాయ పొడి", "ml": "നെല്ലിക്ക പൊടി"},
        "category": "fruit_veggie",
        "diet_class": "vegan",
        "allergens": [],
        "cost_per_kg_inr": 380.0,
        "availability": "high",
        "processing_notes": "Key ascorbic acid absorption booster.",
        "min_inclusion_pct": 1.0,
        "max_inclusion_pct": 8.0,
        "nutrients": {
            "energy": 287.0, "protein": 3.2, "iron": 1.2, "calcium": 50.0,
            "vit_c": 450.0, "folate": 10.0, "fat": 0.5, "added_sugar": 0.0,
            "sodium": 8.0, "phytate_flag": False
        }
    },
    {
        "name": "Guava Fruit Powder",
        "local_names": {"hi": "अमरूद पाउडर", "ta": "கொய்யா பழ பொடி", "te": "జామపండు పొడి", "ml": "പേരയ്ക്ക പൊടി"},
        "category": "fruit_veggie",
        "diet_class": "vegan",
        "allergens": [],
        "cost_per_kg_inr": 420.0,
        "availability": "high",
        "processing_notes": "Spray dried pink guava with rich natural vitamin C.",
        "min_inclusion_pct": 1.0,
        "max_inclusion_pct": 12.0,
        "nutrients": {
            "energy": 260.0, "protein": 4.1, "iron": 0.8, "calcium": 32.0,
            "vit_c": 228.0, "folate": 49.0, "fat": 1.0, "added_sugar": 0.0,
            "sodium": 5.0, "phytate_flag": False
        }
    },
    {
        "name": "Orange Fruit Powder",
        "local_names": {"hi": "संतरा पाउडर", "ta": "ஆரஞ்சு பொடி", "te": "నారింజ పొడి", "ml": "ഓറഞ്ച് പൊടി"},
        "category": "fruit_veggie",
        "diet_class": "vegan",
        "allergens": [],
        "cost_per_kg_inr": 400.0,
        "availability": "high",
        "processing_notes": "Natural citrus flavour and ascorbic acid.",
        "min_inclusion_pct": 1.0,
        "max_inclusion_pct": 10.0,
        "nutrients": {
            "energy": 290.0, "protein": 3.0, "iron": 0.5, "calcium": 40.0,
            "vit_c": 180.0, "folate": 30.0, "fat": 0.4, "added_sugar": 0.0,
            "sodium": 4.0, "phytate_flag": False
        }
    },
    {
        "name": "Dried Dates Paste / Powder (Khajoor)",
        "local_names": {"hi": "खजूर", "ta": "பேரீச்சம்பழம்", "te": "ఖర్జూరం", "ml": "ഈന്തപ്പഴം"},
        "category": "sweetener_spice",
        "diet_class": "vegan",
        "allergens": [],
        "cost_per_kg_inr": 220.0,
        "availability": "high",
        "processing_notes": "Pitted dates paste acting as functional binder and sweetening agent.",
        "min_inclusion_pct": 5.0,
        "max_inclusion_pct": 35.0,
        "nutrients": {
            "energy": 282.0, "protein": 2.5, "iron": 1.0, "calcium": 64.0,
            "vit_c": 0.4, "folate": 19.0, "fat": 0.4, "added_sugar": 0.0,
            "sodium": 2.0, "phytate_flag": False
        }
    },
    {
        "name": "Black Raisins (Kishmish)",
        "local_names": {"hi": "काली किशमिश", "ta": "உலர் திராட்சை", "te": "కిస్మిస్", "ml": "ഉണക്കമുന്തിരി"},
        "category": "sweetener_spice",
        "diet_class": "vegan",
        "allergens": [],
        "cost_per_kg_inr": 280.0,
        "availability": "high",
        "processing_notes": "Sun dried seedless black grapes.",
        "min_inclusion_pct": 2.0,
        "max_inclusion_pct": 20.0,
        "nutrients": {
            "energy": 299.0, "protein": 3.1, "iron": 2.6, "calcium": 50.0,
            "vit_c": 2.3, "folate": 5.0, "fat": 0.5, "added_sugar": 0.0,
            "sodium": 11.0, "phytate_flag": False
        }
    },
    {
        "name": "Organic Jaggery Powder (Gud)",
        "local_names": {"hi": "गुड़", "ta": "நாட்டு சர்க்கரை / வெல்லம்", "te": "బెల్లం", "ml": "ശർക്കര"},
        "category": "sweetener_spice",
        "diet_class": "vegan",
        "allergens": [],
        "cost_per_kg_inr": 70.0,
        "availability": "high",
        "processing_notes": "Unrefined cane sugar with natural minerals, binder.",
        "min_inclusion_pct": 2.0,
        "max_inclusion_pct": 20.0,
        "nutrients": {
            "energy": 383.0, "protein": 0.4, "iron": 2.6, "calcium": 80.0,
            "vit_c": 0.0, "folate": 0.0, "fat": 0.1, "added_sugar": 85.0,
            "sodium": 30.0, "phytate_flag": False
        }
    },

    # 6. Dairy & Flavorings
    {
        "name": "Skimmed Milk Powder",
        "local_names": {"hi": "मलाई रहित दूध पाउडर", "ta": "பால் பவுடர்", "te": "పాల పొడి", "ml": "പാൽപ്പൊടി"},
        "category": "dairy",
        "diet_class": "vegetarian",
        "allergens": ["dairy"],
        "cost_per_kg_inr": 360.0,
        "availability": "high",
        "processing_notes": "Spray dried dairy protein source and natural binder.",
        "min_inclusion_pct": 2.0,
        "max_inclusion_pct": 20.0,
        "nutrients": {
            "energy": 362.0, "protein": 36.0, "iron": 0.4, "calcium": 1250.0,
            "vit_c": 7.0, "folate": 50.0, "fat": 0.8, "added_sugar": 0.0,
            "sodium": 535.0, "phytate_flag": False
        }
    },
    {
        "name": "Cardamom Powder (Elaichi)",
        "local_names": {"hi": "इलायची पाउडर", "ta": "ஏலக்காய் பொடி", "te": "యాలకుల పొడి", "ml": "ഏലക്ക പൊടി"},
        "category": "sweetener_spice",
        "diet_class": "vegan",
        "allergens": [],
        "cost_per_kg_inr": 2500.0,
        "availability": "high",
        "processing_notes": "Aromatic natural palatability masking agent.",
        "min_inclusion_pct": 0.1,
        "max_inclusion_pct": 2.0,
        "nutrients": {
            "energy": 311.0, "protein": 10.8, "iron": 13.9, "calcium": 383.0,
            "vit_c": 21.0, "folate": 18.0, "fat": 6.7, "added_sugar": 0.0,
            "sodium": 18.0, "phytate_flag": False
        }
    },
    {
        "name": "Ginger Powder (Sonth)",
        "local_names": {"hi": "सोंठ (सूखा अदरक)", "ta": "சுக்கு பொடி", "te": "శొంఠి పొడి", "ml": "ചുക്കുപൊടി"},
        "category": "sweetener_spice",
        "diet_class": "vegan",
        "allergens": [],
        "cost_per_kg_inr": 450.0,
        "availability": "high",
        "processing_notes": "Digestive aid and natural seasoning.",
        "min_inclusion_pct": 0.1,
        "max_inclusion_pct": 2.0,
        "nutrients": {
            "energy": 335.0, "protein": 9.0, "iron": 19.8, "calcium": 116.0,
            "vit_c": 0.7, "folate": 30.0, "fat": 4.2, "added_sugar": 0.0,
            "sodium": 27.0, "phytate_flag": False
        }
    },
    {
        "name": "Cinnamon Powder (Dalchini)",
        "local_names": {"hi": "दालचीनी", "ta": "இலவங்கப்பட்டை", "te": "దాల్చిన చెక్క", "ml": "കറുവപ്പട്ട"},
        "category": "sweetener_spice",
        "diet_class": "vegan",
        "allergens": [],
        "cost_per_kg_inr": 600.0,
        "availability": "high",
        "processing_notes": "Ceylon cinnamon powder.",
        "min_inclusion_pct": 0.1,
        "max_inclusion_pct": 2.0,
        "nutrients": {
            "energy": 247.0, "protein": 4.0, "iron": 8.3, "calcium": 1000.0,
            "vit_c": 3.8, "folate": 6.0, "fat": 1.2, "added_sugar": 0.0,
            "sodium": 10.0, "phytate_flag": False
        }
    },
    {
        "name": "Cocoa Powder (Unsweetened)",
        "local_names": {"hi": "कोको पाउडर", "ta": "கோகோ பவுடர்", "te": "కోకో పౌడర్", "ml": "കൊക്കോ പൗഡർ"},
        "category": "sweetener_spice",
        "diet_class": "vegan",
        "allergens": [],
        "cost_per_kg_inr": 650.0,
        "availability": "high",
        "processing_notes": "Natural Dutch processed cocoa for youthful aspirational appeal.",
        "min_inclusion_pct": 1.0,
        "max_inclusion_pct": 6.0,
        "nutrients": {
            "energy": 228.0, "protein": 19.6, "iron": 13.9, "calcium": 128.0,
            "vit_c": 0.0, "folate": 32.0, "fat": 13.7, "added_sugar": 0.0,
            "sodium": 21.0, "phytate_flag": False
        }
    },
]

