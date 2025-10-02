import plotly.graph_objects as go
from .base import Base


class Count_Graph(Base):
    def graph_func_70(self):
        field = self.common_field['review_count']
        Df = self.groupby_agg(self.data, self.Yaxis, field, 1)
        Df = self.standard_filter(Df, self.Yaxis)
        
        fig = self.make_bar_chart(Df, self.Yaxis, 'Source', 1)
        self.add_yaxis(fig, 'N Reviews')
        self.add_title(fig, f'N Reviews for {self.Yaxis}') 
        return fig
    
    def graph_func_71(self):
        field = ['Year_of_Release', 'Critic_Score', 'User_Score']
        Df = self.data[field].dropna()        
        fig = self.make_box_chart(Df, 'Year_of_Release')
        
        self.add_label(fig, 'Year', 'Score 0 to 100')
        self.add_title(fig, 'Comparison') 
        return fig
    
    def graph_func_72(self):
        color_list = ['rgba(0, 72, 255, 1)', 'rgba(255, 24, 24, 1)']
        data = self.frequency_filter(self.data, self.Yaxis, self.Xaxis)
        Df = self.groupby_agg(data, self.Yaxis, self.Xaxis, 4)
        column = self.Yaxis
        
        fig = go.Figure()
        self.add_line_fill(fig, Df, self.yr_str, 'rgba(100, 143, 255, 0.25)')
        
        for i, j in enumerate(['mean', 'median']):
            self.make_line(fig, Df[column], Df[j], j, color_list[i])
            
        self.add_title(fig, 'N Reviews over the years')
        self.add_label(fig, 'Year', 'N Reviews') 
        return fig
    
    def graph_func_73(self):
        color_list = ['rgba(0, 72, 255, 1)', 'rgba(255, 24, 24, 1)']
        arg = [self.data, self.Xaxis, self.Yaxis, None, None, 3]
        data = self.frequency_filter(*arg)

        Df = self.groupby_agg(data, self.Xaxis, self.Yaxis, 4)
        column = self.Xaxis

        fig = go.Figure()
        self.add_line_fill(fig, Df, self.Xaxis, 'rgba(100, 143, 255, 0.25)')
        
        for i, j in enumerate(['mean', 'median']):
            self.make_line(fig, Df[column], Df[j], j, color_list[i])
        
        self.add_title(fig, f'N Reviews compared to {self.Yaxis}')
        self.add_label(fig, 'Sales in million units', 'N Reviews') 
        return fig
