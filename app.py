from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import TFT5ForConditionalGeneration, T5Tokenizer

app = Flask(__name__)
CORS(app)

# Specify the path to your model and tokenizer files
model_path = "/Users/andrewasher/Education/Research Project/Andrew/finetuned model/model"
tokenizer_path = "/Users/andrewasher/Education/Research Project/Andrew/finetuned model/tokenizer_custom"

# Load the model and tokenizer
model = TFT5ForConditionalGeneration.from_pretrained(model_path)
tokenizer = T5Tokenizer.from_pretrained(tokenizer_path)

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Text Summarization API!"

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.json
        document = data.get('document')

        if not document:
            return jsonify({'error': 'Document is missing'}), 400

        # Tokenize and generate the summary
        input_ids = tokenizer.encode("summarize: " + document, return_tensors="tf", max_length=512, truncation=True)
        summary_ids = model.generate(input_ids, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return jsonify({'summary': summary})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5005)
