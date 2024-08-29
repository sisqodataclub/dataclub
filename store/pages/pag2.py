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
app = DjangoDash('dash_dashboard', use_bootstrap=True)
dash.register_page(__name__)


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
    html.H1("Company Details"),

    # Dropdown for company name selection
    dcc.Dropdown(
        id='company-dropdown',
        options=[{'label': company, 'value': company} for company in df['company_name'].unique()],
        value=df['company_name'].unique()[0],
        multi=False,
        style={'width': '50%'}
    ),

    # Tabs for displaying company details
    dcc.Tabs(
        id='tabs-company-details',
        value='tab-total-reviews',
        children=[
            dcc.Tab(
                label='Total Reviews',
                value='tab-total-reviews',
                selected_style=tab_style
            ),
            dcc.Tab(
                label='Positive Reviews',
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


# Callback to update the tab content dynamically for the company details page
@callback(
    Output('tabs-content-company-details', 'children'),
    Input('company-dropdown', 'value'),
    Input('tabs-company-details', 'value')
)



def update_company_details_tab(selected_company, selected_tab):
    filtered_df = df[df['company_name'] == selected_company]

    if selected_tab == 'tab-total-reviews':
        # Display total reviews information
        tab_content = html.Div([
            html.H4("Total Reviews"),
            dcc.Graph(
                id='total-reviews-chart',
                figure={
                    'data': [
                        {'x': filtered_df['reviews_count'], 'type': 'bar', 'name': 'Total Reviews'}
                    ],
                    'layout': {
                        'title': 'Total Reviews for {}'.format(selected_company)
                    }
                }
            )
        ])
    elif selected_tab == 'tab-positive-reviews':
        # Display positive reviews information
        # You can customize this section based on your data
        tab_content = html.Div([
            html.H4("Positive Reviews"),
            # Add components for positive reviews
        ])
    elif selected_tab == 'tab-negative-reviews':
        # Display negative reviews information
        # You can customize this section based on your data
        tab_content = html.Div([
            html.H4("Negative Reviews"),
            # Add components for negative reviews
        ])
    else:
        tab_content = html.Div([])

    return tab_content