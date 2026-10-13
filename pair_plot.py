
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
    with open(filename, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def get_courses(rows):
    return [column for column in rows[0] if column not in EXCLUDED]


def get_values(rows, course_x, course_y, house):
    x_values = []
    y_values = []

    for row in rows:
        if row["Hogwarts House"] != house:
            continue

        try:
            x = float(row[course_x])
            y = float(row[course_y])

            if math.isfinite(x) and math.isfinite(y):
                x_values.append(x)
                y_values.append(y)

        except (ValueError, TypeError):
            continue

    return x_values, y_values


def plot_matrix(rows):
    courses = get_courses(rows)
    n = len(courses)

    fig, axes = plt.subplots(
        n, n, figsize=(26, 26),
        squeeze=False
    )

    for i, course_y in enumerate(courses):
        for j, course_x in enumerate(courses):
            ax = axes[i][j]

            for house, color in HOUSES.items():
                x_values, y_values = get_values(
                    rows, course_x, course_y, house
                )

                if i == j:
                    ax.hist(
                        x_values,
                        bins=15,
                        alpha=0.35,
                        color=color,
                        density=True,
                    )
                else:
                    ax.scatter(
                        x_values,
                        y_values,
                        s=2,
                        alpha=0.3,
                        color=color,
                    )

            if i == n - 1:
                ax.set_xlabel(course_x, rotation=90, fontsize=7)

            if j == 0:
                ax.set_ylabel(course_y, fontsize=7)

            ax.tick_params(
                axis="both",
                labelsize=5,
                labelbottom=False,
                labelleft=False,
            )

    fig.suptitle(
        "Hogwarts Course Pair Plot",
        fontsize=22,
        y=0.995,
    )

    fig.legend(
        handles=[
            plt.Line2D(
                [0], [0],
                marker="o",
                color="w",
                markerfacecolor=color,
                markersize=8,
                label=house,
            )
            for house, color in HOUSES.items()
        ],
        loc="upper right",
    )

    plt.subplots_adjust(
        left=0.10,
        bottom=0.10,
        right=0.95,
        top=0.97,
        wspace=0.15,
        hspace=0.15,
    )

    plt.savefig("pair_plot.png", dpi=120)
    plt.show()


def main():
    if len(sys.argv) != 2:
        print("Usage: python pair_plot.py <dataset.csv>")
        sys.exit(1)

    try:
        rows = load_dataset(sys.argv[1])

        if not rows:
            print("Error: empty dataset.")
            sys.exit(1)

        plot_matrix(rows)

    except (OSError, csv.Error) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
