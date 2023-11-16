from langchain_adapter import langchain_adapter
import dlt

# Press the green button in the gutter to run the script.

@dlt.resource( name="table_name",primary_key="id", write_disposition="merge")
def users():
    yield [
        {'id': 1, 'name': 'Alice 2'},
        {'id': 2, 'name': 'Bob 2'}
    ]

@dlt.source
def source_name():
    return users

if __name__ == '__main__':
    data = [
        {"name": "Anush", "last name": "Smith", "unique_id": "2835859394", "age": "30"},
        {"name": "Banush", "last name": "Jones", "unique_id": "2835859395", "age": "25"}
    ]

    documents = langchain_adapter(data, to_content=["name", "last name"], to_metadata=["unique_id", "age"])
    print(documents)

    # print(users().compute_table_schema())




