from flask import Flask, request, send_file
from gtts import gTTS
import io

app = Flask(__name__)

@app.route('/tts', methods=['POST'])
def generate():
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return "Text is required", 400
    tts = gTTS(text)
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    return send_file(mp3_fp, mimetype="audio/mpeg", as_attachment=True, download_name="voicewave.mp3")
