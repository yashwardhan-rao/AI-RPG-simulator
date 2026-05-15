from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/action", methods=["POST"])
def action():
    data = request.json
    user_message = data.get("action", "").lower()

    if "attack" in user_message:
        reply = "You swing your sword with all your might!"
    elif "look" in user_message:
        reply = "You look around and see a dark, damp cave with a glowing stone in the corner."
    elif "inventory" in user_message:
        reply = "You check your pockets... Empty, except for a bit of lint."
    elif "hello" in user_message or "hi" in user_message:
        reply = "Greetings, traveler! What do you wish to do?"
    else:
        reply = "I don't understand that command. Try 'look', 'attack', or 'inventory'."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)