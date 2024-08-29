import dash
from dash import dcc, dash_table
from dash import html
from dash_html_components import Div
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
from store.models import Book  # Import your actual model
import pandas as pd
import dash_bootstrap_components as dbc



# Initialize DjangoDash app
app = DjangoDash('dash_dashboard', external_stylesheets=[dbc.themes.BOOTSTRAP])



# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "width": "85rem",
    "height": "15rem",
    "padding": "2rem 1rem",
    "background-color": "green",
    'overflowY': 'auto',
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "auto",
    "margin-right": "auto",
    "padding": "2rem 1rem",
}


sidebar = html.Div(
    [
        html.H3("Market Research", className="display-4", style={'color': 'white'}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Company Research", href="/", active="exact"),
                dbc.NavLink("Industry Research", href="/page-1", active="exact"),
            ],
            vertical=False,
            pills=True,
            className="text-center border",
            justified=True,
            fill=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)


# Define your header
header = html.Div(
    [
    dbc.Nav(
            [
                dbc.NavLink("Company Research", href="/", active="exact"),
                dbc.NavLink("Industry Research", href="/page-1", active="exact"),
            ],
            vertical=False,
            pills=True,
            className="text-center border",
            justified=True,
            fill=True,
        )])

# Define your content layout
content = html.Div(id="page-content", style=CONTENT_STYLE)



tab_style = {
    "background": "#539c27",
    'text-transform': 'uppercase',
    'color': 'yellow',
    'border': 'blue',
    'font-size': '20px',
    'font-weight': 1000,
    'align-items': 'center',
    'justify-content': 'center',
    'border-radius': '10px',
    'padding':'30px'}


# Get data from the database
data = Book.objects.all().values()

# Create a Pandas DataFrame
df = pd.DataFrame.from_records(data)
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
df['reviews_count'] = pd.to_numeric(df['reviews_count'], errors='coerce')

# Layout of the Dash app
# Layout of the Dash app

company_page_layout = html.Div([
    
    # Text label for indicating company selection
    html.Div([
        # Text label for indicating company selection
        html.Label("Select Company:", style={'font-weight': 'bold', 'margin-right': '10px'}),

        # Dropdown for company name selection
        dcc.Dropdown(
            id='company-dropdown',
            options=[{'label': company, 'value': company} for company in df['company_name'].unique()],
            value=df['company_name'].unique()[0],
            multi=False,
            style={'width': '50%'}
        ),
    ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'margin-bottom': '20px'}),

    # Tabs for displaying company details
    dcc.Tabs(
        id='tabs-company-details',
        value='tab-total-reviews',
        children=[
            dcc.Tab(
                label='Company Info',
                value='tab-total-reviews',
                selected_style=tab_style
            ),
            dcc.Tab(
                label='Competitor Anslysis',
                value='tab-positive-reviews',
                selected_style=tab_style
            ),
            dcc.Tab(
                label='Negative Reviews',
                value='tab-negative-reviews',
                selected_style=tab_style
            ),
        ]
    ),

    # Container for displaying tab content
    html.Div(id='tabs-content-company-details')
])


category_page_layout = html.Div(
    id='dash-container',  # Add an ID for styling
    # Set height and width
    children=[
        html.H1(children='Company Dashboard'),

        # Total number of companies
        html.Div([
            html.H4(children='Total Companies'),
            html.Div(id='total-companies', children=len(df))
        ]),

        # Average review
        html.Div([
            html.H4(children='Average Review'),
            html.Div(id='average-review', children=df['rating'].astype(float).mean())
        ]),

        # Dropdown for category selection
        dcc.Dropdown(
            id='category-dropdown',
            options=[{'label': category, 'value': category} for category in df['category'].unique()],
            value=df['category'].unique()[0],
            multi=True,
            style={'width': '50%'}
        ),

        # Display the filtered DataFrame
        html.Div(id='filtered-data-table'),

        # Value count from the category column
        html.Div([
            html.H4(children='Category Value Count'),
            dcc.Graph(
                id='category-value-count',
                figure={
                    'data': [
                        {'x': df['category'].value_counts().index, 'y': df['category'].value_counts().values,
                         'type': 'bar', 'name': 'Category Count'},
                        {'x': df.groupby('category')['rating'].mean().index,
                         'y': df.groupby('category')['rating'].mean().values, 'type': 'bar', 'name': 'Avg Rating'},
                        {'x': df.groupby('category')['reviews_count'].sum().index,
                         'y': df.groupby('category')['reviews_count'].sum().values, 'type': 'bar', 'name': 'reviews_count'}
                    ],
                    'layout': {
                        'barmode': 'group', 'title': 'Category Value Count with Avg Rating'}
                }
            )
        ])

        
    ]
)





app.layout = html.Div(
    id='dash-container',  # Add an ID for styling
    children=[
        dcc.Location(id='url', refresh=False),
        header,
        content,
    ]
)


# Callback to update the page content based on the URL
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1' or not pathname:
        return category_page_layout
    elif pathname == '/':
        return company_page_layout
    


# Callbacks to update values dynamically
@app.callback(
    Output('filtered-data-table', 'children'),
    Output('category-value-count', 'figure'),
    Input('category-dropdown', 'value')
)
def update_filtered_data_table(selected_categories):
    if not isinstance(selected_categories, list):
        selected_categories = [selected_categories]
    filtered_df = df[df['category'].isin(selected_categories)]

    # Create a data table for the filtered DataFrame
    data_table = dash_table.DataTable(
        id='filtered-table',
        columns=[{'name': col, 'id': col} for col in filtered_df.columns],
        data=filtered_df.to_dict('records'),
        style_table={'height': '400px', 'overflowY': 'auto'},
    )

    # Create a new category value count graph for the selected categories
    category_value_count_figure = {
        'data': [
            {'x': filtered_df['category'].value_counts().index, 'y': filtered_df['category'].value_counts().values,
             'type': 'bar', 'name': 'Category Count'},
            {'x': filtered_df.groupby('category')['rating'].mean().index,
             'y': filtered_df.groupby('category')['rating'].mean().values, 'type': 'bar', 'name': 'Avg Rating'},
            {'x': filtered_df.groupby('category')['reviews_count'].sum().index,
             'y': filtered_df.groupby('category')['reviews_count'].sum().values, 'type': 'bar', 'name': 'reviews_count'}
        ],
        'layout': {
            'barmode': 'group',
            'title': f'Category Value Count with Avg Rating - {", ".join(selected_categories)}'
        }
    }

    return data_table, category_value_count_figure


# Callback to update the tab content dynamically for the company details page
from dash import Dash, html, dcc, Input, Output, callback

# Callback to update the tab content dynamically for the company details page
@app.callback(
    Output('tabs-content-company-details', 'children'),
    #Output('reviews-filter', 'max'),
    Input('company-dropdown', 'value'),
    Input('tabs-company-details', 'value')
    
)
def update_company_details_tab(selected_company, selected_tab):
    filtered_df = df[df['company_name'] == selected_company]

    if selected_tab == 'tab-total-reviews':
    # Display total reviews information
        tab_content = html.Div([
            html.H5(f"Details for {selected_company}", className="bg-primary text-white p-2 mb-2 text-center"),

            # Display company_name
            html.Div([
                html.Label("Company Name:", style={'font-weight': 'bold', 'margin-right': '10px'}),
                html.Div(selected_company)
            ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '10px'}),

            # Display phone
            html.Div([
                html.Label("Phone:", style={'font-weight': 'bold', 'margin-right': '10px'}),
                html.Div(filtered_df['phone'].iloc[0])  # Assuming 'phone' is a column in your DataFrame
            ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '10px'}),

            # Display website
            html.Div([
                html.Label("Website:", style={'font-weight': 'bold', 'margin-right': '10px'}),
                html.Div(filtered_df['website'].iloc[0])  # Assuming 'website' is a column in your DataFrame
            ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '10px'}),
        ])

    elif selected_tab == 'tab-positive-reviews':
        selected_category = filtered_df['category'].iloc[0]
        same_category_df = df[df['category'] == selected_category]
        
        # Create a list of colors for each bar, highlight the selected company in red
        colors = ['red' if company == selected_company else 'blue' for company in same_category_df['company_name']]
        
        # Create a RangeSlider for filtering based on the number of reviews

        reviews_filter = dcc.RangeSlider(
            id='reviews-filter',
            min=same_category_df['reviews_count'].min(),
            max=same_category_df['reviews_count'].max(),
            step=1,
            marks={i: str(i) for i in range(same_category_df['reviews_count'].min(), same_category_df['reviews_count'].max() + 1)},
            value=[same_category_df['reviews_count'].min(), same_category_df['reviews_count'].max()],
        )
       
        
        reviews_bar_plot = dcc.Graph(
            id='reviews-bar-plot',
            figure={
                'data': [
                    {
                        'x': same_category_df['company_name'],
                        'y': same_category_df['reviews_count'],
                        'type': 'bar',
                        'name': 'Number of Reviews',
                        'marker': {'color': colors},  # Set the color for each bar
                        'text': same_category_df['rating'].round(2),  # Include average rating as text label
                        'textposition': 'auto',  # Automatically position the text above the bars
                    },
                ],
                'layout': {
                    'title': f'Number of Reviews for Each Company in {selected_category}',
                    'xaxis': {'title': 'Company Name'},
                    'yaxis': {'title': 'Number of Reviews'},
                }
            }
        )

    
        
        tab_content = [reviews_bar_plot]
        #max_value = same_category_df['reviews_count'].max()


    elif selected_tab == 'tab-negative-reviews':
        tab_content = html.Div([
            dcc.RangeSlider(min=0, max=20, step=1, value=[5, 15], id='my-range-slider'),
            html.Div(id='output-container-range-slider')
        ])

        def update_output(value):
            return 'You have selected "{}"'.format(value)
        


    else:
        tab_content = html.Div([])

    return tab_content