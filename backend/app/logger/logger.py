import logging

logger = logging.getLogger("audit")
logger.setLevel(logging.INFO)

handler = logging.FileHandler("audit.log")
formatter = logging.Formatter("%(asctime)s | %(message)s")

handler.setFormatter(formatter)
logger.addHandler(handler)