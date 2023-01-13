import os
import json
import logging

# Contextual search logic file path
# contextual_search_logic.json contains business logic of filtering and boosting parameters of the search service.
# It contains both single-field and inter-field configuration
CONF_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'contextual_search_logic.json')

log = logging.getLogger(__name__)

# read contextual search logic json
with open(CONF_PATH, "r") as f:
    contextual_search_config = json.load(f)
