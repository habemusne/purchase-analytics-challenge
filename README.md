# Purchase-Analytics

## Problem

Instacart has published a [dataset](https://www.instacart.com/datasets/grocery-shopping-2017) containing 3 million Instacart orders.

This program calculates, for each department, the number of times a product was requested, number of times a product was requested for the first time and a ratio of those two numbers.

## Approach

From the input csvs, this program firstly generates a hash map from product to department. Then it uses the hash map to quickly calculates the required metrics. The program uses Python, along with only built-in libraries like `csv`.

## Environment

python3.5+, Unix (not tested on Windows)

## Usage

`python3 purchase_analytics.py <path to order-product csv> <path to product csv> <path to report csv>`

## Testing

`cd insight_testsuite && ./run_tests.sh`

## Assumptions

- Assume header columns are in expected order, so as the other rows' columns. This means that if two int columns are switched at a specific row and they are both valid in each other's range, my program will not detect it.

- Assume header names are allowed to be flexible. i.e. "product_id" in products.csv can be "prod_id". This means that I will not check if they match the headers in the given test files.

- Assume python3 is used. If your "python" command points to python2 as default, please explicitly use "python3" command.

- Assume max column as 100 instead of 80 is fine as the code style.

- Assume all given csvs have header. This is usually specified by user input, not by sniffing the csvs.
