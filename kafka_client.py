import logging


class KafkaClient:
    logger = logging.getLogger()

    def __init__(self):
        self._shutdown = False

    def shutdown_requested(self):
        return self._shutdown

    def shutdown(self):
        self.logger.info("Shutdown request")
        self._shutdown = True
