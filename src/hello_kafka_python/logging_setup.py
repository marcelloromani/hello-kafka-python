import json
import logging.config


def configure(logging_config_path: str):
    with open(logging_config_path, "r") as fd:
        conf = json.loads(fd.read())
    logging.config.dictConfig(config=conf)
