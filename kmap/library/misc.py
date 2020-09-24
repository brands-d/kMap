import re
import numpy as np
from math import isclose


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


def range_from_axes(x_axis, y_axis):

    range_ = np.array([[x_axis[0], x_axis[-1]],
                       [y_axis[0], y_axis[-1]]],
                      dtype=np.float64)

    step_size = np.array([abs(x_axis[1] - x_axis[0]),
                          abs(y_axis[1] - y_axis[0])],
                         dtype=np.float64)

    return range_, step_size


def resolution_to_num(range_, resolution):

    num = int((range_[1] - range_[0]) / resolution)

    return num


def num_to_resolution(range_, num):

    resolution = (range_[1] - range_[0]) / num

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


def profile_line_phi(plot_data, phi, x_center, y_center):

    if isclose(abs(phi), np.pi / 2):
        # Catch vertical lines
        # For vertical lines the endpoint is (x_center, min(y)/max(y))
        x_end_idx = idx_closest_value(plot_data.x_axis, x_center)
        y_end_idx = 0 if phi > 0 else len(plot_data.y_axis) - 1

    elif isclose(phi, 0) or isclose(phi, -np.pi):
        # Catch horizontal lines
        x_end_idx = len(plot_data.x_axis) - 1 if phi > -np.pi / 2 else 0
        y_end_idx = idx_closest_value(plot_data.y_axis, y_center)

    else:
        # Line we are looking for is radius of unit circle at
        # angle phi
        x_unit = np.cos(phi) + x_center
        # y axis in image data is reversed, thus reverse circle
        y_unit = -(np.sin(phi) + y_center)
        slope = (y_unit - y_center) / (x_unit - x_center)
        intercept = y_unit - slope * x_unit
        # Upper half: y endpoint == y_axis[0]
        # Lower half: y endpoint == y_axis[-1]
        if phi < 0 and phi > -np.pi:
            x_max_end = (plot_data.y_axis[-1] - intercept) / slope

        else:
            x_max_end = (plot_data.y_axis[0] - intercept) / slope

        # x_end can be at most the first or last element of axis
        # depending on left or right half
        if phi < np.pi / 2 and phi > -np.pi / 2:
            x_end = min(x_max_end, plot_data.x_axis[-1])

        else:
            x_end = max(x_max_end, plot_data.x_axis[0])

        y_end = x_end * slope + intercept
        x_end_idx = idx_closest_value(plot_data.x_axis, x_end)
        y_end_idx = idx_closest_value(plot_data.y_axis, y_end)

    x_start_idx = idx_closest_value(plot_data.x_axis, x_center)
    y_start_idx = idx_closest_value(plot_data.y_axis, y_center)

    start = [y_start_idx, x_start_idx]
    end = [y_end_idx, x_end_idx]

    return start, end


def energy_to_k(E_kin):
    """ Convert kinetic energy in eV to k in Anstroem^-1."""

    # Electron mass
    m = 9.10938356e-31
    # Reduced Planck constant
    hbar = 1.0545718e-34
    # Electron charge
    e = 1.60217662e-19

    fac = 2 * 1e-20 * e * m / hbar**2

    return np.sqrt(fac * E_kin)


def compute_Euler_matrix(phi, theta, psi):
    """Compute rotation matrix according to Eq. (M3.10.3) of
       Lang-Pucker"""

    # Compute sines and cosines of angles
    sin_phi = np.sin(np.radians(phi))
    cos_phi = np.cos(np.radians(phi))
    sin_theta = np.sin(np.radians(theta))
    cos_theta = np.cos(np.radians(theta))
    sin_psi = np.sin(np.radians(psi))
    cos_psi = np.cos(np.radians(psi))

    # Euler matrix r according to eq. (M3.10.3) of Lang-Pucker
    r = np.zeros((3, 3))
    r[0, 0] = cos_phi * cos_psi - sin_phi * cos_theta * sin_psi
    r[1, 0] = -cos_phi * sin_psi - sin_phi * cos_theta * cos_psi
    r[2, 0] = sin_phi * sin_theta

    r[0, 1] = sin_phi * cos_psi + cos_phi * cos_theta * sin_psi
    r[1, 1] = -sin_phi * sin_psi + cos_phi * cos_theta * cos_psi
    r[2, 1] = -cos_phi * sin_theta

    r[0, 2] = sin_theta * sin_psi
    r[1, 2] = sin_theta * cos_psi
    r[2, 2] = cos_theta

    return r


def get_reduced_chi2(data, n):

    N = np.count_nonzero(~np.isnan(data))
    reduced_chi2 = np.nansum(data**2) / (N - n)

    return reduced_chi2
