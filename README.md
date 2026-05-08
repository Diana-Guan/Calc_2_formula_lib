# Calc 2 Formula Lib

## Purpose
This repository contains a formula library designed to support solution checking for Calc 2 work. Its purpose is not only to store formulas, but also to provide computational features that can be used to evaluate expressions, apply rules, and help verify whether a solution is correct. In this repository, the current implementation is tested only with derivative rules, but in the future it could be expanded with additional rules to become a fuller library.

## Project Structure
- `Calc2_formula_lib/`: core library code
- `demo/`: example scripts showing how the library can be used
- `tests/`: test files for the implemented rules
- `docs/Calc_Formula_Library.tex`: LaTeX source for the supporting formula document
- `docs/Calc_Formula_Library.pdf`: rendered version of the formula document

## How to Run
From the repository root, you can run the example scripts directly:

```bash
python demo/demo_function_eval.py
python demo/demo_derivative_rule.py

