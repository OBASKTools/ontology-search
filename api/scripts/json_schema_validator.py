import json
from jsonschema import validate, Draft4Validator, SchemaError
import warnings


def get_json_from_file(filename):
    """Loads json from a file.
    """
    with open(filename, 'r') as f:
        try:
            fc = f.read()
        except Exception as exc:
            warnings.warn('Failed to open ' + filename + ' as JSON')
    return json.loads(fc)


if __name__ == "__main__":
    schema_loc = "api/src/config/contextual_search_logic_schema.json"
    json_loc = "api/src/config/contextual_search_logic.json"

    schema_file = get_json_from_file(schema_loc)
    json_file = get_json_from_file(json_loc)

    try:
        Draft4Validator.check_schema(schema_file)
    except SchemaError as exc:
        raise "contextual_search_logic_schema.json is invalid, please check your JSON schema"

    print("contextual_search_logic_schema.json is valid")

    try:
        validate(instance=json_file, schema=schema_file)
    except Exception as exc:
        raise "contextual_search_logic.json is invalid, please check your JSON file"

    print("contextual_search_logic.json is valid")
