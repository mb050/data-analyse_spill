import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

class Graph_Class():
    def convert_hex(self, x):
        x = x[1:]
        deci = [int(x[i*2:(i+1)*2], 16) for i in range(3)]
        return 'rgba({},{},{},1)'.format(*deci)

    def standard_line(self, dataframe, column, color_list, n, fig):
        for j, i in enumerate(dataframe[column].unique()):
            arr = dataframe[dataframe[column]==i]            
            year_arr = arr['Year_of_Release']

            colr = color_list[j%n]
            fig.add_trace(go.Scatter(x=year_arr, y=arr['median'],
                                     line_color=colr,
                                     mode='lines+markers',
                                     name=f"{i}-median",
                                     line_dash='2',
                                     showlegend=False))
            
            fig.add_trace(go.Scatter(x=year_arr, y=arr['mean'],
                                     line_color=colr,
                                     mode='lines+markers',
                                     name=f"{i}-mean"))
    
    
    def standard_fill(self, dataframe, column, color_list, n, fig):
        for j, i in enumerate(dataframe[column].unique()):
            arr = dataframe[dataframe[column]==i]

            year_arr = arr[self.yr_str]
            min_arr = arr['min']
            
            year_arr = np.concatenate((year_arr, year_arr[::-1]))
            min_max = np.concatenate((min_arr, arr['max'][::-1]))
            colr = color_list[j%n]
    
            fig.add_trace(go.Scatter(x=year_arr, y=min_max,
                                     mode='lines+markers',
                                     fill='toself',
                                     fillcolor=colr[:-2] + '0.1)',
                                     line_color='rgba(255,255,255,0)',
                                     name=f"{i}-min_max",
                                     showlegend=False))
    
    def platform_graph(self, data, xaxis_name, yaxis_name, sub_options): 
        if yaxis_name == self.yr_str:
            field = [xaxis_name, yaxis_name]
            De = data.groupby(field, as_index=False).size()
            De.columns = field + ['count']
        
            if sub_options is not None:
                De = De[De[yaxis_name].isin(sub_options)]
            
            fig = px.line(De, x=yaxis_name, y=De.columns[-1], 
                          color=xaxis_name, hover_name=xaxis_name,markers=True)
            return fig
               
        if yaxis_name in ['Genre', 'Publisher', 'Developer', 'Rating']:
            if sub_options is None:
                return
            
            field = [xaxis_name, yaxis_name]
            De = data.groupby(field, as_index=False).size()
            De.columns = field + ['count']
        
            if sub_options is not None:
                De = De[De[yaxis_name].isin(sub_options)]
                
            fig = px.bar(De, x=xaxis_name, y='count', color=yaxis_name)
            return fig
        
        else:
            data = data.dropna()
            data_year = data.groupby([xaxis_name, 'Year_of_Release']
                                     )[yaxis_name].agg(count='count')
                                     
            data_year = data_year.loc[data_year['count'] > 5].reset_index()
            data = data[data[self.yr_str].isin(data_year[self.yr_str]) 
                        & data[xaxis_name].isin(data_year[xaxis_name])]
            
            De = data.groupby(
                    [self.yr_str, xaxis_name])[yaxis_name].agg(
                    ['median', 'mean', 'min', 'max']).reset_index() 
                    
            color_list = self.custom_color
            n = len(color_list)
            
            fig = go.Figure()
            if sub_options is not None:
                De = De[De[xaxis_name].isin(sub_options)]
                
                self.standard_fill(De, xaxis_name, color_list, n, fig)

            self.standard_line(De, xaxis_name, color_list, n, fig)            
            return fig

    def year_graph(self, data, xaxis_name, yaxis_name, sub_options):
        field = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 
                 'Global_Sales']
        cds = px.colors.qualitative.Dark24
        
        if yaxis_name in ['Platform', 'Genre', 'Publisher', 'Rating', 
                          'Developer']:
            De = data.groupby(['Year_of_Release', yaxis_name], 
                              as_index=False).size()
                              
            De.columns = [xaxis_name, yaxis_name, 'amount']
            
            if sub_options is not None:
                De = De[De[yaxis_name].isin(sub_options)]
            
            fig = px.bar(De, x=self.yr_str, y='amount', color=yaxis_name, 
                         color_discrete_sequence=cds)
            return fig
        
        elif yaxis_name in field:
            field = field[:-1]
            De = data.groupby([self.yr_str], as_index=False)[field].agg('sum')
                              
            if yaxis_name == 'Global_Sales':
                if sub_options is not None:
                    field = sub_options
                
                fig = px.area(De, x=self.yr_str, y=field, markers=True,
                              color_discrete_sequence=cds)
            else:    
                fig = px.line(De, x=self.yr_str, y=yaxis_name, markers=True, 
                              color_discrete_sequence=cds)
          
        elif yaxis_name == 'Review_Count':
            field = ['Critic_Count', 'User_Count']
            
            if sub_options is not None:
                field = sub_options
            
            De = data.groupby(self.yr_str, as_index=False)[field].agg('sum')
            fig = px.line(De, x=self.yr_str, y=field, markers=True,
                          color_discrete_sequence=cds)
        
        elif yaxis_name == 'Score':
            De = data[[self.yr_str, 'Critic_Score', 'User_Score']]
            De = De.melt(id_vars=[self.yr_str], 
                         var_name='Source', 
                         value_name='Score')
            
            fig = px.box(De, x=self.yr_str, y='Score', color='Source')
        else:
            De = data.groupby([self.yr_str], as_index=False).size()
            De.columns = [xaxis_name, 'n games']
            fig = px.line(De, x=self.yr_str, y=De.columns[-1], markers=True)
        return fig

    def genre_graph(self, data, xaxis_name, yaxis_name, sub_options):
         cds = px.colors.qualitative.Dark24
         if yaxis_name == 'Platform':
             field = [xaxis_name, yaxis_name]
             De = data.groupby(field, as_index=False).size()
             De.columns = field + ['count']
             
             if sub_options is not None:
                 De = De[De[yaxis_name].isin(sub_options)]
             
             fig = px.bar(De, x=xaxis_name, y='count', color=yaxis_name, 
                          color_continuous_scale=px.colors.sequential.Jet)
         
         if yaxis_name == 'Year_of_Release':
             field = [xaxis_name, yaxis_name]
             De = data.groupby(field, as_index=False).size()
             De.columns = field + ['count']
             
             if sub_options is not None:
                 De = De[De[xaxis_name].isin(sub_options)]
             
             fig = px.bar(De, x=yaxis_name, y='count', color=xaxis_name, 
                          color_continuous_scale=px.colors.sequential.Jet)
         
         if yaxis_name in ['Publisher', 'Developer'] and sub_options is None:
                 return
         elif yaxis_name in ['Publisher', 'Developer', 'Rating']:
             field = [xaxis_name, yaxis_name]
             De = data.groupby(field, as_index=False).size()
             De.columns = field + ['count']
             
             if sub_options is not None:
                 De = De[De[yaxis_name].isin(sub_options)]
             
             fig = px.bar(De, x=xaxis_name, y='count', color=yaxis_name, 
                          color_continuous_scale=px.colors.sequential.Jet)
         
         if yaxis_name == 'Score':
             De = data[[xaxis_name, 'Critic_Score', 'User_Score']]
             De = De.melt(id_vars=[xaxis_name], 
                          var_name='Source', 
                          value_name='Score')
             
             fig = px.box(De, x=xaxis_name, y='Score', color='Source')
             
         if yaxis_name == 'Review_Count':
             field = ['Critic_Count', 'User_Count']
             
             if sub_options is not None:
                 field = sub_options
             
             De = data.groupby(xaxis_name, as_index=False)[field].agg('sum')
             De = De.melt(id_vars=[xaxis_name])

             fig = px.bar(De, x=xaxis_name, y='value', color='variable')
        
         else:
             field = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 
                      'Global_Sales']
             De = data.groupby([xaxis_name, 'Year_of_Release'], 
                               as_index=False)[field].agg('sum')
             fig = px.area(De, x=self.yr_str, y=yaxis_name, markers=True, 
                           color=xaxis_name,
                           color_discrete_sequence=cds)
         return fig

    def publisher_graph(self, data, xaxis_name, yaxis_name, sub_options):
        if sub_options is None:
            return 
        
        if yaxis_name == 'Year_of_Release':
            field = [yaxis_name, xaxis_name]
            De = data.groupby(field, as_index=False).size()
            De.columns = field + ['count']
            
            if sub_options is not None:
                De = De[De[xaxis_name].isin(sub_options)]
            
            fig = px.line(De, x=yaxis_name, y='count', color=xaxis_name, 
                          markers=True)
        
        if yaxis_name in ['Platform', 'Genre', 'Rating']:
            field = [self.yr_str, xaxis_name, yaxis_name]
            De = data.groupby(field, as_index=False).size()
            De.columns = field + ['count']
            
            if sub_options is not None:
                De = De[De[xaxis_name].isin(sub_options)]
            
            fig = px.bar(De, x='Year_of_Release', y='count', color=yaxis_name,
                         color_continuous_scale=px.colors.sequential.Jet)
        
        if yaxis_name == 'Sales':
            field = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 
                              'Global_Sales']
            
            De = data.groupby([xaxis_name, self.yr_str], 
                              as_index=False)[field].agg('sum')
            
            De = De[De[xaxis_name].isin(sub_options)]
            fig = px.area(De, x=self.yr_str, y=field, markers=True,
                          color_discrete_sequence=px.colors.qualitative.Dark24)
        
        if yaxis_name == 'Score':
            De = data[[xaxis_name, 'Critic_Score', 'User_Score']]
            De = De[De[xaxis_name].isin(sub_options)]
            De = De.melt(id_vars=[xaxis_name], 
                         var_name='Source', 
                         value_name='Score')
            
            fig = px.box(De, x=xaxis_name, y='Score', color='Source')
        
        if yaxis_name =='Review_Count':
            field = ['Critic_Count', 'User_Count']

            De = data.groupby(xaxis_name, as_index=False)[field].agg('sum')
            De = De[De[xaxis_name].isin(sub_options)]
            De = De.melt(id_vars=[xaxis_name])

            fig = px.bar(De, x=xaxis_name, y='value', color='variable') 
            
        return fig

    def rating_graph(self, data, xaxis_name, yaxis_name, sub_options):
        if yaxis_name in ['Platform', 'Genre']:
            field = [xaxis_name, yaxis_name]
            De = data.groupby(field, as_index=False).size()
            De.columns = field + ['count']
            
            if sub_options is not None:
                De = De[De[yaxis_name].isin(sub_options)]
            
            return px.bar(De, x=xaxis_name, y='count', color=yaxis_name,
                          color_continuous_scale=px.colors.sequential.Jet)
        
        elif yaxis_name == 'Year_of_Release':
            field = [yaxis_name, xaxis_name]
            De = data.groupby(field, as_index=False).size()
            De.columns = field + ['count']
            
            if sub_options is not None:
                De = De[De[xaxis_name].isin(sub_options)]
            
            return px.bar(De, x=yaxis_name, y='count', color=xaxis_name)
        
        elif yaxis_name in ['Publisher', 'Developer']:
            field = [xaxis_name, yaxis_name]
            De = data.groupby(field, as_index=False).size()
            De.columns = field + ['count']
            
            rating = self.sub_option_dict[xaxis_name]
            
            if sub_options is not None:
                De = De[De[yaxis_name].isin(sub_options)]
                
                fig = px.bar(De, x=xaxis_name, y='count', color=yaxis_name,
                             color_continuous_scale=px.colors.sequential.Jet)
                return fig
            else:
                for i in rating:
                    rating_range = De.loc[De[xaxis_name] == i]['count']
                    rating_arr = np.unique(rating_range, return_counts=True)
                    
                    if len(rating_arr[0]) >= 10:
                        n = rating_arr[0][-10]
                    else:
                        n = rating_arr[0][-1]
                    
                    De.loc[(De[xaxis_name] == i) & (De['count'] < n), 
                           yaxis_name] = 'other'
            
                De = De.groupby([xaxis_name, yaxis_name], 
                                as_index=False)['count'].agg('sum')
                
                fig = px.bar(De, x=xaxis_name, y='count', color=yaxis_name,
                             color_continuous_scale=px.colors.sequential.Jet)
            
        elif yaxis_name == 'Score':
            De = data[[xaxis_name, 'Critic_Score', 'User_Score']]
            
            if sub_options is not None:
                De = De[De[xaxis_name].isin(sub_options)]
            
            De = De.melt(id_vars=[xaxis_name], 
                         var_name='Source', 
                         value_name='Score')
            
            fig = px.box(De, x=xaxis_name, y='Score', color='Source')
        
        elif yaxis_name =='Review_Count':
            field = ['Critic_Count', 'User_Count']
            De = data.groupby(xaxis_name, as_index=False)[field].agg('sum')
            
            if sub_options is not None:
                De = De[De[xaxis_name].isin(sub_options)]
                
            De = De.melt(id_vars=[xaxis_name])
            fig = px.bar(De, x=xaxis_name, y='value', color='variable') 
        
        else:
            field = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 
                     'Global_Sales']
            
            De = data.groupby([xaxis_name, 'Year_of_Release'], 
                              as_index=False)[field].agg('sum')
            fig = px.area(De, x='Year_of_Release', y=yaxis_name, markers=True, 
                          color=xaxis_name)    
        return fig

    def sale_graph(self, data, xaxis_name, yaxis_name, sub_options):
        if yaxis_name in ['Platform', 'Genre', 'Rating']:
            year_str = 'Year_of_Release'
            data = data.dropna()
            data_year = data.groupby([year_str, yaxis_name]
                                     )[yaxis_name].agg(count='count')

            data_year = data_year.loc[data_year['count'] >= 5].reset_index()
            data = data[data[year_str].isin(data_year[year_str]) 
                        & data[yaxis_name].isin(data_year[yaxis_name])]

            De = data.groupby([year_str, yaxis_name])[xaxis_name].agg(
                              ['median', 'mean', 'min', 'max']).reset_index() 
            
            color_list = self.custom_color
            
            n = len(color_list)
            
            fig = go.Figure()
            if sub_options is not None:
                De = De[De[yaxis_name].isin(sub_options)]
                self.standard_fill(De, yaxis_name, color_list, n, fig)
            
            self.standard_line(De, yaxis_name, color_list, n, fig)
            
            return fig
        
        if yaxis_name == 'Year_of_Release':        
            data = data.dropna()        
            data_year = data.groupby(yaxis_name)[yaxis_name].agg(count='count')
            data_year = data_year.loc[data_year['count'] >= 5].reset_index()
            data = data[data[yaxis_name].isin(data_year[yaxis_name])]

            De = data.groupby([yaxis_name])[xaxis_name].agg(
                ['sum', 'median', 'mean', 'min', 'max']).reset_index() 
            
            color_list = self.custom_color
            colr = color_list[0]
            
            fig = go.Figure()        
            year_arr = De['Year_of_Release']
            
            year_arr_fill = np.concatenate((year_arr, year_arr[::-1]))
            min_max = np.concatenate((De['min'], De['max'][::-1]))
            
            fig.add_trace(go.Scatter(x=year_arr_fill, y=min_max,  
                                     mode='lines+markers',
                                     fill='toself',
                                     fillcolor=colr[:-2] + '0.1)',
                                     line_color='rgba(255,255,255,0)',
                                     name=f"{xaxis_name}-min_max",
                                     showlegend=False))
            
            fig.add_trace(go.Scatter(x=year_arr, y=De['sum'],  
                                     mode='lines+markers',
                                     line_color=color_list[1],
                                     name="total"))
            
            fig.add_trace(go.Scatter(x=year_arr, y=De['mean'],  
                                     mode='lines+markers',
                                     line_color=colr,
                                     name="mean"))
            
            fig.add_trace(go.Scatter(x=year_arr, y=De['median'],  
                                     mode='lines+markers',
                                     line_color=colr,
                                     line_dash='2',
                                     name="median"))
            return fig

        if yaxis_name in ['Publisher', 'Developer']:        
            if sub_options is None:
                return
            
            data = data.groupby([self.yr_str, yaxis_name])[xaxis_name].agg(
                ['sum', 'median', 'mean', 'min', 'max']).reset_index()
            
            De = data[data[yaxis_name].isin(sub_options)]
            color_list = self.custom_color
            n = len(color_list)
            
            fig = go.Figure()
            N = len(sub_options)
            idx = list(np.arange(N)) * 2
            for k, (j, i) in enumerate(zip(idx, sub_options * 2)):
                arr = De[De[yaxis_name]==i]
                year_arr = arr['Year_of_Release']
                colr = color_list[j%n]
                
                if k < N:
                    min_arr = arr['min']
                    
                    year_arr = np.concatenate((year_arr, year_arr[::-1]))
                    min_max = np.concatenate((min_arr, arr['max'][::-1]))
                    
                    fig.add_trace(go.Scatter(x=year_arr, y=min_max,
                                              mode='lines+markers',
                                              fill='toself',
                                              fillcolor=colr[:-2] + '0.1)',
                                              line_color='rgba(255,255,255,0)',
                                              name=f"{i}-min_max",
                                              showlegend=False))
                    continue
                
                fig.add_trace(go.Scatter(x=year_arr, y=arr['median'],
                                          mode='lines+markers',
                                          line_color=colr,
                                          name=f"{i}-median",
                                          line_dash='2',
                                          showlegend=False))
                
                fig.add_trace(go.Scatter(x=year_arr, y=arr['mean'],
                                          mode='lines+markers',
                                          line_color=colr,
                                          name=f"{i}-mean"))        
            return fig

        if yaxis_name in ['Critic_Score', 'User_Score']:
            if yaxis_name == 'User_Score':
                crit_type = 'User_Count'
            else:
                crit_type = 'Critic_Count'
            
            De = data[[yaxis_name, xaxis_name, crit_type]].dropna()
            De = De.loc[(De[xaxis_name] > 0) & (De[crit_type] > 0)]
            
            fig = px.scatter(De, x=xaxis_name, y=yaxis_name, size=crit_type)
            fig.update_xaxes(type='log')
            return fig


    def score_graph(self, data, xaxis_name, yaxis_name, sub_options):
        if xaxis_name == 'User_Score':
            crit_type = 'User_Count'
        else:
            crit_type = 'Critic_Count'
        
        if yaxis_name in ['Platform', 'Genre', 'Year_of_Release', 'Rating', 
                          'Publisher', 'Developer']:
            if sub_options is None and yaxis_name in ['Publisher',
                                                      'Developer']:
                return
            
            De = data[[yaxis_name, 'Critic_Score', 'User_Score']]

            if sub_options is not None:
                De = De[De[yaxis_name].isin(sub_options)]

            De = De.melt(id_vars=[yaxis_name], 
                         var_name='Source', 
                         value_name='Score')
            fig = px.box(De, x=yaxis_name, y='Score', color='Source')
            return fig
        
        if yaxis_name in ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 
                          'Global_Sales']:        
            De = data[[xaxis_name, yaxis_name, crit_type]].dropna()
            De = De.loc[(De[yaxis_name] > 0) & (De[crit_type] > 0)]
            
            fig = px.scatter(De, x=yaxis_name, y=xaxis_name, size=crit_type)
            fig.update_xaxes(type='log')
            return fig

        if yaxis_name in ['Critic_Count', 'User_Count']:
            De = data[[xaxis_name, crit_type]]
            
            fig = px.box(De, x=yaxis_name, y=xaxis_name)
            if yaxis_name == 'User_Count':
                fig.update_xaxes(type='log')
            return fig
            
        if yaxis_name in ['Critic_Score', 'User_Score']:
            field = ['Year_of_Release', 'Critic_Score', 'User_Score']
            De = data[field].dropna()

            De = De.melt(id_vars=['Year_of_Release'], 
                         var_name='Source', 
                         value_name='Score')
            fig = px.box(De, x='Year_of_Release', y='Score', color='Source')        
            return fig
        
    def count_graph(self, data, xaxis_name, yaxis_name, sub_options):            
        if yaxis_name in ['Platform', 'Genre', 'Rating', 
                          'Publisher', 'Developer']:
            if sub_options is None and yaxis_name in ['Publisher', 
                                                      'Developer']:
                return
            
            field = ['Critic_Count', 'User_Count']
            De = data.groupby(yaxis_name, as_index=False)[field].agg('sum')
            
            if sub_options is not None:
                De = De[De[yaxis_name].isin(sub_options)]

            De = De.melt(id_vars=[yaxis_name], 
                         var_name='Source', 
                         value_name='Score')
            
            fig = px.bar(De, x=yaxis_name, y='Score', color='Source')
            return fig
        
        if yaxis_name == 'Score':
            field = ['Year_of_Release', 'Critic_Score', 'User_Score']
            De = data[field].dropna()

            De = De.melt(id_vars=['Year_of_Release'], 
                         var_name='Source', 
                         value_name='Score')
            
            fig = px.box(De, x='Year_of_Release', y='Score', color='Source')
            return fig
        
        if yaxis_name == 'Year_of_Release':
            year_df = data.groupby(yaxis_name)[xaxis_name].agg(count='count')
            year_df = year_df.loc[year_df['count'] > 5].reset_index()

            data = data[data[yaxis_name].isin(year_df['Year_of_Release'])]
            field = ['Critic_Count']

            De = data.groupby([yaxis_name], as_index=False)[xaxis_name].agg(
                ['median', 'mean', 'min', 'max'])
            column = yaxis_name
        
        else:
            year_df = data.groupby(xaxis_name)[yaxis_name].agg(count='count')
            year_df = year_df.loc[year_df['count'] > 0].reset_index()

            data = data[data[xaxis_name].isin(year_df[xaxis_name])]
            field = ['Critic_Count']

            De = data.groupby([xaxis_name], as_index=False)[yaxis_name].agg(
                ['median', 'mean', 'min', 'max'])    
            
            column = xaxis_name
            
        fig = go.Figure()        
        fig.add_trace(
            go.Scatter(x=De[column], y=De['min'],
                mode='lines', name='min', line_dash='2',
                line_color='rgba(100, 143, 255, 0.5)'))
                          
        fig.add_trace(
            go.Scatter(x=De[column], y=De['max'],
                mode='lines', name='max', fill='tonexty', 
                line_dash='2',
                fillcolor='rgba(100, 143, 255, 0.25)',
                line_color='rgba(100, 143, 255, 0.5)'))
        
        fig.add_trace(
            go.Scatter(x=De[column], y=De['mean'],
                mode='lines+markers', name='mean', 
                line_color='rgba(0, 72, 255, 1)'))
         
        fig.add_trace(
            go.Scatter(x=De[column], y=De['median'],
                mode='lines+markers', name='median', 
                line_color='rgba(255, 24, 24, 1)'))
        
        return fig


