import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Calc2_formula_lib.derivative_rule import (
    apply_power_rule_derivative,
    apply_constant_multiple_derivative,
    apply_product_rule,
    apply_chain_rule,
    apply_exponential_derivative_rule,
)

def show(title, result):
    print("=" * 70)
    print(title)
    print(f"Applied?  {result.applied}")
    print(f"Message:  {result.message}")
    print(f"Input:    {result.input_expr}")
    print(f"Output:   {result.output_expr}")
    if result.steps:
        print("Steps:")
        for s in result.steps:
            print(f"  - {s}")
    print()

def main():
    # 1) Power rule derivative (polynomial-only)
    show(
        "Power rule derivative — applicable (polynomial)",
        apply_power_rule_derivative("x^3 + x^2 + 8"),
    )
    show(
        "Power rule derivative — NOT applicable (not a polynomial)",
        apply_power_rule_derivative("sin(x) + x^2"),
    )

    # 2) Constant multiple rule derivative
    show(
        "Constant multiple derivative — applicable",
        apply_constant_multiple_derivative("5*(x^3 + x^2 + 8)"),
    )
    show(
        "Constant multiple derivative — NOT applicable (no outside constant factor)",
        apply_constant_multiple_derivative("x^3 + x^2 + 8"),
    )

    # 3) Product rule
    show(
        "Product rule — applicable (exactly two x-dependent factors)",
        apply_product_rule("(x^2 + 1)*(x + 3)"),
    )
    show(
        "Product rule — NOT applicable (not a product)",
        apply_product_rule("x^2 + 1"),
    )
    show(
        "Product rule — NOT applicable (more than two x-dependent factors in simple mode)",
        apply_product_rule("(x+1)*(x+2)*(x+3)"),
    )

    # 4) Chain rule (simple supported patterns)
    show(
        "Chain rule — applicable: (g(x))^n",
        apply_chain_rule("(3*x + 1)^5"),
    )
    show(
        "Chain rule — applicable: ln(g(x))",
        apply_chain_rule("ln(x^2 + 1)"),
    )
    show(
        "Chain rule — applicable: sin(g(x))",
        apply_chain_rule("sin(2*x)"),
    )
    show(
        "Chain rule — NOT applicable (pattern not supported in simple mode)",
        apply_chain_rule("(x^2 + 1)^(x)"),
    )

    # 5) Exponential derivative rule a^x
    show(
        "Exponential derivative rule — applicable",
        apply_exponential_derivative_rule("2^x"),
    )
    show(
        "Exponential derivative rule — NOT applicable (base is not constant: x^x)",
        apply_exponential_derivative_rule("x^x"),
    )
    show(
        "Exponential derivative rule — NOT applicable (exponent is not x)",
        apply_exponential_derivative_rule("2^(3*x)"),
    )

if __name__ == "__main__":
    main()
