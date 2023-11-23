import os
import logging
from typing import Optional
from weaviate import Client, auth
from dotenv import load_dotenv
load_dotenv()

class Config:
    """Configuration management class."""
    WEAVIATE_URL = os.environ.get("WEAVIATE_URL", "https://cluster-ttst-p3c4qvfy.weaviate.network")
    WEAVIATE_API_KEY = os.environ.get('WEAVIATE_API_KEY', 'default_api_key')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', 'default_openai_key')
    PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY', 'default_pinecone_key')

    @staticmethod
    def get_weaviate_url() -> str:
        return Config.WEAVIATE_URL

    @staticmethod
    def get_api_keys() -> dict:
        return {
            "weaviate_api_key": Config.WEAVIATE_API_KEY,
            "openai_api_key": Config.OPENAI_API_KEY,
            "pinecone_api_key": Config.PINECONE_API_KEY
        }