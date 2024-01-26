import requests
import requests.auth
from rich import print
import json
from bs4 import BeautifulSoup
from ebaysdk.finding import Connection as finding

class CrawlApiE(): # I actually dont think we need to OAUTH or get tokens for this API
    #Data Fields
    
    def __init__(self, clientID, secretID, userID, userPass):
        self.clientID = clientID
        self.secretID = secretID 
        self.userID = userID
        self.userPass = userPass


    def fetch(self, keyword):
        api = finding(appid = self.clientID, siteid = 'EBAY-US', config_file = None)
        count = 0
        api_request = {'keywords' : keyword, 'outputSelector' : 'SellerInfo', 'sortOrder': 'StartTimeNewest'}
        response = api.execute('findItemsByKeywords', api_request)
        soup = BeautifulSoup(response.content, features = 'lxml')
        self.items = soup.find_all('item')

    def parse(self):

        '''
        for item in self.items:
            cat = item.categoryname.string.lower()
            title = item.title.string.lower().strip()
            price = float(item.currentprice.string)
            url = item.viewitemurl.string.lower()
            seller = item.sellerusername.text.lower()
            print('\n')
            print("Category: "  + cat)
            print('\n')
            print(title)
            print('\n')
            print(price)
            print('\n')
            print(url)
            print('\n')
            print("Seller: " + seller)
        '''
        return self.items
    
           
if __name__ == "__main__":

    with open('info.json', 'r') as file:
        info = json.load(file)

    Bot = CrawlApiE(info['clientID'], info['secretID'], info['userID'], info['userPass'])
    Bot.fetch('apparel') 
    Bot.parse()
  