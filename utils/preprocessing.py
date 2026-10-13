#!/usr/bin/env python3

import math

from utils.statistics import mean, standard_deviation


FEATURES = [
    "Arithmancy",
    "Astronomy",
    "Herbology",
    "Divination",
    "Muggle Studies",
    "Ancient Runes",
    "History of Magic",
    "Transfiguration",
    "Potions",
    "Charms",
    "Flying",
]


def parse_number(value):
    """Convert a CSV value to a finite float, or None."""
    try:
        number = float(value)
        if math.isfinite(number):
            return number
    except (ValueError, TypeError):
        pass

    return None


def fit_preprocessing(rows):
    """
    Calculate preprocessing parameters using training data only.
    """
    parameters = {}

    for feature in FEATURES:
        values = []

        for row in rows:
            value = parse_number(row.get(feature))

            if value is not None:
                values.append(value)

        if not values:
            raise ValueError(
                f"No valid values for feature: {feature}"
            )

        avg = mean(values)
        std = standard_deviation(values)

        if std == 0:
            std = 1.0

        parameters[feature] = {
            "mean": avg,
            "std": std,
        }

    return parameters


def transform(rows, parameters, features=None):
    if features is None:
        features = FEATURES

    matrix = []

    for row in rows:
        student = []

        for feature in features:
            avg = parameters[feature]["mean"]
            std = parameters[feature]["std"]

            value = parse_number(row.get(feature))

            if value is None:
                value = avg

            student.append((value - avg) / std)

        matrix.append(student)

    return matrix