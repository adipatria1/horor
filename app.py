from flask import Flask, render_template, request, jsonify
from utils.story_generator import generate_complete_horror_story
from utils.config import AVAILABLE_MODELS
import google.generativeai as genai

def print_startup_banner():
    banner = """
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║                                                            ║
    ║             YouTube Cerita Horor Generator v1.0            ║
    ║             Created by tianoambr                           ║
    ║                                                            ║
    ║                                                            ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    """
    print(banner)
    
app = Flask(__name__)
app.config['API_KEY'] = None

def configure_gemini():
    if app.config['API_KEY']:
        genai.configure(api_key=app.config['API_KEY'])
        return True
    return False

@app.route('/')
def home():
    return render_template('index.html', 
                         api_key_set=bool(app.config['API_KEY']),
                         models=AVAILABLE_MODELS)

@app.route('/set-api-key', methods=['POST'])
def set_api_key():
    api_key = request.form.get('api_key')
    if not api_key:
        return jsonify({'error': 'API key tidak boleh kosong'}), 400
    
    try:
        # Test the API key
        genai.configure(api_key=api_key)
        genai.GenerativeModel('gemini-2.0-flash-exp')
        app.config['API_KEY'] = api_key
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': f'API key tidak valid: {str(e)}'}), 400

@app.route('/generate', methods=['POST'])
def generate():
    if not app.config['API_KEY']:
        return jsonify({'error': 'API key belum diatur'}), 403
    
    title = request.form.get('title')
    if not title:
        return jsonify({'error': 'Judul tidak boleh kosong'}), 400
    
    try:
        parts = int(request.form.get('parts', 3))
        if parts < 1 or parts > 10:
            return jsonify({'error': 'Jumlah bagian harus antara 1 dan 10'}), 400
    except ValueError:
        return jsonify({'error': 'Jumlah bagian harus berupa angka'}), 400
    
    model_name = request.form.get('model', 'gemini-2.0-flash-exp')
    if model_name not in AVAILABLE_MODELS:
        return jsonify({'error': 'Model tidak valid'}), 400
    
    configure_gemini()  # Ensure API key is configured
    story = generate_complete_horror_story(title, total_parts=parts, model_name=model_name)
    return jsonify({'story': story})

if __name__ == '__main__':
    print_startup_banner()
    app.run(debug=True)