from flask import Flask,render_template,request,jsonify,make_response,redirect,send_file
from flask_cors import CORS
import os,json,io
from datetime import datetime
import database as db
from auth import get_current_user,login_required,login_required_page,COOKIE_NAME
from agents.orchestrator import AgentOrchestrator
from pdf_report import generate_advisory_pdf
from utils.logger import get_logger
logger=get_logger(__name__)
app=Flask(__name__);CORS(app,supports_credentials=True)
app.config['UPLOAD_FOLDER']='static/uploads'
app.config['MAX_CONTENT_LENGTH']=16*1024*1024
app.secret_key=os.environ.get('SECRET_KEY','cropai-yit-secret-2025')
os.makedirs(app.config['UPLOAD_FOLDER'],exist_ok=True);os.makedirs('data',exist_ok=True)
db.init_db();orchestrator=AgentOrchestrator()

@app.route('/')
def index():
    u=get_current_user();return redirect('/dashboard') if u else render_template('landing.html')
@app.route('/login')
def login_page(): return redirect('/dashboard') if get_current_user() else render_template('auth.html',mode='login')
@app.route('/register')
def register_page(): return redirect('/dashboard') if get_current_user() else render_template('auth.html',mode='register')
@app.route('/dashboard')
@login_required_page
def dashboard(current_user): return render_template('dashboard.html',user=current_user)
@app.route('/advisory')
@login_required_page
def advisory_page(current_user): return render_template('advisory.html',user=current_user)
@app.route('/farmer')
@login_required_page
def farmer_page(current_user): return render_template('farmer.html',user=current_user)

@app.route('/history')
@login_required_page
def history_page(current_user): return render_template('history.html',user=current_user)
@app.route('/profile')
@login_required_page
def profile_page(current_user): return render_template('profile.html',user=current_user)
@app.route('/logout')
def logout():
    token=request.cookies.get(COOKIE_NAME)
    if token: db.delete_session(token)
    resp=make_response(redirect('/login'));resp.delete_cookie(COOKIE_NAME);return resp

@app.route('/api/auth/register',methods=['POST'])
def api_register():
    d=request.get_json()
    if not d: return jsonify({'success':False,'error':'No data'}),400
    name=d.get('name','').strip();email=d.get('email','').strip();pwd=d.get('password','')
    if not name or not email or not pwd: return jsonify({'success':False,'error':'Name, email and password required.'}),400
    if len(pwd)<6: return jsonify({'success':False,'error':'Password must be at least 6 characters.'}),400
    if '@' not in email or '.' not in email.split('@')[-1] or email.count('@')!=1: return jsonify({'success':False,'error':'Enter a valid email address (e.g. name@example.com).'}),400
    try: raw_land=float(d.get('land_area',1.0))
    except (TypeError,ValueError): return jsonify({'success':False,'error':'Land area must be a number.'}),400
    unit=d.get('land_unit','hectare')
    if raw_land<=0: return jsonify({'success':False,'error':'Land area must be greater than zero.'}),400
    land_ha=to_hectares(raw_land,unit)
    if land_ha>10000: return jsonify({'success':False,'error':'Land area looks too large. Please check the value and unit.'}),400
    if land_ha<=0: return jsonify({'success':False,'error':'Land area is too small to record.'}),400
    result=db.create_user(name=name,email=email,password=pwd,phone=d.get('phone',''),state=d.get('state',''),district=d.get('district',''),land_area=land_ha,soil_type=d.get('soil_type','loamy'))
    if not result['ok']: return jsonify({'success':False,'error':result['error']}),409
    user=result['user'];token=db.create_session(user['id'])
    resp=make_response(jsonify({'success':True,'redirect':'/dashboard','user':_safe(user)}))
    resp.set_cookie(COOKIE_NAME,token,httponly=True,samesite='Lax',max_age=7*86400);return resp

@app.route('/api/auth/login',methods=['POST'])
def api_login():
    d=request.get_json()
    if not d: return jsonify({'success':False,'error':'No data'}),400
    email=d.get('email','').strip().lower();pwd=d.get('password','')
    user=db.get_user_by_email(email)
    if not user or not db.verify_password(pwd,user['password_hash']): return jsonify({'success':False,'error':'Invalid email or password.'}),401
    db.update_last_login(user['id']);token=db.create_session(user['id'])
    resp=make_response(jsonify({'success':True,'redirect':'/dashboard','user':_safe(user)}))
    resp.set_cookie(COOKIE_NAME,token,httponly=True,samesite='Lax',max_age=7*86400);return resp

@app.route('/api/auth/me')
def api_me():
    user=get_current_user()
    if not user: return jsonify({'success':False,'authenticated':False}),401
    return jsonify({'success':True,'authenticated':True,'user':_safe(user)})

@app.route('/api/auth/profile',methods=['PUT'])
@login_required
def api_update_profile(current_user):
    d=request.get_json();db.update_user_profile(current_user['id'],d)
    updated=db.get_user_by_id(current_user['id']);return jsonify({'success':True,'user':_safe(updated)})

@app.route('/api/full-advisory',methods=['POST'])
@login_required
def full_advisory(current_user):
    try:
        data=request.form.to_dict();image_path=None
        if 'image' in request.files:
            f=request.files['image']
            if f and f.filename:
                fname=f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{f.filename}"
                image_path=os.path.join(app.config['UPLOAD_FOLDER'],fname);f.save(image_path)
        soil={'N':float(data.get('nitrogen',80)),'P':float(data.get('phosphorus',40)),'K':float(data.get('potassium',60)),'ph':float(data.get('ph',6.5)),'temperature':float(data.get('temperature',26)),'humidity':float(data.get('humidity',70)),'rainfall':float(data.get('rainfall',150)),'soil_type':data.get('soil_type','loamy')}
        fi={'location':data.get('location',f"{current_user.get('district','Mysuru')}, {current_user.get('state','Karnataka')}"),'state':data.get('state',current_user.get('state','Karnataka')),'land_area':float(data.get('area',current_user.get('land_area',1.0))),'primary_concern':data.get('primary_concern','crop selection'),'language':data.get('language','english'),'crop':data.get('crop',''),'crop_type':data.get('leaf_crop',''),'soil_params':soil,'image_path':image_path}
        report=orchestrator.run(fi);aid=db.save_advisory(current_user['id'],fi,report)
        report['advisory_id']=aid;return jsonify({'success':True,'data':report})
    except Exception as e: logger.error(f"Advisory error: {e}",exc_info=True);return jsonify({'success':False,'error':str(e)}),500

@app.route('/api/download-pdf/<int:advisory_id>')
@login_required
def download_pdf(advisory_id,current_user):
    detail=db.get_advisory_detail(advisory_id,current_user['id'])
    if not detail: return jsonify({'success':False,'error':'Not found'}),404
    report=detail.get('report') or {}
    if not report:
        try: report=json.loads(detail.get('report_json','{}'))
        except: return jsonify({'success':False,'error':'Report data unavailable'}),400
    if 'location' not in report: report['location']=detail.get('location','N/A')
    if 'generated_at' not in report: report['generated_at']=(detail.get('created_at','') or '')[:16]
    pdf=generate_advisory_pdf(report,farmer_name=current_user['name'])
    fname=f"CropAI_Advisory_{advisory_id}_{current_user['name'].replace(' ','_')}.pdf"
    return send_file(io.BytesIO(pdf),mimetype='application/pdf',as_attachment=True,download_name=fname)

@app.route('/api/download-latest-pdf',methods=['POST'])
@login_required
def download_latest_pdf(current_user):
    try:
        data=request.get_json();report=data.get('report',{})
        if not report: return jsonify({'success':False,'error':'No report data'}),400
        pdf=generate_advisory_pdf(report,farmer_name=current_user['name'])
        fname=f"CropAI_Advisory_{current_user['name'].replace(' ','_')}.pdf"
        return send_file(io.BytesIO(pdf),mimetype='application/pdf',as_attachment=True,download_name=fname)
    except Exception as e: return jsonify({'success':False,'error':str(e)}),500

@app.route('/api/recommend-crop',methods=['POST'])
@login_required
def recommend_crop(current_user):
    try:
        d=request.get_json()
        alias={'N':'nitrogen','P':'phosphorus','K':'potassium'}
        def pick(k,dv):
            v=d.get(k,d.get(alias.get(k,k)))
            try: return float(v) if v not in (None,'') else dv
            except (TypeError,ValueError): return dv
        soil={k:pick(k,v) for k,v in [('N',80),('P',40),('K',60),('ph',6.5),('temperature',26),('humidity',70),('rainfall',150)]}
        raw=orchestrator.crop_agent.recommend(soil);top3=raw.get('top3',[])
        return jsonify({'success':True,'data':{'top_crop':raw.get('top_crop',''),'confidence':top3[0]['confidence']/100 if top3 else 0,'all_crops':[{'crop':c['crop'],'confidence':c['confidence']/100} for c in top3],'recommendations':[{'crop':c['crop'],'confidence':c['confidence']/100,'description':c.get('description','')} for c in top3],'feature_importance':raw.get('feature_importance',{}),'method':'Random Forest Classifier (scikit-learn)'}})
    except Exception as e: return jsonify({'success':False,'error':str(e)}),500

@app.route('/api/detect-disease',methods=['POST'])
@login_required
def detect_disease(current_user):
    try:
        if 'image' not in request.files: return jsonify({'success':False,'error':'Please choose a leaf photo first.'}),400
        f=request.files['image']
        if not f or not f.filename: return jsonify({'success':False,'error':'Please choose a leaf photo first.'}),400
        if not f.filename.lower().endswith(('.jpg','.jpeg','.png','.webp','.bmp')):
            return jsonify({'success':False,'error':'Unsupported file type. Upload a JPG, PNG or WEBP photo.'}),400
        fname=f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{f.filename}"
        path=os.path.join(app.config['UPLOAD_FOLDER'],fname);f.save(path)
        crop_hint=(request.form.get('crop_type') or request.form.get('crop') or request.form.get('leaf_crop') or '').strip()
        dlang=(request.form.get('lang') or 'en').strip()
        raw=orchestrator.disease_agent.detect(path,lang=dlang,crop=crop_hint)
        if raw.get('error'): return jsonify({'success':False,'error':raw['error']}),400
        return jsonify({'success':True,'data':{'disease_name':raw.get('disease_name','Unknown'),'severity':raw.get('severity','Unknown'),'confidence':raw.get('confidence',0)/100,'status':raw.get('status','unknown'),'cause':raw.get('cause','—'),'treatment':raw.get('treatment',[]),'prevention':raw.get('prevention',''),'top3':raw.get('top3',[]),'crop_used':raw.get('crop_used','auto-detect'),'image_features':raw.get('image_features',{})}})
    except Exception as e: return jsonify({'success':False,'error':str(e)}),500

@app.route('/api/weather',methods=['POST','GET'])
@login_required
def weather(current_user):
    try:
        loc=(request.get_json() or {}).get('location') if request.method=='POST' else request.args.get('location','Mysuru')
        raw=orchestrator.weather_agent.analyze(loc or 'Mysuru')
        return jsonify({'success':True,'data':{'condition':raw.get('description',raw.get('condition','N/A')),'temperature':raw.get('temperature',25),'humidity':raw.get('humidity',60),'wind_speed':raw.get('wind_speed',5),'rainfall_mm':raw.get('rainfall_mm',0),'uv_index':raw.get('uv_index',5),'advisory':raw.get('advisory',[]),'irrigation':{'net_irrigation':max(0,round(5-raw.get('rainfall_mm',0),1))},'source':raw.get('source','mock')}})
    except Exception as e: return jsonify({'success':False,'error':str(e)}),500

@app.route('/api/soil-health',methods=['POST'])
@login_required
def soil_health(current_user):
    try:
        d=request.get_json()
        soil={'N':d.get('nitrogen',80),'P':d.get('phosphorus',40),'K':d.get('potassium',60),'ph':d.get('ph',6.5),'soil_type':d.get('soil_type','loamy')}
        raw=orchestrator.soil_agent.assess(soil,recommended_crop=d.get('crop','general'))
        return jsonify({'success':True,'data':{'health_score':raw.get('health_score',0),'overall_health':raw.get('overall_health','—'),'nitrogen':raw.get('nitrogen'),'nitrogen_status':raw.get('nitrogen_status'),'phosphorus':raw.get('phosphorus'),'phosphorus_status':raw.get('phosphorus_status'),'potassium':raw.get('potassium'),'potassium_status':raw.get('potassium_status'),'ph':raw.get('ph'),'ph_status':raw.get('ph_status'),'soil_type':raw.get('soil_type','Loamy'),'amendments':raw.get('amendments',[])}})
    except Exception as e: return jsonify({'success':False,'error':str(e)}),500

@app.route('/api/market-prices',methods=['POST'])
@login_required
def market_prices(current_user):
    try:
        d=request.get_json();raw=orchestrator.market_agent.analyze(d.get('crop','rice').lower(),d.get('location','Karnataka'),land_area_ha=float(d.get('area',1.0)))
        p=raw.get('price_per_unit',{});i=raw.get('income_estimate',{})
        return jsonify({'success':True,'data':{'crop':d.get('crop'),'avg_price_quintal':p.get('avg',0),'min_price_quintal':p.get('min',0),'max_price_quintal':p.get('max',0),'price_trend':raw.get('trend','stable').lower(),'best_market':(raw.get('nearby_markets') or ['APMC'])[0],'yield_estimate':f"{i.get('yield_units',0)} quintals/ha",'gross_income_inr':i.get('gross_income',0),'net_income_inr':i.get('net_income',0),'advisory':raw.get('advisory',[]),'nearby_markets':raw.get('nearby_markets',[])}})
    except Exception as e: return jsonify({'success':False,'error':str(e)}),500

@app.route('/api/policy',methods=['POST','GET'])
@login_required
def policy_route(current_user):
    try:
        if request.method=='POST': d=request.get_json() or {};crop=d.get('crop','general');state=d.get('state','Karnataka')
        else: crop=request.args.get('crop','general');state=request.args.get('state','Karnataka')
        raw=orchestrator.policy_agent.get_schemes(crop,state);msp=raw.get('msp_info',{})
        schemes=[{'name':s['name'],'benefit':s['benefit'],'category':s.get('category','')} for s in raw.get('national_schemes',[])+raw.get('state_schemes',[])]
        return jsonify({'success':True,'data':{'crop':crop,'state':state,'msp':{'msp':msp.get('msp'),'year':msp.get('year','2024-25'),'unit':msp.get('unit','₹/quintal')},'schemes':schemes,'key_insight':(raw.get('advisory') or [''])[0],'helpline':'1800-180-1551 (Kisan Call Centre)','contacts':raw.get('key_contacts',[])}})
    except Exception as e: return jsonify({'success':False,'error':str(e)}),500

@app.route('/api/chat',methods=['POST'])
@login_required
def api_chat(current_user):
    try:
        d=request.get_json() or {}
        message=d.get('message','');lang=d.get('lang','en');intent=d.get('intent')
        recent=db.get_user_history(current_user['id'],limit=1)
        last_advisory=None
        if recent:
            last_advisory=db.get_advisory_detail(recent[0]['id'],current_user['id'])
        result=orchestrator.chatbot_agent.run(message,lang=lang,chip_intent=intent,
                                               user_name=current_user['name'].split()[0],last_advisory=last_advisory)
        return jsonify({'success':True,'reply':result['reply'],'intent':result['intent']})
    except Exception as e:
        logger.error(f"Chat error: {e}",exc_info=True)
        return jsonify({'success':False,'error':str(e)}),500

@app.route('/api/chat/chips')
@login_required
def api_chat_chips(current_user):
    lang=request.args.get('lang','en')
    return jsonify({'success':True,'chips':orchestrator.chatbot_agent.get_chips(lang)})

@app.route('/api/history')
@login_required
def api_history(current_user):
    limit=int(request.args.get('limit',20));history=db.get_user_history(current_user['id'],limit)
    return jsonify({'success':True,'history':history,'total':len(history)})

@app.route('/api/history/<int:advisory_id>')
@login_required
def api_history_detail(advisory_id,current_user):
    detail=db.get_advisory_detail(advisory_id,current_user['id'])
    if not detail: return jsonify({'success':False,'error':'Not found'}),404
    return jsonify({'success':True,'data':detail})

@app.route('/api/stats')
@login_required
def api_stats(current_user):
    stats=db.get_user_stats(current_user['id']);return jsonify({'success':True,'stats':stats})

@app.route('/api/health')
def health_check(): return jsonify({'status':'ok','timestamp':datetime.now().isoformat()})

UNITS_TO_HA={'hectare':1.0,'ha':1.0,'acre':0.404686,'guntha':0.010117,'cent':0.0040469,'bigha':0.2529,'sqft':0.0000092903}
def to_hectares(value,unit):
    u=(unit or 'hectare').strip().lower()
    return round(float(value)*UNITS_TO_HA.get(u,1.0),4)

def _safe(u): return{k:u[k] for k in ['id','name','email','phone','state','district','land_area','soil_type','created_at','last_login'] if k in u}

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
