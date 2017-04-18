from __future__ import division
# import math

METER_INCH = 39.37008
METER_FEET = 3.28084
MPA_PSI = 145.037738007


def psi_to_mpa(psi):
    return psi / MPA_PSI


def mpa_to_psi(mpa):
    return mpa * MPA_PSI


def feet_to_meters(feet):
    return feet / METER_FEET


def meters_to_inches(meters):
    return meters * METER_INCH


def inches_to_meter(inches):
    return inches / METER_INCH


def meters_to_feet(meters):
    return meters * METER_FEET


class StrVariable(str):

    def __new__(cls, value="", name=None, *args, **kwargs):
        string = str.__new__(cls, value)
        string.name = name
        return string

    def __init__(self, value="", encoding='utf8', errors='strict', name=None):
        super(StrVariable, self).__init__(object=value, encoding=encoding, errors=errors)
        self.name = name


class Slave(object):
    """
    Represents an imperial unit where conversion can only be done by using a function
    e.g. converting between celsius and fahrenheit
    It is possible to use this for units where conversion is by a factor. Just put the
    factor in a lambda function e.g.
    _to = lambda x: x * factor
    _from = lambda x: x / factor
    """

    def __init__(self, _to, _from, symbol=None):
        """
        _to - a function that converts a value from the imperial unit to the metric equivalent
        _from - a function that converts a value from the metric unit to the equivalent imperial
        """
        self._to = _to
        self._from = _from
        self.symbol = symbol

    def __get__(self, instance, owner):
        return self._from(instance.master)

    def __set__(self, instance, value):
        instance.master = self._to(value)

    def __str__(self, instance):
        return "%f %s" % (self._from(instance.master) ,self.symbol)


class FactorSlave(object):
    """
    Represents an imperial unit which can be converted to its corresponding metric
    by multiplying by a factor. e.g converting between meter and feet
    """

    def __init__(self, factor, symbol=None):
        """
        factor - a factor to multiply by when converting from this imperial unit
        to the corresponding metric unit
        """
        self.factor = factor
        self.symbol = symbol

    def __get__(self, instance, owner):
        return instance.master * (1 / self.factor)

    def __set__(self, instance, value):
        instance.master = value * self.factor

    def __str__(self, instance):
        return "%f %s" % (instance.master * (1 / self.factor), self.symbol)


class Master(object):

    def __init__(self, value=0.0, symbol=None):
        """
        function - a function that converts from metric units to the equivalent
        imperial unit
        value - value of the quantity in imperial units
        """
        self.value = value
        self.symbol = None

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        self.value = value

    def __str__(self):
        return "{} {}".format(self.value, self.symbol)

    def __repr__(self):
        return self.__str__()


class Quantity(object):

    master = None
    slave = None

    def __init__(self, value=0.0, unit="master"):
        if unit == "master":
            self.master = value
        else:
            self.slave = value

    @property
    def value(self):
        return self.slave

    def __add__(self, other):
        if type(self) == type(other):
            return self.value + other.value
        else:
            return self.value + other

    def __sub__(self, other):
        if type(self) == type(other):
            return self.value - other.value
        else:
            return self.value - other

    def __mul__(self, other):
        if type(self) == type(other):
            return self.value - other.value
        else:
            return self.value - other

    def __truediv__(self, other):
        return self.value / other.value

    def __eq__(self, other):
        current_type = type(self)
        if isinstance(other, current_type):
            return self.value == other.value
        return self.value == other

    def __ne__(self, other):
        return self.value != other.value

    def __gt__(self, other):
        return self.value > other.value

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __str__(self):
        return "%s" % self.value


class Length(Quantity):

    slave = FactorSlave(factor=METER_FEET, symbol="ft")
    master = Master(symbol="m")

    def __init__(self, value=0.0, unit="master"):
        super(Length, self).__init__(value, unit)

    def __str__(self):
        return "Lenght: {}{}".format(self.value, self.master.symbol)


def create_named_object(obj, name):
    obj.name = name
    return obj


class NamedStr(str):
    def __new__(cls, word, *args, **kwargs):
        name = kwargs.get('name', None)
        cls.name = name
        if name:
            del kwargs["name"]
        return str.__new__(cls, word, *args, **kwargs)

    # def __init__(self, *args, **kwargs):
    #     super(NamedStr, self).__init__(*args, **kwargs)

    def set_name(self, name):
        self.name = name

    def __str__(self):
        norm_string = super(NamedStr, self).__str__()
        if self.name:
            return "{}: {}".format(self.name, norm_string)
        else:
            return norm_string

    def __repr__(self):
        if self.name:
            return self.__str__()
        else:
            return super(NamedStr, self).__repr__()


class NamedInt(int):
    def __new__(cls, number, **kwargs):
        name = kwargs.get('name', None)
        cls.name = name
        if name:
            del kwargs["name"]
        return int.__new__(cls, number)

    def set_name(self, name):
        self.name = name

    def __str__(self):
        norm_string = super(NamedInt, self).__str__()
        if self.name:
            return "{}: {}".format(self.name, norm_string)
        else:
            return norm_string

    def __repr__(self):
        if self.name:
            return self.__str__()
        else:
            return super(NamedInt, self).__repr__()


class NamedFloat(float):
    def __new__(cls, number, **kwargs):
        name = kwargs.get('name', None)
        cls.name = name
        if name:
            del kwargs["name"]
        return float.__new__(cls, number)

    def set_name(self, name):
        self.name = name

    def __str__(self):
        norm_string = super(NamedFloat, self).__str__()
        if self.name:
            return "{}: {}".format(self.name, norm_string)
        else:
            return norm_string

    def __repr__(self):
        if self.name:
            return self.__str__()
        else:
            return super(NamedFloat, self).__repr__()
