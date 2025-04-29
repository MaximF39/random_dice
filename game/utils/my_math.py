def sum_ap(start, step, n):
    return sum(arithmetic_progression(start, step, n))


def arithmetic_progression(start, step, n):
    return [start + i * step for i in range(n)]
