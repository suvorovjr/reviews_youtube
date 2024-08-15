import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / '.env')

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
