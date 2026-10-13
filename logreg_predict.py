
#!/usr/bin/env python3

import csv
import json
import sys

from utils.preprocessing import transform
from utils.logistic_regression import predict_house


def load_dataset(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def main():
    if len(sys.argv) != 3:
        print(
            "Usage: python logreg_predict.py "
            "<dataset_test.csv> <weights.json>"
        )
        sys.exit(1)

    dataset_path = sys.argv[1]
    weights_path = sys.argv[2]

    try:
        rows = load_dataset(dataset_path)

        if not rows:
            raise ValueError("Test dataset is empty.")

        with open(weights_path, "r", encoding="utf-8") as file:
            saved_data = json.load(file)

        parameters = saved_data["preprocessing"]
        models = saved_data["models"]
        features = saved_data["features"]

        X = transform(rows, parameters, features)

        predictions = []

        for features in X:
            house = predict_house(features, models)
            predictions.append(house)

        with open("houses.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Index", "Hogwarts House"])

            for row, house in zip(rows, predictions):
                writer.writerow([row["Index"], house])

        print(f"Predictions generated: {len(predictions)}")
        print("Results saved to houses.csv")

    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
