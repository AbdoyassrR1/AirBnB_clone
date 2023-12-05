#!/usr/bin/python3
'''Base class module'''
import datetime
from uuid import uuid4


class BaseModel:
    '''
    Base class for other classes.

    Attributes:
        id (int): A unique identifier for each instance.
        created_at (datetime): The timestamp
        when the instance was created.
        updated_at (datetime): The timestamp
        when the instance was last updated.

    Methods:
        save: updates the public instance attribute
        updated_at with the current datetime
        to_dict: returns a dictionary containing all
        keys/values of __dict__ of the instance
    '''

    def __init__(self, *args, **kwargs) -> None:
        '''Class constructor'''
        if kwargs:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                elif key == "created_at" or key == "updated_at":
                    setattr(self, key, datetime.datetime.fromisoformat(value))
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.datetime.now()
            self.updated_at = datetime.datetime.now()

    def __str__(self) -> str:
        '''String representation of class'''
        return "[{}] ({}) {}" \
            .format(self.__class__.__name__, self.id, self.__dict__)

    def save(self) -> None:
        '''Updates the public instance attribute
        updated_at with the current datetime'''
        self.updated_at = datetime.datetime.now()

    def to_dict(self):
        '''Returns a dictionary containing all
        keys/values of __dict__ of the instance'''
        output = self.__dict__.copy()
        output['__class__'] = self.__class__.__name__
        output['created_at'] = output['created_at'].isoformat()
        output['updated_at'] = output['updated_at'].isoformat()
        return output
