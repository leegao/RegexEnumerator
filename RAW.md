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
     * [Additional Examples](#additional-examples)


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

This library is just meant to be a demonstration. 

You will need Python 2.7 or up, though it seems to be most stable on Python 3+.

Note that you will need to install `numpy`, `scipy`, and `sympy` in order to support solving a few
linear equations and to translate numerically computed roots into algebraic forms, if they are available.

```bash
git clone https://github.com/leegao/RegexEnumerator.git
cd RegexEnumerator
sudo python setup.py develop
```

To uninstall, run

```bash
pip uninstall RegexEnumerator
```

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

* `disambiguate(regex)`: [EXPERIMENTAL] attempts to construct an unambiguous regular expression. In many cases,
  regular expressions are ambiguous. For example, $(0\mid 0)$ is a classic example. Ambiguities is the source of
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
  $R_{k}^{L}(u, v)$, which will be described below.
  
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
$$
r = (xx^*,)^*xx^*
$$
We've seen above that this follows a fibonacci-like sequence. Is there some-way that we can derive this
fact without brute-force enumeration?

Let's start with the sequence of `x`es: $x*$. This language, in an infinitely expanded form, looks like
$$
x^* = \epsilon \mid x \mid xx \mid xxx \mid \cdots
$$

Now, here's a trick. Let's pretend that our bar ($\mid$) is a plus sign ($+$), so that
$$
x^* = \epsilon + x + xx + xxx + \cdots
$$

This looks remarkably familiar. In fact, if you are working within a numerical field, then a little bit of
precalculus would also show that
$$
\frac{1}{1 - x} = 1 + x + xx + xxx + \cdots
$$

Could there be some connection here? Well, let's find out. To do this, let's equate the two expressions:
$$
x^* = \epsilon + x + xx + xxx + \cdots ~~~ \equiv ~~~ 1 + x + xx + xxx + \cdots = \frac{1}{1 - x}
$$
so $\epsilon \equiv 1$ and $x^* \equiv \frac{1}{1 - x}$ if we pretend that each regular expression has a numerical value.

In fact, this works for every regular expression. For any regular expressions $e_0, e_1$ and for any letters $x, y, z$ we have
\begin{align*}
\epsilon &\equiv 1 \\
x, y, z &\equiv x, y, z \\
e_0 e_1 &\equiv e_0 \times e_1 \\
e_0 \mid e_1 &\equiv e_0 + e_1 \\
e^* &\equiv \frac{1}{1 - e}
\end{align*}
As long as you don't need to invoke the axiom of multiplicative-commutativity, this reduction works.

For example, for the comma-separated list example, we have
\begin{align*}
(xx^*,)^*xx^* &\equiv \frac{1}{1 - (xx^*,)}xx^* \\
&\equiv \frac{1}{1 - (x\frac{1}{1 - x},)} x \frac{1}{1 - x}
\end{align*}

Note here that $,$ is a variable! It might be tempting to try to simplify this further. Letting $z_{,}$ denote the comma, 
we might try
\begin{align*}
\frac{1}{1 - (x\frac{1}{1 - x}z_{,})} x \frac{1}{1 - x} &= \frac{\frac{x}{1 - x}}{\frac{1 - x}{1 - x} - \frac{xz_{,}}{1 - x}} \\
&= \frac{x}{(1 - x) - xz_{,}}
\end{align*}

But this requires a crucial axiom that we do not have:

* We do not have multiplicative commutativity, so we couldn't merge $\frac{1}{1 - x}\times x \ne \frac{x}{1 - x}$, since 
  no longer know whether this is $x \times \frac{1}{1 - x}$ or $\frac{1}{1 - x} \times x$.
[](
This begs a natural question. If we can't take inverses or negate things, then why do we admit the expression $\frac{1}{1 - x}$?
Well, in this language, that term is **atomic**. Therefore, we cannot break it down and look at it as a subtraction followed by
an inverse; it is just $\frac{1}{1-x}$. I'll clear this up later.
)

Now that we have this weird "compiler" taking us from regular expressions to numerical formulas, can you tell us what it means
for a regular expression to take a numerical value?

The answer: none. There is no meaning to assign a value of say $0.1$ to $x$, or that $y^* = 0.2$. It doesn't mean anything, 
it's just pure gibberish. Don't do it, except maybe values of $0$ or $1$; we'll get to that later.

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
$$
(xx^*,)^*xx^* \equiv \frac{x}{(1 - x) - xz_{,}}
$$
Which tells us that our regular expression is isomorphic to the regular expression $(x \mid x,)^*x$. That is, for each
comma-separated list, you can map it to one of the words in $(x \mid x,)^*x$. In fact, not only are these two languages
isomorphic; they are the same! A moment of thought reveals that this new regular expression also matches only comma-separated list
of sequences as well.

That's a pretty cool trick to deduce equivalences between regular expressions, but is that all there is to it?

It turns out that each of these translated numerical expressions also admit an infinite series expansion (in terms of its free variables). So
$$
\frac{x}{(1 - x) - xz_{,}} = a_{0,0} + a_{0, 1} z_{,}^1 + a_{1, 0} x^1 + a_{1, 1} x^1 z_{,}^1 + a_{0, 2} z_{,}^2 + a_{1,2} x^1z_{,}^2 \cdots
$$
and in general, we have the multivariable expansion
$$
f(x_0, x_1, \dots, x_n) = \sum_{(i_0, \dots, i_n) \in \mathbb{N}^n} a_{i_0, \dots, i_n} x_0^{i_0} \cdots x_n^{i_n}
$$
where $a_{i}$ is the coefficient attached to the $x_0^{i_0} \cdots x_n^{i_n}$ term.

However, recall that each of the $x^uz_{,}^v = x\stackrel{u}{\dots} x,\stackrel{v}{\dots},$ corresponds to exactly one of
the words in our language. Therefore, if there are 5 words of size 6 with just one comma in our language, the coefficient in front
of $x^5z_{,}^1$ in the series expansion must be 5.

Herein lies the key to our approach. Once we grant the freedom of commutativity, each of these regular expressions "generates"
a numerical function with some infinite series expansion. The coefficients of the $x_0^{i} x_1^{j} x_2^{k}$ term in this
expansion is then the total count of all objects in this regular language that has `i` $x_0$s, `j` $x_1$s, and `k` $x_2$s.

This approach is called the generating function approach within elementary combinatorics. It is a powerful idea to create
these compact analytical (if a bit nonsensical) representations of your combinatorial objects of interest in order to
use more powerful analytical tools to find properties about them.

#### Rational Functions

We know that there's a translation for our regular expression
$$
(xx^*,)^*xx^* \equiv \frac{x}{(1 - x) - xz_{,}} = \sum_{n,m} a_{n,m} x^nz_{,}^m
$$
into some numerical field. We also know that this numerical formula admits a two-variable infinite series expansion.
The task at hand now is one familiar to most students of complex analysis: coefficient extraction. Given a function
$f(x, y)$, how are we going to find the coefficients of $x^ny^m$?

Before we tackle that beast, let's develop some more intuition about the functions that we will be working with.
In general combinatorics, you may face complicated functions using an exotic variety of functions, differential forms,
and even implicit functions that can't be expressed in some explicit form. So where do regular expressions sit on
this spectrum?

As it turns out, things are much nicer with regular expression (part of the reason they are called "regular"; their regularities
ensure that their algebraic properties are easier to analyze than general unbounded constructions). In particular
if a regular expression has a translation
$$
[\![e]\!] = f(x_0, \dots, x_n),
$$
then we know for a fact that $f(\vec{x})$ is rational. What this means is that there's some pair of **polynomials** $p, q$ such that
$$
f(\vec{x}) = \frac{p(\vec{x})}{q(\vec{x})}
$$
The proof of this fact will be included in the appendix for interested readers, however that proof does not contribute much here.
Polynomials are interesting in the context of infinite expansions. Since polynomials are already in the form
$$
p(\vec{x}) = \sum_{\vec{i} \in \mathbb{N}^n}^{\deg(p)} a_{\vec{i}}\vec{x}^{\vec{i}},
$$
their infinite expansions are in fact finite. Now, the same cannot be said of $\frac{1}{q(\vec{x})}$, but a bit of algebra
shows that the series expansion of this inverse is also computable:
\begin{align*}
\frac{1}{q(\vec{x})} &= \frac{q(0)}{\frac{q(0) + \sum_{\vec{i} \ne 0}a_{\vec{i}} \vec{x}^{\vec{i}}}{q(0)}} \\
&= q(0) \frac{1}{1 - \underbrace{(-\sum_{\vec{i} \ne 0}\frac{a_{\vec{i}}}{q(0)} \vec{x}^{\vec{i}})}_{\text{call this }\hat q(\vec{x})}} \\
&= q(0) (1 + \hat{q}(\vec{x}) + \hat{q}(\vec{x})^2 + \dots)
\end{align*}

This form is particularly amenable for coefficient extraction, and a memoized version of this sits at the heart of the
validation algorithm we use to test that the algebra for everything else is done correctly. See the appendix for a derivation
of the dynamic program that can turn this into a somewhat fast coefficient extraction algorithm.

#### Univariate Functions

Now, up to now, we've been talking about multivariable functions $f(\vec{x})$. This makes sense since we need to parameterize
our model on each of the letters in our alphabet (oh boy). In general however, multivariable coefficient extraction problems
are prohibitively difficult. Not only that, the numerical tools needed to compute saddle-points are outside the scope of this
toy project. For more on general methods of multivariate enumeration techniques, check out [ACVS].

The situation isn't so bleak within the rational-function realm however, and while there is a straightforward extension of
the traditional coefficient-extraction technique to multivariable rational-functions, I just never got to it. See [Stoutemyer08]
for a brief summary of the multivariate partial-fraction decomposition method. Just know that this isn't supported currently.

Instead, we will only support the class of enumeration problems that counts the total number of words of a certain (singular) size in some language family.
The trick here is to turn a blind eye on the fact that $x$ and $y$ are different variables. In order to do this, we just set them both equal
to some other variable $z$. Therefore, the Fibonnacci generating function above
$$
\frac{x}{1 - x - xz_{,}} = \frac{z}{1 - z - z^2}
$$

#### Partial Fraction Decompositions

Now that we have a univariate rational function of the form
$$
f(z) = \frac{p(z)}{q(z)}
$$
where $p,q$ are mutually irreducible (that is, there isn't some other polynomial $r(z)$ that evenly divides both $p$ and $q$).

There's a concept within polynomial algebra known as a partial fraction decomposition. This decomposition theorem tells us that
$$
f(z) = \frac{p(z)}{q(z)} = \sum_{r \in \mathcal{V}(q)} \sum_{k = 1}^{\mathrm{multiplicity}(r)} \frac{a_{r,k}}{(z - r)^k}
$$
where $\mathcal{V}(q)$ (the variety) is the set of roots of $q(z) = 0$ and $\mathrm{multiplicity}(r)$ is its multiplicity.

So for example, the rational function $\frac{p(z)}{(z - 1)^2(z - \pi)}$ has the partial fraction decomposition of
$$
\frac{p(z)}{(z - 1)^2(z - \pi)} = \frac{a_{1,1}}{z - 1} + \frac{a_{1,2}}{(z - 1)^2} + \frac{a_{\pi,1}}{z - \pi}
$$
no matter what $p(z)$ is. To solve for $a_{r,k}$, you can exploit the fact that
$$
\frac{A}{(z - r_0)} + \frac{B}{(z - r_1)} + \cdots + \frac{Z}{(z - r_n)} = \frac{A \frac{q(z)}{z - r_0} + \cdots + Z \frac{q(z)}{z - r_n}}{(z - r_0) \cdots (z - r_n) = p(z)}
$$
expanding the numerator and setting them equal to $p(z)$ will give you a linear system to solve. The details of how we are going
to solve this linear system doesn't matter, it'll be taken care of for you under the hood by `numpy`.

Now, how does the partial fraction decomposition help us? Recall that
$$
\frac{A}{z - r} = \frac{\frac{A}{-r}}{1 - \frac{z}{r}} = \left(-\frac{A}{r}\right) \times \left(1 + r^{-1} z + r^{-2}z^2 + \cdots\right)
$$
and in general (by way of the binomial theorem)
$$
\frac{A}{(z - r)^k} = \frac{A(-r)^{-k}}{(1 - \frac{z}{r})^k} = \left(A(-r)^{-k}\right) \left(1 + \binom{k}{k-1}r^{-1}z + \binom{k + 1}{k}r^{-2}z^2 + \cdots\right)
$$
which means that if 
$$
f(z) = \sum_{r,k} \frac{a_{r,k}}{(z - r)^k}
$$
then the coefficients on $z^n$ is
$$
[z^n]f(z) = \sum_{r, k} (-1)^k a_{r, k}\binom{n + k - 1}{k - 1} r^{-(n+k)}
$$

*Bam!* Closed form expression for any arbitrary regular expression!

While this might seem super complicated, at the heart of this method, we're just using a very well-known method to expand
a rational function. This is in part why the functional part of this project that deals with computing this closed form is only
a couple of lines long. It's actually a really simple idea.

#### Fibonacci, Redux

### Additional Examples
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


[ACVS]: https://www.math.upenn.edu/~pemantle/papers/ACSV.pdf
[Stoutemyer08]: https://doi.org/10.1145/1504341.1504346