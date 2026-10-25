#!/usr/bin/env -S python3 -I -P
"""Exact certificate for the four-node result on Erdos Problem 1131."""

import sys


class VerificationFailure(RuntimeError):
    """An exact certificate invariant failed."""


def fail(message):
    print(f"EXACT_CERTIFICATE=FAIL reason={message}", file=sys.stderr)
    raise SystemExit(1)


if sys.flags.optimize != 0:
    fail("optimized Python is forbidden")
if not sys.flags.isolated or not sys.flags.safe_path:
    fail("isolated safe-path Python is required; use python3 -I -P")


import os


if "PYTHONOPTIMIZE" in os.environ:
    fail("PYTHONOPTIMIZE must be unset")


import sympy as sp


EXPECTED_PYTHON = (3, 12, 3)
EXPECTED_SYMPY = "1.14.0"


def require(condition, message):
    if not bool(condition):
        raise VerificationFailure(message)


def check_environment():
    require(sys.version_info[:3] == EXPECTED_PYTHON, f"Python version is {sys.version_info[:3]}, expected {EXPECTED_PYTHON}")
    require(sp.__version__ == EXPECTED_SYMPY, f"SymPy version is {sp.__version__}, expected {EXPECTED_SYMPY}")


def lagrange_objective(nodes, variable):
    total = sp.S.Zero
    for index, node in enumerate(nodes):
        basis = sp.S.One
        for other_index, other in enumerate(nodes):
            if index != other_index:
                basis *= (variable - other) / (node - other)
        total += sp.integrate(sp.expand(basis**2), (variable, -1, 1))
    return sp.factor(total)


def verify_gram_identity(variable):
    nodes = [sp.Rational(-1), sp.Rational(-2, 5), sp.Rational(1, 3), sp.Rational(1)]
    legendre = [
        sp.S.One,
        variable,
        (3 * variable**2 - 1) / 2,
        (5 * variable**3 - 3 * variable) / 2,
    ]
    orthonormal = [
        sp.sqrt(sp.Rational(2 * degree + 1, 2)) * polynomial
        for degree, polynomial in enumerate(legendre)
    ]
    matrix = sp.Matrix(
        [[polynomial.subs(variable, node) for polynomial in orthonormal] for node in nodes]
    )
    gram_value = sp.factor(sp.trace((matrix.T * matrix).inv()))
    direct_value = lagrange_objective(nodes, variable)
    require(sp.factor(gram_value - direct_value) == 0, "Gram trace identity failed")


def verify_affine_derivative():
    u, scale, center = sp.symbols("u scale center")
    coefficients = sp.symbols("s0:7")
    polynomial = sum(coefficient * u**degree for degree, coefficient in enumerate(coefficients))
    primitive = sp.integrate(polynomial, u)
    lower = center + (-1 - center) / scale
    upper = center + (1 - center) / scale
    transformed = scale * (primitive.subs(u, upper) - primitive.subs(u, lower))
    derivative = sp.expand(sp.diff(transformed, scale).subs(scale, 1))
    integral = primitive.subs(u, 1) - primitive.subs(u, -1)
    expected = integral - (1 - center) * polynomial.subs(u, 1) - (1 + center) * polynomial.subs(u, -1)
    require(sp.expand(derivative - expected) == 0, "affine derivative identity failed")


def verify_certificate():
    x, a, h, z, t, y, lam = sp.symbols("x a h z t y lam")
    objective = lagrange_objective([-1, h - a, h + a, 1], x)
    centered = sp.factor(objective.subs(h, 0))
    centered_expected = 4 * (35 * a**6 - 28 * a**4 + 23 * a**2 + 2) / (
        105 * a**2 * (a - 1) ** 2 * (a + 1) ** 2
    )
    require(sp.factor(centered - centered_expected) == 0, "centered objective failed")

    claimed_p = (
        119 * a**10
        - 259 * a**8 * h**2
        - 131 * a**8
        + 161 * a**6 * h**4
        + 268 * a**6 * h**2
        - 138 * a**6
        - 21 * a**4 * h**6
        - 87 * a**4 * h**4
        - 354 * a**4 * h**2
        + 202 * a**4
        + 6 * a**2 * h**6
        + 43 * a**2 * h**4
        + 108 * a**2 * h**2
        - 61 * a**2
        - h**6
        + 11 * h**4
        - 19 * h**2
        + 9
    )
    claimed_d = (
        105
        * a**2
        * (a - 1) ** 2
        * (a + 1) ** 2
        * (a - h - 1) ** 2
        * (a - h + 1) ** 2
        * (a + h - 1) ** 2
        * (a + h + 1) ** 2
    )
    require(
        sp.factor(objective - centered - 8 * h**2 * claimed_p / claimed_d) == 0,
        "fixed-endpoint difference identity failed",
    )

    polynomial_z = sp.Poly(sp.expand(claimed_p.subs(h**2, z * (1 - a) ** 2)), z)
    power = [polynomial_z.nth(degree) for degree in range(4)]
    bernstein = [
        power[0],
        power[0] + power[1] / 3,
        power[0] + 2 * power[1] / 3 + power[2] / 3,
        sum(power),
    ]
    a0 = 119 * a**6 + 107 * a**4 - 43 * a**2 + 9
    a1 = 49 * a**6 + 63 * a**5 + 46 * a**4 - 18 * a**3 - 19 * a**2 + 3 * a + 4
    a2 = 49 * a**4 + 63 * a**3 - 73 * a**2 + 13 * a + 4
    expected_bernstein = [
        (1 - a**2) ** 2 * a0,
        sp.Rational(2, 3) * (1 - a) ** 2 * (a**2 + 6 * a + 1) * a1,
        sp.Rational(8, 3) * a * (1 - a**2) ** 2 * a2,
        64 * a**2 * (1 - a**2) ** 2 * (7 * a**2 - 7 * a + 2),
    ]
    for index, (actual, expected) in enumerate(zip(bernstein, expected_bernstein)):
        require(sp.factor(actual - expected) == 0, f"Bernstein coefficient b{index} failed")

    require(sp.discriminant(107 * y**2 - 43 * y + 9, y) == -2003, "A0 discriminant failed")
    completed_square = 7 * (a - sp.Rational(1, 2)) ** 2 + sp.Rational(1, 4)
    require(sp.expand(7 * a**2 - 7 * a + 2 - completed_square) == 0, "last Bernstein factor failed")

    expected_transforms = [
        [4, 35, 114, 155, 56, 16, 224, 320, 128],
        [4, 45, 130, 122, 4, 45, 214, 196, 56],
    ]
    for index, (factor, expected) in enumerate(zip((a1, a2), expected_transforms), start=1):
        transformed = sp.Poly(sp.cancel((1 + t) ** 8 * factor.subs(a, t / (1 + t))), t)
        coefficients = [transformed.nth(degree) for degree in range(9)]
        require(coefficients == expected, f"A{index} positive transform failed")
        require(all(coefficient > 0 for coefficient in coefficients), f"A{index} transform is not strict")

    derivative_expected = -16 * (21 * a**6 + 9 * a**4 + 3 * a**2 - 1) / (
        105 * a**3 * (a - 1) ** 3 * (a + 1) ** 3
    )
    require(sp.factor(sp.diff(centered, a) - derivative_expected) == 0, "centered derivative failed")
    require(sp.limit(centered, a, 0, dir="+") == sp.oo, "a -> 0 boundary failed")
    require(sp.limit(centered, a, 1, dir="-") == sp.oo, "a -> 1 boundary failed")

    critical = 21 * y**3 + 9 * y**2 + 3 * y - 1
    require(sp.discriminant(critical, y) == -20736, "critical discriminant failed")
    require(critical.subs(y, 0) < 0 < critical.subs(y, 1), "critical sign interval failed")
    require(
        critical.subs(y, sp.Rational(185, 1000)) < 0 < critical.subs(y, sp.Rational(186, 1000)),
        "critical rational isolation failed",
    )

    value_y = 4 * (35 * y**3 - 28 * y**2 + 23 * y + 2) / (105 * y * (1 - y) ** 2)
    equation_numerator = sp.together(lam - value_y).as_numer_denom()[0]
    resultant = sp.factor(sp.resultant(critical, equation_numerator, y))
    minimum_polynomial = 165375 * lam**3 - 519750 * lam**2 + 491040 * lam - 146912
    require(sp.expand(resultant - 7168 * minimum_polynomial) == 0, "resultant failed")
    require(
        sp.discriminant(minimum_polynomial, lam) == -19439210456064000000,
        "minimum-value discriminant failed",
    )
    require(
        minimum_polynomial.subs(lam, sp.Rational(1710, 1000)) < 0
        < minimum_polynomial.subs(lam, sp.Rational(1711, 1000)),
        "minimum-value rational isolation failed",
    )
    require(
        sp.factor(centered.subs(a, 1 / sp.sqrt(5)) - sp.Rational(12, 7)) == 0,
        "Fejer value failed",
    )


def main():
    check_environment()
    x = sp.symbols("x")
    verify_gram_identity(x)
    verify_affine_derivative()
    verify_certificate()
    print("EXACT_CERTIFICATE=PASS")
    print("gram_trace=PASS affine_derivative=PASS bernstein_strict=PASS resultant=PASS")
    print("critical_discriminant=-20736")
    print("minimum_discriminant=-19439210456064000000")


if __name__ == "__main__":
    try:
        main()
    except (VerificationFailure, ArithmeticError) as error:
        fail(str(error))
