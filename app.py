from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "The Game Engine is Warming up"

if __name__ == "__main__":
    app.run(debug=True)