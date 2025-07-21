from flask import Flask, request, jsonify
from flask_cors import CORS
from random_loadout import RandomLoadout
import os

app = Flask(__name__)
CORS(app)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# Vercel部署需要这个
app.debug = True 