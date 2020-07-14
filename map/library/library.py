import numpy as np


def round_to(x, base):

    return base * round(x / base)


def idx_closest_value(axis, value):

    shift = axis[0]
    base = axis[1] - axis[0]
    mapped_value = round_to(value - shift, base) + shift

    try:
        idx = list(axis).index(mapped_value)

    except ValueError:
        idx = None

    return idx


def centered_meshgrid(x_axis, x_shift, y_axis, y_shift):

    X = np.copy(x_axis).reshape(len(x_axis), 1) - x_shift
    Y = np.copy(y_axis).reshape(1, len(y_axis)) - y_shift

    return X, Y


def distance_in_meshgrid(X, Y):

    return np.sqrt(X**2 + Y**2)
