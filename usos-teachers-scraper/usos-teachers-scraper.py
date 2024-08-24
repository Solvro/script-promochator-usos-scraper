from flask import Flask, request, redirect, session, jsonify
from rauth import OAuth1Service
import json, os

with open("config.json", "r") as config_file:
    config = json.load(config_file)

    app = Flask(__name__)
    app.secret_key = config["secret_key"]

    usos = OAuth1Service(
        name="usos",
        consumer_key=config["consumer_key"],
        consumer_secret=config["consumer_secret"],
        request_token_url="https://apps.usos.pwr.edu.pl/services/oauth/request_token",
        access_token_url="https://apps.usos.pwr.edu.pl/services/oauth/access_token",
        authorize_url="https://apps.usos.pwr.edu.pl/services/oauth/authorize",
        base_url="https://apps.usos.pwr.edu.pl/",
    )


@app.route("/start_oauth")
def start_oauth():
    request_token, request_token_secret = usos.get_request_token(
        method="POST", params={"oauth_callback": "http://127.0.0.1:5000/oauth_callback"}
    )
    session["request_token"] = request_token
    session["request_token_secret"] = request_token_secret
    return redirect(usos.get_authorize_url(request_token))


@app.route("/oauth_callback")
def oauth_callback():
    request_token = session.get("request_token")
    request_token_secret = session.get("request_token_secret")
    oauth_verifier = request.args.get("oauth_verifier")

    if not request_token or not request_token_secret:
        return "Session expired or invalid request. Please start over.", 400

    access_token, access_token_secret = usos.get_access_token(
        request_token,
        request_token_secret,
        method="POST",
        data={"oauth_verifier": oauth_verifier},
    )

    session.pop("request_token", None)
    session.pop("request_token_secret", None)

    session["access_token"] = access_token
    session["access_token_secret"] = access_token_secret

    return f"Access token received! Token: {access_token}"


def check_faculty_id(session_oauth, base_url, faculty_id):
    params = {
        "fac_ids": faculty_id,
        "teachers_only": "true",
        "fields": "users[id|first_name|last_name|titles]",
        "num": "1",
        "start": "0",
        "format": "json",
    }
    response = session_oauth.get(base_url, params=params)
    if response.status_code == 200 and response.json().get("users"):
        return True
    return False


@app.route("/fetch_staff")
def fetch_staff():
    access_token = session.get("access_token")
    if not access_token:
        return "Access token is missing. Please authenticate first.", 403

    session_oauth = usos.get_session((access_token, session.get("access_token_secret")))
    base_url = "https://apps.usos.pwr.edu.pl/services/users/staff_index"

    faculties = [
        f"W{i}N" if check_faculty_id(session_oauth, base_url, f"W{i}N") else f"W{i}"
        for i in range(1, 15)
    ]

    results = []

    folder = "teachers_data"

    os.makedirs(folder, exist_ok=True)

    for faculty in faculties:
        all_data = []
        start = 0

        while True:
            params = {
                "fac_ids": faculty,
                "teachers_only": "true",
                "fields": "users[id|first_name|last_name|titles]|next_page|total",
                "num": "100",
                "start": str(start),
                "format": "json",
            }
            response = session_oauth.get(base_url, params=params)
            if response.status_code == 200:
                data = response.json()
                all_data.extend(data["users"])

                if data.get("next_page"):
                    start += 100
                else:
                    break
            else:
                return f"Failed to fetch data for {faculty}: {response.status_code}"

        file_path = os.path.join(folder, f"{faculty}_teachers_data.json")

        with open(file_path, "w") as file:
            json.dump(all_data, file, indent=6)
            results.append(f"Data for {faculty} saved.")

    return jsonify(results)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
