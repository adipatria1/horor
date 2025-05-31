import tkinter as tk
from tkinter import font as tkfont
import socket
import webbrowser
import threading
import os

from flask import Flask, render_template, request, jsonify
# Impor dari utils Anda (pastikan path ini benar relatif terhadap app.py)
from utils.story_generator import generate_complete_horror_story
from utils.config import AVAILABLE_MODELS
import google.generativeai as genai

# --- Konfigurasi dan Variabel Global ---
SERVER_PORT = 5000
root_window = None
status_label = None

# --- Definisi Aplikasi Flask ---
app = Flask(__name__) # Instance Flask didefinisikan di sini
app.config['API_KEY'] = None # Akan diatur melalui antarmuka web

def print_startup_banner(): # Fungsi ini masih bisa digunakan jika dijalankan dari konsol
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

def configure_gemini_in_flask(): # Ganti nama agar tidak bentrok jika ada fungsi lain
    if app.config['API_KEY']:
        try:
            genai.configure(api_key=app.config['API_KEY'])
            # Lakukan tes sederhana untuk memastikan API key valid
            # genai.GenerativeModel('gemini-pro') # Ganti dengan model yang ringan jika perlu tes
            return True
        except Exception as e:
            print(f"Error configuring Gemini with API key: {e}")
            # Mungkin reset API key di sini jika konfigurasi gagal
            # app.config['API_KEY'] = None
            return False
    return False

# --- Rute Flask ---
@app.route('/')
def home():
    api_key_is_set = configure_gemini_in_flask()
    return render_template('index.html',
                         api_key_set=api_key_is_set, # Gunakan hasil konfigurasi
                         models=AVAILABLE_MODELS)

@app.route('/set-api-key', methods=['POST'])
def set_api_key():
    api_key = request.form.get('api_key')
    if not api_key:
        return jsonify({'error': 'API key tidak boleh kosong'}), 400

    try:
        # Test API key sebelum menyimpannya
        genai.configure(api_key=api_key)
        # Lakukan list models atau operasi ringan untuk verifikasi
        # genai.list_models() # Contoh operasi ringan
        # Jika Anda menggunakan model spesifik untuk tes, pastikan model itu ada
        # genai.GenerativeModel('gemini-1.0-pro') # Sesuaikan nama model jika perlu
        app.config['API_KEY'] = api_key
        print(f"API Key set successfully: {api_key[:5]}...") # Jangan log seluruh API key
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error setting API key: {e}")
        return jsonify({'error': f'API key tidak valid atau terjadi kesalahan: {str(e)}'}), 400

@app.route('/generate', methods=['POST'])
def generate():
    if not app.config['API_KEY']:
        return jsonify({'error': 'API key belum diatur. Silakan atur melalui halaman utama.'}), 403

    if not configure_gemini_in_flask(): # Pastikan Gemini dikonfigurasi dengan benar
         return jsonify({'error': 'Konfigurasi API key gagal. Periksa API key Anda.'}), 403

    title = request.form.get('title')
    if not title:
        return jsonify({'error': 'Judul tidak boleh kosong'}), 400

    try:
        parts = int(request.form.get('parts', 3))
        if parts < 1 or parts > 10: # Batasan contoh
            return jsonify({'error': 'Jumlah bagian harus antara 1 dan 10'}), 400
    except ValueError:
        return jsonify({'error': 'Jumlah bagian harus berupa angka'}), 400

    model_name = request.form.get('model', 'gemini-1.5-flash') # Gunakan model default dari AVAILABLE_MODELS
    if model_name not in AVAILABLE_MODELS: # Pastikan model_name ada di AVAILABLE_MODELS
        return jsonify({'error': 'Model tidak valid'}), 400

    try:
        story = generate_complete_horror_story(title, total_parts=parts, model_name=model_name)
        return jsonify({'story': story})
    except Exception as e:
        print(f"Error generating story: {e}")
        return jsonify({'error': f'Gagal membuat cerita: {str(e)}'}), 500

# --- Fungsi untuk GUI Tkinter ---
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def run_flask_server_thread(): # Ganti nama agar lebih jelas ini untuk thread
    """Menjalankan server Flask."""
    global root_window, status_label
    try:
        # Sekarang kita menggunakan instance 'app' Flask yang didefinisikan di file ini
        print(f"Starting Flask server on http://0.0.0.0:{SERVER_PORT}")
        app.run(host='0.0.0.0', port=SERVER_PORT, debug=False, use_reloader=False)
    except Exception as e:
        print(f"Error starting Flask server: {e}")
        if root_window and status_label:
            root_window.after(0, status_label.config, {"text": f"Error: Server gagal dimulai!\n{e}", "fg": "red"})

def open_browser():
    ip_addr = get_local_ip()
    webbrowser.open(f'http://{ip_addr}:{SERVER_PORT}')

def create_main_window():
    global root_window, status_label

    root = tk.Tk()
    root_window = root
    root.title("YouTube Cerita Horor Generator")
    root.geometry("450x250")
    root.configure(bg='#2E2E2E')

    default_font = tkfont.Font(family="Helvetica", size=10)
    title_font = tkfont.Font(family="Helvetica", size=14, weight="bold")
    status_font = tkfont.Font(family="Helvetica", size=9)

    main_frame = tk.Frame(root, bg='#2E2E2E', padx=20, pady=20)
    main_frame.pack(expand=True, fill=tk.BOTH)

    app_title_label = tk.Label(
        main_frame, text="YouTube Cerita Horor Generator", font=title_font,
        bg='#2E2E2E', fg='#00A2FF'
    )
    app_title_label.pack(pady=(0, 20))

    ip_addr = get_local_ip()
    status_text = f"Server berjalan di: http://{ip_addr}:{SERVER_PORT}\nAtur API Key Anda melalui antarmuka web."
    status_label_widget = tk.Label(
        main_frame, text=status_text, font=default_font,
        bg='#2E2E2E', fg='#E0E0E0', justify=tk.CENTER
    )
    status_label_widget.pack(pady=10)
    status_label = status_label_widget

    open_button = tk.Button(
        main_frame, text="Buka di Peramban", command=open_browser, font=default_font,
        bg='#007BFF', fg='white', relief=tk.FLAT, padx=10, pady=5
    )
    open_button.pack(pady=15)

    credit_label = tk.Label(
        main_frame, text="Created by tianoambr", font=status_font,
        bg='#2E2E2E', fg='#888888'
    )
    credit_label.pack(side=tk.BOTTOM, pady=(10,0))

    return root

# --- Main Execution ---
if __name__ == '__main__':
    # Banner akan tercetak jika dijalankan dari konsol
    print_startup_banner()

    # Pastikan direktori yang dibutuhkan oleh Flask ada (jika ada)
    # Contoh:
    # static_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'generated_media')
    # os.makedirs(os.path.join(static_folder, 'audio'), exist_ok=True)
    # ... (sesuaikan dengan kebutuhan aplikasi Anda)

    # Buat dan jalankan thread Flask
    flask_thread = threading.Thread(target=run_flask_server_thread, daemon=True)
    flask_thread.start()

    # Buat dan jalankan GUI Tkinter
    gui_root = create_main_window()
    gui_root.mainloop()
