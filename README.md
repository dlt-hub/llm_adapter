# Haystack Adapter

This project aims to integrate dlt into Haystack
It cointains two main functions:
- llm_adapter -> converts the data into the format that can be used by Haystack
- haystack_adapter -> wraps dlt into Haystack pipeline

## Getting Started

These instructions will guide you through setting up the Haystack integration in your local environment.
### Prerequisites

You need Python installed on your system. The function is compatible with Python 3.11 and above. You can download Python from [here](https://www.python.org/downloads/).

Poetry is used to manage library dependencies. Make sure to have Poetry installed. 

### Installation

Clone this repository or download the source code to your local machine. The primary function is contained in the `llm_adapter.py` file.

```bash
git clone https://github.com/dlt-hub/llm_adapter
cd llm_adapter
```



### Haystack 2.0 Integration

The `DltConnector` function is used to integrate dlt into the Haystack pipeline. The function is contained in the `dlt_haystack.py` file.

```python cryptodataconnector.py```




### dlt llm adapter
Usage

An example of the implementation is in the 'demo' folder

Run the following command to start the Poetry shell:

```poetry shell```

To see a working example, navigate to the `demo` folder and run the following command:

```python main.py```

Otherwise, to use the llm_adapter function in your Python script, first import it:
```

from llm_adapter import llm_adapter

```
Then, call the function with your data:
```

data = [
    {"name": "Anush", "last name": "Smith", "unique_id": "2835859394", "age": "30"},
    # ... other data entries ...
]

documents = llm_adapter(data, to_content=["name", "last name"], to_metadata=["unique_id", "age"], llm_framework='haystack')
```
The same structure works for haystack
In the main function, after adding Pinecone key, you can also write haystack docs to Pinecone
```
    documents = llm_adapter(data, to_content=["name", "age", "city"], to_metadata=["id", "email"], llm_framework='haystack')
    from vectorstore_manager import _init_haystack_pinecone

    #example of haystack writer, requries pinecone key to be provided
    retriever = _init_haystack_pinecone()
    retriever.write_documents(documents)

```
In addition to this, additional feature was added which represents Haystack 2.0 integration with the dlthub.

In that context, dlthub is used for document loading and transformation as a part of the Haystack pipeline.
Each element was defined as a Haystack 2.0 component and can be used as a part of the Haystack pipeline.
