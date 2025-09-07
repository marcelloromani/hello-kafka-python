import json
import logging.config
from pathlib import Path


def configure(logging_config_path: Path):
    conf = json.loads(logging_config_path.read_text())
    logging.config.dictConfig(config=conf)
