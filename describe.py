#!/usr/bin/env python3

import csv
import sys


def is_number(value):
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


def read_dataset(filename):
    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    return rows


def get_numerical_features(rows):
    numerical_features = {}

    if not rows:
        return numerical_features

    for column in rows[0].keys():
        values = []

        for row in rows:
            value = row[column]

            if value != "" and is_number(value):
                values.append(float(value))

        if values:
            numerical_features[column] = values

    return numerical_features

from utils.statistics import (
    count,
    mean,
    minimum,
    maximum,
    standard_deviation,
    percentile,
)


def is_number(value):
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


def read_dataset(filename):
    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def get_numerical_features(rows):
    features = {}

    if not rows:
        return features

    for column in rows[0]:
        if column == "Index":
            continue

        values = []
        has_text = False

        for row in rows:
            value = row[column].strip()

            if value == "":
                continue

            if is_number(value):
                values.append(float(value))
            else:
                has_text = True
                break

        if values and not has_text:
            features[column] = values

    return features


def display_statistics(features):
    statistics = {
        "Count": count,
        "Mean": mean,
        "Std": standard_deviation,
        "Min": minimum,
        "25%": lambda values: percentile(values, 0.25),
        "50%": lambda values: percentile(values, 0.50),
        "75%": lambda values: percentile(values, 0.75),
        "Max": maximum,
    }

    column_width = 34
    label_width = 10

    print(" " * label_width, end="")

    for feature in features:
        print(f"{feature:>{column_width}}", end="")
    print()

    for name, function in statistics.items():
        print(f"{name:<{label_width}}", end="")

        for values in features.values():
            result = function(values)
            print(f"{result:>{column_width}.6f}", end="")

        print()


def main():
    if len(sys.argv) != 2:
        print("Usage: ./describe.py <dataset.csv>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        rows = read_dataset(filename)
        features = get_numerical_features(rows)

        if not features:
            print("No numerical features found.")
            sys.exit(1)

        display_statistics(features)

    except (OSError, csv.Error, UnicodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
