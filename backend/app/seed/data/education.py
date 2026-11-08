"""Seed data for educational content and multilingual medical glossary."""

EDUCATION_MODULES_SEED = [
    {
        "slug": "understanding-anaemia",
        "category": "clinical_basics",
        "title": {
            "en": "Understanding Anaemia: Beyond Just Iron",
            "ta": "இரத்த சோகையைப் புரிந்துகொள்வது: இரும்புச்சத்தை மட்டும் கடந்து",
            "hi": "एनीमिया को समझना: केवल आयरन से आगे",
            "te": "రక్తహీనతను అర్థం చేసుకోవడం: కేవలం ఐరన్ మాత్రమే కాదు",
            "ml": "വിളർച്ചയെക്കുറിച്ച് മനസ്സിലാക്കാം: കേവലം ഇരുമ്പിനപ്പുറം",
        },
        "body": {
            "en": (
                "Anaemia is a condition where the number of red blood cells or the haemoglobin concentration "
                "within them is lower than normal. Haemoglobin is needed to carry oxygen to tissues throughout the body.\n\n"
                "While iron deficiency is the most common cause, anaemia can also arise from folate deficiency, "
                "vitamin B12 deficiency, chronic inflammation, or inherited haemoglobin variants (such as thalassaemia trait). "
                "That is why a comprehensive lab panel (including Ferritin and MCV) is critical before self-prescribing supplements."
            ),
            "ta": (
                "இரத்த சோகை என்பது உடலில் இரத்த சிவப்பணுக்கள் அல்லது ஹீமோகுளோபின் அளவு இயல்பை விட குறைவாக இருக்கும் ஒரு நிலையாகும். "
                "ஹீமோகுளோபின் உடலின் அனைத்து பாகங்களுக்கும் ஆக்ஸிஜனை கொண்டு செல்ல அவசியமானது.\n\n"
                "இரும்புச்சத்து குறைபாடே இதற்கு பொதுவான காரணமாக இருந்தாலும், ஃபோலேட், வைட்டமின் B12 குறைபாடு அல்லது தாலசீமியா போன்ற பரம்பரை "
                "காரணங்களாலும் இது ஏற்படலாம். எனவே முழுமையான ஆய்வக பரிசோதனை மிகவும் அவசியமானது."
            ),
            "hi": (
                "एनीमिया एक ऐसी स्थिति है जिसमें लाल रक्त कोशिकाओं या हीमोग्लोबिन का स्तर सामान्य से कम हो जाता है। "
                "हीमोग्लोबिन शरीर के सभी अंगों तक ऑक्सीजन पहुंचाने का काम करता है।\n\n"
                "यद्यपि आयरन की कमी इसका सबसे सामान्य कारण है, लेकिन यह फोलेट, विटामिन बी12 की कमी या थैलेसीमिया जैसे कारणों से भी हो सकता है।"
            ),
            "te": (
                "రక్తహీనత అనేది శరీరంలో ఎర్ర రక్త కణాలు లేదా హిమోగ్లోబిన్ పరిమాణం తక్కువగా ఉండే పరిస్థితి. "
                "శరీర భాగాలకు ఆక్సిజన్ చేరవేయడానికి హిమోగ్లోబిన్ అవసరం. సరైన ఆహారం మరియు వైద్య పరీక్షలు అవసరం."
            ),
            "ml": (
                "ശരീരത്തിലെ ചുവന്ന രക്താണുക്കളുടെയോ ഹീമോഗ്ലോബിന്റെയോ അളവ് സാധാരണ നിലയേക്കാൾ കുറയുന്ന അവസ്ഥയാണ് വിളർച്ച. "
                "ഇരുമ്പിന്റെ കുറവ് മാത്രമല്ല, ഫോളേറ്റ്, വിറ്റാമിൻ ബി12 എന്നിവയുടെ കുറവും ഇതിന് കാരണമാകാം."
            ),
        },
        "status": "published",
        "translation_review_status": {
            "en": "expert_reviewed",
            "ta": "machine_draft",
            "hi": "machine_draft",
            "te": "machine_draft",
            "ml": "machine_draft",
        },
        "references_list": [
            "WHO. Nutritional anaemias: tools for effective prevention and control. Geneva: World Health Organization; 2017.",
            "ICMR-NIN. Dietary Guidelines for Indians. Hyderabad: National Institute of Nutrition; 2024.",
        ],
    },
    {
        "slug": "bioavailability-and-pairing",
        "category": "dietary_science",
        "title": {
            "en": "The Science of Iron Bioavailability: Enhancers vs Inhibitors",
            "ta": "இரும்பு உறிஞ்சுதல் அறிவியல்: அதிகரிக்கும் மற்றும் தடுக்கும் காரணிகள்",
            "hi": "आयरन अवशोषण का विज्ञान: बढ़ाने वाले और रोकने वाले कारक",
            "te": "ఐరన్ శోషణ విజ్ఞానం: పెంచే మరియు తగ్గించే అంశాలు",
            "ml": "ഇരുമ്പ് ആഗിരണ ശാസ്ത്രം: സഹായിക്കുന്ന ഘടകങ്ങളും തടസ്സങ്ങളും",
        },
        "body": {
            "en": (
                "Plant-based food contains non-heme iron, which requires an acidic reducing environment for optimal absorption. "
                "Pairing iron-rich millets and pulses with natural ascorbic acid (Vitamin C from amla, guava, or lemon) can double "
                "or triple iron bioavailability.\n\n"
                "Conversely, drinking tea or coffee immediately with meals introduces tannins and polyphenols that bind iron and "
                "drastically reduce absorption. Waiting at least 45 minutes between tea and meals supports maximum mineral uptake."
            ),
            "ta": (
                "தாவர உணவுகளில் உள்ள இரும்புச்சத்தை உடல் எளிதாக உறிஞ்சுவதற்கு வைட்டமின் சி அவசியமானது. நெல்லிக்காய், கொய்யாப்பழம் அல்லது எலுமிச்சையை "
                "தினையோடு சேர்த்து உட்கொள்வது இரும்பு உறிஞ்சுதலை 2 முதல் 3 மடங்கு அதிகரிக்கிறது. உணவுடன் தேநீர் அல்லது காபி குடிப்பதை தவிர்க்க வேண்டும்."
            ),
            "hi": (
                "पौधों से मिलने वाले नॉन-हीम आयरन के बेहतर अवशोषण के लिए विटामिन सी बहुत जरूरी है। "
                "भोजन के तुरंत बाद चाय या कॉफी पीने से बचें, क्योंकि इनमें मौजूद टैनिन आयरन के अवशोषण को बाधित करते हैं।"
            ),
            "te": (
                "మొక్కల ఆధారిత ఐరన్ శోషణను విటమిన్ సి గణనీయంగా పెంచుతుంది. ఉసిరి లేదా నిమ్మరసంతో కూడిన ఆహారం మంచిది. భోజన సమయంలో టీ, కాఫీలను నివారించండి."
            ),
            "ml": (
                "സസ്യഭക്ഷണങ്ങളിലെ ഇരുമ്പ് ശരീരം നന്നായി ആഗിരണം ചെയ്യാൻ വിറ്റാമിൻ സി അത്യാവശ്യമാണ്. ഭക്ഷണത്തോടൊപ്പം ചായയോ കാപ്പിയോ കുടിക്കുന്നത് ഒഴിവാക്കുക."
            ),
        },
        "status": "published",
        "translation_review_status": {
            "en": "expert_reviewed",
            "ta": "machine_draft",
            "hi": "machine_draft",
            "te": "machine_draft",
            "ml": "machine_draft",
        },
        "references_list": [
            "Hallberg L, Brune M, Rossander L. The role of vitamin C in iron absorption. Int J Vitam Nutr Res Suppl. 1989;30:103-8.",
        ],
    },
]

