import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

fusion_header = {
    'Authorization': f'Bearer {os.environ.get("FUSION_KEY")}',
    'accept': 'application/json',
}

