"""
Chatbot Agent
---------------
A conversational assistant for the Smart Crop Advisory System. Since this
app has real user accounts, the chatbot pulls context from the farmer's
own MOST RECENT saved advisory (via database.py) rather than a throwaway
session — so "which crop should I grow?" answers with the farmer's actual
last recommendation, even in a brand-new chat window days later.

Rule-based intent matching answers with zero configuration. If
GEMINI_API_KEY is set, open-ended free text that doesn't match a known
intent is additionally routed to Gemini for a grounded free-text answer.
"""
import os
from utils.logger import get_logger
import i18n
logger=get_logger(__name__)

GEMINI_API_KEY=os.environ.get('GEMINI_API_KEY','')

CHIPS=[
    {'intent':'ask_crop','en':'Which crop should I grow?','kn':'ಯಾವ ಬೆಳೆ ಬೆಳೆಯಬೇಕು?','ta':'எந்த பயிர் வளர்க்க வேண்டும்?','hi':'मुझे कौन सी फसल उगानी चाहिए?','te':'నేను ఏ పంట పండించాలి?'},
    {'intent':'ask_fert','en':'Fertiliser plan','kn':'ಗೊಬ್ಬರ ಯೋಜನೆ','ta':'உர திட்டம்','hi':'उर्वरक योजना','te':'ఎరువుల ప్రణాళిక'},
    {'intent':'ask_weather','en':'Weather advice','kn':'ಹವಾಮಾನ ಸಲಹೆ','ta':'வானிலை ஆலோசனை','hi':'मौसम सलाह','te':'వాతావరణ సలహా'},
    {'intent':'ask_market','en':'Market price today','kn':'ಇಂದಿನ ಮಾರುಕಟ್ಟೆ ಬೆಲೆ','ta':'இன்றைய சந்தை விலை','hi':'आज का बाजार भाव','te':'నేటి మార్కెట్ ధర'},
    {'intent':'ask_scheme','en':'Government schemes','kn':'ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು','ta':'அரசு திட்டங்கள்','hi':'सरकारी योजनाएं','te':'ప్రభుత్వ పథకాలు'},
    {'intent':'ask_disease','en':'My plant looks sick','kn':'ನನ್ನ ಸಸ್ಯ ಅನಾರೋಗ್ಯವಾಗಿದೆ','ta':'என் செடி நோய்வாய்ப்பட்டுள்ளது','hi':'मेरा पौधा बीमार लग रहा है','te':'నా మొక్క అనారోగ్యంగా కనిపిస్తోంది'},
    {'intent':'ask_soil','en':'About my soil health','kn':'ನನ್ನ ಮಣ್ಣಿನ ಆರೋಗ್ಯ','ta':'என் மண் ஆரோக்கியம் பற்றி','hi':'मिट्टी के स्वास्थ्य के बारे में','te':'నా నేల ఆరోగ్యం గురించి'},
]

TEMPLATES={
 'greeting':{'en':"Namaste {name}! 🌱 I'm your crop advisory assistant. Ask me about crops, fertiliser, weather, market prices, government schemes, or plant diseases — or tap a suggestion below.",
             'kn':"ನಮಸ್ಕಾರ {name}! 🌱 ನಾನು ನಿಮ್ಮ ಬೆಳೆ ಸಲಹಾ ಸಹಾಯಕ. ಬೆಳೆ, ಗೊಬ್ಬರ, ಹವಾಮಾನ, ಮಾರುಕಟ್ಟೆ ಬೆಲೆ, ಯೋಜನೆ ಅಥವಾ ರೋಗಗಳ ಬಗ್ಗೆ ಕೇಳಿ.",
             'ta':"வணக்கம் {name}! 🌱 நான் உங்கள் பயிர் ஆலோசனை உதவியாளர். பயிர், உரம், வானிலை, சந்தை விலை, திட்டங்கள் அல்லது நோய்கள் பற்றி கேளுங்கள்.",
             'hi':"नमस्ते {name}! 🌱 मैं आपका फसल सलाह सहायक हूं। फसल, उर्वरक, मौसम, बाजार भाव, योजनाओं या रोगों के बारे में पूछें।",
             'te':"నమస్తే {name}! 🌱 నేను మీ పంట సలహా సహాయకుడిని. పంటలు, ఎరువులు, వాతావరణం, ధరలు, పథకాలు లేదా వ్యాధుల గురించి అడగండి."},
 'no_history':{'en':"You haven't generated an advisory report yet. Go to 'Get Advisory' and fill in your farm details — then I can answer using your own data!",
               'kn':"ನೀವು ಇನ್ನೂ ಸಲಹಾ ವರದಿ ರಚಿಸಿಲ್ಲ. 'Get Advisory' ಗೆ ಹೋಗಿ ವಿವರ ತುಂಬಿ — ನಂತರ ನಿಮ್ಮ ಡೇಟಾ ಬಳಸಿ ಉತ್ತರಿಸುತ್ತೇನೆ!",
               'ta':"நீங்கள் இன்னும் அறிக்கை உருவாக்கவில்லை. 'Get Advisory' க்குச் சென்று விவரங்களை நிரப்பவும் — பிறகு உங்கள் தரவைப் பயன்படுத்தி பதிலளிப்பேன்!",
               'hi':"आपने अभी तक रिपोर्ट नहीं बनाई। 'Get Advisory' पर जाएं और विवरण भरें — फिर मैं आपके डेटा से उत्तर दूंगा!",
               'te':"మీరు ఇంకా నివేదిక రూపొందించలేదు. 'Get Advisory'కి వెళ్లి వివరాలు నింపండి — తర్వాత మీ డేటాతో సమాధానం ఇస్తాను!"},
 'ask_crop':{'en':"Your last advisory recommended {crop} ({conf}% confidence) for {loc}. Other good options: {others}.",
             'kn':"{loc} ಗಾಗಿ ನಿಮ್ಮ ಕೊನೆಯ ಸಲಹೆ {crop} ({conf}% ವಿಶ್ವಾಸ) ಶಿಫಾರಸು ಮಾಡಿತ್ತು. ಇತರ ಆಯ್ಕೆಗಳು: {others}.",
             'ta':"{loc} க்கான உங்கள் கடைசி அறிக்கை {crop} ({conf}% நம்பிக்கை) பரிந்துரைத்தது. மற்ற விருப்பங்கள்: {others}.",
             'hi':"{loc} के लिए आपकी पिछली रिपोर्ट में {crop} ({conf}% विश्वास) की सिफारिश की गई थी। अन्य विकल्प: {others}।",
             'te':"{loc} కోసం మీ చివరి నివేదిక {crop} ({conf}% విశ్వాసం) సిఫార్సు చేసింది. ఇతర ఎంపికలు: {others}."},
 'ask_fert':{'en':"For {crop}: {plan}",'kn':"{crop} ಗೆ: {plan}",'ta':"{crop} க்கு: {plan}",'hi':"{crop} के लिए: {plan}",'te':"{crop} కోసం: {plan}"},
 'ask_weather':{'en':"Last known conditions in {loc}: {temp}°C, {hum}% humidity, {rain}mm rainfall. {advisory}",
                'kn':"{loc} ನಲ್ಲಿ ಕೊನೆಯ ಹವಾಮಾನ: {temp}°C, {hum}% ಆರ್ದ್ರತೆ, {rain}mm ಮಳೆ. {advisory}",
                'ta':"{loc} இல் கடைசி வானிலை: {temp}°C, {hum}% ஈரப்பதம், {rain}mm மழை. {advisory}",
                'hi':"{loc} में अंतिम मौसम: {temp}°C, {hum}% आर्द्रता, {rain}mm वर्षा। {advisory}",
                'te':"{loc}లో చివరి వాతావరణం: {temp}°C, {hum}% తేమ, {rain}mm వర్షం. {advisory}"},
 'ask_market':{'en':"{crop}: avg ₹{price}/quintal, trend {trend}. Estimated net income for your {area} ha: ₹{income}.",
               'kn':"{crop}: ಸರಾಸರಿ ₹{price}/ಕ್ವಿಂಟಲ್, ಪ್ರವೃತ್ತಿ {trend}. ನಿಮ್ಮ {area} ಹೆ.ಗೆ ಅಂದಾಜು ಆದಾಯ: ₹{income}.",
               'ta':"{crop}: சராசரி ₹{price}/குவிண்டல், போக்கு {trend}. உங்கள் {area} ஹெக்டேருக்கு மதிப்பிடப்பட்ட வருமானம்: ₹{income}.",
               'hi':"{crop}: औसत ₹{price}/क्विंटल, रुझान {trend}। आपके {area} हेक्टेयर के लिए अनुमानित आय: ₹{income}।",
               'te':"{crop}: సగటు ₹{price}/క్వింటాల్, ధోరణి {trend}. మీ {area} హెక్టార్లకు అంచనా ఆదాయం: ₹{income}."},
 'ask_scheme':{'en':"Key schemes: PM-KISAN (income support), PMFBY (crop insurance), Kisan Credit Card (low-interest loans), Soil Health Card (free soil testing). See the 'Policy & Schemes' section of your report for full details.",
               'kn':"ಪ್ರಮುಖ ಯೋಜನೆಗಳು: PM-KISAN, PMFBY, ಕಿಸಾನ್ ಕ್ರೆಡಿಟ್ ಕಾರ್ಡ್, ಸಾಯಿಲ್ ಹೆಲ್ತ್ ಕಾರ್ಡ್. ಪೂರ್ಣ ವಿವರಗಳಿಗೆ ವರದಿಯ 'Policy & Schemes' ವಿಭಾಗ ನೋಡಿ.",
               'ta':"முக்கிய திட்டங்கள்: PM-KISAN, PMFBY, கிசான் கிரெடிட் கார்டு, மண் சுகாதார அட்டை. முழு விவரங்களுக்கு உங்கள் அறிக்கையின் 'Policy & Schemes' பகுதியைப் பாருங்கள்.",
               'hi':"मुख्य योजनाएं: PM-KISAN, PMFBY, किसान क्रेडिट कार्ड, सॉइल हेल्थ कार्ड। पूरी जानकारी के लिए रिपोर्ट के 'Policy & Schemes' सेक्शन देखें।",
               'te':"ముఖ్య పథకాలు: PM-KISAN, PMFBY, కిసాన్ క్రెడిట్ కార్డ్, సాయిల్ హెల్త్ కార్డ్. పూర్తి వివరాలకు మీ నివేదికలోని 'Policy & Schemes' విభాగం చూడండి."},
 'ask_disease_none':{'en':"Your last report didn't include a leaf photo. Upload one on the 'Get Advisory' page and I'll help diagnose it.",
                      'kn':"ನಿಮ್ಮ ಕೊನೆಯ ವರದಿಯಲ್ಲಿ ಎಲೆಯ ಫೋಟೋ ಇರಲಿಲ್ಲ. 'Get Advisory' ಪುಟದಲ್ಲಿ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ, ನಾನು ಪತ್ತೆ ಮಾಡಲು ಸಹಾಯ ಮಾಡುತ್ತೇನೆ.",
                      'ta':"உங்கள் கடைசி அறிக்கையில் இலை புகைப்படம் இல்லை. 'Get Advisory' பக்கத்தில் பதிவேற்றவும், நான் கண்டறிய உதவுவேன்.",
                      'hi':"आपकी पिछली रिपोर्ट में पत्ती की फोटो नहीं थी। 'Get Advisory' पेज पर अपलोड करें, मैं पहचानने में मदद करूंगा।",
                      'te':"మీ చివరి నివేదికలో ఆకు ఫోటో లేదు. 'Get Advisory' పేజీలో అప్‌లోడ్ చేయండి, నేను గుర్తించడంలో సహాయం చేస్తాను."},
 'ask_disease':{'en':"Your last uploaded photo showed: {disease} (severity: {severity}). Treatment: {treatment}",
                'kn':"ನಿಮ್ಮ ಕೊನೆಯ ಫೋಟೋದಲ್ಲಿ: {disease} (ತೀವ್ರತೆ: {severity}). ಚಿಕಿತ್ಸೆ: {treatment}",
                'ta':"உங்கள் கடைசி புகைப்படத்தில்: {disease} (தீவிரம்: {severity}). சிகிச்சை: {treatment}",
                'hi':"आपकी पिछली फोटो में: {disease} (गंभीरता: {severity})। उपचार: {treatment}",
                'te':"మీ చివరి ఫోటోలో: {disease} (తీవ్రత: {severity}). చికిత్స: {treatment}"},
 'ask_soil':{'en':"Your soil ({soil_type}): N {n}, P {p}, K {k}, pH {ph}. Score: {score}/100.",
             'kn':"ನಿಮ್ಮ ಮಣ್ಣು ({soil_type}): N {n}, P {p}, K {k}, pH {ph}. ಅಂಕ: {score}/100.",
             'ta':"உங்கள் மண் ({soil_type}): N {n}, P {p}, K {k}, pH {ph}. மதிப்பெண்: {score}/100.",
             'hi':"आपकी मिट्टी ({soil_type}): N {n}, P {p}, K {k}, pH {ph}। स्कोर: {score}/100।",
             'te':"మీ నేల ({soil_type}): N {n}, P {p}, K {k}, pH {ph}. స్కోరు: {score}/100."},
 'thanks':{'en':"You're welcome! 🌾 Happy farming.",'kn':"ಸ್ವಾಗತ! 🌾 ಶುಭ ಕೃಷಿ.",'ta':"வரவேற்கிறேன்! 🌾 நல்ல விவசாயம்.",'hi':"आपका स्वागत है! 🌾 शुभ खेती।",'te':"మీకు స్వాగతం! 🌾 శుభ వ్యవసాయం."},
 'fallback':{'en':"I can help with crop selection, fertiliser, weather, market prices, government schemes, and disease treatment. Try a suggestion below.",
             'kn':"ನಾನು ಬೆಳೆ, ಗೊಬ್ಬರ, ಹವಾಮಾನ, ಮಾರುಕಟ್ಟೆ ಬೆಲೆ, ಯೋಜನೆ ಮತ್ತು ರೋಗ ಚಿಕಿತ್ಸೆಯಲ್ಲಿ ಸಹಾಯ ಮಾಡಬಲ್ಲೆ.",
             'ta':"பயிர், உரம், வானிலை, சந்தை விலை, திட்டங்கள் மற்றும் நோய் சிகிச்சை பற்றி உதவ முடியும்.",
             'hi':"मैं फसल, उर्वरक, मौसम, बाजार भाव, योजनाओं और रोग उपचार में मदद कर सकता हूं।",
             'te':"నేను పంట, ఎరువులు, వాతావరణం, ధరలు, పథకాలు మరియు వ్యాధి చికిత్సలో సహాయం చేయగలను."},
}

INTENT_KEYWORDS={
    'ask_crop':['crop','grow','plant','cultivat','sow'],'ask_fert':['fertiliz','fertilis','urea','dap','manure','dose'],
    'ask_weather':['weather','rain','temperature','humidity','forecast'],'ask_market':['price','market','sell','profit','rate','mandi'],
    'ask_scheme':['scheme','subsidy','loan','government','pm-kisan','pmfby','insurance'],
    'ask_disease':['disease','pest','sick','spot','wilt','fungus','infect','leaf'],
    'ask_soil':['soil','ph','nutrient','nitrogen','phosphorus','potassium'],
    'thanks':['thank'],'greeting':['hi','hello','hey','namaste'],
}


def _detect_intent(message,chip_intent=None):
    if chip_intent: return chip_intent
    msg=(message or '').lower().strip()
    if not msg: return 'greeting'
    for intent,kws in INTENT_KEYWORDS.items():
        if any(kw in msg for kw in kws): return intent
    return 'fallback'


def _tpl(key,lang):
    e=TEMPLATES.get(key,{});lang=i18n.norm_lang(lang);return e.get(lang,e.get('en',''))


class ChatbotAgent:
    def run(self,message,lang='en',chip_intent=None,user_name='',last_advisory=None):
        lang=i18n.norm_lang(lang)
        intent=_detect_intent(message,chip_intent)

        if intent=='greeting':
            return {'reply':_tpl('greeting',lang).format(name=user_name or ''),'intent':intent}
        if intent=='thanks':
            return {'reply':_tpl('thanks',lang),'intent':intent}

        report=(last_advisory or {}).get('report') if last_advisory else None
        if intent in ('ask_crop','ask_fert','ask_weather','ask_market','ask_disease','ask_soil') and not report:
            return {'reply':_tpl('no_history',lang),'intent':intent}

        secs=(report or {}).get('sections',{})
        loc=(report or {}).get('location','your area')

        if intent=='ask_crop':
            c=secs.get('crop_recommendation',{});all3=c.get('all_crops',[])
            if not all3: return {'reply':_tpl('no_history',lang),'intent':intent}
            top=all3[0];conf=round(top['confidence']*100 if top['confidence']<=1 else top['confidence'])
            others=', '.join(i18n.crop_name(x['crop'],lang) for x in all3[1:])
            reply=_tpl('ask_crop',lang).format(crop=i18n.crop_name(top['crop'],lang),conf=conf,loc=loc,others=others or '-')
            return {'reply':reply,'intent':intent}

        if intent=='ask_fert':
            s=secs.get('soil_health',{});c=secs.get('crop_recommendation',{})
            plan='; '.join(s.get('amendments',[])) or '-'
            reply=_tpl('ask_fert',lang).format(crop=i18n.crop_name(c.get('top_crop',''),lang),plan=plan)
            return {'reply':reply,'intent':intent}

        if intent=='ask_weather':
            w=secs.get('weather_analysis',{})
            reply=_tpl('ask_weather',lang).format(loc=loc,temp=w.get('temperature','-'),hum=w.get('humidity','-'),
                                                    rain=w.get('rainfall_mm','-'),advisory=(w.get('advisory') or [''])[0])
            return {'reply':reply,'intent':intent}

        if intent=='ask_market':
            m=secs.get('market_intelligence',{})
            reply=_tpl('ask_market',lang).format(crop=m.get('crop','').capitalize() or '-',
                        price=str(m.get('avg_price','-')).replace('₹','').split('/')[0],
                        trend=m.get('price_trend','-'),area=(report or {}).get('farmer_input',{}).get('land_area','-'),
                        income=str(m.get('net_income','-')).replace('₹',''))
            return {'reply':reply,'intent':intent}

        if intent=='ask_scheme':
            return {'reply':_tpl('ask_scheme',lang),'intent':intent}

        if intent=='ask_disease':
            d=secs.get('disease_detection',{})
            if not d or d.get('status')=='No image submitted' or not d.get('disease'):
                return {'reply':_tpl('ask_disease_none',lang),'intent':intent}
            reply=_tpl('ask_disease',lang).format(disease=d.get('disease','-'),severity=d.get('severity','-'),
                        treatment='; '.join(d.get('treatment',[])) or '-')
            return {'reply':reply,'intent':intent}

        if intent=='ask_soil':
            s=secs.get('soil_health',{})
            reply=_tpl('ask_soil',lang).format(soil_type=s.get('soil_type','-'),n=s.get('nitrogen_status','-'),
                        p=s.get('phosphorus_status','-'),k=s.get('potassium_status','-'),ph=s.get('ph','-'),score=s.get('health_score','-'))
            return {'reply':reply,'intent':intent}

        # fallback -> optional Gemini, else canned fallback
        llm_reply=self._try_llm(message,report,lang) if message else None
        return {'reply':llm_reply or _tpl('fallback',lang),'intent':'fallback'}

    def _try_llm(self,message,report,lang):
        if not GEMINI_API_KEY: return None
        try:
            import requests
            ctx=''
            if report:
                c=report.get('sections',{}).get('crop_recommendation',{})
                ctx=f"Farmer's location: {report.get('location')}. Last recommended crop: {c.get('top_crop')}."
            prompt=(f"You are a helpful agricultural advisory assistant. Answer in language code '{lang}'. "
                    f"Be concise (under 80 words), practical, and safe (no unverified pesticide dosages). "
                    f"Context: {ctx}\nFarmer's question: {message}")
            resp=requests.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent',
                                params={'key':GEMINI_API_KEY},json={'contents':[{'parts':[{'text':prompt}]}]},timeout=8)
            resp.raise_for_status();data=resp.json()
            return data['candidates'][0]['content']['parts'][0]['text'].strip()
        except Exception:
            return None

    def get_chips(self,lang='en'):
        lang=i18n.norm_lang(lang)
        return [{'intent':c['intent'],'label':c.get(lang,c['en'])} for c in CHIPS]
