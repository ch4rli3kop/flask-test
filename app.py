'''
TODO: 패스워드 해시처리해서 저장하기
TODO: 장치가 많아질 경우를 대비하여 장치 정보를 이중 형태로 저장해야함
TODO: 온도 변화 그래프를 보여주기 위해서 DB 추가
TODO: flask-login으로 로그인 기능 대체하기

# administration
TODO: 데이터 제거 기능 추가
TODO: 온도 변화 그래프 보여주기
TODO: 현재 온도 보여주기
TODO: administration 페이지에서 계정의 패스워드를 변경하는 기능 추가
'''



from flask import Flask, render_template, redirect, request, flash, session
from flask.helpers import url_for
from flask_login import fresh_login_required
import os

app = Flask(__name__)

#app.secret_key = os.urandom(32)
app.config['SECRET_KEY'] = os.urandom(32)

device_states = {
    'temperature':0,
    'humidity':0,
    'pump':True
}

login_data = {
    'id':'',
    'pw':''
}

# FIXME: 임시 변수, 관리자 계정이 생성되었는지 확인함
admin_exist = False

# 모든 페이지에서 관리자 계정이 정상적으로 존재하는지 확인 => 없으면 바로 index로 리다이렉트

@app.route('/')
def index():

    # 현재 세션 검사
    if 'username' in session:
        return redirect(url_for('administration'))

    if login_data['id']:
        # 로그인 화면으로 이동
        return redirect(url_for('login'))
    else:
        # 관리자 계정 생성 화면으로 이동
        return redirect(url_for('register'))
    #return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if login_data['id'] == '':
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if  username == login_data['id'] and\
            password == login_data['pw']:
            session['username'] = password
            #return 'login success!'
            return redirect(url_for('administration'))
        flash('login failed!')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/changepw', methods=['GET', 'POST'])
def changepw():
    # 현재 세션이 존재하는지 확인
    # FIXME: api가 노출되서 로그인하지 않아도 패스워드 변경이 가능 세션 검사가 제대로 되지 않음. Internel 혹은 flask-login으로 쉽게 가능함
    if 'username' in session:
        return redirect(url_for('index'))

    # 패스워드가 일치하는지 확인
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        cpassword = request.form['cpassword']
        if current_password == login_data['pw'] and\
            new_password == cpassword:
            login_data['pw'] = new_password
            session['username'] = new_password
            #return 'login success!'
            return redirect(url_for('login'))
        flash('incorrect password!')

    return render_template('changepw.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # 관리자 계정이 만들어졌는지 체크
    if login_data['id'] != '' and login_data['pw'] != '':
        # FIXME: logging 추가
        #app.logger.debug('')
        return 'admin already exists!'
    
    # 관리자 계정은 하나밖에 만들지 못하기 때문에 입력 검사하기
    if request.method == 'POST' and \
        request.form['username'] != '' and \
            request.form['password'] != '':
        login_data['id'] = request.form['username']
        login_data['pw'] = request.form['password']
        return redirect(url_for('index'))

    # else:
    #     # FIXME: 팝업으로 ID 잘못 입력되었다고 뜨기
    #     return 'Register error'

    return render_template('register.html')

@app.route('/adminstration')
def administration():
    # 로그인 검사 추가
    if 'username' not in session:
        return redirect(url_for('index'))

    return render_template('administration.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.error(error)
    return '페이지를 찾을 수 없습니다.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
