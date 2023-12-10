#!/usr/bin/python3
""" File storage model """
import json


class FileStorage():

    """
    FileStorage class
    Usage : implement the functionality of storing objects and retrieving them
    Cicle : <class 'BaseModel'> -> to_dict() -> <class 'dict'> -> JSON dump ->
    <class 'str'> ->FILE -> <class 'str'> -> JSON load -> <class 'dict'>
    -> <class 'BaseModel'
    """

    __file_path = "file.json"
    __objects = {}

    def __init__(self):
        """do nothing"""
        pass

    def all(self):
        """
        Returns all objects in BaseModel class representing format
        """
        return self.__objects

    def new(self, obj):
        """
        Add new created objects to __objects var to serialize them
        into json objects using save() later
        """
        self.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

    def save(self):
        """"
        Serialize BaseModel objects in __objects to json objects and
        save them in file.json file format
        """
        json_objs = {}
        for key, val in self.__objects.items():
            json_objs[key] = val.to_dict()
        with open(self.__file_path, "w", encoding='utf-8') as f:
            json.dump(json_objs, f, indent=4)

    def reload(self):
        """
        Deserializes the JSON objects in file.json to a python dictionary
        format then pass it as a kwargs to BaseModel constructor to convert it
        BaseModel class representing format
        """
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review
        try:
            with open(self.__file_path, "r", encoding='utf-8') as f:
                json_objs = json.load(f)
            models = {
                'User': User,
                'BaseModel': BaseModel,
                'State': State,
                'City': City,
                'Amenity': Amenity,
                'Place': Place,
                'Review': Review
            }
            for key, val in json_objs.items():
                constractor = val["__class__"]
                for model, cls in models.items():
                    if constractor == model:
                        self.__objects[key] = cls(**val)

        except FileNotFoundError:
            pass
        except Exception as e:
            pass

    # def delete(self, key):
    #     '''delete key in __objects and updates the JSON file'''
    #     if key in self.__objects.keys():
    #         del self.__objects[key]
    #         self.save()

# '''FileStorage class module'''
# import json
# from utils.clsPath import classLocations


# class FileStorage:
#     '''
#     File Storage serializes instances to a JSON file and
#     deserializes JSON file to instances

#     Methods:
#         all: returns the dictionary __objects
#         new: sets in __objects the obj with key <obj class name>.id
#         save: serializes __objects to the JSON file (path: __file_path)
#         reload: deserializes the JSON file to __objects
#         (only if the JSON file (__file_path) exists ;
#         otherwise, do nothing. If the file does not exist,
#         no exception should be raised)
#         delete: delete key in __objects and updates the JSON file
#     '''

#     __file_path = "file.json"
#     __objects = dict()

#     def __init__(self) -> None:
#         '''Class constructor'''
#         pass

#     @classmethod
#     def all(cls):
#         '''returns the dictionary __objects'''
#         return cls.__objects

#     @classmethod
#     def new(cls, obj):
#         '''sets in __objects the obj with key <obj class name>.id'''
#         # if obj is None:
#         #     raise AttributeError
#         # if obj.__class__.__name__ not in classLocations.keys():
#         #     raise ValueError
#         key = obj.__class__.__name__ + "." + obj.id
#         cls.__objects[key] = obj

#     @classmethod
#     def save(cls):
#         '''serializes __objects to the JSON file (path: __file_path)'''
#         obj_dict = {key: obj.to_dict() for key, obj in cls.__objects.items()}
#         with open(cls.__file_path, 'w', encoding="utf-8") as f:
#             json.dump(obj_dict, f)

#     @classmethod
#     def reload(cls):
#         '''
#         deserializes the JSON file to __objects
#         (only if the JSON file (__file_path) exists ;
#         otherwise, do nothing. If the file does not exist,
#         no exception should be raised)
#         '''
#         try:
#             with open(cls.__file_path, 'r', encoding="utf-8") as f:
#                 data = json.load(f)
#                 for key, value in data.items():
#                     class_name, _ = key.split(".")
#                     module = __import__(classLocations[class_name],
#                                         fromlist=[class_name])
#                     class_ = getattr(module, class_name)
#                     instance = class_(**value)
#                     cls.__objects[key] = instance
#         except FileNotFoundError:
#             return
#         except json.decoder.JSONDecodeError:
#             return

#     @classmethod
#     def delete(cls, key):
#         '''delete key in __objects and updates the JSON file'''
#         if key in cls.__objects.keys():
#             del cls.__objects[key]
#             cls.save()
