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
            session["id"] = check[0][0]
            print("session --> ",session)
            return redirect("/project")
        else:
            return render_template('login.html',message="Invalid Email or Password!")
    else:
        if 'id' in session:
            return render_template('url.html',message="You are already logged in! You can continue to the project:)")
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
            return render_template('signup.html',message="User already exists!")
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
        return render_template('login.html', message="You are not logged in! Please login first.")


@app.route('/output',methods=['GET','POST'])
def summarise():
    if request.method=='POST':
        url=request.form['url']
        max_len=request.form.get('max_len','')
        lang=request.form['lang']
        if not max_len.isdigit():
            max_len=150
        else:
            max_len=int(max_len)
        video_id=url.split('=')[1]
        title=db_obj.insert_video_info(video_id,session['id'])
        transcript=summariser.get_transcript(video_id)
        summary=summariser.summarise(video_id, max_len, lang)
        langs={
                'hi':'Hindi', 'mr':'Marathi', 'gu':'Gujarati',\
                'ml':'malayalam', 'kn':'Kannada', 'bn':'Bengali',\
                'pa':'Punjabi', 'ta':'Tamil', 'te':'Telugu',\
                'ar':'Arabic', 'fr':'French', 'de':'German',\
                'ja':'Japanese', 'ru':'Russian', 'es':'Spanish'}
        # tr_len=len(transcript.split())
        # sum_len=len(summary.split())
        return render_template('output.html', transcript=transcript, summary=summary, title=title, lang=langs[lang])
    else:
        return render_template('output.html')

@app.route('/logout')
def logout():
    session.pop('id')
    return render_template('index.html', message='Logout Successful.')

if __name__=="__main__":
    app.run(debug=True)