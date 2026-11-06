from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re
from groq import Groq

app = Flask(__name__)
CORS(app) # Cho phép gọi API trực tiếp không bị chặn CORS

# Khởi tạo client Groq (Bro nhớ thay API Key thực tế vào đây hoặc dùng biến môi trường os.environ.get("GROQ_API_KEY"))
client = Groq(api_key="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")

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

# API hỗ trợ AI tạo thông tin mô tả thực tế bằng Groq
@app.route('/ai-metadata', methods=['POST'])
def ai_metadata():
    data = request.json or {}
    url = data.get('url', '').strip()
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Hãy viết thông tin mô tả cho link audio/video này: {url}. Với định dạng mẫu là
                    Artist: [Tên artist]
                    Duration: [Link youtube này có thời lượng là bao nhiêu]
                    Lyrics: [Một vài dòng lyrics đầu]
                    Trả về đúng định dạng HTML gồm Artist, Duration, và một vài dòng Lyrics mẫu bằng thẻ <b>, <br>.",
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        ai_text = chat_completion.choices[0].message.content
        return jsonify({"success": True, "title": "AI Generated Track", "desc": ai_text})
    except Exception as e:
        # Fallback nếu lỗi API Key hoặc mạng
        fallback_desc = (
            "<b>Artist:</b> Unknown Artist<br>"
            "<b>Duration:</b> 03:30<br>"
            "<b>Description / Lyrics:</b><br>"
            f"Auto-generated details for: {url}"
        )
        return jsonify({"success": True, "title": "Featured Track", "desc": fallback_desc})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
