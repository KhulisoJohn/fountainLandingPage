import logging

logger = logging.getLogger("audit")
logger.setLevel(logging.DEBUG)

if not logger.handlers:

    # FILE logs
    file_handler = logging.FileHandler("audit.log")
    file_handler.setLevel(logging.DEBUG)

    # TERMINAL logs
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)