import context
import logging
import sys
import pytest

test_folder = "api/test/"

if __name__ == "__main__":
    logging.debug(f"PYTHON_ENV is set to '{context.python_env}'")
    logging.info("Start unit testing")
    files = [
        "services/test_ontology_service.py",
    ]
    sys.exit(pytest.main([test_folder + s for s in files]))
