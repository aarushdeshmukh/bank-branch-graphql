"""
Bank Branches GraphQL API
A GraphQL API service for querying Indian bank branch information.
"""

from flask import Flask
from flask_graphql import GraphQLView
from flask_cors import CORS
from schema import schema
from database import init_db

app = Flask(__name__)
CORS(app)

# To initialize database on first run.
init_db()

# GraphQL endpoint
app.add_url_rule(
    '/gql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # Enable GraphiQL intrface for testing
    )
)

@app.route('/')
def home():
    """Health check endpoint"""
    return {
        "status": "running",
        "message": "Bank Branches GraphQL API",
        "endpoints": {
            "graphql": "/gql",
            "graphiql": "/gql (visit in browser)"
        }
    }

@app.route('/health')
def health():
    """Health check for deployment services"""
    return {"status": "healthy"}, 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
