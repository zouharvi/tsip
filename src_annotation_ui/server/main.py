#!/usr/bin/env python3

from pathlib import Path
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
# enable CORS for all routes
CORS(app)

allowed_projects = {"tsip"}


@app.route('/')
def api_hello_world():
    return 'Root endpoint'


@app.route('/read')
def api_read():
    return "Not allowed"
    # with open("logs.txt", "r") as f:
    #     return f.read()


@app.route('/log', methods=['GET', 'POST'])
def api_log():
    if request.content_type != 'application/json':
        return "Invalid content type " + request.content_type

    data = request.get_json()
    if data["project"] not in allowed_projects:
        return "Invalid project"

    # make sure the directory exits
    path_dir = "data/" + data["project"] + "/"
    path_file = path_dir + data["uid"] + ".jsonl"
    Path(path_dir).mkdir(parents=True, exist_ok=True)

    with open(path_file, "a") as f:
        f.write(data["payload"] + "\n")

    return "OK"


app.run()
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5002)
