from flask import Flask, request, render_template, jsonify, session, redirect
from sqldb import mysqlconnector
import summariser

app=Flask(__name__)
app.secret_key='123-456-789'

db_obj=mysqlconnector()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        Email = request.form["email"]
        Password = request.form["password"]
        check = db_obj.user_login(Email,Password)
        print('Information retrieved from SQL.')
        if len(check)>0:
            session["id"] = check[0][1]
            print("session --> ",session)
            return redirect("/project")
        else:
            return render_template('login.html',message="Invalid Email or Password!")
    else:
        if 'id' in session:
            return render_template('nologinreq.html')
        else:
            return render_template("login.html")

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        user_name = request.form["username"]
        Email     = request.form["email"]
        Password  = request.form["password"]
        check = db_obj.user_exists_signup(Email)
        print('Information retrieved from SQL.')
        if len(check)>0:
            return render_template('signup.html',message="User already exists")
        else:
            res = db_obj.user_signup(user_name,Email,Password)
            if 'id' in session:
                session.pop('id')
            return redirect("/login")
    else:
        return render_template("signup.html")

@app.route('/project')
def projectpage():
    if 'id' in session:
        return render_template('url.html')
    else:
        return render_template('nologin.html')


@app.route('/output',methods=['POST'])
def summarise():
    if request.method=='POST':
        url=request.form['url']
        max_len=request.form['max_len']
        if max_len=="":
            max_len=150
        else:
            max_len=int(max_len)
        video_id=url.split('=')[1]
        transcript=summariser.get_transcript(video_id)
        summary=summariser.summarise(video_id, max_len)
        tr_len=len(transcript.split())
        sum_len=len(summary.split())
        return render_template('output.html',transcript=transcript,summary=summary,tr_len=tr_len,sum_len=sum_len)
    else:
        return render_template('output.html')

@app.route('/logout')
def logout():
    session.pop('id')
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)