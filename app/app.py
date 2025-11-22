from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello from the backend app (behind NGINX WAF)!\n"


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/echo")
def echo():
    q = request.args.get("q", "")
    return jsonify(message="Echo endpoint", query=q)


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    return jsonify(message="Login received", username=username, password_length=len(password))
