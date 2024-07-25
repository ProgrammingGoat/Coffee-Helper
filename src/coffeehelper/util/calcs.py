"""Helper functions for various calculations."""


def calculate_ratio(coffee: int, water: int) -> float:
    try:
        return coffee / water
    except ZeroDivisionError:
        return 0


def calculate_coffee_from_water(water: int, ratio: float) -> float:
    return water * ratio


def calculate_water_from_coffee(coffee: int, ratio: float) -> float:
    try:
        return coffee / ratio
    except ZeroDivisionError:
        return 0
