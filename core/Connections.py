from app.models.Client import Client


class Connections(object):

    def __init__(self):
        self.connections = []
        pass

    def add(self, client: Client):
        pass

    def remove(self):
        pass

    def find(self):
        pass

    def is_not_empty(self):
        return len(self.connections) > 0
