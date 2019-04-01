import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SERVER_NAME = os.environ.get("SERVER_NAME")
DOMAIN_NAME = os.environ.get("DOMAIN_NAME")
USER_NAME = os.environ.get("USER_NAME")
PASSWORD = os.environ.get("PASSWORD")
SEARCH_DC = os.environ.get("SEARCH_DC")
