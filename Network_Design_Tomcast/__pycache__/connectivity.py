import platform
import subprocess
import re

class Connectivity_Test:
    percent_loss = 0 

    def __get_packet_loss(self, ip_address):
        p1 = subprocess.Popen(["ping", ("-n" if str(platform.system).lower()=="windows" else "-c"), "4", ip_address], stdout=subprocess.PIPE)
        p2 = subprocess.Popen([("findstr" if str(platform.system).lower()=="windows" else "grep"), "loss"], stdin=p1.stdout, stdout=subprocess.PIPE)
        
        if str(platform.system).lower() == "windows":
            percent_loss_output = str(p2.communicate()[0]).split(',')[2]
            self.percent_loss = int(re.findall(r'\d\d?\d?',percent_loss_output)[1])
        else:
            percent_loss_output = str(p2.communicate()[0]).split(',')
            for output in percent_loss_output:
                if re.findall(r'loss',output) == ['loss']:
                    self.percent_loss = int(re.findall(r'\d\d?\d?',output)[0])
                    break
        

    @classmethod
    def Check_connectivity(self, ip_address):
        self.__get_packet_loss(self, ip_address)
        if self.percent_loss > 25:
            return False
        else:
            return True        