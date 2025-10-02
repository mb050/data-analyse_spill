import plotly.express as px
from .base import Base


class Publisher_Graph(Base):
    def graph_func_50(self):
        field = [self.Yaxis, self.Xaxis]
        Df = self.groupby_size(self.data, field, self.Xaxis)
        
        fig = px.line(Df, x=self.Yaxis, y='count', color=self.Xaxis, 
                      markers=True)
        
        self.add_label(fig, 'Year', 'N Games')
        self.add_title(fig, f'N games released by {self.Xaxis}')
        return fig
    
    def graph_func_51(self):
        field = [self.yr_str, self.Xaxis, self.Yaxis]
        Df = self.groupby_size(self.data, field, self.Xaxis)
        fig = self.make_bar_chart(Df, self.yr_str, self.Yaxis)
        
        title_str = f'N Games released by {self.Xaxis} for {self.Yaxis}'
        self.add_title(fig, title_str)
        self.add_label(fig, 'Year', 'N Games')
        return fig
    
    def graph_func_52(self):
        field = self.common_field['sales']
        
        Df = self.groupby_agg(self.data, [self.Xaxis, self.yr_str], field, 1)
        Df = self.single_filter(Df, self.Xaxis)
        
        fig = px.area(Df, x=self.yr_str, y=field, markers=True,
                      color_discrete_sequence=px.colors.qualitative.Dark24)
        
        self.add_title(fig, f'{self.Yaxis} for {self.Xaxis}')
        self.add_label(fig, 'Year', 'Sales in million units') 
        return fig

    def graph_func_53(self):
        Df = self.data[[self.Xaxis, 'Critic_Score', 'User_Score']]
        Df = self.single_filter(Df, self.Xaxis)
        fig = self.make_box_chart(Df, self.Xaxis)
        
        self.add_yaxis(fig, 'Score 0 to 100')
        self.add_title(fig, f'Score for {self.Xaxis}')
        return fig

    def graph_func_54(self):
        field = self.common_field['review_count']
        Df = self.groupby_agg(self.data, self.Xaxis, field, 1)
        Df = self.single_filter(Df, self.Xaxis)
        
        fig = self.make_bar_chart(Df, self.Xaxis, 'variable', 1, 'variable',
                                  'value')
        self.add_yaxis(fig, 'N Reviews')
        self.add_title(fig, f'Review count for {self.Xaxis}')
        return fig

