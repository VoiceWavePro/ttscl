from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from gtts import gTTS
import os
import io
import uuid

app = Flask(__name__)
CORS(app)

@app.route("/tts", methods=["POST"])
def generate():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "Text is required"}), 400

    try:
        tts = gTTS(text)
        mp3_io = io.BytesIO()
        tts.write_to_fp(mp3_io)
        mp3_io.seek(0)
        return send_file(mp3_io, mimetype="audio/mpeg", download_name="voicewave.mp3")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return jsonify({"error": "Audio generation failed."}), 500

if __name__ == "__main__":
    from waitress import serve
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Serving on port {port}")
    serve(app, host="0.0.0.0", port=port)
