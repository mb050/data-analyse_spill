import plotly.graph_objects as go
import plotly.express as px
from .base import Base


class Sale_Graph(Base):
    def graph_func_40(self):
        data = self.data.dropna()
        field = [self.yr_str, self.Yaxis]

        arg = [data, field, self.Yaxis, self.yr_str, self.Yaxis]
        data = self.frequency_filter(*arg)
        Df = self.groupby_agg(data, [self.yr_str, self.Yaxis], self.Xaxis, 4)
        
        color_list = self.custom_color
        n = len(color_list)
        
        fig = go.Figure()
        if self.sub_options is not None:
            Df = self.single_filter(Df, self.Yaxis)
            self.standard_fill(Df, self.Yaxis, color_list, n, fig)
        
        self.standard_line(Df, self.Yaxis, color_list, n, fig)
        
        self.add_title(fig, f'{self.Xaxis} for {self.Yaxis}')
        self.add_label(fig, 'Year', 'Sales in million units')
        return fig
    
    def graph_func_41(self):
        data = self.data.dropna()
        
        data = self.frequency_filter(data, self.Yaxis, self.Yaxis)
        Df = self.groupby_agg(data, self.Yaxis, self.Xaxis)   
        color_list = self.custom_color
        colr = color_list[0]
        
        fig = go.Figure()
        year_arr = Df['Year_of_Release']
        arg = [['total', color_list[1]], ['mean', colr], ['median', colr, 2]] 
        
        self.add_line_fill(fig, Df, 'Year_of_Release', colr[:-2] + '0.1)')
        
        for i, j in enumerate(['sum', 'mean', 'median']):
            self.make_line(fig, year_arr, Df[j], *arg[i])
        
        self.add_title(fig, f'{self.Xaxis}')
        self.add_label(fig, 'Year', 'Sales in million units')
        return fig
    
    def graph_func_42(self):
        field = [self.yr_str, self.Yaxis]
        data = self.groupby_agg(self.data, field, self.Xaxis) 
                                   
        Df = self.single_filter(data, self.Yaxis)
        color_list = self.custom_color
        n = len(color_list)

        fig = go.Figure()
        self.standard_fill(Df, self.Yaxis, color_list, n, fig)
        self.standard_line(Df, self.Yaxis, color_list, n, fig)
        
        self.add_title(fig, f'{self.Xaxis} for {self.Yaxis}')
        self.add_label(fig, 'Year', 'Sales in million units')
        return fig
    
    def graph_func_43(self):
        if self.Yaxis == 'User_Score':
            crit_type = 'User_Count'
        else:
            crit_type = 'Critic_Count'
        
        Df = self.data[[self.Yaxis, self.Xaxis, crit_type]].dropna()
        Df = Df.loc[(Df[self.Xaxis] > 0) & (Df[crit_type] > 0)]
        
        fig = px.scatter(Df, x=self.Xaxis, y=self.Yaxis, size=crit_type)
        fig.update_xaxes(type='log')
        
        self.add_title(fig, f'{self.Xaxis} compared to {self.Yaxis}')
        self.add_label(fig, 'log of sales in million units', 'Score 0 to 100')
        return fig

