import torchaudio
from flask import Flask, request, jsonify, send_from_directory
from speechbrain.pretrained import Tacotron2
from speechbrain.pretrained import HIFIGAN

app = Flask(__name__)

# Load the models
tacotron2 = Tacotron2.from_hparams(source="/Users/andrewasher/custom_tts_model\custom_tts_model.pth", savedir="tmpdir_tts")
hifi_gan = HIFIGAN.from_hparams(source="speechbrain/tts-hifigan-ljspeech", savedir="tmpdir_vocoder")

@app.route('/convert-text', methods=['POST'])
def convert_text_to_speech():
    text = request.json.get('text')

    # Running the TTS
    mel_output, mel_length, alignment = tacotron2.encode_text(text)

    # Running Vocoder (spectrogram-to-waveform)
    waveforms = hifi_gan.decode_batch(mel_output)

    # Save the waveform to a temporary file
    output_path = "tmp_TTS_output.wav"
    torchaudio.save(output_path, waveforms.squeeze(1), 22050)
    
    return send_from_directory(directory='.', filename=output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5009)
