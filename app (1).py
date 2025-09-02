
from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
SCORES_FILE = "scores.json"

def load_scores():
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_scores(scores):
    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2)

@app.route("/save_score", methods=["POST"])
def save_score():
    data = request.get_json()
    name = data.get("name")
    score = data.get("score")
    if name and isinstance(score, int):
        scores = load_scores()
        scores.append({"name": name, "score": score})
        save_scores(scores)
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error", "message": "Invalid data"}), 400

@app.route("/scores.json", methods=["GET"])
def get_scores():
    scores = load_scores()
    scores.sort(key=lambda x: x["score"], reverse=True)
    return jsonify(scores)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
