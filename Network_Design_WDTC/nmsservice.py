from requests.auth import HTTPBasicAuth
import requests


class NMSService:


    def configure_device(self, ip, config, isTomcast):
        parameters = {"IP":ip, "Config": config}
        if isTomcast:
            response = requests.post("https://2b18347a.ngrok.io/NMSService/ConfigureDevice", json=parameters, auth=HTTPBasicAuth("tomcastadmin","tomcast@123"))#, verify="cert1.pem"
            return response.json()


    def get_interfaces(self, ip, isTomcast):
        parameters = {"IP":ip}
        if isTomcast:
            response = requests.get("https://2b18347a.ngrok.io/NMSService/GetInterfaces", params=parameters, auth=HTTPBasicAuth("tomcastadmin","tomcast@123"))#, verify="cert1.pem"
            return response.json()


    def get_config(self, ip, isTomcast):
        parameters = {"IP":ip}
        if isTomcast:
            response = requests.get("https://2b18347a.ngrok.io/NMSService/GetConfig", params=parameters, auth=HTTPBasicAuth("tomcastadmin","tomcast@123"))#, verify="cert1.pem"
            return response.json()


    def check_connectivity(self, ip, isTomcast):
        parameters = {"IP":ip}
        if isTomcast:
            response = requests.get("https://2b18347a.ngrok.io/NMSService/CheckConnectivity", params=parameters, auth=HTTPBasicAuth("tomcastadmin","tomcast@123"))#, verify="cert1.pem"
            return response.json()


    def start(self):
        response = requests.get("https://2b18347a.ngrok.io/NMSService/GetAllHosts", auth=HTTPBasicAuth("tomcastadmin","tomcast@123"))#, verify="cert1.pem"
        print(response.json())

if __name__ == "__main__":
    # start()
    # check_connectivity("198.51.100.20", True)
    # check_connectivity("198.51.100.10", True)
    # check_connectivity("198.51.100.1", True)
    # check_connectivity("100", True)
    # get_config("198.51.100.10", True)
    # get_config("198.51.100.20", True)
    # get_config("198.51.100.1", True)
    # get_config("100", True)
    # get_config("192.168.1.2", True)
    # get_interfaces("198.51.100.10", True)
    # get_interfaces("198.51.100.20", True)
    # get_interfaces("198.51.100.1", True)
    # get_interfaces("100", True)
    # get_interfaces("192.168.1.2", True)
    NMSService().configure_device("198.51.100.10", "interface FastEthernet 0/1\n ip address 192.168.1.10 255.255.255.0\n no shut\nend", True)