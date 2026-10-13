
#!/usr/bin/env python3

import csv
import json
import sys

from utils.preprocessing import (
    FEATURES,
    fit_preprocessing,
    transform,
)

from utils.logistic_regression import (
    train_one_vs_all,
    predict_house,
)


HOUSES = [
    "Gryffindor",
    "Hufflepuff",
    "Ravenclaw",
    "Slytherin",
]


def load_dataset(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def calculate_accuracy(X, labels, models):
    correct = 0

    for features, actual_house in zip(X, labels):
        predicted_house = predict_house(features, models)

        if predicted_house == actual_house:
            correct += 1

    return correct / len(labels) * 100


def main():
    if len(sys.argv) != 2:
        print("Usage: python logreg_train.py <dataset_train.csv>")
        sys.exit(1)

    try:
        rows = load_dataset(sys.argv[1])

        if not rows:
            raise ValueError("Training dataset is empty.")

        labels = [row["Hogwarts House"] for row in rows]

        if any(label not in HOUSES for label in labels):
            raise ValueError("Invalid or missing Hogwarts house.")

        print("Preparing dataset...")

        parameters = fit_preprocessing(rows)
        X = transform(rows, parameters)

        print(f"Students: {len(X)}")
        print(f"Features: {len(FEATURES)}")

        models = train_one_vs_all(
            X,
            labels,
            HOUSES,
            learning_rate=0.1,
            iterations=3000,
        )

        accuracy = calculate_accuracy(X, labels, models)

        print(f"\nTraining accuracy: {accuracy:.2f}%")

        data = {
            "features": FEATURES,
            "preprocessing": parameters,
            "models": models,
        }

        with open("weights.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print("Model saved to weights.json")

    except (OSError, ValueError, KeyError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()