from flask import Flask, render_template, request, jsonify
from transformers import pipeline
import torch

app = Flask(__name__)

DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"

generator = pipeline('text-generation', model='deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B', tokenizer='deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B', device=DEVICE)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    global generator
    data = request.get_json()

    user_input = data.get('input_text', '')

    if not user_input.strip():
        return jsonify({'error': 'No input provided'}), 400
    
    try:
        result = generator(user_input, max_length=512, num_return_sequences=1, temperature=0.1, top_k=50, top_p=0.9)
        return jsonify({"generated_text": result[0]["generated_text"]})
    except Exception as e:
        print(f"Error during generation: {e}")
        return jsonify({"error": "An error occurred while generating text"}), 500

if __name__ == '__main__':
    app.run(debug=True)