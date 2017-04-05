from rpm.utils import *
import pytest


def test_get_variable_value_less_than_lower_limit_raises_error():
    data = Variable(10, 1, 1.0)
    with pytest.raises(ValueError):
        print(data.previous)


def test_get_variable_value_greater_than_upper_limit_raises_error():
    data = Variable(upper=10, lower=1, step=10)
    data.set_value(5)
    with pytest.raises(ValueError):
        _ = data.next


def test_initial_value_of_variable_is_lower_limit():
    data = Variable(10, 1, 2)
    assert data.get_value() == 1


def test_get_next_value_does_not_change_current_value():
    data = Variable(10, 1, 1)
    data.get_next_value()
    assert data.get_value() == 1


def test_get_previous_value_does_not_change_current_value():
    data = Variable(10, 1, 1)
    data.set_value(5)
    data.get_previous_value()
    assert data.get_value() == 5


if __name__ == '__main__':
    pytest.main()
