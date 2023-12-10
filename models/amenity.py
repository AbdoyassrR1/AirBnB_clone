"""
amenity model
"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """
    amenity class
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.name = kwargs.get('name', "")
