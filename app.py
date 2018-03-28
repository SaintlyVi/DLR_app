#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 16:09:33 2017

@author: saintlyvi
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
from dash.dependencies import Input, Output#, State

import plotly.graph_objs as go
#import plotly.offline as offline
#offline.init_notebook_mode(connected=True)

import pandas as pd
import numpy as np
import os
import base64

import features
from support import appProfiles

# Load images
erc_logo = os.path.join('img', 'erc_logo.jpg')
erc_encoded = base64.b64encode(open(erc_logo, 'rb').read())
sanedi_logo = os.path.join('img', 'sanedi_logo.jpg')
sanedi_encoded = base64.b64encode(open(sanedi_logo, 'rb').read())

# Get mapbox token
mapbox_access_token = 'pk.eyJ1Ijoic2FpbnRseXZpIiwiYSI6ImNqZHZpNXkzcjFwejkyeHBkNnp3NTkzYnQifQ.Rj_C-fOaZXZTVhTlliofMA'

# Get load profile data from disk
print('...loading load profile data...')
profiles = appProfiles()

print('...loading socio demographic data...')
# Load datasets
ids = features.loadID()
loc_summary = ids[ids.AnswerID!=0].groupby(['Year','LocName','Lat','Long','Municipality','Province'])['AnswerID'].count().reset_index()
loc_summary.rename(columns={'AnswerID':'# households'}, inplace=True)

print('Your app is starting now. Visit 127.0.0.1:8050 in your browser')

app = dash.Dash()
app.config['suppress_callback_exceptions']=True

external_css = ["https://fonts.googleapis.com/css?family=Overpass:300,300i",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/dab6f937fd5548cebf4c6dc7e93a10ac438f5efb/dash-technical-charting.css"]

for css in external_css:
    app.css.append_css({"external_url": css})

app.layout = html.Div([
        html.Div([
            html.Div([
                html.Img(src='data:image/png;base64,{}'.format(erc_encoded.decode()), 
                         style={'width': '100%', 'paddingLeft':'5%', 'marginTop':'20%' })    
            ],
                className='three columns',
                style={'margin_top':'20'}
            ),
            html.Div([
                html.H2('South African Domestic Load Research',
                        style={'textAlign': 'center'}
                ),
                html.H1('Data Explorer',
                        style={'textAlign':'center'}
                )                    
            ],
                className='six columns'
            ),        
            html.Div([
                 html.Img(src='data:image/png;base64,{}'.format(sanedi_encoded.decode()), 
                          style={'width':'100%','margin-left':'-5%','marginTop':'10%' })                       
            ],
                className='three columns'
            ),              
        ],
            className='row',
            style={'background':'white',
                   'margin-bottom':'40'}
        ), 
        html.Div([
            html.H3('Survey Locations'
            ),
            html.Div([
                html.Div([
                    dcc.Graph(
                        animate=True,
                        style={'height': 450},
                        id='map'
                    ),
                    dcc.RangeSlider(
                        id = 'input-years',
                        marks={i: i for i in range(1994, 2015, 2)},
                        min=1994,
                        max=2014,
                        step=1,
                        included=True,
                        value= [1994, 2014],
                        updatemode='drag',
                        dots = True
                    )       
                ],
                    className='Eleven columns'
                ),
            ],
                className='columns',
                style={'margin-bottom':'10',
                       'margin-left':'0',
                       'width':'50%',
                       'float':'left'}
            ),
            html.Div([
                dt.DataTable(
                    id='output-location-list',
                    rows=[{}], # initialise the rows
                    row_selectable=False,
                    columns = ['Year','Province','Municipality','LocName','# households'],
                    filterable=True,
                    sortable=True,
                    column_widths=100,
                    min_height = 450,
                    resizable=True,
                    selected_row_indices=[],),
                html.P('"# households" is the number of households surveyed at that location',
                       style={'font-style': 'italic'}
                       )     
            ],
                className='columns',
                style={'margin-bottom':'10',
                       'margin-top':'30',
                       'width':'45%',
                       'float':'right'}
            ),
        ],
            className='row',
        ),
        html.Hr(),
        html.Div([ 
            html.Div([
                html.H3('Survey Questions'
                ),
                html.P('The DLR socio-demographic survey was updated in 2000. Select the surveys that you want to search.'),
                html.Div([
                    dcc.Checklist(
                        id = 'input-survey',
                        options=[
                                {'label': '1994 - 1999', 'value': 6},
                                {'label': '2000 - 2014', 'value': 3}
                                ],
                        values=[3]
                    )
                ],
                    className='container',
                    style={'margin': '10'}
                ),
                html.Div([
                    dcc.Input(
                        id='input-search-word',
                        placeholder='search term',
                        type='text',
                        value=''
                    )
                ],
                    className='container',
                    style={'margin': '10'}
                ),
                dt.DataTable(
                    id='output-search-word-questions',
                    rows=[{}], # initialise the rows
                    row_selectable=True,
                    filterable=False,
                    sortable=True,
                    selected_row_indices=[],)
            ],
                className='columns',
                style={'margin':10,
                       'width':'40%',
                       'float':'left'}
            ),
            html.Div([
                html.H3('Survey Responses Overview'
                ),
                html.P('Select a question and set of locations to see the distribution of responses.'),
                html.Div([
                    dcc.RadioItems(
                        id = 'input-summarise',
                        options=[
                                {'label': 'mean', 'value': 'mean'},
                                {'label': 'count', 'value': 'count'}
                                ],
                        value='count',
                        labelStyle={'display': 'inline-block'}
                    )
                ],
                    className='container',
                    style={'margin': '10'}
                ),
                dt.DataTable(
                    id='output-locqu-summary',
                    rows=[{}], # initialise the rows
                    row_selectable=True,
                    filterable=True,
                    sortable=True,
                    column_widths=40,
                    selected_row_indices=[],)
            ],
                className='columns',
                style={'margin':10,
                       'width':'50%',
                       'float':'right'}
            )
        ],
            className='row'
        ),
        html.Hr(),
        html.Div([
            html.Div([
                dcc.Graph(
                    id='graph-profiles'
                ),
                dcc.RangeSlider(
                    id = 'input-months',
                    marks=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
                    min=1,
                    max=12,
                    step=1,
                    included=True,
                    value= [1,12],
                    updatemode='drag',
                    dots = True
                )       
            ])
        ]),        
        html.Div([
            html.H3('Download Data'
            ),
            html.Div([
                html.Label('Select year range'
                ),
                dcc.RangeSlider(
                    id = 'input-years-download',
                    marks={i: i for i in range(1994, 2015, 2)},
                    min=1994,
                    max=2014,
                    step=1,
                    value=[2011, 2011],
#                    dots = True,
#                    included=True
                )
            ],
                className='seven columns',
                style={'margin-bottom': '50'}
            ),
            html.P(),
            html.Div([
                html.Label('Specify comma-separated list of search terms to select question responses'
                ),
                dcc.Input(
                    id='search-list',
                    placeholder='search term',
                    type='text',
                    value=''
                )
            ],
                className='seven columns',
                style={'margin-bottom': '10'}
            )
        ],
            className='container',
            style={'margin': 10,
                   'padding': 0}
        ),
    ],
    #Set the style for the overall dashboard
    style={
        'width': '100%',
        'max-width': '1200',
        'margin-left': 'auto',
        'margin-right': 'auto',
        'font-family': 'overpass',
        'background-color': '#F3F3F3',
        'padding': '40',
        'padding-top': '20',
        'padding-bottom': '20',
    },
)

#Define outputs
@app.callback(
        Output('output-location-list','rows'),
        [Input('input-years','value')]
        )
def update_locations(input_years):
    dff = pd.DataFrame()
    for y in range(input_years[0], input_years[1]+1):
        df = loc_summary.loc[loc_summary.Year.astype(int) == y, ['Year','Province','Municipality','LocName', '# households']]
        dff = dff.append(df)
    dff.reset_index(inplace=True, drop=True)
    return dff.to_dict('records')
            
@app.callback(
        Output('output-search-word-questions','rows'),
        [Input('input-search-word','value'),
         Input('input-survey','values')]
        )
def update_questions(search_word, surveys):
    if isinstance(surveys, list):
        pass
    else:
        surveys = [surveys]
    df = features.searchQuestions(search_word)[['Question','QuestionaireID']]
    dff = df.loc[df['QuestionaireID'].isin(surveys)]
    questions = pd.DataFrame(dff['Question'])
    return questions.to_dict('records')

@app.callback(
        Output('map','figure'),        
        [Input('output-location-list','rows')]
        )

def update_map(input_locations):

    loc_list = pd.DataFrame(input_locations)
    keys=['Year','LocName']
    i_loc = loc_list.set_index(keys).index
    i_site = loc_summary.set_index(keys).index
    
    georef = loc_summary[i_site.isin(i_loc)]
        
    traces = []
    for y in range(georef.Year.min(), georef.Year.max()+1):
        lat = georef.loc[(georef.Year==y), 'Lat']
        lon = georef.loc[(georef.Year==y), 'Long']
        text = georef.loc[(georef.Year==y), 'LocName'] + ', ' + georef.loc[(georef.Year==y), 'Municipality']
#        marker_size = site_geo.loc[site_geo.Year==y,'# households']
        trace=go.Scattermapbox(
                name=y,
                lat=lat,
                lon=lon,
                mode='markers',
                marker=go.Marker(
                    size=12
                ),
                text=text,
            )
        traces.append(trace)
    figure=go.Figure(
        data=go.Data(traces),
        layout = go.Layout(
                autosize=True,
                hovermode='closest',
                mapbox=dict(
                    accesstoken=mapbox_access_token,
                    bearing=0,
                    center=dict(
                        lat=loc_summary[loc_summary.LocName=='Ikgomotseng'] ['Lat'].unique()[0],
                        lon=loc_summary[loc_summary.LocName=='Ikgomotseng']['Long'].unique()[0]
                    ),
                    pitch=0,
                    zoom=4.2,
                    style='light'
                ),
                margin = go.Margin(
                        l = 10,
                        r = 10,
                        t = 20,
                        b = 30
                ),
                showlegend=False
            )
    )
    return figure
   
@app.callback(
        Output('output-locqu-summary','rows'),
        [#Input('output-location-list','selected_row_indices'),
         Input('output-location-list','rows'),
         Input('output-search-word-questions','selected_row_indices'),
         Input('output-search-word-questions','rows'),
         Input('input-summarise', 'value')
         ]
        )
def update_locqu_summary(loc_rows, qu_selected_ix, qu_rows, summarise):

    locations = pd.DataFrame(loc_rows)
    years = locations.Year.unique()
    idselect = ids.loc[(ids.Year.isin(years)) & (ids.LocName.isin(locations.LocName.unique())), ['id','Year','LocName']]
    idselect.reset_index(inplace=True, drop=True)
    
    searchterms = list(pd.DataFrame(qu_rows).loc[qu_selected_ix, 'Question'])
    
    d = pd.DataFrame()
    for y in years.astype(int):
        df = features.buildFeatureFrame(searchterms, y)[0]
        d = d.append(df)

    locqu = idselect.merge(d, how='left',left_on='id',right_on='AnswerID')
    locqu.drop('id', axis=1, inplace=True)
    aggcols = locqu.columns[3::]
    group_locqu = locqu.groupby(by=['Year','LocName'])[aggcols].describe()
 
    
    if summarise == 'mean':
        locqu_summary = group_locqu.iloc[:, (group_locqu.columns.get_level_values(1)=='mean')|(group_locqu.columns.get_level_values(1)=='50%')|(group_locqu.columns.get_level_values(1)=='std')]
        locqu_summary.reset_index(inplace=True)
            
    elif summarise == 'count':
        locqu_summary = group_locqu.iloc[:, (group_locqu.columns.get_level_values(1)=='count')]
        locqu_summary.reset_index(inplace=True)
        
    return locqu_summary.to_dict('records')

@app.callback(
        Output('graph-profiles','figure'),
        [Input('output-location-list','rows'),
         Input('input_months','value')
        ]
        )
def graph_profiles(input_locations, selected_months):

#TODO first filter by answerID based on questions, then by profileid
    loc_list = pd.DataFrame(input_locations)
    years = loc_list.Year.unique()
    locs = loc_list.LocName.unique()
    months=['January','February','March','April','May','June','July','August','September','October','November','December']

    g = profiles[(profiles.ProfileID_i.isin(ids.loc[(ids.Year.isin(years))&(ids.LocName.isin(locs))&(ids.AnswerID!=0),'ProfileID']))]
    gg = g.groupby(['daytype','month','hour'])['kw_mean'].mean().reset_index()

    for i in ['Weekday']:#gg.daytype.unique():
        
        dt_mean = gg[(gg.daytype==i)&gg.month.isin(selected_months)]
#        dt_profiles = g[(g.daytype==i)&g.month.isin(selected_months)]
    
        dt_mean['tix'] = 24*(dt_mean.month-selected_months[0]) + dt_mean.hour
        dt_mean['tixnames'] = dt_mean.apply(lambda x: 'mean demand'+'<br />'+months[int(x.month)-1]+' '+ str(int(x.hour))+'h00', axis=1)
        
#        dt_profiles['tix'] = 24*(dt_profiles.month-1) + dt_profiles.hour
#        dt_profiles['tixnames'] = dt_profiles.apply(lambda x: 'mean demand'+'<br />Month '+str(int(x.month))+'<br />'+str(int(x.hour))+'h00', axis=1)
        data = []
        
        for m in range(0, len(months)+1):
        
            trace = go.Scatter(
                showlegend=True,
                opacity=1,
                x=dt_mean.loc[dt_mean['month']==m, 'hour'],#'tix'],
                y=dt_mean.loc[dt_mean['month']==m, 'kw_mean'],
                mode='lines',
                name=months[m-1],
                line=dict(
                    #color='red',
                    width=1.5),
                hoverinfo = 'name+y'
            )
            data.append(trace)
        
        layout = go.Layout(showlegend=True, 
            title= i + ' Average Daily Demand for Selected Locations',
            margin = dict(t=150,r=150,b=50,l=150),
            height = 400,
            yaxis = dict(
                    title = 'mean hourly demand (kW)',
                    ticksuffix=' kW'),
            xaxis = dict(                        
                    title = 'time of day',
                    ticktext = dt_mean['hour'].unique(),#[months[i-1] for i in selected_months],
                    tickvals = dt_mean['hour'].unique(),#np.arange(12, (len(selected_months)*24), 24),
#                    ticks = "",
                    showgrid = False)
                    )
        fig = go.Figure(data=data, layout=layout)   
    
    return fig

# Run app from script. Go to 127.0.0.1:8050 to view
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)