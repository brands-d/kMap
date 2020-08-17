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


def orientation_to_euler_angle(orientation):

    phi = 0 if orientation in ['xy', 'xz', 'zx'] else 90
    theta = 0 if orientation in ['xy', 'yx'] else 90
    psi = 0 if orientation in ['xy', 'yx', 'yz', 'xz'] else 90

    return phi, theta, psi


def axis_from_range(range_, num):
    """Calculates a full 1D axis from range values and number of
    elements. Result can be used for interpolation method.

    Args:
        range_ (float): 1D list with min and max value (inclusive).
        num (int): Number of points.

    Returns:
        (float): 1D np.array containing the resulting axis.

    """

    return np.linspace(range_[0], range_[1], num=num, endpoint=True,
                       dtype=np.float64)


def resolution_to_num(range_, resolution):

    num = int((range_[1] - range_[0]) / resolution)

    return num


def num_to_resolution(range_, num):

    resolution = (range_[1] - range_[0]) / resolution

    return resolution


def get_rotation_axes(phi, theta):

    deg2rad = np.pi / 180
    cos_phi = np.cos(phi * deg2rad)
    sin_phi = np.sin(phi * deg2rad)
    cos_theta = np.cos(theta * deg2rad)
    sin_theta = np.sin(theta * deg2rad)

    axis1 = [0, 0, 1]  # first axis is always the z-axis
    axis2 = [cos_phi, sin_phi, 0]  # x' axis
    axis3 = [sin_phi * sin_theta, -cos_phi *
             sin_theta, cos_theta]  # z'' axis

    return [axis1, axis2, axis3]
