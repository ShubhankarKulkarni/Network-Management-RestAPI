from flask import Flask, jsonify, make_response, request, abort
from flask_httpauth import HTTPBasicAuth
from nms import NMS_Manager
import threading

app = Flask(__name__)
#nms_app =  Flask(__name__)
auth = HTTPBasicAuth()


administrators = {
    "wdtcadmin":"password@1233",
    "tomcastadmin":"tomcast@123"
}

@auth.get_password
def get_pass(username):
    if username in administrators:
        return administrators.get(username)
    return None


@app.route("/")
@auth.login_required
def hello():
    return "Hello World!!" + auth.username()

@app.route("/NMSService/GetAllHosts", methods=["GET"])
@auth.login_required
def GetAllHosts():
    hosts = [
        {
            "id":1,
            "name": "Something"
        },
        {
            "id":2,
            "name":"Something_else"
        }
    ]

    return jsonify({"hosts": hosts})

# @nms_app.route("/")
# def getSomething():
#     return "some shit"

@app.route("/NMSService/CheckConnectivity", methods=["GET"])
@auth.login_required
def check_connectivity():
    IP = request.args.get("IP")
    response = NMS_Manager.CheckConnectivity(IP)
    return jsonify({"response": response})


@app.route("/NMSService/GetConfig", methods=["GET"])
@auth.login_required
def get_config():
    IP = request.args.get("IP")
    response = NMS_Manager().GetRunningConfig(IP)
    return response


@app.route("/NMSService/GetInterfaces", methods=["GET"])
@auth.login_required
def get_interfaces():
    IP = request.args.get("IP")
    response = NMS_Manager().GetInterfacesOnRouter(IP)
    return response


@app.route("/NMSService/ConfigureDevice", methods=["POST"])
@auth.login_required
def configure_device():
    if not request.json or not "IP" in request.json or not "Config" in request.json:
        abort(400)
    IP = request.json["IP"]
    config = request.json["Config"]
    response = NMS_Manager().ConfigureDevice(IP, config)
    return response


if __name__ == "__main__":
    # server_para = [{"host": "10.0.2.15", "port": "4430", "flask_obj":app},
    # {"host":"127.0.0.1","port":"4431", "flask_obj": nms_app}]
    # for para in server_para:
    #     threading.Thread(target="StartServer", args=(para["flask_obj"], para["host"], para["port"]))
    app.run(host="192.168.1.2", port="4430", ssl_context=("cert1.pem","key1.pem"))
    #nms_app.run(host="127.0.0.1", port="4431", ssl_context="adhoc")