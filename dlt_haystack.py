import subprocess
from typing import Dict, List, Any, Optional
from canals.serialization import default_to_dict, default_from_dict
from haystack import Document

from haystack.core.component import component
import glob, json
import dlt
import duckdb
import requests









@component
class DltConnector:
    def __init__(self, source, resource, pipeline_name:str=None, full_refresh:bool=None, dataset_name:str=None ):

        self.source = source
        self.resource = resource
        self.pipeline_name = pipeline_name
        self.full_refresh = full_refresh
        self.dataset_name = dataset_name

    def to_dict(self) -> Dict[str, Any]:
        return default_to_dict(self, source=str(self.source), resource=self.resource, pipeline_name=self.pipeline_name, full_refresh=self.full_refresh, dataset_name=self.dataset_name)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DltConnector":
        return default_from_dict(cls, data)

    @component.output_types(documents=List[Document])
    def run(self):
        haystack_docs = []
        dlt_metadata = {}

        con = duckdb.connect(':memory:', read_only=False)

        pipeline = dlt.pipeline(
            pipeline_name=self.pipeline_name,
            destination="duckdb",
            full_refresh=self.full_refresh,
            dataset_name=self.dataset_name,
            credentials=con
        )
        info = pipeline.run(self.source)
        print(info)
        print(info.load_packages[0])
        # print the information on the first completed job in the first load package
        print(info.load_packages[0].jobs["completed_jobs"][0])
        print(pipeline.last_trace)

        schemas_query = "SELECT schema_name FROM information_schema.schemata;"
        schemas = con.execute(schemas_query).fetchall()

        # Print available schemas
        for schema in schemas:
            # print(schema[0])
            if schema[0].startswith(self.dataset_name):
                selected_schema = schema[0]
                print(selected_schema)

                # con.sql(f"SELECT * FROM {selected_schema}").fetchdf()

                # Fetch all tables within the selected schema
                tables_query = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{selected_schema}';"
                tables = con.execute(tables_query).fetchall()

                # Iterate over each table and select data
                for table in tables:
                    table_name = table[0]
                    print(f"Fetching data from table: {table_name}")

                    # Construct and execute the query
                    # Note: Using triple quotes for f-string to handle potential special characters in table name
                    data_query = f"""SELECT * FROM "{selected_schema}"."{table_name}";"""
                    data = con.execute(data_query).fetchall()

                    if "dlt" in table_name:
                        # Aggregate data from "dlt" tables into 'dlt_metadata'
                        dlt_metadata[table_name] = data
                    else:
                        # Process non-"dlt" tables row by row
                        for row in data:
                            # Convert row data to text and create metadata for the row
                            row_text = ', '.join(map(str, row))  # Convert each value to string and join with ', '
                            row_metadata = {"table_name": table_name, "row_data": row}
                            # Create a Document for each row with its metadata
                            haystack_docs.append(Document(content=row_text, meta=dlt_metadata))

        # print(haystack_docs)

        return {"documents": haystack_docs}



