import random,os,csv,statistics
from collections import defaultdict
from utils.logger import get_logger
import i18n
logger=get_logger(__name__)

# Fallback baseline (used only for crops absent from the dataset)
PRICES={'rice':(1800,2200),'maize':(1400,1800),'cotton':(5500,7000),'sugarcane':(290,350),'wheat':(2000,2400),'chickpea':(4800,5800),'tomato':(500,3000),'banana':(800,1500),'mango':(2000,5000),'coconut':(1200,2800),'coffee':(7500,12500),'lentil':(5000,7000),'blackgram':(5200,7200),'soybean':(4500,5500),'groundnut':(5500,7200),'potato':(600,1800)}
YIELD={'rice':50,'maize':55,'cotton':20,'sugarcane':700,'wheat':40,'chickpea':12,'tomato':200,'banana':300,'mango':80,'coconut':8000,'coffee':10,'lentil':10,'general':30}
MKTS={'karnataka':['APMC Mysuru','APMC Bangalore','APMC Hubli'],'tamil nadu':['Koyambedu Chennai','APMC Coimbatore'],'maharashtra':['APMC Pune','Lasalgaon Nashik'],'andhra pradesh':['APMC Guntur','APMC Kurnool']}
DATA_CSV=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data','market_prices.csv')


def _load_dataset():
    """Builds per-crop (min/avg/max) price stats and per-state mandi lists
    from market_prices.csv (3,000 real-format rows) so figures reflect the
    provided dataset instead of a small hardcoded table."""
    by_crop=defaultdict(list);by_state_mandi=defaultdict(set)
    if not os.path.exists(DATA_CSV): return {},{}
    try:
        with open(DATA_CSV,newline='',encoding='utf-8') as f:
            for r in csv.DictReader(f):
                crop=r.get('crop','').strip().lower()
                try: avg=float(r['avg_price'])
                except (KeyError,ValueError): continue
                by_crop[crop].append(avg)
                state=r.get('state','').strip().lower();mandi=r.get('mandi','').strip()
                if state and mandi: by_state_mandi[state].add(mandi)
    except Exception as e:
        logger.warning(f"market_prices.csv load failed: {e}")
        return {},{}
    stats={c:{'min':round(min(v)),'avg':round(statistics.mean(v)),'max':round(max(v))} for c,v in by_crop.items()}
    mandis={s:sorted(list(m))[:4] for s,m in by_state_mandi.items()}
    logger.info(f"MarketAgent: loaded price stats for {len(stats)} crops from market_prices.csv")
    return stats,mandis

_STATS,_MANDIS=_load_dataset()


class MarketIntelligenceAgent:
    def analyze(self,crop,location,land_area_ha=1.0,lang='en'):
        ck=crop.lower().strip()
        if ck in _STATS:
            s=_STATS[ck];lo,hi,avg=s['min'],s['max'],s['avg']
        else:
            lo,hi=PRICES.get(ck,(2000,4000));avg=round(random.uniform(lo,hi)*(1+random.uniform(-0.03,0.03)))
        trend_key={'tomato':'Rising','mango':'Seasonal','maize':'Rising','coffee':'Rising'}.get(ck,'Stable')
        yu=YIELD.get(ck,YIELD['general']);ty=yu*land_area_ha;gi=ty*avg;ni=gi*0.70
        state=location.split(',')[-1].strip().lower()
        mkts=_MANDIS.get(state) or next((v for k,v in MKTS.items() if k in state),['Local APMC'])
        adv=[]
        if trend_key=='Rising': adv.append(i18n.market_phrase_rising(lang))
        elif trend_key=='Volatile': adv.append(i18n.market_phrase_volatile(lang))
        else: adv.append(i18n.market_phrase_stable(lang))
        adv.append(i18n.market_phrase_income(lang,round(ni)))
        return{'crop':ck,'crop_display':i18n.crop_name(ck,lang),'price_per_unit':{'min':round(lo),'max':round(hi),'avg':avg,'unit':'quintal','trend':trend_key},
               'trend':i18n.status(trend_key,lang),
               'income_estimate':{'area_ha':land_area_ha,'yield_units':round(ty,1),'price_per_unit':avg,'gross_income':round(gi),'input_cost':round(gi*0.30),'net_income':round(ni)},
               'nearby_markets':mkts,'advisory':adv}
