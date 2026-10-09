from utils.logger import get_logger
import i18n
logger=get_logger(__name__)
NR={'N':{'lo':30,'ol':50,'oh':80,'hi':100},'P':{'lo':20,'ol':35,'oh':60,'hi':80},'K':{'lo':15,'ol':30,'oh':55,'hi':70},'ph':{'lo':5,'ol':6,'oh':7,'hi':8}}
def _cls(v,r):
    if v<r['lo']: return 'Very Low'
    if v<r['ol']: return 'Low'
    if v<=r['oh']: return 'Optimal'
    if v<=r['hi']: return 'High'
    return 'Very High'
def _score(v,r): return 100 if r['ol']<=v<=r['oh'] else max(0,100-abs(v-r['ol'])*2 if v<r['ol'] else 100-abs(v-r['oh'])*2)
class SoilHealthAgent:
    def assess(self,soil,recommended_crop='general',lang='en'):
        N=float(soil.get('N',50));P=float(soil.get('P',40));K=float(soil.get('K',30));ph=float(soil.get('ph',6.5));st=soil.get('soil_type','loamy').lower()
        ns={'N':{'value':N,'status':_cls(N,NR['N'])},'P':{'value':P,'status':_cls(P,NR['P'])},'K':{'value':K,'status':_cls(K,NR['K'])},'pH':{'value':ph,'status':_cls(ph,NR['ph'])}}
        fp=[]
        if 'Low' in ns['N']['status']: fp.append(i18n.soil_phrase_n_low(lang))
        if 'High' in ns['N']['status']: fp.append(i18n.soil_phrase_n_high(lang))
        if 'Low' in ns['P']['status']: fp.append(i18n.soil_phrase_p_low(lang))
        if 'High' in ns['P']['status']: fp.append(i18n.soil_phrase_p_high(lang))
        if 'Low' in ns['K']['status']: fp.append(i18n.soil_phrase_k_low(lang))
        if ph<6: fp.append(i18n.soil_phrase_ph_acidic(lang))
        elif ph>7: fp.append(i18n.soil_phrase_ph_alkaline(lang))
        else: fp.append(i18n.soil_phrase_ph_optimal(lang))
        if not fp: fp.append(i18n.soil_phrase_balanced(lang))
        hs=round((_score(N,NR['N'])+_score(P,NR['P'])+_score(K,NR['K'])+_score(ph,NR['ph']))/4)
        health_label='Excellent' if hs>=80 else 'Good' if hs>=60 else 'Fair' if hs>=40 else 'Poor'
        return{'nutrient_status':ns,'soil_type':st.capitalize(),'fertiliser_plan':fp,'amendments':fp,'health_score':hs,
               'overall_health':i18n.status(health_label,lang),
               'nitrogen':N,'nitrogen_status':i18n.status(ns['N']['status'],lang),
               'phosphorus':P,'phosphorus_status':i18n.status(ns['P']['status'],lang),
               'potassium':K,'potassium_status':i18n.status(ns['K']['status'],lang),
               'ph':ph,'ph_status':i18n.status(ns['pH']['status'],lang)}
