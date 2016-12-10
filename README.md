# Regex Enumerator

<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/3be5b46356ad1be74d4b8030a050c49d.svg?invert_in_darkmode" align=middle width=655.4196pt height=39.45249pt/></p>

<sub>*Or how I learned to stop worrying and start counting things with calculus*</sub>

-----

Have you ever wondered about how many different strings you can form that fits your favorite regex?

Yeah, chances are you probably haven't. But it's on your mind now.

Here's one of my favorite regexes:

    (0+, )*0+
    
It specifies the class of languages that are comma-separated list of strings of zeros. For example,
`000, 0, 00000` belongs to this language, but `0,,0` and `0,0,` does not.

Now, it might seem like a masochistic endeavor, but if you enumerate every possible word in this language, you'll
find that there are no empty strings, 1 single letter string, 1 two letter string, 2 three letter strings, 3 four letter
strings, and so on. This pattern actually looks like

    0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, ...

"Why, that is the fibonacci sequence! How did it end up in such a mundane place?"

Now, I could give you a combinatorial interpretation for this amazeballs result, but I still get shivers up my spine
whenever I think back to my undergrad Combinatorics course. Instead, I'll give a more general way to compute these
enumerations.

However, that's not the end of it. It turns out that this algorithm can also compute a closed-form expression
for this sequence.
<p align="center"><img src="https://rawgit.com/leegao/RegexEnumerator/svgs/svgs/ed522eedb3660b291b47e81f834440d8.svg?invert_in_darkmode" align=middle width=472.60785pt height=52.667175pt/></p>

Now, this might not look very pretty, but it's still pretty cool that there is a (computable) closed form expression that
counts every regular expression.