import dash
from dash import dcc, dash_table
from dash import html
from dash_html_components import Div
from dash.dependencies import Input, Output
from store.models import Book  # Import your actual model
import pandas as pd
from dash import callback  # Add this line

# Initialize DjangoDash app

from django_plotly_dash import DjangoDash
# app = DjangoDash('dash_dashboard', use_bootstrap=True)

dash.register_page('dash_dashboard', path='/')

# Get data from the database
data = Book.objects.all().values()

# Create a Pandas DataFrame
df = pd.DataFrame.from_records(data)
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
df['reviews_count'] = pd.to_numeric(df['reviews_count'], errors='coerce')

# Layout of the Dash app
# Layout of the Dash app

# Layout of the Dash app

# Layout of the Dash app
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

# Callbacks to update values dynamically
@callback(
    Output('filtered-data-table', 'children'),
    Output('category-value-count', 'figure'),
    Input('category-dropdown', 'value')
)
def update_filtered_data_table(selected_categories):
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
