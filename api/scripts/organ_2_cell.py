#!/usr/bin/env python3
# organ_2_cell.py v1.0.0

# ACTION:
#  As part of generation of YAML config for organ_cell semantic tags, generate a dictionary YAML file of
#  organ_id: semantic_tag. Semantic tag name is set in YAML config.

import sys
import ruamel.yaml
from SPARQLWrapper import SPARQLWrapper, JSON

# SPARQL query grabs IRIs and rdfs:labels from UBERON organ_slim
sparql = SPARQLWrapper(
    "http://localhost:8080/rdf4j-server/repositories/cap"
)
sparql.setReturnFormat(JSON)

sparql.setQuery("""
PREFIX inSubset: <http://www.geneontology.org/formats/oboInOwl#inSubset>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT  ?x ?xLabel
WHERE 
{
      ?x inSubset: <http://purl.obolibrary.org/obo/uberon/core#organ_slim> .
      ?x rdfs:label ?xLabel 
}
    """
                )

ret = sparql.queryAndConvert()

query_output = []
for line in ret["results"]["bindings"]:
    query_output.append(line)

# generate list of CURIEs and organ labels
organs = []
for n in query_output:
    CURIE = n['x']['value'].replace("_", ":")
    CURIE = CURIE.partition('http://purl.obolibrary.org/obo/')[-1]
    label = n['xLabel']['value'].replace(" ", "_") + "_cell"
    organs.append((CURIE, label))

# convert list to dictionary
organ_dictionary = {tup[0]: tup[1] for tup in organs}

# ramuel.yaml initialization
yaml = ruamel.yaml.YAML()

# export populated dictionary to file
with open('../src/config/organ_2_cell.yaml', 'w') as file:
    documents = yaml.dump(organ_dictionary, file)