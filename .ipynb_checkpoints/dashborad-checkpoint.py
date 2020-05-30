import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import pandas as pd
import numpy as np

# Data Preprocessing
clubstats = pd.read_csv('clubstats.csv')
tables = pd.read_csv('tables.csv')

# Change to proper data types
clubstats['cross_accuracy'] = clubstats['cross_accuracy'].map(lambda x: x.rstrip('%')).astype('int')
clubstats['pass_accuracy'] = clubstats['pass_accuracy'].map(lambda x: x.rstrip('%')).astype('int')
clubstats['shooting_accuracy'] = clubstats['shooting_accuracy'].map(lambda x: x.rstrip('%')).astype('int')
clubstats['tackle_success'] = clubstats['tackle_success'].map(lambda x: x.rstrip('%')).astype('int')
clubstats['aerial_battles'] = clubstats['aerial_battles'].str.replace(',','').astype('int')
clubstats['clearance'] = clubstats['clearance'].str.replace(',','').astype('int')
clubstats['cross'] = clubstats['cross'].str.replace(',','').astype('int')

# In 'clubstats' AFC Bournemouth is named as it is, but in 'tables' it is named as 'Bournemouth'.
# So in order to join the two data frames, the club_name for AFC Bournmouth has to be changed.
clubstats['club_name'].iloc[53] = 'Bournemouth'
clubstats['club_name'].iloc[54] = 'Bournemouth'
clubstats['club_name'].iloc[55] = 'Bournemouth'
clubstats['club_name'].iloc[56] = 'Bournemouth'
clubstats['club_name'].iloc[57] = 'Bournemouth'

season_info = clubstats[clubstats['club_name'] == "Arsenal"]['season']
seasons = []

for i in range(len(season_info)):
    if i < 25:
        seasons.append([season_info[i],] * 20)
    else:
        seasons.append([season_info[i],] * 22)

seasons_flat = [season for sub_season in seasons for season in sub_season]
tables['season'] = seasons_flat

# Join two data frames
data = pd.merge(tables, clubstats, on=['club_name', 'season'])

# To get total number of games
data['total_games'] = data['won'] + data['drawn'] + data['lost']
# Add top4 indicator 
data['is_top4'] = data['position'].apply(lambda x: 1 if (x <= 4) else 0)



# Dashboard
app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

row = html.Div(
    [
        # Title
        dbc.Row(dbc.Col(html.H1('EPL Dashborad', style={'margin-bottom': '1%'}))),
        # Team & Season Selector 
        dbc.Row(dbc.Col(
            [
                html.P('Select the group that you want to see.', style={'margin-top': '2%'}),
                html.Div(
                    [
                        dcc.Checklist(options=[
                                                {'label': 'Top 4', 'value': 'Top4'},
                                                {'label': 'Below 4', 'value': 'Below4'}
                                                ], inputStyle={'margin-left': '10px', 'margin-right': '1px'}),
                        html.A('Select Table features'),
                        dcc.Dropdown(options=[
                                                {'label': 'Top 4', 'value': 'Top4'},
                                                {'label': 'Below 4', 'value': 'Below4'}
                                                ], multi=True),
                        html.A(''),
                        html.A('Select Club Statistics features', style={'margin-top': '3%'}),
                        dcc.Dropdown(options=[
                                                {'label': 'Top 4', 'value': 'Top4'},
                                                {'label': 'Below 4', 'value': 'Below4'}
                                                ], multi=True),
                                            ], style={'margin-top': '1%'}
                                        ),
                html.P('Select the range of season', style= {'margin-top': '2%'}),
                html.Div(dcc.RangeSlider(min=1993,
                                        max=2020,
                                        tooltip={'always_visible': False, 'placement': 'bottomRight'},
                                        )
                                    )
                                ]
                            ), style= {
                                'border-radius': '10px',
                                'box-shadow': '3px 3px #e6ebed',
                                'width': '30%',
                                'background': '#f7f9fa',
                                'margin-left': '0%',
                                'margin-bottom': '1%'
                            }
                        ),
        # Plot contents
        dbc.Row(
            [
                dbc.Col(html.Div('Table Barplots', style= {
                                                        'border-radius': '10px',
                                                        'box-shadow': '3px 3px #e6ebed',
                                                        'background': '#f7f9fa',
                                                        'padding': '4%',
                                                        'margin-bottom': '1%'
                                                    }
                                                ), width=6),
                dbc.Col(html.Div('Club stats Barplots', style= {
                                                        'border-radius': '10px',
                                                        'box-shadow': '3px 3px #e6ebed',
                                                        'background': '#f7f9fa',
                                                        'padding': '4%',
                                                        'margin-bottom': '1%'
                                                    }
                                                ), width=6),
                dbc.Col(html.Div('Table-timeseries', style= {
                                                        'border-radius': '10px',
                                                        'box-shadow': '3px 3px #e6ebed',
                                                        'background': '#f7f9fa',
                                                        'padding': '4%'
                                                    }
                                                ), width=6),
                dbc.Col(html.Div('Club stats-timeseries', style= {
                                                        'border-radius': '10px',
                                                        'box-shadow': '3px 3px #e6ebed',
                                                        'background': '#f7f9fa',
                                                        'padding': '4%'
                                                    }
                                                ), width=6)
            ]
        )
    ], style={'padding':'3%'}
)


app.layout = row


if __name__ == '__main__':
    app.run_server(debug=True)