"""Unit Tests"""

from coffeehelper.util import calcs


def test_ratio_1_1():
    assert calcs.calculate_ratio(1, 1) == 1.0


def test_ratio_50_10():
    assert calcs.calculate_ratio(50, 10) == 5.0


def test_ratio_10_50():
    assert calcs.calculate_ratio(10, 50) == 0.2


def test_coffee_from_water_1_1():
    assert calcs.calculate_coffee_from_water(1, 1) == 1


def test_coffee_from_water_500_0_5():
    assert calcs.calculate_coffee_from_water(500, 0.5) == 250


def test_water_from_coffee_1_1():
    assert calcs.calculate_water_from_coffee(1, 1) == 1


def test_water_from_coffee_500_0_5():
    assert calcs.calculate_water_from_coffee(500, 0.5) == 1000
