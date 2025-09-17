from dash import Dash, dcc, callback, Output, Input, callback_context
import pandas as pd
import numpy as np
import json as js

from layout import get_layout
from utility import Utility

default_port = 8057

file = open('menu_option.json', 'r')
js_file = js.load(file)
file.close()

c_list = js_file['color_map']
option_dict = js_file['main_option']

df = pd.read_csv('Video_Games_Sales_22_Dec_2016.csv')
df['User_Score'] = pd.to_numeric(df['User_Score'], errors='coerce')
df.loc[:, "User_Score"] *= 10

app = Dash()
opt = list(df.columns)

util = Utility(df, js_file)

reduced_column_list = util.reduced_column_list
sub_option_dict = util.sub_option_dict

special_cases = util.special_cases

year_list = util.year_list

year_column = df['Year_of_Release']
app.layout = get_layout(opt, year_list)

function_dict = util.function_dict

@app.callback(Output('y-axis_column', 'style'),
              Output('y-axis_column', 'options'),
              Output('y-axis_column', 'value'),
              Input('x-axis_column', 'value'))
def toggle_container(toggle_value):
    return {'display': 'block'}, option_dict[toggle_value], None

@app.callback(Output('sub_options', 'style'),
              Output('sub_options', 'options'),
              Input('x-axis_column', 'value'),
              Input('y-axis_column', 'value'))
def sub_container(xaxis_input, yaxis_input):
    try:
        return {'display': 'block'}, special_cases[xaxis_input][yaxis_input]
    except:
        pass
    
    if yaxis_input in reduced_column_list:
        return {'display': 'block'}, sub_option_dict[yaxis_input]
    elif xaxis_input in ['Publisher', 'Developer']:
        return {'display': 'block'}, sub_option_dict[xaxis_input]
    
    else:
        return {'display': 'none'}, []

@app.callback(Output('toggle_all', 'value'),
              Output('sub_options', 'value'),
              Output('toggle_reset', 'n_clicks'),
              Input('toggle_all', 'value'),
              Input('sub_options', 'value'),
              Input('toggle_reset', 'n_clicks'))
def sub_container_display(toggle_all, sub_display, clicks=0):
    if clicks != 0:
        return [1], [], 0 
    elif 'all' in toggle_all and toggle_all[0] == 0:
        return [1, 'all'], [], clicks
    
    if len(sub_display) > 0:
        return [0], sub_display, clicks
    elif 'all' in toggle_all:
        return [1, 'all'], [], clicks
    else:
        return [1], [], clicks


@callback(
    Output('scatter-graph', 'figure'),
    Input('x-axis_column', 'value'),
    Input('y-axis_column', 'value'), 
    Input('year_slider', 'value'), 
    Input('toggle_all', 'value'),
    Input('sub_options', 'value'))
def update_graph(xaxis_name, yaxis_name, year_value, toggle_all, sub_option):
    if yaxis_name is None:
        return
    
    sub_option = util.effective_sub_option(yaxis_name, toggle_all, sub_option)
    D = util.get_year_df(df, year_value)
    arg = [D, xaxis_name, yaxis_name, sub_option]
    
    return function_dict[xaxis_name](*arg)

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8057)
    print(f'go to http://127.0.0.1:8057/{default_port}')
    # pass
