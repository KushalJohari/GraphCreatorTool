import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from io import BytesIO

Data = None

class graph():
    def __init__(self, data):
        self.data = data
        self.x = None
        self.y = None
        self.a = None
        self.b = None
        self.c = None
        self.axis_count = None
        self.axis_mean = None
        self.axis_sum = None
        self.axis_value = None
        self.axis_uni = None

    def xaxis(self):
        # self.x = input("X-axis")
        if self.x in Data.columns:
            self.a = Data[self.x]
              
    def yaxis(self):
        # self.y = input("Y-axis")
        if self.y in Data.columns:
            self.b = Data[self.y]

    def axiscount(self):
        # self.axis_count = input("Enter count: ")
        if self.axis_count in Data.columns:
            self.a = Data.groupby([self.c])[self.axis_count].count()
        else:
            return('error, cannot count this column')
        
    def axissum(self):
        if self.axis_sum in Data.columns:
            self.a = Data.groupby([self.c])[self.axis_sum].sum()
        else:
            return('error, cannot count this column')
        
    def axismean(self):
        if self.axis_mean in Data.columns:
            self.a = Data.groupby([self.c])[self.axis_mean].mean()

    def axisValueCount(self):
        if self.axis_value in Data.columns:
            self.a = Data[self.axis_value].value_counts()
        
    def barGraph(self):
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.set_facecolor((1,1,1,0.0))
        fig.patch.set_facecolor((1,1,1,0.0))
        if self.b is None:
            self.a.plot(kind='bar', ax=ax, color= color)
            ax.set_xlabel(self.axis_count or self.axis_sum or self.axis_mean or self.axis_value,color='white', size=14)
            ax.set_ylabel('value', color='white', size=14)
            ax.set_xticks(range(len(self.a.index)))
            ax.set_xticklabels(self.a.index, rotation=90, color='white')
            ax.tick_params(axis='x', colors= 'white', labelsize=12)
            ax.tick_params(axis='y', colors= 'white', labelsize=12)
        elif self.a is not None and self.b is not None:
            ax.bar(self.a, self.b, color= 'cyan')
            ax.set_xlabel(self.x)
            ax.set_ylabel(self.y)
            ax.tick_params(axis='x', colors= 'white', labelsize=12)
            ax.tick_params(axis='y', colors= 'white', labelsize=12)
        return fig

    
    def linePlot(self):
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.set_facecolor((1,1,1,0.0))
        fig.patch.set_facecolor((1,1,1,0.0))
        if self.b is None and self.a is not None:
            self.a.plot(kind='line', marker='o', ax=ax, linestyle='--', color=color)
            ax.set_xlabel(self.axis_count or self.axis_sum or self.axis_mean or self.axis_value, color='white', size=14)
            ax.set_ylabel('value', color='white', size=14)
            ax.set_xticks(range(len(self.a.index)))
            ax.set_xticklabels(self.a.index, rotation=90, color= 'white')
            ax.tick_params(axis='x', colors= 'white', labelsize=12)
            ax.tick_params(axis='y', colors= 'white', labelsize=12)
        elif self.a is not None and self.b is not None:
            ax.plot(self.a, self.b, marker='o')
            ax.set_xlabel(self.x)
            ax.set_ylabel(self.y)
            ax.tick_params(axis='x', labelrotation=90, colors= 'white')
            ax.tick_params(axis='y', colors= 'white')
        return fig

    def pieChart(self):
        fig, ax = plt.subplots(figsize=(10,5))
        ax.set_facecolor((1,1,1,0.0))
        fig.patch.set_facecolor((1,1,1,0.0))
        if self.a is not None:
            ax.pie(self.a, labels=self.a.index, autopct='%.2f%%', textprops={'color':'white'})
        elif self.b is not None:
            ax.pie(self.b, labels=self.b.index, autopct='%.2f%%', textprops={'color':'white'})
        return fig
    
    def histogram(self):
        fig, ax = plt.subplots(figsize=(10,5))
        ax.set_facecolor((1,1,1,0.0))
        fig.patch.set_facecolor((1,1,1,0.0))
        if self.b is None:
            self.a.plot(kind='hist', color= color)
            ax.set_xlabel(self.axis_count or self.axis_sum or self.axis_mean or self.axis_value or self.x or self.y, color= 'white', size=14)
            ax.set_ylabel("Value", color= 'white', size=14)
            ax.tick_params(axis='x', colors= 'white', labelsize=12)
            ax.tick_params(axis='y', colors= 'white', labelsize=12)
            ax.legend()
        elif self.a is None:
            self.b.plot(kind='hist')
            ax.set_xlabel(self.axis_count or self.axis_sum or self.axis_mean or self.axis_value or self.x or self.y, color='white', size=14)
            ax.set_ylabel("Value", color= 'white', size=14)
            ax.tick_params(axis='x', colors= 'white', labelsize=12)
            ax.tick_params(axis='y', colors= 'white', labelsize=12)
            ax.legend()
        return fig

def fig_to_img(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches= 'tight')
    buf.seek(0)
    return buf


    
st.title("Graph Creator Tool")
upload_file = st.file_uploader("Load Csv", type='csv')

if upload_file is not None:
    Data = pd.read_csv(upload_file)
    st.success("Your file is uploaded!")

if Data is not None and not Data.empty:
    columns = [None] + Data.columns.to_list()
    x_val = st.selectbox("Select X-axis",options=columns)
    y_val = st.selectbox("Select y-axis",options=columns)
    agg = st.selectbox("Select Aggregation", options=[None,'count','mean','sum', 'value_counts'])
    Graphtype = st.selectbox("Select Graph Type", options=['BarGraph', 'LinePlot', 'PieChart', 'Histogram'])
    color = st.color_picker("Pick a color for your graph", '#00FFFF')


    if st.button("Generate Graph"):
        g = graph(Data)
        g.x = x_val
        g.y = y_val

        if agg == 'count':
            g.axis_count = y_val
            g.c = x_val
            g.axiscount()
        elif agg == 'mean':
            g.axis_mean = y_val
            g.c = x_val
            g.axismean()
        elif agg == 'sum':
            g.axis_sum = y_val
            g.c = x_val
            g.axissum()
        elif agg == 'value_counts':
            if Graphtype == 'PieChart':
                g.axis_value = y_val or x_val
                g.c = x_val or y_val
                g.axisValueCount()
            else:  
                g.axis_value = y_val
                g.c = x_val
                g.axisValueCount()
        else:
            g.xaxis()
            g.yaxis()
        if Graphtype == 'LinePlot':
            fig = g.linePlot()
        elif Graphtype == 'BarGraph':
            fig = g.barGraph()
        elif Graphtype == 'PieChart':
            fig = g.pieChart()
        elif Graphtype == 'Histogram':
            fig = g.histogram()
        else:
            st.error("Select the Graph Type!")

        st.pyplot(fig)

        img_Data = fig_to_img(fig)
        st.download_button(label='Download Graph', data=img_Data, file_name='graph.png', mime='image/png')

        
