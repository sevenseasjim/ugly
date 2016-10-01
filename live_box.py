import json
import requests
import pandas as pd
from bokeh.io import output_file, save

def make_cash_data():
    date_format_str = "%Y-%m-%d %H:%M:%S"
    date_parser = lambda u: pd.datetime.strptime(u, date_format_str)
    df = pd.read_csv("../manhattan.csv",
                     parse_dates=True,
                     date_parser=date_parser,
                     header = 0,
                     index_col=1) # peek into the csv: col 0 is 'timestamp'
    # Save only vehicle id
    df = df[['vehicle_id','latitude', 'longitude']]
    #df.to_csv('bus_id.csv')
    df_bus_count = df['vehicle_id'].groupby(pd.TimeGrouper(freq='60min')).nunique()
    bus_count = pd.DataFrame({'hour': df_bus_count.index.hour,
                              'bus_count': df_bus_count.values})
    bus_count.to_csv('cash/bus_count_static.csv')
    return df, bus_count
                            
def _flatten_dict(root_key, nested_dict, flattened_dict):
    for key, value in nested_dict.iteritems():
        next_key = root_key + "_" + key if root_key != "" else key
        if isinstance(value, dict):
            _flatten_dict(next_key, value, flattened_dict)
        else:
            flattened_dict[next_key] = value
    return flattened_dict
    
#This is useful for the live MTA Data
def nyc_current():
    MTA_API_BASE = "http://bustime.mta.info/api/siri/vehicle-monitoring.json?key={}"
    MTA_API_KEY="6c3380cc-279a-4cbe-99d3-a51bdd760b2e"
    resp = requests.get(MTA_API_BASE.format(MTA_API_KEY)).json()
    #resp = requests.get('http://api.prod.obanyc.com/api/siri/vehicle-monitoring.json',params=dict(key=MTA_API_KEY)).json()
    info = resp['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']
    return pd.DataFrame([_flatten_dict('', i, {}) for i in info])

def read_bus_count():
    bus_count = pd.read_csv('cash/bus_count_static.csv', index_col = 0)
    return bus_count

def Make_boxplot(df):
    from bokeh.charts import BoxPlot, Scatter, output_file, show
    from bokeh.models.glyphs import Circle
    from bokeh.embed import components
    plot = BoxPlot(df, values='bus_count', label='hour', color='hour', title="Historical Bus Count Chart")
    #output_file("boxplot.html")
    #save(plot)
    script, div = components(plot)
    return script, div
    
if __name__=="__main__":
    #df, bus_count =  make_cash_data()

    #df_live = nyc_current()
    #print df_live['RecordedAtTime']
    bus_count = read_bus_count()
    Make_boxplot(bus_count)

    

    
    
