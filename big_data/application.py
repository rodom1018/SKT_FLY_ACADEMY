from flask import Flask, render_template, request, session, redirect
import sys
from wordcloud import WordCloud
import time
import matplotlib.pyplot as plt
import pymysql

application = Flask(__name__)
application.config['SECRET_KEY'] = 'apptools'

dbconn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='1234',
    db='aifly',
    charset='utf8'
)
cursor = dbconn.cursor()
@application.route("/", methods = ['GET', 'POST'])
def hello():
    if session.get('ss_id') == False:
        return redirect('/login')
    
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        #기사 제목 받기
        content = request.form['content']
        #print(content) 잘 출력됨
        
        #wordcloud 만들고
        font_path ='/workspace/sample/static/NanumGothic.ttf'
        wordcloud = WordCloud(font_path=font_path, background_color='white', 
                              width=400, height=400)
        wordcloud = wordcloud.generate(content)
        
        #wordcloud 그림 저장 . 
        fig = plt.figure(figsize=(6,6))
        plt.imshow(wordcloud)
        plt.axis('off')
        fig.savefig('/workspace/sample/static/wordcloud.png')
        
        return render_template('index.html', content = content, time = time.time())
   
@application.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        userid = request.form['userid']
        userpw = request.form['userpw']
        """
        print(userid)
        print("!!!!")
        print(userpw)
        print("!!!!")
        정상 
        """
        sql = """select name from member where userid='%s' and userpw=password('%s');""" % (userid,userpw)
        
        cursor.execute(sql)
        rows = cursor.fetchone()
        #dbconn.close()
        
        if rows:
            session['ss_id'] = userid
            session['ss_name'] = rows[0]
            return redirect('/')
        else: 
        	return render_template('login.html', msg="아이디 또는 비번이 틀림")
        
@application.route("/logout")
def logout():
    session['ss_id'] = False
    session['ss_name'] = False
    return redirect('/login')

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=int(sys.argv[1]))
