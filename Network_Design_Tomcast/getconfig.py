import napalm
import datetime
import types
import json
import logging

class GetConfig:

    napalm_device = types.SimpleNamespace()

    def __init__(self, router, ip_address, username, password, network_driver):
        try:
            driver = napalm.get_network_driver(network_driver)
            self.napalm_device = driver(ip_address, username, password)
            self.napalm_device.open()
        except Exception as ex:
            print("SSH is not configured on router {}".format(router))
            print("Exception is: {}".format(str(ex)))


    def __get_running_config(self):
        try:
            if self.napalm_device is not types.SimpleNamespace():
                config = self.napalm_device.get_config(retrieve="running")
                return json.dumps(config, indent=4)
            else:
                print("Problem with SSH connection")
        except Exception as ex:
            print("Exception while retriving the running configuration: {}".format(str(ex)))

    
    def __close_napalm_connection(self):
        try:
            if self.napalm_device is not types.SimpleNamespace():
                self.napalm_device.close()
            else:
                print("Problem closing SSH connection")
        except Exception as ex:
            print("Exception while closing SSH connection: {}".format(str(ex)))


    def save_config_to_file(self, router):
        file_name = router + "_" + str(datetime.datetime.now().isoformat()) + ".txt"
        with open(file_name, 'w') as config_file:            
            config_file.write(self.__get_running_config())
        config_file.close()
        self.__close_napalm_connection()
        return file_name


    def get_config_json(self, router):
        result = self.__get_running_config()
        self.__close_napalm_connection()
        return result


    def get_interface_information(self, router):
        try:
            if self.napalm_device is not types.SimpleNamespace():
                result = dict()
                interface_information = self.napalm_device.get_interfaces()
                interface_parameters = self.napalm_device.get_interfaces_ip()
                interface_stats =  self.napalm_device.get_interfaces_counters()
                for interface in interface_information.keys():
                    interface_info_list = list()
                    interface_info_list.append(interface_information.get(interface))
                    interface_info_list.append(interface_parameters.get(interface))
                    interface_info_list.append(interface_stats.get(interface))
                    result[interface] = interface_info_list 
                self.__close_napalm_connection()   
                return result
            else:
                print("Problem with SSH connection")
        except Exception as ex:
            print("Exception while retriving the running configuration: {}".format(str(ex)))


    