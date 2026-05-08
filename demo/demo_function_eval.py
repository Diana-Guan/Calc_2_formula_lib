import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Calc2_formula_lib import evaluate_derivative_at, evaluate_function
from Calc2_formula_lib.calculator import differentiate_with_rules


def main():
    expr = "(x^2 + 1)*(x + 3)"
    x_value = 2

    fx = evaluate_function(expr, x_value)
    derivative = differentiate_with_rules(expr)
    dfx = evaluate_derivative_at(expr, x_value)

    print(f"f(x)      = {expr}")
    print(f"f({x_value})   = {fx}")
    print(f"f'(x)     = {derivative.output_expr}")
    print(f"f'({x_value})  = {dfx}")


if __name__ == "__main__":
    main()
