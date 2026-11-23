def is_sorted(xs):
    """Return whether xs is in non-decreasing order."""
    return all(xs[index] <= xs[index + 1] for index in range(len(xs) - 1))
