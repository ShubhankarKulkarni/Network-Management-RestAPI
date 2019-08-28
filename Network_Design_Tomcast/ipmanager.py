import ipaddress


class IPFunctions:


    @classmethod
    def validate_IP_address(self, ip):
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
        except Exception as ex:
            print("Exception while validating the IP {}: {}".format(ip, str(ex)))
            return False


    @classmethod
    def get_subnet_mask_from_ip(self, ip):
        if self.validate_IP_address(str(ip).split("/")[0]):
            subnet_mask = ipaddress.ip_network(ip, strict=False).netmask.compressed
            return subnet_mask
        else:
            raise Exception("Invalid ip address {}".format(ip))

    
    @classmethod
    def get_wildcard_mask_from_ip(self, ip):
        if self.validate_IP_address(str(ip).split("/")[0]):
            wildcard_mask = ipaddress.ip_network(ip, strict=False).hostmask.compressed
            return wildcard_mask
        else:
            raise Exception("Invalid ip address {}".format(ip))

    
    @classmethod
    def get_network_from_ip_and_subnet(self, ip):
        if self.validate_IP_address(str(ip).split("/")[0]):
            network = str(ipaddress.ip_network(ip, strict=False).compressed).split("/")[0]
            return network
        else:
            raise Exception("Invalid ip address {}".format(ip))
  