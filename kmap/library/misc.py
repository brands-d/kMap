"""Provides various useful methods for any part of kMap.py.

This file defines a multitude of methods not part of any specific part
of kMap.py. Those methods are intended for use throughout kMap.py to
reduce the amount of copy-paste code.
"""

import json
from urllib import request

import numpy as np


def round_to(x, base):
    """Rounds 'x' to the nearest multiple of 'base'.

    Args:
        x (float): Number to be rounded.
        base (float): Base to be rounded to.

    Returns:
        (float): Rounded number.

    """

    return base * round(x / base)


def idx_closest_value(axis, value, decimals=5, bounds_error=True):
    """Returns the index of the value in 'axis' closest to the 'value'.

    Args:
        axis (list): Axis of which the closest value is to be found.
            Needs to be a regular grid without NaN values.
        value (float): Value the closes axis point is to be found.
        decimals (int): Decimals places float values get rounded to
            to avoid machine error.
    Returns:
        (int): Index of the axis element closes to 'value'.

    """

    # Shift the axis to start at 0 -> rounding to step size (=base)
    shift = axis[0]
    base = axis[1] - axis[0]
    mapped_value = round_to(value - shift, base) + shift

    try:
        # Round to fifth decimal place because machine error
        idx = list(np.around(axis, decimals=decimals)).index(
            np.around(mapped_value, decimals=decimals)
        )

    except ValueError:
        # Value not found in list -> larger (smaller) than max (min)
        # + (-) step_size/2

        if bounds_error:
            return None

        else:
            if value > max(axis):
                idx = list(axis).index(max(axis))

            else:
                idx = list(axis).index(min(axis))

    return idx


def centered_meshgrid(x_axis, x_shift, y_axis, y_shift):
    """Returns a meshgrid made of 'x_axis' and 'y_axis' shifted by
    (x_shift, y_shift).

    Args:
        x_axis (list): x-axis for the meshgrid. Needs to be a regular
            grid without NaN values.
        x_shift (float): Shift for the x-axis.
        y_axis (list): y-axis for the meshgrid. Needs to be a regular
            grid without NaN values.
        y_shift (float): Shift for the y-axis.

    Returns:
        (list, list.T): Shifted meshgrides for the x and y axes shifted.
    """

    X = np.copy(x_axis).reshape(1, len(x_axis)) - x_shift
    Y = np.copy(y_axis).reshape(len(y_axis), 1) - y_shift

    return X, Y


def distance_in_meshgrid(X, Y):
    """Returns the grid entered filled with the distance to its center.

    Args:
        X (list): x-axis for the meshgrid. Needs to be a regular
            grid without NaN values.
        Y (list.T): y-axis for the meshgrid. Needs to be a regular
            grid without NaN values.

    Returns:
        (np.array): 2D numpy array with same size as grid. Each element
            carries the distance of its position in the grid.
    """

    return np.sqrt(X**2 + Y**2)


def normalize(data):
    """Normalizes the data to the number of non NaN values in the data.

    Args:
        data (list): Arbitrary list of any shape with numbers to be
            normalized. Can contain NaN values.

    Returns:
        (np.array): Numpy array of the same size as input but each value
            normalized.
    """

    data = np.array(data)
    num_elements = len(data[~np.isnan(data)])

    if num_elements == 0:
        norm = np.nan

    else:
        norm = np.nansum(data) / num_elements

    return norm


def orientation_to_euler_angle(orientation):
    """Returns the Euler angles for the plane specified in 'orientation'.

    Args:
        orientation (string): Plane for which the Euler angles are to be
            return. Possible values: 'xy', 'yx', 'xz', 'zx'

    Returns:
        (list): List of length three containing the Euler angles in the
            following order: Phi, Theta, Psi
    """

    phi = 0 if orientation in ["xy", "xz", "zx"] else 90
    theta = 0 if orientation in ["xy", "yx"] else 90
    psi = 0 if orientation in ["xy", "yx", "yz", "xz"] else 90

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

    return np.linspace(range_[0], range_[1], num=num, endpoint=True, dtype=np.float64)


def range_from_axes(*args):
    """Returns a range list for both axis.

    Args:
        *args (list): Arbitrary many axis. Each axis has to be a 1D list
            with no NaN values.

    Returns:
        (list): List of ranges for each axis supplied.
        (list): List of step sizes for each axis supplied.
    """

    range_ = []
    step_size = []

    for axis in args:
        range_.append([axis[0], axis[-1]])
        step_size.append(abs(axis[1] - axis[0]))

    range_ = np.array(range_, dtype=np.float64)
    step_size = np.array(step_size, dtype=np.float64)

    return range_, step_size


def step_size_to_num(range_, step_size):
    """Returns the number of points an axis with a range_ and step_size.

    Args:
        range_ (list): Max and min value of the axis.
        step_size (float): Step size of the axis.

    Returns:
        (int): Number of points in the axis.
    """

    num = int((range_[1] - range_[0]) / step_size) + 1

    return num


def get_rotation_axes(phi, theta):
    """Returns the rotation axes when rotating with Euler angles.

    Args:
        phi (float): Phi (first rotation) angle in degrees.
        theta (float): Theta (second rotation) angle in degrees.

    Returns:
        (list): List of axes (3D list). First is always unchanged
        z-axis. Second is the new x'-axis and third new z''-axis.
    """

    cos_phi = np.cos(np.radians(phi))
    sin_phi = np.sin(np.radians(phi))
    cos_theta = np.cos(np.radians(theta))
    sin_theta = np.sin(np.radians(theta))

    # First axis is always the z-axis
    axis1 = [0, 0, 1]
    # x'-axis
    axis2 = [cos_phi, sin_phi, 0]
    # z''-axis
    axis3 = [sin_phi * sin_theta, -cos_phi * sin_theta, cos_theta]

    return [axis1, axis2, axis3]


def energy_to_k(E_kin):
    """Convert kinetic energy in [eV] to k in [Anstroem^-1].

    Args:
        E_kin (float): Kinetic energy in [eV].

    Returns:
        (float): Wave number in [Anstroem^-1].
    """

    # Electron mass
    m = 9.10938356e-31
    # Reduced Planck constant
    hbar = 1.0545718e-34
    # Electron charge
    e = 1.60217662e-19

    fac = 2 * 1e-20 * e * m / hbar**2

    return np.sqrt(fac * E_kin)


def compute_Euler_matrix(phi, theta, psi):
    """Compute rotation matrix according to Eq. (M3.10.3) of Lang-Pucker.

    Args:
        phi (float): Phi (first rotation) angle in degrees.
        theta (float): Theta (second rotation) angle in degrees.
        psi (float): Psi (third rotation) angle in degrees.

    Returns:
        (array): 3x3 Rotation matrix.
    """

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
    """Returns the reduced Chi^2 (sum of squares normalized by number of
        non NaN values minus the degrees of freedom 'n').

    Args:
        data (list): List of arbitrary shape. Contains the NOT
            squared data.
        n (int): Degrees of freedom.

    Returns:
        (float): Reduced Chi^2 value.
    """

    N = np.count_nonzero(~np.isnan(data))
    reduced_chi2 = np.nansum(np.array(data) ** 2) / (N - n)

    return reduced_chi2


def transpose_axis_order(constant_axis):
    if constant_axis == 0:
        axis_order = (0, 2, 1)

    elif constant_axis == 1:
        axis_order = (2, 1, 0)

    else:
        axis_order = (1, 0, 2)

    return axis_order


def split_view(data_1, data_2, type_, scale=1):
    data = data_1.copy()

    if type_ == "Top Bottom":
        half_idx = int(np.ceil(data.data.shape[0] / 2))
        data.data[:half_idx] = scale * data_2.data[:half_idx]

    elif type_ == "Bottom Top":
        half_idx = int(np.ceil(data.data.shape[0] / 2))
        data.data[half_idx:] = scale * data_2.data[half_idx:]

    elif type_ == "Right Left":
        half_idx = int(np.ceil(data.data.shape[1] / 2))
        data.data.T[:half_idx] = scale * data_2.data.T[:half_idx]

    elif type_ == "Left Right":
        half_idx = int(np.ceil(data.data.shape[1] / 2))
        data.data.T[half_idx:] = scale * data_2.data.T[half_idx:]

    return data


def get_remote_hdf5_orbital(server, port, ID, orbital_number):
    url = "http://" + server + ":" + str(port)
    filename = "%05i.hdf5" % ID

    req = request.Request(url + "/hdf5", headers={"Host": filename + ".hdfgroup.org"})
    with request.urlopen(req) as response:
        body = json.loads(response.read())

    group_uuid = body["groups"][orbital_number]

    psi = {}
    fields = ["x", "y", "z", "data", "name"]
    for field in fields:
        req = request.Request(
            url + "/groups/" + group_uuid + "/links/" + field,
            headers={"Host": filename + ".hdfgroup.org"},
        )
        with request.urlopen(req) as response:
            body = json.loads(response.read())

        for href in body["hrefs"]:
            if href["rel"] == "target":
                uuid = href["href"].split("/")[-1]

        req = request.Request(
            url + "/datasets/" + uuid + "/value",
            headers={"Host": filename + ".hdfgroup.org"},
        )

        with request.urlopen(req) as response:
            body = json.loads(response.read())

        if field == "name":
            psi[field] = body["value"]
        else:
            psi[field] = np.array(body["value"])

    psi["nx"] = len(psi["x"])
    psi["ny"] = len(psi["y"])
    psi["nz"] = len(psi["z"])
    psi["dx"] = psi["x"][1] - psi["x"][0]
    psi["dy"] = psi["y"][1] - psi["y"][0]
    psi["dz"] = psi["z"][1] - psi["z"][0]

    req = request.Request(url, headers={"Host": filename + ".hdfgroup.org"})
    with request.urlopen(req) as response:
        body = json.loads(response.read())

    uuid = body["root"]

    fields = ["num_atom", "chemical_numbers", "atomic_coordinates"]
    molecule = {}
    for field in fields:
        req = request.Request(
            url + "/groups/" + uuid + "/links/" + field,
            headers={"Host": filename + ".hdfgroup.org"},
        )
        with request.urlopen(req) as response:
            body = json.loads(response.read())

        for href in body["hrefs"]:
            if href["rel"] == "target":
                uuid_field = href["href"].split("/")[-1]

        req = request.Request(
            url + "/datasets/" + uuid_field + "/value",
            headers={"Host": filename + ".hdfgroup.org"},
        )

        with request.urlopen(req) as response:
            body = json.loads(response.read())

        molecule[field] = body["value"]

    return molecule, psi


def write_cube(psi, molecule, filename):
    """Write real space orbital data as cube file"""

    b2a = 0.529177105787531
    x0 = psi["x"][0] / b2a
    y0 = psi["y"][0] / b2a
    z0 = psi["z"][0] / b2a
    dx = psi["dx"] / b2a
    dy = psi["dy"] / b2a
    dz = psi["dz"] / b2a
    nx = psi["nx"]
    ny = psi["ny"]
    nz = psi["nz"]
    num_atom = molecule["num_atom"]

    # define output format for volume data as 6 columns
    form = ""
    ncolumns = 6
    count = 0
    for k in range(nz):
        form += " %10.6e "
        count += 1
        if count == ncolumns:
            form += "\n"
            count = 0
    form += "\n"

    with open(filename, "w") as file:
        print("Cube file generated by Orbital class of kMap.py", file=file)
        print(psi["name"], file=file)
        print("%5i %10.6f  %10.6f  %10.6f" % (num_atom, x0, y0, z0), file=file)
        print("%5i %10.6f  %10.6f  %10.6f" % (nx, dx, 0, 0), file=file)
        print("%5i %10.6f  %10.6f  %10.6f" % (ny, 0, dy, 0), file=file)
        print("%5i %10.6f  %10.6f  %10.6f" % (nz, 0, 0, dz), file=file)
        for i in range(num_atom):
            Z = molecule["chemical_numbers"][i]
            x = molecule["atomic_coordinates"][i][0] / b2a
            y = molecule["atomic_coordinates"][i][1] / b2a
            z = molecule["atomic_coordinates"][i][2] / b2a
            print("%5i %10.6f  %10.6f  %10.6f  %10.6f" % (Z, Z, x, y, z), file=file)

        # now write out the volume data
        for i in range(nx):
            for j in range(ny):
                file.write(form % tuple(psi["data"][i, j, :]))
