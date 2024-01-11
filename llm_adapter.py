from typing import Any, Union, List

from dlt.common.schema.typing import TColumnNames, TTableSchemaColumns
from dlt.extract.decorators import resource as make_resource
from dlt.extract.source import DltResource



def llm_adapter(
    data: Any,
    to_content: TColumnNames = None,
    to_metadata: TColumnNames = None,
    llm_framework: str = None,
) -> List[Any]:
    """Prepares data for the Langchain or Haystack destination by specifying which columns
    should become a part of the Langchain or Haystack page_content.

    Args:
        data (Any): The data to be transformed. It can be raw data or an instance
            of DltResource. If raw data, the function wraps it into a DltResource
            object.
        to_content (TColumnNames, optional): Specifies columns to add to Langchain page content.
            Can be a single column name as a string or a list of column names.
        to_metadata (TColumnNames, optional): Specifies columns to add to Langchain metadata.
            Can be a single column name as a string or a list of column names.
        llm_framework (str, optional): Specifies the framework to use. Can be Langchain or Haystack

    Returns:
        Document: Langchain or Haystack Document object. https://api.python.langchain.com/en/latest/schema/langchain.schema.document.Document.html?highlight=document

    Raises:
        ValueError: If input for `to_content` or `to_metadata` invalid or empty.

    Examples:
        >>> data =     data = [
        {"name": "Anush", "last name": "Smith", "unique_id": "2835859394", "age": "30"},
        {"name": "Banush", "last name": "Jones", "unique_id": "2835859395", "age": "25"}]
        >>> llm_adapter(data, to_content="name", to_metadata="unique_id", llm_framework="langchain")
        [Langchain/Haystack Document object]
    """
    # wrap `data` in a resource if not an instance already
    if llm_framework not in ["langchain", "haystack"]:
        raise ValueError("Invalid llm_framework. Must be 'langchain' or 'haystack'.")

    resource: DltResource
    if not isinstance(data, DltResource):
        resource_name: str = None
        if not hasattr(data, "__name__"):
            resource_name = "content"
        resource = make_resource(data, name=resource_name)
    else:
        resource = data
    document_list = []
    for row in data:
        if llm_framework == "langchain":
            from langchain.schema.document import Document as LangchainDocument
            # For Langchain, create a Document with 'page_content' and 'metadata'
            content = ' '.join([row.get(col, "") for col in to_content]) if isinstance(to_content, list) else row.get(to_content, "")
            metadata = {col: row.get(col, "") for col in to_metadata} if isinstance(to_metadata, list) else {to_metadata: row.get(to_metadata, "")}
            doc = LangchainDocument(page_content=content, metadata=metadata)
        else:
            from haystack import Document as HaystackDocument
            content = ' '.join(
                    [row.get(col, '') for col in (to_content if isinstance(to_content, list) else [to_content])])

            # Combine fields for metadata
            meta = {col: row.get(col, '') for col in (to_metadata if isinstance(to_metadata, list) else [to_metadata])}
            doc = HaystackDocument(content=content, meta=meta)
        # Append the created Document object to the document list
        document_list.append(doc)

    return document_list



