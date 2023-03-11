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

@app.route('/databases', methods=['GET'])
def databases():

    client = FaunaClient(secret=FAUNA_SECRET)

    try:
        result = client.query(
            q.map_(
                q.lambda_("ref", q.get(q.var("ref"))),
                q.paginate(q.documents(q.collection("Databases")))
            )
        )

        databases = map(
            lambda doc: {
                "id": doc["ref"].id(),
                "name": doc["data"]["name"],
                "id": doc["data"]["id"],
                "url": doc["data"]["url"],
                "last_scraped": doc["data"]["last_scraped"]
            },
            result["data"]
        )

        return {
            "databases": list(databases)
        }

    except faunadb.errors.Unauthorized as exception:
        error = exception.errors[0]
        return {
            "code": error.code,
            "description": error.description
        }, 401

app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))

