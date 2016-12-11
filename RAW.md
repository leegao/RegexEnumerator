# Regex Enumerator

Enumerate Regular Expressions the Fun Way.

$$
[z^n] \frac{p(z)}{q(z)} = \Theta\left({n + k - 1 \choose k - 1}\rho^{-n}\right) ~~~ \text{where $\rho$ is the smallest root of $q(z)$, and $k$ its multiplicity.}
$$

<p align="center">
<img src="http://i.imgur.com/sRo5tQz.png?invert_in_darkmode"/>
</p>

<sub>*Or how I learned to stop worrying and start counting things with calculus*</sub>

-----

Have you ever wondered about how many different strings you can form that fits your favorite regex?

Yeah, chances are you probably haven't. But it's on your mind now.

Here's one of my favorite regular expressions:
$$
(0^+,)^*0^+
$$
It specifies the class of languages that are comma-separated list of strings of zeros. For example,
`000, 0, 00000` belongs to this language, but `0,,0` and `0,0,` does not.

Now, it might seem like a masochistic endeavor, but if you enumerate every possible word in this language, you'll
find that there are no empty strings, 1 single letter string, 1 two letter string, 2 three letter strings, 3 four letter
strings, and so on. This pattern actually looks like

    0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, ...

Why, that is the fibonacci sequence! How did it end up in such a mundane place?

Now, I could give you a combinatorial interpretation for this amazeballs result, but I still get shivers up my spine
whenever I think back to my undergrad Combinatorics course. Instead, I'll give a more general way to compute these
enumerations.

However, that's not the end of it. It turns out that this algorithm can also compute a closed-form formula
for this sequence.
$$
F_n = \left(- \frac{1}{2} + \frac{\sqrt{5}}{2}\right)^{- n - 1} \left(- \frac{\sqrt{5}}{10} + \frac{1}{2}\right) + \left(- \frac{\sqrt{5}}{2} - \frac{1}{2}\right)^{- n - 1} \left(\frac{\sqrt{5}}{10} + \frac{1}{2}\right)
$$
where $F_n$ is the number of comma-separated lists of size $n$.

Now, this might not look very pretty, but it's still pretty cool that there is a (computable) closed form expression that
counts every regular expression.

-----------------------------------

### Installation

This library is just meant to be a demonstration. For now, you can install it by adding the `regex_enumerate` directory
to your `PYTHONPATH`. Note that you will first need to install `numpy`, `scipy`, and `sympy` in order to support solving a few
linear equations and to translate numerically computed roots into algebraic forms, if they are available.

### Usage

#### Regular Expression Syntax

We are using vanilla regular expression, so the standard `*`, `+`, `?`, `|` variety. Note that for `+` and `?`, we've
encoded them using just `*` and `|` instead:

* $$e^+ \to e \cdot e^*$$
* $$e? \to (e \mid \%)$$

Here, `%` denotes the "empty" transition $\epsilon$ in formal languages. In effect, it acts as the
identity element of concatenation, so that $\epsilon \cdot e \to e$. For example, the regular expression of
comma delimited language $(e^+,)*e^+$ can be encoded as
```python
e = '0' # or any other regular expression
regex = '({e}{e}*,)*{e}{e}*'.format(e = e)
```

#### Library Functions

`regex_enumerate` offers a few library functions for you to use.

* `enumerate_coefficients`: Runs the magical algorithm to give you an algorithm that can compute
  the count of words of size `n` in time that is only proportional (linearly) to the number of terms in your
  regular expression.
  
  ```python
  from regex_enumerate import enumerate_coefficients
  from itertools import islice
  
  print(list(islice(enumerate_coefficients('(0+1)*0+'), 10)))
  # [0.0, 1.0, 0.99999999999999989, 1.9999999999999998, 2.9999999999999996, 4.9999999999999982, 7.9999999999999982, 12.999999999999998, 20.999999999999993, 33.999999999999986].
  ```

* `exact_coefficients`: Uses a dynamic program to compute the same coefficients. Useful for validation
  and pure computation, but does not reveal any algebraic structure within the problem.
  
  ```python
  from regex_enumerate import exact_coefficients
  from itertools import islice
  
  print(list(islice(exact_coefficients('(0+1)*0+'), 10)))
  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
  ```

* `algebraic_form`: Computes the algebraic closed form of a regular expression.

  ```python
  from regex_enumerate import algebraic_form, evaluate_expression
  from sympy import latex, pprint
  
  formula = algebraic_form('(0+1)0+')
  
  # Normal Form
  print(formula)
  # 2.0*DiracDelta(n) + 1.0*DiracDelta(n - 1) + binomial(n + 1, 1) - 3
  
  # Latex
  print(latex(formula))
  # 2.0 \delta\left(n\right) + 1.0 \delta\left(n - 1\right) + {\binom{n + 1}{1}} - 3
  
  # ASCII/Unicode pretty print
  print(pprint(formula))
  #                                             /n + 1\
  # 2.0*DiracDelta(n) + 1.0*DiracDelta(n - 1) + |     | - 3
  #                                             \  1  /
  
  print(evaluate_expression(formula, 10))
  # 8
  ```

The magic behind this will be discussed in the next section. The $\text{\LaTeX}$ code looks like 
$$
2.0 \delta\left(n\right) + 1.0 \delta\left(n - 1\right) + {\binom{n + 1}{1}} - 3
$$
Note that this differs from the above since we're enumerating $(0^+1)0^+$ instead of $(0^+1)^* 0^+$.

In addition, regular expressions correspond to the family of rational functions (quotient of two polynomials).
To see the generating function of a regular expression, try

```python
from regex_enumerate import generating_function
from sympy import latex

print(latex(generating_function("(0+1)*0+")))
```

which outputs
$$
\frac{1.0 z}{- 1.0 z^{2} - 1.0 z + 1.0}
$$

#### Caveat

There are many regular expressions that are ambiguous. For example, the regular expression
$$
0 \mid 0
$$
is inherently ambiguous. On encountering a `0`, it's not clear which side of the bar it belongs to. While
this poses no challenges to parsing (since we don't output a parse-tree), it does matter in enumeration.
In particular, the direct translation of this expression will claim that there are 2 strings of size 1
in this language.

There are ways to circumvent this, but I haven't gotten around to tackling this problem yet. Therefore, know that
for some regular expressions, this technique will fail unless you manually reduce it to an unambiguous form.
There is always a way to do this, though it might create an exponential number of additional states.

#### Additional Examples
* `(00*1)*`: 1-separated strings that starts with 0 and ends with 1

  Its generating function is
  $$
  \frac{1.0 z - 1.0}{1.0 z^{2} + 1.0 z - 1.0}
  $$
  For words of sizes up to 20 in this language, their counts are:

      1, 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584

  Its closed form is
  $$
  \left(- \frac{1}{2} + \frac{3 \sqrt{5}}{10}\right) \left(- \frac{1}{2} + \frac{\sqrt{5}}{2}\right)^{- n - 1} + \left(- \frac{\sqrt{5}}{2} - \frac{1}{2}\right)^{- n - 1} \left(- \frac{3 \sqrt{5}}{10} - \frac{1}{2}\right)
  $$

  A list of OEIS entries that contains this subsequence.

  1. Fibonacci numbers: https://oeis.org/A000045
  1. Pisot sequences E(3,5), P(3,5): https://oeis.org/A020701
  1. Fibonacci numbers whose decimal expansion does not contain any digit 0: https://oeis.org/A177194
  1. Expansion of (1-x)/(1-x-x^2): https://oeis.org/A212804
  1. Pisot sequence E(2,3): https://oeis.org/A020695
  1. Least k such that the maximum number of elements among the continued fractions for k/1, k/2, k/3, k/4 : https://oeis.org/A071679
  1. a(n) = Fibonacci(n) mod n^3: https://oeis.org/A132636
  1. Expansion of 1/(1 - x - x^2 + x^18 - x^20): https://oeis.org/A185357
  1. Numbers generated by a Fibonacci-like sequence in which zeros are suppressed: https://oeis.org/A243063
  1. Fibonacci numbers Fib(n) whose decimal expansion does not contain any digit 6: https://oeis.org/A177247

* `(%|1|11)(00*(1|11))*0* | 1`: complete 1 or 11-separated strings

  Its generating function is
  $$
  1.0 z + \frac{1.0 z^{2} + 1.0 z + 1.0}{- 1.0 z^{3} - 1.0 z^{2} - 1.0 z + 1.0}
  $$
  For words of sizes up to 20 in this language, their counts are:

      1, 3, 4, 7, 13, 24, 44, 81, 149, 274, 504, 927, 1705, 3136, 5768, 10609, 19513, 35890, 66012, 121415

  Its closed form is
  $$
  0.61842 \cdot 0.54369^{- n - 1} + \left(-0.77184 - 1.11514282226563 i\right)^{- n - 1} \left(0.19079 - 0.0187005698680878 i\right) + \left(-0.77184 + 1.11514282226563 i\right)^{- n - 1} \left(0.19079 + 0.0187005698680878 i\right) + 1.0 \delta\left(n - 1\right)
  $$

  A list of OEIS entries that contains this subsequence.

  1. Tribonacci numbers: https://oeis.org/A000073

* `(000)*(111)*(22)*(33)*(44)*`: complex root to $\frac{1}{(1 - z^3)^2} * \frac{1}{(1 - z^2)^3}$

  Its generating function is
  $$
  \frac{1.0}{- 1.0 z^{12} + 3.0 z^{10} + 2.0 z^{9} - 3.0 z^{8} - 6.0 z^{7} + 6.0 z^{5} + 3.0 z^{4} - 2.0 z^{3} - 3.0 z^{2} + 1.0}
  $$
  For words of sizes up to 20 in this language, their counts are:

      1, 0, 3, 2, 6, 6, 13, 12, 24, 24, 39, 42, 63, 66, 96, 102, 138, 150, 196, 210

  Its closed form is
  $$
  - 0.03125 \left(-1\right)^{- n - 3} {\binom{n + 2}{2}} + 0.14063 \left(-1\right)^{- n - 2} {\binom{n + 1}{1}} - 0.30469 \left(-1\right)^{- n - 1} + \left(- \frac{1}{2} - 0.5 \sqrt{3} i\right)^{- n - 2} \left(-0.018519 - 0.0107015457788347 i\right) {\binom{n + 1}{1}} + \left(- \frac{1}{2} - 0.5 \sqrt{3} i\right)^{- n - 1} \left(\frac{2}{27} - 0.0855333805084229 i\right) + \left(- \frac{1}{2} + 0.5 \sqrt{3} i\right)^{- n - 2} \left(-0.018519 + 0.0107015457788347 i\right) {\binom{n + 1}{1}} + \left(- \frac{1}{2} + 0.5 \sqrt{3} i\right)^{- n - 1} \left(\frac{2}{27} + 0.0855333805084229 i\right) + 0.13542 {\binom{n + 1}{1}} + 0.094907 {\binom{n + 2}{2}} + 0.048611 {\binom{n + 3}{3}} + 0.013889 {\binom{n + 4}{4}} + 0.15654
  $$

  A list of OEIS entries that contains this subsequence.


* `1*(22)*(333)*(4444)*(55555)*`: number of ways to make change give coins of denomination 1 2 3 4 and 5

  Its generating function is
  $$
  \frac{1.0}{- 1.0 z^{15} + 1.0 z^{14} + 1.0 z^{13} - 1.0 z^{10} - 1.0 z^{9} - 1.0 z^{8} + 1.0 z^{7} + 1.0 z^{6} + 1.0 z^{5} - 1.0 z^{2} - 1.0 z + 1.0}
  $$
  For words of sizes up to 20 in this language, their counts are:

      1, 1, 2, 3, 5, 7, 10, 13, 18, 23, 30, 37, 47, 57, 70, 84, 101, 119, 141, 164

  Its closed form is
  $$
  \frac{1}{64} \left(-1\right)^{- n - 2} {\binom{n + 1}{1}} - 0.10156 \left(-1\right)^{- n - 1} + \left(1.0 i\right)^{- n - 1} \left(-0.03125 + 0.03125 i\right) + \left(- 1.0 i\right)^{- n - 1} \left(-0.03125 - 0.03125 i\right) + \left(- \frac{1}{2} - 0.5 \sqrt{3} i\right)^{- n - 1} \left(-0.018519 - 0.0320749878883362 i\right) + \left(- \frac{1}{2} + 0.5 \sqrt{3} i\right)^{- n - 1} \left(-0.018519 + 0.0320749878883362 i\right) + \left(0.012361 - 0.0380422472953796 i\right) \left(- \frac{1}{4} + \frac{\sqrt{5}}{4} - 0.951056480407715 i\right)^{- n - 1} + \left(0.012361 + 0.0380422472953796 i\right) \left(- \frac{1}{4} + \frac{\sqrt{5}}{4} + 0.951056480407715 i\right)^{- n - 1} + \left(-0.032361 - 1.0 i \left(- \frac{\sqrt{537}}{38} + \frac{29}{38}\right)^{2}\right) \left(- \frac{\sqrt{5}}{4} - \frac{1}{4} - 0.587785720825195 i\right)^{- n - 1} + \left(-0.032361 + 1.0 i \left(- \frac{\sqrt{537}}{38} + \frac{29}{38}\right)^{2}\right) \left(- \frac{\sqrt{5}}{4} - \frac{1}{4} + 0.587785720825195 i\right)^{- n - 1} + \frac{3}{16} {\binom{n + 1}{1}} + 0.10764 {\binom{n + 2}{2}} + \frac{1}{24} {\binom{n + 3}{3}} + 0.0083333 {\binom{n + 4}{4}} + 0.2411
  $$

  A list of OEIS entries that contains this subsequence.

  1. Number of partitions of n into at most 5 parts: https://oeis.org/A001401
  1. Number of partitions of n in which the greatest part is 5: https://oeis.org/A026811

* `11* 22* 33* 44* 55*`: 5 compositions of n

  Its generating function is
  $$
  \frac{80.0 z^{4} - 160.0 z^{3} + 160.0 z^{2} - 80.0 z + 16.0}{- 16.0 z^{5} + 80.0 z^{4} - 160.0 z^{3} + 160.0 z^{2} - 80.0 z + 16.0} - 1.0
  $$
  For words of sizes up to 20 in this language, their counts are:

      0, 0, 0, 0, 0, 1, 5, 15, 35, 70, 126, 210, 330, 495, 715, 1001, 1365, 1820, 2380, 3060

  Its closed form is
  $$
  - 1.0 \delta\left(n\right) - 10 {\binom{n + 1}{1}} + 10 {\binom{n + 2}{2}} - 5 {\binom{n + 3}{3}} + {\binom{n + 4}{4}} + 5
  $$

  A list of OEIS entries that contains this subsequence.

  1. Binomial coefficient binomial(n,4) = n*(n-1)*(n-2)*(n-3)/24: https://oeis.org/A000332

* `(11*)*`: all compositions of n

  Its generating function is
  $$
  0.5 + \frac{1.0}{- 4.0 z + 2.0}
  $$
  For words of sizes up to 20 in this language, their counts are:

      1, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144

  Its closed form is
  $$
  \frac{1}{4} 2^{n + 1} + 0.5 \delta\left(n\right)
  $$

  A list of OEIS entries that contains this subsequence.

  1. Powers of 2: https://oeis.org/A000079
  1. Expansion of (1-x)/(1-2*x) in powers of x: https://oeis.org/A011782
  1. Zero followed by powers of 2 (cf: https://oeis.org/A131577
  1. Powers of 2, omitting 2 itself: https://oeis.org/A151821
  1. Orders of finite Abelian groups having the incrementally largest numbers of nonisomorphic forms (A046054): https://oeis.org/A046055
  1. a(n) = floor(2^|n-1|/2): https://oeis.org/A034008
  1. Smallest exponent such that -1+3^a(n) is divisible by 2^n: https://oeis.org/A090129
  1. Pisot sequences E(4,8), L(4,8), P(4,8), T(4,8): https://oeis.org/A020707
  1. Numbers n such that in the difference triangle of the divisors of n (including the divisors of n) the diagonal from the bottom entry to n gives the divisors of n: https://oeis.org/A273109
  1. a(n)=2*A131577(n): https://oeis.org/A155559

* `(.........................)* (..........)* (.....)* (.)*`: number of ways to make n cents with US coins.

  Its generating function is
  $$
  \frac{1.0}{1.0 z^{41} - 1.0 z^{40} - 1.0 z^{36} + 1.0 z^{35} - 1.0 z^{31} + 1.0 z^{30} + 1.0 z^{26} - 1.0 z^{25} - 1.0 z^{16} + 1.0 z^{15} + 1.0 z^{11} - 1.0 z^{10} + 1.0 z^{6} - 1.0 z^{5} - 1.0 z + 1.0}
  $$
  For words of sizes up to 20 in this language, their counts are:

      1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 6, 6, 6, 6, 6

  Its closed form is
  $$
  - 0.0125 \left(-1\right)^{- n - 1} + \left(-0.99212 - 0.125333309173584 i\right)^{- n - 1} \left(-0.0069053 - 1.0 i \left(- \frac{13}{6} + \frac{\sqrt{181}}{6}\right)^{2}\right) + \left(-0.99212 + 0.125333309173584 i\right)^{- n - 1} \left(-0.0069053 + 1.0 i \left(- \frac{13}{6} + \frac{\sqrt{181}}{6}\right)^{2}\right) + \left(-0.92978 + 1.0 i \left(- \frac{3}{4} + \frac{\sqrt{21}}{12}\right)\right)^{- n - 1} \left(-0.0043866 + 1.0 i \left(- \frac{\sqrt{3}}{3} + \frac{2}{3}\right)^{2}\right) + \left(-0.92978 + 1.0 i \left(- \frac{\sqrt{21}}{12} + \frac{3}{4}\right)\right)^{- n - 1} \left(-0.0043866 - 1.0 i \left(- \frac{\sqrt{3}}{3} + \frac{2}{3}\right)^{2}\right) + \left(-0.63742 + 1.0 i \left(\frac{3}{28} + \frac{\sqrt{345}}{28}\right)\right)^{- n - 1} \left(0.0012389 + 1.0 i \left(-5 + \sqrt{26}\right)^{2}\right) + \left(-0.63742 + 1.0 i \left(- \frac{\sqrt{345}}{28} - \frac{3}{28}\right)\right)^{- n - 1} \left(0.0012389 - 1.0 i \left(-5 + \sqrt{26}\right)^{2}\right) + \left(-0.42578 - 0.904827117919922 i\right)^{- n - 1} \left(-0.010572 + 0.000665162689983845 i\right) + \left(-0.42578 + 0.904827117919922 i\right)^{- n - 1} \left(-0.010572 - 0.000665162689983845 i\right) + \left(-0.18738 - 0.982287406921387 i\right)^{- n - 1} \left(- \left(- \frac{\sqrt{74}}{26} + \frac{5}{13}\right)^{2} - 0.0112435072660446 i\right) + \left(-0.18738 + 0.982287406921387 i\right)^{- n - 1} \left(- \left(- \frac{\sqrt{74}}{26} + \frac{5}{13}\right)^{2} + 0.0112435072660446 i\right) + \left(0.062791 - 0.998026847839355 i\right)^{- n - 1} \left(- \left(- \frac{4}{11} + \frac{3 \sqrt{3}}{11}\right)^{2} + 1.0 i \left(- \frac{\sqrt{41}}{8} + \frac{7}{8}\right)^{2}\right) + \left(0.062791 + 0.998026847839355 i\right)^{- n - 1} \left(- \left(- \frac{4}{11} + \frac{3 \sqrt{3}}{11}\right)^{2} - 1.0 i \left(- \frac{\sqrt{41}}{8} + \frac{7}{8}\right)^{2}\right) + \left(0.53583 - 0.844327926635742 i\right)^{- n - 1} \left(\left(- \frac{\sqrt{15}}{10} + \frac{1}{2}\right)^{2} - 0.0135340839624405 i\right) + \left(0.53583 + 0.844327926635742 i\right)^{- n - 1} \left(\left(- \frac{\sqrt{15}}{10} + \frac{1}{2}\right)^{2} + 0.0135340839624405 i\right) + \left(-0.020515 - 0.0130189061164856 i\right) \left(0.72897 - 0.684547424316406 i\right)^{- n - 1} + \left(-0.020515 + 0.0130189061164856 i\right) \left(0.72897 + 0.684547424316406 i\right)^{- n - 1} + \left(0.87631 - 0.481753826141357 i\right)^{- n - 1} \left(\left(- \frac{2}{3} + \frac{\sqrt{22}}{6}\right)^{2} - 1.0 i \left(- \frac{29}{54} + \frac{\sqrt{949}}{54}\right)\right) + \left(0.87631 + 0.481753826141357 i\right)^{- n - 1} \left(\left(- \frac{2}{3} + \frac{\sqrt{22}}{6}\right)^{2} - 1.0 i \left(- \frac{\sqrt{949}}{54} + \frac{29}{54}\right)\right) + \left(-0.0701 - 0.0133722722530365 i\right) \left(0.96858 - 0.248689889907837 i\right)^{- n - 1} + \left(-0.0701 + 0.0133722722530365 i\right) \left(0.96858 + 0.248689889907837 i\right)^{- n - 1} + 0.000680520199239254 i \left(- \frac{1}{4} + \frac{\sqrt{5}}{4} - 0.951056480407715 i\right)^{- n - 3} {\binom{n + 2}{2}} + \left(-0.012442 + 0.00355014950037003 i\right) \left(- \frac{1}{4} + \frac{\sqrt{5}}{4} - 0.951056480407715 i\right)^{- n - 2} {\binom{n + 1}{1}} + \left(- \frac{19}{40} + \frac{\sqrt{281}}{40} - 0.0925073623657227 i\right) \left(- \frac{1}{4} + \frac{\sqrt{5}}{4} - 0.951056480407715 i\right)^{- n - 1} - 0.000680520199239254 i \left(- \frac{1}{4} + \frac{\sqrt{5}}{4} + 0.951056480407715 i\right)^{- n - 3} {\binom{n + 2}{2}} + \left(-0.012442 - 0.00355014950037003 i\right) \left(- \frac{1}{4} + \frac{\sqrt{5}}{4} + 0.951056480407715 i\right)^{- n - 2} {\binom{n + 1}{1}} + \left(- \frac{19}{40} + \frac{\sqrt{281}}{40} + 0.0925073623657227 i\right) \left(- \frac{1}{4} + \frac{\sqrt{5}}{4} + 0.951056480407715 i\right)^{- n - 1} + \left(-0.0125 - 0.0384615384615385 i\right) \left(\frac{1}{4} + \frac{\sqrt{5}}{4} - 0.587785720825195 i\right)^{- n - 1} + \left(-0.0125 + 0.0384615384615385 i\right) \left(\frac{1}{4} + \frac{\sqrt{5}}{4} + 0.587785720825195 i\right)^{- n - 1} - 0.000420584809035063 i \left(- \frac{\sqrt{5}}{4} - \frac{1}{4} - 0.587785720825195 i\right)^{- n - 3} {\binom{n + 2}{2}} + \left(\left(- \frac{7}{10} + \frac{\sqrt{59}}{10}\right)^{2} + 1.0 i \left(- \frac{6}{5} + \frac{\sqrt{41}}{5}\right)^{2}\right) \left(- \frac{\sqrt{5}}{4} - \frac{1}{4} - 0.587785720825195 i\right)^{- n - 2} {\binom{n + 1}{1}} + \left(-0.063078 - 0.0218961536884308 i\right) \left(- \frac{\sqrt{5}}{4} - \frac{1}{4} - 0.587785720825195 i\right)^{- n - 1} + 0.000420584809035063 i \left(- \frac{\sqrt{5}}{4} - \frac{1}{4} + 0.587785720825195 i\right)^{- n - 3} {\binom{n + 2}{2}} + \left(\left(- \frac{7}{10} + \frac{\sqrt{59}}{10}\right)^{2} - 1.0 i \left(- \frac{6}{5} + \frac{\sqrt{41}}{5}\right)^{2}\right) \left(- \frac{\sqrt{5}}{4} - \frac{1}{4} + 0.587785720825195 i\right)^{- n - 2} {\binom{n + 1}{1}} + \left(-0.063078 + 0.0218961536884308 i\right) \left(- \frac{\sqrt{5}}{4} - \frac{1}{4} + 0.587785720825195 i\right)^{- n - 1} + \left(-0.0125 - 0.00908178091049194 i\right) \left(- \frac{\sqrt{5}}{4} + \frac{1}{4} - 0.951056480407715 i\right)^{- n - 1} + \left(-0.0125 + 0.00908178091049194 i\right) \left(- \frac{\sqrt{5}}{4} + \frac{1}{4} + 0.951056480407715 i\right)^{- n - 1} + 0.1194 {\binom{n + 1}{1}} + 0.0148 {\binom{n + 2}{2}} + 0.0008 {\binom{n + 3}{3}} + 0.5005
  $$

  A list of OEIS entries that contains this subsequence.

  1. Highest minimal distance of any Type I (strictly) singly-even binary self-dual code of length 2n: https://oeis.org/A105674
  1. Number of ways of making change for n cents using coins of 1, 5, 10, 25 cents: https://oeis.org/A001299
  1. Number of ways of making change for n cents using coins of 1, 5, 10, 25, 50 cents: https://oeis.org/A001300
  1. Number of ways of making change for n cents using coins of 1, 5, 10, 25, 50 and 100 cents: https://oeis.org/A169718
  1. Number of ways of making change for n cents using coins of 1, 5, 10, 20, 50, 100 cents: https://oeis.org/A001306
  1. Repetition of even numbers, with initial zeros, five times: https://oeis.org/A130496
  1. Number of ways of making change for n cents using coins of 1, 5, 10 cents: https://oeis.org/A187243
  1. Coefficients of the mock theta function chibar(q): https://oeis.org/A260984

* `(00*1)*00*`: list of 0-sequences

  Its generating function is
  $$
  \frac{1.0 z}{- 1.0 z^{2} - 1.0 z + 1.0}
  $$
  For words of sizes up to 20 in this language, their counts are:

      0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181

  Its closed form is
  $$
  \left(- \frac{1}{2} + \frac{\sqrt{5}}{2}\right)^{- n - 1} \left(- \frac{\sqrt{5}}{10} + \frac{1}{2}\right) + \left(- \frac{\sqrt{5}}{2} - \frac{1}{2}\right)^{- n - 1} \left(\frac{\sqrt{5}}{10} + \frac{1}{2}\right)
  $$

  A list of OEIS entries that contains this subsequence.

  1. Fibonacci numbers: https://oeis.org/A000045
  1. Pisot sequences E(3,5), P(3,5): https://oeis.org/A020701
  1. Expansion of (1-x)/(1-x-x^2): https://oeis.org/A212804
  1. Pisot sequence E(2,3): https://oeis.org/A020695
  1. Least k such that the maximum number of elements among the continued fractions for k/1, k/2, k/3, k/4 : https://oeis.org/A071679
  1. a(n) = Fibonacci(n) mod n^3: https://oeis.org/A132636
  1. Expansion of 1/(1 - x - x^2 + x^18 - x^20): https://oeis.org/A185357
  1. Nearly-Fibonacci sequence: https://oeis.org/A264800
  1. Pisot sequences E(5,8), P(5,8): https://oeis.org/A020712
  1. a(n) = s(1)t(n) + s(2)t(n-1) + : https://oeis.org/A024595
