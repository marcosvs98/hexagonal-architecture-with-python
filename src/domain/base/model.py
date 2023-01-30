from pydantic import BaseModel, Extra
from typing import Any, List

class Model(BaseModel, extra=Extra.allow):
    """ Base class for model objects """


class ModelMeta(Model):
    """ Base class responsible for building objects
    dynamically from the structure contained in
    a python dictionary. """

    __exceptions: List[Any] = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Model = ModelMeta