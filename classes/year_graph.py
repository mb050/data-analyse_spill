import plotly.express as px
from .base import Base


class Year_Graph(Base):
    def graph_func_10(self):
        field = ['Year_of_Release', self.Yaxis]
        Df = self.groupby_size(self.data, field, self.Yaxis, 'amount')
        fig = self.make_bar_chart(Df, self.yr_str, self.Yaxis)
        
        self.add_yaxis(fig, 'N')
        self.add_title(fig, f'N games released for {self.Yaxis}')
        return fig

    def graph_func_11(self):
        field = self.common_field['sales']
        cds = px.colors.qualitative.Dark24
        field = field[:-1]
        
        Df = self.groupby_agg(self.data, self.yr_str, field, 1)
                          
        if self.Yaxis == 'Global_Sales':
            if self.sub_options is not None:
                field = self.sub_options
            
            fig = px.area(Df, x=self.yr_str, y=field, markers=True,
                          color_discrete_sequence=cds)
        else:    
            fig = px.line(Df, x=self.yr_str, y=self.Yaxis, markers=True, 
                          color_discrete_sequence=cds)
            
        self.add_title(fig, self.Yaxis)
        self.add_label(fig, 'Year', 'Sales in million units')
        return fig
    
    def graph_func_12(self):
        cds = px.colors.qualitative.Dark24
        field = self.common_field['review_count']
        
        if self.sub_options is not None:
            field = self.sub_options
        
        Df = self.groupby_agg(self.data, self.yr_str, field, 1)
        fig = px.line(Df, x=self.yr_str, y=field, markers=True,
                      color_discrete_sequence=cds)
        
        self.add_title(fig, 'Review count')
        self.add_label(fig, 'Year', 'N Review')
        return fig
    
    def graph_func_13(self):
        Df = self.data[[self.yr_str, 'Critic_Score', 'User_Score']]
        fig = self.make_box_chart(Df, self.yr_str)
        
        self.add_title(fig, 'Review score')
        self.add_label(fig, 'Year', 'Score 0 to 100')
        return fig
    
    def graph_func_14(self):
        Df = self.groupby_size(self.data, [self.Xaxis])
        fig = px.line(Df, x=self.yr_str, y=Df.columns[-1], markers=True)
        
        self.add_label(fig, 'Year', 'N games released')
        self.add_title(fig, 'Number of games Released')
        return fig
