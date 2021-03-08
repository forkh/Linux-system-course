from flask import Flask, request, render_template, redirect, url_for
import requests
import json
import sys
import os
import matplotlib.pyplot as plt
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)

IMAGES_FOLDER = os.path.join('static')

app.config['IMAGES_FOLDER'] = IMAGES_FOLDER

# Refresh rate of websites
REFRESH_RATE = os.environ['REFRESH_RATE']

# Addresses
REST_API_SERVER_ADDRESS         = os.environ['REST_API_ADDRESS']
CONTROLLER_API_SERVER_ADDRESS   = os.environ['CONTROLLER_API_SERVER_ADDRESS']

# Ports:
REST_API_PORT           = os.environ['REST_API_PORT']
CONTROLLER_SERVICE_PORT = os.environ['CONTROLLER_API_PORT']

# Full address and ports
REST_API_ADDRESS        = 'http://' + REST_API_SERVER_ADDRESS        + ':' + REST_API_PORT
CONTROLLER_API_ADDRESS  = 'http://' + CONTROLLER_API_SERVER_ADDRESS  + ':' + CONTROLLER_SERVICE_PORT

@app.route("/", methods=['GET'])
def main():
    tux_image = os.path.join(app.config['IMAGES_FOLDER'], 'logo.png')
    return render_template("bootstrap_index.html", tux=tux_image)

@app.route("/devices", methods=['GET','POST'])
def device_list():
    tux_image = os.path.join(app.config['IMAGES_FOLDER'], 'logo.png')
    plug_image = os.path.join(app.config['IMAGES_FOLDER'], 'hs110.png')
    on_image = os.path.join(app.config['IMAGES_FOLDER'], 'on.png')
    off_image = os.path.join(app.config['IMAGES_FOLDER'], 'off.png')
    devices = requests.get(REST_API_ADDRESS + "/devices")
    json_data = json.loads(devices.json())
    device_info_all = requests.get(REST_API_ADDRESS + "/device_info_all")
    dev_info_all = json.loads(device_info_all.text)
    return render_template("device_list.html", list1=json_data, tux=tux_image, hs110=plug_image, all_data=dev_info_all, on=on_image, off=off_image)

#@app.route("/device", methods=['GET','POST'])
#def message():
#    tux_image = os.path.join(app.config['IMAGES_FOLDER'], 'logo.png')
#    ip = request.args['ip'].strip('/')
#    socket_data = requests.get(REST_API_ADDRESS + "/device/" + ip)
#    data = json.loads(socket_data.text)
#    data_packet = data[ip]
#    #emeter_stat = data[ip]["emeter_statistics_daily
#    return render_template("index.html", ip=ip, packet=data_packet, tux=tux_image, refresh=REFRESH_RATE)

@app.route("/device", methods=['GET', 'POST'])
def message():
    cwd = os.getcwd()
    print(f'CWD: {cwd}')
    sys.stdout.flush()
    tux_image = os.path.join(app.config['IMAGES_FOLDER'], 'logo.png')
    ip = request.args['ip'].strip('/')
    socket_data = requests.get(REST_API_ADDRESS + "/device/" + ip)
    data = json.loads(socket_data.text)
    on_since = data[ip]["on_since"].split('.')
    data_packet = data[ip]
    emeter_stat = data[ip]["emeter_statistics_daily"]
    values = emeter_stat.values() #    Retrieve dictionary values
    values_list = list(values) #Convert to list
    fig, ax = plt.subplots( nrows=1, ncols=1 )
    plt.plot(values_list)
    plt.ylabel('watts')
    plt.xlabel('dates in this the month')
    #plt.show()
    fig.savefig(cwd + '/website_service/static/plot' + str(ip) + '.png')   # save the figure to file
    #plt.close(fig)
    plot_image = os.path.join(app.config['IMAGES_FOLDER'], 'plot' + str(ip) + '.png')
    return render_template("index.html", ip=ip, packet=data_packet, tux=tux_image, plot=plot_image, On_since=on_since)


#@app.route("/device", methods=['GET','POST'])
#def message():
#    cwd = os.getcwd()
#    tux_image = os.path.join(app.config['IMAGES_FOLDER'], 'logo.png')
#    ip = request.args['ip'].strip('/')
#    #ip = "192.168.8.101"
#    socket_data = requests.get("http://192.168.8.241:3000" + "/device/" + ip)
#    data = json.loads(socket_data.text)
#    print(data)
#    data_packet = data[ip]
#    print(ip)
#    sys.stdout.flush()
#    emeter_stat = data[ip]["emeter_statistics_daily"]
#    values = emeter_stat.values() #    Retrieve dictionary values
#    values_list = list(values) #Convert to list
#    fig, ax = plt.subplots( nrows=1, ncols=1 )
#    plt.plot(values_list)
#    plt.ylabel('watts')
#    plt.xlabel('dates in this the month')
#    #plt.show()
#    output = io.BytesIO()
#    FigureCanvas(fig).print_png(output)
#    fig.savefig(cwd + '/plot.png')   # save the figure to file
#    #fig.savefig(cwd + '/website_service/static/plot.png')   # save the figure to file
#    #print(os.getcwd())
#    #plt.close(fig)
#    #plot_image = os.path.join(app.config['IMAGES_FOLDER'], 'plot.png')
#    #print(plot_image)
#    return render_template("index.html", ip=ip, packet=data_packet, tux=tux_image, refresh=REFRESH_RATE, plot=output.getvalue())

@app.route("/dev", methods=['GET','POST'])
def dev():
    tux_image = os.path.join(app.config['IMAGES_FOLDER'], 'logo.png')
    alias = request.args['alias'].strip('/')
    ip = requests.get(REST_API_ADDRESS + '/ip/' + alias).text
    ip = ip[1:-2]
    socket_data = requests.get(REST_API_ADDRESS + "/device/" + ip)
    data = json.loads(socket_data.text)
    data_packet = data[ip]
    return render_template("index.html", ip=ip, packet=data_packet, tux=tux_image, refresh=REFRESH_RATE)


@app.route("/test", methods=['GET', 'POST'])
def posttest():
    data = request.form
    ip = data["ip"].strip('/')
    onoff = data["onoff"]
    requests.post(REST_API_ADDRESS + '/device/' + ip + '?state=' + onoff)
    return redirect(url_for("message", ip=ip))

@app.route("/test1", methods=['GET'])
def get_ip():
    ip = request.args.get('plug_ip')
    return redirect(url_for("message", ip=ip))

@app.route("/timers", methods=['GET'])
def all_timers():
    tux_image = os.path.join(app.config['IMAGES_FOLDER'], 'logo.png')
    data = requests.get(CONTROLLER_API_ADDRESS + '/timers')
    #print(data.json())
    #sys.stdout.flush()
    return render_template('timers.html', timers=data.json(), tux=tux_image, refresh=REFRESH_RATE)

@app.route("/create_timer_input", methods=['GET'])
def create_timer_input():
    tux_image = os.path.join(app.config['IMAGES_FOLDER'], 'logo.png')
    return render_template('add_timer.html', tux=tux_image)

@app.route("/create_timer", methods=['POST'])
def create_timer():
    data = request.form
    #print(data)
    #sys.stdout.flush()
    post_values = dict()
    post_values['alias'] = data['alias'].upper()
    post_values['deletable'] = data['deletable']
    post_values['comment'] = data['comment']
    if data['time'] != '':
        post_values['time'] = data['time']
    else:
        post_values['time'] = '00:00'
    post_values['date'] = data['date']
    if data['status'].lower() == 'on' or data['status'].lower() == 'off':
        post_values['status'] = data['status'].lower()
    else:
        post_values['status'] = 'OFF'
    requests.post(CONTROLLER_API_ADDRESS + '/create', data = post_values)
    return redirect(url_for("all_timers"))

@app.route("/remove", methods=['POST'])
def remove_timer():
    data = request.form
    #print(data)
    #sys.stdout.flush()
    requests.get(CONTROLLER_API_ADDRESS + '/remove/' + data['removetimer'])
    return redirect(url_for("all_timers"))
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3005)
