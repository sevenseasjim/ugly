import pandas as pd
import numpy as np
import datetime as datetime
from bokeh.plotting import figure, show, save, output_file, vplot
from bokeh.embed import components
#from bokeh.models import CustomJS, ColumnDataSource, Slider
from bokeh.models import ColumnDataSource, Slider

from bokeh.io import output_file, save
from bokeh.models import GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool


def make_cash_data():
    date_format_str = "%Y-%m-%d %H:%M:%S"
    date_parser = lambda u: pd.datetime.strptime(u, date_format_str)
    df = pd.read_csv("../manhattan.csv",
                     parse_dates=True,
                     date_parser=date_parser,
                     header = 0,
                     index_col=1) # peek into the csv: col 0 is 'timestamp'
    # Save only vehicle id
    # down sampling
    df = df.ix[::5]
    df = df[['latitude', 'longitude']]
    df.to_csv('bus_latlon.csv')
    return 0

def read_bus_loc(date):
    date_format_str = '%Y-%m-%d %H:%M:%S'
    date_parser = lambda u: pd.datetime.strptime(u, date_format_str)
    # read it again
    name_list = ['datetime','vehicle_id','latitude','longitude']
    df = pd.read_csv('cash/bus_data.csv',names = name_list, parse_dates=True, date_parser=date_parser,index_col = 0, header=0)
    df = df.ix[::5]

    # pstart = pd.datetime.strptime(date[0]+"/00/00", '%Y/%m/%d/%H/%M')
    pstart = pd.datetime.strptime(date[0]+"/00", '%Y/%m/%d/%H/%M')

    print pstart
    pend   = pd.datetime.strptime(date[1]+"/23", '%Y/%m/%d/%H/%M')
    try:
        df = df.ix[pstart:pend][['latitude','longitude']]
    except:
        df = df[['latitude','longitude']]
    return df

if __name__=='__main__':
    #make_cash_data()
    bus_loc = read_bus_loc(['2015/9/12/10','2015/9/14/17'])
    #Map
    map_options = GMapOptions(lat=40.71, lng=-73.98, map_type="roadmap", zoom=11)

    plot = GMapPlot(
        x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, title="New York City"
    )

    source = ColumnDataSource(data=dict(
        lat=bus_loc['latitude'].values,
        lon=bus_loc['longitude'].values,
    ))

    circle = Circle(x="lon", y="lat", size=1, fill_color="blue", fill_alpha=0.5, line_color=None)
    plot.add_glyph(source, circle)

    plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())
    output_file("gmap_static.html")
    save(plot)
