import plotly.graph_objects as go
import plotly.express as px
from .base import Base

class Platform_Graph(Base): 
    def graph_func_00(self):
        field = [self.Xaxis, self.Yaxis]
        Df = self.groupby_size(self.data, field, self.Xaxis)

        fig = px.line(Df, x=self.Yaxis, y=Df.columns[-1], markers=True,
                      color=self.Xaxis, hover_name=self.Xaxis)
        
        self.add_label(fig, 'Year', 'N')
        self.add_title(fig, 'N games released on platforms')
        return fig

    def graph_func_01(self):        
        field = [self.Xaxis, self.Yaxis]
        Df = self.groupby_size(self.data, field, self.Yaxis)
        fig = self.make_bar_chart(Df, self.Xaxis, self.Yaxis)
        
        self.add_yaxis(fig, 'N')
        self.add_title(fig, f'N games released for {self.Yaxis}')
        return fig
    
    def graph_func_02(self):
        field = [self.Xaxis, self.yr_str]        
        data = self.data.dropna()
        
        arg = [data, field, self.Yaxis, self.yr_str, self.Xaxis]
        data = self.frequency_filter(*arg)
        
        Df = self.groupby_agg(data, [self.yr_str, self.Xaxis], self.Yaxis, 4)
        color_list = self.custom_color
        n = len(color_list)
        
        fig = go.Figure()
        if self.sub_options is not None:
            Df = self.single_filter(Df, self.Xaxis)
            self.standard_fill(Df, self.Xaxis, color_list, n, fig)

        self.standard_line(Df, self.Xaxis, color_list, n, fig)
        
        self.add_title(fig, f'{self.Yaxis} on a given Platform')
        self.add_xaxis(fig, 'Year')
   
        if self.Yaxis in self.common_field['score']:
            self.add_yaxis(fig, 'Score 0 to 100')
        elif self.Yaxis in self.common_field['review_count']:
            self.add_yaxis(fig, 'N')
        else:
            self.add_yaxis(fig, 'Sales in million units')
        return fig

