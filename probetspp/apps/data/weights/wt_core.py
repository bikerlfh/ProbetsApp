from decimal import Decimal


def calculate_score_item(
    wt: Decimal,
    total: int,
    won: int,
    lost: int
) -> Decimal:
    if total == 0:
        return Decimal(0)
    w_per = 100 * (won / total)
    l_per = 100 * (lost / total)
    score = wt * Decimal(w_per - l_per)
    return Decimal(score)
