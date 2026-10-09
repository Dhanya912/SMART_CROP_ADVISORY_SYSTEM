# -*- coding: utf-8 -*-
"""
i18n.py — Centralized translations for the Smart Crop Advisory System.

Supported language codes: en (English), kn (Kannada), ta (Tamil),
hi (Hindi), te (Telugu).

Scope: this module fully localizes the ADVISORY REPORT (on-screen +
PDF) and the CHATBOT — structural labels, status words, crop names,
and the template sentences the agents generate (weather advisory,
soil amendments, market advisory, policy notes). Government scheme
names/benefits are sourced from data/government_schemes.csv (English)
and shown with translated field labels (Benefit / Eligibility / etc.)
— translating 17+ scheme descriptions verbatim into 5 languages isn't
attempted here to keep official scheme wording authoritative; this is
documented in the README. The rest of the site chrome (nav, dashboard,
forms) remains English, matching what was asked (the advisory report
+ assistant in 5 languages).
"""

LANGUAGES = {"en": "English", "kn": "ಕನ್ನಡ", "ta": "தமிழ்", "hi": "हिन्दी", "te": "తెలుగు"}

LANG_ALIASES = {
    "english": "en", "en": "en",
    "kannada": "kn", "kn": "kn",
    "tamil": "ta", "ta": "ta",
    "hindi": "hi", "hi": "hi",
    "telugu": "te", "te": "te",
    "bilingual": "en",  # legacy value from older UI -> default to English
}


def norm_lang(lang):
    if not lang:
        return "en"
    return LANG_ALIASES.get(str(lang).strip().lower(), "en")


# ---------------------------------------------------------------- LABELS ---
LABELS = {
    "report_title": {"en": "Smart Crop Advisory Report", "kn": "ಸ್ಮಾರ್ಟ್ ಬೆಳೆ ಸಲಹಾ ವರದಿ", "ta": "ஸ்மார்ட் பயிர் ஆலோசனை அறிக்கை", "hi": "स्मार्ट फसल सलाह रिपोर्ट", "te": "స్మార్ట్ పంట సలహా నివేదిక"},
    "prepared_for": {"en": "Prepared for", "kn": "ಇವರಿಗಾಗಿ ಸಿದ್ಧಪಡಿಸಲಾಗಿದೆ", "ta": "இதற்காக தயாரிக்கப்பட்டது", "hi": "इनके लिए तैयार", "te": "వీరి కోసం సిద్ధం చేయబడింది"},
    "location": {"en": "Location", "kn": "ಸ್ಥಳ", "ta": "இடம்", "hi": "स्थान", "te": "స్థలం"},
    "generated_on": {"en": "Generated on", "kn": "ರಚಿಸಿದ ದಿನಾಂಕ", "ta": "உருவாக்கப்பட்ட தேதி", "hi": "निर्मित तिथि", "te": "రూపొందించిన తేదీ"},
    "executive_summary": {"en": "Executive Summary", "kn": "ಸಾರಾಂಶ", "ta": "நிர்வாக சுருக்கம்", "hi": "कार्यकारी सारांश", "te": "కార్యనిర్వాహక సారాంశం"},

    "sec_crop": {"en": "Crop Recommendation", "kn": "ಬೆಳೆ ಶಿಫಾರಸು", "ta": "பயிர் பரிந்துரை", "hi": "फसल अनुशंसा", "te": "పంట సిఫార్సు"},
    "sec_disease": {"en": "Disease Detection", "kn": "ರೋಗ ಪತ್ತೆ", "ta": "நோய் கண்டறிதல்", "hi": "रोग पहचान", "te": "వ్యాధి గుర్తింపు"},
    "sec_weather": {"en": "Weather Analysis", "kn": "ಹವಾಮಾನ ವಿಶ್ಲೇಷಣೆ", "ta": "வானிலை பகுப்பாய்வு", "hi": "मौसम विश्लेषण", "te": "వాతావరణ విశ్లేషణ"},
    "sec_soil": {"en": "Soil Health Analysis", "kn": "ಮಣ್ಣಿನ ಆರೋಗ್ಯ ವಿಶ್ಲೇಷಣೆ", "ta": "மண் ஆரோக்கிய பகுப்பாய்வு", "hi": "मिट्टी स्वास्थ्य विश्लेषण", "te": "నేల ఆరోగ్య విశ్లేషణ"},
    "sec_market": {"en": "Market Intelligence", "kn": "ಮಾರುಕಟ್ಟೆ ಮಾಹಿತಿ", "ta": "சந்தை தகவல்", "hi": "बाजार जानकारी", "te": "మార్కెట్ సమాచారం"},
    "sec_policy": {"en": "Policy & Government Schemes", "kn": "ನೀತಿ ಮತ್ತು ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು", "ta": "கொள்கை மற்றும் அரசு திட்டங்கள்", "hi": "नीति और सरकारी योजनाएं", "te": "విధానం మరియు ప్రభుత్వ పథకాలు"},
    "sec_action_plan": {"en": "Priority Action Plan", "kn": "ಆದ್ಯತಾ ಕ್ರಿಯಾ ಯೋಜನೆ", "ta": "முன்னுரிமை செயல் திட்டம்", "hi": "प्राथमिकता कार्य योजना", "te": "ప్రాధాన్యత కార్యాచరణ ప్రణాళిక"},

    "recommended_crop": {"en": "Recommended Crop", "kn": "ಶಿಫಾರಸು ಮಾಡಿದ ಬೆಳೆ", "ta": "பரிந்துரைக்கப்பட்ட பயிர்", "hi": "अनुशंसित फसल", "te": "సిఫార్సు చేసిన పంట"},
    "confidence_scores": {"en": "Confidence Scores", "kn": "ವಿಶ್ವಾಸಾರ್ಹತೆ ಅಂಕಗಳು", "ta": "நம்பிக்கை மதிப்பெண்கள்", "hi": "विश्वास स्कोर", "te": "విశ్వాస స్కోర్లు"},
    "method": {"en": "Method", "kn": "ವಿಧಾನ", "ta": "முறை", "hi": "विधि", "te": "పద్ధతి"},
    "key_influencing_factors": {"en": "Key Influencing Factors", "kn": "ಪ್ರಮುಖ ಪ್ರಭಾವಶಾಲಿ ಅಂಶಗಳು", "ta": "முக்கிய பாதிக்கும் காரணிகள்", "hi": "मुख्य प्रभावकारी कारक", "te": "ముఖ్య ప్రభావిత అంశాలు"},

    "disease": {"en": "Disease", "kn": "ರೋಗ", "ta": "நோய்", "hi": "रोग", "te": "వ్యాధి"},
    "severity": {"en": "Severity", "kn": "ತೀವ್ರತೆ", "ta": "தீவிரம்", "hi": "गंभीरता", "te": "తీవ్రత"},
    "confidence": {"en": "Confidence", "kn": "ವಿಶ್ವಾಸ", "ta": "நம்பிக்கை", "hi": "विश्वास", "te": "విశ్వాసం"},
    "cause": {"en": "Cause", "kn": "ಕಾರಣ", "ta": "காரணம்", "hi": "कारण", "te": "కారణం"},
    "treatment_steps": {"en": "Treatment Steps", "kn": "ಚಿಕಿತ್ಸೆಯ ಹಂತಗಳು", "ta": "சிகிச்சை படிகள்", "hi": "उपचार के चरण", "te": "చికిత్స దశలు"},
    "prevention": {"en": "Prevention", "kn": "ತಡೆಗಟ್ಟುವಿಕೆ", "ta": "தடுப்பு", "hi": "रोकथाम", "te": "నివారణ"},
    "no_image_msg": {"en": "No leaf image uploaded. Upload a clear leaf photo to enable disease detection.", "kn": "ಎಲೆಯ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿಲ್ಲ. ರೋಗ ಪತ್ತೆಗಾಗಿ ಸ್ಪಷ್ಟ ಎಲೆಯ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.", "ta": "இலை படம் பதிவேற்றப்படவில்லை. நோய் கண்டறிதலுக்கு தெளிவான இலை புகைப்படத்தை பதிவேற்றவும்.", "hi": "कोई पत्ती की फोटो अपलोड नहीं हुई। रोग पहचान हेतु स्पष्ट पत्ती की फोटो अपलोड करें।", "te": "ఆకు ఫోటో అప్‌లోడ్ చేయలేదు. వ్యాధి గుర్తింపు కోసం స్పష్టమైన ఆకు ఫోటోను అప్‌లోడ్ చేయండి."},
    "no_disease_detected": {"en": "No Disease Detected", "kn": "ಯಾವುದೇ ರೋಗ ಪತ್ತೆಯಾಗಿಲ್ಲ", "ta": "நோய் எதுவும் கண்டறியப்படவில்லை", "hi": "कोई रोग नहीं मिला", "te": "వ్యాధి ఏదీ కనుగొనబడలేదు"},

    "condition": {"en": "Condition", "kn": "ಸ್ಥಿತಿ", "ta": "நிலை", "hi": "स्थिति", "te": "పరిస్థితి"},
    "temperature": {"en": "Temperature", "kn": "ತಾಪಮಾನ", "ta": "வெப்பநிலை", "hi": "तापमान", "te": "ఉష్ణోగ్రత"},
    "humidity": {"en": "Humidity", "kn": "ಆರ್ದ್ರತೆ", "ta": "ஈரப்பதம்", "hi": "आर्द्रता", "te": "తేమ"},
    "wind_speed": {"en": "Wind Speed", "kn": "ಗಾಳಿಯ ವೇಗ", "ta": "காற்றின் வேகம்", "hi": "हवा की गति", "te": "గాలి వేగం"},
    "rainfall": {"en": "Rainfall", "kn": "ಮಳೆ", "ta": "மழை", "hi": "वर्षा", "te": "వర్షపాతం"},
    "irrigation_need": {"en": "Irrigation Need", "kn": "ನೀರಾವರಿ ಅಗತ್ಯ", "ta": "பாசன தேவை", "hi": "सिंचाई आवश्यकता", "te": "నీటిపారుదల అవసరం"},
    "farm_advisories": {"en": "Farm Advisories", "kn": "ಕೃಷಿ ಸಲಹೆಗಳು", "ta": "பண்ணை ஆலோசனைகள்", "hi": "कृषि सलाह", "te": "వ్యవసాయ సలహాలు"},
    "source": {"en": "Data Source", "kn": "ಡೇಟಾ ಮೂಲ", "ta": "தரவு மூலம்", "hi": "डेटा स्रोत", "te": "డేటా మూలం"},
    "live": {"en": "Live", "kn": "ಲೈವ್", "ta": "நேரலை", "hi": "लाइव", "te": "ప్రత్యక్షం"},
    "demo": {"en": "Demo", "kn": "ಡೆಮೊ", "ta": "டெமோ", "hi": "डेमो", "te": "డెమో"},

    "score": {"en": "Score", "kn": "ಅಂಕ", "ta": "மதிப்பெண்", "hi": "स्कोर", "te": "స్కోరు"},
    "nitrogen": {"en": "Nitrogen (N)", "kn": "ಸಾರಜನಕ (N)", "ta": "நைட்ரஜன் (N)", "hi": "नाइट्रोजन (N)", "te": "నత్రజని (N)"},
    "phosphorus": {"en": "Phosphorus (P)", "kn": "ರಂಜಕ (P)", "ta": "பாஸ்பரஸ் (P)", "hi": "फास्फोरस (P)", "te": "భాస్వరం (P)"},
    "potassium": {"en": "Potassium (K)", "kn": "ಪೊಟ್ಯಾಶಿಯಂ (K)", "ta": "பொட்டாசியம் (K)", "hi": "पोटैशियम (K)", "te": "పొటాషియం (K)"},
    "ph": {"en": "pH", "kn": "pH", "ta": "pH", "hi": "pH", "te": "pH"},
    "soil_type": {"en": "Soil Type", "kn": "ಮಣ್ಣಿನ ವಿಧ", "ta": "மண் வகை", "hi": "मिट्टी का प्रकार", "te": "నేల రకం"},
    "fertiliser_plan": {"en": "Fertiliser Plan", "kn": "ಗೊಬ್ಬರ ಯೋಜನೆ", "ta": "உர திட்டம்", "hi": "उर्वरक योजना", "te": "ఎరువుల ప్రణాళిక"},

    "crop": {"en": "Crop", "kn": "ಬೆಳೆ", "ta": "பயிர்", "hi": "फसल", "te": "పంట"},
    "avg_price": {"en": "Average Price", "kn": "ಸರಾಸರಿ ಬೆಲೆ", "ta": "சராசரி விலை", "hi": "औसत मूल्य", "te": "సగటు ధర"},
    "price_trend": {"en": "Trend", "kn": "ಪ್ರವೃತ್ತಿ", "ta": "போக்கு", "hi": "रुझान", "te": "ధోరణి"},
    "best_market": {"en": "Best Market", "kn": "ಉತ್ತಮ ಮಾರುಕಟ್ಟೆ", "ta": "சிறந்த சந்தை", "hi": "सर्वश्रेष्ठ बाजार", "te": "ఉత్తమ మార్కెట్"},
    "yield_estimate": {"en": "Yield Estimate", "kn": "ಇಳುವರಿ ಅಂದಾಜು", "ta": "மகசூல் மதிப்பீடு", "hi": "उपज अनुमान", "te": "దిగుబడి అంచనా"},
    "net_income": {"en": "Net Income", "kn": "ನಿವ್ವಳ ಆದಾಯ", "ta": "நிகர வருமானம்", "hi": "शुद्ध आय", "te": "నికర ఆదాయం"},
    "market_advisory": {"en": "Market Advisory", "kn": "ಮಾರುಕಟ್ಟೆ ಸಲಹೆ", "ta": "சந்தை ஆலோசனை", "hi": "बाजार सलाह", "te": "మార్కెట్ సలహా"},

    "applicable_schemes": {"en": "Applicable Schemes", "kn": "ಅನ್ವಯವಾಗುವ ಯೋಜನೆಗಳು", "ta": "பொருந்தும் திட்டங்கள்", "hi": "लागू योजनाएं", "te": "వర్తించే పథకాలు"},
    "benefit": {"en": "Benefit", "kn": "ಪ್ರಯೋಜನ", "ta": "பயன்", "hi": "लाभ", "te": "ప్రయోజనం"},
    "helpline": {"en": "Helpline", "kn": "ಸಹಾಯವಾಣಿ", "ta": "உதவி எண்", "hi": "हेल्पलाइन", "te": "హెల్ప్‌లైన్"},
    "toll_free": {"en": "Toll Free", "kn": "ಟೋಲ್ ಫ್ರೀ", "ta": "இலவச எண்", "hi": "टोल फ्री", "te": "టోల్ ఫ్రీ"},

    "priority": {"en": "Priority", "kn": "ಆದ್ಯತೆ", "ta": "முன்னுரிமை", "hi": "प्राथमिकता", "te": "ప్రాధాన్యత"},
    "timeline": {"en": "Timeline", "kn": "ಕಾಲಮಿತಿ", "ta": "காலவரிசை", "hi": "समयसीमा", "te": "కాలక్రమం"},
    "immediately": {"en": "Immediately", "kn": "ತಕ್ಷಣ", "ta": "உடனடியாக", "hi": "तुरंत", "te": "వెంటనే"},
    "this_week": {"en": "This Week", "kn": "ಈ ವಾರ", "ta": "இந்த வாரம்", "hi": "इस सप्ताह", "te": "ఈ వారం"},
    "before_sowing": {"en": "Before Sowing", "kn": "ಬಿತ್ತನೆಗೆ ಮೊದಲು", "ta": "விதைப்பதற்கு முன்", "hi": "बुवाई से पहले", "te": "విత్తే ముందు"},
    "this_month": {"en": "This Month", "kn": "ಈ ತಿಂಗಳು", "ta": "இந்த மாதம்", "hi": "इस महीने", "te": "ఈ నెల"},

    "footer_note": {"en": "This report was generated by an AI-based advisory system and supports — but does not replace — expert agronomic advice. Verify scheme details on official portals before applying.",
                     "kn": "ಈ ವರದಿಯನ್ನು AI ಆಧಾರಿತ ಸಲಹಾ ವ್ಯವಸ್ಥೆಯಿಂದ ರಚಿಸಲಾಗಿದೆ; ಇದು ತಜ್ಞರ ಸಲಹೆಗೆ ಪೂರಕವಾಗಿದೆ, ಪರ್ಯಾಯವಲ್ಲ. ಅರ್ಜಿ ಸಲ್ಲಿಸುವ ಮೊದಲು ಅಧಿಕೃತ ಪೋರ್ಟಲ್‌ಗಳಲ್ಲಿ ಯೋಜನಾ ವಿವರಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.",
                     "ta": "இந்த அறிக்கை AI ஆதாரித ஆலோசனை முறைமையால் உருவாக்கப்பட்டது; இது வல்லுநர் ஆலோசனைக்கு துணையாக உள்ளது, மாற்றாக அல்ல. விண்ணப்பிக்கும் முன் அதிகாரப்பூர்வ போர்ட்டல்களில் திட்ட விவரங்களை சரிபார்க்கவும்.",
                     "hi": "यह रिपोर्ट AI-आधारित सलाह प्रणाली द्वारा तैयार की गई है और विशेषज्ञ कृषि सलाह की पूरक है, विकल्प नहीं। आवेदन से पहले आधिकारिक पोर्टल पर योजना विवरण सत्यापित करें।",
                     "te": "ఈ నివేదిక AI ఆధారిత సలహా వ్యవస్థ ద్వారా రూపొందించబడింది; ఇది నిపుణుల సలహాకు అనుబంధం, ప్రత్యామ్నాయం కాదు. దరఖాస్తు చేయడానికి ముందు అధికారిక పోర్టళ్లలో పథక వివరాలు ధృవీకరించండి."},
}


def t(key, lang="en"):
    entry = LABELS.get(key, {})
    lang = norm_lang(lang)
    return entry.get(lang, entry.get("en", key))


# ------------------------------------------------------------ CROP NAMES ---
CROP_NAMES = {
    "rice": {"en": "Rice", "kn": "ಭತ್ತ", "ta": "நெல்", "hi": "चावल", "te": "వరి"},
    "maize": {"en": "Maize", "kn": "ಮೆಕ್ಕೆಜೋಳ", "ta": "மக்காச்சோளம்", "hi": "मक्का", "te": "మొక్కజొన్న"},
    "chickpea": {"en": "Chickpea", "kn": "ಕಡಲೆ", "ta": "கொண்டைக்கடலை", "hi": "चना", "te": "శనగలు"},
    "kidneybeans": {"en": "Kidney Beans", "kn": "ರಾಜ್ಮಾ", "ta": "ராஜ்மா", "hi": "राजमा", "te": "రాజ్మా"},
    "pigeonpeas": {"en": "Pigeon Peas", "kn": "ತೊಗರಿ", "ta": "துவரை", "hi": "अरहर", "te": "కంది పప్పు"},
    "mothbeans": {"en": "Moth Beans", "kn": "ಮತ್ಕಿ", "ta": "மொத் பீன்ஸ்", "hi": "मोठ", "te": "మోత్ బీన్స్"},
    "mungbean": {"en": "Mung Bean", "kn": "ಹೆಸರುಬೇಳೆ", "ta": "பாசிப்பயறு", "hi": "मूंग", "te": "పెసలు"},
    "blackgram": {"en": "Black Gram", "kn": "ಉದ್ದಿನಬೇಳೆ", "ta": "உளுந்து", "hi": "उड़द", "te": "మినుములు"},
    "lentil": {"en": "Lentil", "kn": "ಮಸೂರ್ ಬೇಳೆ", "ta": "பருப்பு", "hi": "मसूर", "te": "మసూర్ పప్పు"},
    "pomegranate": {"en": "Pomegranate", "kn": "ದಾಳಿಂಬೆ", "ta": "மாதுளை", "hi": "अनार", "te": "దానిమ్మ"},
    "banana": {"en": "Banana", "kn": "ಬಾಳೆಹಣ್ಣು", "ta": "வாழைப்பழம்", "hi": "केला", "te": "అరటి"},
    "mango": {"en": "Mango", "kn": "ಮಾವು", "ta": "மாம்பழம்", "hi": "आम", "te": "మామిడి"},
    "grapes": {"en": "Grapes", "kn": "ದ್ರಾಕ್ಷಿ", "ta": "திராட்சை", "hi": "अंगूर", "te": "ద్రాక్ష"},
    "watermelon": {"en": "Watermelon", "kn": "ಕಲ್ಲಂಗಡಿ", "ta": "தர்பூசணி", "hi": "तरबूज", "te": "పుచ్చకాయ"},
    "muskmelon": {"en": "Muskmelon", "kn": "ಖರ್ಬೂಜ", "ta": "முலாம்பழம்", "hi": "खरबूजा", "te": "ఖర్బూజా"},
    "apple": {"en": "Apple", "kn": "ಸೇಬು", "ta": "ஆப்பிள்", "hi": "सेब", "te": "ఆపిల్"},
    "orange": {"en": "Orange", "kn": "ಕಿತ್ತಳೆ", "ta": "ஆரஞ்சு", "hi": "संतरा", "te": "నారింజ"},
    "papaya": {"en": "Papaya", "kn": "ಪರಂಗಿ ಹಣ್ಣು", "ta": "பப்பாளி", "hi": "पपीता", "te": "బొప్పాయి"},
    "coconut": {"en": "Coconut", "kn": "ತೆಂಗಿನಕಾಯಿ", "ta": "தேங்காய்", "hi": "नारियल", "te": "కొబ్బరి"},
    "cotton": {"en": "Cotton", "kn": "ಹತ್ತಿ", "ta": "பருத்தி", "hi": "कपास", "te": "పత్తి"},
    "jute": {"en": "Jute", "kn": "ಸೆಣಬು", "ta": "சணல்", "hi": "जूट", "te": "జనుము"},
    "coffee": {"en": "Coffee", "kn": "ಕಾಫಿ", "ta": "காபி", "hi": "कॉफी", "te": "కాఫీ"},
    "wheat": {"en": "Wheat", "kn": "ಗೋಧಿ", "ta": "கோதுமை", "hi": "गेहूं", "te": "గోధుమ"},
    "sugarcane": {"en": "Sugarcane", "kn": "ಕಬ್ಬು", "ta": "கரும்பு", "hi": "गन्ना", "te": "చెరకు"},
    "tomato": {"en": "Tomato", "kn": "ಟೊಮೇಟೊ", "ta": "தக்காளி", "hi": "टमाटर", "te": "టమాటా"},
    "potato": {"en": "Potato", "kn": "ಆಲೂಗಡ್ಡೆ", "ta": "உருளைக்கிழங்கு", "hi": "आलू", "te": "బంగాళదుంప"},
    "soybean": {"en": "Soybean", "kn": "ಸೋಯಾಬೀನ್", "ta": "சோயாபீன்", "hi": "सोयाबीन", "te": "సోయాబీన్"},
    "groundnut": {"en": "Groundnut", "kn": "ಕಡಲೆಕಾಯಿ", "ta": "நிலக்கடலை", "hi": "मूंगफली", "te": "వేరుశనగ"},
}


def crop_name(key, lang="en"):
    if not key:
        return "-"
    entry = CROP_NAMES.get(str(key).lower().strip(), {})
    lang = norm_lang(lang)
    return entry.get(lang, entry.get("en", str(key).title()))


# --------------------------------------------------------- STATUS WORDS ---
STATUS = {
    "Very Low": {"en": "Very Low", "kn": "ಅತಿ ಕಡಿಮೆ", "ta": "மிகக் குறைவு", "hi": "बहुत कम", "te": "చాలా తక్కువ"},
    "Low": {"en": "Low", "kn": "ಕಡಿಮೆ", "ta": "குறைவு", "hi": "कम", "te": "తక్కువ"},
    "Optimal": {"en": "Optimal", "kn": "ಸೂಕ್ತ", "ta": "உகந்தது", "hi": "उपयुक्त", "te": "సరైనది"},
    "High": {"en": "High", "kn": "ಹೆಚ್ಚು", "ta": "அதிகம்", "hi": "अधिक", "te": "ఎక్కువ"},
    "Very High": {"en": "Very High", "kn": "ಅತಿ ಹೆಚ್ಚು", "ta": "மிக அதிகம்", "hi": "बहुत अधिक", "te": "చాలా ఎక్కువ"},
    "Excellent": {"en": "Excellent", "kn": "ಅತ್ಯುತ್ತಮ", "ta": "மிகச் சிறந்தது", "hi": "उत्कृष्ट", "te": "అద్భుతం"},
    "Good": {"en": "Good", "kn": "ಉತ್ತಮ", "ta": "நல்லது", "hi": "अच्छा", "te": "మంచిది"},
    "Fair": {"en": "Fair", "kn": "ಸಾಧಾರಣ", "ta": "நடுத்தரம்", "hi": "ठीक", "te": "మధ్యస్థం"},
    "Poor": {"en": "Poor", "kn": "ಕಳಪೆ", "ta": "மோசம்", "hi": "खराब", "te": "పేలవం"},
    "Rising": {"en": "Rising", "kn": "ಏರುತ್ತಿದೆ", "ta": "உயர்கிறது", "hi": "बढ़ रहा है", "te": "పెరుగుతోంది"},
    "Falling": {"en": "Falling", "kn": "ಇಳಿಯುತ್ತಿದೆ", "ta": "குறைகிறது", "hi": "घट रहा है", "te": "తగ్గుతోంది"},
    "Stable": {"en": "Stable", "kn": "ಸ್ಥಿರ", "ta": "நிலையானது", "hi": "स्थिर", "te": "స్థిరంగా"},
    "Volatile": {"en": "Volatile", "kn": "ಅಸ್ಥಿರ", "ta": "நிலையற்றது", "hi": "अस्थिर", "te": "అస్థిరం"},
    "Seasonal": {"en": "Seasonal", "kn": "ಋತುಮಾನದ", "ta": "பருவகாலம்", "hi": "मौसमी", "te": "కాలానుగుణం"},
    "None": {"en": "None", "kn": "ಯಾವುದೂ ಇಲ್ಲ", "ta": "இல்லை", "hi": "कोई नहीं", "te": "ఏదీ లేదు"},
    "Moderate": {"en": "Moderate", "kn": "ಮಧ್ಯಮ", "ta": "மிதமான", "hi": "मध्यम", "te": "మధ్యస్థ"},
    "healthy": {"en": "Healthy", "kn": "ಆರೋಗ್ಯಕರ", "ta": "ஆரோக்கியமானது", "hi": "स्वस्थ", "te": "ఆరోగ్యంగా"},
    "diseased": {"en": "Diseased", "kn": "ರೋಗಪೀಡಿತ", "ta": "நோய்வாய்ப்பட்டது", "hi": "रोगग्रस्त", "te": "వ్యాధిగ్రస్తం"},
    "Acidic": {"en": "Acidic", "kn": "ಆಮ್ಲೀಯ", "ta": "அமிலத்தன்மை", "hi": "अम्लीय", "te": "ఆమ్లం"},
    "Alkaline": {"en": "Alkaline", "kn": "ಕ್ಷಾರೀಯ", "ta": "காரத்தன்மை", "hi": "क्षारीय", "te": "క్షారం"},
}


def status(word, lang="en"):
    if not word:
        return "-"
    entry = STATUS.get(str(word).strip(), {})
    lang = norm_lang(lang)
    return entry.get(lang, entry.get("en", word))


# ------------------------------------------------------- WEATHER PHRASES ---
WEATHER_PHRASES = {
    "high_heat": {"en": "🌡️ High heat: Increase irrigation; use shade nets.", "kn": "🌡️ ಹೆಚ್ಚಿನ ಶಾಖ: ನೀರಾವರಿ ಹೆಚ್ಚಿಸಿ; ಶೇಡ್ ನೆಟ್ ಬಳಸಿ.", "ta": "🌡️ அதிக வெப்பம்: பாசனத்தை அதிகரிக்கவும்; நிழல் வலை பயன்படுத்தவும்.", "hi": "🌡️ अधिक गर्मी: सिंचाई बढ़ाएं; शेड नेट का उपयोग करें।", "te": "🌡️ అధిక వేడి: నీటిపారుదల పెంచండి; షేడ్ నెట్ ఉపయోగించండి."},
    "cool": {"en": "❄️ Cool conditions: Protect seedlings from cold damage.", "kn": "❄️ ತಂಪಾದ ಪರಿಸ್ಥಿತಿ: ಸಸಿಗಳನ್ನು ಚಳಿಯ ಹಾನಿಯಿಂದ ರಕ್ಷಿಸಿ.", "ta": "❄️ குளிர்ந்த நிலை: இளம் தாவரங்களை குளிர் சேதத்திலிருந்து பாதுகாக்கவும்.", "hi": "❄️ ठंडी स्थिति: पौध को ठंड से बचाएं।", "te": "❄️ చల్లని పరిస్థితులు: మొలకలను చలి నష్టం నుండి రక్షించండి."},
    "optimal_temp": {"en": "🌤️ Optimal temperature for most crops.", "kn": "🌤️ ಹೆಚ್ಚಿನ ಬೆಳೆಗಳಿಗೆ ಸೂಕ್ತ ತಾಪಮಾನ.", "ta": "🌤️ பெரும்பாலான பயிர்களுக்கு உகந்த வெப்பநிலை.", "hi": "🌤️ अधिकांश फसलों के लिए उपयुक्त तापमान।", "te": "🌤️ చాలా పంటలకు అనువైన ఉష్ణోగ్రత."},
    "high_humidity": {"en": "💧 High humidity: Fungal disease risk. Apply preventive fungicide.", "kn": "💧 ಹೆಚ್ಚಿನ ಆರ್ದ್ರತೆ: ಶಿಲೀಂಧ್ರ ರೋಗದ ಅಪಾಯ. ತಡೆಗಟ್ಟುವ ಶಿಲೀಂಧ್ರನಾಶಕ ಬಳಸಿ.", "ta": "💧 அதிக ஈரப்பதம்: பூஞ்சை நோய் அபாயம். தடுப்பு பூஞ்சைக்கொல்லி பயன்படுத்தவும்.", "hi": "💧 अधिक आर्द्रता: फफूंद रोग का खतरा। निवारक फफूंदनाशक लगाएं।", "te": "💧 అధిక తేమ: శిలీంధ్ర వ్యాధి ప్రమాదం. నివారణ శిలీంధ్రనాశకం వేయండి."},
    "low_humidity": {"en": "🏜️ Low humidity: Increase irrigation; mulch soil.", "kn": "🏜️ ಕಡಿಮೆ ಆರ್ದ್ರತೆ: ನೀರಾವರಿ ಹೆಚ್ಚಿಸಿ; ಮಣ್ಣಿಗೆ ಮಲ್ಚ್ ಹಾಕಿ.", "ta": "🏜️ குறைந்த ஈரப்பதம்: பாசனத்தை அதிகரிக்கவும்; மண்ணை மல்ச் செய்யவும்.", "hi": "🏜️ कम आर्द्रता: सिंचाई बढ़ाएं; मिट्टी पर मल्च करें।", "te": "🏜️ తక్కువ తేమ: నీటిపారుదల పెంచండి; నేలకు మల్చ్ చేయండి."},
    "heavy_rain": {"en": "🌧️ Heavy rainfall: Ensure drainage; delay fertiliser.", "kn": "🌧️ ಭಾರೀ ಮಳೆ: ಒಳಚರಂಡಿ ಖಚಿತಪಡಿಸಿ; ಗೊಬ್ಬರವನ್ನು ವಿಳಂಬಿಸಿ.", "ta": "🌧️ கனமழை: வடிகால் உறுதி செய்யவும்; உரமிடுவதை தாமதப்படுத்தவும்.", "hi": "🌧️ भारी वर्षा: जल निकासी सुनिश्चित करें; उर्वरक में देरी करें।", "te": "🌧️ భారీ వర్షం: డ్రైనేజీ నిర్ధారించండి; ఎరువులు ఆలస్యం చేయండి."},
    "no_rain_heat": {"en": "☀️ No rain + high heat: Irrigate early morning or late evening.", "kn": "☀️ ಮಳೆ ಇಲ್ಲ + ಹೆಚ್ಚಿನ ಶಾಖ: ಬೆಳಿಗ್ಗೆ ಬೇಗ ಅಥವಾ ಸಂಜೆ ತಡವಾಗಿ ನೀರಾವರಿ ಮಾಡಿ.", "ta": "☀️ மழை இல்லை + அதிக வெப்பம்: அதிகாலை அல்லது மாலையில் பாசனம் செய்யவும்.", "hi": "☀️ बारिश नहीं + अधिक गर्मी: सुबह जल्दी या शाम को देर से सिंचाई करें।", "te": "☀️ వర్షం లేదు + అధిక వేడి: ఉదయం లేదా సాయంత్రం ఆలస్యంగా నీరు పెట్టండి."},
    "strong_wind": {"en": "💨 Strong winds: Avoid pesticide spraying.", "kn": "💨 ಬಲವಾದ ಗಾಳಿ: ಕೀಟನಾಶಕ ಸಿಂಪಡಣೆ ತಪ್ಪಿಸಿ.", "ta": "💨 பலத்த காற்று: பூச்சிக்கொல்லி தெளிப்பதை தவிர்க்கவும்.", "hi": "💨 तेज़ हवा: कीटनाशक छिड़काव से बचें।", "te": "💨 బలమైన గాలులు: పురుగుమందుల పిచికారీ నివారించండి."},
}


def weather_phrase(key, lang="en"):
    entry = WEATHER_PHRASES.get(key, {})
    return entry.get(norm_lang(lang), entry.get("en", ""))


# ---------------------------------------------------------- SOIL PHRASES ---
def soil_phrase_n_low(lang):
    return {"en": "Apply Urea (46-0-0) at 100 kg/ha or FYM at 5 tonnes/ha.", "kn": "ಯೂರಿಯಾ (46-0-0) ಅನ್ನು 100 ಕೆಜಿ/ಹೆ. ಅಥವಾ FYM 5 ಟನ್/ಹೆ. ಅನ್ವಯಿಸಿ.", "ta": "யூரியா (46-0-0) 100 கிலோ/ஹெக்டேர் அல்லது FYM 5 டன்/ஹெக்டேர் இடவும்.", "hi": "यूरिया (46-0-0) 100 किग्रा/हेक्टेयर या FYM 5 टन/हेक्टेयर डालें।", "te": "యూరియా (46-0-0) 100 కిలో/హెక్టారు లేదా FYM 5 టన్నులు/హెక్టారు వేయండి."}.get(norm_lang(lang))


def soil_phrase_n_high(lang):
    return {"en": "Reduce nitrogen — excess causes vegetative overgrowth.", "kn": "ಸಾರಜನಕ ಕಡಿಮೆ ಮಾಡಿ — ಅಧಿಕವಾದರೆ ಎಲೆ ಬೆಳವಣಿಗೆ ಅತಿಯಾಗುತ್ತದೆ.", "ta": "நைட்ரஜனை குறைக்கவும் — அதிகமானால் தாவர வளர்ச்சி மிகைப்படும்.", "hi": "नाइट्रोजन कम करें — अधिकता से अनियंत्रित वानस्पतिक वृद्धि होती है।", "te": "నత్రజనిని తగ్గించండి — అధికమైతే ఆకుల పెరుగుదల మితిమీరుతుంది."}.get(norm_lang(lang))


def soil_phrase_p_low(lang):
    return {"en": "Apply DAP (18-46-0) at 100 kg/ha.", "kn": "DAP (18-46-0) ಅನ್ನು 100 ಕೆಜಿ/ಹೆ. ಅನ್ವಯಿಸಿ.", "ta": "DAP (18-46-0) 100 கிலோ/ஹெக்டேர் இடவும்.", "hi": "DAP (18-46-0) 100 किग्रा/हेक्टेयर डालें।", "te": "DAP (18-46-0) 100 కిలో/హెక్టారు వేయండి."}.get(norm_lang(lang))


def soil_phrase_p_high(lang):
    return {"en": "Skip phosphorus application this season.", "kn": "ಈ ಋತುವಿನಲ್ಲಿ ರಂಜಕ ಬಳಕೆ ಬೇಡ.", "ta": "இந்த பருவத்தில் பாஸ்பரஸ் இடுவதை தவிர்க்கவும்.", "hi": "इस मौसम में फास्फोरस न डालें।", "te": "ఈ సీజన్‌లో భాస్వరం వేయవద్దు."}.get(norm_lang(lang))


def soil_phrase_k_low(lang):
    return {"en": "Apply Muriate of Potash (0-0-60) at 50 kg/ha.", "kn": "ಮ್ಯೂರಿಯೇಟ್ ಆಫ್ ಪೊಟ್ಯಾಶ್ (0-0-60) ಅನ್ನು 50 ಕೆಜಿ/ಹೆ. ಅನ್ವಯಿಸಿ.", "ta": "மியூரியேட் ஆஃப் பொட்டாஷ் (0-0-60) 50 கிலோ/ஹெக்டேர் இடவும்.", "hi": "म्यूरेट ऑफ पोटाश (0-0-60) 50 किग्रा/हेक्टेयर डालें।", "te": "మ్యూరియేట్ ఆఫ్ పొటాష్ (0-0-60) 50 కిలో/హెక్టారు వేయండి."}.get(norm_lang(lang))


def soil_phrase_ph_acidic(lang):
    return {"en": "Acidic soil: Apply agricultural lime at 2–4 tonnes/ha.", "kn": "ಆಮ್ಲೀಯ ಮಣ್ಣು: ಕೃಷಿ ಸುಣ್ಣವನ್ನು 2–4 ಟನ್/ಹೆ. ಅನ್ವಯಿಸಿ.", "ta": "அமில மண்: விவசாய சுண்ணாம்பு 2–4 டன்/ஹெக்டேர் இடவும்.", "hi": "अम्लीय मिट्टी: कृषि चूना 2–4 टन/हेक्टेयर डालें।", "te": "ఆమ్ల నేల: వ్యవసాయ సున్నం 2–4 టన్నులు/హెక్టారు వేయండి."}.get(norm_lang(lang))


def soil_phrase_ph_alkaline(lang):
    return {"en": "Alkaline soil: Apply gypsum or sulphur to lower pH.", "kn": "ಕ್ಷಾರೀಯ ಮಣ್ಣು: pH ಕಡಿಮೆ ಮಾಡಲು ಜಿಪ್ಸಂ ಅಥವಾ ಗಂಧಕ ಅನ್ವಯಿಸಿ.", "ta": "காரம் மண்: pH குறைக்க ஜிப்சம் அல்லது கந்தகம் இடவும்.", "hi": "क्षारीय मिट्टी: pH कम करने हेतु जिप्सम या सल्फर डालें।", "te": "క్షార నేల: pH తగ్గించడానికి జిప్సం లేదా గంధకం వేయండి."}.get(norm_lang(lang))


def soil_phrase_ph_optimal(lang):
    return {"en": "pH is optimal (6–7). No pH amendment needed.", "kn": "pH ಸೂಕ್ತವಾಗಿದೆ (6–7). ಯಾವುದೇ pH ತಿದ್ದುಪಡಿ ಅಗತ್ಯವಿಲ್ಲ.", "ta": "pH உகந்ததாக உள்ளது (6–7). pH திருத்தம் தேவையில்லை.", "hi": "pH उपयुक्त है (6–7)। किसी सुधार की आवश्यकता नहीं।", "te": "pH సరైనది (6–7). ఎలాంటి సవరణ అవసరం లేదు."}.get(norm_lang(lang))


def soil_phrase_balanced(lang):
    return {"en": "Soil nutrients are balanced. Maintain with compost.", "kn": "ಮಣ್ಣಿನ ಪೋಷಕಾಂಶಗಳು ಸಮತೋಲಿತವಾಗಿವೆ. ಕಾಂಪೋಸ್ಟ್‌ನೊಂದಿಗೆ ನಿರ್ವಹಿಸಿ.", "ta": "மண் ஊட்டச்சத்துக்கள் சமநிலையில் உள்ளன. உரம் மூலம் பராமரிக்கவும்.", "hi": "मिट्टी के पोषक तत्व संतुलित हैं। कंपोस्ट से बनाए रखें।", "te": "నేల పోషకాలు సమతుల్యంగా ఉన్నాయి. కంపోస్ట్‌తో నిర్వహించండి."}.get(norm_lang(lang))


# -------------------------------------------------------- MARKET PHRASES ---
def market_phrase_rising(lang):
    return {"en": "📈 Prices rising. Consider holding stock 2–4 weeks.", "kn": "📈 ಬೆಲೆ ಏರುತ್ತಿದೆ. 2–4 ವಾರ ಸಂಗ್ರಹಿಸಿಡುವುದನ್ನು ಪರಿಗಣಿಸಿ.", "ta": "📈 விலை உயர்கிறது. 2–4 வாரங்கள் சேமித்து வைக்கலாம்.", "hi": "📈 कीमतें बढ़ रही हैं। 2–4 सप्ताह स्टॉक रोकने पर विचार करें।", "te": "📈 ధరలు పెరుగుతున్నాయి. 2–4 వారాలు నిల్వ ఉంచడం పరిశీలించండి."}.get(norm_lang(lang))


def market_phrase_volatile(lang):
    return {"en": "⚠️ Volatile prices. Sell in small batches.", "kn": "⚠️ ಅಸ್ಥಿರ ಬೆಲೆ. ಸಣ್ಣ ಪ್ರಮಾಣದಲ್ಲಿ ಮಾರಾಟ ಮಾಡಿ.", "ta": "⚠️ நிலையற்ற விலை. சிறு அளவில் விற்கவும்.", "hi": "⚠️ अस्थिर कीमतें। छोटे बैचों में बेचें।", "te": "⚠️ అస్థిర ధరలు. చిన్న మొత్తాలలో అమ్మండి."}.get(norm_lang(lang))


def market_phrase_stable(lang):
    return {"en": "📊 Stable price. Sell soon after harvest.", "kn": "📊 ಸ್ಥಿರ ಬೆಲೆ. ಕೊಯ್ಲಿನ ನಂತರ ಬೇಗ ಮಾರಾಟ ಮಾಡಿ.", "ta": "📊 நிலையான விலை. அறுவடைக்குப் பிறகு விற்கவும்.", "hi": "📊 स्थिर मूल्य। कटाई के तुरंत बाद बेचें।", "te": "📊 స్థిర ధర. కోత తర్వాత వెంటనే అమ్మండి."}.get(norm_lang(lang))


def market_phrase_income(lang, amount):
    tmpl = {"en": "✅ Estimated net income: ₹{amt}.", "kn": "✅ ಅಂದಾಜು ನಿವ್ವಳ ಆದಾಯ: ₹{amt}.", "ta": "✅ மதிப்பிடப்பட்ட நிகர வருமானம்: ₹{amt}.", "hi": "✅ अनुमानित शुद्ध आय: ₹{amt}।", "te": "✅ అంచనా నికర ఆదాయం: ₹{amt}."}.get(norm_lang(lang))
    return tmpl.format(amt=f"{amount:,}")


# -------------------------------------------------------- POLICY PHRASES ---
def policy_advisory_lines(lang):
    return {
        "en": ["📋 Register on pmkisan.gov.in for ₹6,000/year.", "🌾 Enrol in PMFBY before sowing season.", "💳 Apply for Kisan Credit Card for low-interest credit."],
        "kn": ["📋 ₹6,000/ವರ್ಷಕ್ಕಾಗಿ pmkisan.gov.in ನಲ್ಲಿ ನೋಂದಾಯಿಸಿ.", "🌾 ಬಿತ್ತನೆ ಋತುವಿನ ಮೊದಲು PMFBY ಗೆ ಸೇರಿ.", "💳 ಕಡಿಮೆ ಬಡ್ಡಿ ಸಾಲಕ್ಕಾಗಿ ಕಿಸಾನ್ ಕ್ರೆಡಿಟ್ ಕಾರ್ಡ್‌ಗೆ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ."],
        "ta": ["📋 ₹6,000/ஆண்டுக்கு pmkisan.gov.in இல் பதிவு செய்யவும்.", "🌾 விதைப்பு பருவத்திற்கு முன் PMFBY இல் சேரவும்.", "💳 குறைந்த வட்டி கடனுக்கு கிசான் கிரெடிட் கார்டுக்கு விண்ணப்பிக்கவும்."],
        "hi": ["📋 ₹6,000/वर्ष हेतु pmkisan.gov.in पर पंजीकरण करें।", "🌾 बुवाई से पहले PMFBY में नामांकन करें।", "💳 कम ब्याज ऋण हेतु किसान क्रेडिट कार्ड के लिए आवेदन करें।"],
        "te": ["📋 ₹6,000/సంవత్సరం కోసం pmkisan.gov.in లో నమోదు చేసుకోండి.", "🌾 విత్తే సీజన్‌కు ముందు PMFBYలో చేరండి.", "💳 తక్కువ వడ్డీ రుణం కోసం కిసాన్ క్రెడిట్ కార్డ్‌కు దరఖాస్తు చేయండి."],
    }.get(norm_lang(lang))


def policy_key_insight(lang):
    return {"en": "Register on pmkisan.gov.in for ₹6,000/year income support.", "kn": "₹6,000/ವರ್ಷದ ಆದಾಯ ಬೆಂಬಲಕ್ಕಾಗಿ pmkisan.gov.in ನಲ್ಲಿ ನೋಂದಾಯಿಸಿ.", "ta": "₹6,000/ஆண்டு வருமான ஆதரவுக்கு pmkisan.gov.in இல் பதிவு செய்யவும்.", "hi": "₹6,000/वर्ष आय सहायता हेतु pmkisan.gov.in पर पंजीकरण करें।", "te": "₹6,000/సంవత్సరం ఆదాయ మద్దతు కోసం pmkisan.gov.in లో నమోదు చేసుకోండి."}.get(norm_lang(lang))


# ------------------------------------------------------- REPORT SENTENCES ---
def executive_summary(lang, loc, top_crop_display, soil_score, disease_line, avg_price_display, net_income_display):
    tmpl = {
        "en": "Based on your soil parameters for {loc}, AI recommends growing {crop} this season. Soil health: {score}/100. {disease} Market price: {price}. Estimated net income: {income}.",
        "kn": "{loc} ಗಾಗಿ ನಿಮ್ಮ ಮಣ್ಣಿನ ನಿಯತಾಂಕಗಳ ಆಧಾರದ ಮೇಲೆ, AI ಈ ಋತುವಿನಲ್ಲಿ {crop} ಬೆಳೆಯಲು ಶಿಫಾರಸು ಮಾಡುತ್ತದೆ. ಮಣ್ಣಿನ ಆರೋಗ್ಯ: {score}/100. {disease} ಮಾರುಕಟ್ಟೆ ಬೆಲೆ: {price}. ಅಂದಾಜು ನಿವ್ವಳ ಆದಾಯ: {income}.",
        "ta": "{loc} க்கான உங்கள் மண் அளவுருக்களின் அடிப்படையில், AI இந்த பருவத்தில் {crop} வளர்க்க பரிந்துரைக்கிறது. மண் ஆரோக்கியம்: {score}/100. {disease} சந்தை விலை: {price}. மதிப்பிடப்பட்ட நிகர வருமானம்: {income}.",
        "hi": "{loc} के लिए आपकी मिट्टी के मापदंडों के आधार पर, AI इस मौसम में {crop} उगाने की सलाह देता है। मिट्टी स्वास्थ्य: {score}/100। {disease} बाजार मूल्य: {price}। अनुमानित शुद्ध आय: {income}।",
        "te": "{loc} కోసం మీ నేల పారామితుల ఆధారంగా, AI ఈ సీజన్‌లో {crop} పండించాలని సిఫార్సు చేస్తోంది. నేల ఆరోగ్యం: {score}/100. {disease} మార్కెట్ ధర: {price}. అంచనా నికర ఆదాయం: {income}.",
    }.get(norm_lang(lang))
    return tmpl.format(loc=loc, crop=top_crop_display.upper(), score=soil_score, disease=disease_line, price=avg_price_display, income=net_income_display)


def disease_summary_line(lang, healthy, disease_name=None):
    if healthy:
        return {"en": "No disease detected.", "kn": "ಯಾವುದೇ ರೋಗ ಪತ್ತೆಯಾಗಿಲ್ಲ.", "ta": "நோய் எதுவும் கண்டறியப்படவில்லை.", "hi": "कोई रोग नहीं मिला।", "te": "వ్యాధి ఏదీ కనుగొనబడలేదు."}.get(norm_lang(lang))
    tmpl = {"en": "⚠️ {d} detected. Immediate treatment advised.", "kn": "⚠️ {d} ಪತ್ತೆಯಾಗಿದೆ. ತಕ್ಷಣ ಚಿಕಿತ್ಸೆ ಸಲಹೆ.", "ta": "⚠️ {d} கண்டறியப்பட்டது. உடனடி சிகிச்சை பரிந்துரைக்கப்படுகிறது.", "hi": "⚠️ {d} पाया गया। तत्काल उपचार आवश्यक।", "te": "⚠️ {d} కనుగొనబడింది. వెంటనే చికిత్స సిఫార్సు చేయబడింది."}.get(norm_lang(lang))
    return tmpl.format(d=disease_name or "")


def soil_key_insight(lang, score):
    good = score >= 70
    if good:
        return {"en": f"Soil health: {score}/100. Minimal amendments needed.", "kn": f"ಮಣ್ಣಿನ ಆರೋಗ್ಯ: {score}/100. ಕನಿಷ್ಠ ತಿದ್ದುಪಡಿ ಅಗತ್ಯ.", "ta": f"மண் ஆரோக்கியம்: {score}/100. குறைந்தபட்ச திருத்தம் தேவை.", "hi": f"मिट्टी स्वास्थ्य: {score}/100। न्यूनतम सुधार आवश्यक।", "te": f"నేల ఆరోగ్యం: {score}/100. కనీస సవరణలు అవసరం."}.get(norm_lang(lang))
    return {"en": f"Soil health: {score}/100. Improvement recommended.", "kn": f"ಮಣ್ಣಿನ ಆರೋಗ್ಯ: {score}/100. ಸುಧಾರಣೆ ಶಿಫಾರಸು.", "ta": f"மண் ஆரோக்கியம்: {score}/100. மேம்பாடு பரிந்துரைக்கப்படுகிறது.", "hi": f"मिट्टी स्वास्थ्य: {score}/100। सुधार अनुशंसित।", "te": f"నేల ఆరోగ్యం: {score}/100. మెరుగుదల సిఫార్సు చేయబడింది."}.get(norm_lang(lang))


def crop_key_insight(lang, crop_display, conf):
    tmpl = {"en": "Based on your soil NPK and climate data, {c} is most suitable with {p}% confidence.", "kn": "ನಿಮ್ಮ ಮಣ್ಣಿನ NPK ಮತ್ತು ಹವಾಮಾನ ದತ್ತಾಂಶದ ಆಧಾರದ ಮೇಲೆ, {c} {p}% ವಿಶ್ವಾಸದೊಂದಿಗೆ ಅತ್ಯಂತ ಸೂಕ್ತವಾಗಿದೆ.", "ta": "உங்கள் மண் NPK மற்றும் காலநிலை தரவின் அடிப்படையில், {c} {p}% நம்பிக்கையுடன் மிகவும் பொருத்தமானது.", "hi": "आपकी मिट्टी NPK और जलवायु डेटा के आधार पर, {c} {p}% विश्वास के साथ सबसे उपयुक्त है।", "te": "మీ నేల NPK మరియు వాతావరణ డేటా ఆధారంగా, {c} {p}% విశ్వాసంతో అత్యంత అనుకూలం."}.get(norm_lang(lang))
    return tmpl.format(c=crop_display, p=conf)
