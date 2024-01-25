# Warning: Database is no longer active
# Research Reports folder holds pipeline progress documentation
---------------------------------------------------------------------------------------------
# Summary of code and functionality

The goal of our code is to visualize the data we extracted from eBay and Reddit and stored it in our database. When you run the code, you are given the option to customize the parameter of two different graphs. The first graph allows you to pick a category of clothing and compare the average prices of the listings of eBay listings to the US Labor Statistics data. The second graph allows you to pick from big-name brands and misc options to see the prevalence of discussion in our two main subreddits, r/findfashion and r/fashionreps.


## app.py

**Imports**:

Imports necessary libraries like Dash, Plotly Express, and Pandas.
Uses a custom module Scavenge to retrieve and process data.
Prepares dataframes ebayPrices and averagePrices representing prices from eBay and average prices (from the Consumer Price Index via US Bureau of Labor Statistics), respectively.
Combines these dataframes into combinedPrices.
Retrieves popularity data of different fashion brands from Reddit (from findfashion and fashionreps subreddits) and stores them in respective dataframes, which are then combined into combinedHype.

**Dash App**:

Initializes a Flask server and a Dash app.
Sets up the layout of the Dash app, which includes HTML components and Dropdowns for selecting categories and brands.
Includes two sections: one for displaying eBay category prices and another for displaying brand popularity on Reddit.

**Graphs and Callbacks**:

Defines two callback functions that update the graphs based on user interaction.
The first callback (update_category_price_graph) updates a bar graph showing eBay and average prices for a selected category.
The second callback (update_popularity_graph) updates a bar graph showing the popularity of selected brands on the findfashion and fashionreps Reddit platforms.

**Server Routing and Execution**:

Defines a route in the Flask app to redirect the base URL to the dashboard.
Runs the Flask app with debug mode on.

Overall, the script provides an interactive platform for analyzing and comparing fashion prices and brand popularity trends based on Reddit data. Users can select different categories and brands from dropdown menus to visualize the corresponding data in bar graphs.

## plots.py

**Data Collection and Initialization**:

Imports a custom module Scavenge for data collection, mysql.connector for database interactions, and various other modules for data handling and visualization.
Initializes a connection to a MySQL database and populates data using the Scavenge object.

**Analysis and Visualization Functions**:

tableOne(dataObject): Analyzes brand popularity across different fashion categories from the findfashionList dataset. It uses defined category mappings to classify data and then visualizes this information in a table format using matplotlib.

ebayPrice(dataObject): Computes and plots the average price of different fashion categories based on data from eBay.

threeDataSets(dataObject): Compares the distribution of fashion categories across three datasets (ebayList, findfashionList, and fashionrepsList) and visualizes this comparison using scatter plots.

twoDataSets(dataObject): Analyzes the popularity of various fashion brands in two Reddit subreddits (r/findfashion and r/fashionreps) and visualizes the data with scatter plots.

moderateHateSpeechFigureFind(dataObject), moderateHateSpeechFigureReps(dataObject), and moderateHateSpeechFigurePol(dataObject): These functions analyze the level of flagged versus non-flagged comments (presumably for hate speech) in different Reddit subreddits and visualize the results in bar charts.

rPoliticsFigure(dataObject): Visualizes the number of posts in the r/politics subreddit over a specific period in November 2023 using a line plot.

## scavenge.py

**Class Initialization**:

Initializes the Scavenge class with lists for storing data from eBay, fashionreps, findfashion, and politics subreddits.
Establishes a connection to a MySQL database. If a connection (cxn) is provided, it uses that; otherwise, it creates a new connection using the mydb configuration.

**Closing Database Connection (close function)**:

Closes the database cursor and connection.

**Populating Data (populate function)**:

Connects to the database and executes SQL queries to fetch data from redditPosts and ebayPosts.
Processes the fetched data, categorizing Reddit posts into fashionrepsList, findfashionList, and politicsList based on the subreddit they belong to. eBay posts are stored in ebayList.
For each Reddit post, associated comments are also fetched and stored along with the post.

**Printing Data (print function)**:

Iterates over the lists (ebayList, fashionrepsList, findfashionList, politicsList) and prints a subset of the stored data to the console for verification or analysis purposes.

**eBay Prices Analysis (ebayPrices function)**:

Analyzes eBay data to calculate average prices for different categories like shoes, shirts, dresses, etc.
Uses a mapping of categories to match items to their respective categories and calculates the average price for each category.

**Reddit Data Analysis (twoDataSets function)**:

Analyzes the popularity of various brands in the findfashion and fashionreps subreddits.
Uses brand mappings to count occurrences of each brand in the post titles from these subreddits.

To run:
- Activate Python env variable
- pipinstall pandas, plotly, flask, dash
- Run on: http://127.0.0.1:5000/dashboard/
