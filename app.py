import time
import re
import hashlib
import urllib.request
import urllib.parse
from flask import Flask,render_template,request,session,url_for,redirect,make_response,abort

from config import Config,basedir
from users import *


app = Flask(__name__)
app.config.from_object(Config)



@app.route('/')
def hello_world():
    return "It's Work!"

@app.route('/diessrf')
def newtestproxy():
    return render_template('diessrf.html')

@app.route('/newtestproxy',methods=['GET',"POST"])
def proxy():
    url = str(request.form.get('url'))
    if(re.findall(r'LiUU',url) != []):
        return render_template('error.html',string='URL中含有十分敏感的语句')
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            html = response.read()
            html = str(html, encoding='UTF-8')
            return html
    except:
        abort(500)

@app.route('/l3m0n')
def l3mon():
    return render_template('l3m0n.html')
@app.route('/tttttttestlogin',methods=['GET','POST'])
def test():
    from users import db
    if request.method == 'GET':
        return render_template('login.html')
    username=request.form.get('name')
    password=request.form.get('password')
    signature = request.form.get('sign')
    #防XSS
    username = re.search(r'<(\w+)>', username).group(1) if re.search(r'<(\w+)>', username) is not None else username
    password = re.search(r'<(\w+)>', password).group(1) if re.search(r'<(\w+)>', password) is not None else password
    signature = re.search(r'<(\w+)>', signature).group(1) if re.search(r'<(\w+)>', signature) is not None else signature

    #防注入
    username = re.sub(r'[\\,/,\',",#,\-,(,),<,>]','', username)
    password = re.sub(r'[\\,/,\',",#,\-,(,),<,>]','', password)
    signature = re.sub(r'[\\,/,\',",#,\-,(,),<,>]','', signature)

    #登陆判断
    session['token'] = hashlib.md5((username + password).encode("utf8")).hexdigest()
    session['name'] = username
    try:
        d_username = DB_User.query.filter_by(name=username).first().name
    except Exception:
        d_username = None
    if d_username is None:
        # 添加新普通用户
        newuser = DB_User(name=username, passwd=password, \
                          token=session['token'], signature=signature)
        db.session.add(newuser)
        db.session.commit()
    time.sleep(2)  # 防止登陆爆破
    # ------------------------------------------------#
    db_user = DB_User.query.filter_by(name=username, passwd=password).first()

    if db_user is None:
        session.pop('token')
        session.pop('name')
        return render_template('error.html',string='密码错误！')
    else:
        if username is 'LiUU':
            user = Users(True, username)
        else:
            user = Users(False, username)
    # 欢迎语句
    str1 = 'Hello {user.username}'
    str2 = 'Your signature:' + signature
    str3 = 'Your token:' + session['token']
    string = (str1 +'<br>'*2 + str2 + '<br>'*2 + str3).format(user=user)

    return render_template('home.html', string=string)


@app.route('/tttttestchpasswd',methods=['GET','POST'])
def chpasswd():
    from users import db
    if request.method == 'GET':
        if session.get('name') is None:
            return render_template('chpasswd.html', notlogin=1)
        else:
            return render_template('chpasswd.html', notlogin=0,name=session.get('name'))

    username = str(request.form.get('name'))
    password = str(request.form.get('password'))
    token = str(request.form.get('token'))


    if username == 'LiUU':
        return render_template('error.html',string='你不能更改又又学长的密码！')

    #防XSS
    username = re.search(r'<(\w+)>', username).group(1) if re.search(r'<(\w+)>', username) is not None else username
    password = re.search(r'<(\w+)>', password).group(1) if re.search(r'<(\w+)>', password) is not None else password
    token = re.search(r'<(\w+)>', token).group(1) if re.search(r'<(\w+)>', token) is not None else token

    #防注入
    username = re.sub(r'[\\,/,\',",#,\-,(,),<,>]','', username)
    password = re.sub(r'[\\,/,\',",#,\-,(,),<,>]','', password)
    token = re.sub(r'[\\,/,\',",#,\-,(,),<,>]','', token)

    if username is None:
        name = DB_User.query.filter_by(token = token,name = session.get('name')).first()
    else:
        name = DB_User.query.filter_by(token=token, name=username).first()

    if name is None:
        return render_template('error.html',string = '你无权修改这个密码！')
    else:
        #密码强度检测
        a = re.findall(r'[A-Z]*',password) == []
        b = re.findall(r'[0-9]*',password) == []
        c = re.findall(r'[a-z]*',password) == []
        d = len(password) < 16
        if a or b or c or d:
            return render_template('error.html',string='密码太弱')
        #change!
        name.passwd = password
        db.session.add(name)
        db.session.commit()
        return render_template('success.html',string='成功修改密码')
@app.route('/robots.txt')
def robots():
    route = basedir + '/robots.txt'
    with open(route) as txt:
        resp = make_response(txt.read())
    resp.headers["Content-type"]="text/plain;charset=UTF-8"
    return resp
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html',string='404 Not Found!'), 404

@app.errorhandler(500)
def internal_server_error(e):
    resp = make_response(render_template('error.html',string = "500 Internal Server Error!"))
    resp.headers['content-type'] = 'text/html'
    resp.headers['charset'] = 'utf-8'
    return resp
if __name__ == '__main__':
    app.run(debug=True)
