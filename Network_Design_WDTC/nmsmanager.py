from nmsservice import NMSService
import json
import datetime

class NMSManager:

    def get_config(self, ip, isTomcast):
        response = NMSService().get_config(ip, isTomcast)
        if json.loads(response["ConnectivityJson"])["Connectivity"] and response["ConfigStatus"]:
            config_file = "RunningConfig_{}_isTomcast_{}_{}.conf".format(ip, isTomcast, str(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
            with open(config_file,"w") as conf:
                conf.write(str(json.loads(response["Config"])["running"]))
            return config_file, "success"
        else:
            return None, response["Error"]

    
    def configure_device(self, ip, isTomcast, config_file):
        with open("configs/{}".format(config_file), "r") as conf_file:
            config= conf_file.read()
            conf_file.close()
        response = NMSService().configure_device(ip, config, isTomcast)
        if json.loads(response["ConnectivityJson"])["Connectivity"] and response["ConfigStatus"]:
            return "Configuration is Successful. Please go to Running Config terminal to see new running config."
        else:
            return response["Error"]

    
    def check_ping_connectivity(self, ip, isTomcast):
        response = NMSService().check_connectivity(ip, isTomcast)
        if json.loads(response["response"])["Connectivity"]:
            return "Connectivity test is successful for IP {}".format(ip)
        elif not json.loads(response["response"])["IPValidity"]:
            return "Invalid IP address"
        else:
            return "No connectivity to IP {}".format(ip)


    