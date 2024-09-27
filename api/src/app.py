import os
from flask import Flask, Blueprint
from restplus import api
from endpoints.ontology_service import ns as api_namespace
from config.search_config import solr_config as config
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Get URL prefix from environment variable or use root ('/') by default
url_prefix = os.environ.get("OBASK_URL_PREFIX", "")
if not url_prefix:  # if empty, set to root '/'
    url_prefix = "/"

blueprint = Blueprint("obask", __name__, url_prefix=url_prefix)


def initialize_app(flask_app):
    api.init_app(blueprint)
    api.add_namespace(api_namespace)
    flask_app.register_blueprint(blueprint)


def main():
    initialize_app(app)
    app.run(
        host=config["web_expose_hostname"],
        port=int(config["web_expose_port"]),
        debug=False if config["python_env"] == "production" else True,
    )


if __name__ == "__main__":
    main()
