from bokeh.models import ColumnDataSource, Select
from bokeh.plotting import figure, show
from bokeh.layouts import column, row
from bokeh.io import curdoc
from bokeh.models.callbacks import CustomJS
from bokeh.embed import json_item, components

from bokeh.palettes import Category20c
from bokeh.transform import cumsum

import math
import pandas as pd
import json

class PlotService:
    def __init__(self, df : pd.DataFrame, columns):
        self.df = df
        self.columns = columns

    def create_time_series_plot(self):
        # find datetime column
        df_dtypes = self.df.dtypes
        print(df_dtypes)
        # print(self.columns)
        # find datetime column
        datetime_col = df_dtypes[df_dtypes == 'datetime64[ns]'].index[0]   
        # print(datetime_col)
        # Create a ColumnDataSource with the data that contains first [column_count] columns        
        source = ColumnDataSource(data=self.df[self.columns])        
        # Create a new plot
        plot = figure(x_axis_type='datetime', max_height=200)
        # Add lines
        line = plot.line(x=datetime_col, y=self.columns[1], source=source, line_width=2, line_alpha=0.6)
        # Create Select widget by excluding datetime column
        select = Select(title="Select a column", value=self.columns[1], options=[col for col in self.columns if col != datetime_col])
        # Create a callback
        callback = CustomJS(args=dict(source=source, line=line), code="""
            var data = source.data;
            const column = cb_obj.value;
            console.log(column);                
            line.glyph.y.field = column;                            
            source.change.emit();
        """)

        select.js_on_change('value', callback)
        # Create layout
        layout = column(select, plot)
        # return json dump of layout
        return json.dumps(json_item(layout, "time_series_plot"))
    

    def create_pair_scatter_plot(self):        
        print(self.df.dtypes)
        source = ColumnDataSource(data=self.df[self.columns])
        # if df is 50000 or more and column is 10 or more, sample the data
        if len(self.df) >= 50000:
            self.df = self.df.sample(50000, replace=False, random_state=1).sort_index()
            source = ColumnDataSource(data=self.df[self.columns])

        # Create a new plot
        plot = figure()
        # Add circles
        circle = plot.circle(x=self.columns[0], y=self.columns[1], source=source, size=4, color="navy", alpha=0.5)
        # Create Select widget
        select_x = Select(title="Select X column", value=self.columns[0], options=list(self.columns))
        select_y = Select(title="Select Y column", value=self.columns[1], options=list(self.columns))
        # Create a callback
        callback_x = CustomJS(args=dict(source=source, circle=circle), code="""
            var data = source.data;
            const column = cb_obj.value;
            console.log(column)               
            circle.glyph.x.field = column;                            
            source.change.emit();
        """)

        callback_y = CustomJS(args=dict(source=source, circle=circle), code="""
            var data = source.data;
            const column = cb_obj.value;
            console.log(column)               
            circle.glyph.y.field = column;                            
            source.change.emit();
        """)
        select_x.js_on_change('value', callback_x)
        select_y.js_on_change('value', callback_y)
        # Create layout
        layout = column(row(select_x, select_y), plot)
        # return json dump of layout
        return json.dumps(json_item(layout, "pair_scatter_plot"))
        
    def create_pie_chart(self):
        print(self.df.dtypes)
        # Takes only columns with object type
        object_columns = self.df.select_dtypes(include=['object']).columns
        # Create source data from object columns with value counts
        

        # Create a new plot
        plot = figure(x_range=object_columns, plot_height=250, title="Pie Chart")
        # Add pie chart
        plot.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('value', include_zero=True), end_angle=cumsum('value'),
            line_color="white", fill_color=Category20c[5], legend_field='index', source=source)
        # Create select widget to change between columns
        select = Select(title="Select a column", value=object_columns[0], options=list(object_columns))
        # Create a callback to change data source
        callback = CustomJS(args=dict(source=source), code="""
            var data = source.data;
            const column = cb_obj.value;
            console.log(column)               
            source.data = JSON.parse(JSON.stringify(data[column].stack().value_counts()));
            source.change.emit();
        """)
        select.js_on_change('value', callback)
        # Create layout
        layout = column(select, plot)
        # return json dump of layout
        return json.dumps(json_item(layout, "pie_chart"))

        
