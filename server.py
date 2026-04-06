from flask import Flask, request, jsonify
import os

app = Flask(__name__)

banned_users = set()
kicked_users = {}  # userId: reason

# 🔨 BAN
@app.route("/ban", methods=["POST"])
def ban():
    data = request.json
    user_id = data.get("userId")

    banned_users.add(user_id)
    return jsonify({"success": True})

# 🔓 UNBAN
@app.route("/unban", methods=["POST"])
def unban():
    data = request.json
    user_id = data.get("userId")

    banned_users.discard(user_id)
    return jsonify({"success": True})

# 👢 KICK (temporal)
@app.route("/kick", methods=["POST"])
def kick():
    data = request.json
    user_id = data.get("userId")
    reason = data.get("reason", "No reason")

    kicked_users[user_id] = reason
    return jsonify({"success": True})

# 🔍 CHECK (🔥 FIX DEL KICK)
@app.route("/check/<int:user_id>", methods=["GET"])
def check(user_id):
    is_kicked = user_id in kicked_users
    reason = kicked_users.get(user_id)

    # 🔥 CLAVE: borrar el kick después de usarlo
    if is_kicked:
        del kicked_users[user_id]

    return jsonify({
        "banned": user_id in banned_users,
        "kicked": is_kicked,
        "kickReason": reason
    })

# 🚀 RUN (Render compatible)
port = int(os.environ.get("PORT", 3000))
app.run(host="0.0.0.0", port=port)
