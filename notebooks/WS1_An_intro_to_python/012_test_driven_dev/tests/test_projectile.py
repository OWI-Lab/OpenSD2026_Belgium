"""Projectile tests using parametrized OpenStax reference values.

``pytest.mark.parametrize`` runs the same test once for every tuple in
``REFERENCE_CASES`` and reports each tuple as a separate test case.
"""
import pytest

from Awesome_openSD.projectile import landing_distance

REFERENCE_CASES = [
    (30, 45, 91.8),
    (40, 45, 163),
    (50, 45, 255),
    (50, 15, 128),
    (50, 75, 128),
]


def test_vertical_launch_has_zero_range():
    assert landing_distance(10, 90) == pytest.approx(0, abs=1e-12)


@pytest.mark.parametrize(
    ("speed", "angle_degrees", "expected_range"),
    REFERENCE_CASES,
)
def test_openstax_reference(speed, angle_degrees, expected_range):
    result = landing_distance(speed, angle_degrees)
    assert result == pytest.approx(expected_range, rel=0.01)
