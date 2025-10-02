from types import FunctionType
import numpy as np

from .publisher_graph import Publisher_Graph
from .platform_graph import Platform_Graph
from .rating_graph import Rating_Graph
from .genre_graph import Genre_Graph
from .score_graph import Score_Graph
from .count_graph import Count_Graph
from .year_graph import Year_Graph
from .sale_graph import Sale_Graph

class Utility(Platform_Graph, Year_Graph, Genre_Graph, Publisher_Graph, 
              Rating_Graph, Sale_Graph, Score_Graph, Count_Graph):
    def __init__(self, dataframe, json_file):
        self.common_field = json_file['fields']
        self.yr_str = 'Year_of_Release'
        self.js_file = json_file
        self.df = dataframe
        
        self.check_instances()
        
        self.color_map = self.js_file['color_map']
        self.custom_color = list(map(self.convert_hex, self.color_map))
        
        self.reduced_column_list = self.js_file['sub_options']

        self.sub_option_dict = self.get_sub_options()
        self.get_special_cases()
                               
        year_list = self.column_options('Year_of_Release')
        self.year_list = np.sort(year_list)[:-2]

        self.year_column = self.df['Year_of_Release']
        return

    def check_instances(self):
        cls_names = type(self).__mro__[:-1]
        instance_dict = {}
        
        for i in cls_names:
            I = i.__dict__
            for j in I.keys():
                if isinstance(I[j], FunctionType):
                    self.filter_instances(j, I[j], instance_dict)

        self.make_func_dict(instance_dict)

    def make_func_dict(self, instance_dict):        
        shared_func = self.js_file["shared_functions"]
        class_idx = self.js_file['class_idx']
        is_path = self.js_file["instance_path"]
        
        var_combination = {i: {} for i in class_idx.values()}
        func_dict = {}
        
        for i in is_path:
            val = is_path[i]
            for j in val:
                var_combination[class_idx[j[0]]][i] = instance_dict[j]
        
        dict_const = 0
        dict_tuple = lambda x: (x, dict_const)
        
        for i, (key, val) in enumerate(shared_func.items()):
            dict_const = var_combination[key]
            func_dict.update(dict(map(dict_tuple, val)))
            
        self.func_dict = func_dict

    def graph_control(self, dataframe, Xaxis, Yaxis, year_value, toggle_all, 
                      sub_option):
        sub_option = self.effective_sub_option(Yaxis, toggle_all, sub_option)
        
        if self.check_developer_publisher(Xaxis, Yaxis, sub_option):
            return
        
        self.data = self.get_year_df(dataframe, year_value)
        
        self.sub_options = sub_option
        self.Xaxis = Xaxis
        self.Yaxis = Yaxis
        
        return self.func_dict[Xaxis][Yaxis](self)
    
    def filter_instances(self, key, value, dictionary):
        if 'graph_func_' not in key:
            return
        
        dictionary[key[-2:]] = value
    
    def compare(self, var, const=['Developer', 'Publisher']):
        return 1 if var in const else 0
    
    def check_developer_publisher(self, x_var, y_var, sub_options):
        var = [x_var, y_var]
        if x_var == 'Rating' and sum(map(self.compare, [y_var])) > 0:
            return

        if sum(map(self.compare, var)) > 0 and sub_options is None:
            return True
        
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

    def get_common_field(self):
        self.common_field = self.js_file['fields']

    def get_year_df(self, data, year_value):
        a = np.where(self.year_list == year_value[0])[0][0]
        b = np.where(self.year_list == year_value[1])[0]
        
        if len(b) == 0:
            b = None
        else:
            b = b[0] + 1
            
        return data[self.year_column.isin(self.year_list[a:b])]
