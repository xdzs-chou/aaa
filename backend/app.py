from flask import Flask, request, jsonify
from flask_cors import CORS
from random_loadout import RandomLoadout
import os
import requests

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "https://xdzs-chou.github.io"}})

def get_cookie_from_file():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'cookie.txt'), 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception:
        return ''

@app.route('/api/gun_solution_loadout', methods=['POST'])
def gun_solution_loadout():
    cookie = request.json.get('cookie', '') or get_cookie_from_file()
    rl = RandomLoadout(cookie)
    result = rl.generate_gun_solution_loadout()
    return jsonify(result)

@app.route('/api/daily_secret', methods=['POST', 'OPTIONS'])
def daily_secret():
    if request.method == 'OPTIONS':
        return '', 200
    url = "https://comm.ams.game.qq.com/ide/"
    payload = {
        "iChartId": "384918",
        "iSubChartId": "384918",
        "sIdeToken": "mbq5GZ",
        "method": "dist.contents",
        "param": '{"distType":"bannerManage","contentType":"secretDay"}'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;',
        'Cookie': 'openid=D7AF10F0E80DD74A6844FB54A131C95D; acctype=qc; appid=101491592; access_token=57C57406873816CC7BA6C46708C36150'
    }
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10, verify=False)
        print("腾讯接口返回：", response.text)
        if response.status_code == 200:
            data = response.json()
            # 取出 desc 字段
            desc = None
            try:
                desc = data["jData"]["data"]["data"]["content"]["secretDay"]["data"][0]["desc"]
            except Exception as e:
                return jsonify({"error": f"解析desc失败: {str(e)}"}), 500
            return jsonify({"desc": desc})
        else:
            return jsonify({"error": f"请求失败，状态码: {response.status_code}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/gun_solution_detail', methods=['POST'])
def gun_solution_detail():
    code = request.json.get('solution_code')
    cookie = request.json.get('cookie', '') or get_cookie_from_file()
    rl = RandomLoadout(cookie)
    result = rl.get_gun_solution_by_code(code)
    return jsonify(result)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000) 