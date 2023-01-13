#!/usr/bin/env python3
# version v1.0.0
import json
from json_schema_validator import get_json_from_file
from SPARQLWrapper import SPARQLWrapper, JSON
from iteration_utilities import unique_everseen

organ_query = """
PREFIX inSubset: <http://www.geneontology.org/formats/oboInOwl#inSubset>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT  ?x ?xLabel
WHERE 
{
      ?x inSubset: 	<http://purl.obolibrary.org/obo/uberon#cap_organ_slim> .
      ?x rdfs:label ?xLabel 
}
    """
sparql = SPARQLWrapper(
    "http://localhost:8080/rdf4j-server/repositories/cap"
)
sparql.setReturnFormat(JSON)
sparql.setQuery(organ_query)
ret = sparql.queryAndConvert()

query_output = []
for line in ret["results"]["bindings"]:
    label = line["xLabel"]["value"].capitalize()
    if label not in query_output:
        query_output.append(label)

json_file = "../src/config/contextual_search_logic.json"
contextual_search_dict = get_json_from_file(json_file)

for item in contextual_search_dict:
    if item["Source_field_name"] != "Organ" or item["Target_field_name"] != "Cell_type":
        continue
    for organ in query_output:
        item["Context_map"].append(
            {
                'Source_field_tag': organ.replace(" ", "_"),
                'Target_field_tag': [organ.replace(" ", "_")],
                'Effect': 'boost'
            })
    item["Context_map"] = list(unique_everseen(item["Context_map"]))
with open(json_file, "w") as outfile:
    json.dump(contextual_search_dict, outfile, indent=2)
