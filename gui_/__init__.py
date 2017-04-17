from pint import UnitRegistry

unit_reg = UnitRegistry()
Q_ = unit_reg.Quantity


class NamedQuantity(Q_):

    def __new__(cls, *args, **kwargs):
        if kwargs.get("name", None):
            # print("Name is not none")
            NamedQuantity.name = kwargs["name"]
            del kwargs["name"]
        return Q_.__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(NamedQuantity, self).__init__(*args, **kwargs)

    def set_name(self, name):
        assert isinstance(name, str)
        self.name = name

    def __repr__(self):
        return "%s: %s %s" % (self.name, self.m, self.units)

    def __gt__(self, other):
        print("\nThere is to be a comparison")
        print(type(other))
        try:
            return self.magnitude > other
        except ValueError as e:
            return super(NamedQuantity, self).__gt__(other)

    # def __cmp__(self, other):
    #     if issubclass(other, Q_):
    #         return super(NamedQuantity, self).__cmp__(other)
    #
    #     else:
    #         if self.magnitude > other:
    #             return 1
    #         elif self.magnitude < other:
    #             return 1
    #         else:
    #             return 0
    #
    # # def __eq__(self, other):
    #     if isinstance(other, Q_):
    #         return super(NamedQuantity, self).__eq__(other)
    #     else:
    #         return self.magnitude == other
    #
    # def __ne__(self, other):
    #     if isinstance(other, Q_):
    #         return super(NamedQuantity, self).__ne__(other)
    #     else:
    #         return self.magnitude != other
    #
    # def __gt__(self, other):
    #     if isinstance(other, Q_) or isinstance(other, NamedQuantity):
    #         return super(NamedQuantity, self).__gt__(other)
    #     else:
    #         return self.magnitude > other
    #
    # def __lt__(self, other):
    #     if isinstance(other, Q_):
    #         return super(NamedQuantity, self).__lt__(other)
    #     else:
    #         return self.magnitude < other
    #
    # def __ge__(self, other):
    #     if isinstance(other, Q_):
    #         return super(NamedQuantity, self).__ge__(other)
    #     else:
    #         return self.magnitude >= other
    #
    # def __le__(self, other):
    #     if isinstance(other, Q_):
    #         return super(NamedQuantity, self).__eq__(other)
    #     else:
    #         return self.magnitude <= other


class NamedStr(str):

    def __new__ (cls, word, *args, **kwargs):
        name = kwargs.get('name', None)
        cls.name = name
        if name:
            del kwargs["name"]
        return str.__new__(cls, word, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(NamedStr, self).__init__(*args, **kwargs)

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
