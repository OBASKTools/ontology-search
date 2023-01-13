import sys
sys.path.insert(0, '../../src')
from app import initialize_app, app as flask_app
from endpoints.ontology_service import generate_suggest_request, concat_with_and, add_highlight, config_lookup, add_cors_headers
from typing import Dict, List

initialize_app(flask_app)

expected_healthcheck_response: Dict[str, str] = {"message": "ok"}
expected_config_response: Dict[str, List[str]] = {"boost": ["Common_species"], "filter": ["Metazoan", "Species"]}
expected_config_dict: Dict[str, List[str]] = {"boost": ["Mammalia", "Kidney"], "filter": ["Cell"]}


query_param = "mus%20musculus"
filter_param = ["metazoan", "species"]
boost_param = ["common_species"]
target_field = "Cell_type"
source_tag = ["Mammalia", "Kidney"]


def test_healthcheck_endpoint(client):
    res = client.get("/ontology/api/healthcheck")
    assert res.status_code == 200
    assert res.content_type == "application/json"
    assert expected_healthcheck_response == res.get_json()


def test_config_endpoint(client):
    res = client.get("/ontology/api/config?target_field=Organism")
    assert res.status_code == 200
    assert res.content_type == "application/json"
    assert expected_config_response == res.get_json()


def test_generate_suggest_request():
    solr_query = generate_suggest_request(query_param, filter_param, boost_param, None)
    assert any(item in solr_query for item in ["&q", "&qf", "&fq",  "&bq", "&hl"])


def test_concat_with_and():
    concat = concat_with_and(filter_param)
    assert "AND" in concat
    assert len(concat) == 22


def test_add_highlight():
    solr_url = add_highlight("")
    assert len(solr_url) == 134


def test_config_lookup():
    config_dict = config_lookup(target_field, source_tag)
    assert config_dict == expected_config_dict
