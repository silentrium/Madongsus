from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re

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