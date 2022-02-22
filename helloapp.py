from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "App is Up"

app.run(port=5000)