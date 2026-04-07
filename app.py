from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return {"status": "Phase 1 complete", "vm": "running in private VNet - Central_India_New"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)