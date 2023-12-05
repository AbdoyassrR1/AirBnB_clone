#!/usr/bin/python3
'''FileStorage class module'''
import json


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
    '''

    def __init__(self) -> None:
        '''Class constructor'''
        self.__file_path = "file.json"
        self.__objects = dict()

    def all(self):
        '''returns the dictionary __objects'''
        return self.__objects

    def new(self, obj):
        '''sets in __objects the obj with key <obj class name>.id'''
        key = obj.__class__.__name__ + "." + obj.id
        self.__objects[key] = obj

    def save(self):
        '''serializes __objects to the JSON file (path: __file_path)'''
        obj_dict = {key: obj.to_dict() for key, obj in self.__objects.items()}
        with open(self.__file_path, 'w') as f:
            json.dump(obj_dict, f)

    def reload(self):
        '''
        deserializes the JSON file to __objects
        (only if the JSON file (__file_path) exists ;
        otherwise, do nothing. If the file does not exist,
        no exception should be raised)
        '''
        try:
            # [TODO] Update this variable for each child in
            classLocations = {
                "BaseModel": "models.base_model",
            }
            with open(self.__file_path, 'r') as f:
                data = json.load(f)
                for key, value in data.items():
                    class_name, _ = key.split(".")
                    module = __import__(classLocations[class_name],
                                        fromlist=[class_name])
                    class_ = getattr(module, class_name)
                    instance = class_(**value)
                    self.__objects[key] = instance
        except FileNotFoundError:
            return