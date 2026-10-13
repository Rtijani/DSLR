PYTHON = python3

TRAIN = datasets/dataset_train.csv
TEST = datasets/dataset_test.csv

WEIGHTS = weights.json
PREDICTIONS = houses.csv

SCRIPTS = describe.py histogram.py scatter_plot.py pair_plot.py logreg_train.py logreg_predict.py validate.py

.PHONY: all help install describe histogram scatter pair graphs train predict validate test check clean fclean re

.DEFAULT_GOAL := help

help:
	@echo "======================================"
	@echo "        DSLR PROJECT COMMANDS         "
	@echo "======================================"
	@echo "make install    - Install dependencies"
	@echo "make describe   - Generate statistics"
	@echo "make histogram  - Generate histogram"
	@echo "make scatter    - Generate scatter plot"
	@echo "make pair       - Generate pair plot"
	@echo "make graphs     - Generate all graphs"
	@echo "make train      - Train logistic regression"
	@echo "make predict    - Predict Hogwarts houses"
	@echo "make validate   - Run validation"
	@echo "make test       - Run automated checks"
	@echo "make check      - Check Python syntax"
	@echo "make all        - Run full workflow"
	@echo "make clean      - Remove generated graphs"
	@echo "make fclean     - Remove all generated files"
	@echo "make re         - Clean and rebuild everything"

install:
	$(PYTHON) -m pip install -r requirements.txt

describe:
	$(PYTHON) describe.py $(TRAIN)

histogram:
	$(PYTHON) histogram.py $(TRAIN)

scatter:
	$(PYTHON) scatter_plot.py $(TRAIN)

pair:
	$(PYTHON) pair_plot.py $(TRAIN)

graphs: histogram scatter pair

train:
	$(PYTHON) logreg_train.py $(TRAIN)

predict:
	@test -f $(WEIGHTS) || (echo "Error: Run make train first"; exit 1)
	$(PYTHON) logreg_predict.py $(TEST) $(WEIGHTS)

validate:
	$(PYTHON) validate.py 42

check:
	$(PYTHON) -m compileall -q $(SCRIPTS) utils
	@echo "PASS: Python syntax check"

test: check
	$(PYTHON) -c 'from utils.statistics import mean, count, minimum, maximum, standard_deviation, percentile; values = [1, 2, 3, 4, 5]; assert count(values) == 5; assert mean(values) == 3; assert minimum(values) == 1; assert maximum(values) == 5; assert abs(standard_deviation(values) - 1.58113883) < 0.00001; assert percentile(values, 50) == 3; print("PASS: Statistics tests")'
	$(PYTHON) -c 'from utils.logistic_regression import sigmoid; assert abs(sigmoid(0) - 0.5) < 0.00001; assert sigmoid(-10) < sigmoid(0) < sigmoid(10); print("PASS: Sigmoid tests")'
	@echo "All basic tests passed!"

all: describe graphs train predict
	@echo "======================================"
	@echo " DSLR WORKFLOW COMPLETED SUCCESSFULLY "
	@echo "======================================"

clean:
	rm -f histogram.png scatter_plot.png pair_plot.png
	rm -f describe_output.txt

fclean: clean
	rm -f $(WEIGHTS) $(PREDICTIONS)

re: fclean all