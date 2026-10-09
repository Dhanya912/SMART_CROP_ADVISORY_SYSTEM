import os,requests,random,csv
from utils.logger import get_logger
import i18n
logger=get_logger(__name__)
API_KEY=os.environ.get('OPENWEATHER_API_KEY','')
DATA_CSV=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data','weather_advisory.csv')

def _load_dataset():
    """Loads weather_advisory.csv once, grouped by state, so the offline
    fallback can return climate-realistic values for the farmer's region
    instead of pure random noise."""
    rows=[]
    if os.path.exists(DATA_CSV):
        try:
            with open(DATA_CSV,newline='',encoding='utf-8') as f:
                for r in csv.DictReader(f): rows.append(r)
        except Exception as e:
            logger.warning(f"weather_advisory.csv load failed: {e}")
    return rows

_DATASET=_load_dataset()

def _dataset_fallback(loc):
    """Pick a dataset row matching the farmer's state/city if possible,
    else a deterministic-but-plausible seeded pseudo-reading."""
    if _DATASET:
        loc_l=loc.lower()
        matches=[r for r in _DATASET if r.get('state','').lower() in loc_l or r.get('city','').lower() in loc_l]
        pool=matches or _DATASET
        import hashlib
        seed=int(hashlib.md5(loc.encode()).hexdigest(),16)%len(pool)
        r=pool[seed]
        try:
            return{'location':loc,'temperature':float(r['temperature_c']),'humidity':float(r['humidity_pct']),
                   'wind_speed':float(r['wind_speed_kmh']),'rainfall_mm':float(r['rainfall_mm']),
                   'uv_index':float(r.get('uv_index',5)),'description':'Dataset-grounded estimate','source':'dataset'}
        except (KeyError,ValueError):
            pass
    import hashlib;seed=int(hashlib.md5(loc.encode()).hexdigest(),16)%1000;random.seed(seed)
    return{'location':loc,'temperature':round(random.uniform(22,35),1),'humidity':round(random.uniform(45,85),1),'wind_speed':round(random.uniform(1,12),1),'rainfall_mm':round(random.uniform(0,20),1),'uv_index':round(random.uniform(3,10),1),'description':'Estimated (no live data)','source':'mock'}

class WeatherAnalysisAgent:
    def analyze(self,loc,lang='en'):
        w=self._fetch(loc);w['advisory']=self._advise(w,lang);return w
    def _fetch(self,loc):
        if not API_KEY: return _dataset_fallback(loc)
        try:
            r=requests.get('https://api.openweathermap.org/data/2.5/weather',params={'q':loc,'appid':API_KEY,'units':'metric'},timeout=8);r.raise_for_status();d=r.json()
            return{'location':d.get('name',loc),'temperature':d['main']['temp'],'humidity':d['main']['humidity'],'wind_speed':d['wind']['speed'],'rainfall_mm':d.get('rain',{}).get('1h',0),'uv_index':None,'description':d['weather'][0]['description'].capitalize(),'source':'openweathermap'}
        except Exception as e:
            logger.info(f"Live weather fetch failed ({e}); using dataset-grounded fallback.")
            return _dataset_fallback(loc)
    def _advise(self,w,lang='en'):
        a=[];t=w.get('temperature',25);h=w.get('humidity',60);wn=w.get('wind_speed',5);r=w.get('rainfall_mm',0)
        if t>35: a.append(i18n.weather_phrase('high_heat',lang))
        elif t<15: a.append(i18n.weather_phrase('cool',lang))
        else: a.append(i18n.weather_phrase('optimal_temp',lang))
        if h>80: a.append(i18n.weather_phrase('high_humidity',lang))
        elif h<40: a.append(i18n.weather_phrase('low_humidity',lang))
        if r>15: a.append(i18n.weather_phrase('heavy_rain',lang))
        elif r==0 and t>28: a.append(i18n.weather_phrase('no_rain_heat',lang))
        if wn>10: a.append(i18n.weather_phrase('strong_wind',lang))
        return a
