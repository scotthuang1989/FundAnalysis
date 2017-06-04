
import logging
import sys

root_logger = logging.getLogger()
fh = logging.FileHandler('log.log',mode='w')
fh.setLevel(logging.ERROR)


# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(asctime)s  %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

root_logger.addHandler(fh)


