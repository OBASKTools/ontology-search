# OBASK tools ontology-search

Ontology search APIs for OBASKTools.  API calls support autosuggest queries optimised for ontology search, as well as filtering and boosting of content using semantic tags.  
  
  

# OBASK Ontology RESTFUL API
Ontology Based Application Starter Kit, Ontology restful API that wraps SOLR search.

## Version: 1.0.0

---
## api
Ontology API

### /api/healthcheck

#### GET
##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Success |

### /api/suggest

#### GET
##### Summary

Search service wrapper for Solr

##### Description

* <b>query</b> (mandatory): search terms

* <b>filter</b> (optional): Semantic tags for query filtering

* <b>boost</b> (optional): Semantic tags for query boosting

* <b>curie</b> (optional): Compact uniform resource identifier, used for dynamic boosting. i.e. UBERON:0002113

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| query | query |  | Yes | string |
| filter | query |  | No | [ string ] |
| boost | query |  | No | [ string ] |
| curie | query |  | No | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Success |
   
WARNING: OBASK tools originated with work carried out to support the [Virtual Fly Brain](virtualflybrain.org) project, the [Allen Cell-Type Knowledge Explorer](https://knowledge.brain-map.org/celltypes) and the [Cell Annotation Platform](celltype.info). Work to split this out into OBASK tools is currently ongoing and so code on this repo should be considered Alpha and may be subject to breaking changes
