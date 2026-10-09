import time
from concurrent.futures import ThreadPoolExecutor,as_completed
from utils.logger import get_logger
from agents.crop_agent import CropRecommendationAgent
from agents.disease_agent import DiseaseDetectionAgent
from agents.weather_agent import WeatherAnalysisAgent
from agents.soil_agent import SoilHealthAgent
from agents.market_agent import MarketIntelligenceAgent
from agents.policy_agent import PolicyAdvisoryAgent
from agents.report_agent import ReportGenerationAgent
from agents.chatbot_agent import ChatbotAgent
import i18n
logger=get_logger(__name__)
class AgentOrchestrator:
    def __init__(self):
        logger.info("Initialising agents...")
        self.crop_agent=CropRecommendationAgent();self.disease_agent=DiseaseDetectionAgent()
        self.weather_agent=WeatherAnalysisAgent();self.soil_agent=SoilHealthAgent()
        self.market_agent=MarketIntelligenceAgent();self.policy_agent=PolicyAdvisoryAgent()
        self.report_agent=ReportGenerationAgent();self.chatbot_agent=ChatbotAgent()
        logger.info("All 8 agents ready (7 advisory + chatbot).")
    def _parallel(self,tasks):
        results={}
        with ThreadPoolExecutor(max_workers=min(len(tasks),4)) as ex:
            futs={ex.submit(fn,*a,**kw):k for k,(fn,a,kw) in tasks.items()}
            for f in as_completed(futs):
                k=futs[f]
                try: results[k]=f.result()
                except Exception as e: logger.warning(f"Agent '{k}' failed: {e}");results[k]={}
        return results
    def run(self,fi):
        t0=time.time();soil=fi['soil_params'];loc=fi['location']
        lang=i18n.norm_lang(fi.get('language','english'))
        area=float(fi.get('land_area',1.0));state=fi.get('state',loc.split(',')[-1].strip())
        s1=self._parallel({'weather':(self.weather_agent.analyze,[loc],{'lang':lang}),'market':(self.market_agent.analyze,['general',loc],{'land_area_ha':area,'lang':lang})})
        s2_t={'crop':(self.crop_agent.recommend,[soil],{'weather':s1.get('weather',{}),'lang':lang})}
        if fi.get('image_path'): s2_t['disease']=(self.disease_agent.detect,[fi['image_path']],{'lang':lang,'crop':fi.get('crop_type') or fi.get('crop') or ''})
        s2=self._parallel(s2_t)
        top=s2.get('crop',{}).get('top_crop',fi.get('crop','rice'))
        soil_res=self.soil_agent.assess(soil,recommended_crop=top,lang=lang)
        pol_res=self.policy_agent.get_schemes(top,state,lang=lang)
        # re-run market analysis for the ACTUAL recommended crop (first pass used 'general' for parallelism)
        market_res=self.market_agent.analyze(top,loc,land_area_ha=area,lang=lang)
        ctx={'farmer_input':fi,'weather':s1.get('weather',{}),'market':market_res,'crop_recommendation':s2.get('crop',{}),'disease_detection':s2.get('disease',None),'soil_health':soil_res,'policy':pol_res}
        report=self.report_agent.generate(ctx,language=lang)
        report['processing_time_s']=round(time.time()-t0,2)
        return report
