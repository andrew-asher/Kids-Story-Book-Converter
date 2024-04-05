from flask import Flask, request, send_file, jsonify
from flask_cors import CORS  # Import the CORS module
from gtts import gTTS
import os

app = Flask(__name__)
CORS(app)  

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    data = request.json
    text = data['text']
    tts = gTTS(text=text, lang='en', slow=False)
    file_name = "output.mp3"
    tts.save(file_name)
    return send_file(file_name, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, port=5009)
