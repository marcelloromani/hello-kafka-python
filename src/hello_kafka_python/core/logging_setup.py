import json
import logging.config
from pathlib import Path

DEFAULT_LOGGING_CONFIG_FILE = Path(__file__).parent / "logging_config.json"


def configure(logging_config_path: Path = DEFAULT_LOGGING_CONFIG_FILE):
    conf = json.loads(logging_config_path.read_text())
    logging.config.dictConfig(config=conf)
