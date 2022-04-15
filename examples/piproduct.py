import os
import sys
import math

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from exactshort.exactshort import *


z=31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989

base = 10
desired_digits = 10

def select_top_digits(value, digits, base):
    if digits <= 0:
        raise ValueError("number of digits should be a positive integer")
    while value < base ** (digits-1):
        value *= base
    while value >= base ** digits:
        value //=base
    return value

def construct_top_digits_divisor(value, digits, base):
    if digits <= 0:
        raise ValueError("number of digits should be a positive integer")
    M = 1
    while value//M >= base ** digits:
        M *= base
    return M

for digits in range(1,desired_digits+50):
    shortz = select_top_digits(z, digits, base)
    try:
      mi, ma = find_range_for_exact_most_significant_digits(shortz, desired_digits, base)
      print(digits, mi, ma)
      assert select_top_digits(shortz*(ma-1), desired_digits, base) == select_top_digits(z*(ma-1), desired_digits, base)
      Mp = construct_top_digits_divisor(shortz*ma, desired_digits, base)
      tmpz = shortz *10**100 + (10**100-1)
      assert (shortz*ma)%Mp >= Mp - ma + 1
      assert select_top_digits(shortz*ma, desired_digits, base) != select_top_digits(tmpz*ma, desired_digits, base)
    except TypeError:
        pass


