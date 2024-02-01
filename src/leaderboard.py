from urllib import request, parse
import json
import os
import hashlib # auth

base_url = "https://flask.puzzl3d.dev"
api = "/blackjack"
# if you wanna bomb the api, add "jared_" before it (e.g. "/blackjack/jared_data") please :)
data_endpoint = "/data"
top_endpoint = "/top"
signup_endpoint = "/signup"
updatePass_endpoint = "/update_password"
exists_endpoint = "/user_exists"
hasAuth_endpoint = "/has_auth"

username = None
auth = None

def hash(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()

def has_auth(user):
    query_params = parse.urlencode({'name': user})
    try:
        with request.urlopen(f"{base_url}{api}{hasAuth_endpoint}?{query_params}") as response:
            charset = response.headers.get_content_charset()
            return json.loads(response.read().decode(charset or 'utf-8')).get("auth")
    except Exception as e:
        return False

def user_exists(user):
    query_params = parse.urlencode({'name': user})
    try:
        with request.urlopen(f"{base_url}{api}{exists_endpoint}?{query_params}") as response:
            charset = response.headers.get_content_charset()
            return json.loads(response.read().decode(charset or 'utf-8')).get("exists")
    except Exception as e:
        return True

def signup(user, auth):
    query_params = parse.urlencode({'name': user, 'auth': auth})
    req = request.Request(f"{base_url}{api}{signup_endpoint}?{query_params}", method="POST")
    try:
        with request.urlopen(req) as response:
            charset = response.headers.get_content_charset()
            return response.read().decode(charset or 'utf-8')
    except Exception as e:
        return f"An error occurred: {e}"

def update_auth(user, old_auth, new_auth):
    query_params = parse.urlencode({'name': user, 'auth': old_auth, "new": new_auth})
    req = request.Request(f"{base_url}{api}{updatePass_endpoint}?{query_params}", method="POST")
    try:
        with request.urlopen(req) as response:
            charset = response.headers.get_content_charset()
            return response.read().decode(charset or 'utf-8')
    except Exception as e:
        return f"An error occurred: {e}"

def read_user():
    if not os.path.exists("session"): return None
    with open("session", "r") as file:
        username = file.read().split("\n")[0].strip()
    return username
def write_user(user):
    with open("session", "w") as file:
        file.write(user)
def read_auth():
    if not os.path.exists("auth"): return None
    with open("auth", "r") as file:
        auth = file.read().split("\n")[0].strip()
    return auth
def write_auth(auth):
    with open("auth", "w") as file:
        file.write(auth)


def get_user():
    global username
    global auth

    username = read_user() or input("Username: ")
    auth = read_auth() or hash(input("Password: "))

    write_user(username)
    write_auth(auth)
    
    exists, auth_exists = user_exists(username), has_auth(username)
    if exists and not auth_exists:
        update_auth(username, None, auth)
    elif not exists:
        signup(username,auth)
    
    return username, auth

def get_top():
    try:
        with request.urlopen(f"{base_url}{api}{top_endpoint}") as response:
            charset = response.headers.get_content_charset()
            return json.loads(response.read().decode(charset or 'utf-8'))
    except Exception as e:
        print("ERROR |",e)
        return {}
def get_data():
    try:
        with request.urlopen(f"{base_url}{api}{data_endpoint}") as response:
            charset = response.headers.get_content_charset()
            return json.loads(response.read().decode(charset or 'utf-8'))
    except Exception as e:
        return {}
def get_self_data():
    query_params = parse.urlencode({'name': username or get_user()})
    try:
        with request.urlopen(f"{base_url}{api}{data_endpoint}?{query_params}") as response:
            charset = response.headers.get_content_charset()
            return json.loads(response.read().decode(charset or 'utf-8'))
    except Exception as e:
        return {}
def update(value):
    query_params = parse.urlencode({'name': username or get_user(), 'value': value, 'auth': auth})
    req = request.Request(f"{base_url}{api}{data_endpoint}?{query_params}", method="POST")
    try:
        with request.urlopen(req) as response:
            charset = response.headers.get_content_charset()
            return response.read().decode(charset or 'utf-8')
    except Exception as e:
        return f"An error occurred: {e}"
def ordinal_suffix(position):
    position = int(position)
    if 10 <= position % 100 <= 20:
        suffix = 'th'
    else:
        suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
        suffix = suffixes.get(position % 10, 'th')
    return f"{position}{suffix}"
