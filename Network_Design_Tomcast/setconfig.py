import napalm
import datetime
import types
import json
import logging

class SetConfig:

    napalm_device = types.SimpleNamespace()

    def __init__(self, router, ip_address, username, password, network_driver):
        try:
            driver = napalm.get_network_driver(network_driver)
            self.napalm_device = driver(ip_address, username, password)
            self.napalm_device.open()
        except Exception as ex:
            print("SSH is not configured on router {}".format(router))
            print("Exception is: {}".format(str(ex)))

    
    def __set_running_config(self, config):
        try:
            if self.napalm_device is not types.SimpleNamespace():
                self.napalm_device.load_merge_candidate(config=config)
                self.napalm_device.commit_config()
            else:
                print("Problem with SSH connection")
        except Exception as ex:
            print("Exception while configuring: {}".format(str(ex)))


    def __close_napalm_connection(self):
        try:
            if self.napalm_device is not types.SimpleNamespace():
                self.napalm_device.close()
            else:
                print("Problem closing SSH connection")
        except Exception as ex:
            print("Exception while closing SSH connection: {}".format(str(ex)))


    def configure(self, config):
        self.__set_running_config(config)
        self.__close_napalm_connection()
