import json
import requests
import pandas as pd
from bokeh.io import output_file, save
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool
)

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


if __name__=="__main__":
    df = nyc_current()
    bus_loc = df[['MonitoredVehicleJourney_VehicleLocation_Latitude', 'MonitoredVehicleJourney_VehicleLocation_Longitude']]
    #Map
    map_options = GMapOptions(lat=40.71, lng=-73.98, map_type="roadmap", zoom=11)

    plot = GMapPlot(x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, title="New York City")
    source = ColumnDataSource(data=dict(
        lat=df['MonitoredVehicleJourney_VehicleLocation_Latitude'].values,
        lon=df['MonitoredVehicleJourney_VehicleLocation_Longitude'].values,
    ))

    circle = Circle(x="lon", y="lat", size=10, fill_color="blue", fill_alpha=0.8, line_color=None)
    plot.add_glyph(source, circle)

    plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())
    output_file("gmap_live.html")
    save(plot)
