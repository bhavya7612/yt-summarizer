from flask import Flask, request, render_template, jsonify, session, redirect, send_file
from gtts import gTTS
from langdetect import detect
from io import BytesIO
from bs4 import BeautifulSoup
from sqldb import mysqlconnector
import summariser
import translator

app=Flask(__name__)
app.secret_key='123-456-789'

db_obj=mysqlconnector()

@app.route('/')
def home():
    return render_template('index.html', logged_in = session.get('logged_in', False))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        Email = request.form["email"]
        Password = request.form["password"]
        check = db_obj.user_login(Email,Password)
        print('Information retrieved from SQL.')
        if len(check)>0:
            session["id"] = check[0][0]
            session['logged_in'] = True
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

@app.route('/speak', methods=['POST'])
def text_to_speech():
    try:
        # Parse JSON data from the frontend
        data = request.get_json()
        text = data.get('text')
        language = data.get('language')

        if not text:
            return jsonify({'error': 'Text is required!'}), 400

        plain_text = BeautifulSoup(text, "html.parser").get_text() # Remove HTML tags
        lang_det = detect(plain_text)
        
        if lang_det != language:
            language = lang_det

        # Generate a unique filename for the audio
        # with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False, dir="/tmp") as temp_file:
        #     filename = temp_file.name

        # Convert text to speech
        tts = gTTS(text=plain_text, lang=language, slow=False)
        audio_file=BytesIO()
        tts.write_to_fp(audio_file)
        audio_file.seek(0)
        # tts.save(filename)

        # Serve the audio file
        response = send_file(audio_file, mimetype='audio/mpeg', as_attachment=False, download_name='output.mp3')

        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/output',methods=['GET','POST'])
def summarise():
    if request.method=='POST':
        url=request.form['url']
        max_len=request.form.get('max_len','')
        temperature=request.form['temperature']
        temperature=float(temperature)
        if not max_len.isdigit():
            max_len=150
        else:
            max_len=int(max_len)
        if url[11]=='.':
            video_id = url.split('=')[1]
        else:
            video_id = url.split('?')[0][17:]
        title=db_obj.insert_video_info(video_id,session['id'])
        result=summariser.summarise(video_id, max_len, temperature)
        # langs={
        #         'en':'English', 'hi':'Hindi', 'mr':'Marathi',\
        #         'gu':'Gujarati', 'ml':'malayalam', 'kn':'Kannada',\
        #         'bn':'Bengali', 'pa':'Punjabi', 'ta':'Tamil',\
        #         'te':'Telugu', 'ar':'Arabic', 'fr':'French',\
        #         'de':'German', 'ja':'Japanese', 'ru':'Russian', 'es':'Spanish'}
        
        summary=result[0]
        transcript=result[1]
        
        formatted_summary_en = summariser.process_summary(summary)

        summary_hi=translator.translate_to_hindi(summary)
        formatted_summary_hi = summariser.process_summary(summary_hi)

        summary_mr=translator.translate_to_marathi(summary)
        formatted_summary_mr = summariser.process_summary(summary_mr)

        summary_guj=translator.translate_to_guj(summary)
        formatted_summary_guj = summariser.process_summary(summary_guj)

        summary_malaya=translator.translate_to_malayalam(summary)
        formatted_summary_malaya = summariser.process_summary(summary_malaya)

        summary_kan=translator.translate_to_kannada(summary)
        formatted_summary_kan = summariser.process_summary(summary_kan)
        
        summary_ben=translator.translate_to_bengali(summary)
        formatted_summary_ben = summariser.process_summary(summary_ben)

        summary_pj=translator.translate_to_punjabi(summary)
        formatted_summary_pj = summariser.process_summary(summary_pj)

        summary_tam=translator.translate_to_tamil(summary)
        formatted_summary_tam = summariser.process_summary(summary_tam)

        summary_tel=translator.translate_to_telugu(summary)
        formatted_summary_tel = summariser.process_summary(summary_tel)

        summary_ar=translator.translate_to_arabic(summary)
        formatted_summary_ar = summariser.process_summary(summary_ar)

        summary_french=translator.translate_to_french(summary)
        formatted_summary_french = summariser.process_summary(summary_french)

        summary_germ=translator.translate_to_german(summary)
        formatted_summary_germ = summariser.process_summary(summary_germ)

        summary_jap=translator.translate_to_japanese(summary)
        formatted_summary_jap = summariser.process_summary(summary_jap)

        summary_rus=translator.translate_to_russian(summary)
        formatted_summary_rus = summariser.process_summary(summary_rus)

        summary_sp=translator.translate_to_spanish(summary)
        formatted_summary_sp = summariser.process_summary(summary_sp)
        
        return render_template('output.html', transcript=transcript, vid_title=title,
                               summary_en = formatted_summary_en,
                               summary_hi = formatted_summary_hi,
                               summary_mr = formatted_summary_mr,
                               summary_guj = formatted_summary_guj,
                               summary_malaya = formatted_summary_malaya,
                               summary_kan = formatted_summary_kan,
                               summary_ben = formatted_summary_ben,
                               summary_pj = formatted_summary_pj, 
                               summary_tam = formatted_summary_tam,
                               summary_tel = formatted_summary_tel,
                               summary_ar = formatted_summary_ar,
                               summary_french = formatted_summary_french,
                               summary_germ = formatted_summary_germ,
                               summary_jap = formatted_summary_jap,
                               summary_rus = formatted_summary_rus,
                               summary_sp = formatted_summary_sp)
    else:
        return render_template('output.html')

@app.route('/logout')
def logout():
    session.pop('id')
    session.pop('logged_in', None)
    return render_template('index.html', message='Logout Successful.')

if __name__=="__main__":
    app.run(debug=True)