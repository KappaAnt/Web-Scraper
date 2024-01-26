import requests
import requests.auth
from rich import print
import json

class CrawlApiR():
    #Data Fields
    
    def __init__(self, clientID, secretID, userID, userPass):
        self.clientID = clientID
        self.secretID = secretID 
        self.userID = userID
        self.userPass = userPass

    def tokenAuthenticate(self): #Officially connect to the REST Reddit API
                            #OAuth 
        clientAuth = requests.auth.HTTPBasicAuth(self.clientID, self.secretID)
        post_data = {'grant_type': 'password', 
                     'username': self.userID,
                     'password': self.userPass
                    }
        headers = {
            'User-Agent': 'our Bot 1.0' #Very important to set up our own User-Agent
                                        #Request limit around 30-60 per minute
        }
        Token_Endpoint = 'https://www.reddit.com/api/v1/access_token'
        response = requests.post(Token_Endpoint, data=post_data, headers=headers, auth=clientAuth)
        print("Authentication Status: " + response.reason)
        expires_in = response.json()['expires_in']
        if(response.status_code == 200):
            self.tokenID = response.json()['access_token'] #We need to refresh this token after the expiration time
            print("Token Expires In: " + str(expires_in) + "s")

    def useToken_Post(self, subReddit, limit): #Im going to try to pull a post
        #GET[/r/subreddit]/new
        #Endpoint is a listing
        OAUTH_ENDPOINT = 'https://oauth.reddit.com'
        get_param = {
            'limit': limit #X Posts
        }
        get_headers = {
            'User-Agent': 'our Bot 1.0',
            'Authorization' : 'Bearer ' + self.tokenID
        }
        response = requests.get(OAUTH_ENDPOINT + '/r/' + subReddit + '/new/', headers = get_headers, params = get_param)
        #print(response.json()) #JSON format of the most recent post on r/FashionReps
                               #I manually checked and the post Titles Match!!!
        data1 = response.json()  
        #print(data1)       
        #for post in data['data']['children']: # Navigates through each post
        #    print('POST : ' + post['data']['id'])
        #    print(post['data']['title'])
        #    print(post['data']['selftext']) 
        #['data]['children']['data']['body']
        #post_id = data['data']['children'][33]['data']['id']  # Replace with the actual post ID you want to retrieve comments for
        
        #post_id = data['data']['children'][3]['data']['id']
        #comments = requests.get(OAUTH_ENDPOINT + '/r/' + subReddit + '/comments/' + post_id, headers = get_headers, params = get_param) #/r/[subreddit]/comments/[id]
        #data = comments.json()
        #print(data)
        #return response
        
        commentDictionary = {}
        
        for i in range(limit):
            post_id = data1['data']['children'][i]['data']['id']
            
            """ This Gets Our TimeStamp
            created_utc = data1['data']['children'][i]['data']['created_utc'] ## Time Stamp Of Post
            import datetime
            datetime_obj = datetime.datetime.utcfromtimestamp(created_utc)
            formatted_datetime = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
            print(formatted_datetime)
            """
            
            comments = requests.get(OAUTH_ENDPOINT + '/r/' + subReddit + '/comments/' + post_id, headers = get_headers, params = get_param) #/r/[subreddit]/comments/[id]
            data = comments.json()
            #print(created_utc)
            commentDictionary[post_id] = None # add post key
            
            for post in data[1]['data']['children']: # Navigates through each comment in a post
                try:
                    if(post['data']['author'] == 'AutoModerator' or post['data']['author'] == 'Panda-Decode' or post['data']['author'] =='Fashionreps_Linkify'): # This is for fashionReps
                        continue #very common bots on fashionReps subreddit
                    #print("Comment HERE: ")
                    #print(post['data']['body'])
                    if commentDictionary[post_id] is None:
                        commentDictionary[post_id] = [(post['data']['body'], post['data']['id'])]
                    else:
                        commentDictionary[post_id].append((post['data']['body'], post['data']['id']))
                except Exception as e:
                    print('Comment Fail: 1')
        
        return response, commentDictionary
        

if __name__ == "__main__":

    with open('info.json', 'r') as file:
        info = json.load(file)

    Bot = CrawlApiR(info['clientID'], info['secretID'], info['userID'], info['userPass'])
    Bot.tokenAuthenticate() #Should Print OK #If Not, we requested again too fast
    Bot.useToken_Post(info['subreddit-1'], 5) #"r/FashionReps" ~ 'FashionReps'



    