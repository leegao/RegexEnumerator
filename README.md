# Regex Enumerator

Enumerate Regular Expressions the Fun Way.

<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/aa4d414dd40b418624756ba65b24c190.svg?invert_in_darkmode" align=middle width=672.31395pt height=39.45249pt/></p>

<p align="center">
<img src="http://i.imgur.com/sRo5tQz.png?invert_in_darkmode"/>
</p>

<sub>*Or how I learned to stop worrying and started counting things with calculus; TeX rendered using [readme2tex](https://github.com/leegao/readme2tex)*</sub>

-----

### Table of Contents

* [Regex Enumerator](#regex-enumerator)
     * [Table of Contents](#table-of-contents)
     * [Installation](#installation)
     * [Usage](#usage)
        * [Regular Expression Syntax](#regular-expression-syntax)
        * [Library Functions](#library-functions)
        * [Caveat](#caveat)
     * [Justification](#justification)
        * [Regular Expressions as Numerical Expressions](#regular-expressions-as-numerical-expressions)
        * [Rational Functions](#rational-functions)
        * [Univariate Functions](#univariate-functions)
        * [Partial Fraction Decompositions](#partial-fraction-decompositions)
        * [Fibonacci, Redux](#fibonacci-redux)
     * [Appendix](#appendix)
        * [Library Architecture](#library-architecture)
        * [Additional Examples](#additional-examples)

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

You will need Python 2.7 or up, though it seems to be most stable on Python 3+.

```bash
git clone https://github.com/leegao/RegexEnumerator.git
cd RegexEnumerator
sudo python setup.py develop
```

Note that you will need to install `numpy`, `scipy`, and `sympy` in order to support solving a few
linear equations and to translate numerically computed roots into algebraic forms, if they are available.

To uninstall, run

```bash
pip uninstall RegexEnumerator
```

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
  <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/1fc3c5fe30de9b941a91921b8527493b.svg?invert_in_darkmode" align=middle width=267.8313pt height=39.45249pt/></p>
  Note that this differs from the above since we're enumerating <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/d2432a60d1dc5806cd53447ce48d2e43.svg?invert_in_darkmode" align=middle width=57.942225pt height=26.95407pt/> instead of <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/f9d2f9a74a3d1a9fc852220717fcbd49.svg?invert_in_darkmode" align=middle width=65.49939pt height=26.95407pt/>.

* `check_on_oeis`: This will search https://oeis.org for a potential combinatorial interpretation of your
  enumeration.
  
  ```python
  from regex_enumerate import check_on_oeis
  sequences = check_on_oeis("(0+,)*0+", start=5)
  for oeis in sequences:
    print('%s: https://oeis.org/%s' % (oeis.name, oeis.id))

  # Fibonacci numbers: https://oeis.org/A000045
  # Pisot sequences E(3,5), P(3,5): https://oeis.org/A020701
  # Expansion of (1-x)/(1-x-x^2): https://oeis.org/A212804
  # Pisot sequence E(2,3): https://oeis.org/A020695
  # Least k such that the maximum number of elements among the continued fractions for k/1, k/2, k/3, k/4 : https://oeis.org/A071679
  # a(n) = Fibonacci(n) mod n^3: https://oeis.org/A132636
  # Expansion of 1/(1 - x - x^2 + x^18 - x^20): https://oeis.org/A185357
  # Nearly-Fibonacci sequence: https://oeis.org/A264800
  # Pisot sequences E(5,8), P(5,8): https://oeis.org/A020712
  # a(n) = s(1)t(n) + s(2)t(n-1) + : https://oeis.org/A024595
  ```

* `disambiguate(regex)`: *[Experimental]* attempts to construct an unambiguous regular expression. In many cases,
  regular expressions are ambiguous. For example, <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/a5e47a69368560eb1f96acf425b6b4da.svg?invert_in_darkmode" align=middle width=42.416715pt height=25.43409pt/> is a classic example. Ambiguities is the source of
  redundancy, and unfortunately, our enumeration methods won't understand that the redundant components are already
  taken care of. Therefore, care must be taken to to ensure that the regular expression is unambiguous.
  
  This is an experimental algorithm that reduces any regular expression into an ambiguity free form. The cost is a
  potentially exponential blow-up in the size of your regular expression. However, for most of the simple cases, this
  is alright.
  
  ```python
  from regex_enumerate import disambiguate, enumerate_coefficients
  from itertools import islice
  
  # 0*0* is equivalent to just 0*
  print(list(islice(enumerate_coefficients('0*0*'), 10)))
  # [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
  
  # Let's disambiguate this problem
  print(list(islice(enumerate_coefficients(disambiguate('0*0*')), 10)))
  # [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
  ```
  
  In general, this should work. However, it does require a fair bit of term-rewriting to
  ensure that some of the intermediate steps can be reduced properly. Therefore, if something
  seems fishy, you can always inspect the reconstructed DFA and its disambiguation form
  <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/d507b0de6241f92619c33714931ba5f0.svg?invert_in_darkmode" align=middle width=60.00258pt height=28.43346pt/>, which will be described below.
  
  ```python
  from regex_enumerate import compile_disambiguously, reduce
  from random import sample
  R, dfa, accepts, number_of_states = compile_disambiguously("0*0*")
  # The states are arbitrarily ordered, so we can say that a state u < v when its 'id' is less than that of the others.
  
  # R(u, v, k) is the regular expression that allows an automaton to transition from u to v using only nodes
  # [1, ..., k] in its intermediate steps.
  print(R(1, *sample(accepts), 3)) # 1 -> ...(<3) -> some random final state
  print(R(1, *sample(accepts), number_of_states)) # Regex describing all the ways of getting from start (node 1) to some final state
  # Additionally, R(u, v, k) is designed to be mutually orthogonal, so R(u, v, k) + R(u, v', k) is unambiguous
  ```

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

To remedy this, you can try to use `regex_enumerate.disambiguate(regex)`, but it's not completely clear
that this is correct. Therefore, know that
for some regular expressions, this technique will fail unless you manually reduce it to an unambiguous form.
There is always a way to do this, though it might create an exponential number of additional states.

### Justification

Now, all of this might feel a little bullshitty. (Shameless plug, for more bullshitty math, check out http://bullshitmath.lol)
Is there any real justification for what you are doing here? Am I just enumerating a bunch of pre-existing cases
and running through a giant table lookup?

Well, it's actually a lot simpler than that. However, there's a bit of a setup for the problem.

#### Regular Expressions as Numerical Expressions

Let's rewind back to our first example; that of enumerating comma-separated sequences of `x`es:
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/c6281cf4f962d25fbc36c57ce7850bbf.svg?invert_in_darkmode" align=middle width=109.31118pt height=16.438356pt/></p>
We've seen above that this follows a fibonacci-like sequence. Is there some-way that we can derive this
fact without brute-force enumeration?

Let's start with the sequence of `x`es: <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/4522248e54d76be0a26031c14eeb96a9.svg?invert_in_darkmode" align=middle width=17.108685pt height=16.07364pt/>. This language, in an infinitely expanded form, looks like
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/3381c5da3dc46afe9e4deb717a7f6664.svg?invert_in_darkmode" align=middle width=175.8834pt height=16.438356pt/></p>

Now, here's a trick. Let's pretend that our bar (<img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/57fe5a91a139252a27ed191b2680eda7.svg?invert_in_darkmode" align=middle width=4.0607325pt height=25.43409pt/>) is a plus sign (<img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/df33724455416439909c33a7db76b2bc.svg?invert_in_darkmode" align=middle width=12.27996pt height=19.95477pt/>), so that
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/e6a8413df070790dcc80a7af6dc4e05b.svg?invert_in_darkmode" align=middle width=201.4551pt height=13.511025pt/></p>

This looks remarkably familiar. In fact, if you are working within a numerical field, then a little bit of
precalculus would also show that
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/a48f22fd8de4155848bc1a018da8b40e.svg?invert_in_darkmode" align=middle width=225.72825pt height=34.360095pt/></p>

Could there be some connection here? Well, let's find out. To do this, let's equate the two expressions:
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/bf7e136f136c7efe33bc173e1bf1a070.svg?invert_in_darkmode" align=middle width=484.71555pt height=34.360095pt/></p>
so <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/fe2120e91ad08218bdfb64ad6b47fa90.svg?invert_in_darkmode" align=middle width=36.303795pt height=21.96381pt/> and <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/6b424929bb1a83860737d2188f80b16f.svg?invert_in_darkmode" align=middle width=64.617795pt height=28.55226pt/> if we pretend that each regular expression has a numerical value.

In fact, this works for every regular expression. For any regular expressions <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/49f3694ae5275a3e33da3e17e4dd9528.svg?invert_in_darkmode" align=middle width=36.03567pt height=14.93184pt/> and for any letters <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/6ecf10ed1c08ba92db30119ef192228f.svg?invert_in_darkmode" align=middle width=40.51806pt height=14.93184pt/> we have
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/5f1add925794ecf4a2957a175b9ee8cc.svg?invert_in_darkmode" align=middle width=114.99972pt height=131.41953pt/></p>
As long as you don't need to invoke the axiom of multiplicative-commutativity, this reduction works.

For example, for the comma-separated list example, we have
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/52d12c6130dc0b733e761d30072694e5.svg?invert_in_darkmode" align=middle width=241.30095pt height=84.50739pt/></p>

Note here that <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/497403162f282a343c315086f75ba766.svg?invert_in_darkmode" align=middle width=4.0607325pt height=14.93184pt/> is a variable! It might be tempting to try to simplify this further. Letting <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/2404d424965cf131c13c2080768326c8.svg?invert_in_darkmode" align=middle width=11.043285pt height=14.93184pt/> denote the comma, 
we might try
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/d8c119d2514099b760bc51bb48b0e9fd.svg?invert_in_darkmode" align=middle width=260.3436pt height=84.74664pt/></p>

But this requires a crucial axiom that we do not have:

* We do not have multiplicative commutativity, so we couldn't merge <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/080bdd9337021a90b67fc7ed0a645b6e.svg?invert_in_darkmode" align=middle width=103.39791pt height=28.55226pt/>, since 
  no longer know whether this is <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/5a43d840c0717ad3ba88234ef1d697fb.svg?invert_in_darkmode" align=middle width=55.234245pt height=28.55226pt/> or <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/76f426704274ce73132925d7690385b3.svg?invert_in_darkmode" align=middle width=55.22682pt height=28.55226pt/>.
[](
This begs a natural question. If we can't take inverses or negate things, then why do we admit the expression <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/3f332093a7dbcc97f190d6d57fa8d322.svg?invert_in_darkmode" align=middle width=23.768085pt height=28.55226pt/>?
Well, in this language, that term is **atomic**. Therefore, we cannot break it down and look at it as a subtraction followed by
an inverse; it is just <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/982c522bfaa34942669aa7ebd7bbdca3.svg?invert_in_darkmode" align=middle width=23.768085pt height=28.55226pt/>. I'll clear this up later.
)

Now that we have this weird "compiler" taking us from regular expressions to numerical formulas, can you tell us what it means
for a regular expression to take a numerical value?

The answer: none. There is no meaning to assign a value of say <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/22f2e6fc19e491418d1ec4ee1ef94335.svg?invert_in_darkmode" align=middle width=20.499105pt height=21.96381pt/> to <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/332cc365a4987aacce0ead01b8bdcc0b.svg?invert_in_darkmode" align=middle width=8.88954pt height=14.93184pt/>, or that <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/3f6a01eca3b8d6c424522f2e11ccb80e.svg?invert_in_darkmode" align=middle width=58.623015pt height=23.41515pt/>. It doesn't mean anything, 
it's just pure gibberish. Don't do it, except maybe values of <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/29632a9bf827ce0200454dd32fc3be82.svg?invert_in_darkmode" align=middle width=7.713717pt height=21.96381pt/> or <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/034d0a6be0424bffe9a6e7ac9236c0f5.svg?invert_in_darkmode" align=middle width=7.713717pt height=21.96381pt/>; we'll get to that later.

Okay. So why did we go on this wild goose-hunt if their values don't even mean anything? 
It turns out that the value of a formula is not what we are interested in; these objects are compact and have nice algebraic properties.
When we count things, we just care about how many objects there are that satisfies a certain property.
When we count all words of, say, size 5 in a language, we don't care whether these strings are `000,0` or `0,0,0`. The ordering
of the letters in these strings are extraneous details that we no longer care about. Therefore, it would be nice to be able to
forget these details. More formally, if the order of letters in a word doesn't matter, we would say that
*we want the concatenation operator to be commutative*. If there's a representational equivalence to the numerical "field",
then the translation would be that *we want the multiplication operator to be commutative.*

This is a huge game-changer. In the above example, we weren't able to fully simplify that ugly product of fractions precisely
because we lacked this crucial axiom. Luckily for us, it now allows us to fully simplify the expression
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/b5a38b664b97b87056dd23d6d12873bf.svg?invert_in_darkmode" align=middle width=196.581pt height=34.177275pt/></p>
Which tells us that our regular expression is isomorphic to the regular expression <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/82bb6a5e8e09489f748ec969fe5190f4.svg?invert_in_darkmode" align=middle width=69.026265pt height=25.43409pt/>. That is, for each
comma-separated list, you can map it to one of the words in <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/82bb6a5e8e09489f748ec969fe5190f4.svg?invert_in_darkmode" align=middle width=69.026265pt height=25.43409pt/>. In fact, not only are these two languages
isomorphic; they are the same! A moment of thought reveals that this new regular expression also matches only comma-separated list
of sequences as well.

That's a pretty cool trick to deduce equivalences between regular expressions, but is that all there is to it?

It turns out that each of these translated numerical expressions also admit an infinite series expansion (in terms of its free variables). So
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/473f23014075bbcd0c0de58e6318aae8.svg?invert_in_darkmode" align=middle width=511.00995pt height=34.177275pt/></p>
and in general, we have the multivariable expansion
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/ac3262648c32411a072d132fd3c8085f.svg?invert_in_darkmode" align=middle width=341.8173pt height=40.54809pt/></p>
where <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/0aae089ed20772138e327117bd8c6bac.svg?invert_in_darkmode" align=middle width=12.834525pt height=14.93184pt/> is the coefficient attached to the <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/1949bc43d509deddd1ed78695ad786ff.svg?invert_in_darkmode" align=middle width=66.720555pt height=30.61674pt/> term.

However, recall that each of the <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/1abf06af410e5fda80c06d2b5d246d77.svg?invert_in_darkmode" align=middle width=133.7292pt height=22.61622pt/> corresponds to exactly one of
the words in our language. Therefore, if there are 5 words of size 6 with just one comma in our language, the coefficient in front
of <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/60406b22dbf1f8660041fb24bb74e5e1.svg?invert_in_darkmode" align=middle width=31.184175pt height=27.5385pt/> in the series expansion must be 5.

Herein lies the key to our approach. Once we grant the freedom of commutativity, each of these regular expressions "generates"
a numerical function with some infinite series expansion. The coefficients of the <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/1a1ddd375cabb38c3e605c08d7df4181.svg?invert_in_darkmode" align=middle width=49.69437pt height=31.80408pt/> term in this
expansion is then the total count of all objects in this regular language that has `i` <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/e714a3139958da04b41e3e607a544455.svg?invert_in_darkmode" align=middle width=15.44202pt height=14.93184pt/>s, `j` <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/277fbbae7d4bc65b6aa601ea481bebcc.svg?invert_in_darkmode" align=middle width=15.44202pt height=14.93184pt/>s, and `k` <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/95d239357c7dfa2e8d1fd21ff6ed5c7b.svg?invert_in_darkmode" align=middle width=15.44202pt height=14.93184pt/>s.

This approach is called the generating function approach within elementary combinatorics. It is a powerful idea to create
these compact analytical (if a bit nonsensical) representations of your combinatorial objects of interest in order to
use more powerful analytical tools to find properties about them.

#### Rational Functions

We know that there's a translation for our regular expression
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/8606a7f23ef7cbb3634c38fd0d1b7c79.svg?invert_in_darkmode" align=middle width=318.5358pt height=39.33996pt/></p>
into some numerical field. We also know that this numerical formula admits a two-variable infinite series expansion.
The task at hand now is one familiar to most students of complex analysis: coefficient extraction. Given a function
<img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/cf23450151a368a8b73be5295d28b948.svg?invert_in_darkmode" align=middle width=47.4474pt height=25.43409pt/>, how are we going to find the coefficients of <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/277251a7ce43b611d5199e923eb207ad.svg?invert_in_darkmode" align=middle width=38.151465pt height=22.61622pt/>?

Before we tackle that beast, let's develop some more intuition about the functions that we will be working with.
In general combinatorics, you may face complicated functions using an exotic variety of functions, differential forms,
and even implicit functions that can't be expressed in some explicit form. So where do regular expressions sit on
this spectrum?

As it turns out, things are much nicer with regular expression (part of the reason they are called "regular"; their regularities
ensure that their algebraic properties are easier to analyze than general unbounded constructions). In particular
if a regular expression has a translation
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/ab6b439a7b6f2f7bb1c89b15f3f86c33.svg?invert_in_darkmode" align=middle width=141.168225pt height=16.438356pt/></p>
then we know for a fact that <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/6bda3dbae94e295bc19dc26f6c98e392.svg?invert_in_darkmode" align=middle width=31.492395pt height=25.43409pt/> is rational. What this means is that there's some pair of **polynomials** <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/10984eabe311a6010d1a7c9ed19f290e.svg?invert_in_darkmode" align=middle width=22.99902pt height=14.93184pt/> such that
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/bb2c9595e133b232ec7531adc21556bb.svg?invert_in_darkmode" align=middle width=86.339055pt height=38.834895pt/></p>
The proof of this fact will be included in the appendix for interested readers, however that proof does not contribute much here.
Polynomials are interesting in the context of infinite expansions. Since polynomials are already in the form
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/2214bde9017d94e45c0e5fbf9ba8d168.svg?invert_in_darkmode" align=middle width=125.589255pt height=54.17544pt/></p>
their infinite expansions are in fact finite. Now, the same cannot be said of <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/4a8e6af385d1ec34270cdfef01270ec5.svg?invert_in_darkmode" align=middle width=23.653245pt height=28.55226pt/>, but a bit of algebra
shows that the series expansion of this inverse is also computable:
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/9fbd3c34d5a97baaf79cac3b11ee574f.svg?invert_in_darkmode" align=middle width=253.71885pt height=176.4015pt/></p>

This form is particularly amenable for coefficient extraction, and a memoized version of this sits at the heart of the
validation algorithm we use to test that the algebra for everything else is done correctly. See the appendix for a derivation
of the dynamic program that can turn this into a somewhat fast coefficient extraction algorithm.

#### Univariate Functions

Now, up to now, we've been talking about multivariable functions <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/6bda3dbae94e295bc19dc26f6c98e392.svg?invert_in_darkmode" align=middle width=31.492395pt height=25.43409pt/>. This makes sense since we need to parameterize
our model on each of the letters in our alphabet (oh boy). In general however, multivariable coefficient extraction problems
are prohibitively difficult. Not only that, the numerical tools needed to compute saddle-points are outside the scope of this
toy project. For more on general methods of multivariate enumeration techniques, check out [ACVS].

The situation isn't so bleak within the rational-function realm however, and while there is a straightforward extension of
the traditional coefficient-extraction technique to multivariable rational-functions, I just never got to it. See [Stoutemyer08]
for a brief summary of the multivariate partial-fraction decomposition method. Just know that this isn't supported currently.

Instead, we will only support the class of enumeration problems that counts the total number of words of a certain (singular) size in some language family.
The trick here is to turn a blind eye on the fact that <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/332cc365a4987aacce0ead01b8bdcc0b.svg?invert_in_darkmode" align=middle width=8.88954pt height=14.93184pt/> and <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/deceeaf6940a8c7a5a02373728002b0f.svg?invert_in_darkmode" align=middle width=8.14374pt height=14.93184pt/> are different variables. In order to do this, we just set them both equal
to some other variable <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/f93ce33e511096ed626b4719d50f17d2.svg?invert_in_darkmode" align=middle width=7.862085pt height=14.93184pt/>. Therefore, the Fibonnacci generating function above
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/984dadf6da36aa5408797007bd6f15cc.svg?invert_in_darkmode" align=middle width=177.936pt height=34.177275pt/></p>

#### Partial Fraction Decompositions

Now that we have a univariate rational function of the form
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/7dabb5affcaf18da653acdfa0ff2b07f.svg?invert_in_darkmode" align=middle width=84.28431pt height=38.834895pt/></p>
where <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/9ee547e0827e5bb29b5feb9f5f574193.svg?invert_in_darkmode" align=middle width=22.99902pt height=14.93184pt/> are mutually irreducible (that is, there isn't some other polynomial <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/07df09780199cd1c3b3d1dd82379f7aa.svg?invert_in_darkmode" align=middle width=28.52058pt height=25.43409pt/> that evenly divides both <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=7.765065pt height=14.93184pt/> and <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/d5c18a8ca1894fd3a7d25f242cbe8890.svg?invert_in_darkmode" align=middle width=7.4226075pt height=14.93184pt/>).

There's a concept within polynomial algebra known as a partial fraction decomposition. This decomposition theorem tells us that
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/8469ee2486413b1cb2d49a25f0d14ea2.svg?invert_in_darkmode" align=middle width=297.25905pt height=53.88141pt/></p>
where <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/4dbaa1ab010763c5072bb490bdbdf9d5.svg?invert_in_darkmode" align=middle width=31.63281pt height=25.43409pt/> (the variety) is the set of roots of <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/6691168338edf252db6a5fb234f77fea.svg?invert_in_darkmode" align=middle width=58.712445pt height=25.43409pt/> and <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/f400b03e899ac819ce6290b0df16a7d6.svg?invert_in_darkmode" align=middle width=103.029795pt height=25.43409pt/> is its multiplicity.

So for example, the rational function <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/02c1631f5be5eb90a102ce60a458bb0e.svg?invert_in_darkmode" align=middle width=75.156015pt height=33.9834pt/> has the partial fraction decomposition of
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/4076d8eaca686675b43659a2d77b30c3.svg?invert_in_darkmode" align=middle width=313.9125pt height=38.834895pt/></p>
no matter what <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/8fffcccc47f9f88dac738cc6bbf65e09.svg?invert_in_darkmode" align=middle width=28.918065pt height=25.43409pt/> is. To solve for <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/c5c1cb5ecc00088ca2051b21a52d9357.svg?invert_in_darkmode" align=middle width=25.10343pt height=14.93184pt/>, you can exploit the fact that
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/437096621f5105075f864f97c3f54c0f.svg?invert_in_darkmode" align=middle width=472.52535pt height=45.711435pt/></p>
expanding the numerator and setting them equal to <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/8fffcccc47f9f88dac738cc6bbf65e09.svg?invert_in_darkmode" align=middle width=28.918065pt height=25.43409pt/> will give you a linear system to solve. The details of how we are going
to solve this linear system doesn't matter, it'll be taken care of for you under the hood by `numpy`.

Now, how does the partial fraction decomposition help us? Recall that
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/5ebcb0a6aef6336b53761379189db9f7.svg?invert_in_darkmode" align=middle width=379.07595pt height=44.72919pt/></p>
and in general (by way of the binomial theorem)
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/64b69890c199d02a3533d94b2a0fd322.svg?invert_in_darkmode" align=middle width=565.9731pt height=42.021375pt/></p>
which means that if 
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/bc50720b080c2bd9cd215c626870be73.svg?invert_in_darkmode" align=middle width=138.54984pt height=40.20753pt/></p>
then the coefficients on <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/d0d4c612492648caccbb6e4c2986e6ea.svg?invert_in_darkmode" align=middle width=15.98817pt height=22.61622pt/> is
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/a5e38cd8560cabca93520f790be6b17c.svg?invert_in_darkmode" align=middle width=316.83795pt height=45.845085pt/></p>

*Bam!* Closed form expression for any arbitrary regular expression!

While this might seem super complicated, at the heart of this method, we're just using a very well-known method to expand
a rational function. This is in part why the functional part of this project that deals with computing this closed form is only
a couple of lines long. It's actually a really simple idea.

#### Fibonacci, Redux

Let's come back to our favorite example once more. Given the regular expression <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/3379fa0e924be5123ee64e1f421a6deb.svg?invert_in_darkmode" align=middle width=66.93753pt height=26.95407pt/>, we know that it has the
generating function
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/d246479c1e11056e3eec08efd05a84f6.svg?invert_in_darkmode" align=middle width=306.89505pt height=33.58377pt/></p>
where <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/910f819b1d6c9bf336c25bc5345df020.svg?invert_in_darkmode" align=middle width=98.746395pt height=33.98736pt/> are the roots of the quadratic equation <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/3cc39928a4ebb8f13a9f49054471ee59.svg?invert_in_darkmode" align=middle width=102.14259pt height=27.5385pt/>. We know that this
admits a partial fraction decomposition of
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/0827a49d6b346954aed332b700cd9fdf.svg?invert_in_darkmode" align=middle width=311.5695pt height=78.99408pt/></p>
therefore <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/84e844b383c9257a41794dfa105758c9.svg?invert_in_darkmode" align=middle width=156.285195pt height=25.43409pt/> and <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/15a33695022d67cbc910abf1007bc517.svg?invert_in_darkmode" align=middle width=140.55129pt height=23.60787pt/>. Solving this linear system
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/32995b846087bc4805747e48d4e72228.svg?invert_in_darkmode" align=middle width=246.9753pt height=39.45249pt/></p>
will yield the coefficients <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/6c2c48406a5f21d3e7eb2c6f15b824cf.svg?invert_in_darkmode" align=middle width=26.54454pt height=14.93184pt/> and <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/46ad6e581ba2202a520dbe64748603c5.svg?invert_in_darkmode" align=middle width=27.751845pt height=14.93184pt/>, and you'll find that
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/23ff9545b6fda5cbf8af03fc5f2503be.svg?invert_in_darkmode" align=middle width=594.7194pt height=52.667175pt/></p>

In addition, if you plot the generating function <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/65e60fac43981f156ec935ea689c64d7.svg?invert_in_darkmode" align=middle width=46.50789pt height=23.62998pt/> (as is in picture at the top of this page):
<p align="center">
<img src="http://i.imgur.com/sRo5tQz.png?invert_in_darkmode"/>
</p>
you'll find that the singularities (the points where the graph suddenly jumps up and forms an infinitely tall column) are
located exactly at where the roots of <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/3cc39928a4ebb8f13a9f49054471ee59.svg?invert_in_darkmode" align=middle width=102.14259pt height=27.5385pt/> are found. This isn't surprising, since by the fact that <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/65e60fac43981f156ec935ea689c64d7.svg?invert_in_darkmode" align=middle width=46.50789pt height=23.62998pt/>
is irreducible, the roots of the denominator must be non-removable singularities! In fact, if all you cared about is the
asymptotic exponential behavior, then there's a simple graphical method to compute the asymptotic complexity of enumerating
your regular expression. Take <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/6dec54c48a0438a5fcde6053bdb9d712.svg?invert_in_darkmode" align=middle width=7.993425pt height=14.93184pt/> to be the root of the denominator that is closest to the origin on the complex plane, then
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/d27af326c61370ef2bf5c335e915ba52.svg?invert_in_darkmode" align=middle width=138.679035pt height=38.834895pt/></p>
In addition, if you can figure out the multiplicity of <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/6dec54c48a0438a5fcde6053bdb9d712.svg?invert_in_darkmode" align=middle width=7.993425pt height=14.93184pt/> (repeatedly divide out <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/17f7467ecdc06a6fd94ee61a8ccf8f79.svg?invert_in_darkmode" align=middle width=36.45213pt height=19.95477pt/> until that column disappears), you can
get an exact asymptotic characterization
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/d9d51ef1d54ad230bfea7ea95c0a1465.svg?invert_in_darkmode" align=middle width=152.980905pt height=38.834895pt/></p>

### Appendix

#### Library Architecture

It's definitely not too difficult to compute all of this by hand, but the math is really tedious and error prone. This
is why this library exists: it automates away the boring parts. In particular, nothing really complicated is going on here.

1. `regex_enumerate.parse` has a Shunting-Yard style stack-based parser to convert a regular expression into a regex tree.
2. `regex_enumerate.transfer` translates a regex tree into its equivalent numerical expression tree. In addition, it includes
  several algorithms for computations on polynomial rings and can simplify any induced numerical expression into a canonical form
  of 
  <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/dc53b77e5ef123b49af9752a7f39f211.svg?invert_in_darkmode" align=middle width=178.46895pt height=38.834895pt/></p>
  where <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/0d77c0b9d12687569adb6493ad31476b.svg?invert_in_darkmode" align=middle width=84.11799pt height=25.43409pt/> is a small polynomial in general and <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/4dcc632db84650b4f4ed212ad248db1f.svg?invert_in_darkmode" align=middle width=23.289915pt height=33.9834pt/> is irreducible (thus ensuring that all roots of <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/d5c18a8ca1894fd3a7d25f242cbe8890.svg?invert_in_darkmode" align=middle width=7.4226075pt height=14.93184pt/> are non-removable singularities).
3. `regex_enumerate.enumerate` has the exact dynamic-programming algorithm referenced above as well as the
   partial fraction decomposition algorithm to compute the closed-form counting expression.
4. `regex_enumerate.nfa` contains a set of utility functions to work with the semiring of regular language/finite automata.
   In particular, it will use a conflict-free characterization of cycles in an automata to compile every regular expression
   into some other non-ambiguous expression. The resulting regex is usually significantly larger (in terms of state-size), but
   they are equivalent in terms of counting.

#### Rationalizing Reduction

In general, it is not immediately obvious that the expression trees created from regular expressions are rational functions.
However, if we already know (ahead of time) that a function is rational, we can rationalize the expression into the form
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/1c70b94d3328498a6a28622d47fbd2d7.svg?invert_in_darkmode" align=middle width=29.423625pt height=38.834895pt/></p>
(where <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=7.765065pt height=14.93184pt/> and <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/d5c18a8ca1894fd3a7d25f242cbe8890.svg?invert_in_darkmode" align=middle width=7.4226075pt height=14.93184pt/> are not necessarily irreducible) through a pair of mutually inductive reductions.

Suppose that the language of regular expressions of unreduced numerical expressions is given by
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/d23af21acca0faae913d1a72f67c6bcc.svg?invert_in_darkmode" align=middle width=371.67075pt height=31.939875pt/></p>
we would like to reduce an arbitrary expression <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/8cd34385ed61aca950a6b06d09fb50ac.svg?invert_in_darkmode" align=middle width=7.1486415pt height=14.93184pt/> into some <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/6d25c0088d279b5b442786aca8d291fa.svg?invert_in_darkmode" align=middle width=6.263565pt height=25.35192pt/> where <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/9ee547e0827e5bb29b5feb9f5f574193.svg?invert_in_darkmode" align=middle width=22.99902pt height=14.93184pt/> are straightforward polynomials.

To do this, let's start by defining the canonical class of polynomial expressions <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/9ee547e0827e5bb29b5feb9f5f574193.svg?invert_in_darkmode" align=middle width=22.99902pt height=14.93184pt/>:
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/f6e959817dc1f543aa5fc29c2805ef3a.svg?invert_in_darkmode" align=middle width=110.351835pt height=37.032105pt/></p>

and define the canonical form of <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/a0f90601fb401814382478ecda71d394.svg?invert_in_darkmode" align=middle width=41.478855pt height=23.60787pt/>, where
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/11ae769488435622f7096dfd4cd13625.svg?invert_in_darkmode" align=middle width=40.033785pt height=32.670495pt/></p>

To construct this reduction <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/fec4d30366d4fc888a2f24a5a9b4fc53.svg?invert_in_darkmode" align=middle width=15.997575pt height=23.60787pt/>, we need another inductive class of the simple ring of polynomials, <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/247e6146381bd6874658519e61e6cc5b.svg?invert_in_darkmode" align=middle width=9.10932pt height=23.60787pt/>, defined
by
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/44d6618766f7333bd286f2dea6d029f1.svg?invert_in_darkmode" align=middle width=229.85655pt height=19.680375pt/></p>
with an associated reduction operator <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/92fa58483a7d853cff728d148cd4e84d.svg?invert_in_darkmode" align=middle width=47.3781pt height=31.91826pt/> that simplifies arithmetic on polynomials.

Now, let us give the inductive definition of the reduction relations:

* For <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/05f9c4cd6855734f3cc4141abbcdb89d.svg?invert_in_darkmode" align=middle width=52.29972pt height=25.43409pt/>
  <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/2b2abf6fc82fa5d1ef27efc1032c5ae1.svg?invert_in_darkmode" align=middle width=400.21245pt height=202.9104pt/></p>
* For <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/92fa58483a7d853cff728d148cd4e84d.svg?invert_in_darkmode" align=middle width=47.3781pt height=31.91826pt/>
  <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/a3cc4d671ad1b63e919f898b70f87921.svg?invert_in_darkmode" align=middle width=363.52635pt height=201.2241pt/></p>

This pair of reduction rules are implemented in `regex_enumerate.transfer.down_r` and `regex_enumerate.transfer.down_p`
respectively.

#### Additional Examples
* `(00*1)*`: 1-separated strings that starts with 0 and ends with 1

  Its generating function is
  <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/1123f13a5cf59d4870e9a7320d2f869e.svg?invert_in_darkmode" align=middle width=127.30608pt height=34.360095pt/></p>
  For words of sizes up to 20 in this language, their counts are:

      1, 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584

  Its closed form is
  <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/4ce1b82d1485300e9111c68da61e077b.svg?invert_in_darkmode" align=middle width=501.83265pt height=52.667175pt/></p>

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
  <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/b8aeb10e24f0dcd276ca81740fa7667f.svg?invert_in_darkmode" align=middle width=248.3646pt height=37.147275pt/></p>
  For words of sizes up to 20 in this language, their counts are:

      1, 3, 4, 7, 13, 24, 44, 81, 149, 274, 504, 927, 1705, 3136, 5768, 10609, 19513, 35890, 66012, 121415

  Its closed form is
  <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/024a6cd2f5d2a9090ad4da3705edb0b6.svg?invert_in_darkmode" align=middle width=1286.4951pt height=19.789935pt/></p>

  A list of OEIS entries that contains this subsequence.

  1. Tribonacci numbers: https://oeis.org/A000073

* `(000)*(111)*(22)*(33)*(44)*`: complex root to <img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/6e5a3ffb1d1e0a7d544ce8768d90c76d.svg?invert_in_darkmode" align=middle width=112.325565pt height=28.55226pt/>

  Its generating function is
  <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/744d2e9b7793e8d7eeebd74a206f57ed.svg?invert_in_darkmode" align=middle width=558.4359pt height=34.360095pt/></p>
  For words of sizes up to 20 in this language, their counts are:

      1, 0, 3, 2, 6, 6, 13, 12, 24, 24, 39, 42, 63, 66, 96, 102, 138, 150, 196, 210

  Its closed form is
  <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/e3e434f9f80fd7bd07e85029a3b48196.svg?invert_in_darkmode" align=middle width=2908.026pt height=42.804135pt/></p>

  A list of OEIS entries that contains this subsequence.


* `1*(22)*(333)*(4444)*(55555)*`: number of ways to make change give coins of denomination 1 2 3 4 and 5

  Its generating function is
  <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/88cc6eed2a47cad72b2f75df37e3223f.svg?invert_in_darkmode" align=middle width=677.8431pt height=34.360095pt/></p>
  For words of sizes up to 20 in this language, their counts are:

      1, 1, 2, 3, 5, 7, 10, 13, 18, 23, 30, 37, 47, 57, 70, 84, 101, 119, 141, 164

  Its closed form is
  <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/a2d29ceab49c773111de5872c5afe7ee.svg?invert_in_darkmode" align=middle width=4482.1095pt height=59.178735pt/></p>

  A list of OEIS entries that contains this subsequence.

  1. Number of partitions of n into at most 5 parts: https://oeis.org/A001401
  1. Number of partitions of n in which the greatest part is 5: https://oeis.org/A026811

* `11* 22* 33* 44* 55*`: 5 compositions of n

  Its generating function is
  <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/2478a0938079a952ba396709115a9a3c.svg?invert_in_darkmode" align=middle width=419.4267pt height=37.147275pt/></p>
  For words of sizes up to 20 in this language, their counts are:

      0, 0, 0, 0, 0, 1, 5, 15, 35, 70, 126, 210, 330, 495, 715, 1001, 1365, 1820, 2380, 3060

  Its closed form is
  <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/7e7aeb9917c208bc8ac08bbf703d1ff9.svg?invert_in_darkmode" align=middle width=466.39395pt height=39.45249pt/></p>

  A list of OEIS entries that contains this subsequence.

  1. Binomial coefficient binomial(n,4) = n*(n-1)*(n-2)*(n-3)/24: https://oeis.org/A000332

* `(11*)*`: all compositions of n

  Its generating function is
  <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/aec8780df1f8cf1561a4af35a738592a.svg?invert_in_darkmode" align=middle width=126.32202pt height=34.360095pt/></p>
  For words of sizes up to 20 in this language, their counts are:

      1, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144

  Its closed form is
  <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/9d2cd0af8c8bd1f4a588934cfc61fddc.svg?invert_in_darkmode" align=middle width=118.418685pt height=32.9901pt/></p>

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
  <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/db2edcc857a1573432da15c9c6371800.svg?invert_in_darkmode" align=middle width=944.8296pt height=34.360095pt/></p>
  For words of sizes up to 20 in this language, their counts are:

      1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 6, 6, 6, 6, 6

  Its closed form is
  <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/9c329eacacd565a206f02bc5bbe8179f.svg?invert_in_darkmode" align=middle width=21417.99pt height=59.178735pt/></p>

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
  <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/dff15208c98f51e2b1f62cf27a693988.svg?invert_in_darkmode" align=middle width=140.091435pt height=34.360095pt/></p>
  For words of sizes up to 20 in this language, their counts are:

      0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181

  Its closed form is
  <p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/841cce6bf5f0f977e25c033bc101dd71.svg?invert_in_darkmode" align=middle width=472.60785pt height=52.667175pt/></p>

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


[ACVS]: https://www.math.upenn.edu/~pemantle/papers/ACSV.pdf
[Stoutemyer08]: https://doi.org/10.1145/1504341.1504346