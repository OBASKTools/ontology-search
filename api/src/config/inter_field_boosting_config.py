import os
import yaml
import logging

# inter field config file path
# organ_2cell.yaml maps organs to cell types, organs are given with their CURIEs as keys and
# cell types are string values correspond to those keys
CONF_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'organ_2_cell.yaml')

log = logging.getLogger(__name__)

# read inter field config yaml
with open(CONF_PATH, 'r') as stream:
    inter_field_config = yaml.safe_load(stream)

