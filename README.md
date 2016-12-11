# Regex Enumerator

Enumerate Regular Expressions the Fun Way.

<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/aa4d414dd40b418624756ba65b24c190.svg?invert_in_darkmode" align=middle width=672.31395pt height=39.45249pt/></p>

<p align="center">
<img src="http://i.imgur.com/sRo5tQz.png?invert_in_darkmode"/>
</p>

<sub>*Or how I learned to stop worrying and start counting things with calculus*</sub>

-----

Have you ever wondered about how many different strings you can form that fits your favorite regex?

Yeah, chances are you probably haven't. But it's on your mind now.

Here's one of my favorite regular expressions:
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/120bcbe220479f3fb301392b145130a5.svg?invert_in_darkmode" align=middle width=65.09151pt height=18.020145pt/></p>
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
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/c709d2b386c7588133c620efa335e165.svg?invert_in_darkmode" align=middle width=514.0443pt height=52.667175pt/></p>
where <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/c9c53a99901c4a67544997f70b0f01bc.svg?invert_in_darkmode" align=middle width=18.19125pt height=23.24256pt/> is the number of comma-separated lists of size <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode" align=middle width=9.36144pt height=14.93184pt/>.

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

* <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/b44b0a181653840433cbcd08a7638cb7.svg?invert_in_darkmode" align=middle width=78.053415pt height=13.9105725pt/></p>
* <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/197232bbcfbca260e636689189e10f3b.svg?invert_in_darkmode" align=middle width=88.823955pt height=16.438356pt/></p>

Here, `%` denotes the "empty" transition <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/7ccca27b5ccc533a2dd72dc6fa28ed84.svg?invert_in_darkmode" align=middle width=6.1668915pt height=14.93184pt/> in formal languages. In effect, it acts as the
identity element of concatenation, so that <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/ffbd759215219ed839b38b1f27aedd2f.svg?invert_in_darkmode" align=middle width=58.917705pt height=15.38856pt/>. For example, the regular expression of
comma delimited language <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/4052b2961cf5ab33404b96cd5e12aae9.svg?invert_in_darkmode" align=middle width=71.423715pt height=26.95407pt/> can be encoded as
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

The magic behind this will be discussed in the next section. The <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/c068b57af6b6fa949824f73dcb828783.svg?invert_in_darkmode" align=middle width=41.681475pt height=23.24256pt/> code looks like 
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/2382f4301164b8719a1e94d28f7c7e73.svg?invert_in_darkmode" align=middle width=267.8313pt height=39.45249pt/></p>
Note that this differs from the above since we're enumerating <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/d2432a60d1dc5806cd53447ce48d2e43.svg?invert_in_darkmode" align=middle width=57.942225pt height=26.95407pt/> instead of <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/f9d2f9a74a3d1a9fc852220717fcbd49.svg?invert_in_darkmode" align=middle width=65.49939pt height=26.95407pt/>.

In addition, regular expressions correspond to the family of rational functions (quotient of two polynomials).
To see the generating function of a regular expression, try

```python
from regex_enumerate import generating_function
from sympy import latex

print(latex(generating_function("(0+1)*0+")))
```

which outputs
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/2f5a67f61cf674ae11beb062c1f892d6.svg?invert_in_darkmode" align=middle width=140.091435pt height=34.360095pt/></p>

#### Caveat

There are many regular expressions that are ambiguous. For example, the regular expression
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/c983706ca99ab3174d64641faec9442f.svg?invert_in_darkmode" align=middle width=30.13692pt height=16.438356pt/></p>
is inherently ambiguous. On encountering a `0`, it's not clear which side of the bar it belongs to. While
this poses no challenges to parsing (since we don't output a parse-tree), it does matter in enumeration.
In particular, the direct translation of this expression will claim that there are 2 strings of size 1
in this language.

There are ways to circumvent this, but I haven't gotten around to tackling this problem yet. Therefore, know that
for some regular expressions, this technique will fail unless you manually reduce it to an unambiguous form.
There is always a way to do this, though it might create an exponential number of additional states.

#### Additional Examples
* `(00*1)*`: 1-separated strings that starts with 0 and ends with 1
  Its generating function is <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/1123f13a5cf59d4870e9a7320d2f869e.svg?invert_in_darkmode" align=middle width=127.30608pt height=34.360095pt/></p>
  For words of sizes up to 20 in this language, their counts are:

      1, 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584

  Its closed form is <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/4ce1b82d1485300e9111c68da61e077b.svg?invert_in_darkmode" align=middle width=501.83265pt height=52.667175pt/></p>

* `(%|1|11)(00*(1|11))*0* | 1`: complete 1 or 11-separated strings
  Its generating function is <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/b8aeb10e24f0dcd276ca81740fa7667f.svg?invert_in_darkmode" align=middle width=248.3646pt height=37.147275pt/></p>
  For words of sizes up to 20 in this language, their counts are:

      1, 3, 4, 7, 13, 24, 44, 81, 149, 274, 504, 927, 1705, 3136, 5768, 10609, 19513, 35890, 66012, 121415

  Its closed form is <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/024a6cd2f5d2a9090ad4da3705edb0b6.svg?invert_in_darkmode" align=middle width=1286.4951pt height=19.789935pt/></p>

* `(000)*(111)*(22)*(33)*(44)*`: complex root to (1 - z**3)**-2 * (1 - z**2)**-3
  Its generating function is <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/744d2e9b7793e8d7eeebd74a206f57ed.svg?invert_in_darkmode" align=middle width=558.4359pt height=34.360095pt/></p>
  For words of sizes up to 20 in this language, their counts are:

      1, 0, 3, 2, 6, 6, 13, 12, 24, 24, 39, 42, 63, 66, 96, 102, 138, 150, 196, 210

  Its closed form is <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/e3e434f9f80fd7bd07e85029a3b48196.svg?invert_in_darkmode" align=middle width=2908.026pt height=42.804135pt/></p>

* `1*(22)*(333)*(4444)*(55555)*`: number of ways to make change give coins of denomination 1 2 3 4 and 5
  Its generating function is <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/88cc6eed2a47cad72b2f75df37e3223f.svg?invert_in_darkmode" align=middle width=677.8431pt height=34.360095pt/></p>
  For words of sizes up to 20 in this language, their counts are:

      1, 1, 2, 3, 5, 7, 10, 13, 18, 23, 30, 37, 47, 57, 70, 84, 101, 119, 141, 164

  Its closed form is <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/a2d29ceab49c773111de5872c5afe7ee.svg?invert_in_darkmode" align=middle width=4482.1095pt height=59.178735pt/></p>

* `11* 22* 33* 44* 55*`: 5 compositions of n
  Its generating function is <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/2478a0938079a952ba396709115a9a3c.svg?invert_in_darkmode" align=middle width=419.4267pt height=37.147275pt/></p>
  For words of sizes up to 20 in this language, their counts are:

      0, 0, 0, 0, 0, 1, 5, 15, 35, 70, 126, 210, 330, 495, 715, 1001, 1365, 1820, 2380, 3060

  Its closed form is <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/7e7aeb9917c208bc8ac08bbf703d1ff9.svg?invert_in_darkmode" align=middle width=466.39395pt height=39.45249pt/></p>

* `(11*)*`: all compositions of n
  Its generating function is <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/aec8780df1f8cf1561a4af35a738592a.svg?invert_in_darkmode" align=middle width=126.32202pt height=34.360095pt/></p>
  For words of sizes up to 20 in this language, their counts are:

      1, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144

  Its closed form is <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/9d2cd0af8c8bd1f4a588934cfc61fddc.svg?invert_in_darkmode" align=middle width=118.418685pt height=32.9901pt/></p>

* `(.........................)* (..........)* (.....)* (.)*`: number of ways to make n cents with US coins.
  Its generating function is <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/db2edcc857a1573432da15c9c6371800.svg?invert_in_darkmode" align=middle width=944.8296pt height=34.360095pt/></p>
  For words of sizes up to 20 in this language, their counts are:

      1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 6, 6, 6, 6, 6

  Its closed form is <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/9c329eacacd565a206f02bc5bbe8179f.svg?invert_in_darkmode" align=middle width=21417.99pt height=59.178735pt/></p>

* `(00*1)*00*`: list of 0-sequences
  Its generating function is <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/dff15208c98f51e2b1f62cf27a693988.svg?invert_in_darkmode" align=middle width=140.091435pt height=34.360095pt/></p>
  For words of sizes up to 20 in this language, their counts are:

      0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181

  Its closed form is <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/841cce6bf5f0f977e25c033bc101dd71.svg?invert_in_darkmode" align=middle width=472.60785pt height=52.667175pt/></p>
