import requests
class MLAPI:

    def __init__(self, url: str, key: str, version: str = "2023-04-01") -> None:
        self.__endpoint = url
        self.__headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': key
        }
        self.version = version

    def genPayload(self, kind: str, documents: list[dict[str, str]]) -> dict:
        return {
            "kind": kind,
            "parameters": {
                "modelVersion": "latest"
            },
            "analysisInput": {
                "documents": documents
            }
        }

    def apiCall(self, url: str, payload: dict, data: str) -> list[dict[str, any]] | str:
        try:
            response = requests.post(url, headers=self.__headers, json=payload)
            if len(response.json()['results']['errors']) != 0:
                return response.json()['results']['errors']
            return [{'id': i['id'], data: i[data]} for i in response.json()['results']['documents']]
        except Exception as e:
            return str(e)

    def detectEntities(self, documents: list[dict[str, str]]) -> list[dict[str, any]] | str:
        url = self.__endpoint + "/language/:analyze-text?api-version=" + self.version
        payload = self.genPayload("PiiEntityRecognition", documents)

        return self.apiCall(url, payload, 'entities')

    def redactDocuments(self, documents: list[dict[str, str]]) -> list[dict[str, any]] | str:
        url = self.__endpoint + "/language/:analyze-text?api-version=" + self.version
        payload = self.genPayload("PiiEntityRecognition", documents)

        return self.apiCall(url, payload, 'redactedText')

    def keywordExtraction(self, documents: list[dict[str, str]]) -> list[dict[str, any]] | str:
        url = self.__endpoint + "/language/:analyze-text?api-version=" + self.version
        payload = self.genPayload("KeyPhraseExtraction", documents)

        return self.apiCall(url, payload, 'keyPhrases')

    def entityLinking(self, documents: list[dict[str, str]]) -> list[dict[str, any]] | str:
        url = self.__endpoint + "/language/:analyze-text?api-version=" + self.version
        payload = self.genPayload("EntityLinking", documents)

        return self.apiCall(url, payload, 'entities')

    def entityRecognition(self, documents: list[dict[str, str]]) -> list[dict[str, any]] | str:
        url = self.__endpoint + "/language/:analyze-text?api-version=" + self.version
        payload = self.genPayload("EntityRecognition", documents)

        return self.apiCall(url, payload, 'entities')

    def sentimentAnalysis(self, documents: list[dict[str, str]]) -> list[dict[str, any]] | str:
        url = self.__endpoint + "/language/:analyze-text?api-version=" + self.version
        payload = self.genPayload("SentimentAnalysis", documents)

        return self.apiCall(url, payload, 'sentiment')

    def languageDetection(self, documents: list[dict[str, str]]) -> list[dict[str, any]] | str:
        url = self.__endpoint + "/language/:analyze-text?api-version=" + self.version
        payload = self.genPayload("LanguageDetection", documents)

        return self.apiCall(url, payload, 'detectedLanguage')

