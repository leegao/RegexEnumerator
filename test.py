from regex_enumerate import enumerate_coefficients, exact_coefficients
from itertools import islice

print(list(islice(exact_coefficients("(00*1)*00*"), 10)))