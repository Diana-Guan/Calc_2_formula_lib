from __future__ import annotations

from typing import Union

import sympy as sp

from ._core import RuleResult, get_symbol, not_applicable, parse_expr


def apply_power_rule_derivative(expr: Union[str, sp.Expr], var: Union[str, sp.Symbol] = "x") -> RuleResult:
    """
    Power Rule (polynomial-only mode):
    Applies ONLY if the expression is a polynomial in x.
    """
    x = get_symbol(var)
    rule_name = "power_rule"
    f = parse_expr(expr, local_dict={str(x): x})
    f = sp.expand(f)

    if not f.is_polynomial(x):
        return not_applicable(f, rule_name, "Not applicable: expression is not a polynomial in x (power-rule mode).")

    out = sp.simplify(sp.diff(f, x))
    return RuleResult(
        input_expr=f,
        output_expr=out,
        applied=True,
        rule_name=rule_name,
        message="Applied power rule term-by-term (polynomial).",
        steps=("Recognize polynomial in x.", "Differentiate each term."),
    )


def apply_constant_multiple_derivative(expr: Union[str, sp.Expr], var: Union[str, sp.Symbol] = "x") -> RuleResult:
    """
    Constant Multiple Rule:
      d/dx[c f(x)] = c f'(x)
    Applies ONLY if expr has a non-1 constant factor outside all x-dependence.
    Example: 5*(x^2 + 1) or 5*x^2.
    """
    x = get_symbol(var)
    rule_name = "constant_multiple_rule"
    f = parse_expr(expr, local_dict={str(x): x})
    # Keep structure and factor terms so 5*(...) is still detectable.
    f_s = sp.factor_terms(f)
    c, rest = f_s.as_independent(x, as_Add=False)
    if c == 1:
        return not_applicable(f_s, rule_name, "Not applicable: no constant multiple factor found.")

    out = sp.simplify(c * sp.diff(rest, x))
    return RuleResult(
        input_expr=f_s,
        output_expr=out,
        applied=True,
        rule_name=rule_name,
        message="Applied constant multiple rule for derivatives.",
        steps=(f"Factor out constant c = {c}.", "Differentiate the remaining part."),
    )


def apply_product_rule(expr: Union[str, sp.Expr], var: Union[str, sp.Symbol] = "x") -> RuleResult:
    """
    Product Rule:
      d/dx[f(x)g(x)] = f g' + f' g
    Applies ONLY if expression is a product with exactly TWO non-constant factors (simple version).
    """
    x = get_symbol(var)
    rule_name = "product_rule"
    e = parse_expr(expr, local_dict={str(x): x})
    e = sp.simplify(e)

    if not isinstance(e, sp.Mul):
        return not_applicable(e, rule_name, "Not applicable: expression is not a product.")

    c, rest = e.as_independent(x, as_Add=False)
    factors = list(rest.args) if isinstance(rest, sp.Mul) else [rest]
    nonconst = [f for f in factors if f.has(x)]
    if len(nonconst) != 2:
        return not_applicable(
            e,
            rule_name,
            "Not applicable: product rule requires exactly two x-dependent factors (simple mode).",
        )

    f1, f2 = nonconst
    out = sp.simplify(c * (f1 * sp.diff(f2, x) + sp.diff(f1, x) * f2))
    return RuleResult(
        input_expr=e,
        output_expr=out,
        applied=True,
        rule_name=rule_name,
        message="Applied product rule.",
        steps=("Identify f(x) and g(x).", "Compute f g' + f' g."),
    )


def apply_chain_rule(expr: Union[str, sp.Expr], var: Union[str, sp.Symbol] = "x") -> RuleResult:
    """
    Chain Rule (simple patterns):
    Applies ONLY for these common outer forms:
      (g(x))^n    with constant n != 1
      exp(g(x))
      ln(g(x))
      sin(g(x)), cos(g(x))
    If it doesn't match these patterns, returns not applicable.
    """
    x = get_symbol(var)
    rule_name = "chain_rule"
    e = parse_expr(expr, local_dict={str(x): x})
    e = sp.simplify(e)

    if isinstance(e, sp.Pow):
        g = e.base
        n = e.exp
        if g.has(x) and (not n.has(x)) and n != 1:
            out = sp.simplify(n * (g ** (n - 1)) * sp.diff(g, x))
            steps = ("Match pattern (g(x))^n.", "Derivative: n*(g(x))^(n-1)*g'(x).")
            return RuleResult(e, out, True, rule_name, "Applied chain rule for power of inner function.", steps)

    if e.func == sp.exp and e.args and e.args[0].has(x):
        g = e.args[0]
        out = sp.simplify(sp.exp(g) * sp.diff(g, x))
        steps = ("Match pattern exp(g(x)).", "Derivative: exp(g(x))*g'(x).")
        return RuleResult(e, out, True, rule_name, "Applied chain rule for exponential.", steps)

    if e.func == sp.log and len(e.args) == 1 and e.args[0].has(x):
        g = e.args[0]
        out = sp.simplify(sp.diff(g, x) / g)
        steps = ("Match pattern ln(g(x)).", "Derivative: g'(x)/g(x).")
        return RuleResult(e, out, True, rule_name, "Applied chain rule for natural log.", steps)

    if e.func == sp.sin and e.args[0].has(x):
        g = e.args[0]
        out = sp.simplify(sp.cos(g) * sp.diff(g, x))
        steps = ("Match pattern sin(g(x)).", "Derivative: cos(g(x))*g'(x).")
        return RuleResult(e, out, True, rule_name, "Applied chain rule for sine.", steps)

    if e.func == sp.cos and e.args[0].has(x):
        g = e.args[0]
        out = sp.simplify(-sp.sin(g) * sp.diff(g, x))
        steps = ("Match pattern cos(g(x)).", "Derivative: -sin(g(x))*g'(x).")
        return RuleResult(e, out, True, rule_name, "Applied chain rule for cosine.", steps)

    return not_applicable(
        e,
        rule_name,
        "Not applicable: expression does not match supported chain-rule patterns (simple mode).",
    )


def apply_exponential_derivative_rule(expr: Union[str, sp.Expr], var: Union[str, sp.Symbol] = "x") -> RuleResult:
    """
    Exponential Derivative Rule:
      d/dx(a^x) = a^x ln(a)
    Applies ONLY if expression is a^x with constant base a.
    """
    x = get_symbol(var)
    rule_name = "exponential_rule"
    # Do not simplify first; simplification can rewrite 2^(3*x) -> 8^x.
    e = parse_expr(expr, local_dict={str(x): x})

    if not isinstance(e, sp.Pow):
        return not_applicable(e, rule_name, "Not applicable: expression is not a^x.")

    a = e.base
    expo = e.exp
    if expo != x:
        return not_applicable(e, rule_name, "Not applicable: exponent is not x.")
    if a.has(x):
        return not_applicable(e, rule_name, "Not applicable: base a is not constant.")

    out = sp.simplify(e * sp.log(a))
    return RuleResult(
        input_expr=e,
        output_expr=out,
        applied=True,
        rule_name=rule_name,
        message="Applied exponential derivative rule.",
        steps=("Match pattern a^x with constant a.", "Derivative: a^x ln(a)."),
    )


__all__ = [
    "apply_power_rule_derivative",
    "apply_constant_multiple_derivative",
    "apply_chain_rule",
    "apply_product_rule",
    "apply_exponential_derivative_rule",
]
