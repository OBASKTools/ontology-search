import ast
import copy
import logging
from typing import Dict, List
from flask import request, jsonify
import requests
from flask_restx import Resource
from restplus import api
from config.search_config import solr_config, suggest_query_config, cell_type_query_config
from config.inter_field_boosting_config import inter_field_config
from config.contextual_search_config import contextual_search_config
from endpoints.parser import suggest_arguments, config_arguments, wrapper_arguments, cell_type_check_arguments
from endpoints.serializers import metadata

ns = api.namespace('api', description='Cell Annotation Platform Ontology API')

log = logging.getLogger(__name__)


@ns.route('/healthcheck', methods=['GET'])
class HealthcheckEndpoint(Resource):

    @api.expect(validate=False)
    def get(self):
        result_dict: Dict[str, str] = {
            "message": "ok"
        }
        return result_dict


@ns.route('/suggest', methods=['GET'])
class SuggestEndpoint(Resource):

    @api.expect(suggest_arguments, validate=False)
    def get(self):
        """
        Search service wrapper for Solr.

        * <b>query</b> (mandatory): search terms

        * <b>filter</b> (optional): Semantic tags for query filtering

        * <b>boost</b> (optional): Semantic tags for query boosting

        * <b>curie</b> (optional): Compact uniform resource identifier, used for dynamic boosting. i.e. UBERON:0002113

        """
        # Service parameters
        args = suggest_arguments.parse_args()
        query_variable = args.get('query')
        filtering_variable = args.get('filter')
        boosting_variable = args.get('boost')
        curie_variable = args.get('curie')
        # Generate SOLR query
        request_url = generate_suggest_request(query_variable, filtering_variable, boosting_variable, curie_variable)
        log.warning('Request: ' + request_url)
        response = requests.get(request_url)
        add_cors_headers(response)
        return jsonify(response.json())


@ns.route('/suggest/v2')
@api.expect(wrapper_arguments, validate=False)
@api.param('query', 'Search terms', type=str, required=True)
@api.param('target_field', 'Location of where the suggest request will be made', type=str, required=True)
class WrappedSuggestEndpoint(Resource):

    @api.expect(metadata, validate=False)
    def post(self):
        """
        Wrapper service to wrap config and suggest endpoint.

        * <b>query</b> (mandatory): search terms

        * <b>target_field</b> (mandatory): Location of where the suggest request will be made

        """
        # Retrieve filtering and boosting parameters
        args = wrapper_arguments.parse_args()
        target_field = args.get('target_field')
        query_variable = args.get('query')
        config_dict = config_lookup_with_body(target_field, request.json)
        log.info(config_dict)
        # Generate SOLR query
        # TODO Curie parameter will be removed after the integration
        request_url = generate_suggest_request(query_variable, config_dict.get('filter'), config_dict.get('boost'), None)
        log.warning('Request: ' + request_url)
        # Handle the Solr request
        response = requests.get(request_url)
        add_cors_headers(response)
        return jsonify(response.json())

    @api.expect(wrapper_arguments, validate=False)
    def get(self):
        """
        Wrapper service to wrap config and suggest endpoint.

        * <b>query</b> (mandatory): search terms

        * <b>target_field</b> (mandatory): Location of where the suggest request will be made

        * <b>source_tag</b> (optional): The semantic tag of the element which the request is made depends on.

        """
        # Retrieve filtering and boosting parameters
        args = wrapper_arguments.parse_args()
        target_field = args.get('target_field')
        query_variable = args.get('query')
        source_tags = args.get('source_tags')
        config_dict = config_lookup(target_field, source_tags)
        # Generate SOLR query
        # TODO Curie parameter will be removed after the integration
        request_url = generate_suggest_request(query_variable, config_dict.get('filter'), config_dict.get('boost'), None)
        log.warning('Request: ' + request_url)
        # Handle the Solr request
        response = requests.get(request_url)
        add_cors_headers(response)
        return jsonify(response.json())


@ns.route('/config', methods=['GET'])
class ConfigEndpoint(Resource):

    @api.expect(config_arguments, validate=False)
    def get(self):
        """
        Configuration look-up service to retrieve filter and boost parameters for /suggest service.

        * <b>target_field</b> (mandatory): Location of where the suggest request will be made

        * <b>source_tag</b> (optional): The semantic tag of the element which the request is made depends on

        """
        args = config_arguments.parse_args()
        target_field = args.get('target_field')
        source_tags = args.get('source_tags')
        return config_lookup(target_field, source_tags)


@ns.route('/cell_type_check', methods=['GET'])
class CellTypeCheck(Resource):

    @api.expect(cell_type_check_arguments, validate=True)
    def get(self):
        """
        Cell type lookup service to check whether the given cell type exists in the CL.

        * <b>cell_type</b> (mandatory): Input cell type

        """
        # Service parameters
        args = cell_type_check_arguments.parse_args()
        cell_type = args.get('cell_type')
        # Generate SOLR query
        request_url = generate_cell_lookup_request(cell_type)
        log.warning('Request: ' + request_url)
        response = requests.get(request_url)
        add_cors_headers(response)
        return parse_cell_type_response(response.json(), cell_type)


# TODO Curie parameter will be removed after the integration
def generate_suggest_request(query_variable: str, filtering_variable: List[str], boosting_variable: List[str],
                             curie_variable: str) -> str:
    request_url = 'http://{host}:{port}/solr/{collection}/select?defType=edismax&fl=*,score&indent=true'. \
        format(host=solr_config['solr_host'], port=solr_config['solr_port'],
               collection=solr_config['solr_collection'])

    # Filtering process
    if filtering_variable:
        request_url += '&fq=facets_annotation:' + concat_with_and(filtering_variable)

    # Boosting process
    if curie_variable and curie_variable in inter_field_config:
        # Boosting with inter field dependency configuration
        request_url += '&bq=facets_annotation:' + inter_field_config[curie_variable]
    else:
        # Boosting with given parameters
        if boosting_variable:
            request_url += '&bq=facets_annotation:' + concat_with_and(boosting_variable)

    request_url += '&q=' + query_variable
    request_url += '&qf=' + ' '.join(get_config_list(suggest_query_config, 'qf_weight_schema'))
    request_url = add_highlight(request_url)
    
    return request_url


def config_lookup_with_body(target_field: str, request_body: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """ Looks-up for filtering and boosting parameters that will be used for suggest service. Parameters depend on given
    'target_field' and 'source_tag' parameters of config service

    Args:
        target_field (str): Location of where the suggest request will be made.
        request_body (Dict[str, List[str]]): Request body that contains metadata field tags that are inputted so far

    Returns:
        Dict[str, List[str]]: Returns a dict that contains filtering and boosting parameters if there are any
    """
    result_dict: Dict[str, List[str]] = {}
    for metadata_field, metadata_value in request_body.items():
        for item in contextual_search_config:
            if target_field != item.get("Target_field_name").lower() or \
                    metadata_field != item.get("Source_field_name").lower():
                continue
            for context in item.get("Context_map"):
                if context.get("Source_field_tag") and context.get("Source_field_tag") \
                        not in capitalize_and_concatenate_tags(metadata_value):
                    continue
                if result_dict.get(context.get("Effect")):
                    result_dict.get(context.get("Effect")).extend(context.get("Target_field_tag"))
                else:
                    result_dict.update(
                        {context.get("Effect"): copy.deepcopy(context.get("Target_field_tag"))})
    return result_dict


def config_lookup(target_field: str, source_tags: List[str]) -> Dict[str, List[str]]:
    """ Looks-up for filtering and boosting parameters that will be used for suggest service. Parameters depend on given
    'target_field' and 'source_tag' parameters of config service

    Args:
        target_field (str): Location of where the suggest request will be made.
        source_tags (List[str}): The semantic tag of the element which the request is made depends on

    Returns:
        Dict[str, List[str]]: Returns a dict that contains filtering and boosting parameters if there are any
    """
    result_dict: Dict[str, List[str]] = {}
    for item in contextual_search_config:
        if target_field != item.get("Target_field_name"):
            continue
        for context in item.get("Context_map"):
            for tag in capitalize_and_concatenate_tags(source_tags):
                if tag != context.get("Source_field_tag") \
                        and context.get("Source_field_tag"):
                    continue
                if result_dict.get(context.get("Effect")) and \
                        not (all(item in result_dict.get(context.get("Effect"))
                                 for item in context.get("Target_field_tag"))):
                    result_dict.get(context.get("Effect")).extend(context.get("Target_field_tag"))
                elif not result_dict.get(context.get("Effect")):
                    result_dict.update(
                        {context.get("Effect"): copy.deepcopy(context.get("Target_field_tag"))})
    return result_dict


def generate_cell_lookup_request(cell_type: str):
    """ Generates a Solr query to make a cell type lookup against CL

    Args:
        cell_type (str): Inputted cell type

    Returns:
        str: Returns a Solr query
    """
    cell_filter = ['animal_cell']
    request_url = 'http://{host}:{port}/solr/{collection}/select?defType=edismax&fl=*,score&indent=true'. \
        format(host=solr_config['solr_host'], port=solr_config['solr_port'],
               collection=solr_config['solr_collection'])
    request_url += '&fq=facets_annotation:' + concat_with_and(cell_filter)
    request_url += '&q=' + cell_type
    request_url += '&qf=' + ' '.join(get_config_list(cell_type_query_config, 'qf_weight_schema'))
    return request_url


def check_cell_type_response(response: Dict):
    return response['response']['numFound'] != 0


def parse_cell_type_response(response: Dict, cell_type: str):
    parsed_response = {}
    for term in response['response']['docs']:
        parsed_response.update({term['iri'][0]: term['label'][0]})
        # Exact matches will always be top result. Stop adding new items when an exact matches found.
        if cell_type.lower() == term['label'][0]:
            break
    return parsed_response


def concat_with_and(param_list):
    return '(' + ' AND '.join(param_list) + ')'


def add_highlight(request_url):
    request_url += '&hl=true'
    request_url += '&hl.preserveMulti=true'
    request_url += '&hl.simple.pre=<b>'
    request_url += '&hl.simple.post=</b>'
    request_url += '&hl.fragsize=120'
    request_url += '&hl.fl=label,synonym_hasExactSynonym_autosuggest_e'
    return request_url


def add_cors_headers(response):
    """
    Adds cross origin request support.
    """
    headers = response.headers
    headers['Access-Control-Allow-Origin'] = '*'


def get_config_list(config, name):
    """
    Reads configuration list in string format, and parses value to list.
    """
    parsed = ast.literal_eval(config[name])
    return [item.strip() for item in parsed]


def capitalize_and_concatenate_tags(tag_list: List[str]) -> List[str]:
    """
    Capitalize and concatenate given tags in the list.
    Args:
        tag_list (List[str]tr): Semantic tag list used in contextual search

    Returns (List[str]): Capitalized and concatenated version of given tag list

    """
    return [tag.replace(" ", "_").capitalize() for tag in tag_list]
