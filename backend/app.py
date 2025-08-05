from flask import Flask, request, jsonify
from flask_cors import CORS
from random_loadout import RandomLoadout
import os
import requests

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "https://xdzs-chou.github.io"}}, allow_headers="*", methods=["GET", "POST", "OPTIONS"])

def get_cookie_from_file():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'cookie.txt'), 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception:
        return ''

@app.route('/api/gun_solution_loadout', methods=['POST', 'OPTIONS'])
def gun_solution_loadout():
    if request.method == 'OPTIONS':
        return '', 204
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
        "iChartId": "316969",
        "iSubChartId": "316969", 
        "sIdeToken": "NoOapI",
        "method": "dfm/center.day.secret",
        "source": "2",
        "param": "{}"
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;',
        'Cookie': 'openid=oA2F77Y62VZgXZzWJnokI_XWgLso; acctype=mini; appid=wx1c36464bbea2507a; ieg_ams_session_token=70fedda1bbbf49c4fb9b9efc1e253a37058d48637411a33bc59f7301f0b6d570ea89; ieg_ams_token=38d08229b8c3d4788b983d524c4129da; ieg_ams_token_time=1754454110; ieg_ams_token_v2=b0d4ffb400bf18d3c42ebcd397f72b4b; unionid=null;'
    }
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10, verify=False)
        print("腾讯接口返回：", response.text)
        if response.status_code == 200:
            data = response.json()
            # 新接口解析逻辑
            try:
                secret_list = data["jData"]["data"]["data"]["list"]
                # 格式化为旧格式：零号大坝:5703;长弓溪谷:5754;...
                formatted_secrets = []
                for item in secret_list:
                    map_name = item.get("mapName", "")
                    secret = item.get("secret", "")
                    if map_name and secret:
                        formatted_secrets.append(f"{map_name}:{secret}")
                desc = ";".join(formatted_secrets)
                return jsonify({"desc": desc})
            except Exception as e:
                return jsonify({"error": f"解析desc失败: {str(e)}"}), 500
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