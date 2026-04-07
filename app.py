from flask import Flask, redirect, url_for, session, request
import msal
import os

app = Flask(__name__)
app.secret_key = "your-secret-key"

print("TENANT_ID:", os.environ.get("TENANT_ID"))

# 🔹 Replace these with YOUR values
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
CLIENT_ID = os.environ.get("CLIENT_ID")
TENANT_ID = os.environ.get("TENANT_ID")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_PATH = "/getAToken"
SCOPE = ["User.Read"]

@app.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return f"<h1>Welcome {session['user']}</h1><p>FileHealth App Running ✅</p>"

@app.route("/login")
def login():
    auth_url = _build_auth_url()
    return redirect(auth_url)

@app.route(REDIRECT_PATH)
def callback():
    code = request.args.get("code")
    result = _get_token_from_code(code)

    if "id_token_claims" in result:
        session["user"] = result["id_token_claims"]["name"]

    return redirect(url_for("home"))

def _build_auth_url():
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET,
    ).get_authorization_request_url(
        SCOPE,
        redirect_uri=request.host_url.replace("http://", "https://") + "getAToken"
    )

def _get_token_from_code(code):
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET,
    ).acquire_token_by_authorization_code(
        code,
        scopes=SCOPE,
        redirect_uri=request.host_url.replace("http://", "https://") + "getAToken"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)