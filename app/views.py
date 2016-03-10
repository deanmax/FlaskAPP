from flask import request
from flask import render_template
from flask import make_response
from app import app
from lib import audio_process as ap
import os

@app.route('/')
def index():
    return render_template('form.html',
            title = 'Digging Quizlet Audios',
           )

@app.route('/get_audio', methods = ['POST'])
def get_audio():
    url = request.form["url"]
    audio_urls = ap.get_audio_urls(url)
    file_path = ap.generate_combined_audio(audio_urls)

    with open(file_path, 'r') as f:
        body = f.read()
    os.remove(file_path)
    rsp = make_response(body)
    rsp.headers["Content-Disposition"] = "attachment; filename=%s" % os.path.basename(file_path)
    return rsp
