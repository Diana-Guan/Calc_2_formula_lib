import os
import sys
import unittest
import sympy as sp

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Calc2_formula_lib import (
    apply_chain_rule,
    apply_constant_multiple_derivative,
    apply_derivative_rule,
    apply_exponential_derivative_rule,
    apply_power_rule_derivative,
    apply_product_rule,
    differentiate_with_rules,
)


class DerivativeRuleTests(unittest.TestCase):
    def test_power_rule_applicable(self):
        result = apply_power_rule_derivative("x^3 + x^2 + 8")
        self.assertTrue(result.applied)
        self.assertEqual(result.rule_name, "power_rule")
        self.assertEqual(sp.simplify(result.output_expr - (3 * sp.Symbol("x") ** 2 + 2 * sp.Symbol("x"))), 0)

    def test_power_rule_not_applicable(self):
        result = apply_power_rule_derivative("sin(x) + x^2")
        self.assertFalse(result.applied)
        self.assertEqual(result.rule_name, "power_rule")

    def test_constant_multiple_rule_applicable(self):
        result = apply_constant_multiple_derivative("5*(x^2 + 1)")
        x = sp.Symbol("x")
        self.assertTrue(result.applied)
        self.assertEqual(result.rule_name, "constant_multiple_rule")
        self.assertEqual(sp.simplify(result.output_expr - 10 * x), 0)

    def test_product_rule_not_applicable_three_factors(self):
        result = apply_product_rule("(x+1)*(x+2)*(x+3)")
        self.assertFalse(result.applied)
        self.assertEqual(result.rule_name, "product_rule")

    def test_chain_rule_applicable(self):
        result = apply_chain_rule("sin(2*x)")
        x = sp.Symbol("x")
        self.assertTrue(result.applied)
        self.assertEqual(result.rule_name, "chain_rule")
        self.assertEqual(sp.simplify(result.output_expr - 2 * sp.cos(2 * x)), 0)

    def test_exponential_rule_not_applicable_for_scaled_exponent(self):
        result = apply_exponential_derivative_rule("2^(3*x)")
        self.assertFalse(result.applied)
        self.assertEqual(result.rule_name, "exponential_rule")

    def test_apply_derivative_rule_specific(self):
        result = apply_derivative_rule("(x+1)*(x+2)", rule="product_rule")
        self.assertTrue(result.applied)
        self.assertEqual(result.rule_name, "product_rule")

    def test_apply_derivative_rule_auto(self):
        result = apply_derivative_rule("(3*x + 1)^5")
        self.assertTrue(result.applied)
        self.assertIn(
            result.rule_name,
            {
                "power_rule",
                "constant_multiple_rule",
                "product_rule",
                "chain_rule",
                "exponential_rule",
            },
        )

    def test_apply_derivative_rule_unknown_rule_raises(self):
        with self.assertRaisesRegex(ValueError, "Unknown rule"):
            apply_derivative_rule("x^2", rule="bad_rule")  # type: ignore[arg-type]

    def test_differentiate_with_rules_fallback(self):
        result = differentiate_with_rules("x^x")
        self.assertTrue(result.applied)
        self.assertEqual(result.rule_name, "symbolic_fallback")

    def test_invalid_expression_message_is_user_friendly(self):
        with self.assertRaisesRegex(ValueError, "Invalid expression"):
            apply_power_rule_derivative("x**")


if __name__ == "__main__":
    unittest.main()
