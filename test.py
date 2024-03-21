import pytest
from mlapi import MLAPI

url = "https://pythoncandidatetest.cognitiveservices.azure.com/"
key = "47163f4aae724873b04b360fb9178594"


class TestMLAPI:

    def test_apiCall(self):
        mlapi = MLAPI(url, key)
        payload = mlapi.genPayload("PiiEntityRecognition", [{"id": "1", "text": "Hello, world!"}])
        assert (mlapi.apiCall(url + "language/:analyze-text?api-version=2023-04-01", payload, 'entities')
                == [{"id": "1", "entities": []}])

    def test_detectEntities(self):
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

        assert results[0]['id'] == '1'

        assert results[0]['entities'][0]['text'] == '312-555-1234'
        assert results[0]['entities'][0]['category'] == 'PhoneNumber'
        assert results[0]['entities'][0]['offset'] == 19
        assert results[0]['entities'][0]['length'] == 12

        assert results[0]['entities'][1]['text'] == 'support@contoso.com'
        assert results[0]['entities'][1]['category'] == 'Email'
        assert results[0]['entities'][1]['offset'] == 53
        assert results[0]['entities'][1]['length'] == 19

        assert results[1]['id'] == '2'

        assert results[1]['entities'][0]['text'] == 'employee'
        assert results[1]['entities'][0]['category'] == 'PersonType'
        assert results[1]['entities'][0]['offset'] == 4
        assert results[1]['entities'][0]['length'] == 8

        assert results[1]['entities'][1]['text'] == '2211 Old York Rd, Springfield, IL 62704'
        assert results[1]['entities'][1]['category'] == 'Address'
        assert results[1]['entities'][1]['offset'] == 26
        assert results[1]['entities'][1]['length'] == 39

    def test_redactDocuments(self):
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
        results = mlapi.redactDocuments(documents)

        assert results[0]['id'] == '1'
        assert results[0]['redactedText'] == "Call our office at ************, or send an email to *******************"

        assert results[1]['id'] == '2'
        assert results[1]['redactedText'] == "The ********'s address is ***************************************"

    def test_keywordExtraction(self):
        mlapi = MLAPI(url, key)
        documents = [
            {
                "id": "1",
                "language": "en",
                "text": "Dr. Smith has a very modern medical office, and she has great staff."
            }
        ]
        results = mlapi.keywordExtraction(documents)

        assert results[0]['id'] == '1'

        assert 'Dr. Smith' in results[0]['keyPhrases']
        assert 'modern medical office' in results[0]['keyPhrases']
        assert 'great staff' in results[0]['keyPhrases']

    def test_entityLinking(self):
        mlapi = MLAPI(url, key)
        documents = [
            {
                "id": "1",
                "language": "en",
                "text": "Microsoft was founded by Bill Gates and Paul Allen on April 4, 1975."
            }
        ]
        results = mlapi.entityLinking(documents)

        assert results[0]['id'] == '1'

        assert results[0]['entities'][0]['name'] == 'Microsoft'
        assert results[0]['entities'][0]['url'] == 'https://en.wikipedia.org/wiki/Microsoft'

        assert results[0]['entities'][1]['name'] == 'Bill Gates'
        assert results[0]['entities'][1]['url'] == 'https://en.wikipedia.org/wiki/Bill_Gates'

        assert results[0]['entities'][2]['name'] == 'Paul Allen'
        assert results[0]['entities'][2]['url'] == 'https://en.wikipedia.org/wiki/Paul_Allen'

    def test_entityRecognition(self):
        mlapi = MLAPI(url, key)
        documents = [
            {
                "id": "1",
                "language": "en",
                "text": "I had a wonderful trip to Seattle last week."
            }
        ]
        results = mlapi.entityRecognition(documents)

        assert results[0]['id'] == '1'

        assert results[0]['entities'][0]['text'] == 'trip'
        assert results[0]['entities'][0]['category'] == 'Event'

        assert results[0]['entities'][1]['text'] == 'Seattle'
        assert results[0]['entities'][1]['category'] == 'Location'

        assert results[0]['entities'][2]['text'] == 'last week'
        assert results[0]['entities'][2]['category'] == 'DateTime'

    def test_sentiAnalysis(self):
        mlapi = MLAPI(url, key)
        documents = [
            {
                "id": "1",
                "language": "en",
                "text": "The food and service were unacceptable. The concierge was nice, however."
            },
            {
                "id": "2",
                "language": "en",
                "text": "The rooms were beautiful."
            },
            {
                "id": "3",
                "language": "en",
                "text": "The service was slow."
            },
            {
                "id": "4",
                "language": "en",
                "text": "I wake up every day"
            }
        ]
        results = mlapi.sentimentAnalysis(documents)

        assert results[0]['id'] == '1'
        assert results[0]['sentiment'] == 'mixed'

        assert results[1]['id'] == '2'
        assert results[1]['sentiment'] == 'positive'

        assert results[2]['id'] == '3'
        assert results[2]['sentiment'] == 'negative'

        assert results[3]['id'] == '4'
        assert results[3]['sentiment'] == 'neutral'

    def test_languageDetection(self):
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

        assert results[0]['id'] == '1'
        assert results[0]['detectedLanguage']['name'] == 'English'
        assert results[0]['detectedLanguage']['iso6391Name'] == 'en'

        assert results[1]['id'] == '2'
        assert results[1]['detectedLanguage']['name'] == 'Spanish'
        assert results[1]['detectedLanguage']['iso6391Name'] == 'es'

        assert results[2]['id'] == '3'
        assert results[2]['detectedLanguage']['name'] == 'French'
        assert results[2]['detectedLanguage']['iso6391Name'] == 'fr'

        assert results[3]['id'] == '4'
        assert results[3]['detectedLanguage']['name'] == 'Chinese_Simplified'
        assert results[3]['detectedLanguage']['iso6391Name'] == 'zh_chs'


if __name__ == '__main__':
    pytest.main(["-v", "test.py"])