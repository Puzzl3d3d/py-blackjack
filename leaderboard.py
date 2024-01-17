from urllib import request, parse
import json
import os

base_url = "https://flask.puzzl3d.dev"
endpoint = "/blackjack/leaderboard"

username = None

def get_user():
    global username
    if not os.path.exists("session"):
        with open("session", "w") as file:
            username = input("Username: ")
            file.write(username)
    else:
        with open("session", "r") as file:
            username = file.read().split("\n")[0].strip()
    return username

def get():
    try:
        with request.urlopen(base_url + endpoint) as response:
            charset = response.headers.get_content_charset()
            return json.loads(response.read().decode(charset or 'utf-8'))
    except Exception as e:
        return f"An error occurred: {e}"
def update(value):
    query_params = parse.urlencode({'name': username or get_user(), 'value': value})
    req = request.Request(f"{base_url}{endpoint}?{query_params}", method="POST")
    try:
        with request.urlopen(req) as response:
            charset = response.headers.get_content_charset()
            return response.read().decode(charset or 'utf-8')
    except Exception as e:
        return f"An error occurred: {e}"