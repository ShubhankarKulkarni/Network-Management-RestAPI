from flask import Flask, render_template, Markup, request, send_file
from werkzeug.utils import secure_filename
from nmsmanager import NMSManager
import json
import os

netman_app = Flask(__name__)

UPLOAD_FOLDER = 'configs'
ALLOWED_EXTENSIONS = set(['txt', 'conf'])
netman_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@netman_app.route("/GetConfigPage")
def get_config_page():
    return render_template("getConfig.html")


@netman_app.route("/GetConfig")
def get_config():
    ip = request.args.get("IP")
    isTomcast = json.loads(request.args.get("isTomcast").lower())
    running_config_file, status = NMSManager().get_config(ip, isTomcast)
    if running_config_file:
        return send_file(running_config_file, as_attachment=True)
    else:
        return status


@netman_app.route("/Configure", methods=["GET", "POST"])
def configure():
    if request.method == "POST" and 'config_file' in request.files:
        IP = request.form.get("IP")
        if request.form.get("isTomcast") and request.form.get("isTomcast") == "on":
            isTomcast = True
        else :
            isTomcast = False
        config_file = request.files["config_file"]
        file_name = secure_filename(config_file.filename)
        config_file.save(os.path.join(netman_app.config["UPLOAD_FOLDER"], file_name))
        response = NMSManager().configure_device(IP, isTomcast, file_name)
        return render_template("config.html", running_config=response)
    return render_template("config.html")


# @netman_app.route("/Configure", methods=["POST"])
# def configure_with_file():
#     print(request)
#     return "something"

# @netman_app.route("/DiffConfig")
# def compare_config():
#     differences = ConfigurationFunctions().compare_configuretions()
#     print(differences)
#     return render_template("diffConfig.html", differences=differences)


# @netman_app.route("/OspfConfigJson", methods=["POST"])
# def configure_ospf_with_json():
#     status = ConfigurationFunctions().configure_OSPF(request.get_json())
#     print(status)
#     return status

# @netman_app.route("/Migration")
# def migrate():
#     status = ConfigurationFunctions().perform_migration()
#     return status


@netman_app.route("/PingTest", methods=["GET","POST"])
def ping_test():
    if request.method == "POST":
        ip = request.form.get("IP")
        if request.form.get("isTomcast") and request.form.get("isTomcast") == "on":
            isTomcast = True
        else :
            isTomcast = False
        ping_status = NMSManager().check_ping_connectivity(ip, isTomcast) 
        print(ping_status)
        return render_template("pingtest.html", ping_status=ping_status)
    return render_template("pingtest.html")


@netman_app.route("/")
def index():
    return render_template("main.html")


if __name__ == "__main__":
    netman_app.debug = True
    netman_app.run(host="0.0.0.0", port=8080)
    