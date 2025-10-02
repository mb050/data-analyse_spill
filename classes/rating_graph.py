import plotly.express as px
import numpy as np
from .base import Base

class Rating_Graph(Base):
    def graph_func_30(self):
        field = [self.Xaxis, self.Yaxis]
        Df = self.groupby_size(self.data, field, self.Yaxis)
        fig = self.make_bar_chart(Df, self.Xaxis, self.Yaxis)
        
        self.add_yaxis(fig, 'N Games')
        self.add_title(fig, f'N games with rating for {self.Yaxis}')
        return fig
    
    def graph_func_31(self):
        field = [self.Yaxis, self.Xaxis]        
        Df = self.groupby_size(self.data, field, self.Xaxis)
        fig = self.make_bar_chart(Df, self.Yaxis, self.Xaxis)
        
        self.add_label(fig, 'Year', 'N Games')
        self.add_title(fig, 'N games released with rating')
        return fig

    def graph_func_32(self):
        field = [self.Xaxis, self.Yaxis]
        Df = self.groupby_size(self.data, field)
        rating = self.sub_option_dict[self.Xaxis]
        
        if self.sub_options is not None:
            Df = self.single_filter(Df, self.Yaxis)
        else:
            for i in rating:
                rating_range = Df.loc[Df[self.Xaxis] == i]['count']
                rating_arr = np.unique(rating_range, return_counts=True)
                
                if len(rating_arr[0]) >= 10:
                    n = rating_arr[0][-10]
                else:
                    n = rating_arr[0][-1]
                
                Df.loc[(Df[self.Xaxis] == i) & (Df['count'] < n), 
                       self.Yaxis] = 'other'
        
            Df = self.groupby_agg(Df, [self.Xaxis, self.Yaxis], 'count', 1)
        
        fig = self.make_bar_chart(Df, self.Xaxis, self.Yaxis)
        self.add_title(fig, f'N games released by {self.Yaxis}')
        self.add_yaxis(fig, 'N Games')
        return fig
    
    def graph_func_33(self):
        Df = self.data[[self.Xaxis, 'Critic_Score', 'User_Score']]
        Df = self.standard_filter(Df, self.Xaxis)
        fig = self.make_box_chart(Df, self.Xaxis)
        
        self.add_yaxis(fig, 'Score 0 to 100')
        self.add_title(fig, 'Score for a given rating')
        return fig
    
    def graph_func_34(self):
        field = self.common_field['review_count']
        
        Df = self.groupby_agg(self.data, self.Xaxis, field, 1)
        Df = self.standard_filter(Df, self.Xaxis)
        
        fig = self.make_bar_chart(Df, self.Xaxis, 'variable', 1, 'variable', 
                                  'value')
        self.add_yaxis(fig, 'N Reviews')
        self.add_title(fig, 'Review count for a given rating')
        return fig
    
    def graph_func_35(self):
        primary_field = [self.Xaxis, 'Year_of_Release']
        field = self.common_field['sales']
        
        Df = self.groupby_agg(self.data, primary_field, field, 1)
        fig = px.area(Df, x='Year_of_Release', y=self.Yaxis, markers=True, 
                      color=self.Xaxis)
        
        self.add_label(fig, 'Year', 'Sales in million units')
        self.add_title(fig, 'Sales for a given rating')
        return fig

