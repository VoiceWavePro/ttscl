from flask import Flask, request, send_file
from TTS.api import TTS
import os

app = Flask(__name__)
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

@app.route('/tts', methods=['POST'])
def tts_generate():
    data = request.get_json()
    text = data.get("text", "")
    output_path = "output.wav"
    tts.tts_to_file(text=text, file_path=output_path)
    return send_file(output_path, mimetype="audio/wav", as_attachment=True, download_name="voicewave.wav")
