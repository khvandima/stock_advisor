from loguru import logger
import sys
from app.config import settings


logger.remove()
logger.add(sys.stdout, level=settings.LOG_LEVEL)
logger.add('logs/app.log', rotation='10 MB', level=settings.LOG_LEVEL)
logger.add('logs/errors.log', rotation='10 MB', level='ERROR')
