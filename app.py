import os
import json
from flask import Flask, render_template, request, jsonify 
from dotenv import load_dotenv
from models import db, GameSession

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY','default-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rpg.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


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