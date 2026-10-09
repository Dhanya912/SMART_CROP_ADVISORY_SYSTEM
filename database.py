import sqlite3,hashlib,hmac,os,json,secrets
from datetime import datetime,timedelta
from utils.logger import get_logger
logger=get_logger(__name__)
DB_PATH=os.environ.get('DB_PATH','data/cropai.db')
PEPPER=os.environ.get('PEPPER','cropai-pepper-yit-2025')

def get_conn():
    os.makedirs(os.path.dirname(DB_PATH),exist_ok=True)
    conn=sqlite3.connect(DB_PATH,check_same_thread=False)
    conn.row_factory=sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db():
    conn=get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,phone TEXT,state TEXT,
            district TEXT,land_area REAL DEFAULT 1.0,
            soil_type TEXT DEFAULT 'loamy',
            created_at TEXT DEFAULT(datetime('now')),
            last_login TEXT,is_active INTEGER DEFAULT 1);
        CREATE TABLE IF NOT EXISTS sessions(
            token TEXT PRIMARY KEY,user_id INTEGER NOT NULL REFERENCES users(id),
            created_at TEXT DEFAULT(datetime('now')),expires_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS advisory_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES users(id),
            created_at TEXT DEFAULT(datetime('now')),
            location TEXT,land_area REAL,primary_concern TEXT,language TEXT,
            nitrogen REAL,phosphorus REAL,potassium REAL,ph REAL,
            temperature REAL,humidity REAL,rainfall REAL,soil_type TEXT,
            image_path TEXT,report_json TEXT,
            top_crop TEXT,crop_confidence REAL,
            disease_name TEXT,disease_severity TEXT,
            soil_score INTEGER,market_price REAL,net_income REAL,processing_time REAL);
        CREATE INDEX IF NOT EXISTS idx_ah_user ON advisory_history(user_id);
    """)
    conn.commit();conn.close();logger.info("DB initialised.")

def hash_password(p): return hashlib.sha256((p+PEPPER).encode()).hexdigest()
def verify_password(p,h): return hmac.compare_digest(hash_password(p),h)

def create_session(uid):
    token=secrets.token_urlsafe(32)
    exp=(datetime.utcnow()+timedelta(days=7)).isoformat()
    conn=get_conn();conn.execute("INSERT INTO sessions(token,user_id,expires_at)VALUES(?,?,?)",(token,uid,exp))
    conn.commit();conn.close();return token

def get_session_user(token):
    if not token: return None
    conn=get_conn()
    row=conn.execute("SELECT u.* FROM sessions s JOIN users u ON u.id=s.user_id WHERE s.token=? AND s.expires_at>datetime('now') AND u.is_active=1",(token,)).fetchone()
    conn.close();return dict(row) if row else None

def delete_session(token):
    conn=get_conn();conn.execute("DELETE FROM sessions WHERE token=?",(token,));conn.commit();conn.close()

def create_user(name,email,password,phone='',state='',district='',land_area=1.0,soil_type='loamy'):
    conn=get_conn()
    try:
        conn.execute("INSERT INTO users(name,email,password_hash,phone,state,district,land_area,soil_type)VALUES(?,?,?,?,?,?,?,?)",
            (name,email.lower().strip(),hash_password(password),phone,state,district,land_area,soil_type))
        conn.commit()
        user=conn.execute("SELECT * FROM users WHERE email=?",(email.lower(),)).fetchone()
        conn.close();return{'ok':True,'user':dict(user)}
    except sqlite3.IntegrityError:
        conn.close();return{'ok':False,'error':'Email already registered.'}

def get_user_by_email(email):
    conn=get_conn();row=conn.execute("SELECT * FROM users WHERE email=? AND is_active=1",(email.lower(),)).fetchone();conn.close();return dict(row) if row else None

def get_user_by_id(uid):
    conn=get_conn();row=conn.execute("SELECT * FROM users WHERE id=?",(uid,)).fetchone();conn.close();return dict(row) if row else None

def update_last_login(uid):
    conn=get_conn();conn.execute("UPDATE users SET last_login=datetime('now') WHERE id=?",(uid,));conn.commit();conn.close()

def update_user_profile(uid,data):
    allowed=['name','phone','state','district','land_area','soil_type']
    sets,vals=[],[]
    for k in allowed:
        if k in data: sets.append(f"{k}=?");vals.append(data[k])
    if not sets: return
    vals.append(uid);conn=get_conn()
    conn.execute(f"UPDATE users SET {','.join(sets)} WHERE id=?",vals);conn.commit();conn.close()

def save_advisory(user_id,inputs,report):
    secs=report.get('sections',{})
    crop=secs.get('crop_recommendation',{});dis=secs.get('disease_detection',{})
    soil=secs.get('soil_health',{});mkt=secs.get('market_intelligence',{})
    top3=crop.get('all_crops',[]);conf=top3[0].get('confidence',0) if top3 else 0
    if conf>1: conf=conf/100
    def parse_num(s):
        s=str(s).replace('₹','').replace('Rs.','').replace(',','').strip()
        try: return float(''.join(c for c in s if c.isdigit() or c=='.'))
        except: return 0.0
    net_val=parse_num(mkt.get('net_income','0'))
    price_val=parse_num(str(mkt.get('avg_price','0')).split('/')[0])
    sp=inputs.get('soil_params',{});conn=get_conn()
    cur=conn.execute("""INSERT INTO advisory_history
        (user_id,location,land_area,primary_concern,language,
         nitrogen,phosphorus,potassium,ph,temperature,humidity,rainfall,soil_type,
         image_path,report_json,top_crop,crop_confidence,disease_name,disease_severity,
         soil_score,market_price,net_income,processing_time)VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (user_id,inputs.get('location'),inputs.get('land_area'),inputs.get('primary_concern'),inputs.get('language'),
         sp.get('N'),sp.get('P'),sp.get('K'),sp.get('ph'),sp.get('temperature'),sp.get('humidity'),sp.get('rainfall'),sp.get('soil_type'),
         inputs.get('image_path'),json.dumps(report),
         crop.get('top_crop_key',crop.get('top_crop','')).lower(),conf,dis.get('disease',''),dis.get('severity',''),
         soil.get('health_score',0),price_val,net_val,report.get('processing_time_s',0)))
    conn.commit();rid=cur.lastrowid;conn.close();logger.info(f"Advisory #{rid} saved");return rid

def get_user_history(user_id,limit=20):
    conn=get_conn()
    rows=conn.execute("SELECT id,created_at,location,land_area,primary_concern,top_crop,crop_confidence,disease_name,disease_severity,soil_score,market_price,net_income,processing_time,language FROM advisory_history WHERE user_id=? ORDER BY created_at DESC LIMIT ?",(user_id,limit)).fetchall()
    conn.close();return[dict(r) for r in rows]

def get_advisory_detail(aid,uid):
    conn=get_conn();row=conn.execute("SELECT * FROM advisory_history WHERE id=? AND user_id=?",(aid,uid)).fetchone();conn.close()
    if not row: return None
    d=dict(row)
    if d.get('report_json'):
        try: d['report']=json.loads(d['report_json'])
        except: pass
    return d

def get_user_stats(uid):
    conn=get_conn()
    row=conn.execute("SELECT COUNT(*) as total,AVG(soil_score) as avg_soil,AVG(net_income) as avg_income,MAX(created_at) as last_advisory FROM advisory_history WHERE user_id=?",(uid,)).fetchone()
    crops=conn.execute("SELECT top_crop,COUNT(*) as cnt FROM advisory_history WHERE user_id=? AND top_crop!='' GROUP BY top_crop ORDER BY cnt DESC LIMIT 3",(uid,)).fetchall()
    conn.close();return{'total_advisories':row['total'] or 0,'avg_soil_score':round(row['avg_soil'] or 0,1),'avg_net_income':round(row['avg_income'] or 0),'last_advisory':row['last_advisory'],'top_crops':[dict(r) for r in crops]}
