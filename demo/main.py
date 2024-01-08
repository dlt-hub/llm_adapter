import posixpath
import os


# Disable telemetry by setting the environment variable
os.environ["HAYSTACK_TELEMETRY_ENABLED"] = "False"

# Get the directory where the current script is located
script_directory = os.path.dirname(os.path.realpath(__file__))

# Move up one level (parent directory)
parent_directory = os.path.dirname(script_directory)

# Set the current working directory to the parent directory
os.chdir(parent_directory)

import sys
sys.path.append(parent_directory)

print("Current Working Directory set to:", os.getcwd())
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
from langchain_community.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv

from haystack.core.component import component

load_dotenv()

import logging
from config import Config

api_keys = Config.get_api_keys()

OPENAI_API_KEY = api_keys["openai_api_key"]
embeddings = OpenAIEmbeddings()



from haystack.document_stores import InMemoryDocumentStore
from haystack.components.writers import DocumentWriter
from haystack import Document




# TESTS_BUCKET_URL = posixpath.abspath("/Users/vasa/PycharmProjects/DLTLangchain/.data/")
#
# jsonl_reader = readers(TESTS_BUCKET_URL, file_glob="**/*.jsonl").read_jsonl(
#     chunksize=10000
# )
# @dlt.source
# def filesystem_jsonl():
#     return jsonl_reader

@component
class dltLoader:
    @component.output_types(the_answer=list)
    def run(self, path:str):
        print("SCRIPT DIR IS ", script_directory)
        TESTS_BUCKET_URL = posixpath.abspath(script_directory +"/" +path)
        jsonl_reader = readers(TESTS_BUCKET_URL, file_glob="**/*.jsonl").read_jsonl(
            chunksize=10000
        )
        @dlt.source
        def filesystem_jsonl():
            return jsonl_reader
        data = list(filesystem_jsonl())
        # data_str = [str(item) for item in data]
        return {"the_answer": data}


@component
class dltAdapter:
    @component.output_types(the_answer=list[Document] )
    def run(self, data_source:list, content: list, metadata:list) :
        value = llm_adapter(data=data_source, to_content=content, to_metadata=metadata, llm_framework='haystack')
        return {"the_answer": value}


if __name__ == '__main__':

    #sample data that can  be used for testing
    data = [
        {"name": "Anush", "age": "30", "id": "2835859394", "email": "111@gmail.com", "city": "Yerevan"},
        {"name": "Banush", "age": "32", "id": "2835859395", "email": "222@gmail.com", "city": "London"},
    ]

    #pipeline init
    from haystack import Pipeline

    p = Pipeline()

    #components added to the pipeline

    p.add_component("dltLoader", dltLoader())
    p.add_component("dltAdapter", dltAdapter())
    #components connected to each other
    p.connect("dltLoader.the_answer", "dltAdapter.data_source")
    # run the pipeline
    p.add_component('writer', DocumentWriter(document_store=InMemoryDocumentStore()))
    p.connect("dltAdapter.the_answer", "writer.documents")

    f = p.run(data={"dltLoader": {"path":".data/"} ,"dltAdapter": { "content": ["name", "city"], "metadata": ["id", "email"]}})

    print(f)


    #

    #
    #

    # p = Pipeline()
    # p.add_component("dltAdapter", dltAdapter())
    # f = p.run(data={"dltAdapter": { "data_source":data, "content": ["name", "age", "city"], "metadata": ["id", "email"]}})
    # print(f)




    # print(p.context)
    # p.connect()

    # documents = llm_adapter(data, to_content=["name", "age", "city"], to_metadata=["id", "email"], llm_framework='haystack')
    # print(documents)
    # from vectorstore_manager import _init_haystack_pinecone
    # retriever = _init_haystack_pinecone()
    # retriever.write_documents(documents)
    # print(documents)
    # print(users().compute_table_schema())




