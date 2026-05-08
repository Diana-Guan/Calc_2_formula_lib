from __future__ import annotations

from typing import Literal, Union

import sympy as sp

from ._core import RuleResult, evaluate_function, get_symbol, parse_expr
from .derivative_rule import (
    apply_chain_rule,
    apply_constant_multiple_derivative,
    apply_exponential_derivative_rule,
    apply_power_rule_derivative,
    apply_product_rule,
)


RuleName = Literal[
    "auto",
    "power_rule",
    "constant_multiple_rule",
    "product_rule",
    "chain_rule",
    "exponential_rule",
]


def apply_derivative_rule(
    expr: Union[str, sp.Expr],
    var: Union[str, sp.Symbol] = "x",
    rule: RuleName = "auto",
) -> RuleResult:
    """
    Apply one specific derivative rule or auto-select the first applicable one.
    """
    rule_map = {
        "power_rule": apply_power_rule_derivative,
        "constant_multiple_rule": apply_constant_multiple_derivative,
        "product_rule": apply_product_rule,
        "chain_rule": apply_chain_rule,
        "exponential_rule": apply_exponential_derivative_rule,
    }

    if rule == "auto":
        ordered_rules = (
            "power_rule",
            "constant_multiple_rule",
            "product_rule",
            "chain_rule",
            "exponential_rule",
        )
        last_result = None
        for rule_name in ordered_rules:
            result = rule_map[rule_name](expr, var=var)
            if result.applied:
                return result
            last_result = result
        return last_result

    if rule not in rule_map:
        allowed = ", ".join(["auto", *rule_map.keys()])
        raise ValueError(f"Unknown rule {rule!r}. Allowed values: {allowed}.")

    return rule_map[rule](expr, var=var)


def differentiate_with_rules(expr: Union[str, sp.Expr], var: Union[str, sp.Symbol] = "x") -> RuleResult:
    """Try derivative rule handlers in order, then fall back to SymPy diff."""
    result = apply_derivative_rule(expr, var=var, rule="auto")
    if result.applied:
        return result

    x = get_symbol(var)
    f = parse_expr(expr, local_dict={str(x): x})
    out = sp.simplify(sp.diff(f, x))
    return RuleResult(
        input_expr=f,
        output_expr=out,
        applied=True,
        rule_name="symbolic_fallback",
        message="No simple rule matched; used symbolic differentiation fallback.",
        steps=("Apply generic symbolic derivative d/dx.",),
    )


def evaluate_derivative_at(
    expr: Union[str, sp.Expr],
    x_value: Union[int, float, sp.Expr],
    var: Union[str, sp.Symbol] = "x",
) -> sp.Expr:
    derivative = differentiate_with_rules(expr, var=var)
    return evaluate_function(derivative.output_expr, x_value, var=var)


__all__ = ["apply_derivative_rule", "differentiate_with_rules", "evaluate_derivative_at"]
