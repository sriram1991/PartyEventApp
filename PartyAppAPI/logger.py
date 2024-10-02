import logging
import sys
from logging.handlers import TimedRotatingFileHandler

#get logger
logger = logging.getLogger()

#create format
log_format = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s")

#creating Handler
streamHandler = logging.StreamHandler(sys.stdout)
fileHandler = TimedRotatingFileHandler('logs/app.log', when="d", interval=2, backupCount=100)

streamHandler.setFormatter(log_format)
fileHandler.setFormatter(log_format)

logger.handlers = [streamHandler, fileHandler]

logger.setLevel(logging.INFO)

