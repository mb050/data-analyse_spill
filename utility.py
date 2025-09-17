from dash import Dash, html, dash_table, dcc, callback, Output, Input, callback_context
from graph_class import Graph_Class
import pandas as pd
import numpy as np
import json as js

class Utility(Graph_Class):
    def __init__(self, dataframe, json_file):
        self.yr_str = 'Year_of_Release'
        self.js_file = json_file
        self.df = dataframe
        
        self.color_map = self.js_file['color_map']
        self.custom_color = list(map(self.convert_hex, self.color_map))
        
        self.reduced_column_list = self.js_file['sub_options']

        self.sub_option_dict = self.get_sub_options()
        self.get_special_cases()
                               
        year_list = self.column_options('Year_of_Release')
        self.year_list = np.sort(year_list)[:-2]

        self.year_column = self.df['Year_of_Release']
        key_list = self.js_file['shared_functions']
        
        func_list = [self.platform_graph, self.year_graph, self.genre_graph, 
                     self.rating_graph, self.sale_graph, self.publisher_graph, 
                     self.score_graph, self.count_graph]
        
        self.function_dict = self.get_function_dict(key_list, func_list)
    
    def convert_hex(self, x):
        x = x[1:]
        deci = [int(x[i*2:(i+1)*2], 16) for i in range(3)]
        return 'rgba({},{},{},1)'.format(*deci)
        
    def column_options(self, column_name):
        return list(self.df[column_name].dropna().unique())

    def get_sub_options(self):
        sub_option = {}
        for i in self.reduced_column_list:
            sub_option[i] = self.column_options(i)
        return sub_option

    def get_special_cases(self):
        case_dict = self.js_file['sub_option_exceptions']
        self.special_cases = {}
        
        for i in case_dict.keys():
            self.special_cases[i] = {}
            temp = case_dict[i]
            
            for j in temp.keys():
                if type(temp[j]) != list:
                    self.special_cases[i][j] = self.sub_option_dict[temp[j]]
                else:
                    self.special_cases[i][j] = temp[j]
        
        return self.special_cases

    def effective_sub_option(self, yaxis_name, toggle_all, sub_options):
        if len(sub_options) != 0:
            return sub_options
        elif 'all' in toggle_all:
            try:
                return self.sub_option_dict[yaxis_name]
            except:
                return None

    def get_function_dict(self, key_list, func_list):
        func_dict = {}
        for i, nested_names in enumerate(key_list):
            val = [func_list[i]] * len(nested_names)
            func_dict.update(dict(zip(nested_names, val)))
            
        return func_dict

    def get_year_df(self, data, year_value):
        a = np.where(self.year_list == year_value[0])[0][0]
        b = np.where(self.year_list == year_value[1])[0]
        
        if len(b) == 0:
            b = None
        else:
            b = b[0] + 1
            
        return data[self.year_column.isin(self.year_list[a:b])]
