from flask import Flask
from prometheus_client import Counter, generate_latest
from flask import Response

app = Flask(__name__)

REQUESTS = Counter('app_requests_total', 'Total requests')

@app.route("/")
def home():
    REQUESTS.inc()
    return "BLUE APP"

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype="text/plain")

app.run(host="0.0.0.0", port=8000)