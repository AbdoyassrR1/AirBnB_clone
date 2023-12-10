#!/usr/bin/python3
'''User class module'''
from models.base_model import BaseModel


class User(BaseModel):
    '''
    User class

    Attributes:
        email: string - empty string
        password: string - empty string
        first_name: string - empty string
        last_name: string - empty string
    '''

    def __init__(self, *args, **kwargs) -> None:
        '''constructor'''
        super().__init__(*args, **kwargs)

        self.email = kwargs.get('email', "")
        self.password = kwargs.get('password', "")
        self.first_name = kwargs.get('first_name', "")
        self.last_name = kwargs.get('last_name', "")
