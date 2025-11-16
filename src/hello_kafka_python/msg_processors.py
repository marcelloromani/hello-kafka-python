import logging


class IMsgProcessor:

    def pre_send_hook(self, payload: str):
        """
        Called before writing the payload to a topic
        :param payload: the string to be written to the topic
        """
        pass

    def post_send_hook(self, payload: str):
        """
        Called after writing the payload to a topic
        :param payload: the string written to the topic
        """
        pass

    def post_receive_hook(self, payload: str):
        """
        Called after reading a message from the topic
        :param payload: contents of the message
        """
        pass


class PersistToTextFileMsgProcessor(IMsgProcessor):
    """
    Appends sent and received payloads to a text file.
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

    def _write_payload(self, payload: str) -> None:
        self._fd.write(payload)
        self._fd.write("\n")

    def post_receive_hook(self, payload: str):
        self._write_payload(payload)

    def post_send_hook(self, payload: str):
        self._write_payload(payload)
