import pytest

from gui_ import (NamedQuantity, NamedStr, NamedInt, NamedFloat)


@pytest.fixture
def named_int(request):
    return NamedInt(55, name="Angle")


@pytest.fixture
def named_float(request):
    return NamedFloat(98.8, name="Average")


@pytest.fixture
def named_string(request):
    return NamedStr("Michael", name="Candidate 1")


def test_initialization_of_named_quantity():
    me = NamedQuantity("3.4cm")


def test_setting_name_of_named_quantity():
    first = NamedQuantity("3.4", name="First")
    assert first.name == "First"


def test_representation_of_named_quantity():
    second = NamedQuantity("3cm", name="Second")
    assert repr(second) == "Second: 3 centimeter dimensionless"

# ------------ NAMED STRING TESTS ----------------------


def test_creation_of_named_string():
    candidate1 = NamedStr("Michael", name="Candidate 1")
    del candidate1


def test_named_str_returns_correct_name(named_string):
    assert named_string.name == "Candidate 1"


def test_str_method_of_named_string_with_name_returns_correct_value(named_string):
    assert str(named_string) == "Candidate 1: Michael"


def test_str_method_of_nameless_named_string_returns_correct_value():
    variable = NamedStr('Me')
    assert str(variable) == 'Me'

# ------------ NAMED INT TESTS ----------------------


def test_creation_of_named_int():
    candidate1 = NamedStr("Michael", name="Candidate 1")
    del candidate1


def test_named_int_returns_correct_name(named_int):
    assert named_int.name == "Angle"


def test_str_method_of_named_int_with_name_returns_correct_value(named_int):
    assert str(named_int) == "Angle: 55"


def test_named_int_has_correct_value(named_int):
    assert named_int * 1 == 55


def test_str_method_of_nameless_named_int_returns_correct_value():
    variable = NamedInt(3)
    assert str(variable) == '3'

# ------------ NAMED FLOAT TESTS ----------------------


def test_creation_of_named_float():
    candidate1 = NamedFloat(50.003, name="Random Value")
    del candidate1


def test_named_float_returns_correct_name(named_float):
    assert named_float.name == "Average"


def test_str_method_of_named_float_with_name_returns_correct_value(named_float):
    assert str(named_float) == "Average: 98.8"


def test_named_float_has_correct_value(named_float):
    assert named_float * 1 == 98.8


def test_str_method_of_nameless_named_float_returns_correct_value():
    variable = NamedFloat(3.3)
    assert str(variable) == '3.3'
