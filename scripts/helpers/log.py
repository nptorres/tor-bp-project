import logging


class Log:
    """
    Simple logger with printout to console
    """

    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        self.log_format = "%(asctime)s [%(levelname)s]: %(message)s"
        logging.basicConfig(format=self.log_format, level=logging.INFO)

    def get_logger(self) -> logging.Logger:
        return self.log
