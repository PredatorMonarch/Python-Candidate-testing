## Overview

This is a Python class that provides an interface to the Microsoft Language API. The purpose of this class is to make it easy to call various text analysis endpoints provided by the Microsoft Language API.

## Dependencies

This class requires the `requests` library. You can install it using pip:

```commandline
pip install requests
```

## Usage

To use this class, you need to have a Microsoft Azure account and a subscription key. You can sign up for a free account at [https://azure.microsoft.com/en-us/free/](https://azure.microsoft.com/en-us/free/).

### Variables

- `__endpoint` : - The endpoint URL for the Microsoft Language API.
- `__headers`  : - The headers to be sent with the request. It contains the subscription key.
- `version`    : - The version of the Microsoft Language API. Defaults to "2023-04-01"

### Methods

- `__init__(self, url: str, key: str, version: str = "2023-04-01")` : - Constructor for the class. Initializes the endpoint URL and headers.
    - `url` : - The endpoint URL for the Microsoft Language API.
    - `key` : - The subscription key for the Microsoft Language API.
    - `version` : - The version of the Microsoft Language API. Defaults to "2023-04-01"
- `genPayload(self, kind: str, documents: list[dict[str, str]]) -> dict` : - Generates the payload for the request. Used by the other methods.
    - `kind` : - The kind of text analysis to be made.
    - `documents` : - The list of documents to be analyzed. Each element is a dictionary with the format `{"id": "DOC_ID", "language": "LANG_ABREVATION", "text": "DOC CONTENT"}`.
    - Returns a dictionary to be used as the payload for the request.
- `apiCall(self, url: str, payload: dict, data: str) -> list[dict[str, any]] | str` : - Tries to make the API call to the Microsoft Language API endpoint.
    - `url` : - The endpoint URL for the Microsoft Language API.
    - `payload` : - The payload to be sent with the request.
    - `data` : - The data key value to extract from the json response.
    - If successful returns the response from the API as a list of dictionaries containing the id with the data extracted, otherwise returns the error message.
- `detectEntities(self, documents: list[dict[str, str]]) -> list[dict[str, any]] | str` : - Detects and categorizes entities in the given documents.
    - `documents` : - The list of documents to be analyzed. Same format as described above.
    - Returns the response from the API as a list of dictionaries containing the id with the entities detected.
- `redactDocuments(self, documents: list[dict[str, str]]) -> list[dict[str, any]] | str` : - Redacts the sensitive information in the given documents.
    - `documents` : - The list of documents to be analyzed. Same format as described above.
    - Returns the response from the API as a list of dictionaries containing the id with the redacted text.
- `keywordExtraction(self, documents: list[dict[str, str]]) -> list[dict[str, any]] | str` : - Identify the main concepts in the given documents.
    - `documents` : - The list of documents to be analyzed. Same format as described above.
    - Returns the response from the API as a list of dictionaries containing the id with the key phrases extracted.
- `entityLinking(self, documents: list[dict[str, str]]) -> list[dict[str, any]] | str` : - Identifies the entities in the given documents and links them to the relevant Wikipedia pages.
    - `documents` : - The list of documents to be analyzed. Same format as described above.
    - Returns the response from the API as a list of dictionaries containing the id with the entities linked.
- `entityRecognition(self, documents: list[dict[str, str]]) -> list[dict[str, any]] | str` : - identify and categorize entities in the given documents.
    - `documents` : - The list of documents to be analyzed. Same format as described above.
    - Returns the response from the API as a list of dictionaries containing the id with the entities recognized.
- `sentimentAnalysis(self, documents: list[dict[str, str]]) -> list[dict[str, any]] | str` : - Sentiment Analysis feature provides sentiment labels (such as "negative" "neutral" and "positive") and confidence scores at the sentence and document-level.
    - `documents` : - The list of documents to be analyzed. Same format as described above.
    - Returns the response from the API as a list of dictionaries containing the id with the sentiment detected.
- `languageDetection(self, documents: list[dict[str, str]]) -> list[dict[str, any]] | str` : - Identifies the language of the given documents.
    - `documents` : - The list of documents to be analyzed. Same format as described above.
    - Returns the response from the API as a list of dictionaries containing the id with the language detected.

### Examples

```python
url = "https://pythoncandidatetest.cognitiveservices.azure.com/"
key = "47163f4aae724873b04b360fb9178594"

mlapi = MLAPI(url, key)
documents = [
    {
        "id": "1",
        "language": "en",
        "text": "Call our office at 312-555-1234, or send an email to support@contoso.com"
    },
    {
        "id": "2",
        "language": "en",
        "text": "The employee's address is 2211 Old York Rd, Springfield, IL 62704"
    }
]
results = mlapi.detectEntities(documents)

'''
results = [{
        'id': '1', 
        'entities': [{
            'text': '312-555-1234', 
            'category': 'PhoneNumber', 
            'offset': 19, 
            'length': 12, 
            'confidenceScore': 0.8
            }, {
            'text': 'support@contoso.com', 
            'category': 'Email', 
            'offset': 53, 
            'length': 19, 
            'confidenceScore': 0.8
            }]
    }, {
        'id': '2', 
        'entities': [{
            'text': 'employee', 
            'category': 'PersonType', 
            'offset': 4, 
            'length': 8, 
            'confidenceScore': 0.88
            }, {
            'text': '2211 Old York Rd, Springfield, IL 62704', 
            'category': 'Address', 
            'offset': 26, 
            'length': 39, 
            'confidenceScore': 1.0
            }]
    }]
'''
```

```python
url = "https://pythoncandidatetest.cognitiveservices.azure.com/"
key = "47163f4aae724873b04b360fb9178594"

mlapi = MLAPI(url, key)
documents = [
    {
        "id": "1",
        "text": "This is a document written in English."
    },
    {
        "id": "2",
        "text": "Este es un documento escrito en Español."
    },
    {
        "id": "3",
        "text": "Ceci est un document rédigé en Français."
    },
    {
        "id": "4",
        "text": "这是用中文写的文件"
    }
]
results = mlapi.languageDetection(documents)

'''
results = [{
        'id': '1', 
        'detectedLanguage': {
            'name': 'English', 
            'iso6391Name': 'en', 
            'confidenceScore': 1.0
        }
    }, 
    {
        'id': '2', 
        'detectedLanguage': {
            'name': 'Spanish', 
            'iso6391Name': 'es', 
            'confidenceScore': 1.0
        }
    }, 
    {
        'id': '3', 
        'detectedLanguage': {
            'name': 'French', 
            'iso6391Name': 'fr', 
            'confidenceScore': 1.0
            }
    }, 
    {
        'id': '4', 
        'detectedLanguage': {
        'name': 'Chinese_Simplified', 
        'iso6391Name': 'zh_chs', 
        'confidenceScore': 1.0
        }
    }]
'''
```

## Testing

To run the test script, you need to have the `pytest` library installed. You can install it using pip:

```commandline
pip install pytest
```

To run the test script, use the following command:

```commandline
python test.py
```

Or you can use pytest command:

```commandline
pytest -v test.py
```

## Further Reading

For more information on the Microsoft Language API, please refer to the [official documentation](https://learn.microsoft.com/en-us/azure/ai-services/language-service/).
