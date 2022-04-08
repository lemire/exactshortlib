## Exact Short Products


This is a small Python library to check that short multipliers
are exact.

Main functions:

* `short_multiplier_for_exact_most_significant_digits(z, R, digits, base)`: find the a short multiplier version of `z`, such that we have `digits` accurate digits in base `base` when computing `w*z` for `w` in  `[0,R)` 

* `find_range_for_exact_most_significant_digits(z, digits, base)` finds the range of values (a,b) such that the most significant `digits` digits of `z*w` are exact even if `z` is a truncated value, for `w` in `[a,b)`.


## Example

Suppose that you want a truncated version of an integer version of pi so that you can compute the product with numbers in `[0,10**7)` with 6 digits of accuracy. You can do it with a 13-digit short multiplier: 3141592653589.


```Python
def select_top_digits(value, digits, base):
    if digits <= 0:
        raise ValueError("number of digits should be a positive integer")
    while value < base ** (digits-1):
        value *= base
    while value >= base ** digits:
        value //=base
    return value

z=31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989

base = 10
digits = 6
R = 10**7
short_z = short_multiplier_for_exact_most_significant_digits(z, R, digits, base)
# 3141592653589
print(short_z)

#314158 314158
print(select_top_digits(short_z*(R-1), digits, base), select_top_digits(z*(R-1), digits, base))
```

Once we have a truncated multiplier such as 3141592653589, we might ask for the range of values supporting 
6-digit of accuracy. That is, we want to find a range of values for `w` such that `w*z` has its
6 most significant digits accurate, even though we know that the multiplier was truncated. It turns out
that we support the range of values from 1 to 15591614.

```Python
mi, ma = find_range_for_exact_most_significant_digits(short_z, digits, base)
# 1 15591614
print(mi, ma)

# 489824 489824
# 489824 489825
print(select_top_digits(short_z*(ma-1), digits, base), select_top_digits(z*(ma-1), digits, base))
print(select_top_digits(short_z*ma, digits, base), select_top_digits(z*ma, digits, base))
```

See examples subdirectory for other examples.