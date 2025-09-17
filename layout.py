from dash import html, dcc
import numpy as np

def get_layout(opt, year_list):
    ymark = {int(year): str(int(year)) for year in year_list}
    
    app_layout = [
        html.Div([
            html.Div([
                dcc.Dropdown(opt[1:], 'Platform', id='x-axis_column')
                ], style={'padding': '0px 10px', 
                          'width': '49%', 
                          'display': 'inline-block'}),       
            html.Div([
                dcc.Dropdown(opt[1:], value='Genre', id='y-axis_column')
                ], style={'width': '49%', 
                          'display': 'inline-block'}),
            ], style={'margin': 'auto', 'width': '100%'}),
        
        html.Div([        
            html.Div([        
                dcc.Checklist(options=['all'], value=[1], id='toggle_all')
                    ], style={'padding': '10px', 'width':'2%'}),

            html.Div([        
                html.Button('reset', id='toggle_reset', n_clicks=0)
                    ], style={'padding': '10px', 'width':'2.75%'}),
            
            html.Div([
                dcc.Dropdown(options=[], value=[],
                             id='sub_options', multi=True)
                    ], style={'width':'87.5%'})
                
            ], style={'display':'flex'}),
        
        html.Div([
            dcc.Graph(id='scatter-graph'), 
            
            dcc.RangeSlider(
               np.min(year_list),
               np.max(year_list),
               value=[np.min(year_list), np.max(year_list)],
               marks=ymark,
               step=1,
               id='year_slider'
               )
            ])
        ]
    return app_layout