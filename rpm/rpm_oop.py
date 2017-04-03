# from .rpm_functions import *


class RoomAndPillar:
    pass


class Pillar:

    def __init__(self, length, height, breadth=None):
        """
        For square pillars leave breadth as None
        :param length: Length of the pillar
        :param height: Height of the pillar
        :param breadth: Breadth of the pillar
        """
        self.breadth = self.length = length
        self.height = height
        if breadth:
            self.breadth = breadth

    def is_square(self):
        return self.length == self.breadth

    def __call__(self, length, height, breadth=None):
        self.__init__(length, height, breadth)
