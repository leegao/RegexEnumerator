from regex_enumerate import enumerate_coefficients
from itertools import islice

print(list(islice(enumerate_coefficients("(00*1)*00*"), 10)))