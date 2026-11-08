"""Seed data for assessment rules, safety gate cutoffs, and product format templates."""

RULE_SETS_SEED = [
    {
        "version": "icmr_v2020.1",
        "status": "draft",
        "approved_by": None,
        "approved_at": None,
        "rules": {
            "hb_cutoffs_non_pregnant": {
                "severe": 7.0,
                "moderate": 10.0,
                "mild": 12.0,
            },
            "hb_cutoffs_pregnant": {
                "severe": 7.0,
                "moderate": 10.0,
                "mild": 11.0,
            },
            "ferritin_cutoff_depleted": 15.0,
            "ferritin_cutoff_elevated": 150.0,
            "mcv_cutoff_microcytic": 80.0,
            "b12_cutoff_low": 200.0,
            "folate_cutoff_low": 4.0,
            "iron_target_range_mg": [4.0, 5.0],
            "hfss_caps": {
                "added_sugar_max_g": 5.0,
                "saturated_fat_max_g": 3.0,
                "sodium_max_mg": 100.0,
            },
        },
    }
]

PRODUCT_CATEGORIES_SEED = [
    {
        "slug": "bars",
        "name": {
            "en": "Roasted Millet Energy Bar",
            "ta": "வறுத்த தினை ஊட்டச்சத்து பார்",
            "hi": "भुना हुआ बाजरा पोषण बार",
            "te": "వేయించిన చిరుధాన్యాల బార్",
            "ml": "വറുത്ത തിന ന്യൂട്രിഷൻ ബാർ",
        },
        "description": {
            "en": "A crunchy, aspirational roasted millet bar bonded with dates and sesame, delivering 4-5 mg bioavailable iron.",
            "ta": "பேரீச்சம்பழம் மற்றும் எள் சேர்க்கப்பட்ட சுவையான தினை பார்.",
            "hi": "खजूर और तिल से युक्त स्वादिष्ट और पौष्टिक बाजरा बार।",
            "te": "ఖర్జూరం మరియు నువ్వులతో కూడిన రుచికరమైన చిరుధాన్యాల బార్.",
            "ml": "ഈന്തപ്പഴവും എള്ളും ചേർത്ത രുചികരമായ തിന ബാർ.",
        },
        "format_template": {
            "serving_size_g": 35.0,
            "binder_min_pct": 15.0,
            "allowed_ingredient_categories": ["cereal_millet", "pulse_legume", "oilseed_nut", "sweetener_spice", "fruit_veggie", "dairy"],
            "storage_instructions": "Store in a cool, dry place away from direct sunlight. Shelf life: 90 days (prototype concept).",
            "preparation_instructions": "Ready to eat. Enjoy as a mid-morning or post-school nutrition snack.",
        },
    },
    {
        "slug": "laddoos",
        "name": {
            "en": "Nutrient-Dense Multigrain Laddoo / Bite",
            "ta": "ஊட்டச்சத்து நிறைந்த சிறுதானிய லட்டு",
            "hi": "पोषक तत्वों से भरपूर बहुअनाज लड्डू",
            "te": "పోషకాలతో కూడిన మల్టీగ్రెయిన్ లడ్డూ",
            "ml": "പോഷക സമ്പുഷ്ടമായ മൾട്ടിഗ്രെയിൻ ലഡ്ഡു",
        },
        "description": {
            "en": "Traditional Indian confectionery re-engineered with ragi, roasted gram, and amla for maximum iron absorption.",
            "ta": "கேழ்வரகு, பொட்டுக்கடலை மற்றும் நெல்லிக்காய் கலந்த பாரம்பரிய சத்தான லட்டு.",
            "hi": "रागी, भुना चना और आंवला से समृद्ध पारंपरिक भारतीय पौष्टिक लड्डू।",
            "te": "రాగులు, పుట్నాల పప్పు, ఉసిరికాయతో తయారైన సంప్రదాయ లడ్డూ.",
            "ml": "റാഗിയും നെല്ലിക്കയും ചേർത്ത പരമ്പരാഗത പോഷക ലഡ്ഡു.",
        },
        "format_template": {
            "serving_size_g": 40.0,
            "binder_min_pct": 20.0,
            "allowed_ingredient_categories": ["cereal_millet", "pulse_legume", "oilseed_nut", "sweetener_spice", "fruit_veggie", "dairy"],
            "storage_instructions": "Keep in an airtight container at ambient temperature. Consume within 45 days.",
            "preparation_instructions": "Ready to eat. 1 laddoo daily with water or milk.",
        },
    },
    {
        "slug": "breakfast_mix",
        "name": {
            "en": "Fortified Instant Breakfast Porridge Mix",
            "ta": "ஊட்டச்சத்து காலை உணவு கஞ்சி மிக்ஸ்",
            "hi": "पौष्टिक इंस्टेंट नाश्ता दलिया मिक्स",
            "te": "పోషక అల్పాహార గంజి మిక్స్",
            "ml": "പോഷക സമ്പുഷ്ടമായ പ്രഭാതഭക്ഷണ കുറുക്ക് മിക്സ്",
        },
        "description": {
            "en": "Sprouted multigrain pre-cooked cereal mix that cooks in 2 minutes with warm water or milk.",
            "ta": "2 நிமிடங்களில் தயார் செய்யக்கூடிய சத்தான முளைகட்டிய தானிய கஞ்சி மிக்ஸ்.",
            "hi": "2 मिनट में बनने वाला अंकुरित अनाज दलिया मिक्स।",
            "te": "2 నిమిషాల్లో తయారయ్యే మొలకెత్తిన ధాన్యాల అల్పాహార మిక్స్.",
            "ml": "2 മിനിറ്റിനുള്ളിൽ തയ്യാറാക്കാവുന്ന മുളപ്പിച്ച ധാന്യ കുറുക്ക് മിക്സ്.",
        },
        "format_template": {
            "serving_size_g": 30.0,
            "binder_min_pct": 0.0,
            "allowed_ingredient_categories": ["cereal_millet", "pulse_legume", "oilseed_nut", "leafy_green", "fruit_veggie", "sweetener_spice"],
            "storage_instructions": "Store in a dry pouch. Reseal tightly after opening.",
            "preparation_instructions": "Mix 30g with 150ml warm water or milk. Stir well and consume warm.",
        },
    },
    {
        "slug": "beverage_mix",
        "name": {
            "en": "Cold Drink / Shake Nutrition Mix",
            "ta": "குளிர்பான ஊட்டச்சத்து பான மிக்ஸ்",
            "hi": "कोल्ड ड्रिंक पोषण पेय मिक्स",
            "te": "కోల్డ్ డ్రింక్ న్యూట్రిషన్ మిక్స్",
            "ml": "പോഷക പാനീയ മിക്സ്",
        },
        "description": {
            "en": "Refreshing instant soluble drink powder naturally flavoured with cocoa and amla vitamin C.",
            "ta": "கோகோ மற்றும் நெல்லிக்காய் வைட்டமின் சி கலந்த புத்துணர்ச்சியூட்டும் சத்து பானம்.",
            "hi": "कोको और आंवला विटामिन सी से भरपूर ताज़ा पौष्टिक पेय।",
            "te": "కోకో మరియు ఉసిరి విటమిన్ సితో కూడిన రిఫ్రెషింగ్ న్యూట్రిషన్ డ్రింక్.",
            "ml": "കൊക്കോയും നെല്ലിക്കയും ചേർത്ത ഉന്മേഷദായകമായ പോഷക പാനീയം.",
        },
        "format_template": {
            "serving_size_g": 25.0,
            "binder_min_pct": 0.0,
            "allowed_ingredient_categories": ["pulse_legume", "oilseed_nut", "fruit_veggie", "sweetener_spice", "dairy"],
            "storage_instructions": "Store in moisture-free pouch. Protect from heat.",
            "preparation_instructions": "Dissolve 25g in 180ml chilled water or milk. Shake vigorously.",
        },
    },
    {
        "slug": "chikkis",
        "name": {
            "en": "Crisp Sesame & Seed Iron Chikki",
            "ta": "மொறுமொறுப்பான எள் மற்றும் விதை சிக்கி",
            "hi": "कुरकुरी तिल और बीज आयरन चिक्की",
            "te": "నువ్వులు మరియు గింజల చిక్కీ",
            "ml": "എള്ളും വിത്തുകളും ചേർത്ത മൊരിഞ്ഞ ചിക്കി",
        },
        "description": {
            "en": "Crunchy roasted sesame, pumpkin seed, and jaggery brittle with natural plant iron.",
            "ta": "வறுத்த எள், பூசணி விதை மற்றும் வெல்லம் சேர்ந்த மொறுமொறுப்பான சத்து சிக்கி.",
            "hi": "भुने तिल, कद्दू के बीज और गुड़ से बनी कुरकुरी पौष्टिक चिक्की।",
            "te": "వేయించిన నువ్వులు, గుమ్మడి గింజలు మరియు బెల్లంతో చేసిన క్రిస్పీ చిక్కీ.",
            "ml": "വറുത്ത എള്ളും മത്തങ്ങ വിത്തും ശർക്കരയും ചേർത്ത ചിക്കി.",
        },
        "format_template": {
            "serving_size_g": 35.0,
            "binder_min_pct": 25.0,
            "allowed_ingredient_categories": ["oilseed_nut", "sweetener_spice", "cereal_millet"],
            "storage_instructions": "Store in a cool dry container. Protect from humidity.",
            "preparation_instructions": "Ready to eat. Crisp iron-dense snack.",
        },
    },
]

