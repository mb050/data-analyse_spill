import plotly.graph_objects as go
import plotly.express as px
import numpy as np

class Base():
    def make_line(self, fig, x_val, y_val, name, line_color, dash=False, 
                  showlegend=True, mode='lines+markers'):
        var_dict = {'x': x_val, 'y': y_val, 'name': name, 'mode': mode,
                    'line_color': line_color, 'showlegend': showlegend}
        
        if dash is not False:
            var_dict['line_dash'] = str(dash)
        
        fig.add_trace(go.Scatter(**var_dict))
        
    def standard_line(self, dataframe, column, color_list, n, fig):
        for j, i in enumerate(dataframe[column].unique()):
            arr = dataframe[dataframe[column]==i]            
            year_arr = arr['Year_of_Release']

            colr = color_list[j%n]
            self.make_line(fig, year_arr, arr['median'], f"{i}-median", colr,
                           2, False)
            self.make_line(fig, year_arr, arr['mean'], f"{i}-mean", colr)

    
    def add_line_fill(self, fig, dataframe, field, fill_color, 
                      fill_name='min_max'):
        x_val = dataframe[field]
        min_arr = dataframe['min']
        
        x_val = np.concatenate((x_val, x_val[::-1]))
        min_max = np.concatenate((min_arr, dataframe['max'][::-1]))

        fig.add_trace(go.Scatter(x=x_val, y=min_max,
                                  mode='lines+markers',
                                  fill='toself',
                                  fillcolor=fill_color,
                                  line_color='rgba(255,255,255,0)',
                                  name=fill_name,
                                  showlegend=False))
        
    def standard_fill(self, dataframe, column, color_list, n, fig, 
                      field='Year_of_Release'):
        for j, i in enumerate(dataframe[column].unique()):
            arr = dataframe[dataframe[column]==i]
            
            fill_color = color_list[j%n][:-2] + '0.1)'
            self.add_line_fill(fig, arr, field, fill_color, f"{i}-min_max")
            
    
    def add_label(self, fig, xaxis_str='', yaxis_str=''):
        if xaxis_str != '':
            fig.update_layout(xaxis=dict(title=dict(text=xaxis_str)))
        
        if yaxis_str != '':
            fig.update_layout(yaxis=dict(title=dict(text=yaxis_str)))
        
    def add_title(self, fig, text):
        fig.update_layout(title_text=text, title_x=0.5)
    
    def add_xaxis(self, fig, text_str):
        fig.update_layout(xaxis=dict(title=dict(text=text_str)))
        
    def add_yaxis(self, fig, text_str):
        fig.update_layout(yaxis=dict(title=dict(text=text_str)))
    
    def groupby_size(self, dataframe, field, std_filter=None, 
                     column_name='count'):
        dataframe = dataframe.groupby(field, as_index=False).size()
        dataframe.columns = field + [column_name]
        
        if std_filter is not None:
            dataframe = self.standard_filter(dataframe, std_filter)
        
        return dataframe

    def groupby_count(self, dataframe, field, columns):
        dataframe = dataframe.groupby(field, as_index=False)[columns].count()
        return dataframe

    def groupby_agg(self, dataframe, field, agg_field, amount=None):
        agg_list = ['sum', 'median', 'mean', 'min', 'max']
        Slice = slice(None)
        
        if amount == 1:
            Slice = 0 
        elif amount == 4:
            Slice = slice(1, None)
        
        dataframe = dataframe.groupby(field, as_index=False)
        return dataframe[agg_field].agg(agg_list[Slice])
    
    def make_bar_chart(self, dataframe, x_val, color_field, melt_df=False, 
                       var_name='Source', value_name='Score', 
                       dafault_color=True):
        if melt_df is not False:
            color_field = var_name
            dataframe = dataframe.melt(id_vars=[x_val], var_name=var_name, 
                                       value_name=value_name)
        y_val = dataframe.columns[-1]
        
        if dafault_color is True:
            fig = px.bar(dataframe, x=x_val, y=y_val, color=color_field, 
                         color_continuous_scale=px.colors.sequential.Jet)
        else:
            fig = px.bar(dataframe, x=x_val, y=y_val, color=color_field)
            
        self.add_bar_chart_number(fig, dataframe, x_val, y_val)
        return fig
    
    def add_bar_chart_number(self, fig, dataframe, column, value_column):
        dataframe = dataframe.groupby(column, as_index=False)
        dataframe = dataframe[value_column].agg('sum')
        
        fig.add_trace(go.Scatter(
                        x=dataframe[column], 
                        y=dataframe[value_column],
                        text=dataframe[value_column],
                        mode='text',
                        textposition='top center',
                        showlegend=False))
    
    def make_box_chart(self, dataframe, field, var_name='Source', 
                       val_name='Score'):
        dataframe = dataframe.melt(id_vars=[field], 
                                   var_name=var_name, 
                                   value_name=val_name)
        
        fig = px.box(dataframe, x=field, y=val_name, color=var_name)
        return fig
    
    def frequency_filter(self, dataframe, field, filter_var, field_1=None, 
                       field_2=None, minimum=5):        
        filtered = dataframe.groupby(field)[filter_var].agg(count='count')
        filtered = filtered.loc[filtered['count'] >= minimum].reset_index()
        
        if field_1 is None:
            field_1 = field
        
        if field_2 is None:
            return self.single_filter(dataframe, field_1, filtered)
        
        con = [0, 0]
        for i, j in enumerate([field_1, field_2]):
            con[i] = self.single_filter(dataframe, j, filtered, False)

        return self.double_filter(dataframe, *con)
    
    def standard_filter(self, dataframe, field):
        if self.sub_options is not None:
            dataframe = dataframe[dataframe[field].isin(self.sub_options)]
        
        return dataframe
    
    def single_filter(self, dataframe, field, column=None, normal=True):
        if column is None:
            column = self.sub_options
        else:
            column = column[field]
            
        data = dataframe[field].isin(column)
        if normal is True:
            return dataframe[data]
        else:
            return data
    
    def double_filter(self, dataframe, condition_1, condition_2):
        return dataframe[condition_1 & condition_2]
