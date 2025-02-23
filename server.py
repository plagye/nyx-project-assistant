from flask import Flask, render_template, request, jsonify
from transformers import pipeline
import torch
import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", 'deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B')
MAX_LENGTH = int(os.getenv("MAX_LENGTH", 1024))
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.6))
FLASK_ENV = os.getenv("FLASK_ENV", 'production')

def create_app():
    app = Flask(__name__)
    app.config['ENV'] = FLASK_ENV

    DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"
    generator = pipeline(
        'text-generation', 
        model=MODEL_NAME,
        tokenizer=MODEL_NAME, 
        device=DEVICE
    )

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/generate', methods=['POST'])
    def generate():
        data = request.get_json()
        user_input = data.get('input_text', '')

        if not user_input.strip():
            return jsonify({'error': 'No input provided'}), 400

        try:
            result = generator(
                user_input, 
                max_length=MAX_LENGTH,
                num_return_sequences=1,
                temperature=TEMPERATURE, 
                top_k=50, 
                top_p=0.9, 
                truncation=True
            )
            return jsonify({"generated_text": result[0]["generated_text"]})
        
        except Exception as e:
            print(f"Error during generation: {e}")
            return jsonify({"error": "An error occurred while generating text"}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)