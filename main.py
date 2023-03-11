import os
FAUNA_SECRET = os.environ.get('FAUNA_SECRET')

import flask
from flask import request

import faunadb
from faunadb import query as q
from faunadb.client import FaunaClient

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/test', methods=['GET'])
def test():

    # body = request.json
    # client = FaunaClient(secret=FAUNA_SECRET)

    return {
        "message": "Hello World"
    }


app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))

