from flask import Flask, request, jsonify
import os

app = Flask(__name__)

banned_users = set()
kicked_users = {}  # userId: reason

@app.route("/ban", methods=["POST"])
def ban():
    data = request.json
    user_id = data.get("userId")

    banned_users.add(user_id)
    return jsonify({"success": True})

@app.route("/unban", methods=["POST"])
def unban():
    data = request.json
    user_id = data.get("userId")

    banned_users.discard(user_id)
    return jsonify({"success": True})

@app.route("/kick", methods=["POST"])
def kick():
    data = request.json
    user_id = data.get("userId")
    reason = data.get("reason", "No reason")

    kicked_users[user_id] = reason
    return jsonify({"success": True})

@app.route("/check/<int:user_id>", methods=["GET"])
def check(user_id):
    return jsonify({
        "banned": user_id in banned_users,
        "kicked": user_id in kicked_users,
        "kickReason": kicked_users.get(user_id)
    })

port = int(os.environ.get("PORT", 3000))
app.run(host="0.0.0.0", port=port)
