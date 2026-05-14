from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/action", methods=["POST"])
def action():
    data = request.json
    user_message = data.get("action", "")

    return jsonify({"reply": f"Python received: {user_message}"})

if __name__ == "__main__":
    app.run(debug=True)