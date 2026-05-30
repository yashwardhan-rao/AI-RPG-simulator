import os
import json
from flask import Flask, render_template, request, jsonify, Response, stream_with_context
import engine
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
    user_message = data.get("action", "")

    session = GameSession.query.first()
    if not session:
        session = GameSession()
        db.session.add(session)
        db.session.commit()
    
    history = json.loads(session.history_json)

    def generate():
        ai_full_response = ""
        try:
            response_stream = engine.get_gemini_stream(history, user_message)

            for chunk in response_stream:
                if chunk.text:
                    ai_full_response += chunk.text
                    yield f"data: {json.dumps({'chunk': chunk.text})}\n\n"

            history.append({"role": "user", "parts":[user_message]})
            history.append({"role":"model","parts":[ai_full_response]})

            session.history_json = json.dumps(history)
            db.session.commit()

        except Exception as e:
            print(f"Error: {e}")
            yield f"data:{json.dumps({'error':'The Game Master encountered an error.'})}\n\n"

    return Response(stream_with_context(generate()), mimetype='text/event-stream')        
if __name__ == "__main__":
    app.run(debug=True)