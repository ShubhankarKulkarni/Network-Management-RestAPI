import json
import os

class SSH_Info:

    json_string = ""

    def __init__(self, file_name):
        if os.path.isfile(file_name):
            with open(file_name, 'r') as json_file:
                self.json_string = json_file.read()
        else:
            raise Exception("{} File Does not exist".format(file_name))


    def Get_SSH_Information(self):
        json_object = json.loads(self.json_string)
        return json_object            