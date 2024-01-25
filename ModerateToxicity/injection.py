from controllerTX import ModerateToxicity
from varDB import mydb
import json
import mysql.connector

if __name__ == '__main__':
    connection = mysql.connector.connect(**mydb)
    print(connection)
    cursor = connection.cursor()

    databases = ("show databases")
    cursor.execute(databases)
    for x in cursor:
        print(x)
        
    # Execute the SELECT query
    #query = "SELECT * FROM redditCommentsInPost;"
    query = "SELECT * FROM redditCommentsInPost where id > 13324;"
    cursor.execute(query)

    # Fetch all rows
    rows = cursor.fetchall()
    
    #Get toxic api 
    with open('info.json', 'r') as file:
        info = json.load(file)
    toxicity = ModerateToxicity(info["clientID"])

    # Print or process the rows as needed
    for row in rows:
        ID = row[0]
        comment = row[2]
        toxicTouple = toxicity.evaluateToxicity(comment)
        
        confidence = toxicTouple[0]
        flag = toxicTouple[1]
        
        print(str(ID) + " : " + comment)
        print(str(confidence) + " : " + str(flag))
        
        # Example values for the update
        new_value_for_column1 = str(flag)
        new_value_for_column2 = confidence
        condition_column = 'id'
        condition_value = ID

        # Execute the UPDATE query to update two specific columns in a specific row
        update_query = f"UPDATE redditCommentsInPost SET flag = %s, confidence = %s WHERE {condition_column} = %s;"
        cursor.execute(update_query, (new_value_for_column1, new_value_for_column2, condition_value))
        
        connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()
        