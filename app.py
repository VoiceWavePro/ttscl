from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from TTS.api import TTS
from pydub import AudioSegment
import os
import io
import uuid

app = Flask(__name__)
CORS(app)

# Load Coqui TTS model once at startup
tts_model = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

@app.route('/tts', methods=['POST'])
def generate():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "Text is required"}), 400

    try:
        # Save WAV temporarily
        tmp_wav_path = f"/tmp/{uuid.uuid4()}.wav"
        tts_model.tts_to_file(text=text, file_path=tmp_wav_path)

        # Convert WAV to MP3 in memory
        audio = AudioSegment.from_wav(tmp_wav_path)
        mp3_io = io.BytesIO()
        audio.export(mp3_io, format="mp3")
        mp3_io.seek(0)

        # Clean up
        os.remove(tmp_wav_path)

        return send_file(
            mp3_io,
            mimetype="audio/mpeg",
            as_attachment=True,
            download_name="voicewave.mp3"
        )
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return jsonify({"error": "Audio generation failed."}), 500
    tts_model = TTS(
    model_name="tts_models/en/ljspeech/tacotron2-DDC",
    progress_bar=False,
    gpu=False,
    # Add this line to ensure model download:
    model_dir="/app/models"
)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
