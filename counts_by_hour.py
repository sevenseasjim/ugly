import pandas as pd
import numpy as np
import datetime as datetime
from bokeh.plotting import figure, show, save, output_file, vplot
from bokeh.embed import components
#from bokeh.models import CustomJS, ColumnDataSource, Slider
from bokeh.models import ColumnDataSource, Slider

def make_cash_data():
    date_format_str = "%Y-%m-%d %H:%M:%S"
    date_parser = lambda u: pd.datetime.strptime(u, date_format_str)
    df = pd.read_csv("manhattan.csv",
                     parse_dates=True,
                     date_parser=date_parser,
                     header = 0,
                     index_col=1) # peek into the csv: col 0 is 'timestamp'
    # Save only vehicle id
    df = df[['vehicle_id','latitude','longitude']]
    df.to_csv('bus_data.csv')
    return 0

_df = None

def get_df():
    global _df
    if _df is None:
        from time import time
        t0 = time()
        print '>>> reading...'
        date_format_str = '%Y-%m-%d %H:%M:%S'
        date_parser = lambda u: pd.datetime.strptime(u, date_format_str)
        name_list = ['datetime','vehicle_id','latitude','longitude']
        _df = pd.read_csv('cash/bus_data.csv', names=name_list, parse_dates=True, date_parser=date_parser,index_col = 0, header=0)
        print '...done! took %s s' % (time() - t0)
    return _df


def plot_count_by_hour(date):
    # read it again
    pstart = pd.datetime.strptime(date[0], '%Y/%m/%d/%H')
    pend   = pd.datetime.strptime(date[1], '%Y/%m/%d/%H')
    try:
        df = get_df().ix[pstart:pend]
    except:
        # pass
        df = get_df()
    bus_count  = df['vehicle_id'].groupby(pd.TimeGrouper(freq='30min')).nunique()

    # bokeh plot
    plot = figure(x_axis_type = 'datetime')
    plot.title = 'bus count'
    plot.grid.grid_line_alpha=0.3
    plot.xaxis.axis_label = 'Time'
    plot.yaxis.axis_label = 'Bus Count'

    plot.line(np.array(bus_count.index, dtype=np.datetime64), bus_count.values, line_color='blue', line_width=2)

    #slider = Slider(start=0.1, end=4, value=1, step=.1, title='power', callback=callback)

    #output_file('plot.html')
    #save(plot) 
    script, div = components(plot)
    return script, div


if __name__=='__main__':
    #make_cash_data()
    plot_count_by_hour(['2015/9/12/10','2015/9/14/17'])
