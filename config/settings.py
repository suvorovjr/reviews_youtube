import os
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger

BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / '.env')

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

LOG_FILE_PATH = BASE_DIR / 'logs' / 'async_parser.log'
LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

logger.add(LOG_FILE_PATH, rotation="10 MB", retention="10 days", mode="a")
