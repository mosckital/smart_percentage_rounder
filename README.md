# smart_percentage_rounder
A smart percentage rounder which guarantees that the sum of the rounded percentages is 100%.

In contrast, simply applying `round()` to the list of percentages may lead the sum of the rounded percentages to 99%, 101% or even less accurate result.

The implementation is based on the [Largest Remainder Method](https://en.wikipedia.org/wiki/Largest_remainder_method).


![Licence Badge](https://img.shields.io/github/license/mosckital/smart_percentage_rounder)
![Build Badge](https://img.shields.io/github/workflow/status/mosckital/smart_percentage_rounder/CI)

## Provided Functionalities

This project provides various methods to this smart rounding functionality for different situations:

- In `rounders/rounder.py`:
  - `percentage_rounder()` can be used to achieve the stated smart rounding
  - `original_rounder()` can convert a list of original data into the list of ratio percentages, then apply the smart roundings on the converted values
- In `rounders/csv_rounder.py`:
  - `csv_rounder()` can apply the percentage conversion and then the smart percentage rounding to all lines in the provided CSV file and save the results in a CSV file aside the input file. The function can correctly handle an input CSV file with title rows, title columns or empty trailing fields in a row, as it will detect these cases and only convert the data columns. By default, the data columns is expected to have the last column as the *total number* column, which will not involve in the conversion and rounding and keep unchanged in the final results. This default behavior can be disable by `-n`/`--no-total-col` flag.

## Usage

Because no third party library has been used, the user can:

- use the functions in `rounder.py` by simply downloading the script and run it as a standalone script via `python rounder.py [data_list]`.
- use the functions in `csv_rounder.py`by simply downloading the zipfile `csv_rounder.zip` under the `bundles` folder. The user can use this zipfile as a standalone script via `python csv_rounder.zip [csv_file_path]`.
