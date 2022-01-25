from functools import reduce

def flat_map(f, xs): return reduce(lambda a, b: a + b, map(f, xs))
