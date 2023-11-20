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
from utils import _load_pdf
import logging
from config import Config
from haystack.document_stores import WeaviateDocumentStore
from haystack.schema import Document

api_keys = Config.get_api_keys()

OPENAI_API_KEY = api_keys["openai_api_key"]
embeddings = OpenAIEmbeddings()


def _init_haystack_pinecone():
    """
    Initialize Pinecone haystack client
    """
    # from milvus_haystack import MilvusDocumentStore
    api_keys = Config.get_api_keys()
    from haystack.document_stores import PineconeDocumentStore

    document_store = PineconeDocumentStore(api_key=api_keys['pinecone_api_key'],
                                           similarity="cosine",
                                           environment="gcp-starter",
                                           index="fjdfdj",
                                           recreate_index=True,
                                           embedding_dim=768)

    # document_store = WeaviateDocumentStore(host=Config.get_weaviate_url(), port=8080, embedding_dim=768, index = "DLTLOADER", api_key=api_keys["weaviate_api_key"] )
    logging.info("Document store loaded")
    return document_store







def _init_weaviate() -> WeaviateHybridSearchRetriever:
    """
    Initialize Weaviate client and retriever.

    Returns:
        WeaviateHybridSearchRetriever: An instance of the Weaviate hybrid search retriever.
    """
    try:
        api_keys = Config.get_api_keys()
        auth_config = weaviate.auth.AuthApiKey(api_key=api_keys["weaviate_api_key"])
        client = weaviate.Client(
            url=Config.get_weaviate_url(),
            auth_client_secret=auth_config,
            additional_headers={"X-OpenAI-Api-Key": api_keys["openai_api_key"]}
        )

        retriever = WeaviateHybridSearchRetriever(
            client=client,
            index_name="PDFloader",
            text_key="text",
            attributes=[],
            embedding=embeddings,
            create_schema_if_missing=True,
        )

        return retriever
    except Exception as e:
        print(e)
        raise Exception("Failed to initialize Weaviate client and retriever.")




def load_to_weaviate(document_path: str, document_source: list = None, llm_framework: str = None):
    """
    Load documents to Weaviate.

    Parameters:
        document_path (str): Path to the document to be loaded.
        document_source (list): Source of the document to be loaded. Could be dlt_filesystem or pdf

    Returns:
        Result of adding documents to Weaviate.
    """
    if not document_path:
        raise ValueError("Document path cannot be None or empty.")

    try:
        retriever = _init_weaviate()
        if document_source == 'dlt_filesystem':


            list_of_source_docs = document_source
            documents = llm_adapter(list_of_source_docs, to_content=["name", "age", "city"],
                                    to_metadata=["id", "email"], llm_framework=llm_framework)

            return retriever.add_documents(documents)
        else:

            pdf_to_text = _load_pdf(document_path)
            docs = llm_adapter(pdf_to_text, to_content="text")
            return retriever.add_documents(docs)
    except Exception as e:
        logging.error(f"Error loading documents to Weaviate: {e}")
        raise