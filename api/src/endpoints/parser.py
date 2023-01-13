from flask_restx import reqparse

suggest_arguments = reqparse.RequestParser()
suggest_arguments.add_argument('query', type=str, required=True)
suggest_arguments.add_argument('filter', type=str, action='append', required=False)
suggest_arguments.add_argument('boost', type=str, action='append', required=False)
suggest_arguments.add_argument('curie', type=str, required=False)

config_arguments = reqparse.RequestParser()
config_arguments.add_argument('target_field', type=str, required=True)
config_arguments.add_argument('source_tags', type=str, action='append', default=[''], required=False)

wrapper_arguments = reqparse.RequestParser()
wrapper_arguments.add_argument('query', type=str, required=True)
wrapper_arguments.add_argument('target_field', type=str, required=True)
wrapper_arguments.add_argument('source_tags', type=str, action='append', default=[''], required=False)

cell_type_check_arguments = reqparse.RequestParser()
cell_type_check_arguments.add_argument('cell_type', type=str, required=True)
