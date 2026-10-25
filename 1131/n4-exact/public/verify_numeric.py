#!/usr/bin/env -S python3 -I -P
"""Optional high-precision numerical smoke checks; not a proof."""

import sys


class NumericFailure(RuntimeError):
    """A numerical smoke-check invariant failed."""


def fail(message):
    print(f"NUMERIC_SMOKE_NONPROOF=FAIL reason={message}", file=sys.stderr)
    raise SystemExit(1)


if sys.flags.optimize != 0:
    fail("optimized Python is forbidden")
if not sys.flags.isolated or not sys.flags.safe_path:
    fail("isolated safe-path Python is required; use python3 -I -P")


import os


if "PYTHONOPTIMIZE" in os.environ:
    fail("PYTHONOPTIMIZE must be unset")


import mpmath as mp


EXPECTED_PYTHON = (3, 12, 3)
EXPECTED_MPMATH = "1.3.0"
mp.mp.dps = 80


def require(condition, message):
    if not bool(condition):
        raise NumericFailure(message)


def lagrange_integral(nodes):
    def integrand(value):
        total = mp.mpf("0")
        for index, node in enumerate(nodes):
            basis = mp.mpf("1")
            for other_index, other in enumerate(nodes):
                if index != other_index:
                    basis *= (value - other) / (node - other)
            total += basis * basis
        return total

    cuts = sorted(set([mp.mpf("-1"), *nodes, mp.mpf("1")]))
    return mp.quad(integrand, cuts)


def gram_integral(nodes):
    def legendre(degree, value):
        if degree == 0:
            return mp.mpf("1")
        if degree == 1:
            return value
        if degree == 2:
            return (3 * value**2 - 1) / 2
        if degree == 3:
            return (5 * value**3 - 3 * value) / 2
        raise NumericFailure(f"unsupported degree {degree}")

    matrix = mp.matrix(
        [
            [mp.sqrt(mp.mpf(2 * degree + 1) / 2) * legendre(degree, node) for degree in range(4)]
            for node in nodes
        ]
    )
    inverse = (matrix.T * matrix) ** -1
    return sum(inverse[index, index] for index in range(4))


def main():
    require(sys.version_info[:3] == EXPECTED_PYTHON, f"Python version is {sys.version_info[:3]}, expected {EXPECTED_PYTHON}")
    require(mp.__version__ == EXPECTED_MPMATH, f"mpmath version is {mp.__version__}, expected {EXPECTED_MPMATH}")

    critical = lambda value: 21 * value**3 + 9 * value**2 + 3 * value - 1
    y0 = mp.findroot(critical, (mp.mpf("0.185"), mp.mpf("0.186")))
    a0 = mp.sqrt(y0)
    nodes = [-mp.mpf("1"), -a0, a0, mp.mpf("1")]
    direct = lagrange_integral(nodes)
    gram = gram_integral(nodes)
    algebraic = 4 * (35 * y0**3 - 28 * y0**2 + 23 * y0 + 2) / (105 * y0 * (1 - y0) ** 2)
    require(abs(direct - gram) < mp.mpf("1e-70"), "quadrature and Gram values disagree")
    require(abs(direct - algebraic) < mp.mpf("1e-70"), "quadrature and algebraic values disagree")

    fejer_nodes = [-mp.mpf("1"), -1 / mp.sqrt(5), 1 / mp.sqrt(5), mp.mpf("1")]
    fejer = lagrange_integral(fejer_nodes)
    require(abs(fejer - mp.mpf(12) / 7) < mp.mpf("1e-70"), "Fejer value disagrees")
    require(direct < fejer < 2, "expected strict comparison failed")

    sample = [mp.mpf("-0.9"), mp.mpf("-0.25"), mp.mpf("0.4"), mp.mpf("0.8")]
    sample_integral = lagrange_integral(sample)

    def s_value(value):
        total = mp.mpf("0")
        for index, node in enumerate(sample):
            basis = mp.mpf("1")
            for other_index, other in enumerate(sample):
                if index != other_index:
                    basis *= (value - other) / (node - other)
            total += basis * basis
        return total

    predicted = sample_integral - s_value(-1) - s_value(1)
    epsilon = mp.mpf("1e-20")
    upper = lagrange_integral([(1 + epsilon) * node for node in sample])
    lower = lagrange_integral([(1 - epsilon) * node for node in sample])
    finite_difference = (upper - lower) / (2 * epsilon)
    require(abs(finite_difference - predicted) < mp.mpf("1e-35"), "affine derivative smoke check failed")

    print("NUMERIC_SMOKE_NONPROOF=PASS")
    print("quadrature_vs_gram=PASS affine_derivative=PASS")
    print("y_0=" + mp.nstr(y0, 60))
    print("a_0=" + mp.nstr(a0, 60))
    print("minimum=" + mp.nstr(direct, 60))
    print("fejer=12/7")


if __name__ == "__main__":
    try:
        main()
    except (NumericFailure, ArithmeticError, ValueError) as error:
        fail(str(error))
