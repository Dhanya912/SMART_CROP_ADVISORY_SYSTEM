import os,csv
from utils.logger import get_logger
import i18n
logger=get_logger(__name__)

# Fallback (used only if the CSVs are missing)
NATIONAL=[{'name':'PM-KISAN','benefit':'₹6,000/year in 3 instalments to bank account.','eligibility':'All small and marginal farmers.','category':'Income Support'},{'name':'PMFBY (Fasal Bima)','benefit':'Crop insurance at 2% premium for Kharif crops.','eligibility':'All farmers growing notified crops.','category':'Insurance'},{'name':'Kisan Credit Card','benefit':'Up to ₹3 lakh credit at 4% interest per annum.','eligibility':'All farmers, share croppers, tenant farmers.','category':'Credit'}]
STATE={'karnataka':[{'name':'Raitha Siri','benefit':'Input subsidy: certified seeds and bio-fertilisers.','category':'Input Subsidy'}],'tamil_nadu':[{'name':'TNAU Advisory','benefit':'Free expert advisory from Tamil Nadu Agricultural University.','category':'Advisory'}]}
MSP_FALLBACK={'rice':2183,'wheat':2275,'maize':2090,'chickpea':5440,'lentil':6425,'sugarcane':340,'cotton':7121}

SCHEMES_CSV=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data','government_schemes.csv')
MSP_CSV=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data','government_msp.csv')


def _load_schemes():
    if not os.path.exists(SCHEMES_CSV): return NATIONAL,STATE
    try:
        national,state=[],{}
        with open(SCHEMES_CSV,newline='',encoding='utf-8') as f:
            for r in csv.DictReader(f):
                item={'name':r.get('scheme_name','').strip(),'benefit':r.get('benefit','').strip(),
                      'category':r.get('category','').strip(),'website':r.get('website','').strip(),
                      'helpline':r.get('helpline','').strip()}
                states=(r.get('applicable_states') or 'All').strip()
                if states.lower()=='all':
                    national.append(item)
                else:
                    for s in [x.strip().lower().replace(' ','_') for x in states.split(';') if x.strip()]:
                        state.setdefault(s,[]).append(item)
        logger.info(f"PolicyAgent: loaded {len(national)} national + {sum(len(v) for v in state.values())} state scheme rows from government_schemes.csv")
        return national or NATIONAL, state or STATE
    except Exception as e:
        logger.warning(f"government_schemes.csv load failed: {e}");return NATIONAL,STATE


def _load_msp():
    if not os.path.exists(MSP_CSV): return MSP_FALLBACK,{}
    try:
        latest={};meta={}
        with open(MSP_CSV,newline='',encoding='utf-8') as f:
            for r in csv.DictReader(f):
                crop=r.get('crop','').strip().lower().split(' (')[0]
                try: val=float(r['msp_per_quintal_inr'])
                except (KeyError,ValueError): continue
                latest[crop]=val;meta[crop]=r.get('year','2024-25')
        logger.info(f"PolicyAgent: loaded MSP for {len(latest)} crops from government_msp.csv")
        return latest or MSP_FALLBACK, meta
    except Exception as e:
        logger.warning(f"government_msp.csv load failed: {e}");return MSP_FALLBACK,{}

_NATIONAL,_STATE=_load_schemes()
_MSP,_MSP_YEAR=_load_msp()


class PolicyAdvisoryAgent:
    def get_schemes(self,crop,state,lang='en'):
        sk=state.lower().replace(' ','_');ss=_STATE.get(sk,[])
        msp_val=_MSP.get(crop.lower())
        year=_MSP_YEAR.get(crop.lower(),'2024-25')
        msp_info={'crop':crop,'msp':msp_val,'year':year,'unit':'₹/quintal',
                  'note':f'Government guarantees ₹{msp_val}/quintal for {crop}.' if msp_val else f'MSP not announced for {crop}.'}
        contacts=[{'name':'Kisan Call Centre','contact':'1800-180-1551','type':'Toll-Free'},{'name':'PM-KISAN Helpline','contact':'155261','type':'Income Support'},{'name':'PMFBY Helpline','contact':'1800-200-7710','type':'Crop Insurance'},{'name':'NABARD','contact':'1800-22-0109','type':'Credit'}]
        return{'crop':crop,'state':state,'national_schemes':_NATIONAL,'state_schemes':ss,'msp_info':msp_info,
               'key_contacts':contacts,'advisory':i18n.policy_advisory_lines(lang)}
