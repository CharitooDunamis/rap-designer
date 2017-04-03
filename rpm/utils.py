class Variable:

    def __init__(self, upper=0.0, lower=0.0, step=0.0):
        self._value = lower
        self._upper = upper
        self._lower = lower
        self._step = step

    @property
    def next(self):
        _next = self._value + self._step
        self.set_value(_next)
        return self.get_value()

    @property
    def previous(self):
        _prev = self._value - self._step
        self.set_value(_prev)
        return self.get_value()

    def is_valid_value(self, value):
        return self._lower <= value <= self._upper

    def get_value(self):
        return self._value

    def set_value(self, value):
        if self.is_valid_value(value):
            self._value = value
        else:
            raise ValueError("Value is not within range")

    def get_next_value(self):
        """Return the next value of the variable without incrementing current value"""
        _next = self._value + self._step
        if self.is_valid_value(_next):
            return _next
        else:
            raise ValueError("Value is not within range")

    def get_previous_value(self):
        """Return the previous value of the variable without changing current value"""
        _prev = self._value - self._step
        if self.is_valid_value(_prev):
            return _prev
        else:
            raise ValueError("Value is not within range")


if __name__ == '__main__':
    trial = Variable(10, 0, 1)
    for i in range(3):
        print(trial.previous)
