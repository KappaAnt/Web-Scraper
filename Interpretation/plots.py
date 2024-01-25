from scavenge import Scavenge
import mysql.connector
from varDB import mydb
import matplotlib.pyplot as plt

def tableOne(dataObject):

    findfashionList = dataObject.findfashionList
    brand = None
    category = None

    column_labels = ['nike', 'addidas', 'gucci', 'versace', 'prada', 'guess', 'balenciaga', 'moncler', 'canada goose', 'new balance', 'misc']
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
    category_mappings2 = {
        'shoes' : ['boots', 'heels', "girls' shoes", 'flats', 'shoes', 'sneakers', 'timbs', 'jordans', 'sneaker', 'jordan', 'dunks', 'boot'],
        'shirts': ['tops', 'aprons', 't-shirts', 'shirt', 'shirts', 'tshirt', 'top', 'hoodie'], 
        'dresses' : ['dress', 'dresses', 'gown'],
        'pants': ['shorts', 'pants', 'skirts', 'bottoms', 'jeans', 'khaki', 'khakis', 'trousers'],
        'headwear': ['hat', 'hats & headgear', 'glasses', 'hats', 'helmets', 'goggles & sunglasses', 'shades', 'sunglasses', 'raybans', 'earring'],
        'coat/jacket': ['puffers', 'puffer', 'sweaters', 'jackets', 'hoodies & sweatshirts', 'coats, jackets & vests', 'coat', 'moncler', 'jacket', 'canada goose', 'goose', 'northface', 'guess'],
        'accessory': ['wristwatches', 'clothing & accessories', 'medals', 'gloves & mittens', 'jewelry', 'necklace', 'ring'],
        'misc': []  # Assuming anything not covered falls into the 'misc' category
        }
    row_labels = ['shoes', 'shirts', 'dresses', 'pants', 'headwear', 'jackets', 'accessory', 'misc']
    fast_map = {
        'shoes' : 0, 
        'shirts' : 1,
        'dresses' : 2,
        'pants' : 3,
        'headwear' : 4,
        'jackets' : 5,
        'accessory' : 6,
        'misc' : 7,
    }
    fast_map2 = {
        'nike': 0,
        'addidas': 1,
        'gucci': 2, 
        'versace': 3, 
        'prada': 4, 
        'guess': 5, 
        'balenciaga': 6, 
        'moncler': 7, 
        'canada goose': 8, 
        'new balance': 9, 
        'misc': 10
    }

    data = rows, cols = 8, 11
    matrix = [[0 for _ in range(cols)] for _ in range(rows)]
    #print(matrix)

    for touple in findfashionList:
        post = touple[0]
        title = post[1].lower()
        
        for key, value in category_mappings.items():
            found = False
            
            if(key == 'misc'):
                break
            
            for element in value:
                
                substring = element
                
                if substring in title: # find brand
                    brand = key
                    found = True
                else:
                    # check once more with another s or -s
                    substring1 = substring + 's'
                    substring2 = substring[:-1]
                    if substring1 in title:
                        brand = key
                        found = True
                    elif substring2 in title:
                        brand = key
                        found = True
            
            if(found): #If we found a category already, go to next post
                break


        for key, value in category_mappings2.items():
            found = False
            
            if(key == 'misc'):
                break
            
            for element in value:
                
                substring = element
                
                if substring in title: # find brand
                    category = key
                    found = True
                else:
                    # check once more with another s or -s
                    substring1 = substring + 's'
                    substring2 = substring[:-1]
                    if substring1 in title:
                        category = key
                        found = True
                    elif substring2 in title:
                        category = key
                        found = True
            
            if(found): #If we found a category already, go to next post
                break

        brand_mapped = False
        category_mapped = False
            

        # Map the brand to a column in the matrix
        for key, values in category_mappings.items():
            if brand in values:
                col_index = fast_map2[key]
                brand_mapped = True
                break
        
        if not brand_mapped:
            col_index = fast_map2['misc']

        # Map the category to a row in the matrix
        for key, values in category_mappings2.items():
            if category in values:
                row_index = fast_map[key]
                category_mapped = True
                break

        if not category_mapped:
            row_index = fast_map['misc']

        # Increment the count in the matrix
        #print("row index: " + str(row_index))
        #print("col index: " + str(col_index ))
        matrix[row_index][col_index] += 1
    
    #print(matrix)

    fig, ax = plt.subplots()
    plt.rcParams["figure.dpi"] = 100
    ax.axis('tight')
    ax.axis('off')

    plt.title('Table 1. Average Brands by Category on r/findFashion', fontweight ="bold")

    table = ax.table(cellText=matrix, colLabels=column_labels, rowLabels=row_labels, loc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    # Display the table
    plt.show()
    pass



def ebayPrice(dataObject):
    ebayList = dataObject.ebayList
    
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
            'shoes' : [0,0], 
            'shirts' : [0,0], 
            'dresses' : [0,0], 
            'pants' : [0,0],
            'headwear' : [0,0],
            'coat/jacket' : [0,0],
            'accessory' : [0,0],
            'misc' : [0,0]
        }
    for row in ebayList:
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
    
    y_EBAY[0] = cash_map['shoes'][0] / cash_map['shoes'][1]
    y_EBAY[1] = cash_map['shirts'][0] / cash_map['shirts'][1]
    y_EBAY[2] = cash_map['dresses'][0] / cash_map['dresses'][1]
    y_EBAY[3] = cash_map['pants'][0] / cash_map['pants'][1]
    y_EBAY[4] = cash_map['headwear'][0] / cash_map['headwear'][1]
    y_EBAY[5] = cash_map['coat/jacket'][0] / cash_map['coat/jacket'][1]
    y_EBAY[6] = cash_map['accessory'][0] / cash_map['accessory'][1]
    y_EBAY[7] = cash_map['misc'][0] / cash_map['misc'][1]
    
    # Plotting the first 
    plt.scatter(x_values, y_EBAY, label='ebay', color='green', marker='o')
    
    # Add labels and title
    plt.xlabel('Category Type')
    plt.ylabel('Average Price')
    plt.title('Ebay Average Price Ranges by Category')

    # Show the plot
    plt.show()

    #plotting table

def threeDataSets(dataObject):
    ebayList = dataObject.ebayList
    findfashionList = dataObject.findfashionList
    fashionrepsList = dataObject.fashionrepsList
    
    x_values = ['shoes', 'shirts', 'dresses', 'pants', 'headwear', 'jackets', 'accessory', 'misc']
    y_EBAY =    [0, 0, 0, 0, 0, 0, 0, 0]
    y_REDDIT1 = [0, 0, 0, 0, 0, 0, 0, 0]
    y_REDDIT2 = [0, 0, 0, 0, 0, 0, 0, 0]
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
    fast_map = {
            'shoes' : 0, 
            'shirts' : 1,
            'dresses' : 2,
            'pants' : 3,
            'headwear' : 4,
            'coat/jacket' : 5,
            'accessory' : 6,
            'misc' : 7
        }
    for row in ebayList:
        category = row[5]
        if category in category_mappings['shoes']:
            y_EBAY[0] += 1
        elif category in category_mappings['shirts']:
            y_EBAY[1] += 1
        elif category in category_mappings['dresses']:
            y_EBAY[2] += 1
        elif category in category_mappings['pants']:
            y_EBAY[3] += 1
        elif category in category_mappings['headwear']:
            y_EBAY[4] += 1
        elif category in category_mappings['coat/jacket']:
            y_EBAY[5] += 1
        elif category in category_mappings['accessory']:
            y_EBAY[6] += 1
        else: #misc
            y_EBAY[7] += 1
    
    # Plotting the first 
    plt.scatter(x_values, y_EBAY, label='ebay', color='green', marker='o')

    for touple in findfashionList:
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

    # Plotting the second 
    plt.scatter(x_values, y_REDDIT1, label='r/findfashion', color='red', marker='o')

    for touple in fashionrepsList:
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
    
    # Plotting the third 
    plt.scatter(x_values, y_REDDIT2, label='r/fashionreps', color='orange', marker='o')

    # Add labels and title
    plt.xlabel('Category Type')
    plt.ylabel('Times Listed')
    plt.title('Category Variety Between DataSets')
 
    # Add a legend to differentiate between the lines
    plt.legend()

    # Show the plot
    plt.show()
    
def twoDataSets(dataObject):
    # use brand names
    findfashionList = dataObject.findfashionList
    fashionrepsList = dataObject.fashionrepsList
    
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

    for touple in findfashionList:
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

    # Plotting the first 
    plt.scatter(x_values, y_REDDIT1, label='r/findfashion', color='red', marker='o')

    for touple in fashionrepsList:
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
    
    # Plotting the second 
    plt.scatter(x_values, y_REDDIT2, label='r/fashionreps', color='orange', marker='o')

    # Add labels and title
    plt.xlabel('Hype Brands')
    plt.ylabel('Times Listed')
    plt.title('Brand Variety on SubReddits')

    # Add a legend to differentiate between the lines
    plt.legend()

    # Show the plot
    plt.show()

def moderateHateSpeechFigureFind(dataObject):
    findList = dataObject.findfashionList
    
    #List Toxicity From ModerateHateSpeech on r/Pol
    x_values = ['Flagged', 'Not Flagged']
    y_values = [0, 0]
    
    for touple in findList:
        for comment in touple[1]:
            #print(comment)
            flagStatus = comment[4]
            if(flagStatus == 'normal'):
                y_values[1] = y_values[1] + 1
            elif(flagStatus == 'flag'):
                y_values[0] = y_values[0] + 1

    # Create a simple plot
    plt.bar(x_values, y_values)

    # Add labels and title
    plt.xlabel('Toxicity')
    plt.ylabel('Comments Posted')
    plt.title('ModerateHateSpeech API on r/findfashion')

    # Show the plot
    plt.show()
    
def moderateHateSpeechFigureReps(dataObject):
    repList = dataObject.fashionrepsList
    
    #List Toxicity From ModerateHateSpeech on r/Pol
    x_values = ['Flagged', 'Not Flagged']
    y_values = [0, 0]
    
    for touple in repList:
        for comment in touple[1]:
            #print(comment)
            flagStatus = comment[4]
            if(flagStatus == 'normal'):
                y_values[1] = y_values[1] + 1
            elif(flagStatus == 'flag'):
                y_values[0] = y_values[0] + 1

    # Create a simple plot
    plt.bar(x_values, y_values)

    # Add labels and title
    plt.xlabel('Toxicity')
    plt.ylabel('Comments Posted')
    plt.title('ModerateHateSpeech API on r/fashionreps')

    # Show the plot
    plt.show()
    
def moderateHateSpeechFigurePol(dataObject):
    polList = dataObject.politicsList
    
    #List Toxicity From ModerateHateSpeech on r/Pol
    x_values = ['Flagged', 'Not Flagged']
    y_values = [0, 0]
    
    for touple in polList:
        for comment in touple[1]:
            #print(comment)
            flagStatus = comment[4]
            if(flagStatus == 'normal'):
                y_values[1] = y_values[1] + 1
            elif(flagStatus == 'flag'):
                y_values[0] = y_values[0] + 1

    # Create a simple plot
    plt.bar(x_values, y_values)

    # Add labels and title
    plt.xlabel('Toxicity : 11/1 - 11/30')
    plt.ylabel('Comments Posted')
    plt.title('ModerateHateSpeech API on r/pol')

    # Show the plot
    plt.show()


def rPoliticsFigure(dataObject):
    polList = dataObject.politicsList

    #November 1st, 2023 until November 14th, 2023.
    x_values = []
    for i in range(14):
        day = str(i + 1)
        x_values.append(f'11/{day}')
        
    y_values = [100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] 
    yDictionary = {}   
    for touple in polList:
        date = touple[0][5]
        #print(date)
        day = date[8:10]
        dayInt = None
        if(day[0] == '0'):
            dayInt = int(day[1])
        else:
            dayInt = int(day)
            
        if(dayInt > 14):
            break
        
        if yDictionary.get(dayInt) is not None:
            #Key Value Found
            yDictionary[dayInt] = yDictionary[dayInt] + 1
        else:
            #Key Value not Found
            yDictionary[dayInt] = 1

    for key, value in yDictionary.items():
        #print(f'{key}: {value}')
        y_values[key-1] = value

    # Create a simple plot
    plt.plot(x_values, y_values)

    # Add labels and title
    plt.xlabel('Day')
    plt.ylabel('# of Posts')
    plt.title('Posts on r/pol from Nov 1st - Nov 14th')

    # Show the plot
    plt.show()


if __name__ == "__main__":
    connection = mysql.connector.connect(**mydb)
    
    data = Scavenge(connection)
    data.populate()
    twoDataSets(data)                   #Figure 1
    threeDataSets(data)                 #Figure 2
    moderateHateSpeechFigurePol(data)   #Figure 3
    moderateHateSpeechFigureReps(data)  #Figure 4
    moderateHateSpeechFigureFind(data)  #Figure 5
    ebayPrice(data)                     #Figure 6
    rPoliticsFigure(data)               #Figure 7 *** 
    tableOne(data)                      #Table 1
    #test.populate()
    #test.print()
    
    
    """
    We Need at least 6 figures
        Your report must include at least one table and at least six figures that describe your dataset.
        These figures must be properly captioned, labeled, and referenced in the text. I.e., you need
        to tell us something about the figures in your text.

        Table vs Figure example https://www.google.com/url?sa=i&url=https%3A%2F%2Fslideplayer.com%2Fslide%2F1649784%2F&psig=AOvVaw2Vbgr_biO6YzblxZHoxGhL&ust=1701109328451000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCIip1KCk4oIDFQAAAAAdAAAAABAD
       
        At least one of your figures must have all your datasets on it. I.e., they should allow the
        reader to directly compare the datasets on the same x- and y-axis.
        
        At least one of your figures must have at least two of your datasets on it. This is a separate
        figure from the above, but it could be another figure that has all three datasets on it.
        
        At least one figure must use data from ModerateHatespeech.
        
        r/Pol plot for # of posts //Does not count as one of the six figures
            In addition to the above requirements, your report must contain one additional figure that
        plots on the x-axis time and on the y-axis the number of submissions that were made in the
        r/politics subreddit from November 1st, 2023 until November 14th, 2023. The x-axis should
        be binned daily. I.e., the plot should be the number of submissions that came in each each
        day from Nov 1st, 2023 to Nov 14th, 2023 (inclusive).
    """