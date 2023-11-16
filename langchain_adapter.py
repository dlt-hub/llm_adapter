from typing import Any

from dlt.common.schema.typing import TColumnNames, TTableSchemaColumns
from dlt.extract.decorators import resource as make_resource
from dlt.extract.source import DltResource
from langchain.schema.document import Document

VECTORIZE_HINT = "x-qdrant-embed"

def langchain_adapter(
    data: Any,
    to_content: TColumnNames = None,
    to_metadata: TColumnNames = None,
) -> list[Document]:
    """Prepares data for the Langchain destination by specifying which columns
    should become a part of the Langchain page_content.

    Args:
        data (Any): The data to be transformed. It can be raw data or an instance
            of DltResource. If raw data, the function wraps it into a DltResource
            object.
        to_content (TColumnNames, optional): Specifies columns to add to Langchain page content.
            Can be a single column name as a string or a list of column names.
        to_metadata (TColumnNames, optional): Specifies columns to add to Langchain metadata.
            Can be a single column name as a string or a list of column names.

    Returns:
        Document: Langchain Document object. https://api.python.langchain.com/en/latest/schema/langchain.schema.document.Document.html?highlight=document

    Raises:
        ValueError: If input for `to_content` or `to_metadata` invalid or empty.

    Examples:
        >>> data =     data = [
        {"name": "Anush", "last name": "Smith", "unique_id": "2835859394", "age": "30"},
        {"name": "Banush", "last name": "Jones", "unique_id": "2835859395", "age": "25"}]
        >>> langchain_adapter(data, to_content="name", to_metadata="unique_id")
        [Langchain Document object]
    """
    # wrap `data` in a resource if not an instance already
    resource: DltResource
    if not isinstance(data, DltResource):
        resource_name: str = None
        if not hasattr(data, "__name__"):
            resource_name = "content"
        resource = make_resource(data, name=resource_name)
    else:
        resource = data

    # column_hints: TTableSchemaColumns = {}

    document_list = []

    for row in data:
        # Handle multiple columns for content
        if isinstance(to_content, list):
            content = ' '.join([row.get(col, "") for col in to_content])
        else:
            content = row.get(to_content, "") if to_content else ""

        # Handle multiple columns for metadata
        metadata = {}
        if isinstance(to_metadata, list):
            for col in to_metadata:
                metadata[col] = row.get(col, "")
        elif to_metadata:
            metadata[to_metadata] = row.get(to_metadata, "")

        # Create a Document object with the specified content and metadata
        doc = Document(page_content=content, metadata=metadata)

        # Append the created Document object to the document list
        document_list.append(doc)

    return document_list



