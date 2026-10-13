#!/usr/bin/env python3

def count(values):
    total = 0

    for _ in values:
        total += 1

    return total


def mean(values):
    if not values:
        return 0.0

    total = 0.0

    for value in values:
        total += value

    return total / count(values)


def minimum(values):
    if not values:
        return None

    result = values[0]

    for value in values[1:]:
        if value < result:
            result = value

    return result


def maximum(values):
    if not values:
        return None

    result = values[0]

    for value in values[1:]:
        if value > result:
            result = value

    return result


def standard_deviation(values):
    n = count(values)

    if n <= 1:
        return 0.0

    avg = mean(values)
    total = 0.0

    for value in values:
        difference = value - avg
        total += difference * difference

    variance = total / (n - 1)

    return variance ** 0.5


def percentile(values, percentage):
    if not values:
        return None

    sorted_values = sorted(values)
    n = count(sorted_values)

    position = (n - 1) * percentage

    lower_index = int(position)
    upper_index = lower_index + 1

    if upper_index >= n:
        return sorted_values[lower_index]

    fraction = position - lower_index

    lower_value = sorted_values[lower_index]
    upper_value = sorted_values[upper_index]

    return lower_value + (upper_value - lower_value) * fraction