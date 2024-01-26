import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from flask import Flask, redirect
from Interpretation.scavenge import Scavenge

# Interactive Querying for TWO of our previous analysis
# One parameter to be changed
data = Scavenge()
data.populate()

eBayList = data.ebayPrices()
print(eBayList)
ebayPrices = pd.DataFrame({
    'Category': ['shoes', 'shirts', 'dresses', 'pants', 'headwear', 'jackets', 'accessory', 'misc'],
    'Price': eBayList
})

averageList = [60, 30, 80, 70, 50, 100, 0, 0]  # From Consumer Price Index via US Bureau of Labor Statistics

averagePrices = pd.DataFrame({
    'Category': ['shoes', 'shirts', 'dresses', 'pants', 'headwear', 'jackets', 'accessory', 'misc'],
    'Price': averageList
})

# Combine eBay and average prices DataFrames
combinedPrices = pd.merge(ebayPrices, averagePrices, on='Category')
combinedPrices = combinedPrices.rename(columns={'Price_x': 'Price_ebay', 'Price_y': 'Price_usa-labor-statistics'})

redditListTouple = data.twoDataSets()
findfashion = redditListTouple[0]
fashionreps = redditListTouple[1]
print(findfashion)
print(fashionreps)

findfashionFrame = pd.DataFrame({
    'Brand': ['nike', 'adidas', 'gucci', 'versace', 'prada', 'guess', 'balenciaga', 'moncler', 'canada goose', 'new balance', 'misc'],
    'Popularity': findfashion
})

fashionrepsFrame = pd.DataFrame({
    'Brand': ['nike', 'adidas', 'gucci', 'versace', 'prada', 'guess', 'balenciaga', 'moncler', 'canada goose', 'new balance', 'misc'],
    'Popularity': fashionreps
})

# Combine findfashion and fashionreps DataFrames
combinedFashion = pd.merge(findfashionFrame, fashionrepsFrame, on='Brand')
combinedHype = combinedFashion.rename(columns={'Popularity_x': 'findfashion', 'Popularity_y': 'fashionreps'})


# Create Server Here
app = Flask(__name__)
dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dashboard/')

dash_app.layout = html.Div([
    html.H1("Fashion Prices and Trends Analysis"),

    # Pick what category to display for EBAY
    html.Label("Select Category:"),
    dcc.Dropdown(
        id='category-dropdown',
        options=[{'label': i, 'value': i} for i in combinedPrices['Category'].unique()],
        value=None
    ),

    dcc.Graph(id='category-price-graph'),

    # Pick what brands you want to display with a multi-dropdown menu
    html.Label("Select Brands:"),
    dcc.Dropdown(
        id='brand-dropdown',
        options=[{'label': i, 'value': i} for i in combinedHype['Brand'].unique()],
        value=None  
    ),

    dcc.Graph(id='popularity-graph'),
])

@dash_app.callback(
    Output('category-price-graph', 'figure'),
    [Input('category-dropdown', 'value')]
)
# NOTE: This is Combined Price Data (eBay and Average)
def update_category_price_graph(selected_category):
    if selected_category is None:
        pass

    print("You Choose Category: " + str(selected_category))
    # Filter combinedPrices DataFrame based on the selected category
    filtered_data = combinedPrices[combinedPrices['Category'] == selected_category]
    print(filtered_data)  # Gets us the Category AND Price

    # Reshape the DataFrame using pd.melt
    melted_data = pd.melt(filtered_data, id_vars=['Category'],
                          value_vars=['Price_ebay', 'Price_usa-labor-statistics'],
                          var_name='Price Type', value_name='Price')

    # Create bar graph with two bars (eBay and Average)
    fig = px.bar(melted_data, x='Category', y='Price',
                 color='Price Type',
                 title=f'Prices in Category: {selected_category}',
                 labels={'Price': 'Price ($)', 'Category': 'Category', 'Price Type': 'Price Type'},
                 color_discrete_sequence=['green', 'blue'],
                 barmode='group')  # Set barmode to 'group' for side-by-side bars

    # Update layout to hide x-axis tick labels
    fig.update_layout(xaxis_title="Avg Price by Category", yaxis_title="Price ($)")
    #fig.update_xaxes(showticklabels=False)
   
    # Set the maximum value for the y-axis
    fig.update_yaxes(range=[0, 150])
    return fig

@dash_app.callback(
    Output('popularity-graph', 'figure'),
    [Input('brand-dropdown', 'value')]  # or use another dropdown for platforms
)
# NOTE: This is REDDIT Data
def update_popularity_graph(selected_brand):
    print("You Choose Brand: " + str(selected_brand))
    # Filter the DataFrame based on the selected brand
    filtered_hypeWear = combinedHype[combinedHype['Brand'] == selected_brand]
    print(filtered_hypeWear)

    # Reshape the DataFrame using pd.melt
    melted_hype = pd.melt(filtered_hypeWear, id_vars=['Brand'],
                          value_vars=['findfashion', 'fashionreps'],
                          var_name='Platform', value_name='Popularity')

    # Create bar graph with two bars (findfashion and fashionreps)
    fig = px.bar(melted_hype, x='Brand', y='Popularity', color='Platform',
                 title=f'Popularity of {selected_brand} on Different Platforms',
                 labels={'Popularity': 'Popularity Metric', 'Brand': 'Brand', 'Platform': 'Platform'},
                 color_discrete_sequence=['red', 'orange'],
                 barmode='group')  # Set barmode to 'group' for side-by-side bars

    # Update layout to hide x-axis tick labels
    fig.update_layout(xaxis_title="Brand", yaxis_title="Popularity Metric")

    return fig

# Changes the thing so that it starts up on the dashboard instead of http://127.0.0.1:5000/
@app.route('/')
def redirect_to_dashboard():
    return redirect('/dashboard/')

# Turn debug mode on
if __name__ == '__main__':
    app.run(debug=True)
