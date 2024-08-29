from django.apps import AppConfig

from django_plotly_dash.apps import DjangoPlotlyDashConfig

class MyAppConfig(DjangoPlotlyDashConfig):
    name = 'dash_dashboard'


