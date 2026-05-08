from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Union

import sympy as sp
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr as _parse_expr,
    standard_transformations,
)


@dataclass(frozen=True)
class RuleResult:
    input_expr: sp.Expr
    output_expr: sp.Expr
    applied: bool
    rule_name: str
    message: str
    steps: tuple[str, ...] = ()


def get_symbol(var: Union[str, sp.Symbol]) -> sp.Symbol:
    return var if isinstance(var, sp.Symbol) else sp.Symbol(str(var))


def parse_expr(expr: Union[str, sp.Expr], local_dict: Optional[dict] = None) -> sp.Expr:
    if isinstance(expr, sp.Expr):
        return expr

    transformations = standard_transformations + (
        implicit_multiplication_application,
        convert_xor,
    )
    try:
        return _parse_expr(expr, local_dict=local_dict or {}, transformations=transformations)
    except Exception as exc:
        raise ValueError(f"Invalid expression: {expr!r}. Please provide a valid math expression in x.") from exc


def not_applicable(input_expr: sp.Expr, rule_name: str, message: str) -> RuleResult:
    return RuleResult(
        input_expr=input_expr,
        output_expr=input_expr,
        applied=False,
        rule_name=rule_name,
        message=message,
        steps=(),
    )


def evaluate_function(
    expr: Union[str, sp.Expr],
    x_value: Union[int, float, sp.Expr],
    var: Union[str, sp.Symbol] = "x",
) -> sp.Expr:
    x = get_symbol(var)
    f = parse_expr(expr, local_dict={str(x): x})
    return sp.simplify(f.subs(x, x_value))
