
#!/usr/bin/env python3

import csv
import random
import sys

from utils.preprocessing import fit_preprocessing, transform
from utils.logistic_regression import train_one_vs_all, predict_house


HOUSES = [
    "Gryffindor",
    "Hufflepuff",
    "Ravenclaw",
    "Slytherin",
]


def main():
    with open("datasets/dataset_train.csv", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    # Shuffle reproducibly before splitting
    

    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 42
    random.Random(seed).shuffle(rows)

    split = int(len(rows) * 0.8)

    training_rows = rows[:split]
    validation_rows = rows[split:]

    # Fit preprocessing on training rows only
    parameters = fit_preprocessing(training_rows)

    X_train = transform(training_rows, parameters)
    X_val = transform(validation_rows, parameters)

    y_train = [row["Hogwarts House"] for row in training_rows]
    y_val = [row["Hogwarts House"] for row in validation_rows]

    print(f"Training students: {len(X_train)}")
    print(f"Validation students: {len(X_val)}")

    models = train_one_vs_all(
        X_train,
        y_train,
        HOUSES,
        learning_rate=0.1,
        iterations=3000,
    )

    correct = 0

    for features, actual in zip(X_val, y_val):
        predicted = predict_house(features, models)

        if predicted == actual:
            correct += 1

    accuracy = correct / len(y_val) * 100

    print(f"\nCorrect predictions: {correct}/{len(y_val)}")
    print(f"Validation accuracy: {accuracy:.2f}%")


if __name__ == "__main__":
    main()
