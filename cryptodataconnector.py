from dlt_haystack import DltConnector
import subprocess
from typing import Dict, List, Any, Optional
from canals.serialization import default_to_dict, default_from_dict
from haystack import component, Document
import glob, json
import dlt
import duckdb
import requests



@dlt.resource(name = "coin_list", write_disposition="replace")
def coin_list():
    response = requests.get('https://api.coinpaprika.com/v1/coins')
    yield from response.json()


@dlt.source
def crypto_data(name = "crypto_source"):
    yield coin_list()



# @component
class CryptoDataConnector(DltConnector):
    """
    A DltConnector subclass designed for fetching and processing cryptocurrency data.
    """
    def __init__(self, source, resource,  pipeline_name: str = "crypto_pipeline", full_refresh: bool = False, dataset_name: str = "crypto_data"):
        super().__init__(source=source, resource=resource, pipeline_name=pipeline_name, full_refresh=full_refresh, dataset_name=dataset_name)

    @component.output_types(documents=List[Document])
    def run(self) -> Dict[str, List[Document]]:
        # Fetch and process data using the inherited DltConnector functionality
        haystack_docs = super().run()

        return {"documents": haystack_docs}




crypto_connector = CryptoDataConnector(
    source=crypto_data(),
    resource=coin_list(),
    pipeline_name="my_crypto_pipeline",  # Specify your actual destination, e.g., "postgresql", "duckdb", etc.
    full_refresh=True,
    dataset_name="my_crypto_dataset"
)

documents = crypto_connector.run()