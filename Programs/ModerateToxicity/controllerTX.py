import requests
import requests.auth
from rich import print
import json

class ModerateToxicity(): 
    #Data Fields
    
    def __init__(self, clientID):
        self.clientID = clientID
      
    def evaluateToxicity(self, text):
        url = "https://api.moderatehatespeech.com/api/v1/moderate/"
        headers = {
            "Content-Type": "application/json",
        }

        data = {
            "token": str(self.clientID),
            "text": str(text),
        }

        try:
            response = requests.post(url, json=data, headers=headers)   
            #print(response) 
            result = response.json()
            print(text)
            if(result.get("class") == "flag"):
                print('Toxicity Confidence: ' + str(result.get("confidence")))
            else:
                print('Purity Confidence: ' + str(result.get("confidence")))
                
            return (result.get("confidence"), result.get("class"))
        
        except Exception as e:
            print(e)
        
        return (0, "NA")

 
if __name__ == "__main__":

    with open('info.json', 'r') as file:
        info = json.load(file)

    ParseToxicity = ModerateToxicity(info['clientID'])
    ParseToxicity.evaluateToxicity("Faggot")
    ParseToxicity.evaluateToxicity("Kill")
    ParseToxicity.evaluateToxicity("Hitler")
    ParseToxicity.evaluateToxicity("turtle")
    ParseToxicity.evaluateToxicity("Israel")
    