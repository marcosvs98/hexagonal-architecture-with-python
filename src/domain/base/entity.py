from typing import Optional
from pydantic import constr
from domain.base.model import Model


class Entity(Model):
    """ Base class for domain entitie objects """

    #id: Optional[constr(max_length=500)]

    def __str__(self):
        return f"{type(self).__name__}"

    def __repr__(self):
        return self.__str__()



class AggregateRoot(Entity):
    """ Base class for domain aggregate objects. Consits of 1+ entities"""
