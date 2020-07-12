import plotly.graph_objects as go
import dash
import dash_table
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output

# Data Preprocessing
clubstats = pd.read_csv('p_clubstats.csv')
tables = pd.read_csv('p_tables.csv')
top4 = pd.read_csv('top4.csv')
below4 = pd.read_csv('below4.csv')
df = pd.read_csv('df.csv')


# Dashboard
app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.BOOTSTRAP]
)
server = app.server

row = html.Div(
    [
        # Title
        dbc.Row(
            [
                html.H1('EPL Dashboard', style={'margin-bottom': '1%'}),
                html.H6(dbc.Badge('Beta'))
            ]),
        # Team & Season Slider 
        dbc.Row(
            [
                dbc.Col(html.Div(
                    [
                        html.Div(
                            [
                                html.A('Select the group that you want to see.', style={'margin-top': '1%', 'fontWeight': '500'}),
                                dcc.Checklist(id='choose_group', options=[
                                                                            {'label': 'Top 4', 'value': 1},
                                                                            {'label': 'Below 4', 'value': 0}
                                                                            ], 
                                                                value=[1, 0],
                                                                inputStyle={'margin-left': '10px', 'margin-right': '1px'}),
                                html.A('Select Table features', style={'fontWeight': '500'}),
                                dcc.Dropdown(id='table_dropdown', options=[
                                                                            {'label': i, 'value': i}
                                                                            for i in tables.columns.drop(['position', 'club_name', 'season'])
                                                                            ], 
                                                                value='goal',
                                                                clearable=False, style={'margin-bottom': '3%'}),
                                html.A('Select Club Statistics features', style={'margin-top': '3%', 'fontWeight': '500'}),
                                dcc.Dropdown(id='club_dropdown', options=[
                                                                            {'label': i, 'value': i}
                                                                            for i in clubstats.columns.drop('club_name')
                                                                            ], 
                                                                value='big_chance_created',
                                                                clearable=False, style={'margin-bottom': '3%'}),
                                html.A('Select the range of season', style= {'fontWeight': '500'}),
                                dcc.RangeSlider(id='season_slider',
                                                min=1993,
                                                max=2020,
                                                value=[1993, 2020],
                                                tooltip={'always_visible': False, 'placement': 'bottomRight'}
                                                )
                                ], style={'margin-top': '0.5%'}
                            )], style= {
                                        'border-radius': '10px',
                                        'box-shadow': '5px 5px #e6ebed',
                                        'background': '#f7f9fa',
                                        'padding': '3%',
                                        'margin-left': '0%',
                                        'margin-bottom': '7%'
                                        }
                                    )
                                ),
                # Tabs for tables
                dbc.Col(
                    [
                        dcc.Tabs(id='table_tabs', value='tab_1', className='custom-tabs-container', 
                            children=[
                                dcc.Tab(label='Table', value='tab_1', className='custom-tab', selected_className='custom-tab--selected'),
                                dcc.Tab(label='Club Stats', value='tab_2', className='custom-tab', selected_className='custom-tab--selected')
                                ]),
                        dcc.Graph(id='table_table')
                        ], width=9)], style={'height': '320px'}),
        # Plot contents
        dbc.Row(
            [
                dbc.Col(html.Div(
                    [
                        html.H5(dbc.Badge('Table Barchart')),
                        dcc.Graph(id='table_bar')
                        ], style= {
                                    'border-radius': '10px',
                                    'box-shadow': '5px 5px #e6ebed',
                                    'background': '#f7f9fa',
                                    'padding': '3%',
                                    'margin-left': '0%',
                                    'margin-bottom': '3.5%'
                                }
                            ), width=6
                        ),
                dbc.Col(html.Div(
                    [
                        html.H5(dbc.Badge('Club Stats Barchart')),
                        dcc.Graph(id='club_bar')
                        ], style= {
                                    'border-radius': '10px',
                                    'box-shadow': '5px 5px #e6ebed',
                                    'background': '#f7f9fa',
                                    'padding': '3%',
                                    'margin-left': '0%',
                                    'margin-bottom': '3.5%'
                                }
                            ), width=6
                        ),
                dbc.Col(html.Div(
                    [
                        html.H5(dbc.Badge('Table Timeseries')),
                        dcc.Graph(id='table_timeseries')
                        ], style= {
                                    'border-radius': '10px',
                                    'box-shadow': '5px 5px #e6ebed',
                                    'background': '#f7f9fa',
                                    'padding': '3%',
                                    'margin-left': '0%',
                                    'margin-bottom': '1%'
                                }
                            ), width=6
                        ),
                dbc.Col(html.Div(
                    [
                        html.H5(dbc.Badge('Club Stats Timeseries')),
                        dcc.Graph(id='club_timeseries')
                    ], style= {
                                    'border-radius': '10px',
                                    'box-shadow': '5px 5px #e6ebed',
                                    'background': '#f7f9fa',
                                    'padding': '3%',
                                    'margin-left': '0%',
                                    'margin-bottom': '1%'
                                }
                            ), width=6
                        )
            ]
        )
    ], style={'padding':'3%'}
)

app.layout = row

# Callbacks
@app.callback(
    Output('table_bar','figure'),
    [
        Input('choose_group', 'value'),
        Input('season_slider', 'value'),
        Input('table_dropdown', 'value')
        ])
def table_barplot(choose_group, season_slider, table_dropdown):
    fig = go.Figure(layout={'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})
    title_plot = str(table_dropdown) + ' from '+ str(season_slider[0]) + '~' + str(season_slider[1])
    fig.update_layout(title={
                            'text': title_plot, 
                            'y': 0.9, 
                            'x': 0.9,
                            'font': {'size': 20}
                        },
                        margin=dict(t=5, b=5), 
                        legend=dict(x=-.1, y=1.2))
    fig.update_xaxes(showgrid=True, gridwidth=3, gridcolor='rgb(242,242,242,242)')
    fig.update_yaxes(showgrid=True, gridwidth=3, gridcolor='rgb(242,242,242,242)')
    if len(choose_group) == 2:
        years = []
        avg_feature_top4 = []
        avg_feature_below4 = []
        for year in range(season_slider[0], season_slider[1]+1):
            years.append(year)
            for goal in top4[top4['season'] == str(year)].loc[:, table_dropdown]:
                avg_feature_top4.append(goal)
            for goal in below4[below4['season'] == str(year)].loc[:, table_dropdown]:
                avg_feature_below4.append(goal)
        fig.add_trace(go.Bar(
            x = pd.Series(avg_feature_top4).value_counts().sort_index().index,
            y = pd.Series(avg_feature_top4).value_counts().sort_index(),
            marker_color = 'purple',
            name='Top 4'
        ))
        fig.add_trace(go.Bar(
            x = pd.Series(avg_feature_below4).value_counts().sort_index().index,
            y = pd.Series(avg_feature_below4).value_counts().sort_index(),
            marker_color = 'navy',
            name='Below 4'
        ))
        return fig.update_layout(barmode='stack')
    else:
        years = []
        avg_feature = []
        if choose_group == [1]:
            for year in range(season_slider[0], season_slider[1]+1):
                years.append(year)
                for goal in top4[top4['season'] == str(year)].loc[:, table_dropdown]:
                    avg_feature.append(goal)
            fig.add_trace(go.Bar(
                x = pd.Series(avg_feature).value_counts().sort_index().index,
                y = pd.Series(avg_feature).value_counts().sort_index(),
                marker_color = 'purple',
                name = 'Top 4'
            ))
            return fig
        else:
            for year in range(season_slider[0], season_slider[1]+1):
                years.append(year)
                for goal in below4[below4['season'] == str(year)].loc[:, table_dropdown]:
                    avg_feature.append(goal)
            fig.add_trace(go.Bar(
                x = pd.Series(avg_feature).value_counts().sort_index().index,
                y = pd.Series(avg_feature).value_counts().sort_index(),
                marker_color = 'navy',
                name = 'Below 4'
            ))
            return fig

@app.callback(
    Output('table_timeseries','figure'),
    [
        Input('choose_group', 'value'),
        Input('season_slider', 'value'),
        Input('table_dropdown', 'value')
        ])
def table_timeSplot(choose_group, season_slider, table_dropdown):
    fig = go.Figure(layout={'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})
    title_plot = str(table_dropdown) + ' from '+ str(season_slider[0]) + '~' + str(season_slider[1])
    fig.update_layout(title={
                            'text': title_plot, 
                            'y': 0.9, 
                            'x': 0.9,
                            'font': {'size': 20}
                        },
                        margin=dict(t=5, b=5), 
                        legend=dict(x=-.1, y=1.2))
    fig.update_xaxes(showgrid=True, gridwidth=3, gridcolor='rgb(242,242,242,242)')
    fig.update_yaxes(showgrid=True, gridwidth=3, gridcolor='rgb(242,242,242,242)')
    if len(choose_group) == 2:
        years = []
        avg_feature_top4 = []
        avg_feature_below4 = []
        for year in range(season_slider[0], season_slider[1]+1):
            years.append(year)
            avg_feature_top4.append(top4[top4['season'] == str(year)].loc[:, table_dropdown].mean())
            avg_feature_below4.append(below4[below4['season'] == str(year)].loc[:, table_dropdown].mean())
        
        fig.add_trace(go.Scatter(
            x = years,
            y = avg_feature_top4,
            marker_color = 'purple',
            name='Top 4'
        ))
        fig.add_trace(go.Scatter(
            x = years,
            y = avg_feature_below4,
            marker_color = 'navy',
            name='Below 4'
        ))
        return fig
    else:
        years = []
        avg_feature = []
        if choose_group == [1]:
            for year in range(season_slider[0], season_slider[1]+1):
                years.append(year)
                avg_feature.append(top4[top4['season'] == str(year)].loc[:, table_dropdown].mean())
            fig.add_trace(go.Scatter(
                x = years,
                y = avg_feature,
                marker_color = 'purple',
                name = 'Top 4'
            ))
            return fig
        else:
            for year in range(season_slider[0], season_slider[1]+1):
                years.append(year)
                avg_feature.append(below4[below4['season'] == str(year)].loc[:, table_dropdown].mean())
            fig.add_trace(go.Scatter(
                x = years,
                y = avg_feature,
                marker_color = 'navy',
                name = 'Below 4'
            ))
            return fig

@app.callback(
    Output('club_bar','figure'),
    [
        Input('choose_group', 'value'),
        Input('season_slider', 'value'),
        Input('club_dropdown', 'value')
        ])
def club_barplot(choose_group, season_slider, club_dropdown):
    fig = go.Figure(layout={'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})
    f_year_club = 2011
    if season_slider[0] > 2011:
        f_year_club = season_slider[0]
    title_plot = str(club_dropdown) + ' from '+ str(f_year_club) + '~' + str(season_slider[1])
    fig.update_layout(title={
                            'text': title_plot, 
                            'y': 0.9, 
                            'x': 0.9,
                            'font': {'size': 20}
                        },
                        margin=dict(t=5, b=5), 
                        legend=dict(x=-.1, y=1.2))
    fig.update_xaxes(showgrid=True, gridwidth=3, gridcolor='rgb(242,242,242,242)')
    fig.update_yaxes(showgrid=True, gridwidth=3, gridcolor='rgb(242,242,242,242)')

    if len(choose_group) == 2:
        years = []
        avg_feature_top4 = []
        avg_feature_below4 = []
        for year in range(f_year_club, season_slider[1]+1):
            years.append(year)
            for goal in top4[top4['season'] == str(year)].loc[:, club_dropdown]:
                avg_feature_top4.append(goal)
            for goal in below4[below4['season'] == str(year)].loc[:, club_dropdown]:
                avg_feature_below4.append(goal)

        fig.add_trace(go.Bar(
            x = pd.Series(avg_feature_top4).value_counts().sort_index().index,
            y = pd.Series(avg_feature_top4).value_counts().sort_index(),
            marker_color = 'purple',
            name='Top 4'
        ))
        fig.add_trace(go.Bar(
            x = pd.Series(avg_feature_below4).value_counts().sort_index().index,
            y = pd.Series(avg_feature_below4).value_counts().sort_index(),
            marker_color = 'navy',
            name='Below 4'
        ))
        return fig.update_layout(barmode='stack')
    else:
        years = []
        avg_feature = []
        if choose_group == [1]:
            for year in range(f_year_club, season_slider[1]+1):
                years.append(year)
                for goal in top4[top4['season'] == str(year)].loc[:, club_dropdown]:
                    avg_feature.append(goal)
            fig.add_trace(go.Bar(
                x = pd.Series(avg_feature).value_counts().sort_index().index,
                y = pd.Series(avg_feature).value_counts().sort_index(),
                marker_color = 'purple',
                name = 'Top 4'
            ))
            return fig
        else:
            for year in range(f_year_club, season_slider[1]+1):
                years.append(year)
                for goal in below4[below4['season'] == str(year)].loc[:, club_dropdown]:
                    avg_feature.append(goal)
            fig.add_trace(go.Bar(
                x = pd.Series(avg_feature).value_counts().sort_index().index,
                y = pd.Series(avg_feature).value_counts().sort_index(),
                marker_color = 'navy',
                name = 'Below 4'
            ))
            return fig

@app.callback(
    Output('club_timeseries','figure'),
    [
        Input('choose_group', 'value'),
        Input('season_slider', 'value'),
        Input('club_dropdown', 'value')
        ])
def club_timeSplot(choose_group, season_slider, club_dropdown):
    fig = go.Figure(layout={'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})
    f_year_club = 2011
    if season_slider[0] > 2011:
        f_year_club = season_slider[0]
    title_plot = str(club_dropdown) + ' from '+ str(f_year_club) + '~' + str(season_slider[1])
    fig.update_layout(title={
                            'text': title_plot, 
                            'y': 0.9, 
                            'x': 0.9,
                            'font': {'size': 20}
                        },
                        margin=dict(t=5, b=5), 
                        legend=dict(x=-.1, y=1.2))
    fig.update_xaxes(showgrid=True, gridwidth=3, gridcolor='rgb(242,242,242,242)')
    fig.update_yaxes(showgrid=True, gridwidth=3, gridcolor='rgb(242,242,242,242)')
    if len(choose_group) == 2:
        years = []
        avg_feature_top4 = []
        avg_feature_below4 = []
        for year in range(f_year_club, season_slider[1]+1):
            years.append(year)
            avg_feature_top4.append(top4[top4['season'] == str(year)].loc[:, club_dropdown].mean())
            avg_feature_below4.append(below4[below4['season'] == str(year)].loc[:, club_dropdown].mean())
        
        fig.add_trace(go.Scatter(
            x = years,
            y = avg_feature_top4,
            marker_color = 'purple',
            name='Top 4'
        ))
        fig.add_trace(go.Scatter(
            x = years,
            y = avg_feature_below4,
            marker_color = 'navy',
            name="Below 4"
        ))
        return fig
    else:
        years = []
        mean_val = []
        avg_feature = []
        if choose_group == [1]:
            for year in range(f_year_club, season_slider[1]+1):
                years.append(year)
                for value in top4[top4['season'] == str(year)].loc[:, club_dropdown]:
                    mean_val.append(value)
                avg_feature.append(np.mean(mean_val))
            fig.add_trace(go.Scatter(
                x = years,
                y = avg_feature,
                marker_color = 'purple',
                name = 'Top 4'
            ))
            return fig
        else:
            for year in range(f_year_club, season_slider[1]+1):
                years.append(year)
                for value in below4[below4['season'] == str(year)].loc[:, club_dropdown]:
                    mean_val.append(value)
                avg_feature.append(np.mean(mean_val))
            fig.add_trace(go.Scatter(
                x = years,
                y = avg_feature,
                marker_color = 'navy',
                name = 'Below 4'
            ))
            return fig

@app.callback(
    Output('table_table', 'figure'),
    [
        Input('table_tabs','value'),
        Input('season_slider', 'value'),
        Input('choose_group', 'value')
    ])
def show_table(table_tabs, season_slider, choose_group):
    fig = go.Figure()
    fig.update_layout(margin=dict(t=0, b=186, l=0, r=0))
    # Something wrong with pandas datetime
    if table_tabs == 'tab_1':
        if len(choose_group) == 2:
            t_df = df[(df['season'] >= season_slider[0]) & (df['season'] <= season_slider[1])]
            fig.add_trace(go.Table(header=dict(
                                                values=[
                                                        'club_name', 'won', 'drawn', 'lost', 'goal',
                                                        'goal_against', 'points', 'position', 'season'
                                                        ],
                                                fill_color='purple', font_color='white', line_color='rgb(242,242,242,242)',
                                                align='left'),
                                    cells=dict(values=[
                                                        t_df.club_name, t_df.won, t_df.drawn, t_df.lost, t_df.goal, 
                                                        t_df.goal_against, t_df.points, t_df.position, t_df.season
                                                        ],
                                    fill_color= '#f7f9fa', line_color='rgb(242,242,242,242)', line={'width': 2},
                                    align='left')))
            return fig
        elif choose_group == [1]:
            t_df = df[(df['season'] >= season_slider[0]) & (df['season'] <= season_slider[1]) & (df['is_top4'] == 1)]
            fig.add_trace(go.Table(header=dict(
                                                values=[
                                                        'club_name', 'won', 'drawn', 'lost', 'goal',
                                                        'goal_against', 'points', 'position', 'season'
                                                        ],
                                                fill_color='purple', font_color='white', line_color='rgb(242,242,242,242)',
                                                align='left'),
                                    cells=dict(values=[
                                                        t_df.club_name, t_df.won, t_df.drawn, t_df.lost, t_df.goal, 
                                                        t_df.goal_against, t_df.points, t_df.position, t_df.season
                                                        ],
                                    fill_color= '#f7f9fa', line_color='rgb(242,242,242,242)', line={'width': 2},
                                    align='left')))
            return fig 
        else:
            t_df = df[(df['season'] >= season_slider[0]) & (df['season'] <= season_slider[1]) & (df['is_top4'] == 0)]
            fig.add_trace(go.Table(header=dict(
                                                values=[
                                                        'club_name', 'won', 'drawn', 'lost', 'goal',
                                                        'goal_against', 'points', 'position', 'season'
                                                        ],
                                                fill_color='purple', font_color='white', line_color='rgb(242,242,242,242)',
                                                align='left'),
                                    cells=dict(values=[
                                                        t_df.club_name, t_df.won, t_df.drawn, t_df.lost, t_df.goal, 
                                                        t_df.goal_against, t_df.points, t_df.position, t_df.season
                                                        ],
                                    fill_color= '#f7f9fa', line_color='rgb(242,242,242,242)', line={'width': 2},
                                    align='left')))
            return fig 
    else:
        if len(choose_group) == 2:
            t_df = df[(df['season'] >= season_slider[0]) & (df['season'] <= season_slider[1])]
            fig.add_trace(go.Table(header=dict(
                                                values=[
                                                        'Club Name', 'Aerial Battle', 'Big Chance Created', 'Clearance', 
                                                        'Cross', 'Cross Accuracy', 'Goal Conceded/match', 'Goal/match',
                                                        'Interceptions', 'Pass Accuracy', 'Pass per game', 'Shooting Accuracy',
                                                        'Shot on Target', 'Tackle success', 'Position'
                                                        ],
                                                fill_color='purple', font_color='white', line_color='rgb(242,242,242,242)',
                                                align='left'),
                                    cells=dict(values=[
                                                        t_df.club_name, t_df.aerial_battles, t_df.big_chance_created, t_df.clearance,
                                                        t_df.cross, t_df.cross_accuracy, t_df.goal_conceded_per_match, 
                                                        t_df.goal_per_match, t_df.interceptions, t_df.pass_accuracy,
                                                        t_df.pass_per_game, t_df.shooting_accuracy, t_df.shot_on_target,
                                                        t_df.tackle_success, t_df.position
                                                        ],
                                    fill_color= '#f7f9fa', line_color='rgb(242,242,242,242)', line={'width': 2},
                                    align='left')))
            return fig 
        elif choose_group == [1]:
            t_df = df[(df['season'] >= season_slider[0]) & (df['season'] <= season_slider[1]) & (df['is_top4'] == 1)]
            fig.add_trace(go.Table(header=dict(
                                                values=[
                                                        'Club Name', 'Aerial Battle', 'Big Chance Created', 'Clearance', 
                                                        'Cross', 'Cross Accuracy', 'Goal Conceded/match', 'Goal/match',
                                                        'Interceptions', 'Pass Accuracy', 'Pass per game', 'Shooting Accuracy',
                                                        'Shot on Target', 'Tackle success', 'Position'
                                                        ],
                                                fill_color='purple', font_color='white', line_color='rgb(242,242,242,242)',
                                                align='left'),
                                    cells=dict(values=[
                                                        t_df.club_name, t_df.aerial_battles, t_df.big_chance_created, t_df.clearance,
                                                        t_df.cross, t_df.cross_accuracy, t_df.goal_conceded_per_match, 
                                                        t_df.goal_per_match, t_df.interceptions, t_df.pass_accuracy,
                                                        t_df.pass_per_game, t_df.shooting_accuracy, t_df.shot_on_target,
                                                        t_df.tackle_success, t_df.position
                                                        ],
                                    fill_color= '#f7f9fa', line_color='rgb(242,242,242,242)', line={'width': 2},
                                    align='left')))
            return fig 
        else:
            t_df = df[(df['season'] >= season_slider[0]) & (df['season'] <= season_slider[1]) & (df['is_top4'] == 0)]
            fig.add_trace(go.Table(header=dict(
                                                values=[
                                                        'Club Name', 'Aerial Battle', 'Big Chance Created', 'Clearance', 
                                                        'Cross', 'Cross Accuracy', 'Goal Conceded/match', 'Goal/match',
                                                        'Interceptions', 'Pass Accuracy', 'Pass per game', 'Shooting Accuracy',
                                                        'Shot on Target', 'Tackle success', 'Position'
                                                        ],
                                                fill_color='purple', font_color='white', line_color='rgb(242,242,242,242)',
                                                align='left'),
                                    cells=dict(values=[
                                                        t_df.club_name, t_df.aerial_battles, t_df.big_chance_created, t_df.clearance,
                                                        t_df.cross, t_df.cross_accuracy, t_df.goal_conceded_per_match, 
                                                        t_df.goal_per_match, t_df.interceptions, t_df.pass_accuracy,
                                                        t_df.pass_per_game, t_df.shooting_accuracy, t_df.shot_on_target,
                                                        t_df.tackle_success, t_df.position
                                                        ],
                                    fill_color= '#f7f9fa', line_color='rgb(242,242,242,242)', line={'width': 2},
                                    align='left')))
            return fig 



if __name__ == '__main__':
    app.run_server()