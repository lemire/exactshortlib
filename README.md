## Exact Short Products


This is a small Python library to check that short multipliers
are exact.

Main functions:

* `find_range_for_exact_most_significant_digits(z, digits, base)` finds the range of values such that the most significant `digits` digits of `z*w` are exact even if `z` is a truncated value, for `w` in `[a,b)`. If no interval is found, then None is returned.


## Reference

- Lemire, Daniel (2024). [Exact Short Products From Truncated Multipliers](https://arxiv.org/abs/2303.14321). Computer Journal, 67 (4). https://doi.org/10.1093/comjnl/bxad077

## Example

Suppose that you want a truncated version of an integer version of pi so that you can compute the product with 6 digits of accuracy. Given a truncated multiplier such as `z=3141592653589`, we might ask for the range of values supporting  6-digit of accuracy. That is, we want to find a range of values for `w` such that `w*z` has its 6 most significant digits accurate, even though we know that the multiplier was truncated. It turns out that we support the range of values from 1 to 15591614.


```Python
base = 10
digits = 6
z = 3141592653589
mi, ma = find_range_for_exact_most_significant_digits(z, digits, base)
# 1 15591614
print(mi, ma)
```

We can test it out in practice:

```Python
def select_top_digits(value, digits, base):
    if digits <= 0:
        raise ValueError("number of digits should be a positive integer")
    while value < base ** (digits-1):
        value *= base
    while value >= base ** digits:
        value //=base
    return value

# 489824 489824
# 489824 489825
print(select_top_digits(z*(ma-1), digits, base), select_top_digits(z*(ma-1), digits, base))
print(select_top_digits(z*ma, digits, base), select_top_digits(z*ma, digits, base))
```

See examples subdirectory for other examples.
