import os
import configparser
import logging
import coloredlogs


# By default the install() function installs a handler on the root logger,
# this means that log messages from your code and log messages from the
# libraries that you use will all show up on the terminal.
coloredlogs.install(level='debug') # un-hardcode log_level

# # Create a logger object.
# logger = logging.getLogger(__name__)

# # If you don't want to see log messages from libraries, you can pass a
# # specific logger object to the install() function. In this case only log
# # messages originating from that logger will show up on the terminal.
# coloredlogs.install(level=log_level, logger=logger)

SEARCH_CONF_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "search_config.ini"
)

log = logging.getLogger(__name__)


def get_config():
    conf = configparser.ConfigParser()
    conf.read(SEARCH_CONF_PATH)
    log.info("conf path: " + SEARCH_CONF_PATH)

    if "PYTHON_ENV" in os.environ:
        conf["DEFAULT"]['python_env'] = os.environ["PYTHON_ENV"]
    else:
        conf["DEFAULT"]['python_env'] = 'development'

    if "SOLR_HOST" in os.environ:
        conf["DEFAULT"]["solr_host"] = os.environ["SOLR_HOST"]
    if "SOLR_PORT" in os.environ:
        conf["DEFAULT"]["solr_port"] = os.environ["SOLR_PORT"]
    if "SOLR_COLLECTION" in os.environ:
        conf["DEFAULT"]["solr_collection"] = os.environ["SOLR_COLLECTION"]
    if "WEB_EXPOSE_HOSTNAME" in os.environ:
        conf["DEFAULT"]["web_expose_hostname"] = os.environ["WEB_EXPOSE_HOSTNAME"]
    if "WEB_EXPOSE_PORT" in os.environ:
        conf["DEFAULT"]["web_expose_port"] = os.environ["WEB_EXPOSE_PORT"]

    return conf


solr_config = get_config()["DEFAULT"]
suggest_query_config = get_config()["Suggest_Query"]
cell_type_query_config = get_config()["Cell_Type_Query"]
