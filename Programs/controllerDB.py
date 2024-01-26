import json
import mysql.connector
from RedditCrawlBot.controller import CrawlApiR
from EBaYCrawlBot.controller import CrawlApiE
from ModerateToxicity.controllerTX import ModerateToxicity
from varDB import mydb

import faktory
from faktory import Worker
import logging
import time

faktory_url = "tcp://localhost:7419"

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')

def querieReddit(touple):

    connection = mysql.connector.connect(**mydb)
    #print(connection)
    cursor = connection.cursor()

    #databases = ("show databases")
    #cursor.execute(databases)
    #for x in cursor:
    #    print(x)
    
    insert_query = "INSERT INTO redditPosts (Title, Body, PostKey, subReddit, dateOfPost) VALUES (%s, %s, %s, %s, %s)" #SQL querie
    
    postdata = touple[0]
    commentDictionary = touple[1]
    response = postdata.json()
    
    for post in response['data']['children']:
        #Prevent Duplicate ReEntry
        search_value = post['data']['id']
        ##Finding Date Of Post
        created_utc = post['data']['created_utc']
        import datetime
        datetime_obj = datetime.datetime.utcfromtimestamp(created_utc)
        dateOfPost = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
        #print(dateOfPost)
            
        query = "SELECT * FROM redditPosts WHERE PostKey = %s" #SQL querie
        cursor.execute(query, (search_value,))
        matching_rows = cursor.fetchall()
        
        
        
        if(matching_rows): #Duplicate!
            # We have a chance to repopulate comments
            try:
                postID = post['data']['id']
                query = "SELECT * FROM redditPosts WHERE PostKey = %s"
                cursor.execute(query, (search_value,))
                referenceID = cursor.fetchone()[0]
                
                if commentDictionary[postID] is not None:   
                    for touple in commentDictionary[postID]:
                        comment = touple[0]
                        comID = touple[1]
                        insert_query2 = "INSERT INTO redditCommentsInPost (PostID, comment, commentID, flag, confidence) VALUES (%s, %s, %s, %s, %s)" #SQL querie
                        #Moderate Toxicity!!!
                        Toxicity = ModerateToxicity("677c38449a417eae797ce481bfcba53b")
                        toxicTouple = Toxicity.evaluateToxicity(comment)
                        confidence = toxicTouple[0]
                        flag = toxicTouple[1]
                        data_to_insert2 = (referenceID, comment, comID, flag, confidence)
                        #check if comment already exists in post
                        search_value = comID
                        query = "SELECT * FROM redditCommentsInPost WHERE commentID = %s" #SQL querie
                        cursor.execute(query, (search_value,))
                        matching_rows = cursor.fetchall()
                        if(matching_rows):
                            continue #skip rest of this loop, dont add duplicate comments to table redditCommentsInPost
                        cursor.execute(insert_query2, data_to_insert2)
                        connection.commit() 
            except Exception as e:
                 print('Comment Fail: 2')
                 
            continue #skip rest of the function, dont add duplicate to table redditPosts
        
        data_to_insert = (post['data']['title'], post['data']['selftext'], post['data']['id'], post['data']['subreddit'], dateOfPost)
        cursor.execute(insert_query, data_to_insert)
        connection.commit()
        
        
        # Extract primary key ID from post inserted into redditPosts
        cursor.execute("SELECT * FROM redditPosts ORDER BY ID DESC LIMIT 1")
        referenceID = cursor.fetchone()[0]
        #print(referenceID)
        # Now add comments in redditCommentsInPost
        # Referencing this specific post primary key ID
        
        postID = post['data']['id']
        #print(commentDictionary[postID])
        if commentDictionary[postID] is not None:   
            for touple in commentDictionary[postID]:
                comment = touple[0]
                comID = touple[1]
                insert_query2 = "INSERT INTO redditCommentsInPost (PostID, comment, commentID, flag, confidence) VALUES (%s, %s, %s, %s, %s)" #SQL querie
                #Toxicity
                Toxicity = ModerateToxicity("677c38449a417eae797ce481bfcba53b")
                toxicTouple = Toxicity.evaluateToxicity(comment)
                confidence = toxicTouple[0]
                flag = toxicTouple[1]
    
                data_to_insert2 = (referenceID, comment, comID, flag, confidence)
                cursor.execute(insert_query2, data_to_insert2)
                connection.commit() 
        
    cursor.close()
    connection.close()
    
def insertEbayData(items):
    
    connection = mysql.connector.connect(**mydb)
    #print(connection)
    cursor = connection.cursor()
    for item in items:
        cat = item.categoryname.string.lower()
        title = item.title.string.lower().strip()
        price = float(item.currentprice.string)
        url = item.viewitemurl.string.lower()
        seller = item.sellerusername.text.lower()
        itemid = str(item.itemid.string.lower())
        cursor.execute("SELECT EXISTS (SELECT 1 FROM pipeline.ebayPosts WHERE itemid = %s) AS item_exists;", (itemid,))
        item_exists = cursor.fetchall()
        if not item_exists[0][0]:
            cursor.execute("INSERT into ebayPosts (Category, Title, Price, Seller, URL, itemid) VALUES(%s, %s, %s, %s, %s, %s)", (cat, title, price, seller, url, itemid,))
            print("Inserted into DB with title: " + str(title))
            print(url)
        else:
            print("Duplicate found with title: " + str(title))
    connection.commit()
    cursor.close()
    connection.close()

def query_reddit_task():
    with open('RedditCrawlBot/info.json', 'r') as file:
        info = json.load(file)
    redditBot = CrawlApiR(info['clientID'], info['secretID'], info['userID'], info['userPass'])
    redditBot.tokenAuthenticate() #Should Print OK #If Not, we requested again too fast
   
    touple = redditBot.useToken_Post(info['subreddit-1'], 100) #"r/FashionReps" ~ 'FashionReps'
    querieReddit(touple)
    touple = redditBot.useToken_Post(info['subreddit-2'], 100) #Do not go over 100 posts pulled per request ~ Find Fashion
    querieReddit(touple)
    touple = redditBot.useToken_Post(info['subreddit-3'], 100) #Do not go over 100 posts pulled per request ~ Politics
    querieReddit(touple)

def query_ebay_task():
    with open('EBaYCrawlBot/info.json', 'r') as file:
        info = json.load(file)
    ebayBot = CrawlApiE(info['clientID'], info['secretID'], info['userID'], info['userPass'])
    ebayBot.fetch('apparel')
    ebayListings = ebayBot.parse()
    insertEbayData(ebayListings)

if __name__ == "__main__":

    w = Worker(faktory = faktory_url, queues=['default'], concurrency=1, use_threads=True)
    w.register('query_reddit_task', query_reddit_task)
    w.register('query_ebay_task', query_ebay_task)

    import threading
    threading.Thread(target=w.run).start()

    while True:
        with faktory.connection() as client:
            # Schedule the Reddit task
            client.queue('query_reddit_task')
            
            # Schedule the eBay task
            client.queue('query_ebay_task')

        #Sleep for 6 hours
        time.sleep(21600)
    # print("starts ebay")
    
    #response = redditBot.useToken_Post(info['subreddit-2'])
    #querieReddit(response)