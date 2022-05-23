from types import DynamicClassAttribute
from enum import Enum


class MyEnum(Enum):

    def __str__(self):
        return self.value

    @DynamicClassAttribute
    def path(self):
        """Class path"""
        return "%s.%s" % (self.__class__.__name__, self.name)










