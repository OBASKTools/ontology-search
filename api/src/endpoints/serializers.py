from flask_restx import fields
from restplus import api

terms = ['Organism', 'Organ', 'Assay', 'Disease', 'Developmental_stage', 'Cell_type', 'Ethnicity', 'Sex']
metadata = api.model('Metadata', dict(map(lambda x: (x, fields.List(fields.String(required=False, default=''),
                                                                    description=f"{x} field inputs")), terms)))