import regex_enumerate
from regex_enumerate import check_on_oeis
from regex_enumerate import enumerate_coefficients, exact_coefficients, generating_function, algebraic_form
from itertools import islice
from sympy import latex
from regex_enumerate.transfer import *

regexes = [
    ("(00*1)*", '1-separated strings that starts with 0 and ends with 1'),
    ("(%|1|11)(00*(1|11))*0* | 1", 'complete 1 or 11-separated strings'),
    ("(000)*(111)*(22)*(33)*(44)*", r'complex root to $\frac{1}{(1 - z^3)^2} * \frac{1}{(1 - z^2)^3}$'),
    ("1*(22)*(333)*(4444)*(55555)*",  'number of ways to make change give coins of denomination 1 2 3 4 and 5'),
    (' '.join("%s%s*" % (i, i) for i in range(1, 6)), '5 compositions of n'),
    ("(11*)*",  'all compositions of n'),
    (' '.join(['(%s)*'%('.' * k) for k in {1, 5, 10, 25}]), 'number of ways to make n cents with US coins.'),
    ("(00*1)*00*", 'list of 0-sequences'),
]
for regex, comment in regexes:
    print("* `%s`: %s\n" % (regex, comment))
    algebraic = list(map(lambda x: int(round(x)), islice(enumerate_coefficients(regex), 20)))
    formula = algebraic_form(regex)
    print("  Its generating function is\n  $$\n  %s\n  $$" % latex(generating_function(regex)))
    print("  For words of sizes up to 20 in this language, their counts are:\n\n      %s\n" % (', '.join(map(str, algebraic))))
    print("  Its closed form is\n  $$\n  %s\n  $$" % latex(formula))
    print("\n  A list of OEIS entries that contains this subsequence.\n")
    for oeis in check_on_oeis(regex, start=5):
        print("  1. %s: https://oeis.org/%s" % (oeis.name, oeis.id))
    print('')