"""
amenity model
"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """
    amenity class
    """
    name = ""

    # def __init__(self, *args, **kwargs) -> None:
    #     '''constructor'''
    #     super().__init__(*args, **kwargs)

    #     self.name = kwargs.get('name', "")
