from flask import request
from flask import render_template
from flask import make_response
from app import app
from lib import audio_process as ap
import os

def send_response(url, file_path):
    with open(file_path, 'r') as f:
        body = f.read()
    os.remove(file_path)
    url_parsed = url.split("/")
    filename = url_parsed[-1] if url_parsed[-1] != '' or len(url_parsed)== 1 else url_parsed[-2]
    rsp = make_response(body)
    rsp.headers["Content-Disposition"] = "attachment; filename=%s.mp3" % os.path.basename(filename)
    return rsp


@app.route('/')
def index():
    return render_template('form.html',
            title = 'Digging Quizlet Audios',
           )

@app.route('/get_audio', methods = ['POST'])
def get_audio():
    url = request.form["url_1"]
    audio_urls = ap.get_audio_urls(url)
    file_path = ap.generate_combined_audio(audio_urls)
    return send_response(url, file_path)

@app.route('/get_starred_audio', methods = ['POST'])
def get_starred_audio():
    url = request.form["url_2"]
    audio_urls = ap.get_starred_audio_urls(url)
    file_path = ap.generate_combined_audio(audio_urls)
    return send_response(url, file_path)
