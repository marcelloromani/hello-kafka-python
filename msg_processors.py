import logging


class IMsgProcessor:

    def process(self, payload: str):
        raise NotImplementedError


class PersistToTextFileMsgProcessor(IMsgProcessor):
    """
    Appends payload to a text file.
    """
    logger = logging.getLogger()

    def __init__(self, filename: str):
        self._filename = filename
        self.logger.info("Opening file %s in append mode", self._filename)
        self._fd = open(self._filename, "a")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._fd.close()

    def process(self, payload: str):
        self._fd.write(payload)
        self._fd.write("\n")
