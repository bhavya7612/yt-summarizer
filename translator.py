from googletrans import Translator

trans=Translator()

def translate_to_hi(text):
    res=trans.translate(text, src='en', dest='hi')
    res=str(res.text)
    return res

def translate_to_marathi(text):
    res=trans.translate(text, src='en', dest='mr')
    res=str(res.text)
    return res

def translate_to_guj(text):
    res=trans.translate(text, src='en', dest='gu')
    res=str(res.text)
    return res

def translate_to_malayalam(text):
    res=trans.translate(text, src='en', dest='ml')
    res=str(res.text)
    return res

def translate_to_kannada(text):
    res=trans.translate(text, src='en', dest='kn')
    res=str(res.text)
    return res

def translate_to_bengali(text):
    res=trans.translate(text, src='en', dest='bn')
    res=str(res.text)
    return res

def translate_to_punjabi(text):
    res=trans.translate(text, src='en', dest='pa')
    res=str(res.text)
    return res

def translate_to_tamil(text):
    res=trans.translate(text, src='en', dest='ta')
    res=str(res.text)
    return res

def translate_to_telugu(text):
    res=trans.translate(text, src='en', dest='te')
    res=str(res.text)
    return res

def translate_to_arabic(text):
    res=trans.translate(text, src='en', dest='ar')
    res=str(res.text)
    return res

def translate_to_french(text):
    res=trans.translate(text, src='en', dest='fr')
    res=str(res.text)
    return res

def translate_to_german(text):
    res=trans.translate(text, src='en', dest='de')
    res=str(res.text)
    return res

def translate_to_japanese(text):
    res=trans.translate(text, src='en', dest='ja')
    res=str(res.text)
    return res

def translate_to_russian(text):
    res=trans.translate(text, src='en', dest='ru')
    res=str(res.text)
    return res

def translate_to_spanish(text):
    res=trans.translate(text, src='en', dest='es')
    res=str(res.text)
    return res