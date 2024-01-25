from varDB import mydb
import json
import mysql.connector

class Scavenge():
    
    def __init__(self, cxn):
        self.ebayList = []
        self.fashionrepsList = []
        self.findfashionList = []
        self.politicsList = []
        self.cxn = cxn
    
    def close(self):
        self.cursor.close()
        self.cxn.close()
        
    def populate(self):
        self.cursor = self.cxn.cursor()
    
        databases = ("show databases")
        self.cursor.execute(databases)
        for x in self.cursor:
            print(x)
            
        # Execute the SELECT query
        # Remove LIMIT for widescale use, large run time however!
        query = "SELECT * FROM redditPosts LIMIT 0, 100"
        #query = "SELECT * FROM redditPosts"
        self.cursor.execute(query)

        # Fetch all rows
        postRows = self.cursor.fetchall()
        
        query = "SELECT * FROM ebayPosts LIMIT 0, 100"
        #query = "SELECT * FROM ebayPosts"
        self.cursor.execute(query)

        # Fetch all rows
        ebayRows = self.cursor.fetchall()
        
        for ebayRow in ebayRows:
            self.ebayList.append((ebayRow))
            
        # Use postID to filter based on subreddits,
        for postRow in postRows:
            ID = postRow[0]
            subReddit = postRow[4]
            
            #Get redditCommentsInPost
            query = "SELECT * from redditCommentsInPost where postID = %s"
            self.cursor.execute(query, (ID,))
            commentRows = self.cursor.fetchall()
            
            if(subReddit == "FashionReps"):
                #print("Adding to FashionReps ... ")
                #print((postRow, commentRows))
                self.fashionrepsList.append((postRow, commentRows))
            elif(subReddit == "findfashion"):
                #print("Adding to findfashion ... ")
                #print((postRow, commentRows))
                self.findfashionList.append((postRow, commentRows))
            elif(subReddit == "politics"):
                #print("Adding to politics ... ")
                #print((postRow, commentRows))
                self.politicsList.append((postRow, commentRows))
                
    def print(self):
        i = 0
        for row in self.ebayList:
            print(f"ebay Post {i}:")
            print(row)
            i = i + 1
            if(i == 5):
                break
        i = 0
        for touple in self.fashionrepsList:
            print(f"r/fashionreps Post {i}:")
            print(touple[0])
            
            print(f"r/fashionreps Post {i} comments:")
            print(touple[1])
            i = i + 1
            if(i == 5):
                break
        i = 0 
        for touple in self.findfashionList:
            print(f"r/findfashion Post {i}:")
            print(touple[0])
            
            print(f"r/findfashion Post {i} comments:")
            print(touple[1])
            i = i + 1
            if(i == 5):
                break
        i = 0    
        for touple in self.politicsList:
            print(f"r/politics Post {i}:")
            print(touple[0])
            
            print(f"r/politics Post {i} comments:")
            print(touple[1])
            i = i + 1
            if(i == 5):
                break
        
if __name__ == '__main__':
    connection = mysql.connector.connect(**mydb)
    
    test = Scavenge(connection)
    test.populate()
    test.print()
    print("Hello")
    