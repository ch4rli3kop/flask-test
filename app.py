from flask import Flask, render_template, redirect, request, flash
from flask.helpers import url_for
from flask_login import fresh_login_required

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ABCD'

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


    if login_data['id']:
        # 로그인 화면으로 이동
        return redirect(url_for('login'))
    else:
        # 관리자 계정 생성 화면으로 이동
        return redirect(url_for('register'))
    #return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == login_data['id'] and\
            request.form['password'] == login_data['pw']:
            return 'login success!'
        return 'login failed!'

    return render_template('login.html')

@app.route('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # 관리자 계정이 만들어졌는지 체크
    if login_data['id'] != '' and login_data['pw'] != '':
        # FIXME: logging 추가
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

app.run(host='0.0.0.0', port=8000, debug=True)
