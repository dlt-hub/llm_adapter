import posixpath

import pdfplumber
from llm_adapter import llm_adapter
import dlt
try:
    from filesystem import FileItemDict, filesystem, readers, read_csv, read_jsonl, read_parquet  # type: ignore
except ImportError:
    from filesystem import (
        FileItemDict,
        filesystem,
        readers,
        read_csv,
        read_jsonl,
        read_parquet,
    )
import weaviate
from langchain.embeddings import OpenAIEmbeddings
from langchain.retrievers import WeaviateHybridSearchRetriever
from dotenv import load_dotenv
load_dotenv()

import logging
from config import Config

api_keys = Config.get_api_keys()

OPENAI_API_KEY = api_keys["openai_api_key"]
embeddings = OpenAIEmbeddings()



TESTS_BUCKET_URL = posixpath.abspath("/Users/vasa/PycharmProjects/DLTLangchain/.data/")

jsonl_reader = readers(TESTS_BUCKET_URL, file_glob="**/*.jsonl").read_jsonl(
    chunksize=10000
)
@dlt.source
def filesystem_jsonl():
    return jsonl_reader


if __name__ == '__main__':
    # data = [
    #     {"name": "Anush", "age": "30", "id": "2835859394", "email": "111@gmail.com", "city": "Yerevan"},
    #     {"name": "Banush", "age": "32", "id": "2835859395", "email": "222@gmail.com", "city": "London"},
    # ]

    data = list(filesystem_jsonl())

    documents = llm_adapter(data, to_content=["name", "age", "city"], to_metadata=["id", "email"], llm_framework='haystack')
    print(documents)




    # print(users().compute_table_schema())




