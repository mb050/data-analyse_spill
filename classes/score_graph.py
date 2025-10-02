import plotly.express as px
from .base import Base

class Score_Graph(Base):
    def graph_func_60(self):
        Df = self.data[[self.Yaxis, 'Critic_Score', 'User_Score']]
        Df = self.standard_filter(Df, self.Yaxis)
        fig = self.make_box_chart(Df, self.Yaxis)
        
        self.add_yaxis(fig, 'Score 0 to 100')
        self.add_title(fig, f'Score for {self.Yaxis}')
        return fig
    
    def graph_func_61(self):
        if self.Xaxis == 'User_Score':
            crit_type = 'User_Count'
        else:
            crit_type = 'Critic_Count'
            
        Df = self.data[[self.Xaxis, self.Yaxis, crit_type]].dropna()
        Df = Df.loc[(Df[self.Yaxis] > 0) & (Df[crit_type] > 0)]
        
        fig = px.scatter(Df, x=self.Yaxis, y=self.Xaxis, size=crit_type, 
                         labels={self.Xaxis: 'Score 0 to 100'})
        fig.update_xaxes(type='log')
        self.add_title(fig, f'{self.Xaxis} compared to {self.Yaxis}')
        self.add_xaxis(fig, 'log of sales in million units')
        return fig
    
    def graph_func_62(self):
        if self.Xaxis == 'User_Score':
            crit_type = 'User_Count'
        else:
            crit_type = 'Critic_Count'
        
        Df = self.data[[self.Xaxis, crit_type]]
        fig = px.box(Df, x=self.Yaxis, y=self.Xaxis)
        
        self.add_label(fig, 'N Reviews', 'Score 0 to 100')
        
        if self.Yaxis == 'User_Count':
            fig.update_xaxes(type='log')
            self.add_xaxis(fig, 'log of N Reviews')
        
        self.add_title(fig, f'{self.Xaxis} compared to {self.Yaxis}') 
        return fig
    
    def graph_func_63(self):
        field = ['Year_of_Release', 'Critic_Score', 'User_Score']
        Df = self.data[field].dropna()        
        fig = self.make_box_chart(Df, 'Year_of_Release')
        
        self.add_title(fig, f'{self.Xaxis} compared to {self.Yaxis}') 
        self.add_label(fig, 'Year', 'Score 0 to 100')
        return fig
    