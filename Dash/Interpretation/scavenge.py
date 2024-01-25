from .varDB import mydb
import json
import mysql.connector

class Scavenge():
    

    def __init__(self, cxn=None):
        self.ebayList = []
        self.fashionrepsList = []
        self.findfashionList = []
        self.politicsList = []
        self.cxn = cxn if cxn else mysql.connector.connect(**mydb)
    
    def close(self):
        self.cursor.close()
        self.cxn.close()
        
    def populate(self):
        self.cursor = self.cxn.cursor()

        """
        databases = ("show databases")
        self.cursor.execute(databases)
        for x in self.cursor:
        print(x)
        """
       
        # Execute the SELECT query
        # Remove LIMIT for widescale use, large run time however!
        #query = "SELECT * FROM redditPosts LIMIT 0, 100"
        query = "SELECT * FROM redditPosts"
        self.cursor.execute(query)

        # Fetch all rows
        postRows = self.cursor.fetchall()
        
        #query = "SELECT * FROM ebayPosts LIMIT 0, 100"
        query = "SELECT * FROM ebayPosts"
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
    
    def ebayPrices(self):
        
        x_values = ['shoes', 'shirts', 'dresses', 'pants', 'headwear', 'jackets', 'accessory', 'misc']
        y_EBAY =    [0, 0, 0, 0, 0, 0, 0, 0]

        category_mappings = {
            'shoes' : ['boots', 'heels', "girls' shoes", 'flats', 'shoes', 'sneakers', 'timbs', 'jordans', 'sneaker', 'jordan', 'dunks', 'boot'],
            'shirts': ['tops', 'aprons', 't-shirts', 'shirt', 'shirts', 'tshirt', 'top', 'hoodie'], 
            'dresses' : ['dress', 'dresses', 'gown'],
            'pants': ['shorts', 'pants', 'skirts', 'bottoms', 'jeans', 'khaki', 'khakis', 'trousers'],
            'headwear': ['hat', 'hats & headgear', 'glasses', 'hats', 'helmets', 'goggles & sunglasses', 'shades', 'sunglasses', 'raybans', 'earring'],
            'coat/jacket': ['puffers', 'puffer', 'sweaters', 'jackets', 'hoodies & sweatshirts', 'coats, jackets & vests', 'coat', 'moncler', 'jacket', 'canada goose', 'goose', 'northface', 'guess'],
            'accessory': ['wristwatches', 'clothing & accessories', 'medals', 'gloves & mittens', 'jewelry', 'necklace', 'ring'],
            'misc': []  # Assuming anything not covered falls into the 'misc' category
            }
        cash_map = {
                'shoes' : [0,1], 
                'shirts' : [0,1], 
                'dresses' : [0,1], 
                'pants' : [0,1],
                'headwear' : [0,1],
                'coat/jacket' : [0,1],
                'accessory' : [0,1],
                'misc' : [0,1]
            }
        for row in self.ebayList:
            category = row[5]
            price = row[2]
            if category in category_mappings['shoes']:
                cash_map['shoes'][0] += price
                cash_map['shoes'][1] += 1
            elif category in category_mappings['shirts']:
                cash_map['shirts'][0] += price
                cash_map['shirts'][1] += 1
            elif category in category_mappings['dresses']:
                cash_map['dresses'][0] += price
                cash_map['dresses'][1] += 1
            elif category in category_mappings['pants']:
                cash_map['pants'][0] += price
                cash_map['pants'][1] += 1
            elif category in category_mappings['headwear']:
                cash_map['headwear'][0] += price
                cash_map['headwear'][1] += 1
            elif category in category_mappings['coat/jacket']:
                cash_map['coat/jacket'][0] += price
                cash_map['coat/jacket'][1] += 1
            elif category in category_mappings['accessory']:
                cash_map['accessory'][0] += price
                cash_map['accessory'][1] += 1
            else: #misc
                cash_map['misc'][0] += price
                cash_map['misc'][1] += 1

        y_EBAY =   [round(cash_map['shoes'][0] / cash_map['shoes'][1], 2),
                    round(cash_map['shirts'][0] / cash_map['shirts'][1], 2),
                    round(cash_map['dresses'][0] / cash_map['dresses'][1], 2),
                    round(cash_map['pants'][0] / cash_map['pants'][1], 2),
                    round(cash_map['headwear'][0] / cash_map['headwear'][1], 2),
                    round(cash_map['coat/jacket'][0] / cash_map['coat/jacket'][1], 2),
                    round(cash_map['accessory'][0] / cash_map['accessory'][1], 2),
                    round(cash_map['misc'][0] / cash_map['misc'][1], 2)]
        
        return y_EBAY
    
    def twoDataSets(self):
    # use brand names
    
        x_values = ['nike', 'addidas', 'gucci', 'versace', 'prada', 'guess', 'balenciaga', 'moncler', 'canada goose', 'new balance', 'misc']
        y_REDDIT1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        y_REDDIT2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        category_mappings = {
            'nike' : ['nike', 'dunks', 'airforce', 'blazer', 'flyknit'],
            'addidas': ['addidas', 'nmd', 'yeezy', 'superstar', 'ultraboost'], 
            'gucci' : ['gucci'],
            'versace': ['versace'],
            'prada': ['prada'],
            'guess': ['guess'],
            'balenciaga': ['balenciaga'],
            'moncler': ['moncler', 'monc'],
            'canada goose' : ['canada goose', 'goose', 'canada', 'canadagoose'],
            'new balance' : ['new balance' ,'balance', 'newbalance'],
            'misc' : []
            }
        fast_map = {
                'nike' : 0, 
                'addidas' : 1,
                'gucci' : 2,
                'versace' : 3,
                'prada' : 4,
                'guess' : 5,
                'balenciaga' : 6,
                'moncler' : 7,
                'canada goose' : 8,
                'new balance' : 9,
                'misc' : 10
            }

        for touple in self.findfashionList:
            post = touple[0]
            title = post[1].lower()
            
            for key, value in category_mappings.items():
                found = False
                
                if(key == 'misc'):
                    index = fast_map[key]
                    y_REDDIT1[index] += 1
                    break
                
                for element in value:
                    
                    substring = element
                    
                    if substring in title:
                        # increment category
                        index = fast_map[key]
                        y_REDDIT1[index] += 1
                        found = True
                        break
                    else:
                        # check once more with another s or -s
                        substring1 = substring + 's'
                        substring2 = substring[:-1]
                        if substring1 in title:
                            # increment category
                            index = fast_map[key]
                            y_REDDIT1[index] += 1
                            found = True
                            break
                        elif substring2 in title:
                            # increment category
                            index = fast_map[key]
                            y_REDDIT1[index] += 1
                            found = True
                            break
                
                if(found): #If we found a category already, go to next post
                    break

        for touple in self.fashionrepsList:
            post = touple[0]
            title = post[1].lower()
            
            for key, value in category_mappings.items():
                found = False
                
                if(key == 'misc'):
                    index = fast_map[key]
                    y_REDDIT2[index] += 1
                    break
                
                for element in value:
                    
                    substring = element
                    
                    if substring in title:
                        # increment category
                        index = fast_map[key]
                        y_REDDIT2[index] += 1
                        found = True
                        break
                    else:
                        # check once more with another s or -s
                        substring1 = substring + 's'
                        substring2 = substring[:-1]
                        if substring1 in title:
                            # increment category
                            index = fast_map[key]
                            y_REDDIT2[index] += 1
                            found = True
                            break
                        elif substring2 in title:
                            # increment category
                            index = fast_map[key]
                            y_REDDIT2[index] += 1
                            found = True
                            break
                
                if(found): #If we found a category already, go to next post
                    break
    
        return (y_REDDIT1, y_REDDIT2)
    
        
if __name__ == '__main__':
    connection = mysql.connector.connect(**mydb)
    
    test = Scavenge(connection)
    test.populate()
    test.print()
    print("Hello")
    