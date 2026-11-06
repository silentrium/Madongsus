from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re
import os

app = Flask(__name__)
CORS(app) # Cho phép HTML gọi API trực tiếp không bị chặn CORS

@app.route('/extract', methods=['POST'])
def extract_audio():
    data = request.json or {}
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({"success": False, "error": "Vui lòng nhập URL!"})
    
    # Nếu người dùng nhập thẳng link .m4a
    if url.endswith('.m4a'):
        return jsonify({"success": True, "m4a_link": url})

    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        res = requests.get(url, headers=headers, timeout=10)
        
        # Dùng Regex tìm link .m4a trong mã nguồn Soundgasm
        match = re.search(r'https://media\.soundgasm\.net/sounds/[a-zA-Z0-9]+\.m4a', res.text)
        if match:
            return jsonify({"success": True, "m4a_link": match.group(0)})
        else:
            return jsonify({"success": False, "error": "Không tìm thấy file audio .m4a!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    # Chạy server ở máy cá nhân (nếu chạy test local)
    app.run(host='127.0.0.1', port=5000, debug=True)

app = Flask(__name__)
CORS(app)

@app.route('/extract', methods=['POST'])
def extract_audio():
    data = request.json or {}
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({"success": False, "error": "Vui lòng nhập URL!"})
    
    if url.endswith('.m4a'):
        return jsonify({"success": True, "m4a_link": url})

    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        res = requests.get(url, headers=headers, timeout=10)
        match = re.search(r'https://media\.soundgasm\.net/sounds/[a-zA-Z0-9]+\.m4a', res.text)
        if match:
            return jsonify({"success": True, "m4a_link": match.group(0)})
        else:
            return jsonify({"success": False, "error": "Không tìm thấy file audio .m4a!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# API hỗ trợ AI tạo thông tin mô tả nếu thiếu
@app.route('/ai-metadata', methods=['POST'])
def ai_metadata():
    data = request.json or {}
    url = data.get('url', '').strip()
    
    # Có thể tích hợp gọi Groq API ở đây nếu có key, hoặc dùng bộ template chuẩn giả lập AI thông minh
    # Ví dụ khuôn mẫu chuẩn yêu cầu:
    generated_title = "Featured Track - " + ("YouTube Video" if "youtube" in url else "Audio Stream")
    generated_desc = (
        "<b>Artist:</b> Unknown Artist<br>"
        "<b>Duration:</b> 03:30<br>"
        "<b>Description / Lyrics:</b><br>"
        "Auto-generated summary and details for the provided link media content..."
    )
    return jsonify({"success": True, "title": generated_title, "desc": generated_desc})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
