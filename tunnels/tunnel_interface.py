import json
from threading import Thread
from kafka import KafkaConsumer
from pymongo import MongoClient


class NewInitCaller(type):
    def __call__(cls, *args, **kwargs):
        """Called when you call MyNewClass() """
        obj = type.__call__(cls, *args, **kwargs)
        Thread(target=obj.spawn, args=()).start()
        return obj


class Tunnel(metaclass=NewInitCaller):

    def __init__(self, _dest, _src):
        self.src = KafkaConsumer(_src, value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        self.collection = MongoClient("mongodb://127.0.0.1:27017")["tweets"][_dest]

    def __new__(cls, *args, **kwargs):
        if cls is Tunnel:
            raise TypeError("This class cannot be instantiated. It can only inherited from")
        return object.__new__(cls)

    def spawn(self):
        # TODO: Note that this error is never caught because it's in a new thread. How fix?
        raise Exception("This method must be overriden!")



