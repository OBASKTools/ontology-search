import os
import sys
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

python_env = os.getenv("PYTHON_ENV")

logging.debug(f"PYTHON_ENV is set to '{python_env}'")
