import re
import numpy as np


def round_to(x, base):

    return base * round(x / base)


def idx_closest_value(axis, value):

    shift = axis[0]
    base = axis[1] - axis[0]
    mapped_value = round_to(value - shift, base) + shift

    try:
        # Round to fifth decimal place because machine error
        idx = list(np.around(axis, decimals=5)).index(
            np.around(mapped_value, decimals=5))

    except ValueError:
        idx = None

    return idx


def centered_meshgrid(x_axis, x_shift, y_axis, y_shift):

    X = np.copy(x_axis).reshape(len(x_axis), 1) - x_shift
    Y = np.copy(y_axis).reshape(1, len(y_axis)) - y_shift

    return X, Y


def distance_in_meshgrid(X, Y):

    return np.sqrt(X**2 + Y**2)


def get_ID_from_tab_text(tab_text):

    return int(re.search(r'\([0-9]+\)', tab_text).group(0)[1:-1])


def normalize(data):

    data = np.array(data)
    num_elements = len(data[~np.isnan(data)])

    if num_elements == 0:
        norm = np.nan

    else:
        norm = np.nansum(data) / num_elements

    return norm
