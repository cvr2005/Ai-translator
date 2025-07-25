from flask import Flask, render_template, request
from googletrans import Translator
from gtts import gTTS
import os
import uuid

app = Flask(__name__)
translator = Translator()

@app.route('/', methods=['GET', 'POST'])
def index():
    translated_text = ''
    audio_path = ''
    
    if request.method == 'POST':
        text = request.form['text']
        target_lang = request.form['target']
        
        # Translate text using Google Translate
        translated = translator.translate(text, dest=target_lang)
        translated_text = translated.text

        # Ensure 'static' folder exists
        if not os.path.exists("static"):
            os.makedirs("static")

        # Generate unique filename and save audio
        filename = f"static/audio_{uuid.uuid4().hex}.mp3"
        tts = gTTS(text=translated_text, lang=target_lang)
        tts.save(filename)
        audio_path = filename

    return render_template('index.html', translated=translated_text, audio_path=audio_path)

if __name__ == '__main__':
    app.run(debug=True)
