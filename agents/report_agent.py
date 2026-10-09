import time
from utils.logger import get_logger
import i18n
logger=get_logger(__name__)

REPORT_LABEL_KEYS=['report_title','prepared_for','location','generated_on','executive_summary','sec_crop','sec_disease',
 'sec_weather','sec_soil','sec_market','sec_policy','sec_action_plan','recommended_crop','confidence_scores','method',
 'key_influencing_factors','disease','severity','confidence','cause','treatment_steps','prevention','no_image_msg',
 'no_disease_detected','condition','temperature','humidity','wind_speed','rainfall','irrigation_need','farm_advisories',
 'source','live','demo','score','nitrogen','phosphorus','potassium','ph','soil_type','fertiliser_plan','crop','avg_price',
 'price_trend','best_market','yield_estimate','net_income','market_advisory','applicable_schemes','benefit','helpline',
 'toll_free','priority','timeline','immediately','this_week','before_sowing','this_month','footer_note']


class ReportGenerationAgent:
    def generate(self,ctx,language='en'):
        lang=i18n.norm_lang(language)
        fi=ctx.get('farmer_input',{});crop=ctx.get('crop_recommendation',{});dis=ctx.get('disease_detection',{})
        wx=ctx.get('weather',{});soil=ctx.get('soil_health',{});mkt=ctx.get('market',{});pol=ctx.get('policy',{})
        loc=fi.get('location','N/A');top=crop.get('top_crop','unknown')
        top_display=crop.get('top_crop_display') or i18n.crop_name(top,lang)
        top3=crop.get('all_crops',[])
        sc=soil.get('health_score',0);pr=mkt.get('price_per_unit',{});inc=mkt.get('income_estimate',{});msp=pol.get('msp_info',{})
        conf_disp=f"{top3[0]['confidence']*100:.0f}" if top3 and top3[0]['confidence']<=1 else f"{top3[0]['confidence']:.0f}" if top3 else '0'

        crop_sec={'title':i18n.t('sec_crop',lang),'top_crop':top_display,'top_crop_key':top,
                  'all_crops':[{'crop':c['crop'],'crop_display':c.get('crop_display') or i18n.crop_name(c['crop'],lang),'confidence':c['confidence']} for c in top3],
                  'method':'Random Forest Classifier (scikit-learn)','feature_importance':crop.get('feature_importance',{}),
                  'key_insight':i18n.crop_key_insight(lang,top_display,conf_disp)}

        if dis:
            healthy=dis.get('severity_raw','')=='None' or dis.get('status')=='healthy'
            dis_sec={'title':i18n.t('sec_disease',lang),'disease':dis.get('disease_name','N/A'),'severity':dis.get('severity','Unknown'),
                     'confidence':f"{dis.get('confidence',0)}%",'cause':dis.get('cause','—'),'treatment':dis.get('treatment',[]),
                     'prevention':dis.get('prevention',''),'status':dis.get('status','unknown'),
                     'confidence_pct':dis.get('confidence',0),'top3':dis.get('top3',[]),
                     'image_features':dis.get('image_features',{}),'crop_used':dis.get('crop_used','auto-detect'),
                     'key_insight':i18n.disease_summary_line(lang,healthy,dis.get('disease_name'))}
        else:
            dis_sec={'title':i18n.t('sec_disease',lang),'status':'No image submitted','key_insight':i18n.t('no_image_msg',lang)}

        wx_sec={'title':i18n.t('sec_weather',lang),'temperature':f"{wx.get('temperature','—')}°C",'humidity':f"{wx.get('humidity','—')}%",
                'condition':wx.get('description','—'),'wind_speed':wx.get('wind_speed',0),'rainfall_mm':wx.get('rainfall_mm',0),
                'advisory':wx.get('advisory',[]),'source':wx.get('source','mock'),
                'irrigation':{'net_irrigation':max(0,round(5-wx.get('rainfall_mm',0),1))},
                'key_insight':(wx.get('advisory') or [''])[0]}

        soil_sec={'title':i18n.t('sec_soil',lang),'health_score':sc,'overall_health':soil.get('overall_health','—'),
                  'nitrogen':soil.get('nitrogen'),'nitrogen_status':soil.get('nitrogen_status'),
                  'phosphorus':soil.get('phosphorus'),'phosphorus_status':soil.get('phosphorus_status'),
                  'potassium':soil.get('potassium'),'potassium_status':soil.get('potassium_status'),
                  'ph':soil.get('ph'),'ph_status':soil.get('ph_status'),'amendments':soil.get('amendments',[]),
                  'soil_type':soil.get('soil_type','Loamy'),'key_insight':i18n.soil_key_insight(lang,sc)}

        mkt_adv=mkt.get('advisory',[])
        mkt_sec={'title':i18n.t('sec_market',lang),'crop':mkt.get('crop_display') or top_display,'avg_price':f"₹{pr.get('avg',0)}/{pr.get('unit','quintal')}",
                 'price_trend':mkt.get('trend','Stable'),'best_market':(mkt.get('nearby_markets') or ['APMC'])[0],
                 'yield_estimate':f"{inc.get('yield_units',0)} quintals/ha",'net_income':f"₹{inc.get('net_income',0):,}",
                 'advisory':mkt_adv,'key_insight':mkt_adv[0] if mkt_adv else ''}

        all_sch=pol.get('national_schemes',[])+pol.get('state_schemes',[])
        pol_sec={'title':i18n.t('sec_policy',lang),'msp':{'msp':msp.get('msp'),'year':msp.get('year','2024-25'),'unit':msp.get('unit','₹/quintal')},
                 'schemes':[{'name':s['name'],'benefit':s['benefit'],'category':s.get('category','')} for s in all_sch[:6]],
                 'key_insight':i18n.policy_key_insight(lang),'helpline':'1800-180-1551 (Kisan Call Centre — Free)'}

        disease_line=dis_sec.get('key_insight','') if dis else i18n.disease_summary_line(lang,True)
        summary=i18n.executive_summary(lang,loc,top_display,sc,disease_line,f"₹{pr.get('avg',0)}/{pr.get('unit','quintal')}",f"₹{inc.get('net_income',0):,}")

        plan=[];p=1
        if dis and dis.get('severity_raw') in ('High','Very High'):
            plan.append({'priority':p,'action':(dis.get('treatment') or ['Consult agronomist.'])[0],'timeline':i18n.t('immediately',lang)});p+=1
        for adv in (wx.get('advisory') or [])[:1]:
            plan.append({'priority':p,'action':adv,'timeline':i18n.t('this_week',lang)});p+=1
        for fert in (soil.get('amendments') or [])[:2]:
            plan.append({'priority':p,'action':fert,'timeline':i18n.t('before_sowing',lang)});p+=1
        plan.append({'priority':p,'action':i18n.policy_key_insight(lang),'timeline':i18n.t('this_month',lang)})

        labels={k:i18n.t(k,lang) for k in REPORT_LABEL_KEYS}

        return{'title':i18n.t('report_title',lang),'location':loc,'generated_at':time.strftime('%d %b %Y, %H:%M'),
               'lang':lang,'labels':labels,'farmer_input':fi,
               'sections':{'crop_recommendation':crop_sec,'disease_detection':dis_sec,'weather_analysis':wx_sec,
                           'soil_health':soil_sec,'market_intelligence':mkt_sec,'policy_advisory':pol_sec},
               'action_plan':plan,'executive_summary':summary}
