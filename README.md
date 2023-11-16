# Langchain Adapter

This project contains the `langchain_adapter` function, a Python utility designed to adapt a given dataset into a structured format suitable for document processing. 
It is particularly useful for transforming data into a format that can be easily handled by document processing or natural language processing (NLP) systems.

## Getting Started

These instructions will guide you through setting up the `langchain_adapter` function in your local environment.

### Prerequisites

You need Python installed on your system. The function is compatible with Python 3.11 and above. You can download Python from [here](https://www.python.org/downloads/).

Poetry is used to manage library dependencies. Make sure to have Poetry installed. 

### Installation

Clone this repository or download the source code to your local machine. The primary function is contained in the `langchain_adapter.py` file.

```bash
git clone https://github.com/dlt-hub/llm_adapter
cd llm_adapter
```
Usage

Run the following command to start the Poetry shell:

```poetry shell```

To use the langchain_adapter function in your Python script, first import it:
```
python

from langchain_adapter import langchain_adapter

```
Then, call the function with your data:
```
python

data = [
    {"name": "Anush", "last name": "Smith", "unique_id": "2835859394", "age": "30"},
    # ... other data entries ...
]

documents = langchain_adapter(data, to_content=["name", "last name"], to_metadata=["unique_id", "age"])
```


Open issues

1. I need advice on the architecture here. Idea is to have unique IDs, merge keys etc in the Langchain format, but that requires a destination