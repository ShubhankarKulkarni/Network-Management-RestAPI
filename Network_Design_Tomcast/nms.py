from ipmanager import IPFunctions
from connectivity import Connectivity_Test
from sshinfo import SSH_Info
from getconfig import GetConfig
from setconfig import SetConfig
import json


class ConnectivityStatus:
    IP = ""
    IPValidity = True
    Connectivity = True
    ConnectivityResult = ""


class RouterConfig:
    ConnectivityJson = ""
    ConfigStatus = False
    ConfigChangeStatus = False
    Config = ""
    Error = ""


class InterfaceInformation:
    ConnectivityJson = ""
    InterfaceInfoJson = ""
    InfoStatus = False
    Error = ""


class NMS_Manager:


    @classmethod
    def CheckConnectivity(self, ip):
        result = ConnectivityStatus()
        result.IP = ip
        if IPFunctions.validate_IP_address(ip):
            result.IPValidity = True
            if Connectivity_Test.Check_connectivity(ip):
                result.Connectivity = True
                result.ConnectivityResult = "Successful"
            else:
                result.Connectivity = False
                result.ConnectivityResult = "Unsuccessful"
        else:
            result.IPValidity = False
            result.Connectivity = False
            result.ConnectivityResult = "Unuccessful"
        json_result = json.dumps(result, default=lambda o:o.__dict__)
        return json_result


    def GetRunningConfig(self, ip):
        result = RouterConfig()
        result.ConnectivityJson = self.CheckConnectivity(ip)
        connectivity = json.loads(result.ConnectivityJson)
        if connectivity["IPValidity"] and connectivity["Connectivity"]:
            ssh_information = SSH_Info("sshinfo.json").Get_SSH_Information()
            for router, router_params in ssh_information.items():
                if router_params["ipaddress"] == ip:
                    ssh_connection = GetConfig(router, ip, router_params["username"], router_params["password"], router_params["networkdriver"])
                    result.Config = ssh_connection.get_config_json(router)
                    result.ConfigStatus = True
            if not result.ConfigStatus:
                result.ConfigStatus = False
                result.Error = "SSH Information is not present for IP {}".format(ip)
        else:
            result.Error = "Problem in connecting to IP {}".format(ip)
        json_result = json.dumps(result, default=lambda o:o.__dict__)
        return json_result

    
    def GetInterfacesOnRouter(self, ip):
        result = InterfaceInformation()
        result.ConnectivityJson = self.CheckConnectivity(ip)
        connectivity = json.loads(result.ConnectivityJson)
        if connectivity["IPValidity"] and connectivity["Connectivity"]:
            ssh_information = SSH_Info("sshinfo.json").Get_SSH_Information()
            for router, router_params in ssh_information.items():
                if router_params["ipaddress"] == ip:
                    ssh_connection = GetConfig(router, ip, router_params["username"], router_params["password"], router_params["networkdriver"])
                    result.InterfaceInfoJson = ssh_connection.get_interface_information(router)
                    result.InfoStatus = True
            if not result.InfoStatus:
                result.Error = "SSH Information is not present for IP {}".format(ip)
        else:
            result.Error = "Problem in connecting to IP {}".format(ip)
        json_result = json.dumps(result, default=lambda o:o.__dict__)
        return json_result


    def ConfigureDevice(self, ip, config):
        result = RouterConfig()
        result.ConnectivityJson = self.CheckConnectivity(ip)
        connectivity = json.loads(result.ConnectivityJson)
        if connectivity["IPValidity"] and connectivity["Connectivity"]:
            ssh_information = SSH_Info("sshinfo.json").Get_SSH_Information()
            for router, router_params in ssh_information.items():
                if router_params["ipaddress"] == ip:
                    set_ssh_connection = SetConfig(router, ip, router_params["username"], router_params["password"], router_params["networkdriver"])
                    set_ssh_connection.configure(config)
                    result.ConfigChangeStatus = True
                    get_ssh_connection = GetConfig(router, ip, router_params["username"], router_params["password"], router_params["networkdriver"])
                    result.Config = get_ssh_connection.get_config_json(router)
                    result.ConfigStatus = True
            if not result.ConfigStatus:
                result.ConfigStatus = False
                result.Error = "SSH Information is not present for IP {}".format(ip)
        else:
            result.Error = "Problem in connecting to IP {}".format(ip)
        json_result = json.dumps(result, default=lambda o:o.__dict__)
        return json_result


if __name__ == "__main__":
    #response = NMS_Manager().GetInterfacesOnRouter("198.51.100.10")
    response = NMS_Manager().ConfigureDevice("198.51.100.10","interface FastEthernet 0/1\n ip address 172.16.1.11 255.255.255.0\n no shut\n !\n !\n end\n")




    