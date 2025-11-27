import re
from typing import Callable, Iterator
from decimal import Decimal


def generator_numbers(text: str) -> Iterator[Decimal]:
    """Extracts all numbers (integers or decimals) from text"""

    pattern = r" \d+(\.\d+)? "

    for match in re.finditer(pattern, text):
        yield Decimal(match.group().strip())


def sum_profit(
    text: str, number_extractor: Callable[[str], Iterator[Decimal]]
) -> Decimal:
    """Calculates the total sum of all numbers extracted from the text"""

    gen = number_extractor(text)
    return sum(gen, Decimal(0))
