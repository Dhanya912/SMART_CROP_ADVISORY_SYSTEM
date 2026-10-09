from functools import wraps
from flask import request,jsonify,redirect
import database as db
COOKIE_NAME='cropai_session'
def get_current_user(): return db.get_session_user(request.cookies.get(COOKIE_NAME))
def login_required(f):
    @wraps(f)
    def d(*a,**kw):
        u=get_current_user()
        if not u: return jsonify({'success':False,'error':'Not authenticated','redirect':'/login'}),401
        return f(*a,**kw,current_user=u)
    return d
def login_required_page(f):
    @wraps(f)
    def d(*a,**kw):
        u=get_current_user()
        if not u: return redirect('/login')
        return f(*a,**kw,current_user=u)
    return d
