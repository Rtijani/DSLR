#!/usr/bin/env python3

import math


def sigmoid(z):
    """Convert a real number into a value between 0 and 1."""
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))

    exp_z = math.exp(z)
    return exp_z / (1.0 + exp_z)


def predict_probability(features, weights, bias):
    """Predict the probability of the positive class."""
    z = bias

    for feature, weight in zip(features, weights):
        z += feature * weight

    return sigmoid(z)


def binary_cross_entropy(X, y, weights, bias):
    """Calculate average binary classification loss."""
    total_loss = 0.0
    epsilon = 1e-15

    for features, target in zip(X, y):
        prediction = predict_probability(
            features, weights, bias
        )

        prediction = max(
            epsilon, min(1.0 - epsilon, prediction)
        )

        total_loss += -(
            target * math.log(prediction)
            + (1 - target) * math.log(1 - prediction)
        )

    return total_loss / len(X)


def train_binary_classifier(
    X,
    y,
    learning_rate=0.1,
    iterations=3000,
):
    """Train binary logistic regression using batch gradient descent."""
    if not X or len(X) != len(y):
        raise ValueError("Invalid training data.")

    n_samples = len(X)
    n_features = len(X[0])

    weights = [0.0] * n_features
    bias = 0.0

    for iteration in range(iterations):
        gradients = [0.0] * n_features
        bias_gradient = 0.0

        for features, target in zip(X, y):
            prediction = predict_probability(
                features, weights, bias
            )

            error = prediction - target

            for j in range(n_features):
                gradients[j] += error * features[j]

            bias_gradient += error

        for j in range(n_features):
            weights[j] -= (
                learning_rate * gradients[j] / n_samples
            )

        bias -= learning_rate * bias_gradient / n_samples

        if (iteration + 1) % 500 == 0:
            loss = binary_cross_entropy(
                X, y, weights, bias
            )
            print(
                f"Iteration {iteration + 1}: "
                f"Loss = {loss:.6f}"
            )

    return weights, bias


def train_one_vs_all(
    X,
    labels,
    houses,
    learning_rate=0.1,
    iterations=3000,
):
    """Train one binary classifier per Hogwarts house."""
    models = {}

    for house in houses:
        print(f"\nTraining classifier for {house}...")

        binary_labels = [
            1 if label == house else 0
            for label in labels
        ]

        weights, bias = train_binary_classifier(
            X,
            binary_labels,
            learning_rate,
            iterations,
        )

        models[house] = {
            "weights": weights,
            "bias": bias,
        }

    return models


def predict_house(features, models):
    """Return the house with the highest predicted probability."""
    best_house = None
    best_probability = -1.0

    for house, model in models.items():
        probability = predict_probability(
            features,
            model["weights"],
            model["bias"],
        )

        if probability > best_probability:
            best_probability = probability
            best_house = house

    return best_house
