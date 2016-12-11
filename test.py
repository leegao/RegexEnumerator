from regex_enumerate import enumerate_coefficients, exact_coefficients, generating_function
from itertools import islice
from sympy import latex

print(list(islice(exact_coefficients("(0+1)*0+"), 10)))
print(latex(generating_function("(0+1)*0+")))