# DSLR

# DSLR — Data Science × Logistic Regression

## Description

DSLR is a machine learning project developed as part of the 42 curriculum.

The objective is to predict a Hogwarts student's house based on academic results using multiclass logistic regression implemented from scratch.

## Features

- Descriptive statistics calculated manually
- Histogram visualization
- Scatter plot and correlation analysis
- Pair plot visualization
- Data preprocessing and standardization
- One-vs-all logistic regression
- Gradient descent optimization
- Hogwarts house prediction

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Descriptive statistics

```bash
python describe.py datasets/dataset_train.csv
```

### Visualizations

```bash
python histogram.py datasets/dataset_train.csv
python scatter_plot.py datasets/dataset_train.csv
python pair_plot.py datasets/dataset_train.csv
```

### Train the model

```bash
python logreg_train.py datasets/dataset_train.csv
```

This generates `weights.json`, containing the model parameters and preprocessing information.

### Predict Hogwarts houses

```bash
python logreg_predict.py datasets/dataset_test.csv weights.json
```

This generates `houses.csv` containing the predicted Hogwarts house for each student.

### Validate the model

```bash
python validate.py 42
```

The validation script uses an 80/20 training-validation split.

## Algorithm

The model uses one-vs-all logistic regression to classify students into four Hogwarts houses:

- Gryffindor
- Hufflepuff
- Ravenclaw
- Slytherin

Each binary classifier uses the sigmoid function and is trained using gradient descent to minimize binary cross-entropy loss.

Missing numerical values are replaced with the training-set feature mean. Features are standardized before training and prediction.

## Results

- Training accuracy: 98.19%
- Validation accuracy, seed 10: 97.81%
- Validation accuracy, seed 21: 99.38%
- Validation accuracy, seed 42: 98.12%
- Average validation accuracy: 98.44%

Official evaluation accuracy has not yet been verified.

## Implementation

The statistical calculations and logistic regression training are implemented manually in Python.

Matplotlib is used for data visualization.

i read the dataset by cnverting ach ro into a dictreader check my logreg_train.py
told it to return list(csv.DictReader(file))

this project is mainly for being able to visualiz data. after thi project you should be able to visually present your data through, histogram, scatter graph amd 

i did not use numpy which could have made mean, median, mode and all of that easy but if you check the statistics. py under the utils i implemented each code to calculate
 Count
Mean
Standard deviation
Minimum
Maximum
Percentiles

standard deviation is the average distance from the mean. which is also the root of the variance

for the homogeneous score distribution I would say care of magical creatures and arithmancy oberlapped very well/significantly 

with the histogram look carefully how the  4 colors overlapped significantly you will see a perfect example is the CARE OF MAGICAL CREATURES
 there you can explain that they have their score almost evenly spread.

 SCATTER PLOT 
 this us ysed to show relationship between 2 numerical variables.for the purpose of this project i would say we did t so that it will return the best pair/best correlation if you check the result of astronomy and the defense agaainst the dark art u will see its the perfect example when astronomy increases the defense against dart art decreases. 

 these 2 shows perfect negative linear relationship and thts why we could get a straight line 

 they also have the strongest relation
#Pearson correlation coefficient manually
 there is also a place in the code where we did this and numerator = 0.0
    denominator_x = 0.0
    denominator_y = 0.0

    for x, y, _ in points:
        dx = x - mean_x
        dy = y - mean_y

        numerator += dx * dy
        denominator_x += dx * dx
        denominator_y += dy * dy

    denominator = (denominator_x * denominator_y) ** 0.5

    Pearson correlation coefficient manually

    do not forget correlation coefficience measures the strength and direction of a linear relationship
    so if r = -0.98 or r = 0.98   theyy ar both strong  the + and - sign are just simply showing what direction they are going 


    pair plot
    unlike scatter plot which lets u compare btw 2 numerical variables pair plot allows us to compare btw multiple numerical featurs against one another 

    logreg_train
    this was where we 