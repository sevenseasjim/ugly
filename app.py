from flask import Flask, render_template, request, redirect
import counts_by_hour
import live_box
import map_static
import map_live

app = Flask(__name__)
app.vars={}

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/bus_count', methods=['Get','post'])
def bus_count():
    if request.method == "GET":
        return render_template('bus_count.html')
    else:
        app.vars['tstart'] = request.form['tstart']
        app.vars['tend'] = request.form['tend']
        date = [app.vars['tstart'],app.vars['tend']]
        script, div = counts_by_hour.plot_count_by_hour(date)
        return render_template('bus_count_plot.html', script=script, div=div)

@app.route('/bus_box')
def bus_box():
    df = live_box.read_bus_count()
    script, div = live_box.Make_boxplot(df)
    return render_template('bus_box.html', script=script, div=div)


@app.route('/bus_static', methods=['Get','post'])
def bus_static():
    if request.method == "GET":
        return render_template('bus_static.html')
    else:
        app.vars['tstart'] = request.form['tstart']
        app.vars['tend'] = request.form['tend']
        date = [app.vars['tstart'],app.vars['tend']]
        nyc = map_static.read_bus_loc(date)
        data = nyc[['latitude','longitude']].values.tolist()
        return render_template('bus_static_plot.html', data=data)

@app.route('/bus_live')
def bus_live():
    nyc = map_live.nyc_current()
    data = nyc[['MonitoredVehicleJourney_VehicleLocation_Latitude',
                'MonitoredVehicleJourney_VehicleLocation_Longitude']].values.tolist()
    return render_template('bus_live.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='0.0.0.0')
