import json



class Packet:


    def __init__(self, data: str | bytes):
        self.__data = json.loads(data)


    def type(self):
        return self.__data['type']
