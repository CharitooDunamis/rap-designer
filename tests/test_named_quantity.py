import pytest

from rpm.utils import (NamedStr, NamedInt, NamedFloat)


@pytest.fixture
def named_int(request):
    return NamedInt(55, name="Angle")


@pytest.fixture
def named_float(request):
    return NamedFloat(98.8, name="Average")


@pytest.fixture
def named_string(request):
    return NamedStr("Michael", name="Candidate 1")

# ------------ NAMED STRING TESTS ----------------------


def test_creation_of_named_string():
    candidate1 = NamedStr("Michael", name="Candidate 1")
    del candidate1


def test_named_string_returns_correct_name(named_string):
    assert named_string.name == "Candidate 1"


def test_repr_method_of_named_string_with_name_returns_correct_value(named_string):
    assert repr(named_string) == "NamedString: Michael"


def test_repr_method_of_nameless_named_string_returns_correct_value():
    variable = NamedStr('Me')
    assert repr(variable) == 'NamedString: Me'

# ------------ NAMED INT TESTS ----------------------


def test_creation_of_named_int():
    candidate1 = NamedStr("Michael", name="Candidate 1")
    del candidate1


def test_named_int_returns_correct_name(named_int):
    assert named_int.name == "Angle"


def test_repr_method_of_named_int_with_name_returns_correct_value(named_int):
    assert repr(named_int) == "NamedInteger: 55"


def test_named_int_has_correct_value(named_int):
    assert named_int * 1 == 55


def test_repr_method_of_nameless_named_int_returns_correct_value():
    variable = NamedInt(3)
    assert repr(variable) == 'NamedInteger: 3'

# ------------ NAMED FLOAT TESTS ----------------------


def test_creation_of_named_float():
    candidate1 = NamedFloat(50.003, name="Random Value")
    del candidate1


def test_named_float_returns_correct_name(named_float):
    assert named_float.name == "Average"


def test_repr_method_of_named_float_with_name_returns_correct_value(named_float):
    assert repr(named_float) == "NamedFloat: 98.8"


def test_named_float_has_correct_value(named_float):
    assert named_float * 1 == 98.8


def test_repr_method_of_nameless_named_float_returns_correct_value():
    variable = NamedFloat(3.3)
    assert repr(variable) == 'NamedFloat: 3.3'


def test_creation_of_two_named_floats_results_in_unique_objects():
    var1 = NamedFloat(20.0, name="First")
    var2 = NamedFloat(20.0, name="First")
    assert not (var1 is var2)


def test_creation_of_two_named_floats_as_attributes_of_same_object_results_in_unique_objects():
    class Dummy(object):
        pass
    a = Dummy()
    a.var1 = NamedFloat(20.0, name="First")
    a.var2 = NamedFloat(20.0, name="First")
    assert not (a.var1 is a.var2)
