import plotly.express as px
from .base import Base

class Genre_Graph(Base):
    def graph_func_20(self):
        field = [self.Xaxis, self.Yaxis]
        Df = self.groupby_size(self.data, field, self.Yaxis)
        fig = self.make_bar_chart(Df, self.Xaxis, self.Yaxis)
        
        self.add_yaxis(fig, 'N Games')
        self.add_title(fig, f'N games released on {self.Yaxis} in a genre')
        return fig
    
    def graph_func_21(self):
        field = [self.Xaxis, self.Yaxis]
        Df = self.groupby_size(self.data, field, self.Xaxis)
        fig = self.make_bar_chart(Df, self.Yaxis, self.Xaxis)
        
        self.add_label(fig, 'Year', 'N Games')
        self.add_title(fig, 'N games released for a given genre')
        return fig
        
    def graph_func_22(self):
        field = [self.Xaxis, self.Yaxis]
        Df = self.groupby_size(self.data, field, self.Yaxis)
        fig = self.make_bar_chart(Df, self.Xaxis, self.Yaxis)
        
        if self.Yaxis == 'Rating':
            edit_str = 'with'
        else:
            edit_str = 'by'
        
        title_str = str('N games released {} {} for a given genre'
                        ).format(edit_str, self.Yaxis)
        
        self.add_title(fig, title_str)
        self.add_yaxis(fig, 'N Games')
        return fig
        
    def graph_func_23(self):
        Df = self.data[[self.Xaxis, 'Critic_Score', 'User_Score']]
        fig = self.make_box_chart(Df, self.Xaxis)
        
        self.add_yaxis(fig, 'Score 0 to 100')
        self.add_title(fig, 'Review score')
        return fig
    
    def graph_func_24(self):
        field = self.common_field['review_count']
        
        if self.sub_options is not None:
            field = self.sub_options
        
        Df = self.groupby_agg(self.data, self.Xaxis, field, 1)
        fig = self.make_bar_chart(Df, self.Xaxis, 'variable', 1, 'variable', 
                                  'value')
        self.add_yaxis(fig, 'N Review')
        self.add_title(fig, 'Review count')
        return fig
       
    def graph_func_25(self):
        primary_field = [self.Xaxis, 'Year_of_Release']
        cds = px.colors.qualitative.Dark24
        field = self.common_field['sales']
        
        Df = self.groupby_agg(self.data, primary_field, field, 1)
        fig = px.area(Df, x=self.yr_str, y=self.Yaxis, markers=True, 
                      color=self.Xaxis,
                      color_discrete_sequence=cds)
        
        self.add_title(fig, f'{self.Yaxis} for genre')
        self.add_label(fig, 'Year', 'Sales in million units')
        return fig
