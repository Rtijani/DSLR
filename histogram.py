
#!/usr/bin/env python3

import csv
import sys

import matplotlib.pyplot as plt


HOUSES = [
    "Gryffindor",
    "Hufflepuff",
    "Ravenclaw",
    "Slytherin",
]


def load_dataset(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def get_courses(rows):
    excluded = {
        "Index",
        "Hogwarts House",
        "First Name",
        "Last Name",
        "Birthday",
        "Best Hand",
    }

    return [
        column
        for column in rows[0].keys()
        if column not in excluded
    ]


def get_house_scores(rows, course, house):
    scores = []

    for row in rows:
        if row["Hogwarts House"] != house:
            continue

        value = row[course]

        if value == "":
            continue

        try:
            scores.append(float(value))
        except ValueError:
            continue

    return scores


def plot_histograms(rows):
    courses = get_courses(rows)

    fig, axes = plt.subplots(4, 4, figsize=(18, 14))
    axes = axes.flatten()

    colors = ["red", "gold", "blue", "green"]

    for index, course in enumerate(courses):
        ax = axes[index]

        for house, color in zip(HOUSES, colors):
            scores = get_house_scores(rows, course, house)

            ax.hist(
                scores,
                bins=20,
                alpha=0.4,
                label=house,
                color=color,
                density=True,
            )

        ax.set_title(course, fontsize=10)
        ax.set_xlabel("Score")
        ax.set_ylabel("Density")
        ax.grid(alpha=0.2)

    for index in range(len(courses), len(axes)):
        axes[index].axis("off")

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="lower center",
        ncol=4,
    )

    fig.suptitle(
        "Hogwarts Course Score Distributions by House",
        fontsize=16,
    )

    plt.tight_layout(rect=(0, 0.05, 1, 0.96))
    plt.savefig("histogram.png", dpi=150)
    plt.show()


def main():
    if len(sys.argv) != 2:
        print("Usage: python histogram.py <dataset.csv>")
        sys.exit(1)

    try:
        rows = load_dataset(sys.argv[1])

        if not rows:
            print("Error: dataset is empty.")
            sys.exit(1)

        plot_histograms(rows)

    except (OSError, csv.Error) as error:
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
