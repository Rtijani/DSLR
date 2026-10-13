
#!/usr/bin/env python3

import csv
import sys
import math
import matplotlib.pyplot as plt


EXCLUDED = {
    "Index",
    "Hogwarts House",
    "First Name",
    "Last Name",
    "Birthday",
    "Best Hand",
}

HOUSES = {
    "Gryffindor": "red",
    "Hufflepuff": "gold",
    "Ravenclaw": "blue",
    "Slytherin": "green",
}


def load_dataset(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def get_courses(rows):
    return [
        column for column in rows[0]
        if column not in EXCLUDED
    ]


def get_points(rows, course_x, course_y):
    points = []

    for row in rows:
        try:
            x = float(row[course_x])
            y = float(row[course_y])

            if math.isfinite(x) and math.isfinite(y):
                points.append((x, y, row["Hogwarts House"]))

        except (ValueError, TypeError):
            continue

    return points


def correlation(points):
    n = len(points)

    if n < 2:
        return 0.0

    mean_x = 0.0
    mean_y = 0.0

    for x, y, _ in points:
        mean_x += x
        mean_y += y

    mean_x /= n
    mean_y /= n

    numerator = 0.0
    denominator_x = 0.0
    denominator_y = 0.0

    for x, y, _ in points:
        dx = x - mean_x
        dy = y - mean_y

        numerator += dx * dy
        denominator_x += dx * dx
        denominator_y += dy * dy

    denominator = (denominator_x * denominator_y) ** 0.5

    if denominator == 0:
        return 0.0

    return numerator / denominator


def find_similar_features(rows, courses):
    best_pair = None
    best_correlation = 0.0

    for i in range(len(courses)):
        for j in range(i + 1, len(courses)):
            points = get_points(rows, courses[i], courses[j])
            value = correlation(points)

            if abs(value) > abs(best_correlation):
                best_correlation = value
                best_pair = (courses[i], courses[j])

    return best_pair, best_correlation


def plot_scatter(rows, course_x, course_y, value):
    points = get_points(rows, course_x, course_y)

    plt.figure(figsize=(10, 7))

    for house, color in HOUSES.items():
        x_values = []
        y_values = []

        for x, y, student_house in points:
            if student_house == house:
                x_values.append(x)
                y_values.append(y)

        plt.scatter(
            x_values,
            y_values,
            color=color,
            label=house,
            alpha=0.5,
            s=15,
        )

    plt.xlabel(course_x)
    plt.ylabel(course_y)
    plt.title(
        f"{course_x} vs {course_y}\n"
        f"Pearson correlation: {value:.4f}"
    )

    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("scatter_plot.png", dpi=150)
    plt.show()


def main():
    if len(sys.argv) != 2:
        print("Usage: python scatter_plot.py <dataset.csv>")
        sys.exit(1)

    try:
        rows = load_dataset(sys.argv[1])

        if not rows:
            print("Error: dataset is empty.")
            sys.exit(1)

        courses = get_courses(rows)
        pair, value = find_similar_features(rows, courses)

        if pair is None:
            print("No valid feature pair found.")
            sys.exit(1)

        print("Most strongly correlated features:")
        print(f"Feature 1: {pair[0]}")
        print(f"Feature 2: {pair[1]}")
        print(f"Correlation: {value:.6f}")

        plot_scatter(rows, pair[0], pair[1], value)

    except (OSError, csv.Error) as error:
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
