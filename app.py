from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from TTS.api import TTS
from pydub import AudioSegment
import os
import io
import uuid

app = Flask(__name__)
CORS(app)

@app.route('/tts', methods=['POST'])
def generate():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "Text is required"}), 400

    try:
        # Lazy-load the model
        tts_model = TTS(model_name="tts_models/en/ljspeech/fastspeech2", gpu=False)
        tmp_wav_path = f"/tmp/{uuid.uuid4()}.wav"
        tts_model.tts_to_file(text=text, file_path=tmp_wav_path)

        audio = AudioSegment.from_wav(tmp_wav_path)
        mp3_io = io.BytesIO()
        audio.export(mp3_io, format="mp3")
        mp3_io.seek(0)
        os.remove(tmp_wav_path)

        return send_file(mp3_io, mimetype="audio/mpeg", download_name="voicewave.mp3")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return jsonify({"error": "Audio generation failed."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
