"""Projectile-motion example used in the testing tutorial."""

from math import radians, sin


def landing_distance(speed, angle_degrees, gravity=9.81):
    """Return the horizontal landing distance for level-ground motion."""
    angle = radians(angle_degrees)
    return speed**2 * sin(2 * angle) / gravity
