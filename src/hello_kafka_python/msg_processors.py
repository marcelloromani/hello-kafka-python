import logging


class IMsgProcessor:

    def pre_send_hook(self, payload: str):
        pass

    def post_send_hook(self, payload: str):
        pass

    def post_receive_hook(self, payload: str):
        pass


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

    def post_receive_hook(self, payload: str):
        self._fd.write(payload)
        self._fd.write("\n")

    def post_send_hook(self, payload: str):
        self._fd.write(payload)
        self._fd.write("\n")
