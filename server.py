from flask import Flask, request, jsonify

app = Flask(__name__)

# 📦 Lista de baneados (temporal)
banned_users = []

# 🔨 Banear usuario
@app.route("/ban", methods=["POST"])
def ban():
    data = request.json
    user_id = data.get("userId")

    if user_id not in banned_users:
        banned_users.append(user_id)

    print("Baneado:", user_id)

    return jsonify({"success": True})

# 🔍 Verificar si está baneado
@app.route("/check/<int:user_id>", methods=["GET"])
def check(user_id):
    return jsonify({
        "banned": user_id in banned_users
    })

# 🚀 Iniciar servidor
import os

port = int(os.environ.get("PORT", 3000))
app.run(host="0.0.0.0", port=port)
