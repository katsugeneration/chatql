# coding=utf-8
#
# Licensed under the MIT License
"""ChatQL demo server."""
from flask import Flask
from flask_graphql import GraphQLView
import chatql


class GraphQLViewCustom(GraphQLView):
    def get_context(self):
        global engine
        return {"engine": engine}


app = Flask(__name__)
app.debug = True

client = chatql.mongodb_client.MongoClient(**{"db": "chatql"})
engine = chatql.engine.DialogEngine(client)
client.import_scenario("scenario.json")

app.add_url_rule(
    '/graphql',
    view_func=GraphQLViewCustom.as_view(
        'graphql',
        schema=chatql.schema,
        graphiql=True  # for having the GraphiQL interface
    )
)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
