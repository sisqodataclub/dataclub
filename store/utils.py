import pandas as pd

def data_overview(data, title):
    overview_analysis = {
        'title': title,
        'columns': data.shape[1],
        'rows': data.shape[0],
        'missing_values': data.isnull().any(axis=1).sum(),
        'missing_values_percentage': data.isnull().any(axis=1).sum() / len(data) * 100,
        'duplicates': data.duplicated().sum(),
        'duplicates_percentage': data.duplicated().sum() / len(data) * 100,
        'categorical_variables': sum((data.dtypes == 'object') & (data.nunique() > 2)),
        'boolean_variables': sum((data.dtypes == 'object') & (data.nunique() < 3)),
        'numerical_variables': data.select_dtypes(include=['int64', 'float64']).shape[1]
    }
    return overview_analysis