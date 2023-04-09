import logging
from http import HTTPStatus

from flask import url_for
from flask_restx import Api, cors
from config.search_config import solr_config
from exception.api_exception import CAPApiException

log = logging.getLogger(__name__)


class OntologyApi(Api):
    @property
    def specs_url(self):
        """Monkey patch for HTTPS"""
        scheme = 'https' if solr_config['python_env'] == 'production' else 'http'
        return url_for(self.endpoint('specs'), _external=True, _scheme=scheme)


api = OntologyApi(version='0.0.1', title='OBASK Ontology RESTFUL API',
                  description='Ontology Based Application Starter Kit, Ontology restful API that wraps SOLR search.',
                  environ='development')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    return {'message': message}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.errorhandler(CAPApiException)
def handle_bad_request(error):
    log.exception(error.message)

    return {'message': error.message}, error.status_code


@api.errorhandler(ValueError)
def handle_value_error(error):
    log.exception(str(error))

    return {'message': str(error)}, HTTPStatus.BAD_REQUEST
