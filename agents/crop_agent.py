import numpy as np,joblib,os
from utils.logger import get_logger
import i18n
logger=get_logger(__name__)
CROPS=['rice','maize','chickpea','kidneybeans','pigeonpeas','mothbeans','mungbean','blackgram','lentil','pomegranate','banana','mango','grapes','watermelon','muskmelon','apple','orange','papaya','coconut','cotton','jute','coffee']
CROP_DESC={'rice':'Staple cereal; thrives in warm wet conditions.','maize':'Versatile cereal; good for warm moderately dry climates.','cotton':'Cash crop; prefers black soil with good drainage.','chickpea':'Legume that fixes nitrogen; grows in semi-arid regions.','banana':'Tropical fruit; needs deep fertile well-drained soil.','coffee':'Shade-loving crop; ideal for hilly red laterite soils.','coconut':'Tropical palm; thrives in coastal sandy soils.','mango':'Tropical fruit tree; heat-tolerant and drought-resistant.','lentil':'High-protein legume; tolerates poor soils.'}
DATA_CSV=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data','crop_recommendation.csv')

def _build(path):
    if os.path.exists(path): return joblib.load(path)
    from sklearn.ensemble import RandomForestClassifier
    m=RandomForestClassifier(n_estimators=200,random_state=42,n_jobs=-1,min_samples_leaf=2)
    if os.path.exists(DATA_CSV):
        # Train on the real crop_recommendation.csv dataset (2,200 rows, 22 crops)
        import csv
        rows=[]
        with open(DATA_CSV,newline='',encoding='utf-8') as f:
            for r in csv.DictReader(f): rows.append(r)
        label_to_idx={c:i for i,c in enumerate(CROPS)}
        X,y=[],[]
        for r in rows:
            lbl=r.get('label','').strip().lower()
            if lbl not in label_to_idx: continue
            try:
                X.append([float(r['N']),float(r['P']),float(r['K']),float(r['temperature']),float(r['humidity']),float(r['ph']),float(r['rainfall'])])
                y.append(label_to_idx[lbl])
            except (KeyError,ValueError): continue
        if len(X)>=100:
            m.fit(np.array(X),np.array(y))
            os.makedirs(os.path.dirname(path),exist_ok=True);joblib.dump(m,path)
            logger.info(f"CropAgent: trained Random Forest on {len(X)} real rows from crop_recommendation.csv")
            return m
    # Fallback: synthetic data if dataset CSV is unavailable
    from sklearn.datasets import make_classification
    np.random.seed(42)
    X,y=make_classification(n_samples=2200,n_features=7,n_classes=22,n_informative=7,n_redundant=0,random_state=42)
    X[:,0]=X[:,0]*40+50;X[:,1]=X[:,1]*30+40;X[:,2]=X[:,2]*30+30
    X[:,3]=X[:,3]*8+22;X[:,4]=X[:,4]*20+60;X[:,5]=X[:,5]*1+6.5;X[:,6]=X[:,6]*80+100
    m.fit(X,y)
    os.makedirs(os.path.dirname(path),exist_ok=True);joblib.dump(m,path)
    logger.warning("CropAgent: crop_recommendation.csv not found — trained on synthetic fallback data.")
    return m

class CropRecommendationAgent:
    def __init__(self): self.model=_build('models/crop_rf.pkl');logger.info("CropAgent ready.")
    def recommend(self,soil,weather=None,lang='en'):
        temp=(weather or {}).get('temperature',soil.get('temperature',25))
        hum=(weather or {}).get('humidity',soil.get('humidity',60))
        feat=np.array([[float(soil.get('N',50)),float(soil.get('P',40)),float(soil.get('K',30)),float(temp),float(hum),float(soil.get('ph',6.5)),float(soil.get('rainfall',100))]])
        proba=self.model.predict_proba(feat)[0];top3idx=np.argsort(proba)[::-1][:3]
        top3=[{'crop':CROPS[i%len(CROPS)],'crop_display':i18n.crop_name(CROPS[i%len(CROPS)],lang),'confidence':round(float(proba[i])*100,1),'description':CROP_DESC.get(CROPS[i%len(CROPS)],'Adaptable crop.')} for i in top3idx]
        fi={n:round(float(v)*100,1) for n,v in zip(['Nitrogen','Phosphorus','Potassium','Temperature','Humidity','pH','Rainfall'],self.model.feature_importances_)}
        return{'top_crop':top3[0]['crop'],'top_crop_display':top3[0]['crop_display'],'top3':top3,'all_crops':[{'crop':c['crop'],'crop_display':c['crop_display'],'confidence':c['confidence']/100} for c in top3],'feature_importance':fi}
