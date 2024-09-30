import logging
from decouple import config


LOG_HANDLER_NAME = config('APP_LOG_NAME')
LOG_FILE_NAME = config('APP_LOG_FILE_NAME')

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
	level=logging.DEBUG,
	handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE_NAME, mode='w')
    ]
)

logging.getLogger(LOG_HANDLER_NAME).setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
