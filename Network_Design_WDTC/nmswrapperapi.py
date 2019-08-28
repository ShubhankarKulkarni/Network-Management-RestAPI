from flask import Flask, jsonify, make_response, request
from flask_httpauth import HTTPBasicAuth
import threading

app = Flask(__name__)
nms_app =  Flask(__name__)
auth = HTTPBasicAuth()

@app.route("/")
def hello():
    return "Hello World!!"

@app.route("/NMSService/GetAllHosts", methods=["GET"])
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

@nms_app.route("/")
def getSomething():
    return "some shit"


def StartServer(flask_obj, host, port):
    try:
        flask_obj.run(host=host, port=port, ssl_context="adhoc")
    except Exception as ex:
        print("Error while running the server {} on port {}".format(host, port))


if __name__ == "__main__":
    server_para = [{"host": "10.0.2.15", "port": "4430", "flask_obj":app},
    {"host":"127.0.0.1","port":"4431", "flask_obj": nms_app}]
    for para in server_para:
        threading.Thread(target="StartServer", args=(para["flask_obj"], para["host"], para["port"]))
    #app.run(host="10.0.2.15", port="4430", ssl_context="adhoc")
    #nms_app.run(host="127.0.0.1", port="4431", ssl_context="adhoc")