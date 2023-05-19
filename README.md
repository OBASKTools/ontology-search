# OBASK tools ontology-search

Ontology search APIs for OBASKTools.  API calls support autosuggest queries optimised for ontology search, as well as filtering and boosting of content using semantic tags.  
  
# Basic Search Concepts
   
## Filtering and Boosting
  
Faceted search allows users to refine their search results by selecting various attributes or facets. These facets represent different dimensions or categories related to the search data. For example, facets could include specific organism, organ or developmental stage. By selecting or deselecting facets, users can dynamically narrow down their search results and explore specific subsets of the data.

Filtering is a key component of faceted search. It involves applying specific criteria or conditions to the search results to exclude or include certain items. Filtering is typically based on the selected facets. For instance, if a user selects the 'homo sapiens' facet and specifies an organism in their query, the search service will filter out terms that are not related with 'homo sapiens'. Multiple filters can be applied simultaneously to further refine the search results.

Boosting is a technique used to assign different levels of importance or relevance to specific attributes or facets. It allows certain facets or criteria to have a higher impact on the ranking of search results. By boosting relevant facets, the search service ensures that items matching those facets are given higher priority in the result set. This helps to improve the overall relevance of the search results and better aligns them with user preferences. For example, after selecting the 'homo sapiens' filter, users can further refine their search by choosing the 'kidney' term. This boosts the visibility of kidney-related terms, placing them higher in the search results compared to other organ-related terms.

In combination, these components create a robust faceted search service with filtering and boosting mechanisms. Users can explore and refine their search results using facets, apply filters to narrow down their selection, and receive highly relevant results based on the boosting mechanism. API definition can be found at [OBASK Ontology RESTFUL API](#obask-ontology-restful-api)

## Contextual Search

This is a feature we haven't implemented yet for OBASK. Filtering and boosting will be applied automatically based on predefined configuration file.


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
