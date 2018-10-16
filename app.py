import time
import re
import hashlib
from flask import Flask,render_template,request,session,url_for,redirect

from config import Config
from users import *


app = Flask(__name__)
app.config.from_object(Config)



@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/tttttttestlogin',methods=['GET','POST'])
def test():
    from users import db
    if request.method == 'GET':
        return render_template('userlogin.html')
    username=request.form.get('name')
    password=request.form.get('password')
    signature = request.form.get('sign')
    #登陆判断
    session['token'] = hashlib.md5((username + password).encode("utf8")).hexdigest()
    session['name'] = username
    try:
        d_username = DB_User.query.filter_by(name=username).first().name
    except AttributeError:
        d_username = None
    if d_username is None:
        # 添加新普通用户
        newuser = DB_User(name=username, passwd=password, \
                          token=session['token'], signature=signature)
        db.session.add(newuser)
        db.session.commit()
    time.sleep(3)  # 防止登陆爆破
    # ------------------------------------------------#
    db_user = DB_User.query.filter_by(name=username, passwd=password).first()

    if db_user is None:
        session.pop('token')
        session.pop('name')
        return render_template('userlogin.html')
    else:
        if username == 'LiUU':
            user = Users(True, username)
        else:
            user = Users(False, username)
    # 欢迎语句
    str1 = 'Hello {user.username}'
    str2 = 'Your signature:' + signature
    str3 = 'Your token:' + session['token']
    string = (str1 +'<br>' + str2 + '<br>' + str3).format(user=user)

    return render_template('userhome.html', string=string)


@app.route('/tttttestchpasswd',methods=['GET','POST'])
def chpasswd():
    from users import db
    if request.method == 'GET':
        if session.get('name') is None:
            return render_template('userchpasswd.html', flag=1)
        else:
            return render_template('userchpasswd.html', name=session.get('name'))
    username = request.form.get('name')
    password = request.form.get('password')
    token = request.form.get('token')

    if username == 'LiUU':
        return render_template('error.html',string='你不能更改又又学长的密码！')

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


if __name__ == '__main__':
    app.run(debug=True)
