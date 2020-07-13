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
