#!/usr/bin/python3
'''FileStorage class module'''
import json
from utils.clsPath import classLocations


class FileStorage:
    '''
    File Storage serializes instances to a JSON file and
    deserializes JSON file to instances

    Methods:
        all: returns the dictionary __objects
        new: sets in __objects the obj with key <obj class name>.id
        save: serializes __objects to the JSON file (path: __file_path)
        reload: deserializes the JSON file to __objects
        (only if the JSON file (__file_path) exists ;
        otherwise, do nothing. If the file does not exist,
        no exception should be raised)
        delete: delete key in __objects and updates the JSON file
    '''

    __file_path = "file.json"
    __objects = dict()

    def __init__(self) -> None:
        '''Class constructor'''
        pass

    @classmethod
    def all(cls):
        '''returns the dictionary __objects'''
        return cls.__objects

    @classmethod
    def new(cls, obj):
        '''sets in __objects the obj with key <obj class name>.id'''
        # if obj is None:
        #     raise AttributeError
        # if obj.__class__.__name__ not in classLocations.keys():
        #     raise ValueError
        key = obj.__class__.__name__ + "." + obj.id
        cls.__objects[key] = obj

    @classmethod
    def save(cls):
        '''serializes __objects to the JSON file (path: __file_path)'''
        obj_dict = {key: obj.to_dict() for key, obj in cls.__objects.items()}
        with open(cls.__file_path, 'w', encoding="utf-8") as f:
            json.dump(obj_dict, f)

    @classmethod
    def reload(cls):
        '''
        deserializes the JSON file to __objects
        (only if the JSON file (__file_path) exists ;
        otherwise, do nothing. If the file does not exist,
        no exception should be raised)
        '''
        try:
            with open(cls.__file_path, 'r', encoding="utf-8") as f:
                data = json.load(f)
                for key, value in data.items():
                    class_name, _ = key.split(".")
                    module = __import__(classLocations[class_name],
                                        fromlist=[class_name])
                    class_ = getattr(module, class_name)
                    instance = class_(**value)
                    cls.__objects[key] = instance
        except FileNotFoundError:
            return
        except json.decoder.JSONDecodeError:
            return

    @classmethod
    def delete(cls, key):
        '''delete key in __objects and updates the JSON file'''
        if key in cls.__objects.keys():
            del cls.__objects[key]
            cls.save()
