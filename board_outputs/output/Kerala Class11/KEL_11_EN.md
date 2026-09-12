<!-- page 0 -->
Appendix 1

INFINITE SERIES

A.1.1 Introduction

As discussed in the Chapter 9 on Sequences and Series, a sequence $a_1, a_2, ..., a_n, ...$
having infinite number of terms is called *infinite sequence* and its indicated sum, i.e.,
$a_1 + a_2 + a_3 + ... + a_n + ...$ is called an *infinite series* associated with infinite sequence.
This series can also be expressed in abbreviated form using the sigma notation, i.e.,

$$a_1 + a_2 + a_3 + \dots + a_n + \dots = \sum_{k=1}^{\infty} a_k$$

In this Chapter, we shall study about some special types of series which may be
required in different problem situations.

A.1.2 Binomial Theorem for any Index

In Chapter 8, we discussed the Binomial Theorem in which the index was a positive
integer. In this Section, we state a more general form of the theorem in which the
index is not necessarily a whole number. It gives us a particular type of infinite series,
called $Binomial$ $Series$. We illustrate few applications, by examples.

We know the formula

$$(1+x)^n = {}^n\mathrm{C}_0 + {}^n\mathrm{C}_1 x + \ldots + {}^n\mathrm{C}_n x^n$$

Here, $n$ is non-negative integer. Observe that if we replace index $n$ by negative
integer or a fraction, then the combinations ${}^n\mathrm{C}_r$ do not make any sense.

We now state (without proof), the Binomial Theorem, giving an infinite series in
which the index is negative or a fraction and not a whole number.

Theorem The formula

$$(1+x)^m = 1 + mx + \frac{m(m-1)}{1.2}x^2 + \frac{m(m-1)(m-2)}{1.2.3}x^3 + ...$$

holds whenever $|x|<1$.

<!-- page 1 -->
$\mathit{Remark}$ 1. Note carefully the condition $|x| < 1$, i.e., $-1 < x < 1$ is necessary when $m$
is negative integer or a fraction. For example, if we take $x = -2$ and $m = -2$, we
obtain

$$(1-2)^{-2}=1+(-2)(-2)+\frac{(-2)(-3)}{1.2}(-2)^{2}+\dots$$

or $1=1+4+12+\dots$

This is not possible

2.    Note that there are infinite number of terms in the expansion of $(1+x)^m$, when $m$
is a negative integer or a fraction

Consider
$$(a+b)^m = \left[ a \left( 1 + \frac{b}{a} \right) \right]^m = a^m \left( 1 + \frac{b}{a} \right)^m$$

$$= a^m \left[ 1 + m \frac{b}{a} + \frac{m(m-1)}{1.2} \left( \frac{b}{a} \right)^2 + ... \right]$$

$$= a^m + ma^{m-1}b + \frac{m(m-1)}{1.2} a^{m-2}b^2 + ...$$

This expansion is valid when $\left| \frac{b}{a} \right| < 1$ or equivalently when $| \ b \ | < | \ a \ |$.

The general term in the expansion of $(a + b)^m$ is

$$\frac{m(m-1)(m-2)...(m-r+1)a^{m-r}b^r}{1.2.3...r}$$

We give below certain particular cases of Binomial Theorem, when we assume
$|x|<1$, these are left to students as exercises:

1. $(1+x)^{-1}=1-x+x^{2}-x^{3}+\ldots$
2. $(1-x)^{-1}=1+x+x^{2}+x^{3}+\ldots$
3. $(1+x)^{-2}=1-2x+3x^{2}-4x^{3}+\ldots$
4. $(1-x)^{-2}=1+2x+3x^{2}+4x^{3}+\ldots$

Example 1 Expand $\left(1-\frac{x}{2}\right)^{-\frac{1}{2}}$, when $|x|<2$.

<!-- page 2 -->
Solution We have

$$\left(1-\frac{x}{2}\right)^{\frac{1}{2}} = 1+\frac{\left(-\frac{1}{2}\right)}{1}\left(\frac{-x}{2}\right)+\frac{\left(-\frac{1}{2}\right)\left(-\frac{3}{2}\right)}{1.2}\left(-\frac{x}{2}\right)^{2}+\dots$$

$$= 1+\frac{x}{4}+\frac{3x^{2}}{32}+\dots$$

A.1.3 Infinite Geometric Series

From Chapter 9, Section 9.5, a sequence $a_1, a_2, a_3, ..., a_n$ is called G.P., if

$\frac{a_{k+1}}{a_k} = r$ (constant) for $k = 1, 2, 3, ..., n-1$. Particularly, if we take $a_1 = a$, then the
resulting sequence $a, ar, ar^2, ..., ar^{r-1}$ is taken as the standard form of G.P., where $a$ is
first term and $r$, the common ratio of G.P.

Earlier, we have discussed the formula to find the sum of finite series
$a + ar + ar^2 + ... + ar^{n-1}$ which is given by

$$S_n = \frac{a(1-r^n)}{1-r}.$$

In this section, we state the formula to find the sum of infinite geometric series
$a + ar + ar^2 + ... + ar^{n-1} + ...$ and illustrate the same by examples.

Let us consider the G.P. 1, $\frac{2}{3}$, $\frac{4}{9}$,....

Here $a=1$, $r=\frac{2}{3}$. We have

$$S_n = \frac{1 - \left( \frac{2}{3} \right)^n}{1 - \frac{2}{3}} = 3 \left[ 1 - \left( \frac{2}{3} \right)^n \right] \quad \dots (1)$$

Let us study the behaviour of $\left(\frac{2}{3}\right)^n$ as $n$ becomes larger and larger.

<!-- page 3 -->
<table>
<thead>
<tr>
<th>n</th>
<th>1</th>
<th>5</th>
<th>10</th>
<th>20</th>
</tr>
</thead>
<tbody>
<tr>
<td>\left(\frac{2}{3}\right)^n</td>
<td>0.6667</td>
<td>0.1316872428</td>
<td>0.01734152992</td>
<td>0.00030072866</td>
</tr>
</tbody>
</table>

We observe that as $n$ becomes larger and larger, $\left(\frac{2}{3}\right)^n$ becomes closer and closer to

zero. Mathematically, we say that as $n$ becomes sufficiently large, $\left(\frac{2}{3}\right)^n$ becomes

sufficiently small. In other words, as $n \rightarrow \infty, \left( \frac{2}{3} \right)^n \rightarrow 0$. Consequently, we find that

the sum of infinitely many terms is given by $S = 3$.

Thus, for infinite geometric progression $a, ar, ar^2, ...$, if numerical value of common
ratio $r$ is less than 1, then

$$S_n = \frac{a(1-r^n)}{1-r} = \frac{a}{1-r} - \frac{ar^n}{1-r}$$

In this case, $r^n \to 0$ as $n \to \infty$ since $|r| < 1$ and then $\frac{ar^n}{1-r} \to 0$. Therefore,

$$S_n \rightarrow \frac{a}{1-r} \text{ as } n \rightarrow \infty.$$

Symbolically, sum to infinity of infinite geometric series is denoted by S. Thus,

we have $$S = \frac{a}{1-r}$$

For example

(i) $1+\frac{1}{2}+\frac{1}{2^2}+\frac{1}{2^3}+...=\frac{1}{1-\frac{1}{2}}=2$


(ii) $1-\frac{1}{2}+\frac{1}{2^2}-\frac{1}{2^3}+...=\frac{1}{1-\left(-\frac{1}{2}\right)}=\frac{1}{1+\frac{1}{2}}=\frac{2}{3}$

<!-- page 4 -->
Example 2 Find the sum to infinity of the G.P. ;

$$\frac{-5}{4}, \frac{5}{16}, \frac{-5}{64}, .....$$

Solution Here $a=\frac{-5}{4}$ and $r=-\frac{1}{4}$. Also $|r|<1$.

Hence, the sum to infinity is $\frac{\frac{-5}{4}}{1+\frac{1}{4}}=\frac{\frac{-5}{4}}{\frac{5}{4}}=-1$.

A.1.4 Exponential Series

Leonhard Euler (1707 – 1783), the great Swiss mathematician introduced the number
$e$ in his calculus text in 1748. The number $e$ is useful in calculus as $\pi$ in the study of the
circle.

Consider the following infinite series of numbers

$$1+\frac{1}{1!}+\frac{1}{2!}+\frac{1}{3!}+\frac{1}{4!}+... \quad \dots (1)$$

The sum of the series given in (1) is denoted by the number $e$
Let us estimate the value of the number $e$.

Since every term of the series (1) is positive, it is clear that its sum is also positive.
Consider the two sums

$$\frac{1}{3!} + \frac{1}{4!} + \frac{1}{5!} + ... + \frac{1}{n!} + ... \quad ... (2)$$

and $\frac{1}{2^2} + \frac{1}{2^3} + \frac{1}{2^4} + .... + \frac{1}{2^{n-1}} + ...$ ... (3)

Observe that

$\frac{1}{3!} = \frac{1}{6}$ and $\frac{1}{2^2} = \frac{1}{4}$, which gives $\frac{1}{3!} < \frac{1}{2^2}$

$\frac{1}{4!} = \frac{1}{24}$ and $\frac{1}{2^3} = \frac{1}{8}$, which gives $\frac{1}{4!} < \frac{1}{2^3}$

$\frac{1}{5!} = \frac{1}{120}$ and $\frac{1}{2^4} = \frac{1}{16}$, which gives $\frac{1}{5!} < \frac{1}{2^4}$.

<!-- page 5 -->
Therefore, by analogy, we can say that

$$\frac{1}{n!} < \frac{1}{2^{n-1}} , \text{ when } n > 2$$

We observe that each term in (2) is less than the corresponding term in (3),

Therefore $\left( \frac{1}{3!} + \frac{1}{4!} + \frac{1}{5!} + ... + \frac{1}{n!} \right) < \left( \frac{1}{2^2} + \frac{1}{2^3} + \frac{1}{2^4} + ... + \frac{1}{2^{n-1}} + ... \right)$ ... (4)

Adding $\left(1+\frac{1}{1!}+\frac{1}{2!}\right)$ on both sides of (4), we get,

$$\left(1+\frac{1}{1!}+\frac{1}{2!}\right)+\left(\frac{1}{3!}+\frac{1}{4!}+\frac{1}{5!}+\dots+\frac{1}{n!}+\dots\right)$$

$$< \left\{ \left( 1 + \frac{1}{1!} + \frac{1}{2!} \right) + \left( \frac{1}{2^2} + \frac{1}{2^3} + \frac{1}{2^4} + ... + \frac{1}{2^{n-1}} + ... \right) \right\} \dots (5)$$

$$= \left\{ 1 + \left( 1 + \frac{1}{2} + \frac{1}{2^2} + \frac{1}{2^3} + \frac{1}{2^4} + ... + \frac{1}{2^{n-1}} + ... \right) \right\}$$

$$= 1 + \frac{1}{1 - \frac{1}{2}} = 1 + 2 = 3$$

Left hand side of (5) represents the series (1). Therefore $e < 3$ and also $e > 2$ and
hence $2 < e < 3$.

Remark The exponential series involving variable $x$ can be expressed as

$$e^x = 1 + \frac{x}{1!} + \frac{x^2}{2!} + \frac{x^3}{3!} + ... + \frac{x^n}{n!} + ...$$

Example 3 Find the coefficient of $x^2$ in the expansion of $e^{2x+3}$ as a series in
powers of $x$.

Solution In the exponential series

$$e^x = 1 + \frac{x}{1!} + \frac{x^2}{2!} + \frac{x^3}{3!} + ...$$

replacing $x$ by $(2x + 3)$, we get

<!-- page 6 -->
$$e^{2x+3} = 1 + \frac{(2x+3)}{1!} + \frac{(2x+3)^2}{2!} + ...$$

Here, the general term is $\frac{(2x+3)^n}{n!} = \frac{(3+2x)^n}{n!}$. This can be expanded by the
Binomial Theorem as

$$\frac{1}{n!} \left[ 3^n + ^n\text{C}_1 3^{n-1} (2x) + ^n\text{C}_2 3^{n-2} (2x)^2 + ... + (2x)^n \right].$$

Here, the coefficient of $x^2$ is $\frac{{}^n\mathbf{C}_2 3^{n-2} 2^2}{n!}$. Therefore, the coefficient of $x^2$ in the whole
series is

$$\sum_{n=2}^{\infty} \frac{{}^nC_2 3^{n-2} 2^2}{n!} = 2 \sum_{n=2}^{\infty} \frac{n(n-1) 3^{n-2}}{n!}$$

$$= 2 \sum_{n=2}^{\infty} \frac{3^{n-2}}{(n-2)!} \quad [\text{using } n! = n \ (n-1) \ (n-2)!]$$

$$= 2 \left[ 1 + \frac{3}{1!} + \frac{3^2}{2!} + \frac{3^3}{3!} + ... \right]$$

$$= 2e^3.$$

Thus $2e^3$ is the coefficient of $x^2$ in the expansion of $e^{2x+3}$.
Alternatively $e^{2x+3} = e^3$ . $e^{2x}$

$$= e^3 \left[ 1 + \frac{2x}{1!} + \frac{(2x)^2}{2!} + \frac{(2x)^3}{3!} + ... \right]$$

Thus, the coefficient of $x^2$ in the expansion of $e^{2x+3}$ is $e^3 \cdot \frac{2^2}{2!} = 2e^3$

Example 4 Find the value of $e^2$, rounded off to one decimal place.

Solution Using the formula of exponential series involving $x$, we have

$$e^x = 1 + \frac{x}{1!} + \frac{x^2}{2!} + \frac{x^3}{3!} + ... + \frac{x^n}{n!} + ...$$

<!-- page 7 -->
Putting $x=2$, we get

$$e^2 = 1 + \frac{2}{1!} + \frac{2^2}{2!} + \frac{2^3}{3!} + \frac{2^4}{4!} + \frac{2^5}{5!} + \frac{2^6}{6!} + ...$$

$$= 1+2+2+\frac{4}{3}+\frac{2}{3}+\frac{4}{15}+\frac{4}{45}+\dots$$

$\ge$ the sum of first seven terms $\ge 7.355$.

On the other hand, we have

$$e^2 < \left( 1 + \frac{2}{1!} + \frac{2^2}{2!} + \frac{2^3}{3!} + \frac{2^4}{4!} \right) + \frac{2^5}{5!} \left( 1 + \frac{2}{6} + \frac{2^2}{6^2} + \frac{2^3}{6^3} + ... \right)$$

$$= 7 + \frac{4}{15} \left( 1 + \frac{1}{3} + \left( \frac{1}{3} \right)^2 + ... \right) = 7 + \frac{4}{15} \left( \frac{1}{1 - \frac{1}{3}} \right) = 7 + \frac{2}{5} = 7.4.$$

Thus, $e^2$ lies between 7.355 and 7.4. Therefore, the value of $e^2$, rounded off to one
decimal place, is 7.4.

A.1.5 Logarithmic Series

Another very important series is logarithmic series which is also in the form of infinite
series. We state the following result without proof and illustrate its application with an
example.

Theorem If $| x | < 1$, then

$$\log_e (1+x) = x - \frac{x^2}{2} + \frac{x^3}{3} - \dots$$

The series on the right hand side of the above is called the $logarithmic$ $series$.

Note The expansion of $\log_e (1+x)$ is valid for $x=1$. Substituting $x=1$ in the
expansion of $\log_e (1+x)$, we get

$$\log_e 2 = 1 - \frac{1}{2} + \frac{1}{3} - \frac{1}{4} + ...$$

<!-- page 8 -->
Example 5 If $\alpha, \beta$ are the roots of the equation $x^2 - px + q = 0$, prove that

$$\log_e \left( 1 + px + qx^2 \right) = (\alpha + \beta)x - \frac{\alpha^2 + \beta^2}{2} x^2 + \frac{\alpha^3 + \beta^3}{3} x^3 - ...$$

Solution Right hand side $= \left[ \alpha x - \frac{\alpha^2 x^2}{2} + \frac{\alpha^3 x^3}{3} - ... \right] + \left[ \beta x - \frac{\beta^2 x^2}{2} + \frac{\beta^3 x^3}{3} - ... \right]$

$= \log_e (1 + \alpha x) + \log (1 + \beta x)$

$= \log_e (1 + (\alpha + \beta)x + \alpha \beta x^2)$

$= \log_e (1 + px + qx^2) =$ Left hand side.

Here, we have used the facts $\alpha + \beta = p$ and $\alpha \beta = q$ . We know this from the
given roots of the quadratic equation. We have also assumed that both $|\alpha x| < 1$ and
$|\beta x| < 1$.

<!-- page 9 -->
MATHEMATICAL MODELLING

A.2.1 Introduction

Much of our progress in the last few centuries has made it necessary to apply
mathematical methods to real-life problems arising from different fields – be it Science,
Finance, Management etc. The use of Mathematics in solving real-world problems
has become widespread especially due to the increasing computational power of digital
computers and computing methods, both of which have facilitated the handling of
lengthy and complicated problems. The process of translation of a real-life problem
into a mathematical form can give a better representation and solution of certain
problems. The process of translation is called Mathematical Modelling.

Here we shall familiaries you with the steps involved in this process through
examples. We shall first talk about what a mathematical model is, then we discuss the
steps involved in the process of modelling.

A.2.2 Preliminaries

Mathematical modelling is an essential tool for understanding the world. In olden days
the Chinese, Egyptians, Indians, Babylonians and Greeks indulged in understanding
and predicting the natural phenomena through their knowledge of mathematics. The
architects, artisans and craftsmen based many of their works of art on geometric
principle.

Suppose a surveyor wants to measure the height of a tower. It is physically very
difficult to measure the height using the measuring tape. So, the other option is to find
out the factors that are useful to find the height. From his knowledge of trigonometry,
he knows that if he has an angle of elevation and the distance of the foot of the tower
to the point where he is standing, then he can calculate the height of the tower.

So, his job is now simplified to find the angle of elevation to the top of the tower
and the distance from the foot of the tower to the point where he is standing. Both of
which are easily measurable. Thus, if he measures the angle of elevation as $40^{\circ}$ and
the distance as $450\text{m}$, then the problem can be solved as given in Example 1.

<!-- page 10 -->
Example 1 The angle of elevation of the top of a tower from a point O on the ground,
which is 450 m away from the foot of the tower, is $40^\circ$. Find the height of the tower.

Solution We shall solve this in different steps.

Step 1 We first try to understand the real problem. In the problem a tower is given and
its height is to be measured. Let $h$ denote the height. It is given that the horizontal
distance of the foot of the tower from a particular point O on the ground is 450 m. Let
$d$ denotes this distance. Then $d = 450\text{m}$. We also know that the angle of elevation,
denoted by $\theta$, is $40^\circ$.

The real problem is to find the height $h$ of the tower using the known distance $d$
and the angle of elevation $\theta$.

Step 2 The three quantities mentioned in the problem are height,
distance and angle of elevation.

So we look for a relation connecting these three quantities.
This is obtained by expressing it geometrically in the following
way (Fig 1).

AB denotes the tower. OA gives the horizontal distance
from the point O to foot of the tower. $\angle$AOB is the angle of
elevation. Then we have

... ...
Fig 1

$$\tan \theta = \frac{h}{d} \text{ or } h = d \tan \theta \quad \dots (1)$$

This is an equation connecting $\theta$, $h$ and $d$.

Step 3 We use Equation (1) to solve $h$. We have $\theta = 40^{\circ}$. and $d = 450\text{m}$. Then we get
$h = \tan 40^{\circ} \times 450 = 450 \times 0.839 = 377.6\text{m}$

Step 4 Thus we got that the height of the tower approximately 378m.

Let us now look at the different steps used in solving the problem. In step 1, we
have studied the real problem and found that the problem involves three parameters
height, distance and angle of elevation. That means in this step we have $studied$ $the$
$real$-$life$ $problem$ $and$ $identified$ $the$ $parameters$.

In the Step 2, we used some geometry and found that the problem can be
represented geometrically as given in Fig 1. Then we used the trigonometric ratio for
the “tangent” function and found the relation as

$$h = d \tan \theta$$

So, in this step we formulated the problem mathematically. That means we found
an equation representing the real problem.

<!-- page 11 -->
In Step 3, we solved the mathematical problem and got that $h = 377.6\text{m}$. That is
we found

Solution of the problem.

In the last step, we interpreted the solution of the problem and stated that the
height of the tower is approximately $378\text{m}$. We call this as

Interpreting the mathematical solution to the real situation

In fact these are the steps mathematicians and others use to study various reallife situations. We shall consider the question, “why is it necessary to use mathematics
to solve different situations.”

Here are some of the examples where mathematics is used effectively to study
various situations.

1. Proper flow of blood is essential to transmit oxygen and other nutrients to various
parts of the body in humanbeings as well as in all other animals. Any constriction
in the blood vessel or any change in the characteristics of blood vessels can
change the flow and cause damages ranging from minor discomfort to sudden
death. The problem is to find the relationship between blood flow and physiological
characteristics of blood vessel.

2. In cricket a third umpire takes decision of a LBW by looking at the trajectory of
a ball, simulated, assuming that the batsman is not there. Mathematical equations
are arrived at, based on the known paths of balls before it hits the batsman's leg.
This simulated model is used to take decision of LBW.

3. Meteorology department makes weather predictions based on mathematical
models. Some of the parameters which affect change in weather conditions are
temperature, air pressure, humidity, wind speed, etc. The instruments are used to
measure these parameters which include thermometers to measure temperature,
barometers to measure airpressure, hygrometers to measure humidity,
anemometers to measure wind speed. Once data are received from many stations
around the country and feed into computers for further analysis and interpretation.

4. Department of Agriculture wants to estimate the yield of rice in India from the
standing crops. Scientists identify areas of rice cultivation and find the average
yield per acre by cutting and weighing crops from some representative fields.
Based on some statistical techniques decisions are made on the average yield of
rice.

How do mathematicians help in solving such problems? They sit with experts in
the area, for example, a physiologist in the first problem and work out a
mathematical equivalent of the problem. This equivalent consists of one or more
equations or inequalities etc. which are called the mathematical models. Then

<!-- page 12 -->
solve the model and interpret the solution in terms of the original problem. Before
we explain the process, we shall discuss what a mathematical model is.

A mathematical model is a representation which comprehends a situation.
An interesting geometric model is illustrated in the following example.

Example 2 (Bridge Problem) Konigsberg is a town on the Pregel River, which in the
18th century was a German
town, but now is Russian. Within
the town are two river islands
that are connected to the banks
with seven bridges as shown
in (Fig 2).
People tried to walk around
the town in a way that only
crossed each bridge once, but it
proved to be difficult problem.
Leonhard Euler, a Swiss
mathematician in the service of
the Russian empire Catherine the Great, heard about the problem. In 1736 Euler proved
that the walk was not possible to do. He proved this by inventing a kind of diagram
called a network, that is made up of vertices
(dots where lines meet) and arcs (lines) (Fig3).

Island C
River Bank B
$\uparrow$
River Bank A
$\rightarrow$
Fig 2
River bank
A

He used four dots (vertices) for the two
river banks and the two islands. These have
been marked A, B and C, D. The seven lines Island C
(arcs) are the seven bridges. You can see that
3 bridges (arcs) join to riverbank, A, and 3 join
to riverbank B. 5 bridges (arcs) join to island
C, and 3 join to island D. This means that all
the vertices have an odd number of arcs, so
they are called odd vertices (An even vertex
would have to have an even number of arcs joining to it).

Fig 3

Remember that the problem was to travel around town crossing each bridge only
once. On Euler’s network this meant tracing over each arc only once, visiting all the
vertices. Euler proved it could not be done because he worked out that, to have an odd
vertex you would have to begin or end the trip at that vertex. (Think about it). Since
there can only be one beginning and one end, there can only be two odd vertices if you
are to trace over each arc only once. Since the bridge problem has 4 odd vertices, it
just not possible to do!

<!-- page 13 -->
After Euler proved his Theorem, much
water has flown under the bridges in Konigsberg.
In 1875, an extra bridge was built in Konigsberg,
joining the land areas of river banks A and B
(Fig 4). Is it possible now for the Konigsbergians
to go round the city, using each bridge only once?

Here the situation will be as in Fig 4. After
the addition of the new edge, both the vertices
A and B have become even degree vertices.
However, D and C still have odd degree. So, it
is possible for the Konigsbergians to go around the city using each bridge exactly once.

River bank
B
Fig 4

The invention of networks began a new theory called graph theory which is now
used in many ways, including planning and mapping railway networks (Fig 4).

A.2.3 What is Mathematical Modelling?

Here, we shall define what mathematical modelling is and illustrate the different
processes involved in this through examples.

Definition Mathematical modelling is an attempt to study some part (or form) of the
real-life problem in mathematical terms.

Conversion of physical situation into mathematics with some suitable
conditions is known as mathematical modelling. Mathematical modelling is
nothing but a technique and the pedagogy taken from fine arts and not from the
basic sciences. Let us now understand the different processes involved in Mathematical
Modelling. Four steps are involved in this process. As an illustrative example, we
consider the modelling done to study the motion of a simple pendulum.

Understanding the problem

This involves, for example, understanding the process involved in the motion of simple
pendulum. All of us are familiar with the simple pendulum. This pendulum is simply a
mass (known as bob) attached to one end of a string whose other end is fixed at a
point. We have studied that the motion of the simple pendulum is periodic. The period
depends upon the length of the string and acceleration due to gravity. So, what we need
to find is the period of oscillation. Based on this, we give a precise statement of the
problem as

Statement How do we find the period of oscillation of the simple pendulum?

The next step is formulation.

Formulation Consists of two main steps.

1. Identifying the relevant factors In this, we find out what are the factors/

<!-- page 14 -->
parameters involved in the problem. For example, in the case of pendulum, the factors
are period of oscillation (T), the mass of the bob ($m$), effective length ($l$) of the pendulum
which is the distance between the point of suspension to the centre of mass of the bob.
Here, we consider the length of string as effective length of the pendulum and acceleration
due to gravity ($g$), which is assumed to be constant at a place.

So, we have identified four parameters for studying the problem. Now, our purpose
is to find T. For this we need to understand what are the parameters that affect the
period which can be done by performing a simple experiment.

We take two metal balls of two different masses and conduct experiment with
each of them attached to two strings of equal lengths. We measure the period of
oscillation. We make the observation that there is no appreciable change of the period
with mass. Now, we perform the same experiment on equal mass of balls but take
strings of different lengths and observe that there is clear dependence of the period on
the length of the pendulum.

This indicates that the mass $m$ is not an $essential$ $parameter$ for finding period
whereas the length $l$ is an essential parameter.

This process of searching the \textbf{essential parameters} is necessary before we go
to the next step.

2. Mathematical description This involves finding an equation, inequality or a
geometric figure using the parameters already identified.

In the case of simple pendulum, experiments were conducted in which the values
of period T were measured for different values of $l$. These values were plotted on a
graph which resulted in a curve that resembled a parabola. It implies that the relation
between T and $l$ could be expressed

$$T^2 = kl \quad \dots (1)$$

It was found that $k = \frac{4\pi^2}{g}$. This gives the equation

$$T = 2\pi \sqrt{\frac{l}{g}} \qquad \dots (2)$$

Equation (2) gives the mathematical formulation of the problem.

Finding the solution The mathematical formulation rarely gives the answer directly.
Usually we have to do some operation which involves solving an equation, calculation
or applying a theorem etc. In the case of simple pendulums the solution involves applying
the formula given in Equation (2).

<!-- page 15 -->
The period of oscillation calculated for two different pendulums having different
lengths is given in Table 1

Table 1

<table>
<tbody>
<tr>
<td>l</td>
<td>225 cm</td>
<td>275cm</td>
</tr>
<tr>
<td>T</td>
<td>3.04 sec</td>
<td>3.36 sec</td>
</tr>
</tbody>
</table>

The table shows that for $l = 225$ cm, T = 3.04 sec and for $l = 275$ cm, T = 3.36 sec.

Interpretation/Validation

A mathematical model is an attempt to study, the essential characteristic of a real life
problem. Many times model equations are obtained by assuming the situation in an
idealised context. The model will be useful only if it explains all the facts that we would
like it to explain. Otherwise, we will reject it, or else, improve it, then test it again. In
other words, \textit{we measure the effectiveness of the model by comparing the results}
\textit{obtained from the mathematical model, with the known facts about the real}
\textit{problem. This process is called validation of the model.} In the case of simple
pendulum, we conduct some experiments on the pendulum and find out period of
oscillation. The results of the experiment are given in Table 2.

Table 2

Periods obtained experimentally for four different pendulums

<table>
<thead>
<tr>
<th>Mass (gms)</th>
<th>Length (cms)</th>
<th>Time (secs)</th>
</tr>
</thead>
<tbody>
<tr>
<td rowspan="2">385</td>
<td>275</td>
<td>3.371</td>
</tr>
<tr>
<td>225</td>
<td>3.056</td>
</tr>
<tr>
<td rowspan="2">230</td>
<td>275</td>
<td>3.352</td>
</tr>
<tr>
<td>225</td>
<td>3.042</td>
</tr>
</tbody>
</table>

Now, we compare the measured values in Table 2 with the calculated values given in
Table 1.

The difference in the observed values and calculated values gives the error. For
example, for $l = 275$ cm, and mass $m = 385$ gm,

$$error = 3.371 - 3.36 = 0.011$$

which is small and the model is accepted.

Once we accept the model, we have to interpret the model. The process of
describing the solution in the context of the real situation is called interpretation
of the model. In this case, we can interpret the solution in the following way:

(a) The period is directly proportional to the square root of the length of the
pendulum.

<!-- page 16 -->
(b) It is inversely proportional to the square root of the acceleration due to gravity.

Our validation and interpretation of this model shows that the mathematical model
is in good agreement with the practical (or observed) values. But we found that there
is some error in the calculated result and measured result. This is because we have
neglected the mass of the string and resistance of the medium. So, in such situation we
look for a better model and this process continues.

This leads us to an important observation. The real world is far too complex to
understand and describe completely. We just pick one or two main factors to be
completely accurate that may influence the situation. Then try to obtain a simplified
model which gives some information about the situation. We study the simple situation
with this model expecting that we can obtain a better model of the situation.

Now, we summarise the main process involved in the modelling as

(a) Formulation (b) Solution (c) Interpretation/Validation

The next example shows how modelling can be done using the techniques of finding
graphical solution of inequality.

Example 3 A farm house uses atleast 800 kg of special food daily. The special food is
a mixture of corn and soyabean with the following compositions

Table 3

<table>
<thead>
<tr>
<th>Material</th>
<th>Nutrients present per Kg<br/>Protein</th>
<th>Nutrients present per Kg<br/>Fibre</th>
<th>Cost per Kg</th>
</tr>
</thead>
<tbody>
<tr>
<td>Corn</td>
<td>.09</td>
<td>.02</td>
<td>Rs 10</td>
</tr>
<tr>
<td>Soyabean</td>
<td>.60</td>
<td>.06</td>
<td>Rs 20</td>
</tr>
</tbody>
</table>

The dietary requirements of the special food stipulate atleast $30\%$ protein and at most
$5\%$ fibre. Determine the daily minimum cost of the food mix.

**Solution Step 1** Here the objective is to minimise the total daily cost of the food which
is made up of corn and soyabean. So the variables (factors) that are to be considered
are
$$x = \text{the amount of corn}$$
$$y = \text{the amount of soyabean}$$
$$z = \text{the cost}$$

Step 2 The last column in Table 3 indicates that $z, x, y$ are related by the equation
$$z = 10x + 20y \qquad \dots (1)$$

The problem is to minimise $z$ with the following constraints:

<!-- page 17 -->
(a) The farm used atleast 800 kg food consisting of corn and soyabean
i.e., $x + y \geq 800$
... (2)

(b) The food should have atleast $30\%$ protein dietary requirement in the proportion
as given in the first column of Table 3. This gives
$$0.09x + 0.6y \geq 0.3 \ (x + y) \quad \dots \ (3)$$

(c) Similarly the food should have atmost $5\%$ fibre in the proportion given in
2nd column of Table 3. This gives

$$0.02x + 0.06 y \leq 0.05 (x + y) \quad \dots (4)$$

We simplify the constraints given in (2), (3) and (4) by grouping all the coefficients
of $x, y$.

Then the problem can be restated in the following mathematical form.
Statement Minimise $z$ subject to

$$x + y \geq 800$$
$$0.21x - .30y \leq 0$$
$$0.03x - .01y \geq 0$$

This gives the formulation of the model.

Step 3 This can be solved graphically. The shaded region in Fig 5 gives the possible
solution of the equations. From the graph it is clear that the minimum value is got at the

Fig 5

point $(470.6,329.4)$ i.e., $x = 470.6$ and $y = 329.4$.
This gives the value of $z$ as $z = 10 \times 470.6 + 20 \times 329.4 = 11294$

<!-- page 18 -->
This is the mathematical solution.

Step 4 The solution can be interpreted as saying that, “The minimum cost of the
special food with corn and soyabean having the required portion of nutrient contents,
protein and fibre is Rs 11294 and we obtain this minimum cost if we use 470.6 kg of
corn and 329.4 kg of soyabean.”

In the next example, we shall discuss how modelling is used to study the population
of a country at a particular time.

Example 4 Suppose a population control unit wants to find out “how many people will
be there in a certain country after 10 years”

Step 1 Formulation We first observe that the population changes with time and it
increases with birth and decreases with deaths.

We want to find the population at a particular time. Let $t$ denote the time in years.
Then $t$ takes values $0, 1, 2, ..., t = 0$ stands for the present time, $t = 1$ stands for the next
year etc. For any time $t$, let $p$ ($t$) denote the population in that particular year.

Suppose we want to find the population in a particular year, say $t_0 = 2006$. How
will we do that. We find the population by Jan. 1st, 2005. Add the number of births in
that year and subtract the number of deaths in that year. Let B($t$) denote the number of
births in the one year between $t$ and $t + 1$ and D($t$) denote the number of deaths
between $t$ and $t + 1$. Then we get the relation

$$\mathrm{P} (t + 1) = \mathrm{P} (t) + \mathrm{B} (t) - \mathrm{D} (t)$$

Now we make some assumptions and definitions

1. $\frac{\text{B}\left(t\right)}{\text{P}\left(t\right)}$ is called the *birth rate* for the time interval $t$ to $t+1$.


2. $\frac{\text{D}\left(\text{t}\right)}{\text{P}\left(\text{t}\right)}$ is called the *death rate* for the time interval $t$ to $t+1$.

Assumptions

1. The birth rate is the same for all intervals. Likewise, the death rate is the same
for all intervals. This means that there is a constant $b$, called the birth rate, and a
constant $d$, called the death rate so that, for all $t \geq 0$,

$$b = \frac{\mathrm{B} (t)}{\mathrm{P} (t)} \quad \text{and} \quad d = \frac{\mathrm{D} (t)}{\mathrm{P} (t)} \qquad \dots (1)$$

2. There is no migration into or out of the population; i.e., the only source of population

<!-- page 19 -->
change is birth and death.

As a result of assumptions 1 and 2, we deduce that, for $t \geq 0$,

$$\begin{aligned} \\ \mathrm{P}(t+1) & =\mathrm{P}(t)+\mathrm{B}(t)-\mathrm{D}(t) \\ \\ & =\mathrm{P}(t)+b \mathrm{P}(t)-d \mathrm{P}(t) \\ \\ & =(1+b-d) \mathrm{P}(t) \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \\ Setting $t = 0$ in (2) gives$$ \mathrm{P}(1) = (1 + b - d)\mathrm{P} (0) \qquad \dots (3) $$Setting $t = 1$ in Equation (2) gives$$ \begin{aligned} \mathrm{P}(2) & = (1 + b - d) \mathrm{P} (1) \\ & = (1 + b - d) (1 + b - d) \mathrm{P} (0) \quad \quad \text{(Using equation 3)} \\ & = (1 + b - d)^2 \mathrm{P}(0) \end{aligned} $$Continuing this way, we get$$ \mathrm{P}(t) = (1 + b - d)^t \mathrm{P} (0) \qquad \dots (4) $$for $t = 0, 1, 2, ...$ The constant $1 + b - d$ is often abbreviated by $r$ and called the $growth$ \\ $rate$ $or$, in more high-flown language, the $Malthusian$ $parameter$, in honor of Robert \\ Malthus who first brought this model to popular attention. In terms of $r$, Equation (4) \\ becomes$$ \mathrm{P}(t) = \mathrm{P}(0)r^t \quad , \quad t = 0, 1, 2, ... \quad ... (5) $$$\mathrm{P}(t)$ is an example of an *exponential function*. Any function of the form $cr^{-1}$, where $c$ \\ and $r$ are constants, is an exponential function. \\ Equation (5) gives the mathematical formulation of the problem. \\ Step 2 – Solution \\ Suppose the current population is 250,000,000 and the rates are $b = 0.02$ and $d = 0.01$. \\ What will the population be in 10 years? Using the formula, we calculate P(10).$$
\begin{aligned}
\mathrm{P}(10) & = (1.01)^{10} (250,000,000) \\
& = (1.104622125) (250,000,000) \\
& = 276,155,531.25
\end{aligned}
$$

Step 3 Interpretation and Validation

Naturally, this result is absurd, since one can’t have $0.25$ of a person.
So, we do some approximation and conclude that the population is $276,155,531$
(approximately). Here, we are not getting the exact answer because of the assumptions
that we have made in our mathematical model.

The above examples show how modelling is done in variety of situations using
different mathematical techniques.

<!-- page 20 -->
Since a mathematical model is a simplified representation of a real problem, by its
very nature, has built-in assumptions and approximations. Obviously, the most important
question is to decide whether our model is a good one or not i.e., when the obtained
results are interpreted physically whether or not the model gives reasonable answers.
If a model is not accurate enough, we try to identify the sources of the shortcomings.
It may happen that we need a new formulation, new mathematical manipulation and
hence a new evaluation. Thus mathematical modelling can be a cycle of the modelling
process as shown in the flowchart given below:

$$- \diamond -$$

<!-- page 21 -->
ANSWERS

EXERCISE 1.1

1. (i), (iv), (v), (vi), (vii) and (viii) are sets.
2. (i) $\in$ (ii) $\notin$ (iii) $\notin$ (vi) $\in$ (v) $\in$ (vi) $\notin$
3. (i) $\mathrm{A} = \{-3, -2, -1, 0, 1, 2, 3, 4, 5, 6\}$ (ii) $\mathrm{B} = \{1, 2, 3, 4, 5\}$
(iii) $\mathrm{C} = \{17, 26, 35, 44, 53, 62, 71, 80\}$ (iv) $\mathrm{D} = \{2, 3, 5\}$
(v) $\mathrm{E} = \{\mathrm{T}, \mathrm{R}, \mathrm{I}, \mathrm{G}, \mathrm{O}, \mathrm{N}, \mathrm{M}, \mathrm{E}, \mathrm{Y}\}$ (vi) $\mathrm{F} = \{\mathrm{B}, \mathrm{E}, \mathrm{T}, \mathrm{R}\}$
4. (i) $\{x : x = 3n, n \in \mathrm{N} \text{ and } 1 \le n \le 4\}$ (ii) $\{x : x = 2^n, n \in \mathrm{N} \text{ and } 1 \le n \le 5\}$
(iii) $\{x : x = 5^n, n \in \mathrm{N} \text{ and } 1 \le n \le 4\}$ (iv) $\{x : x \text{ is an even natural number}\}$
(v) $\{x : x = n^2, n \in \mathrm{N} \text{ and } 1 \le n \le 10\}$
5. (i) $\mathrm{A} = \{1, 3, 5, \dots\}$ (ii) $\mathrm{B} = \{0, 1, 2, 3, 4\}$
(iii) $\mathrm{C} = \{-2, -1, 0, 1, 2\}$ (iv) $\mathrm{D} = \{\mathrm{L}, \mathrm{O}, \mathrm{Y}, \mathrm{A}\}$
(v) $\mathrm{E} = \{\text{ February, April, June, September, November }\}$
(vi) $\mathrm{F} = \{b, c, d, f, g, h, j\}$
6. (i) $\leftrightarrow$ (c) (ii) $\leftrightarrow$ (a) (iii) $\leftrightarrow$ (d) (iv) $\leftrightarrow$ (b)

6. (i) $\leftrightarrow$ (c) (ii) $\leftrightarrow$ (a) (iii) $\leftrightarrow$ (d) (iv) $\leftrightarrow$ (b)

EXERCISE 1.2

1. (i), (iii), (iv)
2. (i) Finite (ii) Infinite (iii) Finite (iv) Infinite (v) Finite
3. (i) Infinite (ii) Finite (iii) Infinite (iv) Finite (v) Infinite
4. (i) Yes (ii) No (iii) Yes (iv) No
5. (i) No (ii) Yes 6. B= D, E = G

EXERCISE 1.3

1. (i) $\subset$ (ii) $\not\subset$ (iii) $\subset$ (iv) $\not\subset$ (v) $\not\subset$ (vi) $\subset$
(vii) $\subset$
2. (i) False (ii) True (iii) False (iv) True (v) False (vi) True
3. (i), (v), (vii), (viii), (ix), (xi)
4. (i) $\phi, \{ a \}$ (ii) $\phi, \{ a \}, \{ b \}, \{ a, b \}$
(iii) $\phi, \{ 1 \}, \{ 2 \}, \{ 3 \}, \{ 1, 2 \}, \{ 1, 3 \}, \{ 2, 3 \}, \{ 1, 2, 3 \}$ (iv) $\phi$
5. 1
6. (i) $(-4, 6]$ (ii) $(-12, -10)$ (iii) $[0, 7)$
(iv) $[3, 4]$
7. (i) $\{ x : x \in \text{R}, -3 < x < 0 \}$ (ii) $\{ x : x \in \text{R}, 6 \le x \le 12 \}$
(iii) $\{ x : x \in \text{R}, 6 < x \le 12 \}$ (iv) $\{ x : x \in \text{R}, -23 \le x < 5 \}$ 9. (iii)

<!-- page 22 -->
EXERCISE 1.4

1. (i) $X \cup Y = \{1, 2, 3, 5\}$ (ii) $A \cup B = \{ a, b, c, e, i, o, u \}$

(iii) $A \cup B = \{x : x = 1, 2, 4, 5 \text{ or a multiple of } 3 \}$

(iv) $A \cup B = \{x : 1 < x < 10, x \in N\}$ (v) $A \cup B = \{1, 2, 3 \}$

2. Yes, $\mathrm{A} \cup \mathrm{B} = \{ a, b, c \}$ 3. $\mathrm{B}$

4. (i) $\{ 1, 2, 3, 4, 5, 6 \}$ (ii) $\{ 1, 2, 3, 4, 5, 6, 7, 8 \}$ (iii) $\{ 3, 4, 5, 6, 7, 8 \}$

(iv) $\{ 3, 4, 5, 6, 7, 8, 9, 10 \}$ (v) $\{ 1, 2, 3, 4, 5, 6, 7, 8 \}$

(vi) $\{ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 \}$ (vii) $\{ 3, 4, 5, 6, 7, 8, 9, 10 \}$

5. (i) $X \cap Y = \{ 1, 3 \}$ (ii) $A \cap B = \{ a \}$ (iii) $\{ 3 \}$ (iv) $\phi$ (v) $\phi$

6. (i) $\{ 7, 9, 11 \}$ (ii) $\{ 11, 13 \}$ (iii) $\phi$ (iv) $\{ 11 \}$

(v) $\phi$ (vi) $\{ 7, 9, 11 \}$ (vii) $\phi$

(viii) $\{ 7, 9, 11 \}$ (ix) $\{ 7, 9, 11 \}$ (x) $\{ 7, 9, 11, 15 \}$

7. (i) B (ii) C (iii) D (iv) $\phi$
(v) $\{ 2 \}$ (vi) $\{ x : x \text{ is an odd prime number } \}$ 8. (iii)

9. (i) $\{3, 6, 9, 15, 18, 21\}$ (ii) $\{3, 9, 15, 18, 21\}$ (iii) $\{3, 6, 9, 12, 18, 21\}$
(iv) $\{4, 8, 16, 20\}$ (v) $\{2, 4, 8, 10, 14, 16\}$ (vi) $\{5, 10, 20\}$
(vii) $\{20\}$ (viii) $\{4, 8, 12, 16\}$ (ix) $\{2, 6, 10, 14\}$
(x) $\{5, 10, 15\}$ (xi) $\{2, 4, 6, 8, 12, 14, 16\}$ (xii) $\{5, 15, 20\}$

10. (i) $\{ a, c \}$ (ii) $\{ f, g \}$ (iii) $\{ b, d \}$
11. Set of irrational numbers 12. (i) F (ii) F (iii) T (iv) T

EXERCISE 1.5

1. (i) $\{ 5, 6, 7, 8, 9 \}$ (ii) $\{ 1, 3, 5, 7, 9 \}$ (iii) $\{ 7, 8, 9 \}$
(iv) $\{ 5, 7, 9 \}$ (v) $\{ 1, 2, 3, 4 \}$ (vi) $\{ 1, 3, 4, 5, 6, 7, 9 \}$
2. (i) $\{ d, e, f, g, h \}$ (ii) $\{ a, b, c, h \}$ (iii) $\{ b, d, f, h \}$
(iv) $\{ b, c, d, e )$
3. (i) $\{ x : x \text{ is an odd natural number } \}$
(ii) $\{ x : x \text{ is an even natural number } \}$
(iii) $\{ x : x \in \mathbf{N} \text{ and } x \text{ is not a multiple of } 3 \}$
(iv) $\{ x : x \text{ is a positive composite number or } x = 1 ]$

<!-- page 23 -->
(v) $\{ x : x \text{ is a positive integer which is not divisible by 3 or not divisible by 5} \}$
(vi) $\{ x : x \in \mathbf{N} \text{ and } x \text{ is not a perfect square } \}$
(vii) $\{ x : x \in \mathbf{N} \text{ and } x \text{ is not a perfect cube } \}$
(viii) $\{ x : x \in \mathbf{N} \text{ and } x \neq 3 \}$                                     (ix) $\{ x : x \in \mathbf{N} \text{ and } x \neq 2 \}$

(x) $\{ x : x \in \mathbf{N} \text{ and } x < 7 \}$                                     (xi) $\{ x : x \in \mathbf{N} \text{ and } x \leq \frac{9}{2} \}$

6. A' is the set of all equilateral triangles.

7. (i) U (ii) A (iii) $\phi$ (iv) $\phi$

EXERCISE 1.6

1. 2
2. 5
3. 50
4. 42
5. 30
6. 19
7. 25, 35
8. 60

Miscellaneous Exercise on Chapter 1

1. $A \subset B$, $A \subset C$, $B \subset C$, $D \subset A$, $D \subset B$, $D \subset C$
2. (i) False (ii) False (iii) True (iv) False (v) False
(vi) True
7. False 12. We may take $A = \{ 1, 2 \}$, $B = \{ 1, 3 \}$, $C = \{ 2, 3 \}$
13. 325 14. 125 15. (i) 52, (ii) 30 16. 11

EXERCISE 2.1

1. $x = 2$ and $y = 1$ 2. The number of elements in A $\times$ B is 9.
3. G $\times$ H = $\{(7, 5), (7, 4), (7, 2), (8, 5), (8, 4), (8, 2)\}$
H $\times$ G = $\{(5, 7), (5, 8), (4, 7), (4, 8), (2, 7), (2, 8)\}$
4. (i) False
P $\times$ Q = $\{(m, n), (m, m), (n, n), (n, m)\}$
(ii) True
(iii) True
5. A $\times$ A = $\{(-1, -1), (-1, 1), (1, -1), (1, 1)\}$
A $\times$ A $\times$ A = $\{(-1, -1, -1), (-1, -1, 1), (-1, 1, -1), (-1, 1, 1), (1, -1, -1), (1, -1, 1),$
$(1, 1, -1), (1, 1, 1)\}$
6. A = $\{a, b\}$, B = $\{x, y\}$
8. A $\times$ B = $\{(1, 3), (1, 4), (2, 3), (2, 4)\}$
A $\times$ B will have $2^4 = 16$ subsets.
9. A = $\{x, y, z\}$ and B = $\{1, 2\}$

<!-- page 24 -->
10. $A = \{-1, 0, 1\}$, remaining elements of
$A \times A$ are $(-1, -1), (-1, 1), (0, -1), (0, 0), (1, -1), (1, 0), (1, 1)$

EXERCISE 2.2

1. $R = \{(1, 3), (2, 6), (3, 9), (4, 12)\}$
Domain of $R = \{1, 2, 3, 4\}$
Range of $R = \{3, 6, 9, 12\}$
Co domain of $R = \{1, 2, ..., 14\}$

2. $R = \{(1, 6), (2, 7), (3, 8)\}$
Domain of $R = \{1, 2, 3\}$
Range of $R = \{6, 7, 8\}$

3. $R = \{(1, 4), (1, 6), (2, 9), (3, 4), (3, 6), (5, 4), (5, 6)\}$

4. (i) $R = \{(x, y) : y = x - 2 \text{ for } x = 5, 6, 7\}$
(ii) $R = \{(5,3), (6,4), (7,5)\}$. Domain of $R = \{5, 6, 7\}$, Range of $R = \{3, 4, 5\}$

5. (i) $R = \{(1, 1), (1,2), (1, 3), (1, 4), (1, 6), (2, 4), (2, 6), (2, 2), (4, 4), (6, 6),$
$(3, 3), (3, 6)\}$
(ii) Domain of $R = \{1, 2, 3, 4, 6\}$
(iii) Range of $R = \{1, 2, 3, 4, 6\}$

6. Domain of $R = \{0, 1, 2, 3, 4, 5\}$
Range of $R = \{5, 6, 7, 8, 9, 10\}$

7. $R = \{(2, 8), (3, 27), (5, 125), (7, 343)\}$
No. of relations from A into $B = 2^6$
9. Domain of $R = \mathbf{Z}$
Range of $R = \mathbf{Z}$

EXERCISE 2.3

1. (i) yes, Domain = $\{2, 5, 8, 11, 14, 17\}$, Range = $\{1\}$
(ii) yes, Domain = $(2, 4, 6, 8, 10, 12, 14)$, Range = $\{1, 2, 3, 4, 5, 6, 7\}$
(iii) No.
2. (i) Domain = $\mathbf{R}$, Range = $(-\infty, 0]$
(ii) Domain of function = $\{x : -3 \le x \le 3\}$
Range of function = $\{x : 0 \le x \le 3\}$
3. (i) $f(0) = -5$ (ii) $f(7) = 9$ (iii) $f(-3) = -11$
4. (i) $t(0) = 32$ (ii) $t(28) = \frac{412}{5}$ (iii) $t(-10) = 14$ (iv) 100
5. (i) Range = $(-\infty, 2)$ (ii) Range = $[2, \infty)$ (iii) Range = $\mathbf{R}$

<!-- page 25 -->
Miscellaneous Exercise on Chapter 2

2. $2.1$
3. Domain of function is set of real numbers except 6 and 2.
4. Domain $= [1, \infty)$, Range $= [0, \infty)$
5. Domain = $\mathbf{R}$, Range = non-negative real numbers
6. Range $= (0, 1)$
7. $(f + g) x = 3x - 2$
$(f - g) x = -x + 4$
$\left( \frac{f}{g} \right) x = \frac{x + 1}{2x - 3}$, $x \neq \frac{3}{2}$
9. (i) No
(ii) No
(iii) No

10. (i) Yes, (ii) No      11. No      12. Range of $f = \{3, 5, 11, 13\}$

EXERCISE 3.1

1. (i) $\frac{5\pi}{36}$ (ii) $-\frac{19\pi}{72}$ (iii) $\frac{4\pi}{3}$ (iv) $\frac{26\pi}{9}$

2. (i) $39^{\circ} 22' 30''$ (ii) $-229^{\circ} 5' 27''$ (iii) $300^{\circ}$ (iv) $210^{\circ}$

3. $12\pi$          4. $12^\circ 36'$          5. $\frac{20\pi}{3}$          6. $5:4$

7. (i) $\frac{2}{15}$ (ii) $\frac{1}{5}$ (iii) $\frac{7}{25}$

EXERCISE 3.2

1. $\sin x = -\frac{\sqrt{3}}{2}$, $\text{cosec } x = -\frac{2}{\sqrt{3}}$, $\sec x = -2$, $\tan x = \sqrt{3}$, $\cot x = \frac{1}{\sqrt{3}}$


2. $\text{cosec } x = \frac{5}{3}$, $\cos x = -\frac{4}{5}$, $\sec x = -\frac{5}{4}$, $\tan x = -\frac{3}{4}$, $\cot x = -\frac{4}{3}$


3. $\sin x = -\frac{4}{5}$, $\text{cosec } x = -\frac{5}{4}$, $\cos x = -\frac{3}{5}$, $\sec x = -\frac{5}{3}$, $\tan x = \frac{4}{3}$


4. $\sin x = -\frac{12}{13}$, $\text{cosec } x = -\frac{13}{12}$, $\cos x = \frac{5}{13}$, $\tan x = -\frac{12}{5}$, $\cot x = -\frac{5}{12}$

<!-- page 26 -->
5. $\sin x = \frac{5}{13}$, $\csc x = \frac{13}{5}$, $\cos x = -\frac{12}{13}$, $\sec x = -\frac{13}{12}$, $\cot x = -\frac{12}{5}$

6. $\frac{1}{\sqrt{2}}$ 7. 2 8. $\sqrt{3}$ 9. $\frac{\sqrt{3}}{2}$ 10. 1

EXERCISE 3.3

5. (i) $\frac{\sqrt{3}+1}{2\sqrt{2}}$ (ii) $2-\sqrt{3}$

EXERCISE 3.4

1. $\frac{\pi}{3}, \frac{4\pi}{3}, n\pi + \frac{\pi}{3}, n \in \mathbf{Z}$
2. $\frac{\pi}{3}, \frac{5\pi}{3}, 2n\pi \pm \frac{\pi}{3}, n \in \mathbf{Z}$
3. $\frac{5\pi}{6}, \frac{11\pi}{6}, n\pi + \frac{5\pi}{6}, n \in \mathbf{Z}$
4. $\frac{7\pi}{6}, \frac{11\pi}{6}, n\pi + (-1)^n \frac{7\pi}{6}, n \in \mathbf{Z}$
5. $x = \frac{n\pi}{3}$ or $x = n\pi, n \in \mathbf{Z}$
6. $x = (2n+1)\frac{\pi}{4}$, or $2n\pi \pm \frac{\pi}{3}, n \in \mathbf{Z}$
7. $x = n\pi + (-1)^n \frac{7\pi}{6}$ or $(2n+1)\frac{\pi}{2}, n \in \mathbf{Z}$
8. $x = \frac{n\pi}{2}$, or $\frac{n\pi}{2} + \frac{3\pi}{8}, n \in \mathbf{Z}$
9. $x = \frac{n\pi}{3}$, or $n\pi \pm \frac{\pi}{3}, n \in \mathbf{Z}$

Miscellaneous Exercise on Chapter 3

8. $\frac{2\sqrt{5}}{5}, \frac{\sqrt{5}}{5}, \frac{1}{2}$

9. $\frac{\sqrt{6}}{3}, -\frac{\sqrt{3}}{3}, -\sqrt{2}$

10. $\frac{\sqrt{8+2\sqrt{15}}}{4}, \frac{\sqrt{8-2\sqrt{15}}}{4}, 4+\sqrt{15}$

<!-- page 27 -->
EXERCISE 5.1

1. $3$
2. $0$
3. $i$
4. $14+28 i$

5. $2-7 i$
6. $-\frac{19}{5}-\frac{21i}{10}$
7. $\frac{17}{3}+i\frac{5}{3}$
8. $-4$

9. $-\frac{242}{27}-26i$
10. $\frac{-22}{3}-i\frac{107}{27}$
11. $\frac{4}{25}+i\frac{3}{25}$
12. $\frac{\sqrt{5}}{14}-i\frac{3}{14}$

13. $i$
14. $\frac{-7\sqrt{2}}{2} i$

13. $i$          14. $\frac{-7\sqrt{2}}{2}i$

EXERCISE 5.2

1. $2, \frac{-2\pi}{3}$
2. $2, \frac{5\pi}{6}$
3. $\sqrt{2}\left(\cos \frac{-\pi}{4} + i \sin \frac{-\pi}{4}\right)$


4. $\sqrt{2}\left(\cos \frac{3\pi}{4} + i \sin \frac{3\pi}{4}\right)$
5. $\sqrt{2}\left(\cos \frac{-3\pi}{4} + i \sin \frac{-3\pi}{4}\right)$


6. $3 (\cos \pi + i \sin \pi)$
7. $2\left(\cos \frac{\pi}{6} + i \sin \frac{\pi}{6}\right)$
8. $\cos \frac{\pi}{2} + i \sin \frac{\pi}{2}$

EXERCISE 5.3

1. $\pm\sqrt{3}i$ 2. $\frac{-1\pm\sqrt{7}i}{4}$ 3. $\frac{-3\pm3\sqrt{3}i}{2}$ 4. $\frac{-1\pm\sqrt{7}i}{-2}$

5. $\frac{-3\pm\sqrt{11}i}{2}$ 6. $\frac{1\pm\sqrt{7}i}{2}$ 7. $\frac{-1\pm\sqrt{7}i}{2\sqrt{2}}$ 8. $\frac{\sqrt{2}\pm\sqrt{34}i}{2\sqrt{3}}$

9. $\frac{-1\pm\sqrt{(2\sqrt{2}-1)i}}{2}$ 10. $\frac{-1\pm\sqrt{7}i}{2\sqrt{2}}$

<!-- page 28 -->
Miscellaneous Exercise on Chapter 5

1. $2-2i$          3. $\frac{307+599i}{442}$

5. (i) $\sqrt{2}\left(\cos \frac{3 \pi}{4}+i \sin \frac{3 \pi}{4}\right)$, (ii) $\sqrt{2}\left(\cos \frac{3 \pi}{4}+i \sin \frac{3 \pi}{4}\right)$

6. $\frac{2}{3} \pm \frac{4}{3} i$     7. $1 \pm \frac{\sqrt{2}}{2} i$     8. $\frac{5}{27} \pm \frac{\sqrt{2}}{27} i$     9. $\frac{2}{3} \pm \frac{\sqrt{14}}{21} i$

10. $\sqrt{2}$ 12. (i) $\frac{-2}{5}$, (ii) 0 13. $\frac{1}{\sqrt{2}}$, $\frac{3\pi}{4}$ 14. $x=3$, $y=-3$

15. 2 17. 1 18. 0 20. 4

EXERCISE 6.1

1. (i) $\{1, 2, 3, 4\}$                                (ii) $\{... -3, -2, -1, 0, 1, 2, 3, 4, \}$

2. (i) No Solution                                     (ii) $\{... -4, -3\}$

3. (i) $\{... -2, -1, 0, 1\}$                                (ii) $(-\infty, 2)$

4. (i) $\{-1, 0, 1, 2, 3, ...\}$                                (ii) $(-2, \infty)$

5. $(-4, \infty)$               6. $(-\infty, -3)$               7. $(-\infty, -3]$               8. $(-\infty, 4]$

9. $(-\infty, 6)$               10. $(-\infty, -6)$               11. $(-\infty, 2]$               12. $(-\infty, 120]$

13. $(4, \infty)$               14. $(-\infty, 2]$               15. $(4, \infty)$               16. $(-\infty, 2]$

17. $x < 3$, $\xleftarrow{x < 3}$               18. $x \ge -1$, $\xleftarrow{x \ge -1}$

                                      0 1 2 3 4               -1 0 1

19. $x > -1$, $\xleftarrow{x > -1}$               20. $x \ge -\frac{2}{7}$, $\xleftarrow{-1 0 1}$

                                      -2-1 0 1 2

21. Greater than or equal to 35                                 22. Greater than or equal to 82

23. $(5,7), (7,9)$                                           24. $(6,8), (8,10), (10,12)$

25. 9 cm                                         26. Greater than or equal to 8 but less than or equal to 22

<!-- page 29 -->
EXERCISE 6.2

1.

2.

3.

4.

5.

6.

<!-- page 30 -->
442 MATHEMATICS

7.

8.

$$9.$$

10.

EXERCISE 6.3

1.

2.

<!-- page 31 -->
3.

4.

5.

6.

7.

8.

<!-- page 32 -->
444 MATHEMATICS

$$9.$$

10.

11.

12.

13.

14.

<!-- page 33 -->
15.

Miscellaneous Exercise on Chapter 6

1. $[2, 3]$
2. $(0, 1]$
3. $[-4, 2]$

4. $(-23, 2]$
5. $\left[ \frac{-80}{3}, \frac{-10}{3} \right]$
6. $\left[ 1, \frac{11}{3} \right]$

7. $(-5, 5)$

$$(-5, 5)$$

$$(-1, 7)$$

8. $(-1, 7)$

$$(5, \infty)$$

9. $(5, \infty)$

10. $[-7, 11]$

11. Between $20^\circ\text{C}$ and $25^\circ\text{C}$

12. More than 320 litres but less than 1280 litres.

13. More than 562.5 litres but less than 900 litres.

14. $9.6 \le \text{MA} \le 16.8$

EXERCISE 7.1

1. (i) 125, (ii) 60.
2. 108
3. 5040
4. 336
5. 8
6. 20

<!-- page 34 -->
EXERCISE 7.2

1. (i) 40320, (ii) 18
2. 30, No
3. 28
4. 64
5. (i) 30, (ii) 15120

EXERCISE 7.3

1. 504

2. 4536

3. 60

4. $120, 48$

5. 56          6. 9          7. (i) 3, (ii) 4          8. 40320

10. 33810

11. (i) 1814400, (ii) 2419200, (iii) 25401600

EXERCISE 7.4

1. 45
5. 2000
9. 35

2. (i) 5, (ii) 6
6. 778320

3. 210
7. 3960

4. 40
8. 200

9. 35

Miscellaneous Exercise on Chapter 7

**1.** 3600                                **2.** 1440                                **3.** (i) 504, (ii) 588, (iii) 1632
**4.** 907200                                **5.** 120                                **6.** 50400                                **7.** 420
**8.** $^4\text{C}_1 \times ^{48}\text{C}_4$                      **9.** 2880                               **10.** $^{22}\text{C}_7 + ^{22}\text{C}_{10}$                      **11.** 151200

EXERCISE 8.1

1. $1-10x + 40x^2 - 80x^3 + 80x^4 - 32x^5$


2. $\frac{32}{x^5} - \frac{40}{x^3} + \frac{20}{x} - 5x + \frac{5}{8}x^3 - \frac{x^5}{32}$


3. $64x^6 - 576x^5 + 2160x^4 - 4320x^3 + 4860x^2 - 2916x + 729$


4. $\frac{x^5}{243} + \frac{5x^3}{81} + \frac{10}{27}x + \frac{10}{9x} + \frac{5}{3x^3} + \frac{1}{x^5}$


5. $x^6 + 6x^4 + 15x^2 + 20 + \frac{15}{x^2} + \frac{6}{x^4} + \frac{1}{x^6}$


6. 884736                                   7. 11040808032                                   8. 104060401


9. 9509900499                                  10. $(1.1)^{10000} > 1000$                                11. $8(a^3b + ab^3); 40\sqrt{6}$


12. $2(x^6 + 15x^4 + 15x^2 + 1), 198$

12. $2(x^6 + 15x^4 + 15x^2 + 1)$, 198

<!-- page 35 -->
EXERCISE 8.2

1. 1512
2. $-101376$
3. $(-1)^r \ ^6\text{C}_r \cdot x^{12-2r} \cdot y^r$

4. $(-1)^r \ ^{12}\text{C}_r \cdot x^{24-r} \cdot y^r$
5. $-1760 \ x^9 y^3$
6. 18564

7. $\frac{-105}{8} x^9 ; \frac{35}{48} x^{12}$
8. $61236 \ x^5 y^5$
10. $n=7 ; \ r=3$

12. $m=4$

Miscellaneous Exercise on Chapter 8

1. $a=3; b=5; n=6$
2. $a=\frac{9}{7}$
3. 171

5. $396\sqrt{6}$
6. $2a^8 + 12a^6 - 10a^4 - 4a^2 + 2$
7. 0.9510
8. $n=10$

9. $\frac{16}{x} + \frac{8}{x^2} - \frac{32}{x^3} + \frac{16}{x^4} - 4x + \frac{x^2}{2} + \frac{x^3}{2} + \frac{x^4}{16} - 5$
10. $27x^6 - 54ax^5 + 117a^2x^4 - 116a^3x^3 + 117a^4x^2 - 54a^5x + 27a^6$

EXERCISE 9.1

2. $\frac{1}{2}, \frac{2}{3}, \frac{3}{4}, \frac{4}{5}, \frac{5}{6}$

1. $3, 8, 15, 24, 35$
2. $\frac{1}{2}, \frac{2}{3}, \frac{3}{4}, \frac{4}{5}, \frac{5}{6}$
3. $2, 4, 8, 16$ and $32$

4. $-\frac{1}{6}, \frac{1}{6}, \frac{1}{2}, \frac{5}{6}, \frac{7}{6}$
5. $25, -125, 625, -3125, 15625$

6. $\frac{3}{2}, \frac{9}{2}, \frac{21}{2}, 21$ and $\frac{75}{2}$
7. $65, 93$
8. $\frac{49}{128}$

9. $729$
10. $\frac{360}{23}$

11. $3, 11, 35, 107, 323;$ $3 + 11 + 35 + 107 + 323 + ...$

12. $-1, \frac{-1}{2}, \frac{-1}{6}, \frac{-1}{24}, \frac{-1}{120}; -1 + \left(\frac{-1}{2}\right) + \left(\frac{-1}{6}\right) + \left(\frac{-1}{24}\right) + \left(\frac{-1}{120}\right) + ...$

<!-- page 36 -->
13. $2, 2, 1, 0, -1;$ $2 + 2 + 1 + 0 + (-1) + ...$ 14. $1, 2, \frac{3}{2}, \frac{5}{3}$ and $\frac{8}{5}$

EXERCISE 9.2

1. 1002001
2. 98450
4. 5 or 20
6. 4

7. $\frac{n}{2}(5n+7)$
8. $2q$
9. $\frac{179}{321}$
10. 0

13. 27
14. 11, 14, 17, 20 and 23
15. 1
16. 14
17. Rs 245
18. 9

EXERCISE 9.3

1. $\frac{5}{2^{20}}, \frac{5}{2^n}$     2. 3072     4. $-2187$

5. (a) $13^{\text{th}}$, (b) $12^{\text{th}}$, (c) $9^{\text{th}}$      6. $\pm 1$      7. $\frac{1}{6}\left[1-(0.1)^{20}\right]$

8. $\frac{\sqrt{7}}{2}(\sqrt{3}+1)\left(3^{\frac{n}{2}}-1\right)$

9. $\frac{\left[1-(-a)^{n}\right]}{1+a}$

10. $\frac{x^3(1-x^{2n})}{1-x^2}$

11. $22+\frac{3}{2}(3^{11}-1)$

12. $r=\frac{5}{2}$ or $\frac{2}{5}$; Terms are $\frac{2}{5}, 1, \frac{5}{2}$ or $\frac{5}{2}, 1, \frac{2}{5}$

13. 4          14. $\frac{16}{7};2;\frac{16}{7}(2^n-1)$

15. 2059

16. $\frac{-4}{3}, \frac{-8}{3}, \frac{-16}{3}, ... \text{ or } 4, -8, 16, -32, 64, ..$
18. $\frac{80}{81}(10^n - 1) - \frac{8}{9}n$

19. 496 20. $r\text{R}$ 21. 3, $-6, 12, -24$ 26. 9 and 27

27. $n=\frac{-1}{2}$

30. 120, 480, 30 ($2^n$)

31. Rs 500 (1.1)$^{10}$

32. $x^2 - 16x + 25 = 0$

EXERCISE 9.4

1. $\frac{n}{3}(n+1)(n+2)$ 2. $\frac{n(n+1)(n+2)(n+3)}{4}$

<!-- page 37 -->
3. $\frac{n}{6}(n+1)(3n^2+5n+1)$      4. $\frac{n}{n+1}$      5. 2840

6. $3n (n + 1) (n + 3)$

$$7. \quad \frac{n(n+1)^2(n+2)}{12}$$

8. $\frac{n(n+1)}{12}(3n^2 + 23n + 34)$

9. $\frac{n}{6}(n+1)(2n+1)+2\left(2^n-1\right)$ 10. $\frac{n}{3}(2n+1)(2n-1)$

Miscellaneous Exercise on Chapter 9

4. 8729

$$5. 3050$$

6. 1210

9. $\pm 3$

10. $8, 16, 32$

11. 4

12. 11

21. (i) $\frac{50}{81}(10^n-1)-\frac{5n}{9}$ , (ii) $\frac{2n}{3}-\frac{2}{27}(1-10^{-n})$ 22. 1680

23. $\frac{n}{3}(n^2+3n+5)$

25. $\frac{n}{24}(2n^2+9n+13)$

27. Rs 16680

28. Rs 39100

29. Rs 43690

30. Rs 17000; 20,000

31. Rs 5120    32. 25 days

EXERCISE 10.1

1. $\frac{121}{2}$ square unit.

2. $(0, a), (0, -a)$ and $(-\sqrt{3}a, 0)$ or $(0, a), (0, -a)$, and $(\sqrt{3}a, 0)$

3. (i) $|y_2 - y_1|$, (ii) $|x_2 - x_1|$          4. $\left(\frac{15}{2}, 0\right)$          5. $-\frac{1}{2}$

7. $-\sqrt{3}$

8. $x=1$

10. $135^\circ$

11. 1 and 2, or $\frac{1}{2}$ and 1, or $-1$ and $-2$, or $-\frac{1}{2}$ and $-1$    14. $\frac{1}{2}$, 104.5 Crores

<!-- page 38 -->
EXERCISE 10.2

1. $y=0$ and $x=0$
2. $x-2y+10=0$
3. $y=mx$
4. $(\sqrt{3}+1)x-(\sqrt{3}-1)y=4(\sqrt{3}-1)$
5. $2x+y+6=0$
6. $x-\sqrt{3}y+2\sqrt{3}=0$
7. $5x+3y+2=0$
8. $\sqrt{3}x+y=10$
9. $3x-4y+8=0$
10. $5x-y+20=0$
11. $(1+n)x+3(1+n)y=n+11$
12. $x+y=5$
13. $x+2y-6=0$, $2x+y-6=0$
14. $\sqrt{3}x+y-2=0$ and $\sqrt{3}x+y+2=0$
15. $2x-9y+85=0$
16. $L=\frac{.192}{90}(C-20)+124.942$
17. 1340 litres.
19. $2kx+hy=3kh$.

16. $L = \frac{.192}{90}(C-20)+124.942$    17. 1340 litres.    19. $2kx + hy = 3kh.$

EXERCISE 10.3

1. (i) $y=-\frac{1}{7}x+0, -\frac{1}{7}, 0$; (ii) $y=-2x+\frac{5}{3}, -2, \frac{5}{3}$; (iii) $y=0x+0, 0, 0$


2. (i) $\frac{x}{4}+\frac{y}{6}=1,4,6$; (ii) $\frac{x}{3}+\frac{y}{-2}=1,\frac{3}{2},-2$;


(iii) $y=-\frac{2}{3}$, intercept with y-axis $= -\frac{2}{3}$ and no intercept with $x$-axis.


3. (i) $x \cos 120^{\circ} + y \sin 120^{\circ} = 4, 4, 120^{\circ}$ (ii) $x \cos 90^{\circ} + y \sin 90^{\circ} = 2, 2, 90^{\circ}$;


(iii) $x \cos 315^{\circ} + y \sin 315^{\circ} = 2\sqrt{2}, 2\sqrt{2}, 315^{\circ}$ 4. 5 units


5. $(-2, 0)$ and $(8, 0)$ 6. (i) $\frac{65}{17}$ units, (ii) $\frac{1}{\sqrt{2}} \left| \frac{p+r}{l} \right|$ units.


7. $3x - 4y + 18 = 0$ 8. $y + 7x = 21$ 9. $30^{\circ}$ and $150^{\circ}$


10. $\frac{22}{9}$


12. $(\sqrt{3}+2)x + (2\sqrt{3}-1)y = 8\sqrt{3}+1$ or $(\sqrt{3}-2)x + (1+2\sqrt{3})y = -1+8\sqrt{3}$

<!-- page 39 -->
13. $2x + y = 5$

14. $\left(\frac{68}{25}, -\frac{49}{25}\right)$

15. $m=\frac{1}{2}, c=\frac{5}{2}$

17. $y - x = 1$, $\sqrt{2}$

Miscellaneous Exercise on Chapter 10

1. (a) $3$, (b) $\pm 2$, (c) $6$ or $1$

2. $\frac{7\pi}{6}, 1$

3. $2x - 3y = 6, -3x + 2y = 6$

4. $\left(0,-\frac{8}{3}\right),\left(0,\frac{32}{3}\right)$

$$\mathbf{5.} \quad \frac{|\sin (\phi - \theta)|}{2 \left| \sin \frac{\phi - \theta}{2} \right|}$$

6. $x=-\frac{5}{22}$

7. $2x - 3y + 18 = 0$

8. $k^2$ square units

$$9. 5$$

11. $3x - y = 7, \quad x + 3y = 9$

12. $13x + 13y = 6$

$$14. 1 : 2$$

15. $\frac{23\sqrt{5}}{18}$ units

16. The line is parallel to $x$ - axis or parallel to $y$-axis

17. $x=1, \quad y=1.$

18. $(-1, -4)$.

19. $\frac{1 \pm 5\sqrt{2}}{7}$

21. $18x + 12y + 11 = 0$

22. $\left(\frac{13}{5}, 0\right)$

24. $119x + 102y = 125$

EXERCISE 11.1

1. $x^2 + y^2 - 4y = 0$
2. $x^2 + y^2 + 4x - 6y - 3 = 0$
3. $36x^2 + 36y^2 - 36x - 18y + 11 = 0$
4. $x^2 + y^2 - 2x - 2y = 0$
5. $x^2 + y^2 + 2ax + 2by + 2b^2 = 0$
6. $c(-5, 3), r = 6$

7. $c(2, 4), r = \sqrt{65}$
8. $c(4, -5), r = \sqrt{53}$
9. $c \left( \frac{1}{4}, 0 \right); r = \frac{1}{4}$

10. $x^2 + y^2 - 6x - 8y + 15 = 0$
11. $x^2 + y^2 - 7x + 5y - 14 = 0$
12. $x^2 + y^2 + 4x - 21 = 0$ & $x^2 + y^2 - 12x + 11 = 0$

<!-- page 40 -->
13. $x^2 + y^2 - ax - by = 0$
14. $x^2 + y^2 - 4x - 4y = 5$
15. Inside the circle; since the distance of the point to the centre of the circle is less
than the radius of the circle.

EXERCISE 11.2

1. F $(3, 0)$, axis - $x$ - axis, directrix $x = -3$, length of the Latus rectum $= 12$


2. F $(0, \frac{3}{2})$, axis - $y$ - axis, directrix $y = -\frac{3}{2}$, length of the Latus rectum $= 6$


3. F $(-2, 0)$, axis - $x$ - axis, directrix $x = 2$, length of the Latus rectum $= 8$


4. F $(0, -4)$, axis - $y$ - axis, directrix $y = 4$, length of the Latus rectum $= 16$


5. F $(\frac{5}{2}, 0)$ axis - $x$ - axis, directrix $x = -\frac{5}{2}$, length of the Latus rectum $= 10$


6. F $(0, \frac{-9}{4})$, axis - $y$ - axis, directrix $y = \frac{9}{4}$, length of the Latus rectum $= 9$


7. $y^2 = 24x$ 8. $x^2 = -12y$ 9. $y^2 = 12x$


10. $y^2 = -8x$ 11. $2y^2 = 9x$ 12. $2x^2 = 25y$

EXERCISE 11.3

1. F ($\pm\sqrt{20}$ ,0); V ($\pm$ 6, 0); Major axis = 12; Minor axis = 8 , $e$ = $\frac{\sqrt{20}}{6}$ ,


Latus rectum = $\frac{16}{3}$


2. F (0, $\pm\sqrt{21}$ ); V (0, $\pm$ 5); Major axis = 10; Minor axis = 4 , $e$ = $\frac{\sqrt{21}}{5}$ ;


Latus rectum = $\frac{8}{5}$


3. F ($\pm\sqrt{7}$ , 0); V ($\pm$ 4, 0); Major axis = 8; Minor axis = 6 , $e$ = $\frac{\sqrt{7}}{4}$ ;


Latus rectum = $\frac{9}{2}$

<!-- page 41 -->
4. F $(0, \pm \sqrt{75})$; V $(0, \pm 10)$; Major axis $= 20$; Minor axis $= 10$ , $e = \frac{\sqrt{3}}{2}$ ;
Latus rectum $= 5$

5. F ($\pm\sqrt{13}$ ,0); V ($\pm$ 7, 0); Major axis =14 ; Minor axis = 12 , $e$ = $\frac{\sqrt{13}}{7}$ ;

Latus rectum = $\frac{72}{7}$

6. F $(0, \pm 10\sqrt{3})$ ; V $(0, \pm 20)$; Major axis $=40$ ; Minor axis $= 20$ , $e = \frac{\sqrt{3}}{2}$ ;
Latus rectum $= 10$

7. F $(0, \pm 4\sqrt{2})$; V $(0,\pm 6)$; Major axis $=12$ ; Minor axis $= 4$ , $e = \frac{2\sqrt{2}}{3}$ ;

Latus rectum $=\frac{4}{3}$

8. $F(0,\pm\sqrt{15})$; $V$ $(0,\pm 4)$; Major axis $= 8$ ; Minor axis $= 2$ , $e = \frac{\sqrt{15}}{4}$ ;

Latus rectum $= \frac{1}{2}$

9. F ($\pm \sqrt{5}$ ,0); V ($\pm$ 3, 0); Major axis = 6 ; Minor axis = 4 , $e = \frac{\sqrt{5}}{3}$ ;

Latus rectum = $\frac{8}{3}$

10. $\frac{x^2}{25} + \frac{y^2}{9} = 1$
11. $\frac{x^2}{144} + \frac{y^2}{169} = 1$
12. $\frac{x^2}{36} + \frac{y^2}{20} = 1$

13. $\frac{x^2}{9} + \frac{y^2}{4} = 1$
14. $\frac{x^2}{1} + \frac{y^2}{5} = 1$
15. $\frac{x^2}{169} + \frac{y^2}{144} = 1$

16. $\frac{x^2}{64} + \frac{y^2}{100} = 1$
17. $\frac{x^2}{16} + \frac{y^2}{7} = 1$
18. $\frac{x^2}{25} + \frac{y^2}{9} = 1$

<!-- page 42 -->
19. $\frac{x^2}{10} + \frac{y^2}{40} = 1$

20. $x^2 + 4y^2 = 52$ or $\frac{x^2}{52} + \frac{y^2}{13} = 1$

EXERCISE 11.4

1. Foci $(\pm 5, 0)$, Vertices $(\pm 4, 0)$; $e = \frac{5}{4}$; Latus rectum $= \frac{9}{2}$

2. Foci $(0 \pm 6)$, Vertices $(0, \pm 3)$; $e = 2$; Latus rectum $= 18$

3. Foci $(0, \pm \sqrt{13})$, Vertices $(0, \pm 2)$; $e = \frac{\sqrt{13}}{2}$; Latus rectum $= 9$

4. Foci $(\pm 10, 0)$, Vertices $(\pm 6, 0)$; $e = \frac{5}{3}$; Latus rectum $= \frac{64}{3}$

5. Foci $(0, \pm \frac{2\sqrt{14}}{\sqrt{5}})$, Vertices $(0, \pm \frac{6}{\sqrt{5}})$; $e = \frac{\sqrt{14}}{3}$; Latus rectum $= \frac{4\sqrt{5}}{3}$

6. Foci $(0, \pm \sqrt{65})$, Vertices $(0, \pm 4)$; $e = \frac{\sqrt{65}}{4}$; Latus rectum $= \frac{49}{2}$

7. $\frac{x^2}{4} - \frac{y^2}{5} = 1$          8. $\frac{y^2}{25} - \frac{x^2}{39} = 1$          9. $\frac{y^2}{9} - \frac{x^2}{16} = 1$

10. $\frac{x^2}{16} - \frac{y^2}{9} = 1$          11. $\frac{y^2}{25} - \frac{x^2}{144} = 1$          12. $\frac{x^2}{25} - \frac{y^2}{20} = 1$

13. $\frac{x^2}{4} - \frac{y^2}{12} = 1$          14. $\frac{x^2}{49} - \frac{9y^2}{343} = 1$          15. $\frac{y^2}{5} - \frac{x^2}{5} = 1$

Miscellaneous Exercise on Chapter 11

1. Focus is at the mid-point of the given diameter.
2. 2.23 m (approx.)
3. 9.11 m (approx.)
4. 1.56m (approx.)

5. $\frac{x^2}{81} + \frac{y^2}{9} = 1$
6. 18 sq units
7. $\frac{x^2}{25} + \frac{y^2}{9} = 1$

8. $8\sqrt{3}a$

<!-- page 43 -->
EXERCISE 12.1

1. $y$ and $z$ - coordinates are zero
2. $y$ - coordinate is zero
3. I, IV, VIII, V, VI, II, III, VII
4. (i) XY - plane
(ii) $(x, y, 0)$
(iii) Eight

EXERCISE 12.2

1. (i) $2\sqrt{5}$ (ii) $\sqrt{43}$ (iii) $2\sqrt{26}$ (iv) $2\sqrt{5}$
4. $x - 2z = 0$ 5. $9x^2 + 25y^2 + 25z^2 - 225 = 0$

EXERCISE 12.3

1. (i) $\left( \frac{-4}{5}, \frac{1}{5}, \frac{27}{5} \right)$ (ii) $(-8, 17, 3)$ 2. $1:2$
3. $2:3$ 5. $(6, -4, -2), (8, -10, 2)$

Miscellaneous Exercise on Chapter 12

1. $(1, -2, 8)$
2. $7, \sqrt{34}, 7$
3. $a = -2, \ b = -\frac{16}{3}, \ c = 2$
4. $(0, 2, 0)$ and $(0, -6, 0)$

5. $(4, -2, 6)$                                     6. $x^2 + y^2 + z^2 - 2x - 7y + 2z = \frac{k^2 - 109}{2}$

EXERCISE 13.1

1. 6
2. $\left(\pi - \frac{22}{7}\right)$
3. $\pi$
4. $\frac{19}{2}$
5. $-\frac{1}{2}$
6. 5
7. $\frac{11}{4}$
8. $\frac{108}{7}$
9. $b$
10. 2
11. 1
12. $-\frac{1}{4}$
13. $\frac{a}{b}$
14. $\frac{a}{b}$
15. $\frac{1}{\pi}$
16. $\frac{1}{\pi}$

<!-- page 44 -->
17. 4 18. $\frac{a+1}{b}$ 19. 0 20. 1

21. 0

22. 2

23. 3,6

24. Limit does not exist at $x = 1$

25. Limit does not exist at $x = 0$ 26. Limit does not exist at $x = 0$

27. $0$          28. $a=0, b=4$

29. $\lim_{x \to a_1} f(x) = 0$ and $\lim_{x \to a} f(x) = (a - a_1) (a - a_2) ... (a - a_x)$

30. $\lim_{x \to a} f(x)$ exists for all $a \neq 0$. 31. 2

32. For $\lim_{x \to 0} f(x)$ to exists, we need $m = n$; $\lim_{x \to 1} f(x)$ exists for any integral value
of $m$ and $n$.

EXERCISE 13.2

1. 20

2. 1

3. 99

4. (i) $3x^2$ (ii) $2x-3$ (iii) $\frac{-2}{x^3}$ (iv) $\frac{-2}{(x-1)^2}$

6. $nx^{n-1} + a(n-1)x^{n-2} + a^2(n-2)x^{n-3} + ... + a^{n-1}$

7. (i) $2x - a - b$ (ii) $4ax(ax^2 + b)$ (iii) $\frac{a - b}{(x - b)^2}$

8. $\frac{nx^n - anx^{n-1} - x^n + a^n}{(x-a)^2}$

9. (i) $2$ (ii) $20x^3 - 15x^2 + 6x - 4$ (iii) $\frac{-3}{x^4}(5 + 2x)$ (iv) $15x^4 + \frac{24}{x^5}$


(v) $\frac{-12}{x^5} + \frac{36}{x^{10}}$ (vi) $\frac{-2}{(x+1)^2} - \frac{x(3x-2)}{(3x-1)^2}$ 10. $-\sin x$

11. (i) $\cos 2x$                                                                    (ii) $\sec x \tan x$
    (iii) $5\sec x \tan x - 4\sin x$                                     (iv) $-\csc x \cot x$
    (v) $-\ 3\csc^2 x - 5 \csc x \cot x$                               (vi) $5\cos x+ 6\sin x$
    (vii) $2\sec^2 x - 7\sec x \tan x$

(vii) $2\sec^2 x - 7\sec x \tan x$

<!-- page 45 -->
Miscellaneous Exercise on Chapter 13

1. (i) $-1$ (ii) $\frac{1}{x^2}$ (iii) $\cos(x+1)$ (iv) $-\sin\left(x-\frac{\pi}{8}\right)$ 2. $1$


3. $\frac{-qr}{x^2} + ps$ 4. $2c(ax+b)(cx+d) + a(cx+d)^2$


5. $\frac{ad-bc}{(cx+d)^2}$ 6. $\frac{-2}{(x-1)^2}$, $x \neq 0,1$ 7. $\frac{-(2ax+b)}{(ax^2+bx+c)^2}$


8. $\frac{-apx^2-2bpx+ar-bq}{(px^2+qx+r)^2}$ 9. $\frac{apx^2+2bpx+bq-ar}{(ax+b)^2}$ 10. $\frac{-4a}{x^5} + \frac{2b}{x^3} - \sin x$


11. $\frac{2}{\sqrt{x}}$ 12. $na(ax+b)^{n-1}$


13. $(ax+b)^{n-1}(cx+d)^{m-1}[mc(ax+b)+na(cx+d)]$ 14. $\cos(x+a)$


15. $-\csc^3 x - \csc x \cot^2 x$ 16. $\frac{-1}{1+\sin x}$


17. $\frac{-2}{(\sin x - \cos x)^2}$ 18. $\frac{2\sec x \tan x}{(\sec x + 1)^2}$ 19. $n \sin^{n-1} x \cos x$


20. $\frac{bc \cos x + ad \sin x + bd}{(c+d \cos x)^2}$ 21. $\frac{\cos a}{\cos^2 x}$


22. $x^3(5x \cos x + 3x \sin x + 20 \sin x - 12\cos x)$


23. $-x^2 \sin x - \sin x + 2x \cos x$


24. $-q \sin x(ax^2 + \sin x) + (p+q \cos x)(2a x + \cos x)$


25. $-\tan^2 x(x+\cos x) + (x-\tan x)(1-\sin x)$


26. $\frac{35+15x \cos x + 28 \cos x + 28x \sin x - 15\sin x}{(3x+7 \cos x)^2}$

<!-- page 46 -->
$$27. \quad \frac{x \cos \frac{\pi}{4}(2 \sin x - x \cos x)}{\sin^2 x}$$

28. $\frac{1 + \tan x - x \sec^2 x}{(1 + \tan x)^2}$

29. $(x + \sec x)(1 - \sec^2 x) + (x - \tan x).(1 + \sec x \tan x)$

$$\mathbf{30.} \quad \frac{\sin x - n x \cos x}{\sin^{n+1} x}$$

EXERCISE 14.1

1.   (i) This sentence is always false because the maximum number of days in a
        month is 31. Therefore, it is a statement.
        (ii) This is not a statement because for some people mathematics can be easy
        and for some others it can be difficult.
        (iii) This sentence is always true because the sum is 12 and it is greater than 10.
        Therefore, it is a statement.
        (iv) This sentence is sometimes true and sometimes not true. For example the
        square of 2 is even number and the square of 3 is an odd number. Therefore,
        it is not a statement.
        (v) This sentence is sometimes true and sometimes false. For example, squares
        and rhombus have equal length whereas rectangles and trapezium have
        unequal length. Therefore, it is not a statement.
        (vi) It is an order and therefore, is not a statement.
        (vii) This sentence is false as the product is $(-8)$. Therefore, it is a statement.
        (viii) This sentence is always true and therefore, it is a statement.
        (ix) It is not clear from the context which day is referred and therefore, it is not
        a statement.
        (x) This is a true statement because all real numbers can be written in the form
        $a + i \times 0$.

2. The three examples can be:
(i) Everyone in this room is bold. This is not a statement because from the
context it is not clear which room is referred here and the term bold is not
precisely defined.
(ii) She is an engineering student. This is also not a statement because who
‘she’ is.
(iii) “$\cos^2\theta$ is always greater than $1/2$”. Unless, we know what $\theta$ is, we cannot
say whether the sentence is true or not.

<!-- page 47 -->
EXERCISES 14.2

1.   (i)  Chennai is not the capital of Tamil Nadu.
     (ii)  $\sqrt{2}$  is a complex number.
     (iii)  All triangles are equilateral triangles.
     (iv)  The number 2 is not greater than 7.
     (v)  Every natural number is not an integer.

2.  (i) The negation of the first statement is “the number $x$ is a rational number.”
        which is the same as the second statement” This is because when a number
        is not irrational, it is a rational. Therefore, the given pairs are negations of
        each other.
    (ii) The negation of the first statement is “$x$ is an irrational number” which is
        the same as the second statement. Therefore, the pairs are negations of
        each other.

3.   (i)  Number 3 is prime; number 3 is odd (True).
     (ii)  All integers are positive; all integers are negative (False).
     (iii)  100 is divisible by 3,100 is divisible by 11 and 100 is divisible by 5 (False).

EXERCISE 14.3

1.   (i)  “And”. The component statements are:
        All rational numbers are real.
        All real numbers are not complex.
    (ii)  “Or”. The component statements are:
        Square of an integer is positive.
        Square of an integer is negative.
    (iii)  “And”. the component statements are:
        The sand heats up quickly in the sun.
        The sand does not cool down fast at night.
    (iv)  “And”. The component statements are:
        $x = 2$ is a root of the equation $3x^2 - x - 10 = 0$
        $x = 3$ is a root of the equation $3x^2 - x - 10 = 0$

2.  (i) “There exists”. The negation is
There does not exist a number which is equal to its square.
(ii) “For every”. The negation is
There exists a real number $x$ such that $x$ is not less than $x + 1$.
(iii) “There exists”. The negation is
There exists a state in India which does not have a capital.

<!-- page 48 -->
3. No. The negation of the statement in (i) is “There exists real number $x$ and
$y$ for which $x + y \neq y + x$”, instead of the statement given in (ii).
4. (i) Exclusive
(ii) Inclusive
(iii) Exclusive

EXERCISE 14.4

1.  (i) A natural number is odd implies that its square is odd.
    (ii) A natural number is odd only if its square is odd.
    (iii) For a natural number to be odd it is necessary that its square is odd.
    (iv) For the square of a natural number to be odd, it is sufficient that the number
        is odd
    (v) If the square of a natural number is not odd, then the natural number
        is not odd.

2.  (i) The contrapositive is
        If a number $x$ is not odd, then $x$ is not a prime number.
        The converse is
        If a number $x$ in odd, then it is a prime number.
    (ii) The contrapositive is
        If two lines intersect in the same plane, then they are not parallel
        The converse is
        If two lines do not interesect in the same plane, then they are parallel
    (iii) The contrapositive is
        If something is not at low temperature, then it is not cold
        The converse is
        If something is at low temperature, then it is cold
    (iv) The contrapositive is
        If you know how to reason deductively, then you can comprehend geometry.
        The converse is
        If you do not know how to reason deductively, then you can not comprehend
        geometry.
    (v) This statement can be written as “If $x$ is an even number, then $x$ is
        divisible by 4”.
        The contrapositive is, If $x$ is not divisible by 4, then $x$ is not an even number.
        The converse is, If $x$ is divisible by 4, then $x$ is an even number.

3. (i) If you get a job, then your credentials are good.
(ii) If the banana tree stays warm for a month, then it will bloom.

<!-- page 49 -->
(iii) If diagonals of a quadrilateral bisect each other, then it is a parallelogram.
(iv) If you get $A^+$ in the class, then you do all the exercises in the book.

4. a (i) Contrapositive
   (ii) Converse
   b (i) Contrapositive
   (ii) Converse

EXERCISE 14.5

5.   (i) False. By definition of the chord, it should intersect the circle in two points.
     (ii) False. This can be shown by giving a counter example. A chord which is not
          a dimaeter gives the counter example.
     (iii) True. In the equation of an ellipse if we put $a = b$, then it is a circle
          (Direct Method)
     (iv) True, by the rule of inequality
     (v) False. Since 11 is a prime number, therefore $\sqrt{11}$ is irrational.

Miscellaneous Exercise on Chapter 14

1. (i) There exists a positive real number $x$ such that $x-1$ is not positive.
(ii) There exists a cat which does not scratch.
(iii) There exists a real number $x$ such that neither $x > 1$ nor $x < 1$.
(iv) There does not exist a number $x$ such that $0 < x < 1$.

2.   (i) The statement can be written as “If a positive integer is prime, then it has no
divisors other than 1 and itself.
The converse of the statement is
If a positive integer has no divisors other than 1 and itself, then it is a prime.
The contrapositive of the statement is
If positive integer has divisors other than 1 and itself then it is not prime.
(ii) The given statement can be written as “If it is a sunny day, then I go
to a beach.
The converse of the statement is
If I go to beach, then it is a sunny day.
The contrapositive is
If I do not go to a beach, then it is not a sunny day.
(iii) The converse is
If you feel thirsty, then it is hot outside.
The contrapositive is
If you do not feel thirsty, then it is not hot outside.

<!-- page 50 -->
3. (i) If you log on to the server, then you have a password.
(ii) If it rains, then there is traffic jam.
(iii) If you can access the website, then you pay a subscription fee.

4. (i) You watch television if and only if your mind in free.
(ii) You get an A grade if and only if you do all the homework regularly.
(iii) A quadrilateral is equiangular if and only if it is a rectangle.

5. The compound statement with “And” is 25 is a multiple of 5 and 8
This is a false statement.
The compound statement with “Or” is 25 is a multiple of 5 or 8
This is true statement.

7. Same as Q1 in Exercise 14.4

EXERCISE 15.1

1. 3
2. 8.4
3. 2.33
4. 7
5. 6.32
6. 16
7. 3.23
8. 5.1
9. 157.92
10. 11.28
11. 10.34
12. 7.35

EXERCISE 15.2

1. 9,9.25
2. $\frac{n+1}{2}, \frac{n^2-1}{12}$
3. 16.5,74.25
4. 19,43.4
5. 100,29.09
6. 64,1.69
7. 107,2276
8. 27,132
9. 93,105.52,10.27
10. 5.55,43.5

EXERCISE 15.3

1. B
2. Y
3. (i) B, (ii) B
4. A
5. Weight

Miscellaneous Exercise on Chapter 15

1. 4, 8          2. 6, 8          3. 24, 12

5. (i) 10.1, 1.99 (ii) 10.2, 1.98

6. Highest Chemistry and lowest Mathematics 7. 20, 3.036

<!-- page 51 -->
EXERCISE 16.1

1. {HHH, HHT, HTH, THH, TTH, HTT, THT, TTT}
2. $\{(x, y) : x, y = 1,2,3,4,5,6\}$
or $\{(1,1), (1,2), (1,3), ..., (1,6), (2,1), (2,2), ..., (2,6), ..., (6, 1), (6, 2), ..., (6,6)\}$
3. {HHHH, HHHT, HHTH, HTHH, THHH, HHTT, HTHT, HTTH, THHT, THTH,
TTHH, HTTT, THTT, TTHT, TTTH, TTTT}
4. {H1, H2, H3, H4, H5, H6, T1, T2, T3, T4, T5, T6}
5. {H1, H2, H3, H4, H5, H6, T}
6. {XB$_1$, XB$_2$, XG$_1$, XG$_2$, YB$_3$, YG$_3$, YG$_4$, YG$_5$}
7. {R1, R2, R3, R4, R5, R6, W1, W2, W3, W4, W5, W6, B1, B2, B3, B4, B5, B6}
8. (i) {BB, BG, GB, GG} (ii) $\{0, 1, 2\}$
9. {RW, WR, WW}
10. [HH, HT, T1, T2, T3, T4, T5, T6]
11. {DDD, DDN, DND, NDD, DNN, NDN, NND, NNN}
12. {T, H1, H3, H5, H21, H22, H23, H24, H25, H26, H41, H42, H43, H44, H45, H46,
H61, H62, H63, H64, H65, H66}
13. {(1,2), (1,3), (1,4), (2,1), (2,3), (2,4), (3,1), (3,2), (3,4), (4,1), (4,2), (4,3)}
14. {1HH, 1HT, 1TH, 1TT, 2H, 2T, 3HH, 3HT, 3TH, 3TT, 4H, 4T, 5HH, 5HT, 5TH,
5TT, 6H, 6T}
15. {TR$_1$, TR$_2$, TB$_1$, TB$_2$, TB$_3$, H1, H2, H3, H4, H5, H6}
16. {6, (1,6), (2,6), (3,6), (4,6), (5,6), (1,1,6), (1,2,6), ..., (1,5,6), (2,1,6). (2,2,6), ...,
(2,5,6), ..., (5,1,6), (5,2,6), ... }

EXERCISE 16.2

1. No.

1. No.
2. (i) $\{1, 2, 3, 4, 5, 6\}$ (ii) $\phi$ (iii) $\{3, 6\}$ (iv) $\{1, 2, 3\}$ (v) $\{6\}$
(vi) $\{3, 4, 5, 6\}, A \cup B = \{1, 2, 3, 4, 5, 6\}, A \cap B = \phi, B \cup C = \{3, 6\}, E \cap F = \{6\},$
$D \cap E = \phi,$
$A - C = \{1, 2, 4, 5\}, D - E = \{1, 2, 3\}, E \cap F' = \phi, F' = \{1, 2\}$
3. $A = \{(3,6), (4,5), (5,4), (6,3), (4,6), (5,5), (6,4), (5,6), (6,5), (6,6)\}$
$B = \{(1,2), (2,2), (3,2), (4,2), (5,2), (6,2), (2,1), (2,3), (2,4), (2,5), (2,6)\}$
$C = \{(3,6), (6,3), (5,4), (4,5), (6,6)\}$
$A$ and $B$, $B$ and $C$ are mutually exclusive.

4. (i) $A$ and $B$; $A$ and $C$; $B$ and $C$; $C$ and $D$ (ii) $A$ and $C$ (iii) $B$ and $D$
5. (i) "Getting at least two heads", and "getting at least two tails"
(ii) "Getting no heads", "getting exactly one head" and "getting at least two
heads"

<!-- page 52 -->
(iii) “Getting at most two tails”, and “getting exactly two tails”
(iv) “Getting exactly one head” and “getting exactly two heads”
(v) “Getting exactly one tail”, “getting exactly two tails”, and getting exactly
three tails”

There may be other events also as answer to the above question.

6. $A = \{(2, 1), (2,2), (2,3), (2,4), (2,5), (2,6), (4,1), (4,2), (4,3), (4,4), (4,5), (4,6),$
$(6,1), (6,2), (6,3), (6,4), (6,5), (6,6)\}$
$B = \{(1, 1), (1,2), (1,3), (1,4), (1,5), (1,6), (3,1), (3,2), (3,3), (3,4), (3,5), (3,6),$
$(5,1), (5,2), (5,3), (5,4), (5,5), (5,6)\}$
$C = \{(1, 1), (1,2), (1,3), (1,4), (2,1), (2,2), (2,3), (3,1), (3,2), (4,1)\}$
(i) $A' = \{(1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (3,1), (3,2), (3,3), (3,4), (3,5), (3,6),$
$(5,1), (5,2), (5,3), (5,4), (5,5), (5,6)\} = B$
(ii) $B' = \{(2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (4,1), (4,2), (4,3), (4,4), (4,5), (4,6),$
$(6,1), (6,2), (6,3), (6,4), (6,5), (6,6)\} = A$
(iii) $A \cup B = \{(1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (3,1), (3,2), (3,3), (3,4), (3,5),$
$(3,6), (5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (2,1), (2,2), (2,3), (2,5),$
$(2,6), (4,1), (4,2), (4,3), (4,4), (4,5), (4,6), (6,1), (6,2), (6,3), (6,4),$
$(6,5), (6,6)\} = S$
(iv) $A \cap B = \phi$
(v) $A - C = \{(2,4), (2,5), (2,6), (4,2), (4,3), (4,4), (4,5), (4,6), (6,1), (6,2), (6,3),$
$(6,4), (6,5), (6,6)\}$
(vi) $B \cup C = \{(1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (2,1), (2,2), (2,3), (3,1), (3,2),$
$(3,3), (3,4), (3,5), (3,6), (4,1), (5,1), (5,2), (5,3), (5,4), (5,5), (5,6)\}$
(vii) $B \cap C = \{(1,1), (1,2), (1,3), (1,4), (3,1), (3,2)\}$
(viii) $A \cap B' \cap C' = \{(2,4), (2,5), (2,6), (4,2), (4,3), (4,4), (4,5), (4,6), (6,1), (6,2),$
$(6,3), (6,4), (6,5), (6,6)\}$

7. (i) True (ii) True (iii) True (iv) False (v) False (vi) False

EXERCISE 16.3

1. (a) Yes (b) Yes (c) No (d) No (e) No 2. $\frac{3}{4}$


3. (i) $\frac{1}{2}$ (ii) $\frac{2}{3}$ (iii) $\frac{1}{6}$ (iv) 0 (v) $\frac{5}{6}$ 4. (a) 52 (b) $\frac{1}{52}$ (c) (i) $\frac{1}{13}$ (ii) $\frac{1}{2}$


5. (i) $\frac{1}{12}$ (ii) $\frac{1}{12}$ 6. $\frac{3}{5}$

<!-- page 53 -->
7. Rs 4.00 gain, Rs 1.50 gain, Re 1.00 loss, Rs 3.50 loss, Rs 6.00 loss.

$$\mathrm{P} \left( \text{Winning Rs } 4.00 \right) = \frac{1}{16} , \mathrm{P} \left( \text{Winning Rs } 1.50 \right) = \frac{1}{4} , \mathrm{P} \left( \text{Losing Re. } 1.00 \right) = \frac{3}{8}$$

$$P (Losing Rs 3.50) = \frac{1}{4}, P (Losing Rs 6.00) = \frac{1}{16}.$$

8. (i) $\frac{1}{8}$ (ii) $\frac{3}{8}$ (iii) $\frac{1}{2}$ (iv) $\frac{7}{8}$ (v) $\frac{1}{8}$ (vi) $\frac{1}{8}$ (vii) $\frac{3}{8}$ (viii) $\frac{1}{8}$ (ix) $\frac{7}{8}$

9. $\frac{9}{11}$                                     10. (i) $\frac{6}{13}$ (ii) $\frac{7}{13}$      11. $\frac{1}{38760}$

12. (i) No, because $P(A \cap B)$ must be less than or equal to $P(A)$ and $P(B)$, (ii) Yes

13. (i) $\frac{7}{15}$ (ii) 0.5 (iii) 0.15 14. $\frac{4}{5}$

15. (i) $\frac{5}{8}$ (ii) $\frac{3}{8}$ 16. No 17. (i) 0.58 (ii) 0.52 (iii) 0.74

18. 0.6

$$19. 0.55$$

$$20. 0.65$$

21. (i) $\frac{19}{30}$ (ii) $\frac{11}{30}$ (iii) $\frac{2}{15}$

Miscellaneous Exercise on Chapter 16

1. (i) $\frac{^{20}\text{C}_5}{^{60}\text{C}_5}$ (ii) $1-\frac{^{30}\text{C}_5}{^{60}\text{C}_5}$ 2. $\frac{^{13}\text{C}_3 \cdot ^{13}\text{C}_1}{^{52}\text{C}_4}$


3. (i) $\frac{1}{2}$ (ii) $\frac{1}{2}$ (iii) $\frac{5}{6}$ 4. (a) $\frac{999}{1000}$ (b) $\frac{^{9990}\text{C}_2}{^{10000}\text{C}_2}$ (c) $\frac{^{9990}\text{C}_{10}}{^{10000}\text{C}_{10}}$


5. (a) $\frac{17}{33}$ (b) $\frac{16}{33}$ 6. $\frac{2}{3}$


7. (i) 0.88 (ii) 0.12 (iii) 0.19 (iv) 0.34 8. $\frac{4}{5}$


9. (i) $\frac{33}{83}$ (ii) $\frac{3}{8}$ 10. $\frac{1}{5040}$

<!-- page 54 -->
MATHEMATICS

Textbook for Class XI

राष्ट्रीय शैक्षिक अनुसंधान और प्रशिक्षण परिषद्
NATIONAL COUNCIL OF EDUCATIONAL RESEARCH AND TRAINING

<!-- page 55 -->
First Edition
February 2006 Phalguna 1927

**Reprinted**
October 2006 Kartika 1928
November 2007 Kartika 1929
December 2008 Pausa 1930
December 2009 Agrahayana 1931
January 2011 Pausa 1932
February 2012 Magha 1933
December 2012 Pausa 1934
November 2013 Kartika 1935
December 2014 Pausa 1936
May 2016 Vaishakha 1938
December 2016 Pausa 1938
December 2017 Agrahayana 1939

ISBN 81-7450-486-9

© National Council of Educational
Research and Training, 2006

PD 400T BS

Published at the Publication Division by
the Secretary, National Council of
Educational Research and Training, Sri
Aurobindo Marg, New Delhi 110 016 and
printed at Pankaj Printing Press, D-28,
Industrial Area, Site-A, Mathura -
281 001 (Uttar Pradesh)

ALL RIGHTS RESERVED

$\square$ No part of this publication may be reproduced, stored in a retrieval
system or transmitted, in any form or by any means, electronic,
mechanical, photocopying, recording or otherwise without the prior
permission of the publisher.

$\square$ This book is sold subject to the condition that it shall not, by way of
trade, be lent, re-sold, hired out or otherwise disposed of without the
publisher's consent, in any form of binding or cover other than that in
which it is published.

$\square$ The correct price of this publication is the price printed on this page,
Any revised price indicated by a rubber stamp or by a sticker or by any
other means is incorrect and should be unacceptable.

Printed on 80 GSM paper with NCERT
watermark

$$₹ 180.00$$

<table>
<thead>
<tr>
<th colspan="2">OFFICES OF THE PUBLICATION<br/>DIVISION, NCERT</th>
</tr>
</thead>
<tbody>
<tr>
<td>NCERT Campus<br/>Sri Aurobindo Marg<br/>New Delhi 110 016</td>
<td>Phone : 011-26562708</td>
</tr>
<tr>
<td>108, 100 Feet Road<br/>Hosdakere Halli Extension<br/>Banashankari III Stage<br/>Bengaluru 560 085</td>
<td>Phone : 080-26725740</td>
</tr>
<tr>
<td>Navjivan Trust Building<br/>P.O.Navjivan<br/>Ahmedabad 380 014</td>
<td>Phone : 079-27541446</td>
</tr>
<tr>
<td>CWC Campus<br/>Opp. Dhankal Bus Stop<br/>Panihati<br/>Kolkata 700 114</td>
<td>Phone : 033-25530454</td>
</tr>
<tr>
<td>CWC Complex<br/>Maligaon<br/>Guwahati 781 021</td>
<td>Phone : 0361-2674869</td>
</tr>
</tbody>
</table>

Publication Team

<table>
<tbody>
<tr>
<td>Head, Publication<br/>Division</td>
<td>: M. Siraj Anwar</td>
</tr>
<tr>
<td>Chief Editor</td>
<td>: Shveta Uppal</td>
</tr>
<tr>
<td>Chief Business<br/>Manager</td>
<td>: Gautam Ganguly</td>
</tr>
<tr>
<td>Chief Production<br/>Officer (In-charge)</td>
<td>: Arun Chitkara</td>
</tr>
<tr>
<td>Editor</td>
<td>: Bijnan Sutar</td>
</tr>
<tr>
<td>Production Assistant</td>
<td>: Mukesh Gaur</td>
</tr>
</tbody>
</table>

Cover and Layout
Arvinder Chawla

<!-- page 56 -->
Foreword

The National Curriculum Framework (NCF), 2005, recommends that children’s life
at school must be linked to their life outside the school. This principle marks a
departure from the legacy of bookish learning which continues to shape our system
and causes a gap between the school, home and community. The syllabi and textbooks
developed on the basis of NCF signify an attempt to implement this basic idea. They
also attempt to discourage rote learning and the maintenance of sharp boundaries
between different subject areas. We hope these measures will take us significantly
further in the direction of a child-centred system of education outlined in the National
Policy on Education (1986).

The success of this effort depends on the steps that school principals and
teachers will take to encourage children to reflect on their own learning and to
pursue imaginative activities and questions. We must recognise that given space,
time and freedom, children generate new knowledge by engaging with the information
passed on to them by adults. Treating the prescribed textbook as the sole basis of
examination is one of the key reasons why other resources and sites of learning are
ignored. Inculcating creativity and initiative is possible if we perceive and treat
children as participants in learning, not as receivers of a fixed body of knowledge.

These aims imply considerable change in school routines and mode of
functioning. Flexibility in the daily time-table is as necessary as rigour in implementing
the annual calendar so that the required number of teaching days are actually devoted
to teaching. The methods used for teaching and evaluation will also determine how
effective this textbook proves for making children’s life at school a happy experience,
rather than a source of stress or boredom. Syllabus designers have tried to address
the problem of curricular burden by restructuring and reorienting knowledge at
different stages with greater consideration for child psychology and the time available
for teaching. The textbook attempts to enhance this endeavour by giving higher
priority and space to opportunities for contemplation and wondering, discussion in
small groups, and activities requiring hands-on experience.

The National Council of Educational Research and Training (NCERT) appreciates
the hard work done by the Textbook Development Committee responsible for this

<!-- page 57 -->
book. We wish to thank the Chairperson of the advisory group in Science and
Mathematics, Professor J.V. Narlikar and the Chief Advisor for this book
Professor P.K. Jain for guiding the work of this committee. Several teachers
contributed to the development of this textbook; we are grateful to their principals
for making this possible. We are indebted to the institutions and organisations which
have generously permitted us to draw upon their resources, material and personnel.
We are especially grateful to the members of the National Monitoring Committee,
appointed by the Department of Secondary and Higher Education, Ministry of Human
Resource Development under the Chairpersonship of Professor Mrinal Miri and
Professor G.P. Deshpande, for their valuable time and contribution. As an organisation
committed to the systemic reform and continuous improvement in the quality of its
products, NCERT welcomes comments and suggestions which will enable us to
undertake further revision and refinement.

New Delhi
20 December 2005

Director
National Council of Educational
Research and Training

<!-- page 58 -->
Textbook Development Committee

CHAIRPERSON, ADVISORY GROUP IN SCIENCE AND MATHEMATICS
J.V. Narlikar, *Emeritus Professor*, Chairman, Advisory Committee Inter University
Centre for Astronomy & Astrophysics (IUCCA), Ganeshkhind, Pune University, Pune

CHIEF ADVISOR

P.K. Jain, $Professor$, Department of Mathematics, University of Delhi, Delhi

CHIEF COORDINATOR

Hukum Singh, *Professor*, DESM, NCERT, New Delhi

MEMBERS

A.K. Rajput, Associate Professor, RIE Bhopal, M.P.

A.K. Wazalwar, Associate Professor, DESM NCERT, New Delhi

B.S.P. Raju, $Professor$, RIE Mysore, Karnataka

C.R. Pradeep, Assistant Professor, Department of Mathematics, Indian Institute of Science,
Bangalore, Karnataka.

Pradeepto Hore, $Sr. Maths Master$, Sarla Birla Academy Bangalore, Karnataka.

S.B. Tripathy, $Lecturer$, Rajkiya Pratibha Vikas Vidyalaya, Surajmal Vihar, Delhi.

S.K.S. Gautam, $Professor$, DESM, NCERT, New Delhi

Sanjay Kumar Sinha, $P.G.T.$, Sanskriti School Chanakyapuri, New Delhi.

Sanjay Mudgal, $Lecturer$, CIET, New Delhi

Sneha Titus, Maths Teacher, Aditi Mallya School Yelaharika, Bangalore, Karnataka

Sujatha Verma, $Reader$ in Mathematics, IGNOU, New Delhi.

Uaday Singh, $Lecturer$, DESM, NCERT, New Delhi.

MEMBER-COORDINATOR

V.P. Singh, Associate Professor, DESM, NCERT, New Delhi

<!-- page 59 -->
Acknowledgements

The Council gratefully acknowledges the valuable contributions of the following
participants of the Textbook Review Workshop: P. Bhaskar Kumar, $P.G.T.$, Jawahar
Navodaya Vidyalaya, Ananthpur, (A.P.); Vinayak Bujade, $Lecturer$, Vidarbha Buniyadi
Junior College, Sakkardara Chowk Nagpur, Maharashtra; Vandita Kalra, $Lecturer$,
Sarvodaya Kanya Vidyalaya Vikashpuri District Centre, New Delhi; P.L. Sachdeva
Deptt. of Mathematics, Indian Institute of Science, Bangalore, Karnataka; P.K.Tiwari
$Assistant$ $Commissioner$ (Retd.), Kendriya Vidyalaya Sangathan; Jagdish Saran,
Department of Statistics, University of Delhi; Quddus Khan, $Lecturer$, Shibli National
P.G. College Azamgarh (U.P.); Sumat Kumar Jain, $Lecturer$, K.L. Jain Inter College
Sasni Hathras (U.P.); R.P. Gihare, $Lecturer$ (BRC), Janpad Shiksha Kendra Chicholi
Distt. Betul (M.P.); Sangeeta Arora, $P.G.T.$, A.P.J. School Saket, New Delhi; P.N.
Malhotra, $ADE$ (Sc.), Directorate of Education, Delhi; D.R. Sharma, $P.G.T.$, J.N.V.
Mungespur, Delhi; Saroj, $P.G.T.$ Government Girls Sr. Secondary School, No. 1,
Roop Nagar, Delhi, Manoj Kumar Thakur, $P.G.T.$, D.A.V. Public School, Rajender
Nagar, Sahibabad, Ghaziabad (U.P.) and R.P. Maurya, $Reader$, DESM, NCERT,
New Delhi.

Acknowledgements are due to Professor M. Chandra, $Head$, Department of
Education in Science and Mathematics for her support.

The Council acknowledges the efforts of the Computer Incharge, Deepak Kapoor;
Rakesh Kumar, Kamlesh Rao and Sajjad Haider Ansari, D.T.P. Operators; Kushal Pal
Singh Yadav, Copy Editor and Proof Readers, Mukhtar Hussain and Kanwar Singh.

The contribution of APC–Office, administration of DESM and Publication
Department is also duly acknowledged.

<!-- page 60 -->
Contents

<table>
<thead>
<tr>
<th>Foreword</th>
<th>iii</th>
</tr>
</thead>
<tbody>
<tr>
<td>1. Sets</td>
<td>1</td>
</tr>
<tr>
<td>1.1 Introduction</td>
<td>1</td>
</tr>
<tr>
<td>1.2 Sets and their Representations</td>
<td>1</td>
</tr>
<tr>
<td>1.3 The Empty Set</td>
<td>5</td>
</tr>
<tr>
<td>1.4 Finite and Infinite Sets</td>
<td>6</td>
</tr>
<tr>
<td>1.5 Equal Sets</td>
<td>7</td>
</tr>
<tr>
<td>1.6 Subsets</td>
<td>9</td>
</tr>
<tr>
<td>1.7 Power Set</td>
<td>12</td>
</tr>
<tr>
<td>1.8 Universal Set</td>
<td>12</td>
</tr>
<tr>
<td>1.9 Venn Diagrams</td>
<td>13</td>
</tr>
<tr>
<td>1.10 Operations on Sets</td>
<td>14</td>
</tr>
<tr>
<td>1.11 Complement of a Set</td>
<td>18</td>
</tr>
<tr>
<td>1.12 Practical Problems on Union and Intersection of Two Sets</td>
<td>21</td>
</tr>
<tr>
<td>2. Relations and Functions</td>
<td>30</td>
</tr>
<tr>
<td>2.1 Introduction</td>
<td>30</td>
</tr>
<tr>
<td>2.2 Cartesian Product of Sets</td>
<td>30</td>
</tr>
<tr>
<td>2.3 Relations</td>
<td>34</td>
</tr>
<tr>
<td>2.4 Functions</td>
<td>36</td>
</tr>
<tr>
<td>3. Trigonometric Functions</td>
<td>49</td>
</tr>
<tr>
<td>3.1 Introduction</td>
<td>49</td>
</tr>
<tr>
<td>3.2 Angles</td>
<td>49</td>
</tr>
<tr>
<td>3.3 Trigonometric Functions</td>
<td>55</td>
</tr>
<tr>
<td>3.4 Trigonometric Functions of Sum and Difference of Two Angles</td>
<td>63</td>
</tr>
<tr>
<td>3.5 Trigonometric Equations</td>
<td>74</td>
</tr>
<tr>
<td>4. Principle of Mathematical Induction</td>
<td>86</td>
</tr>
<tr>
<td>4.1 Introduction</td>
<td>86</td>
</tr>
<tr>
<td>4.2 Motivation</td>
<td>87</td>
</tr>
<tr>
<td>4.3 The Principle of Mathematical Induction</td>
<td>88</td>
</tr>
</tbody>
</table>

<!-- page 61 -->
<table>
<tbody>
<tr>
<td>5.</td>
<td>Complex Numbers and Quadratic Equations</td>
<td>97</td>
</tr>
<tr>
<td></td>
<td>5.1 Introduction</td>
<td>97</td>
</tr>
<tr>
<td></td>
<td>5.2 Complex Numbers</td>
<td>97</td>
</tr>
<tr>
<td></td>
<td>5.3 Algebra of Complex Numbers</td>
<td>98</td>
</tr>
<tr>
<td></td>
<td>5.4 The Modulus and the Conjugate of a Complex Number</td>
<td>102</td>
</tr>
<tr>
<td></td>
<td>5.5 Argand Plane and Polar Representation</td>
<td>104</td>
</tr>
<tr>
<td></td>
<td>5.6 Quadratic Equations</td>
<td>108</td>
</tr>
<tr>
<td>6.</td>
<td>Linear Inequalities</td>
<td>116</td>
</tr>
<tr>
<td></td>
<td>6.1 Introduction</td>
<td>116</td>
</tr>
<tr>
<td></td>
<td>6.2 Inequalities</td>
<td>116</td>
</tr>
<tr>
<td></td>
<td>6.3 Algebraic Solutions of Linear Inequalities in One Variable<br/>and their Graphical Representation</td>
<td>118</td>
</tr>
<tr>
<td></td>
<td>6.4 Graphical Solution of Linear Inequalities in Two Variables</td>
<td>123</td>
</tr>
<tr>
<td></td>
<td>6.5 Solution of System of Linear Inequalities in Two Variables</td>
<td>127</td>
</tr>
<tr>
<td>7.</td>
<td>Permutations and Combinations</td>
<td>134</td>
</tr>
<tr>
<td></td>
<td>7.1 Introduction</td>
<td>134</td>
</tr>
<tr>
<td></td>
<td>7.2 Fundamental Principle of Counting</td>
<td>134</td>
</tr>
<tr>
<td></td>
<td>7.3 Permutations</td>
<td>138</td>
</tr>
<tr>
<td></td>
<td>7.4 Combinations</td>
<td>148</td>
</tr>
<tr>
<td>8.</td>
<td>Binomial Theorem</td>
<td>160</td>
</tr>
<tr>
<td></td>
<td>8.1 Introduction</td>
<td>160</td>
</tr>
<tr>
<td></td>
<td>8.2 Binomial Theorem for Positive Integral Indices</td>
<td>160</td>
</tr>
<tr>
<td></td>
<td>8.3 General and Middle Terms</td>
<td>167</td>
</tr>
<tr>
<td>9.</td>
<td>Sequences and Series</td>
<td>177</td>
</tr>
<tr>
<td></td>
<td>9.1 Introduction</td>
<td>177</td>
</tr>
<tr>
<td></td>
<td>9.2 Sequences</td>
<td>177</td>
</tr>
<tr>
<td></td>
<td>9.3 Series</td>
<td>179</td>
</tr>
<tr>
<td></td>
<td>9.4 Arithmetic Progression (A.P.)</td>
<td>181</td>
</tr>
<tr>
<td></td>
<td>9.5 Geometric Progression (G.P.)</td>
<td>186</td>
</tr>
<tr>
<td></td>
<td>9.6 Relationship Between A.M. and G.M.</td>
<td>191</td>
</tr>
<tr>
<td></td>
<td>9.7 Sum to n terms of Special Series</td>
<td>194</td>
</tr>
<tr>
<td>10.</td>
<td>Straight Lines</td>
<td>203</td>
</tr>
<tr>
<td></td>
<td>10.1 Introduction</td>
<td>203</td>
</tr>
<tr>
<td></td>
<td>10.2 Slope of a Line</td>
<td>204</td>
</tr>
<tr>
<td></td>
<td>10.3 Various Forms of the Equation of a Line</td>
<td>212</td>
</tr>
<tr>
<td></td>
<td>10.4 General Equation of a Line</td>
<td>220</td>
</tr>
<tr>
<td></td>
<td>10.5 Distance of a Point From a Line</td>
<td>225</td>
</tr>
</tbody>
</table>

<!-- page 62 -->
<table>
<tbody>
<tr>
<td>11.</td>
<td>Conic Sections</td>
<td>236</td>
</tr>
<tr>
<td>11.1</td>
<td>Introduction</td>
<td>236</td>
</tr>
<tr>
<td>11.2</td>
<td>Sections of a Cone</td>
<td>236</td>
</tr>
<tr>
<td>11.3</td>
<td>Circle</td>
<td>239</td>
</tr>
<tr>
<td>11.4</td>
<td>Parabola</td>
<td>242</td>
</tr>
<tr>
<td>11.5</td>
<td>Ellipse</td>
<td>247</td>
</tr>
<tr>
<td>11.6</td>
<td>Hyperbola</td>
<td>255</td>
</tr>
<tr>
<td>12.</td>
<td>Introduction to Three Dimensional Geometry</td>
<td>268</td>
</tr>
<tr>
<td>12.1</td>
<td>Introduction</td>
<td>268</td>
</tr>
<tr>
<td>12.2</td>
<td>Coordinate Axes and Coordinate Planes in<br/>Three Dimensional Space</td>
<td>269</td>
</tr>
<tr>
<td>12.3</td>
<td>Coordinates of a Point in Space</td>
<td>269</td>
</tr>
<tr>
<td>12.4</td>
<td>Distance between Two Points</td>
<td>271</td>
</tr>
<tr>
<td>12.5</td>
<td>Section Formula</td>
<td>273</td>
</tr>
<tr>
<td>13.</td>
<td>Limits and Derivatives</td>
<td>281</td>
</tr>
<tr>
<td>13.1</td>
<td>Introduction</td>
<td>281</td>
</tr>
<tr>
<td>13.2</td>
<td>Intuitive Idea of Derivatives</td>
<td>281</td>
</tr>
<tr>
<td>13.3</td>
<td>Limits</td>
<td>284</td>
</tr>
<tr>
<td>13.4</td>
<td>Limits of Trigonometric Functions</td>
<td>298</td>
</tr>
<tr>
<td>13.5</td>
<td>Derivatives</td>
<td>303</td>
</tr>
<tr>
<td>14.</td>
<td>Mathematical Reasoning</td>
<td>321</td>
</tr>
<tr>
<td>14.1</td>
<td>Introduction</td>
<td>321</td>
</tr>
<tr>
<td>14.2</td>
<td>Statements</td>
<td>321</td>
</tr>
<tr>
<td>14.3</td>
<td>New Statements from Old</td>
<td>324</td>
</tr>
<tr>
<td>14.4</td>
<td>Special Words/Phrases</td>
<td>329</td>
</tr>
<tr>
<td>14.5</td>
<td>Implications</td>
<td>335</td>
</tr>
<tr>
<td>14.6</td>
<td>Validating Statements</td>
<td>339</td>
</tr>
<tr>
<td>15.</td>
<td>Statistics</td>
<td>347</td>
</tr>
<tr>
<td>15.1</td>
<td>Introduction</td>
<td>347</td>
</tr>
<tr>
<td>15.2</td>
<td>Measures of Dispersion</td>
<td>349</td>
</tr>
<tr>
<td>15.3</td>
<td>Range</td>
<td>349</td>
</tr>
<tr>
<td>15.4</td>
<td>Mean Deviation</td>
<td>349</td>
</tr>
<tr>
<td>15.5</td>
<td>Variance and Standard Deviation</td>
<td>361</td>
</tr>
<tr>
<td>15.6</td>
<td>Analysis of Frequency Distributions</td>
<td>372</td>
</tr>
</tbody>
</table>

ix

<!-- page 63 -->
<table>
<tbody>
<tr>
<td>16. Probability</td>
<td>383</td>
</tr>
<tr>
<td>16.1 Introduction</td>
<td>383</td>
</tr>
<tr>
<td>16.2 Random Experiments</td>
<td>384</td>
</tr>
<tr>
<td>16.3 Event</td>
<td>387</td>
</tr>
<tr>
<td>16.4 Axiomatic Approach to Probability</td>
<td>394</td>
</tr>
<tr>
<td>Appendix 1: Infinite Series</td>
<td>412</td>
</tr>
<tr>
<td>A.1.1 Introduction</td>
<td>412</td>
</tr>
<tr>
<td>A.1.2 Binomial Theorem for any Index</td>
<td>412</td>
</tr>
<tr>
<td>A.1.3 Infinite Geometric Series</td>
<td>414</td>
</tr>
<tr>
<td>A.1.4 Exponential Series</td>
<td>416</td>
</tr>
<tr>
<td>A.1.5 Logarithmic Series</td>
<td>419</td>
</tr>
<tr>
<td>Appendix 2: Mathematical Modelling</td>
<td>421</td>
</tr>
<tr>
<td>A.2.1 Introduction</td>
<td>421</td>
</tr>
<tr>
<td>A.2.2 Preliminaries</td>
<td>421</td>
</tr>
<tr>
<td>A.2.3 What is Mathematical Modelling</td>
<td>425</td>
</tr>
<tr>
<td>Answers</td>
<td>433</td>
</tr>
<tr>
<td>Supplementary Material</td>
<td>466</td>
</tr>
</tbody>
</table>

Supplementary Material 466

<!-- page 64 -->
Chapter 1

SETS

❖In these days of conflict between ancient and modern studies; there
must surely be something to be said for a study which did not
begin with Pythagoras and will not end with Einstein; but
is the oldest and the youngest. — G.H. HARDY ❖

1.1 Introduction

The concept of set serves as a fundamental part of the
present day mathematics. Today this concept is being used
in almost every branch of mathematics. Sets are used to
define the concepts of relations and functions. The study of
geometry, sequences, probability, etc. requires the knowledge
of sets.

Georg Cantor
(1845-1918)

The theory of sets was developed by German
mathematician Georg Cantor (1845-1918). He first
encountered sets while working on “problems on trigonometric
series”. In this Chapter, we discuss some basic definitions
and operations involving sets.

1.2 Sets and their Representations

In everyday life, we often speak of collections of objects of a particular kind, such as,
a pack of cards, a crowd of people, a cricket team, etc. In mathematics also, we come
across collections, for example, of natural numbers, points, prime numbers, etc. More
specially, we examine the following collections:

(i) Odd natural numbers less than 10, i.e., 1, 3, 5, 7, 9
(ii) The rivers of India
(iii) The vowels in the English alphabet, namely, $a$, $e$, $i$, $o$, $u$
(iv) Various kinds of triangles
(v) Prime factors of 210, namely, 2,3,5 and 7
(vi) The solution of the equation: $x^2 - 5x + 6 = 0$, viz, 2 and 3.

We note that each of the above example is a well-defined collection of objects in

<!-- page 65 -->
the sense that we can definitely decide whether a given particular object belongs to a
given collection or not. For example, we can say that the river Nile does not belong to
the collection of rivers of India. On the other hand, the river Ganga does belong to this
colleciton.

We give below a few more examples of sets used particularly in mathematics, viz.

$\mathbf{N}$ : the set of all natural numbers
$\mathbf{Z}$ : the set of all integers
$\mathbf{Q}$ : the set of all rational numbers
$\mathbf{R}$ : the set of real numbers
$\mathbf{Z}^{+}$ : the set of positive integers
$\mathbf{Q}^{+}$ : the set of positive rational numbers, and
$\mathbf{R}^{+}$ : the set of positive real numbers.

The symbols for the special sets given above will be referred to throughout
this text.

Again the collection of five most renowned mathematicians of the world is not
well-defined, because the criterion for determining a mathematician as most renowned
may vary from person to person. Thus, it is not a well-defined collection.

We shall say that a set is a well-defined collection of objects.

The following points may be noted :

(i) Objects, elements and members of a set are synonymous terms.
(ii) Sets are usually denoted by capital letters A, B, C, X, Y, Z, etc.
(iii) The elements of a set are represented by small letters $a, b, c, x, y, z,$ etc.

If $a$ is an element of a set A, we say that “ $a$ belongs to A” the Greek symbol $\in$
(epsilon) is used to denote the phrase ‘$belongs$ $to$’. Thus, we write $a \in \text{A}$. If ‘$b$’ is not
an element of a set A, we write $b \notin \text{A}$ and read “$b$ does not belong to A”.

Thus, in the set V of vowels in the English alphabet, $a \in \text{V}$ but $b \notin \text{V}$. In the set
P of prime factors of 30, $3 \in \text{P}$ but $15 \notin \text{P}$.

There are two methods of representing a set :

(i) Roster or tabular form
(ii) Set-builder form.

(i) In roster form, all the elements of a set are listed, the elements are being separated
by commas and are enclosed within braces { } . For example, the set of all even
positive integers less than 7 is described in roster form as $\{2, 4, 6\}$. Some more
examples of representing a set in roster form are given below :

(a) The set of all natural numbers which divide 42 is $\{1, 2, 3, 6, 7, 14, 21, 42\}$.

<!-- page 66 -->
Note In roster form, the order in which the elements are listed is immaterial.
Thus, the above set can also be represented as $\{1, 3, 7, 21, 2, 6, 14, 42\}$.

(b) The set of all vowels in the English alphabet is $\{a, e, i, o, u\}$.
(c) The set of odd natural numbers is represented by $\{1, 3, 5, \dots\}$. The dots
tell us that the list of odd numbers continue indefinitely.

**Note** It may be noted that while writing the set in roster form an element is not
generally repeated, i.e., all the elements are taken as distinct. For example, the set
of letters forming the word ‘SCHOOL’ is { S, C, H, O, L} or {H, O, L, C, S}. Here,
the order of listing elements has no relevance.

(ii) In set-builder form, all the elements of a set possess a single common property
which is not possessed by any element outside the set. For example, in the set
$\{a, e, i, o, u\}$, all the elements possess a common property, namely, each of them
is a vowel in the English alphabet, and no other letter possess this property. Denoting
this set by V, we write

$$V = \{x : x \text{ is a vowel in English alphabet}\}$$

It may be observed that we describe the element of the set by using a symbol $x$
(any other symbol like the letters $y$, $z$, etc. could be used) which is followed by a colon
“ : ” . After the sign of colon, we write the characteristic property possessed by the
elements of the set and then enclose the whole description within braces. The above
description of the set V is read as “the set of all $x$ such that $x$ is a vowel of the English
alphabet”. In this description the braces stand for “the set of all”, the colon stands for
“such that”. For example, the set

A = $\{x : x \text{ is a natural number and } 3 < x < 10\}$ is read as “the set of all $x$ such that
$x$ is a natural number and $x$ lies between 3 and 10.” Hence, the numbers 4, 5, 6,
7, 8 and 9 are the elements of the set A.

If we denote the sets described in $(a)$, $(b)$ and $(c)$ above in roster form by A, B,
C, respectively, then A, B, C can also be represented in set-builder form as follows:

A= {x : x is a natural number which divides 42}
B= {y : y is a vowel in the English alphabet}
C= {z : z is an odd natural number}

Example 1 Write the solution set of the equation $x^2 + x - 2 = 0$ in roster form.

Solution The given equation can be written as
$$(x - 1) \ (x + 2) = 0, \text{ i. e., } \quad x = 1, -2$$
Therefore, the solution set of the given equation can be written in roster form as $\{1, -2\}$.

Example 2 Write the set $\{x : x \text{ is a positive integer and } x^2 < 40\}$ in the roster form.

<!-- page 67 -->
**Solution** The required numbers are $1, 2, 3, 4, 5, 6$. So, the given set in the roster form
is $\{1, 2, 3, 4, 5, 6\}$.

Example 3 Write the set $A = \{1, 4, 9, 16, 25, \dots\}$in set-builder form.

Solution We may write the set A as
$$A = \{x : x \text{ is the square of a natural number}\}$$
Alternatively, we can write
$$A = \{x : x = n^2, \text{ where } n \in \mathbf{N}\}$$

Example 4 Write the set $\{\frac{1}{2}, \frac{2}{3}, \frac{3}{4}, \frac{4}{5}, \frac{5}{6}, \frac{6}{7}\}$ in the set-builder form.

Solution We see that each member in the given set has the numerator one less than
the denominator. Also, the numerator begin from 1 and do not exceed 6. Hence, in the
set-builder form the given set is

$$\left\{ x : x = \frac{n}{n+1}, \text{ where } n \text{ is a natural number and } 1 \le n \le 6 \right\}$$

Example 5 Match each of the set on the left described in the roster form with the
same set on the right described in the set-builder form :
(i) $\{ \text{P, R, I, N, C, A, L} \}$ (a) $\{ x : x \text{ is a positive integer and is a divisor of } 18 \}$
(ii) $\{ 0 \}$ (b) $\{ x : x \text{ is an integer and } x^2 - 9 = 0 \}$
(iii) $\{ 1, 2, 3, 6, 9, 18 \}$ (c) $\{ x : x \text{ is an integer and } x + 1 = 1 \}$
(iv) $\{ 3, -3 \}$ (d) $\{ x : x \text{ is a letter of the word PRINCIPAL} \}$

Solution Since in (d), there are 9 letters in the word PRINCIPAL and two letters P and I
are repeated, so (i) matches (d). Similarly, (ii) matches (c) as $x + 1 = 1$ implies
$x = 0$. Also, 1, 2 ,3, 6, 9, 18 are all divisors of 18 and so (iii) matches (a). Finally, $x^2 - 9 = 0$
implies $x = 3, -3$ and so (iv) matches (b).

EXERCISE 1.1

1. Which of the following are sets ? Justify your answer.
(i) The collection of all the months of a year beginning with the letter J.
(ii) The collection of ten most talented writers of India.
(iii) A team of eleven best-cricket batsmen of the world.
(iv) The collection of all boys in your class.
(v) The collection of all natural numbers less than 100.
(vi) A collection of novels written by the writer Munshi Prem Chand.
(vii) The collection of all even integers.

<!-- page 68 -->
(viii) The collection of questions in this Chapter.
(ix) A collection of most dangerous animals of the world.

2. Let $A = \{1, 2, 3, 4, 5, 6\}$. Insert the appropriate symbol $\in$ or $\notin$ in the blank
spaces:

(i)  $5 \dots A$                  (ii)  $8 \dots A$                  (iii)  $0 \dots A$
(iv)  $4 \dots A$                   (v)  $2 \dots A$                   (vi)  $10 \dots A$

3. Write the following sets in roster form:

(i) $A = \{x : x \text{ is an integer and } -3 \leq x < 7\}$
(ii) $B = \{x : x \text{ is a natural number less than } 6\}$
(iii) $C = \{x : x \text{ is a two-digit natural number such that the sum of its digits is } 8\}$
(iv) $D = \{x : x \text{ is a prime number which is divisor of } 60\}$
(v) $E = \text{The set of all letters in the word TRIGONOMETRY}$
(vi) $F = \text{The set of all letters in the word BETTER}$

4. Write the following sets in the set-builder form :

(i) $(3, 6, 9, 12)$ (ii) $\{2,4,8,16,32\}$ (iii) $\{5, 25, 125, 625\}$
(iv) $\{2, 4, 6, \dots\}$ (v) $\{1,4,9, \dots,100\}$

5. List all the elements of the following sets :

(i) $A = \{x : x \text{ is an odd natural number}\}$
(ii) $B = \{x : x \text{ is an integer, } -\frac{1}{2} < x < \frac{9}{2}\}$
(iii) $C = \{x : x \text{ is an integer, } x^2 \leq 4\}$
(iv) $D = \{x : x \text{ is a letter in the word “LOYAL”}\}$
(v) $E = \{x : x \text{ is a month of a year not having 31 days}\}$
(vi) $F = \{x : x \text{ is a consonant in the English alphabet which precedes } k \}$.

6. Match each of the set on the left in the roster form with the same set on the right
described in set-builder form:

(i) $\{1, 2, 3, 6\}$ (a) $\{x : x \text{ is a prime number and a divisor of } 6\}$
(ii) $\{2, 3\}$ (b) $\{x : x \text{ is an odd natural number less than } 10\}$
(iii) $\{M,A,T,H,E,I,C,S\}$ (c) $\{x : x \text{ is natural number and divisor of } 6\}$
(iv) $\{1, 3, 5, 7, 9\}$ (d) $\{x : x \text{ is a letter of the word MATHEMATICS}\}$.

1.3 The Empty Set

Consider the set

$$\text{A} = \{ \ x : x \text{ is a student of Class XI presently studying in a school} \ \}$$
We can go to the school and count the number of students presently studying in
Class XI in the school. Thus, the set A contains a finite number of elements.

We now write another set B as follows:

<!-- page 69 -->
$$\mathrm{B} = \{ x : x \text{ is a student presently studying in both Classes X and XI} \}$$

We observe that a student cannot study simultaneously in both Classes X and XI.
Thus, the set B contains no element at all.

Definition 1 A set which does not contain any element is called the $empty$ $set$ or the
$null$ $set$ or the $void$ $set$.

According to this definition, B is an empty set while A is not an empty set. The
empty set is denoted by the symbol $\phi$ or $\{ \ \ \}$.

We give below a few examples of empty sets.

(i) Let $A = \{x : 1 < x < 2, x \text{ is a natural number}\}$. Then $A$ is the empty set,
because there is no natural number between $1$ and $2$.
(ii) $B = \{x : x^2 - 2 = 0 \text{ and } x \text{ is rational number}\}$. Then $B$ is the empty set because
the equation $x^2 - 2 = 0$ is not satisfied by any rational value of $x$.
(iii) $C = \{x : x \text{ is an even prime number greater than } 2\}$.Then $C$ is the empty set,
because $2$ is the only even prime number.
(iv) $D = \{ x : x^2 = 4, x \text{ is odd } \}$. Then $D$ is the empty set, because the equation
$x^2 = 4$ is not satisfied by any odd value of $x$.

1.4 Finite and Infinite Sets

Let $A = \{1, 2, 3, 4, 5\}, \qquad B = \{a, b, c, d, e, g\}$

and $C = \{ \text{ men living presently in different parts of the world} \}$

We observe that A contains 5 elements and B contains 6 elements. How many elements
does C contain? As it is, we do not know the number of elements in C, but it is some
natural number which may be quite a big number. By number of elements of a set S,
we mean the number of distinct elements of the set and we denote it by $n$ (S). If $n$ (S)
is a natural number, then S is \textit{non-empty finite} set.

Consider the set of natural numbers. We see that the number of elements of this
set is not finite since there are infinite number of natural numbers. We say that the set
of natural numbers is an infinite set. The sets A, B and C given above are finite sets
and $n(\mathrm{A}) = 5$, $n(\mathrm{B}) = 6$ and $n(\mathrm{C}) =$ some finite number.

Definition 2 A set which is empty or consists of a definite number of elements is
called finite otherwise, the set is called infinite.
Consider some examples :
(i) Let W be the set of the days of the week. Then W is finite.
(ii) Let S be the set of solutions of the equation $x^2-16 = 0$. Then S is finite.
(iii) Let G be the set of points on a line. Then G is infinite.
When we represent a set in the roster form, we write all the elements of the set
within braces { }. It is not possible to write all the elements of an infinite set within
braces { } because the numbers of elements of such a set is not finite. So, we represent

<!-- page 70 -->
some infinite set in the roster form by writing a few elements which clearly indicate the
structure of the set followed ( or preceded ) by three dots.

For example, $\{1, 2, 3 \dots\}$ is the set of natural numbers, $\{1, 3, 5, 7, \dots\}$ is the set
of odd natural numbers, $\{\dots, -3, -2, -1, 0, 1, 2, 3, \dots\}$ is the set of integers. All these
sets are infinite.

**Note** All infinite sets cannot be described in the roster form. For example, the
set of real numbers cannot be described in this form, because the elements of this
set do not follow any particular pattern.

Example 6 State which of the following sets are finite or infinite :
(i) $\{x : x \in \text{N} \text{ and } (x - 1) (x - 2) = 0\}$
(ii) $\{x : x \in \text{N} \text{ and } x^2 = 4\}$
(iii) $\{x : x \in \text{N} \text{ and } 2x - 1 = 0\}$
(iv) $\{x : x \in \text{N} \text{ and } x \text{ is prime}\}$
(v) $\{x : x \in \text{N} \text{ and } x \text{ is odd}\}$
Solution (i) Given set = $\{1, 2\}$. Hence, it is finite.
(ii) Given set = $\{2\}$. Hence, it is finite.
(iii) Given set = $\phi$. Hence, it is finite.
(iv) The given set is the set of all prime numbers and since set of prime
numbers is infinite. Hence the given set is infinite
(v) Since there are infinite number of odd numbers, hence, the given set is
infinite.

1.5 Equal Sets

Given two sets A and B, if every element of A is also an element of B and if every
element of B is also an element of A, then the sets A and B are said to be equal.
Clearly, the two sets have exactly the same elements.

Definition 3 Two sets A and B are said to be $equal$ if they have exactly the same
elements and we write A = B. Otherwise, the sets are said to be $unequal$ and we write
A $\neq$ B.

We consider the following examples :

(i) Let $A = \{1, 2, 3, 4\}$ and $B = \{3, 1, 4, 2\}$. Then $A = B$.
(ii) Let $A$ be the set of prime numbers less than 6 and $P$ the set of prime factors
of 30. Then $A$ and $P$ are equal, since 2, 3 and 5 are the only prime factors of
30 and also these are less than 6.

Note A set does not change if one or more elements of the set are repeated.
For example, the sets $A = \{1, 2, 3\}$ and $B = \{2, 2, 1, 3, 3\}$ are equal, since each

<!-- page 71 -->
element of A is in B and vice-versa. That is why we generally do not repeat any
element in describing a set.

Example 7 Find the pairs of equal sets, if any, give reasons:
$$A = \{0\}, \qquad \qquad \qquad B = \{x : x > 15 \text{ and } x < 5\},$$
$$C = \{x : x - 5 = 0 \}, \qquad \quad D = \{x : x^2 = 25\},$$
$$E = \{x : x \text{ is an integral positive root of the equation } x^2 - 2x - 15 = 0\}.$$

Solution Since $0 \in A$ and $0$ does not belong to any of the sets $B$, $C$, $D$ and $E$, it
follows that, $A \neq B$, $A \neq C$, $A \neq D$, $A \neq E$.
Since $B = \phi$ but none of the other sets are empty. Therefore $B \neq C$, $B \neq D$
and $B \neq E$. Also $C = \{5\}$ but $-5 \in D$, hence $C \neq D$.
Since $E = \{5\}$, $C = E$. Further, $D = \{-5, 5\}$ and $E = \{5\}$, we find that, $D \neq E$.
Thus, the only pair of equal sets is $C$ and $E$.

Example 8 Which of the following pairs of sets are equal? Justify your answer.
(i) X, the set of letters in “ALLOY” and B, the set of letters in “LOYAL”.
(ii) A = $\{n : n \in Z \text{ and } n^2 \leq 4\}$ and B = $\{x : x \in R \text{ and } x^2 - 3x + 2 = 0\}$.

Solution (i) We have, $X = \{A, L, L, O, Y\}$, $B = \{L, O, Y, A, L\}$. Then $X$ and $B$ are
equal sets as repetition of elements in a set do not change a set. Thus,

$$X = \{A, L, O, Y\} = B$$

(ii) $A = \{-2, -1, 0, 1, 2\}$, $B = \{1, 2\}$. Since $0 \in A$ and $0 \notin B$, $A$ and $B$ are not equal sets.

EXERCISE 1.2

1. Which of the following are examples of the null set
(i) Set of odd natural numbers divisible by 2
(ii) Set of even prime numbers
(iii) $\{ x : x \text{ is a natural numbers, } x < 5 \text{ and } x > 7 \}$
(iv) $\{ y : y \text{ is a point common to any two parallel lines} \}$
2. Which of the following sets are finite or infinite
(i) The set of months of a year
(ii) $\{1, 2, 3, \dots\}$
(iii) $\{1, 2, 3, \dots .99, 100\}$
(iv) The set of positive integers greater than 100
(v) The set of prime numbers less than 99
3. State whether each of the following set is finite or infinite:
(i) The set of lines which are parallel to the $x$-axis
(ii) The set of letters in the English alphabet
(iii) The set of numbers which are multiple of 5

<!-- page 72 -->
(iv) The set of animals living on the earth
(v) The set of circles passing through the origin $(0,0)$

4. In the following, state whether $A = B$ or not:

(i) $A = \{ a, b, c, d \}$      $B = \{ d, c, b, a \}$
(ii) $A = \{ 4, 8, 12, 16 \}$      $B = \{ 8, 4, 16, 18 \}$
(iii) $A = \{ 2, 4, 6, 8, 10 \}$      $B = \{ x : x \text{ is positive even integer and } x \leq 10 \}$
(iv) $A = \{ x : x \text{ is a multiple of } 10 \},$      $B = \{ 10, 15, 20, 25, 30, \dots \}$

5. Are the following pair of sets equal ? Give reasons.

5.    Are the following pair of sets equal ? Give reasons.
(i) $A = \{2, 3\}$, $B = \{x : x \text{ is solution of } x^2 + 5x + 6 = 0\}$
(ii) $A = \{ x : x \text{ is a letter in the word FOLLOW} \}$
$B = \{ y : y \text{ is a letter in the word WOLF} \}$

6. From the sets given below, select equal sets :
$A = \{ 2, 4, 8, 12 \}, \quad B = \{ 1, 2, 3, 4 \}, \quad C = \{ 4, 8, 12, 14 \}, \quad D = \{ 3, 1, 4, 2 \}$
$E = \{-1, 1 \}, \quad F = \{ 0, a \}, \quad G = \{ 1, -1 \}, \quad H = \{ 0, 1 \}$

1.6 Subsets

Consider the sets : $X =$ set of all students in your school, $Y =$ set of all students in your
class.

We note that every element of $Y$ is also an element of $X$; we say that $Y$ is a subset
of $X$. The fact that $Y$ is subset of $X$ is expressed in symbols as $Y \subset X$. The symbol $\subset$
stands for ‘is a subset of’ or ‘is contained in’.

Definition 4 A set A is said to be a subset of a set B if every element of A is also an
element of B.

In other words, $\mathrm{A} \subset \mathrm{B}$ if whenever $a \in \mathrm{A}$, then $a \in \mathrm{B}$. It is often convenient to
use the symbol “$\Rightarrow$” which means $implies$. Using this symbol, we can write the definiton
of $subset$ as follows:

$$A \subset B \text{ if } a \in A \Rightarrow a \in B$$

We read the above statement as “A is a subset of B if a is an element of A
implies that a is also an element of B”. If A is not a subset of B, we write $A \not\subset B$.

We may note that for A to be a subset of B, all that is needed is that every
element of A is in B. It is possible that every element of B may or may not be in A. If
it so happens that every element of B is also in A, then we shall also have $B \subset A$. In this
case, A and B are the same sets so that we have $A \subset B$ and $B \subset A \Leftrightarrow A = B$, where
“$\Leftrightarrow$” is a symbol for two way implications, and is usually read as *if and only if* (briefly
written as “iff”).

It follows from the above definition that every set $A$ is a subset of itself, i.e.,
$A \subset A$. Since the empty set $\phi$ has no elements, we agree to say that $\phi$ is a subset of
every set. We now consider some examples :

<!-- page 73 -->
(i) The set $\mathbf{Q}$ of rational numbers is a subset of the set $\mathbf{R}$ of real numbes, and
we write $\mathbf{Q} \subset \mathbf{R}$.
(ii) If A is the set of all divisors of 56 and B the set of all prime divisors of 56,
then B is a subset of A and we write $\mathrm{B} \subset \mathrm{A}$.
(iii) Let $\mathrm{A} = \{1, 3, 5\}$ and $\mathrm{B} = \{x : x \text{ is an odd natural number less than } 6\}$. Then
$\mathrm{A} \subset \mathrm{B}$ and $\mathrm{B} \subset \mathrm{A}$ and hence $\mathrm{A} = \mathrm{B}$.
(iv) Let $\mathrm{A} = \{ a, e, i, o, u\}$ and $\mathrm{B} = \{ a, b, c, d\}$. Then $\mathrm{A}$ is not a subset of $\mathrm{B}$,
also $\mathrm{B}$ is not a subset of $\mathrm{A}$.

Let A and B be two sets. If $A \subset B$ and $A \neq B$ , then A is called a \textit{proper subset}
\textit{of} B and B is called \textit{superset} of A. For example,

$A = \{1, 2, 3\}$ is a proper subset of $B = \{1, 2, 3, 4\}$.

If a set A has only one element, we call it a \textit{singleton set}. Thus,$\{ a \}$ is a
singleton set.

Example 9 Consider the sets
$$\phi, A = \{ 1, 3 \}, \quad B = \{ 1, 5, 9 \}, \quad C = \{ 1, 3, 5, 7, 9 \}.$$
Insert the symbol $\subset$ or $\not\subset$ between each of the following pair of sets:

Example 9 Consider the sets
$$\phi, A = \{ 1, 3 \}, \quad B = \{ 1, 5, 9 \}, \quad C = \{ 1, 3, 5, 7, 9 \}.$$
Insert the symbol $\subset$ or $\not\subset$ between each of the following pair of sets:
(i) $\phi \dots B$      (ii) $A \dots B$      (iii) $A \dots C$      (iv) $B \dots C$
Solution (i) $\phi \subset B$ as $\phi$ is a subset of every set.
(ii) $A \not\subset B$ as $3 \in A$ and $3 \not\in B$
(iii) $A \subset C$ as $1, 3 \in A$ also belongs to $C$
(iv) $B \subset C$ as each element of $B$ is also an element of $C$.

Example 10 Let $A = \{ a, e, i, o, u \}$ and $B = \{ a, b, c, d \}$. Is $A$ a subset of $B$ ? No.
(Why?). Is $B$ a subset of $A$? No. (Why?)

Example 11 Let $A, B$ and $C$ be three sets. If $A \in B$ and $B \subset C$, is it true that
$A \subset C$? If not, give an example.

Solution No. Let $A = \{1\}, B = \{\{1\}, 2\}$ and $C = \{\{1\}, 2, 3\}$. Here $A \in B$ as $A = \{1\}$
and $B \subset C$. But $A \not\subset C$ as $1 \in A$ and $1 \notin C$.
Note that an element of a set can never be a subset of itself.

1.6.1 Subsets of set of real numbers

As noted in Section 1.6, there are many important subsets of $\mathbf{R}$. We give below the
names of some of these subsets.

The set of natural numbers $\mathbf{N} = \{1, 2, 3, 4, 5, \dots\}$
The set of integers $\mathbf{Z} = \{\dots, -3, -2, -1, 0, 1, 2, 3, \dots\}$

The set of rational numbers $\mathbf{Q} = \{ x : x = \frac{p}{q} , p, q \in \mathbf{Z} \text{ and } q \neq 0 \}$

<!-- page 74 -->
which is read “ $\mathbf{Q}$ is the set of all numbers $x$ such that $x$ equals the quotient $\frac{p}{q}$ , where
$p$ and $q$ are integers and $q$ is not zero”. Members of $\mathbf{Q}$ include $-5$ (which can be
expressed as $-\frac{5}{1}$ ), $\frac{5}{7}$, $3\frac{1}{2}$ (which can be expressed as $\frac{7}{2}$) and $-\frac{11}{3}$.

The set of irrational numbers, denoted by $\mathbf{T}$, is composed of all other real numbers.
Thus $\quad \mathbf{T} = \{x : x \in \mathbf{R} \text{ and } x \notin \mathbf{Q}\}$, i.e., all real numbers that are not rational.

Members of $\mathbf{T}$ include $\sqrt{2}$ , $\sqrt{5}$ and $\pi$.

Some of the obvious relations among these subsets are:
$$\mathbf{N} \subset \mathbf{Z} \subset \mathbf{Q}, \mathbf{Q} \subset \mathbf{R}, \mathbf{T} \subset \mathbf{R}, \mathbf{N} \not\subset \mathbf{T}.$$

1.6.2 *Intervals as subsets of R* Let $a, b \in \mathbf{R}$ and $a < b$. Then the set of real numbers
$\{ \ y : a < y < b \}$ is called an *open interval* and is denoted by $(a, b)$. All the points
between $a$ and $b$ belong to the open interval $(a, b)$ but $a, b$ themselves do not belong to
this interval.

The interval which contains the end points also is called closed interval and is
denoted by $[ a, b ]$. Thus

$$[a, b] = \{x : a \le x \le b\}$$

We can also have intervals closed at one end and open at the other, i.e.,

$$[ a, b ) = \{ x : a \le x < b \} \text{ is an } \textit{open interval} \text{ from } a \text{ to } b, \text{ including } a \text{ but excluding } b.$$

$(a, b] = \{ x : a < x \le b \}$ is an $open$ $interval$ from $a$ to $b$ including $b$ but excluding $a$.

These notations provide an alternative way of designating the subsets of set of
real numbers. For example , if $A = (-3, 5)$ and $B = [-7, 9]$, then $A \subset B$. The set $[ 0, \infty)$
defines the set of non-negative real numbers, while set $( - \infty, 0 )$ defines the set of
negative real numbers. The set $( - \infty, \infty )$ describes the set of real numbers in relation
to a line extending from $- \infty$ to $\infty$.

On real number line, various types of intervals described above as subsets of $\mathbf{R}$,
are shown in the Fig 1.1.

Fig 1.1

Here, we note that an interval contains infinitely many points.

For example, the set $\{x : x \in \mathbf{R}, -5 < x \leq 7\}$, written in set-builder form, can be
written in the form of interval as $(-5, 7]$ and the interval $[-3, 5)$ can be written in setbuilder form as $\{x : -3 \leq x < 5\}$.

<!-- page 75 -->
The number $(b - a)$ is called the \textit{length of any of the intervals} $(a, b), [a, b],$
$[a, b)$ or $(a, b].$

1.7 Power Set

Consider the set $\{1, 2\}$. Let us write down all the subsets of the set $\{1, 2\}$. We
know that $\phi$ is a subset of every set . So, $\phi$ is a subset of $\{1, 2\}$. We see that $\{1\}$
and $\{ 2 \}$are also subsets of $\{1, 2\}$. Also, we know that every set is a subset of
itself. So, $\{ 1, 2 \}$ is a subset of $\{1, 2\}$. Thus, the set $\{ 1, 2 \}$ has, in all, four
subsets, viz. $\phi, \{ 1 \}, \{ 2 \}$ and $\{ 1, 2 \}$. The set of all these subsets is called the
$power$ $set$ of $\{ 1, 2 \}$.

Definition 5 The collection of all subsets of a set A is called the $power$ $set$ of A. It is
denoted by P(A). In P(A), every element is a set.

Thus, as in above, if $A = \{ 1, 2 \}$, then

$$P(A) = \{ \phi, \{ 1 \}, \{ 2 \}, \{ 1, 2 \} \}$$

Also, note that $n [ \mathrm{P} (\mathrm{A}) ] = 4 = 2^2$

In general, if A  is a set with $n(\mathrm{A}) = m$, then it can be shown that
$n [ \mathrm{P}(\mathrm{A})] = 2^m$.

1.8 Universal Set

Usually, in a particular context, we have to deal with the elements and subsets of a
basic set which is relevant to that particular context. For example, while studying the
system of numbers, we are interested in the set of natural numbers and its subsets such
as the set of all prime numbers, the set of all even numbers, and so forth. This basic set
is called the “*Universal Set*”. The universal set is usually denoted by U, and all its
subsets by the letters A, B, C, etc.

For example, for the set of all integers, the universal set can be the set of rational
numbers or, for that matter, the set $\mathbf{R}$ of real numbers. For another example, in human
population studies, the universal set consists of all the people in the world.

EXERCISE 1.3

1. Make correct statements by filling in the symbols $\subset$ or $\not\subset$ in the blank spaces :
(i) $\{ 2, 3, 4 \} \dots \{ 1, 2, 3, 4, 5 \}$ (ii) $\{ a, b, c \} \dots \{ b, c, d \}$
(iii) $\{ x : x \text{ is a student of Class XI of your school} \} \dots \{ x : x \text{ student of your school} \}$
(iv) $\{ x : x \text{ is a circle in the plane} \} \dots \{ x : x \text{ is a circle in the same plane with}
\text{radius 1 unit} \}$
(v) $\{ x : x \text{ is a triangle in a plane} \} \dots \{ x : x \text{ is a rectangle in the plane} \}$
(vi) $\{ x : x \text{ is an equilateral triangle in a plane} \} \dots \{ x : x \text{ is a triangle in the same plane} \}$
(vii) $\{ x : x \text{ is an even natural number} \} \dots \{ x : x \text{ is an integer} \}$

<!-- page 76 -->
2. Examine whether the following statements are true or false:
(i) $\{ a, b \} \subset \{ b, c, a \}$
(ii) $\{ a, e \} \subset \{ x : x \text{ is a vowel in the English alphabet} \}$
(iii) $\{ 1, 2, 3 \} \subset \{ 1, 3, 5 \}$
(iv) $\{ a \} \subset \{ a, b, c \}$
(v) $\{ a \} \in \{ a, b, c \}$
(vi) $\{ x : x \text{ is an even natural number less than } 6 \} \subset \{ x : x \text{ is a natural number}$
which divides $36 \}$

3. Let $A = \{ 1, 2, \{ 3, 4 \}, 5 \}$. Which of the following statements are incorrect and why?
(i) $\{3, 4\} \subset A$ (ii) $\{3, 4\} \in A$ (iii) $\{ \{3, 4\} \} \subset A$
(iv) $1 \in A$ (v) $1 \subset A$ (vi) $\{1, 2, 5\} \subset A$
(vii) $\{1, 2, 5\} \in A$ (viii) $\{1, 2, 3\} \subset A$ (ix) $\phi \in A$
(x) $\phi \subset A$ (xi) $\{\phi\} \subset A$

4. Write down all the subsets of the following sets
(i) $\{a\}$ (ii) $\{a, b\}$ (iii) $\{1, 2, 3\}$ (iv) $\phi$

5. How many elements has $P(A)$, if $A = \phi$?

6. Write the following as intervals :
(i) $\{x : x \in \mathrm{R}, -4 < x \leq 6\}$ (ii) $\{x : x \in \mathrm{R}, -12 < x < -10\}$
(iii) $\{x : x \in \mathrm{R}, 0 \leq x < 7\}$ (iv) $\{x : x \in \mathrm{R}, 3 \leq x \leq 4\}$

7. Write the following intervals in set-builder form :
(i) $(-3, 0)$ (ii) $[6, 12]$ (iii) $(6, 12]$ (iv) $[-23, 5)$

8. What universal set(s) would you propose for each of the following :
(i) The set of right triangles. (ii) The set of isosceles triangles.

9. Given the sets $A = \{1, 3, 5\}$, $B = \{2, 4, 6\}$ and $C = \{0, 2, 4, 6, 8\}$, which of the
following may be considered as universal set (s) for all the three sets A, B and C
(i) $\{0, 1, 2, 3, 4, 5, 6\}$
(ii) $\phi$
(iii) $\{0,1,2,3,4,5,6,7,8,9,10\}$
(iv) $\{1,2,3,4,5,6,7,8\}$

1.9 Venn Diagrams

Most of the relationships between sets can be
represented by means of diagrams which are known
as $Venn$ $diagrams$. Venn diagrams are named after
the English logician, John Venn (1834-1883). These
diagrams consist of rectangles and closed curves
usually circles. The universal set is represented
usually by a rectangle and its subsets by circles.

In Venn diagrams, the elements of the sets
are written in their respective circles (Figs 1.2 and 1.3)                                   Fig 1.2

<!-- page 77 -->
Illustration 1 In Fig 1.2, $U = \{1,2,3, ..., 10\}$ is the
universal set of which
$A = \{2,4,6,8,10\}$ is a subset.

Illustration 2 In Fig 1.3, $U = \{1,2,3, ..., 10\}$ is the
universal set of which
$A = \{2,4,6,8,10\}$ and $B = \{4, 6\}$ are subsets,
and also $B \subset A$.
The reader will see an extensive use of the
Venn diagrams when we discuss the union, intersection and difference of sets.

1.10 Operations on Sets

In earlier classes, we have learnt how to perform the operations of addition, subtraction,
multiplication and division on numbers. Each one of these operations was performed
on a pair of numbers to get another number. For example, when we perform the
operation of addition on the pair of numbers $5$ and $13$, we get the number $18$. Again,
performing the operation of multiplication on the pair of numbers $5$ and $13$, we get $65$.
Similarly, there are some operations which when performed on two sets give rise to
another set. We will now define certain operations on sets and examine their properties.
Henceforth, we will refer all our sets as subsets of some universal set.

1.10.1 *Union of sets* Let A and B be any two sets. The union of A and B is the set
which consists of all the elements of A and all the elements of B, the common elements
being taken only once. The symbol ‘$\cup$’ is used to denote the *union*. *Symbolically, we*
*write* $A \cup B$ *and usually read as ‘A union B’.

Example 12 Let $A = \{ 2, 4, 6, 8 \}$ and $B = \{ 6, 8, 10, 12 \}$. Find $A \cup B$.

Solution We have $A \cup B = \{ 2, 4, 6, 8, 10, 12 \}$

Note that the common elements 6 and 8 have been taken only once while writing
$A \cup B$.

Example 13 Let $A = \{ a, e, i, o, u \}$ and $B = \{ a, i, u \}$. Show that $A \cup B = A$
Solution We have, $A \cup B = \{ a, e, i, o, u \} = A$.
This example illustrates that union of sets $A$ and its subset $B$ is the set $A$
itself, i.e., if $B \subset A$, then $A \cup B = A$.

Example 14 Let $X = \{ \text{Ram, Geeta, Akbar} \}$ be the set of students of Class XI, who are
in school hockey team. Let $Y = \{ \text{Geeta, David, Ashok} \}$ be the set of students from
Class XI who are in the school football team. Find $X \cup Y$ and interpret the set.

Solution We have, $X \cup Y = \{ \text{Ram, Geeta, Akbar, David, Ashok} \}$. This is the set of
students from Class XI who are in the hockey team or the football team or both.

<!-- page 78 -->
Thus, we can define the union of two sets as follows:

Definition 6 The union of two sets A and B is the set C which consists of all those
elements which are either in A or in B (including
those which are in both). In symbols, we write.
$$A \cup B = \{ x : x \in A \text{ or } x \in B \}$$

The union of two sets can be represented by a
Venn diagram as shown in Fig 1.4.

The shaded portion in Fig 1.4 represents $A \cup B$.

Some Properties of the Operation of Union

(i) $A \cup B = B \cup A$ (Commutative law)
(ii) $( A \cup B ) \cup C = A \cup ( B \cup C )$
(Associative law )
(iii) $A \cup \phi = A$ (Law of identity element, $\phi$ is the identity of $\cup$)
(iv) $A \cup A = A$ (Idempotent law)
(v) $U \cup A = U$ (Law of U)

1.10.2 Intersection of sets The intersection of sets A and B is the set of all elements
which are common to both A and B. The symbol ‘$\cap$’ is used to denote the intersection.
The intersection of two sets A and B is the set of all those elements which belong to
both A and B. Symbolically, we write $A \cap B = \{x : x \in A \text{ and } x \in B\}$.

Example 15 Consider the sets A and B of Example 12. Find $A \cap B$.

Solution We see that 6, 8 are the only elements which are common to both A and B.
Hence $A \cap B = \{ 6, 8 \}$.

Example 16 Consider the sets $X$ and $Y$ of Example 14. Find $X \cap Y$.

Solution We see that element ‘Geeta’ is the only element common to both. Hence,
$$X \cap Y = \{Geeta\}.$$

Example 17 Let $A = \{1, 2, 3, 4, 5, 6, 7, 8, 9, 10\}$ and $B = \{2, 3, 5, 7\}$. Find $A \cap B$ and
hence show that $A \cap B = B$.
Solution We have $A \cap B = \{2, 3, 5, 7\} = B$. We
note that $B \subset A$ and that $A \cap B = B$.
Definition 7 The intersection of two sets $A$ and $B$
is the set of all those elements which belong to both
$A$ and $B$. Symbolically, we write
$A \cap B = \{x : x \in A \text{ and } x \in B\}$
The shaded portion in Fig 1.5 indicates the
intersection of $A$ and $B$.

<!-- page 79 -->
If $A$ and $B$ are two sets such that $A \cap B = \phi$, then
$A$ and $B$ are called \textit{disjoint sets}.

For example, let $A = \{ 2, 4, 6, 8 \}$ and
$B = \{ 1, 3, 5, 7 \}$. Then $A$ and $B$ are disjoint sets,
because there are no elements which are common to
$A$ and $B$. The disjoint sets can be represented by
means of Venn diagram as shown in the Fig 1.6
In the above diagram, $A$ and $B$ are disjoint sets.

Fig 1.6

Some Properties of Operation of Intersection

(i) $A \cap B = B \cap A$ (Commutative law).
(ii) $(A \cap B) \cap C = A \cap (B \cap C)$ (Associative law).
(iii) $\phi \cap A = \phi$, $U \cap A = A$ (Law of $\phi$ and $U$).
(iv) $A \cap A = A$ (Idempotent law)
(v) $A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$ (Distributive law ) i. e.,
$\cap$ distributes over $\cup$

This can be seen easily from the following Venn diagrams [Figs 1.7 (i) to (v)].

(i) (B $\cup$ C)

(iii) $(A \cap B)$

(ii) $A \cap (B \cup C)$

(iv) $(A \cap C)$

(v) $(A \cap B) \cup (A \cap C)$
Figs 1.7 (i) to (v)

<!-- page 80 -->
1.10.3 Difference of sets The difference of the sets A and B in this order is the set
of elements which belong to A but not to B. Symbolically, we write A – B and read as
“A minus B”.

Example 18 Let $A = \{ 1, 2, 3, 4, 5, 6 \}$, $B = \{ 2, 4, 6, 8 \}$. Find $A - B$ and $B - A$.

Solution We have, $A - B = \{ 1, 3, 5 \}$, since the elements $1, 3, 5$ belong to $A$ but
not to $B$ and $B - A = \{ 8 \}$, since the element $8$ belongs to $B$ and not to $A$.
We note that $A - B \neq B - A$.

Example 19 Let $V = \{ a, e, i, o, u \}$ and
$B = \{ a, i, k, u \}$. Find $V - B$ and $B - V$

Solution We have, $\mathrm{V}-\mathrm{B}=\{ e, o \}$, since the elements
$e, o$ belong to $\mathrm{V}$ but not to $\mathrm{B}$ and $\mathrm{B}-\mathrm{V}=\{ k \}$, since
the element $k$ belongs to $\mathrm{B}$ but not to $\mathrm{V}$.

Fig 1.8

We note that $V - B \neq B - V$. Using the setbuilder notation, we can rewrite the definition of
difference as

$$A - B = \{ x : x \in A \text{ and } x \notin B \}$$

The difference of two sets A and B can be
represented by Venn diagram as shown in Fig 1.8.

The shaded portion represents the difference of
the two sets A and B.

Fig 1.9

$\mathit{Remark}$ The sets $A - B$, $A \cap B$ and $B - A$ are
mutually disjoint sets, i.e., the intersection of any of
these two sets is the null set as shown in Fig 1.9.

EXERCISE 1.4

1. Find the union of each of the following pairs of sets :
(i) $X = \{1, 3, 5\}$      $Y = \{1, 2, 3\}$
(ii) $A = [ a, e, i, o, u\}$      $B = \{a, b, c\}$
(iii) $A = \{x : x \text{ is a natural number and multiple of } 3\}$
$B = \{x : x \text{ is a natural number less than } 6\}$
(iv) $A = \{x : x \text{ is a natural number and } 1 < x \le 6 \}$
$B = \{x : x \text{ is a natural number and } 6 < x < 10 \}$
(v) $A = \{1, 2, 3\}, B = \phi$
2. Let $A = \{ a, b \}, B = \{a, b, c\}$. Is $A \subset B$ ? What is $A \cup B$ ?
3. If $A$ and $B$ are two sets such that $A \subset B$, then what is $A \cup B$ ?
4. If $A = \{1, 2, 3, 4\}, B = \{3, 4, 5, 6\}, C = \{5, 6, 7, 8 \}$and $D = \{ 7, 8, 9, 10 \}$; find

<!-- page 81 -->
(i) $A \cup B$          (ii) $A \cup C$          (iii) $B \cup C$          (iv) $B \cup D$
(v) $A \cup B \cup C$     (vi) $A \cup B \cup D$     (vii) $B \cup C \cup D$

5. Find the intersection of each pair of sets of question 1 above.

6. If $A = \{ 3, 5, 7, 9, 11 \}, B = \{ 7, 9, 11, 13 \}, C = \{ 11, 13, 15 \}$ and $D = \{ 15, 17 \}$; find
(i) $A \cap B$ (ii) $B \cap C$ (iii) $A \cap C \cap D$
(iv) $A \cap C$ (v) $B \cap D$ (vi) $A \cap (B \cup C)$
(vii) $A \cap D$ (viii) $A \cap (B \cup D)$ (ix) $(A \cap B) \cap (B \cup C)$
(x) $(A \cup D) \cap (B \cup C)$

7. If A = { $x : x$ is a natural number }, B = { $x : x$ is an even natural number }
C = { $x : x$ is an odd natural number }andD = { $x : x$ is a prime number }, find
(i) A $\cap$ B (ii) A $\cap$ C (iii) A $\cap$ D
(iv) B $\cap$ C (v) B $\cap$ D (vi) C $\cap$ D

8. Which of the following pairs of sets are disjoint

(i) $\{1, 2, 3, 4\}$ and $\{x : x \text{ is a natural number and } 4 \leq x \leq 6 \}$
(ii) $\{ a, e, i, o, u \}$ and $\{ c, d, e, f \}$
(iii) $\{x : x \text{ is an even integer } \}$ and $\{x : x \text{ is an odd integer}\}$

9. If $A = \{3, 6, 9, 12, 15, 18, 21\}, B = \{ 4, 8, 12, 16, 20 \},$
$C = \{ 2, 4, 6, 8, 10, 12, 14, 16 \}, D = \{5, 10, 15, 20 \}$; find
(i) $A - B$          (ii) $A - C$          (iii) $A - D$          (iv) $B - A$
(v) $C - A$          (vi) $D - A$          (vii) $B - C$          (viii) $B - D$
(ix) $C - B$          (x) $D - B$          (xi) $C - D$          (xii) $D - C$

10. If $X = \{ a, b, c, d \}$ and $Y = \{ f, b, d, g \}$, find
(i) $X - Y$ (ii) $Y - X$ (iii) $X \cap Y$

11. If $\mathbf{R}$ is the set of real numbers and $\mathbf{Q}$ is the set of rational numbers, then what is
$\mathbf{R} - \mathbf{Q}$?

12. State whether each of the following statement is true or false. Justify your answer.

(i) $\{ 2, 3, 4, 5 \}$ and $\{ 3, 6 \}$ are disjoint sets.
(ii) $\{ a, e, i, o, u \}$ and $\{ a, b, c, d \}$ are disjoint sets.
(iii) $\{ 2, 6, 10, 14 \}$ and $\{ 3, 7, 11, 15 \}$ are disjoint sets.
(iv) $\{ 2, 6, 10 \}$ and $\{ 3, 7, 11 \}$ are disjoint sets.

1.11 Complement of a Set

Let U be the universal set which consists of all prime numbers and A be the subset of
U which consists of all those prime numbers that are not divisors of 42. Thus,
A = $\{x : x \in \text{ U and } x \text{ is not a divisor of 42 } \}$. We see that $2 \in \text{ U but } 2 \notin \text{ A}$, because
2 is divisor of 42. Similarly, $3 \in \text{ U but } 3 \notin \text{ A}$, and $7 \in \text{ U but } 7 \notin \text{ A}$. Now 2, 3 and 7 are
the only elements of U which do not belong to A. The set of these three prime numbers,
i.e., the set $\{2, 3, 7\}$ is called the \textit{Complement} of A with respect to U, and is denoted by

<!-- page 82 -->
$A'$. So we have $A' = \{2, 3, 7\}$. Thus, we see that
$A' = \{x : x \in U \text{ and } x \notin A \}$. This leads to the following definition.

Definition 8 Let U be the universal set and A a subset of U. Then the complement of
A is the set of all elements of U which are not the elements of A. Symbolically, we
write $A'$ to denote the complement of A with respect to U. Thus,

$A' = \{x : x \in U \text{ and } x \notin A \}$. Obviously $A' = U - A$

We note that the complement of a set A can be looked upon, alternatively, as the
difference between a universal set U and the set A.

Example 20 Let $U = \{1, 2, 3, 4, 5, 6, 7, 8, 9, 10\}$ and $A = \{1, 3, 5, 7, 9\}$. Find $A'$.

Solution We note that 2, 4, 6, 8, 10 are the only elements of U which do not belong to
A. Hence $A' = \{ 2, 4, 6, 8, 10 \}$.

Example 21 Let U be universal set of all the students of Class XI of a coeducational
school and A be the set of all girls in Class XI. Find A'.

Solution Since A is the set of all girls, $A'$ is clearly the set of all boys in the class.

**Note** If A is a subset of the universal set U, then its complement $A'$ is also a
subset of U.
Again in Example 20 above, we have $A' = \{ 2, 4, 6, 8, 10 \}$
Hence $(A')' = \{x : x \in U \text{ and } x \notin A'\}$
$= \{1, 3, 5, 7, 9\} = A$
It is clear from the definition of the complement that for any subset of the universal
set U, we have $(A')' = A$

Now, we want to find the results for ( A $\cup$ B )$'$ and A' $\cap$ B' in the followng
example.

Example 22 Let $U = \{1, 2, 3, 4, 5, 6\}, A = \{2, 3\}$ and $B = \{3, 4, 5\}$.
Find $A', B', A' \cap B', A \cup B$ and hence show that $( A \cup B )' = A' \cap B'$.

Solution Clearly $A' = \{1, 4, 5, 6\}, B' = \{ 1, 2, 6 \}$. Hence $A' \cap B' = \{ 1, 6 \}$
Also $A \cup B = \{ 2, 3, 4, 5 \}$, so that $(A \cup B)' = \{ 1, 6 \}$
$$(A \cup B)' = \{ 1, 6 \} = A' \cap B'$$
It can be shown that the above result is true in general. If $A$ and $B$ are any two
subsets of the universal set $U$, then
$$(A \cup B)' = A' \cap B'. \text{ Similarly, } (A \cap B)' = A' \cup B'. \text{ These two results are stated}$$
in words as follows :

<!-- page 83 -->
The complement of the union of two sets is
the intersection of their complements and the
complement of the intersection of two sets is the
union of their complements. These are called De
Morgan's laws. These are named after the
mathematician De Morgan.

Fig 1.10

The complement $A'$ of a set $A$ can be represented
by a Venn diagram as shown in Fig 1.10.
The shaded portion represents the complement of the set $A$.

Some Properties of Complement Sets

**1. Complement laws:** $\quad$ (i) $A \cup A' = U$ $\quad$ (ii) $A \cap A' = \phi$
**2. De Morgan's law:** $\quad$ (i) $(A \cup B)' = A' \cap B'$ (ii) $(A \cap B)' = A' \cup B'$
**3. Law of double complementation :** $(A')' = A$
**4. Laws of empty set and universal set** $\phi' = U$ and $U' = \phi$.

These laws can be verified by using Venn diagrams.

EXERCISE 1.5

1. Let $U = \{ 1, 2, 3, 4, 5, 6, 7, 8, 9 \}$, $A = \{ 1, 2, 3, 4 \}$, $B = \{ 2, 4, 6, 8 \}$ and
$C = \{ 3, 4, 5, 6 \}$. Find (i) $A'$ (ii) $B'$ (iii) $(A \cup C)'$ (iv) $(A \cup B)'$ (v) $(A')'$
(vi) $(B - C)'$
2. If $U = \{ a, b, c, d, e, f, g, h \}$, find the complements of the following sets :
(i) $A = \{ a, b, c \}$ (ii) $B = \{ d, e, f, g \}$
(iii) $C = \{ a, c, e, g \}$ (iv) $D = \{ f, g, h, a \}$
3. Taking the set of natural numbers as the universal set, write down the complements
of the following sets:
(i) $\{ x : x \text{ is an even natural number} \}$ (ii) $\{ x : x \text{ is an odd natural number} \}$
(iii) $\{ x : x \text{ is a positive multiple of } 3 \}$ (iv) $\{ x : x \text{ is a prime number} \}$
(v) $\{ x : x \text{ is a natural number divisible by } 3 \text{ and } 5 \}$
(vi) $\{ x : x \text{ is a perfect square} \}$ (vii) $\{ x : x \text{ is a perfect cube} \}$
(viii) $\{ x : x + 5 = 8 \}$ (ix) $\{ x : 2x + 5 = 9 \}$
(x) $\{ x : x \geq 7 \}$ (xi) $\{ x : x \in \mathbb{N} \text{ and } 2x + 1 > 10 \}$
4. If $U = \{ 1, 2, 3, 4, 5, 6, 7, 8, 9 \}$, $A = \{ 2, 4, 6, 8 \}$ and $B = \{ 2, 3, 5, 7 \}$. Verify that
(i) $(A \cup B)' = A' \cap B'$ (ii) $(A \cap B)' = A' \cup B'$
5. Draw appropriate Venn diagram for each of the following :
(i) $(A \cup B)'$, (ii) $A' \cap B'$, (iii) $(A \cap B)'$, (iv) $A' \cup B'$
6. Let $U$ be the set of all triangles in a plane. If $A$ is the set of all triangles with at
least one angle different from $60^\circ$, what is $A'$?

<!-- page 84 -->
7. Fill in the blanks to make each of the following a true statement :
(i) $A \cup A' = \dots$ (ii) $\phi' \cap A = \dots$
(iii) $A \cap A' = \dots$ (iv) $U' \cap A = \dots$

1.12 Practical Problems on Union and
Intersection of Two Sets

In earlier Section, we have learnt union, intersection
and difference of two sets. In this Section, we will
go through some practical problems related to our
daily life.The formulae derived in this Section will
also be used in subsequent Chapter on Probability
(Chapter 16).

Fig 1.11

Let $A$ and $B$ be finite sets. If $A \cap B = \phi$, then

(i) $n (\mathrm{A} \cup \mathrm{B}) = n (\mathrm{A}) + n (\mathrm{B}) \quad \dots (1)$

The elements in $A \cup B$ are either in $A$ or in $B$ but not in both as $A \cap B = \phi$. So, (1)
follows immediately.

In general, if A and B are finite sets, then

(ii) $n (\mathrm{A} \cup \mathrm{B} ) = n (\mathrm{A} ) + n (\mathrm{B} ) - n (\mathrm{A} \cap \mathrm{B} )$ ... (2)

Note that the sets $A - B$, $A \cap B$ and $B - A$ are disjoint and their union is $A \cup B$
(Fig 1.11). Therefore

$$\begin{aligned} \\ n (\mathrm{A} \cup \mathrm{B}) &= n (\mathrm{A} - \mathrm{B}) + n (\mathrm{A} \cap \mathrm{B}) + n (\mathrm{B} - \mathrm{A}) \\ \\ &= n (\mathrm{A} - \mathrm{B}) + n (\mathrm{A} \cap \mathrm{B}) + n (\mathrm{B} - \mathrm{A}) + n (\mathrm{A} \cap \mathrm{B}) - n (\mathrm{A} \cap \mathrm{B}) \\ \\ &= n (\mathrm{A}) + n (\mathrm{B}) - n (\mathrm{A} \cap \mathrm{B}), \text{ which verifies (2)} \\ \end{aligned}$$

(iii) If A, B and C are finite sets, then

$$n(\mathrm{A} \cup \mathrm{B} \cup \mathrm{C}) = n(\mathrm{A}) + n(\mathrm{B}) + n(\mathrm{C}) - n(\mathrm{A} \cap \mathrm{B}) - n(\mathrm{B} \cap \mathrm{C})$$
$$- n(\mathrm{A} \cap \mathrm{C}) + n(\mathrm{A} \cap \mathrm{B} \cap \mathrm{C}) \quad \dots (3)$$

In fact, we have

$$n(\mathrm{A} \cup \mathrm{B} \cup \mathrm{C})=n(\mathrm{A})+n(\mathrm{B} \cup \mathrm{C})-n[\mathrm{A} \cap(\mathrm{B} \cup \mathrm{C})] \quad[\text { by }(2)]$$
$$=n(\mathrm{A})+n(\mathrm{B})+n(\mathrm{C})-n(\mathrm{B} \cap \mathrm{C})-n[\mathrm{A} \cap(\mathrm{B} \cup \mathrm{C})] \quad[\text { by }(2)]$$

Since $A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$, we get
$n [A \cap (B \cup C)] = n (A \cap B) + n (A \cap C) - n [(A \cap B) \cap (A \cap C)]$
$= n (A \cap B) + n (A \cap C) - n (A \cap B \cap C)$

Therefore

$$n(\mathrm{A} \cup \mathrm{B} \cup \mathrm{C}) = n(\mathrm{A}) + n(\mathrm{B}) + n(\mathrm{C}) - n(\mathrm{A} \cap \mathrm{B}) - n(\mathrm{B} \cap \mathrm{C})$$
$$- n(\mathrm{A} \cap \mathrm{C}) + n(\mathrm{A} \cap \mathrm{B} \cap \mathrm{C})$$

This proves (3).

Example 23 If $X$ and $Y$ are two sets such that $X \cup Y$ has 50 elements, $X$ has
28 elements and $Y$ has 32 elements, how many elements does $X \cap Y$ have ?

<!-- page 85 -->
Solution Given that

$$n(\mathrm{X} \cup \mathrm{Y}) = 50, n(\mathrm{X}) = 28, n(\mathrm{Y}) = 32,$$
$$n(\mathrm{X} \cap \mathrm{Y}) = ?$$

By using the formula

Fig 1.12

$$n(\mathrm{X} \cup \mathrm{Y}) = n(\mathrm{X}) + n(\mathrm{Y}) - n(\mathrm{X} \cap \mathrm{Y}),$$

we find that

$$n(\mathrm{X} \cap \mathrm{Y}) = n(\mathrm{X}) + n(\mathrm{Y}) - n(\mathrm{X} \cup \mathrm{Y})$$
$$= 28 + 32 - 50 = 10$$

Alternatively, suppose $n ( X \cap Y ) = k$, then

$n(\mathrm{X}-\mathrm{Y})=28-k, n(\mathrm{Y}-\mathrm{X})=32-k$ (by Venn diagram in Fig 1.12)
This gives $50=n(\mathrm{X} \cup \mathrm{Y})=n(\mathrm{X}-\mathrm{Y})+n(\mathrm{X} \cap \mathrm{Y})+n(\mathrm{Y}-\mathrm{X})$
$= (28-k)+k+(32-k)$
nce $k=10$.

Example 24 In a school there are 20 teachers who teach mathematics or physics. Of
these, 12 teach mathematics and 4 teach both physics and mathematics. How many
teach physics ?

Solution Let M denote the set of teachers who teach mathematics and P denote the
set of teachers who teach physics. In the statement of the problem, the word ‘or’ gives
us a clue of union and the word ‘and’ gives us a clue of intersection. We, therefore,
have

$$n (\text{ M } \cup \text{ P }) = 20 , n (\text{ M }) = 12 \text{ and } n (\text{ M } \cap \text{ P }) = 4$$

We wish to determine $n (\text{ P })$.
Using the result

$$n (\text{ M } \cup \text{ P }) = n (\text{ M }) + n (\text{ P }) - n (\text{ M } \cap \text{ P }),$$

we obtain

$$20 = 12 + n (\text{ P }) - 4$$

Thus $n (\text{ P }) = 12$

Hence 12 teachers teach physics.

Hence 12 teachers teach physics.

Example 25 In a class of 35 students, 24 like to play cricket and 16 like to play
football. Also, each student likes to play at least one of the two games. How many
students like to play both cricket and football ?

Solution Let $X$ be the set of students who like to play cricket and $Y$ be the set of
students who like to play football. Then $X \cup Y$ is the set of students who like to play
at least one game, and $X \cap Y$ is the set of students who like to play both games.
Given $n ( X ) = 24, n ( Y ) = 16, n ( X \cup Y ) = 35, n ( X \cap Y ) = ?$
Using the formula $n ( X \cup Y ) = n ( X ) + n ( Y ) - n ( X \cap Y )$, we get
$$35 = 24 + 16 - n ( X \cap Y )$$

<!-- page 86 -->
Thus, $n (\mathrm{X} \cap \mathrm{Y}) = 5$
i.e., 5 students like to play both games.

Example 26 In a survey of 400 students in a school, 100 were listed as taking apple
juice, 150 as taking orange juice and 75 were listed as taking both apple as well as
orange juice. Find how many students were taking neither apple juice nor orange juice.

Solution Let U denote the set of surveyed students and A denote the set of students
taking apple juice and B denote the set of students taking orange juice. Then

$$n (U) = 400, n (A) = 100, n (B) = 150 \text{ and } n (A \cap B) = 75.$$

Now $$n (A' \cap B') = n (A \cup B)'$$
$$= n (U) - n (A) - n (B) + n (A \cap B)$$
$$= 400 - 100 - 150 + 75 = 225$$

Hence 225 students were taking neither apple juice nor orange juice.

**Example 27** There are 200 individuals with a skin disorder, 120 had been exposed to
the chemical $\text{C}_1$, 50 to chemical $\text{C}_2$, and 30 to both the chemicals $\text{C}_1$ and $\text{C}_2$. Find the
number of individuals exposed to

(i) Chemical $\text{C}_1$ but not chemical $\text{C}_2$      (ii) Chemical $\text{C}_2$ but not chemical $\text{C}_1$

(iii) Chemical $\text{C}_1$ or chemical $\text{C}_2$

Solution Let U denote the universal set consisting of individuals suffering from the
skin disorder, A denote the set of individuals exposed to the chemical $\text{C}_1$ and B denote
the set of individuals exposed to the chemical $\text{C}_2$.

Here $n (\text{ U}) = 200, n (\text{ A}) = 120, n (\text{ B}) = 50$ and $n (\text{ A } \cap \text{ B }) = 30$

(i) From the Venn diagram given in Fig 1.13, we have

(i) From the Venn diagram given in Fig 1.13, we have
$$A = (A - B) \cup (A \cap B).$$
$$n(A) = n(A - B) + n(A \cap B)$$ (Since $A - B$) and $A \cap B$ are disjoint.)
or $n(A - B) = n(A) - n(A \cap B) = 120 - 30 = 90$

Hence, the number of individuals exposed to
chemical $\text{C}_1$ but not to chemical $\text{C}_2$ is 90.

(ii) From the Fig 1.13, we have
$$\mathrm{B} = ( \mathrm{B} - \mathrm{A} ) \cup ( \mathrm{A} \cap \mathrm{B} ).$$
and so, $n (\mathrm{B}) = n (\mathrm{B} - \mathrm{A}) + n ( \mathrm{A} \cap \mathrm{B} )$
(Since $\mathrm{B} - \mathrm{A}$ and $\mathrm{A} \cap \mathrm{B}$ are disjoint.)
or $n ( \mathrm{B} - \mathrm{A} ) = n ( \mathrm{B} ) - n ( \mathrm{A} \cap \mathrm{B} )$
$$= 50 - 30 = 20$$

Fig 1.13

<!-- page 87 -->
Thus, the number of individuals exposed to chemical $\text{C}_2$ and not to chemical $\text{C}_1$ is 20.
(iii) The number of individuals exposed either to chemical $\text{C}_1$ or to chemical $\text{C}_2$, i.e.,
$$n (\text{ A } \cup \text{ B }) = n (\text{ A }) + n (\text{ B }) - n (\text{ A } \cap \text{ B })$$
$$= 120 + 50 - 30 = 140.$$

EXERCISE 1.6

1. If X and Y are two sets such that $n(X) = 17$, $n(Y) = 23$ and $n(X \cup Y) = 38$,
find $n(X \cap Y)$.
2. If X and Y are two sets such that $X \cup Y$ has 18 elements, X has 8 elements and
Y has 15 elements ; how many elements does $X \cap Y$ have?
3. In a group of 400 people, 250 can speak Hindi and 200 can speak English. How
many people can speak both Hindi and English?
4. If S and T are two sets such that S has 21 elements, T has 32 elements, and S $\cap$ T
has 11 elements, how many elements does S $\cup$ T have?
5. If X and Y are two sets such that X has 40 elements, $X \cup Y$ has 60 elements and
$X \cap Y$ has 10 elements, how many elements does Y have?
6. In a group of 70 people, 37 like coffee, 52 like tea and each person likes at least
one of the two drinks. How many people like both coffee and tea?
7. In a group of 65 people, 40 like cricket, 10 like both cricket and tennis. How many
like tennis only and not cricket? How many like tennis?
8. In a committee, 50 people speak French, 20 speak Spanish and 10 speak both
Spanish and French. How many speak at least one of these two languages?

Miscellaneous Examples

Example 28 Show that the set of letters needed to spell “ CATARACT ” and the
set of letters needed to spell “ TRACT” are equal.

Solution Let $X$ be the set of letters in “CATARACT”. Then
$$X = \{ C, A, T, R \}$$
Let $Y$ be the set of letters in “ TRACT”. Then
$$Y = \{ T, R, A, C, T \} = \{ T, R, A, C \}$$
Since every element in $X$ is in $Y$ and every element in $Y$ is in $X$. It follows that $X = Y$.

Example 29 List all the subsets of the set $\{ -1, 0, 1 \}$.

Solution Let $A = \{ -1, 0, 1 \}$. The subset of $A$ having no element is the empty
set $\phi$. The subsets of $A$ having one element are $\{ -1 \}, \{ 0 \}, \{ 1 \}$. The subsets of
$A$ having two elements are $\{-1, 0\}, \{-1, 1\}, \{0, 1\}$. The subset of $A$ having three
elements of $A$ is $A$ itself. So, all the subsets of $A$ are $\phi, \{-1\}, \{0\}, \{1\}, \{-1, 0\}, \{-1, 1\},$
$\{0, 1\}$ and $\{-1, 0, 1\}$.

<!-- page 88 -->
Example 30 Show that $A \cup B = A \cap B$ implies $A = B$

Solution Let $a \in A$. Then $a \in A \cup B$. Since $A \cup B = A \cap B$, $a \in A \cap B$. So $a \in B$.
Therefore, $A \subset B$. Similarly, if $b \in B$, then $b \in A \cup B$. Since
$A \cup B = A \cap B$, $b \in A \cap B$. So, $b \in A$. Therefore, $B \subset A$. Thus, $A = B$

Example 31 For any sets A and B, show that
$$P(A \cap B) = P(A) \cap P(B).$$

Solution Let $X \in P(A \cap B)$. Then $X \subset A \cap B$. So, $X \subset A$ and $X \subset B$. Therefore,
$X \in P(A)$ and $X \in P(B)$ which implies $X \in P(A) \cap P(B)$. This gives $P(A \cap B)$
$\subset P(A) \cap P(B)$. Let $Y \in P(A) \cap P(B)$. Then $Y \in P(A)$ and $Y \in P(B)$. So,
$Y \subset A$ and $Y \subset B$. Therefore, $Y \subset A \cap B$, which implies $Y \in P(A \cap B)$. This gives
$P(A) \cap P(B) \subset P(A \cap B)$
Hence $P(A \cap B) = P(A) \cap P(B)$.

Example 32 A market research group conducted a survey of 1000 consumers and
reported that 720 consumers like product A and 450 consumers like product B, what is
the least number that must have liked both products?

Solution Let U be the set of consumers questioned, S be the set of consumers who
liked the product A and T be the set of consumers who like the product B. Given that
$$n( \text{U} ) = 1000, n( \text{S} ) = 720, n( \text{T} ) = 450$$
So $$n( \text{S} \cup \text{T} ) = n( \text{S} ) + n( \text{T} ) - n( \text{S} \cap \text{T} )$$
$$= 720 + 450 - n( \text{S} \cap \text{T} ) = 1170 - n( \text{S} \cap \text{T} )$$
Therefore, $n( \text{S} \cup \text{T} )$ is maximum when $n( \text{S} \cap \text{T} )$ is least. But $\text{S} \cup \text{T} \subset \text{U}$ implies
$$n( \text{S} \cup \text{T} ) \leq n( \text{U} ) = 1000. \text{ So, maximum values of } n( \text{S} \cup \text{T} ) \text{ is 1000. Thus, the least}$$
value of $n( \text{S} \cap \text{T} )$ is 170. Hence, the least number of consumers who liked both products
is 170.

Example 33 Out of 500 car owners investigated, 400 owned car A and 200 owned
car B, 50 owned both A and B cars. Is this data correct?

Solution Let U be the set of car owners investigated, M be the set of persons who
owned car A and S be the set of persons who owned car B.
Given that $n \left( \text{U} \right) = 500, n \left( \text{M} \right) = 400, n \left( \text{S} \right) = 200$ and $n \left( \text{S} \cap \text{M} \right) = 50$.
Then $n \left( \text{S} \cup \text{M} \right) = n \left( \text{S} \right) + n \left( \text{M} \right) - n \left( \text{S} \cap \text{M} \right) = 200 + 400 - 50 = 550$
But $\text{S} \cup \text{M} \subset \text{U}$ implies $n \left( \text{S} \cup \text{M} \right) \le n \left( \text{U} \right)$.
This is a contradiction. So, the given data is incorrect.

Example 34 A college awarded 38 medals in football, 15 in basketball and 20 in
cricket. If these medals went to a total of 58 men and only three men got medals in all
the three sports, how many received medals in exactly two of the three sports ?

<!-- page 89 -->
Solution Let F, B and C denote the set of men who
received medals in football, basketball and cricket,
respectively.
Then $n ( \text{F} ) = 38, n ( \text{B} ) = 15, n ( \text{C} ) = 20$
$n ( \text{F} \cup \text{B} \cup \text{C} ) = 58$ and $n ( \text{F} \cap \text{B} \cap \text{C} ) = 3$
Therefore, $n ( \text{F} \cup \text{B} \cup \text{C} ) = n ( \text{F} ) + n ( \text{B} )$
$+ n ( \text{C} ) - n ( \text{F} \cap \text{B} ) - n ( \text{F} \cap \text{C} ) - n ( \text{B} \cap \text{C} ) +$
$n ( \text{F} \cap \text{B} \cap \text{C} )$,
gives $n ( \text{F} \cap \text{B} ) + n ( \text{F} \cap \text{C} ) + n ( \text{B} \cap \text{C} ) = 18$
Consider the Venn diagram as given in Fig 1.14
Here, $a$ denotes the number of men who got medals in football and basketball only, $b$
denotes the number of men who got medals in football and cricket only, $c$ denotes the
number of men who got medals in basket ball and cricket only and $d$ denotes the
number of men who got medal in all the three. Thus, $d = n ( \text{F} \cap \text{B} \cap \text{C} ) = 3$ and
$a + d + b + d + c + d = 18$
Therefore $a + b + c = 9$,
which is the number of people who got medals in exactly two of the three sports.

which is the number of people who got medals in exactly two of the three sports.

Miscellaneous Exercise on Chapter 1

1. Decide, among the following sets, which sets are subsets of one and another:
$A = \{ x : x \in \mathbf{R} \text{ and } x \text{ satisfy } x^2 - 8x + 12 = 0 \}$,
$B = \{ 2, 4, 6 \}$, $C = \{ 2, 4, 6, 8, \dots \}$, $D = \{ 6 \}$.
2. In each of the following, determine whether the statement is true or false. If it is
true, prove it. If it is false, give an example.

(i) If $x \in A$ and $A \in B$, then $x \in B$
(ii) If $A \subset B$ and $B \in C$, then $A \in C$
(iii) If $A \subset B$ and $B \subset C$, then $A \subset C$
(iv) If $A \not\subset B$ and $B \not\subset C$, then $A \not\subset C$
(v) If $x \in A$ and $A \not\subset B$, then $x \in B$
(vi) If $A \subset B$ and $x \notin B$, then $x \notin A$

3. Let $A$, $B$, and $C$ be the sets such that $A \cup B = A \cup C$ and $A \cap B = A \cap C$. Show
that $B = C$.
4. Show that the following four conditions are equivalent :

(i) $A \subset B$ (ii) $A - B = \phi$ (iii) $A \cup B = B$ (iv) $A \cap B = A$

5. Show that if $A \subset B$, then $C - B \subset C - A$.
6. Assume that $P(A) = P(B)$. Show that $A = B$
7. Is it true that for any sets $A$ and $B$, $P(A) \cup P(B) = P(A \cup B)$? Justify your
answer.

<!-- page 90 -->
8. Show that for any sets A and B,
$A = ( A \cap B ) \cup ( A - B )$ and $A \cup ( B - A ) = ( A \cup B )$
9. Using properties of sets, show that
(i) $A \cup ( A \cap B ) = A$ (ii) $A \cap ( A \cup B ) = A$.
10. Show that $A \cap B = A \cap C$ need not imply $B = C$.
11. Let A and B be sets. If $A \cap X = B \cap X = \phi$ and $A \cup X = B \cup X$ for some set
X, show that $A = B$.
(Hints $A = A \cap ( A \cup X )$, $B = B \cap ( B \cup X )$ and use Distributive law )
12. Find sets A, B and C such that $A \cap B$, $B \cap C$ and $A \cap C$ are non-empty
sets and $A \cap B \cap C = \phi$.
13. In a survey of 600 students in a school, 150 students were found to be taking tea
and 225 taking coffee, 100 were taking both tea and coffee. Find how many
students were taking neither tea nor coffee?
14. In a group of students, 100 students know Hindi, 50 know English and 25 know
both. Each of the students knows either Hindi or English. How many students
are there in the group?
15. In a survey of 60 people, it was found that 25 people read newspaper H, 26 read
newspaper T, 26 read newspaper I, 9 read both H and I, 11 read both H and T,
8 read both T and I, 3 read all three newspapers. Find:
(i) the number of people who read at least one of the newspapers.
(ii) the number of people who read exactly one newspaper.
16. In a survey it was found that 21 people liked product A, 26 liked product B and
29 liked product C. If 14 people liked products A and B, 12 people liked products
C and A, 14 people liked products B and C and 8 liked all the three products.
Find how many liked product C only.

Summary

This chapter deals with some basic definitions and operations involving sets. These
are summarised below:
$\diamond$ A set is a well-defined collection of objects.
$\diamond$ A set which does not contain any element is called empty set.
$\diamond$ A set which consists of a definite number of elements is called finite set,
otherwise, the set is called infinite set.
$\diamond$ Two sets A and B are said to be equal if they have exactly the same elements.
$\diamond$ A set A is said to be subset of a set B, if every element of A is also an element
of B. Intervals are subsets of $\mathbf{R}$.
$\diamond$ A power set of a set A is collection of all subsets of A. It is denoted by P(A).

<!-- page 91 -->
The union of two sets A and B is the set of all those elements which are either
in A or in B.
The intersection of two sets A and B is the set of all elements which are
common. The difference of two sets A and B in this order is the set of elements
which belong to A but not to B.
The complement of a subset A of universal set U is the set of all elements of U
which are not the elements of A.
For any two sets A and B, $(A \cup B)' = A' \cap B'$ and $( A \cap B )' = A' \cup B'$
If A and B are finite sets such that $A \cap B = \phi$, then
$n (A \cup B) = n (A) + n (B)$.
If $A \cap B \neq \phi$, then
$n (A \cup B) = n (A) + n (B) - n (A \cap B)$

Historical Note

The modern theory of sets is considered to have been originated largely by the
German mathematician Georg Cantor (1845-1918). His papers on set theory
appeared sometimes during 1874 to 1897. His study of set theory came when he
was studying trigonometric series of the form $a_1 \sin x + a_2 \sin 2x + a_3 \sin 3x + ...$
He published in a paper in 1874 that the set of real numbers could not be put into
one-to-one correspondence wih the integers. From 1879 onwards, he publishd
several papers showing various properties of abstract sets.
Cantor’s work was well received by another famous mathematician Richard
Dedekind (1831-1916). But Kronecker (1810-1893) castigated him for regarding
infinite set the same way as finite sets. Another German mathematician Gottlob
Frege, at the turn of the century, presented the set theory as principles of logic.
Till then the entire set theory was based on the assumption of the existence of the
set of all sets. It was the famous Englih Philosopher Bertand Russell (18721970 ) who showed in 1902 that the assumption of existence of a set of all sets
leads to a contradiction. This led to the famous Russell’s Paradox. Paul R.Halmos
writes about it in his book ‘Naïve Set Theory’ that “nothing contains everything”.
The Russell’s Paradox was not the only one which arose in set theory.
Many paradoxes were produced later by several mathematicians and logicians.

<!-- page 92 -->
As a consequence of all these paradoxes, the first axiomatisation of set theory
was published in 1908 by Ernst Zermelo. Another one was proposed by Abraham
Fraenkel in 1922. John Von Neumann in 1925 introduced explicitly the axiom of
regularity. Later in 1937 Paul Bernays gave a set of more satisfactory
axiomatisation. A modification of these axioms was done by Kurt Gödel in his
monograph in 1940. This was known as Von Neumann-Bernays (VNB) or GödelBernays (GB) set theory.
    Despite all these difficulties, Cantor’s set theory is used in present day
mathematics. In fact, these days most of the concepts and results in mathematics
are expressed in the set theoretic language.

<!-- page 93 -->
RELATIONS AND FUNCTIONS

❖ Mathematics is the indispensable instrument of
all physical research. – BERTHELOT ❖

2.1 Introduction

Much of mathematics is about finding a pattern – a
recognisable link between quantities that change. In our
daily life, we come across many patterns that characterise
relations such as brother and sister, father and son, teacher
and student. In mathematics also, we come across many
relations such as number $m$ is less than number $n$, line $l$ is
parallel to line $m$, set A is a subset of set B. In all these, we
notice that a relation involves pairs of objects in certain
order. In this Chapter, we will learn how to link pairs of
objects from two sets and then introduce relations between
the two objects in the pair. Finally, we will learn about
special relations which will qualify to be functions. The
concept of function is very important in mathematics since it captures the idea of a
mathematically precise correspondence between one quantity with the other.

G. W. Leibnitz
(1646–1716)

2.2 Cartesian Products of Sets

Suppose A is a set of 2 colours and B is a set of 3 objects, i.e.,

$$A = \{red, blue\}and B = \{b, c, s\},$$

where $b$, $c$ and $s$ represent a particular bag, coat and shirt, respectively.

How many pairs of coloured objects can be made from these two sets?

Proceeding in a very orderly manner, we can see that there will be 6
distinct pairs as given below:

(red, $b$), (red, $c$), (red, $s$), (blue, $b$), (blue, $c$), (blue, $s$).

Fig 2.1

Thus, we get 6 distinct objects (Fig 2.1).

Let us recall from our earlier classes that an ordered pair of elements
taken from any two sets $P$ and $Q$ is a pair of elements written in small

<!-- page 94 -->
brackets and grouped together in a particular order, i.e., $(p,q), p \in \mathrm{P}$ and $q \in \mathrm{Q}$ . This
leads to the following definition:

Definition 1 Given two non-empty sets $P$ and $Q$. The cartesian product $P \times Q$ is the
set of all ordered pairs of elements from $P$ and $Q$, i.e.,

$$\mathrm{P} \times \mathrm{Q} = \{ (p,q) : p \in \mathrm{P}, q \in \mathrm{Q} \}$$

If either $P$ or $Q$ is the null set, then $P \times Q$ will also be empty set, i.e., $P \times Q = \phi$
From the illustration given above we note that

$$A \times B = \{(\text{red},b), (\text{red},c), (\text{red},s), (\text{blue},b), (\text{blue},c), (\text{blue},s)\}.$$

Again, consider the two sets:

A = {DL, MP, KA}, where DL, MP, KA represent Delhi,
Madhya Pradesh and Karnataka, respectively and B = {01,02,
03}representing codes for the licence plates of vehicles issued
by DL, MP and KA .

Fig 2.2

If the three states, Delhi, Madhya Pradesh and Karnataka
were making codes for the licence plates of vehicles, with the
restriction that the code begins with an element from set A,
which are the pairs available from these sets and how many such
pairs will there be (Fig 2.2)?

The available pairs are:(DL,01), (DL,02), (DL,03), (MP,01), (MP,02), (MP,03),
(KA,01), (KA,02), (KA,03) and the product of set A and set B is given by
$$A \times B = \{(DL,01), (DL,02), (DL,03), (MP,01), (MP,02), (MP,03), (KA,01), (KA,02),$$
$$(KA,03)\}.$$

It can easily be seen that there will be 9 such pairs in the Cartesian product, since
there are 3 elements in each of the sets A and B. This gives us 9 possible codes. Also
note that the order in which these elements are paired is crucial. For example, the code
(DL, 01) will not be the same as the code (01, DL).

As a final illustration, consider the two sets A= $\{a_1, a_2\}$ and
B = $\{b_1, b_2, b_3, b_4\}$ (Fig 2.3).

$$\mathrm{A} \times \mathrm{B} = \{ ( \ a_1, \ b_1), \ (a_1, \ b_2), \ (a_1, \ b_3), \ (a_1, \ b_4), \ (a_2, \ b_1), \ (a_2, \ b_2),$$
$$(a_2, \ b_3), \ (a_2, \ b_4) \}.$$

Fig 2.3

The 8 ordered pairs thus formed can represent the position of points in
the plane if A and B are subsets of the set of real numbers and it is
obvious that the point in the position $(a_1, b_2)$ will be distinct from the point
in the position $(b_2, a_1)$.

Remarks

(i) Two ordered pairs are equal, if and only if the corresponding first elements
are equal and the second elements are also equal.

<!-- page 95 -->
(ii) If there are $p$ elements in A and $q$ elements in B, then there will be $pq$
elements in $A \times B$, i.e., if $n(A) = p$ and $n(B) = q$, then $n(A \times B) = pq$.
(iii) If A and B are non-empty sets and either A or B is an infinite set, then so is
$A \times B$.
(iv) $A \times A \times A = \{(a, b, c) : a, b, c \in A\}$. Here $(a, b, c)$ is called an ordered
triplet.

Example 1 If $(x+1, y-2) = (3,1)$, find the values of $x$ and $y$.

Solution Since the ordered pairs are equal, the corresponding elements are equal.

Therefore $x + 1 = 3$ and $y - 2 = 1$.
Solving we get $x = 2$ and $y = 3$.

Example 2 If $P = \{a, b, c\}$ and $Q = \{r\}$, form the sets $P \times Q$ and $Q \times P$.
Are these two products equal?

Solution By the definition of the cartesian product,
$$P \times Q = \{(a, r), (b, r), (c, r)\} \text{ and } Q \times P = \{(r, a), (r, b), (r, c)\}$$
Since, by the definition of equality of ordered pairs, the pair $(a, r)$ is not equal to the pair
$(r, a)$, we conclude that $P \times Q \neq Q \times P$.
However, the number of elements in each set will be the same.

However, the number of elements in each set will be the same.

Example 3 Let $A = \{1,2,3\}$, $B = \{3,4\}$ and $C = \{4,5,6\}$. Find
(i) $A \times (B \cap C)$ (ii) $(A \times B) \cap (A \times C)$
(iii) $A \times (B \cup C)$ (iv) $(A \times B) \cup (A \times C)$

Solution (i) By the definition of the intersection of two sets, $(B \cap C) = \{4\}$.
Therefore, $A \times (B \cap C) = \{(1,4), (2,4), (3,4)\}$.
(ii) Now $(A \times B) = \{(1,3), (1,4), (2,3), (2,4), (3,3), (3,4)\}$
and $(A \times C) = \{(1,4), (1,5), (1,6), (2,4), (2,5), (2,6), (3,4), (3,5), (3,6)\}$
Therefore, $(A \times B) \cap (A \times C) = \{(1, 4), (2, 4), (3, 4)\}$.

(iii) Since, $(B \cup C) = \{3, 4, 5, 6\}$, we have
$A \times (B \cup C) = \{(1,3), (1,4), (1,5), (1,6), (2,3), (2,4), (2,5), (2,6), (3,3),$
$(3,4), (3,5), (3,6)\}$.

(iv) Using the sets $A \times B$ and $A \times C$ from part (ii) above, we obtain
$(A \times B) \cup (A \times C) = \{(1,3), (1,4), (1,5), (1,6), (2,3), (2,4), (2,5), (2,6),$
$(3,3), (3,4), (3,5), (3,6)\}$.

<!-- page 96 -->
Example 4 If $P = \{1, 2\}$, form the set $P \times P \times P$.

Solution We have, $P \times P \times P = \{(1,1,1), (1,1,2), (1,2,1), (1,2,2), (2,1,1), (2,1,2), (2,2,1),$
$(2,2,2)\}.$

Example 5 If $\mathbf{R}$ is the set of all real numbers, what do the cartesian products $\mathbf{R} \times \mathbf{R}$
and $\mathbf{R} \times \mathbf{R} \times \mathbf{R}$ represent?

Solution The Cartesian product $\mathbf{R} \times \mathbf{R}$ represents the set $\mathbf{R} \times \mathbf{R} = \{(x, y) : x, y \in \mathbf{R}\}$
which represents the coordinates of all the points in two dimensional space and the
cartesian product $\mathbf{R} \times \mathbf{R} \times \mathbf{R}$ represents the set $\mathbf{R} \times \mathbf{R} \times \mathbf{R} = \{(x, y, z) : x, y, z \in \mathbf{R}\}$
which represents the coordinates of all the points in three-dimensional space.

Example 6 If $A \times B = \{(p, q), (p, r), (m, q), (m, r)\}$, find A and B.

Solution
A = set of first elements = $\{p, m\}$
B = set of second elements = $\{q, r\}$.

EXERCISE 2.1

1. If $\left(\frac{x}{3}+1, y-\frac{2}{3}\right)=\left(\frac{5}{3}, \frac{1}{3}\right)$, find the values of $x$ and $y$.
2. If the set A has 3 elements and the set B = $\{3, 4, 5\}$, then find the number of
elements in (A$\times$B).
3. If G = $\{7, 8\}$ and H = $\{5, 4, 2\}$, find G $\times$ H and H $\times$ G.
4. State whether each of the following statements are true or false. If the statement
is false, rewrite the given statement correctly.
(i) If P = $\{m, n\}$ and Q = $\{n, m\}$, then P $\times$ Q = $\{(m, n), (n, m)\}$.
(ii) If A and B are non-empty sets, then A $\times$ B is a non-empty set of ordered
pairs $(x, y)$ such that $x \in$ A and $y \in$ B.
(iii) If A = $\{1, 2\}$, B = $\{3, 4\}$, then A $\times$ (B $\cap$ $\phi$) = $\phi$.
5. If A = $\{-1, 1\}$, find A $\times$ A $\times$ A.
6. If A $\times$ B = $\{(a, x), (a, y), (b, x), (b, y)\}$. Find A and B.
7. Let A = $\{1, 2\}$, B = $\{1, 2, 3, 4\}$, C = $\{5, 6\}$ and D = $\{5, 6, 7, 8\}$. Verify that
(i) A $\times$ (B $\cap$ C) = (A $\times$ B) $\cap$ (A $\times$ C). (ii) A $\times$ C is a subset of B $\times$ D.
8. Let A = $\{1, 2\}$ and B = $\{3, 4\}$. Write A $\times$ B. How many subsets will A $\times$ B have?
List them.
9. Let A and B be two sets such that $n(\text{A}) = 3$ and $n(\text{B}) = 2$. If $(x, 1), (y, 2), (z, 1)$
are in A $\times$ B, find A and B, where $x, y$ and $z$ are distinct elements.

<!-- page 97 -->
10. The Cartesian product $A \times A$ has 9 elements among which are found $(-1, 0)$ and
$(0,1)$. Find the set $A$ and the remaining elements of $A \times A$.

2.3 Relations

Consider the two sets $P = \{a, b, c\}$ and $Q = \{Ali, Bhanu, Binoy, Chandra, Divya\}$.
The cartesian product of
$P$ and $Q$ has 15 ordered pairs which
can be listed as $P \times Q = \{(a, Ali),$
$(a, Bhanu), (a, Binoy), ..., (c, Divya)\}$.
We can now obtain a subset of
$P \times Q$ by introducing a relation $R$
between the first element $x$ and the
second element $y$ of each ordered pair
$(x, y)$ as

$\begin{matrix} \mathbf{P} & \mathbf{Q} \end{matrix}$
$\bullet a$
$\bullet b$
$\bullet c$
$\bullet Ali$
$\bullet Bhanu$
$\bullet Binoy$
$\bullet Chandra$
$\bullet Divya$

R= { $(x,y): x$ is the first letter of the name $y, x \in \mathrm{P}, y \in \mathrm{Q}$}.
Then $\mathrm{R} = \{(a, \mathrm{Ali}), (b, \mathrm{Bhanu}), (b, \mathrm{Binoy}), (c, \mathrm{Chandra})\}$
A visual representation of this relation $\mathrm{R}$ (called an arrow diagram) is shown
in Fig 2.4.

Definition 2 A relation R from a non-empty set A to a non-empty set B is a subset of
the cartesian product $A \times B$. The subset is derived by describing a relationship between
the first element and the second element of the ordered pairs in $A \times B$. The second
element is called the $image$ of the first element.

Definition 3 The set of all first elements of the ordered pairs in a relation R from a set
A to a set B is called the $domain$ of the relation R.

Definition 4 The set of all second elements in a relation R from a set A to a set B is
called the range of the relation R. The whole set B is called the codomain of the
relation R. Note that range $\subset$ codomain.

Remarks (i) A relation may be represented algebraically either by the Roster
method or by the Set-builder method.
(ii) An arrow diagram is a visual representation of a relation.

Example 7 Let $A = \{1, 2, 3, 4, 5, 6\}$. Define a relation $R$ from $A$ to $A$ by
$$R = \{(x, y) : y = x + 1 \}$$
(i) Depict this relation using an arrow diagram.
(ii) Write down the domain, codomain and range of $R$.

Solution (i) By the definition of the relation,
$$R = \{(1,2), (2,3), (3,4), (4,5), (5,6)\}.$$

<!-- page 98 -->
The corresponding arrow diagram is
shown in Fig 2.5.

(ii) We can see that the
domain = { 1, 2, 3, 4, 5, }
Similarly, the range = { 2, 3, 4, 5, 6 }
and the codomain = { 1, 2, 3, 4, 5, 6 }.

Fig 2.5

Example 8 The Fig 2.6 shows a relation
between the sets P and Q. Write this relation (i) in set-builder form, (ii) in roster form.
What is its domain and range?

Solution It is obvious that the relation R is
“$x$ is the square of y”.

Fig 2.6

(i) In set-builder form, $R = \{(x, y) : x$
is the square of $y, x \in P, y \in \mathbf{Q}\}$
(ii) In roster form, $R = \{(9, 3),$
$(9, -3), (4, 2), (4, -2), (25, 5), (25, -5)\}$

The domain of this relation is $\{4, 9, 25\}$.

The range of this relation is $\{-2, 2, -3, 3, -5, 5\}$.

Note that the element 1 is not related to any element in set P.

The set $Q$ is the codomain of this relation.

Note The total number of relations that can be defined from a set A to a set B
is the number of possible subsets of A $\times$ B. If $n(\text{A}) = p$ and $n(\text{B}) = q$, then
$n (\text{A} \times \text{B}) = pq$ and the total number of relations is $2^{pq}$.

Example 9 Let $A = \{1, 2\}$ and $B = \{3, 4\}$. Find the number of relations from A to B.

Solution We have,
$$A \times B = \{(1, 3), (1, 4), (2, 3), (2, 4)\}.$$
Since $n$ $(A \times B ) = 4$, the number of subsets of $A \times B$ is $2^4$. Therefore, the number of
relations from A into B will be $2^4$.

Remark A relation R from A to A is also stated as a relation on A.

Remark A relation R from A to A is also stated as a relation on A.

EXERCISE 2.2

1. Let $A = \{1, 2, 3,...,14\}$. Define a relation $R$ from $A$ to $A$ by
$R = \{(x, y) : 3x - y = 0, \text{ where } x, y \in A\}$. Write down its domain, codomain and
range.

<!-- page 99 -->
2. Define a relation R on the set $\mathbf{N}$ of natural numbers by $\mathrm{R} = \{(x, y) : y = x + 5,$
$x$ is a natural number less than 4; $x, y \in \mathbf{N}\}$. Depict this relationship using roster
form. Write down the domain and the range.

3. $A = \{1, 2, 3, 5\}$ and $B = \{4, 6, 9\}$. Define a relation $R$ from $A$ to $B$ by
$R = \{(x, y):$ the difference between $x$ and $y$ is odd; $x \in A, y \in B\}$. Write $R$ in
roster form.

4. The Fig2.7 shows a relationship
between the sets P and Q. Write this
relation

(i) in set-builder form (ii) roster form.
What is its domain and range?

Fig 2.7

5. Let $A = \{1, 2, 3, 4, 6\}$. Let $R$ be the
relation on $A$ defined by
$\{(a, b): a , b \in A, b \text{ is exactly divisible by } a\}$.

(i) Write $R$ in roster form

(ii) Find the domain of $R$

(iii) Find the range of $R$.

6. Determine the domain and range of the relation R defined by
$$R = \{(x, x + 5) : x \in \{0, 1, 2, 3, 4, 5\}\}.$$

7. Write the relation $\text{R} = \{(x, x^3) : x \text{ is a prime number less than } 10\}$ in roster form.
8. Let $\text{A} = \{x, y, z\}$ and $\text{B} = \{1, 2\}$. Find the number of relations from $\text{A}$ to $\text{B}$.

9. Let R be the relation on $\mathbf{Z}$ defined by $\mathrm{R} = \{(a,b): a, \ b \in \mathbf{Z}, \ a - b \text{ is an integer}\}$.
Find the domain and range of $\mathrm{R}$.

2.4 Functions

In this Section, we study a special type of relation called \textit{function}. It is one of the most
important concepts in mathematics. We can, visualise a function as a rule, which produces
new elements out of some given elements. There are many terms such as ‘map’ or
‘mapping’ used to denote a function.

Definition 5 A relation $f$ from a set A to a set B is said to be a $function$ if every
element of set A has one and only one image in set B.

In other words, a function $f$ is a relation from a non-empty set A to a non-empty
set B such that the domain of $f$ is A and no two distinct ordered pairs in $f$ have the
same first element.

If $f$ is a function from A to B and $(a, b) \in f$, then $f(a) = b$, where $b$ is called the
image of $a$ under $f$ and $a$ is called the preimage of $b$ under $f$.

<!-- page 100 -->
The function $f$ from A to B is denoted by $f$: A $\rightarrow$ B.

Looking at the previous examples, we can easily see that the relation in Example 7 is
not a function because the element 6 has no image.

Again, the relation in Example 8 is not a function because the elements in the
domain are connected to more than one images. Similarly, the relation in Example 9 is
also not a function. ($Why?$) In the examples given below, we will see many more
relations some of which are functions and others are not.

Example 10 Let $\mathbf{N}$ be the set of natural numbers and the relation $\mathrm{R}$ be defined on
$\mathrm{N}$ such that $\mathrm{R} = \{(x, y) : y = 2x, x, y \in \mathbf{N}\}$.

What is the domain, codomain and range of R? Is this relation a function?

Solution The domain of R is the set of natural numbers $\mathbf{N}$. The codomain is also $\mathbf{N}$.
The range is the set of even natural numbers.

Since every natural number $n$ has one and only one image, this relation is a
function.

Example 11 Examine each of the following relations given below and state in each
case, giving reasons whether it is a function or not?
(i) $R = \{(2,1),(3,1), (4,2)\}$, (ii) $R = \{(2,2),(2,4),(3,3), (4,4)\}$
(iii) $R = \{(1,2),(2,3),(3,4), (4,5), (5,6), (6,7)\}$

Solution (i) Since 2, 3, 4 are the elements of domain of R having their unique images,
this relation R is a function.
(ii) Since the same first element 2 corresponds to two different images 2
and 4, this relation is not a function.
(iii) Since every element has one and only one image, this relation is a
function.

Definition 6 A function which has either R or one of its subsets as its range is called
a real valued function. Further, if its domain is also either R or a subset of R, it is
called a real function.

Example 12 Let $\mathbf{N}$ be the set of natural numbers. Define a real valued function

$f : \mathbf{N} \rightarrow \mathbf{N} \text{ by } f(x) = 2x + 1$. Using this definition, complete the table given below.

<table>
<thead>
<tr>
<th>x</th>
<th>1</th>
<th>2</th>
<th>3</th>
<th>4</th>
<th>5</th>
<th>6</th>
<th>7</th>
</tr>
</thead>
<tbody>
<tr>
<td>y</td>
<td>f (1) = ...</td>
<td>f (2) = ...</td>
<td>f (3) = ...</td>
<td>f (4) = ...</td>
<td>f (5) = ...</td>
<td>f (6) = ...</td>
<td>f (7) = ...</td>
</tr>
</tbody>
</table>

Solution The completed table is given by

<table>
<thead>
<tr>
<th>x</th>
<th>1</th>
<th>2</th>
<th>3</th>
<th>4</th>
<th>5</th>
<th>6</th>
<th>7</th>
</tr>
</thead>
<tbody>
<tr>
<td>y</td>
<td>f(1) = 3</td>
<td>f(2) = 5</td>
<td>f(3) = 7</td>
<td>f(4) = 9</td>
<td>f(5) = 11</td>
<td>f(6) = 13</td>
<td>f(7) =15</td>
</tr>
</tbody>
</table>

<!-- page 101 -->
2.4.1 Some functions and their graphs

(i) **Identity function** Let $\mathbf{R}$ be the set of real numbers. Define the real valued
function $f : \mathbf{R} \rightarrow \mathbf{R}$ by $y = f(x) = x$ for each $x \in \mathbf{R}$. Such a function is called the
*identity function*. Here the domain and range of $f$ are $\mathbf{R}$. The graph is a straight line as
shown in Fig 2.8. It passes through the origin.

Fig 2.8

(ii) **Constant function** Define the function $f: \mathbf{R} \rightarrow \mathbf{R}$ by $y = f(x) = c, x \in \mathbf{R}$ where
$c$ is a constant and each $x \in \mathbf{R}$. Here domain of $f$ is $\mathbf{R}$ and its range is $\{c\}$.

Fig 2.9

<!-- page 102 -->
The graph is a line parallel to $x$-axis. For example, if $f(x)=3$ for each $x \in \mathbf{R}$, then its
graph will be a line as shown in the Fig 2.9.

(iii) **Polynomial function** A function $f : \mathbf{R} \rightarrow \mathbf{R}$ is said to be *polynomial function* if
for each $x$ in $\mathbf{R}$, $y = f(x) = a_0 + a_1x + a_2x^2 + ... + a_nx^n$, where $n$ is a non-negative
integer and $a_0, a_1, a_2, ..., a_n \in \mathbf{R}$.

The functions defined by $f(x) = x^3 - x^2 + 2$, and $g(x) = x^4 + \sqrt{2} x$ are some examples

of polynomial functions, whereas the function $h$ defined by $h(x) = x^{\frac{2}{3}} + 2x$ is not a
polynomial function.($Why?$)

Example 13 Define the function $f: \mathbf{R} \rightarrow \mathbf{R}$ by $y = f(x) = x^2$, $x \in \mathbf{R}$. Complete the
Table given below by using this definition. What is the domain and range of this function?
Draw the graph of $f$.

<table>
<thead>
<tr>
<th>x</th>
<th>-4</th>
<th>-3</th>
<th>-2</th>
<th>-1</th>
<th>0</th>
<th>1</th>
<th>2</th>
<th>3</th>
<th>4</th>
</tr>
</thead>
<tbody>
<tr>
<td>y = f(x) = x²</td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
</tbody>
</table>

Solution The completed Table is given below:

<table>
<thead>
<tr>
<th>x</th>
<th>−4</th>
<th>−3</th>
<th>−2</th>
<th>−1</th>
<th>0</th>
<th>1</th>
<th>2</th>
<th>3</th>
<th>4</th>
</tr>
</thead>
<tbody>
<tr>
<td>y = f (x) = x²</td>
<td>16</td>
<td>9</td>
<td>4</td>
<td>1</td>
<td>0</td>
<td>1</td>
<td>4</td>
<td>9</td>
<td>16</td>
</tr>
</tbody>
</table>

Domain of $f = \{x : x \in \mathbf{R}\}$. Range of $f = \{x^2 : x \in \mathbf{R}\}$. The graph of $f$ is given
by Fig 2.10

$$f(x) = x^2 \qquad \text{Fig 2.10}$$

<!-- page 103 -->
Example 14 Draw the graph of the function $f : \mathbf{R} \rightarrow \mathbf{R}$ defined by $f(x) = x^3, x \in \mathbf{R}$.

Solution We have
$f(0) = 0, f(1) = 1, f(-1) = -1, f(2) = 8, f(-2) = -8, f(3) = 27; f(-3) = -27$, etc.
Therefore, $f = \{(x, x^3) : x \in \mathbf{R}\}$.
The graph of $f$ is given in Fig 2.11.
$\begin{array}{c} \mathbf{Y} \\ \uparrow \\ 8 \\ 6 \\ 4 \\ 2 \end{array}$
$\begin{array}{c} \mathbf{X}' \leftarrow \\ \hline \end{array}$
$\begin{array}{c} \mathbf{X} \rightarrow \\ \hline \end{array}$
$\begin{array}{c} \mathbf{O} \\ -2 \\ \hline \end{array}$
$\begin{array}{c} \mathbf{Y}' \\ \uparrow \\ 2 \\ 4 \\ 8 \end{array}$
$f(x) = x^3$

Fig 2.11

(iv) **Rational functions** are functions of the type $\frac{f(x)}{g(x)}$, where $f(x)$ and $g(x)$ are
polynomial functions of $x$ defined in a domain, where $g(x) \neq 0$.

Example 15 Define the real valued function $f : \mathbf{R} - \{0\} \to \mathbf{R}$ defined by $f(x) = \frac{1}{x}$,

$x \in \mathbf{R} - \{0\}$. Complete the Table given below using this definition. What is the domain
and range of this function?

<table>
<thead>
<tr>
<th>x</th>
<th>−2</th>
<th>−1.5</th>
<th>−1</th>
<th>−0.5</th>
<th>0.25</th>
<th>0.5</th>
<th>1</th>
<th>1.5</th>
<th>2</th>
</tr>
</thead>
<tbody>
<tr>
<td>y = \frac{1}{x}</td>
<td>...</td>
<td>...</td>
<td>...</td>
<td>...</td>
<td>...</td>
<td>...</td>
<td>...</td>
<td>...</td>
<td>...</td>
</tr>
</tbody>
</table>

Solution The completed Table is given by

<table>
<thead>
<tr>
<th>x</th>
<th>−2</th>
<th>−1.5</th>
<th>−1</th>
<th>−0.5</th>
<th>0.25</th>
<th>0.5</th>
<th>1</th>
<th>1.5</th>
<th>2</th>
</tr>
</thead>
<tbody>
<tr>
<td>y = \frac{1}{x}</td>
<td>− 0.5</td>
<td>− 0.67</td>
<td>−1</td>
<td>− 2</td>
<td>4</td>
<td>2</td>
<td>1</td>
<td>0.67</td>
<td>0.5</td>
</tr>
</tbody>
</table>

<!-- page 104 -->
The domain is all real numbers except 0 and its range is also all real numbers
except 0. The graph of $f$ is given in Fig 2.12.

Fig 2.12

(v) **The Modulus function** The function
$f: \mathbf{R} \rightarrow \mathbf{R}$ defined by $f(x) = |x|$ for each
$x \in \mathbf{R}$ is called *modulus function*. For each
non-negative value of $x$, $f(x)$ is equal to $x$.
But for negative values of $x$, the value of
$f(x)$ is the negative of the value of $x$, i.e.,

$$f(x) = \begin{cases} x, x \geq 0 \\ -x, x < 0 \end{cases}$$

The graph of the modulus function is given
in Fig 2.13.

Fig 2.13

(vi) **Signum function** The function
$f:\mathbf{R}\rightarrow\mathbf{R}$ defined by

$$f(x) = \begin{cases} 1, \text{if } x > 0 \\ 0, \text{if } x = 0 \\ -1, \text{if } x < 0 \end{cases}$$

<!-- page 105 -->
is called the $signum$ $function$. The domain of the signum function is $\mathbf{R}$ and the range is
the set $\{-1, 0, 1\}$. The graph of the signum function is given by the Fig 2.14.

$$f(x)=\frac{|x|}{x}, x^{\prime} \quad \mathbf{0} \text { and } \mathbf{0} \text { for } x=\mathbf{0}$$

Fig 2.14

(vii) **Greatest integer function**
The function $f: \mathbf{R} \rightarrow \mathbf{R}$ defined
by $f(x) = [x], x \in \mathbf{R}$ assumes the
value of the greatest integer, less
than or equal to $x$. Such a function
is called the *greatest integer*
*function*. $\mathbf{X}$

From the definition of $[x]$, we
can see that

$[x] = -1$ for $-1 \le x < 0$
$[x] = \quad 0$ for $0 \le x < 1$
$[x] = \quad 1$ for $1 \le x < 2$
$[x] = \quad 2$ for $2 \le x < 3$ and

$$f(x) = [x]$$

Fig 2.15

so on.

The graph of the function is
shown in Fig 2.15.

2.4.2 Algebra of real functions In this Section, we shall learn how to add two real
functions, subtract a real function from another, multiply a real function by a scalar
(here by a scalar we mean a real number), multiply two real functions and divide one
real function by another.

(i) Addition of two real functions Let $f : X \to \mathbf{R}$ and $g : X \to \mathbf{R}$ be any two real
functions, where $X \subset \mathbf{R}$. Then, we define $(f + g) : X \to \mathbf{R}$ by

$$(f + g) (x) = f (x) + g (x), \text{ for all } x \in \mathrm{X}.$$

<!-- page 106 -->
(ii) **Subtraction of a real function from another** Let $f : \mathrm{X} \to \mathbf{R}$ and $g : \mathrm{X} \to \mathbf{R}$ be
any two real functions, where $\mathrm{X} \subset \mathbf{R}$. Then, we define $(f - g) : \mathrm{X} \to \mathbf{R}$ by
$(f-g) (x) = f(x) - g(x)$, for all $x \in \mathrm{X}$.

(iii) **Multiplication by a scalar** Let $f : \mathrm{X} \rightarrow \mathbf{R}$ be a real valued function and $\alpha$ be a
scalar. Here by scalar, we mean a real number. Then the product $\alpha f$ is a function from
$\mathrm{X}$ to $\mathbf{R}$ defined by $(\alpha f) (x) = \alpha f (x), x \in \mathrm{X}$.

(iv) **Multiplication of two real functions** The product (or multiplication) of two real
functions $f:\mathbf{X}\rightarrow\mathbf{R}$ and $g:\mathbf{X}\rightarrow\mathbf{R}$ is a function $fg:\mathbf{X}\rightarrow\mathbf{R}$ defined by
$(fg)\ (x) = f(x)\ g(x)$, for all $x \in \mathbf{X}$.
This is also called *pointwise multiplication*.

(v) **Quotient of two real functions** Let $f$ and $g$ be two real functions defined from

$$X \rightarrow \mathbf{R}, \text{ where } X \subset \mathbf{R}. \text{ The quotient of } f \text{ by } g \text{ denoted by } \frac{f}{g} \text{ is a function defined by ,}$$

$$\left( \frac{f}{g} \right) (x) = \frac{f(x)}{g(x)}, \text{ provided } g(x) \neq 0, x \in \mathbb{X}$$

Example 16 Let $f(x) = x^2$ and $g(x) = 2x + 1$ be two real functions.Find


$$(f + g) (x), (f - g) (x), (fg) (x), \left( \frac{f}{g} \right) (x).$$


Solution We have,


$$(f + g) (x) = x^2 + 2x + 1, (f - g) (x) = x^2 - 2x - 1,$$


$$(fg) (x) = x^2 (2x + 1) = 2x^3 + x^2, \left( \frac{f}{g} \right) (x) = \frac{x^2}{2x + 1}, x \neq -\frac{1}{2}$$

Example 17 Let $f(x) = \sqrt{x}$ and $g(x) = x$ be two functions defined over the set of non-


negative real numbers. Find $(f + g) (x), (f - g) (x), (fg) (x)$ and $\left( \frac{f}{g} \right) (x)$.


Solution We have


$$(f + g) (x) = \sqrt{x} + x, (f - g) (x) = \sqrt{x} - x ,$$


$$(fg) x = \sqrt{x} (x) = x^{\frac{3}{2}} \text{ and } \left( \frac{f}{g} \right) (x) = \frac{\sqrt{x}}{x} = x^{-\frac{1}{2}}, x \neq 0$$

<!-- page 107 -->
EXERCISE 2.3

1. Which of the following relations are functions? Give reasons. If it is a function,
determine its domain and range.
(i) $\{(2,1), (5,1), (8,1), (11,1), (14,1), (17,1)\}$
(ii) $\{(2,1), (4,2), (6,3), (8,4), (10,5), (12,6), (14,7)\}$
(iii) $\{(1,3), (1,5), (2,5)\}$.
2. Find the domain and range of the following real functions:
(i) $f(x) = -|x|$ (ii) $f(x) = \sqrt{9-x^2}$.
3. A function $f$ is defined by $f(x) = 2x-5$. Write down the values of
(i) $f(0)$, (ii) $f(7)$, (iii) $f(-3)$.
4. The function '$t$' which maps temperature in degree Celsius into temperature in
degree Fahrenheit is defined by $t(\text{C}) = \frac{9\text{C}}{5} + 32$.
Find (i) $t(0)$ (ii) $t(28)$ (iii) $t(-10)$ (iv) The value of C, when $t(\text{C}) = 212$.
5. Find the range of each of the following functions.
(i) $f(x) = 2 - 3x$, $x \in \mathbf{R}$, $x > 0$.
(ii) $f(x) = x^2 + 2$, $x$ is a real number.
(iii) $f(x) = x$, $x$ is a real number.

Miscellaneous Examples

Example 18 Let $\mathbf{R}$ be the set of real numbers.
Define the real function
$$f: \mathbf{R} \rightarrow \mathbf{R} \text{ by } f(x) = x + 10$$
and sketch the graph of this function.
Solution Here $f(0) = 10, f(1) = 11, f(2) = 12, ..., f(10) = 20$, etc., and
$f(-1) = 9, f(-2) = 8, ..., f(-10) = 0$ and so on.
Therefore, shape of the graph of the given
function assumes the form as shown in Fig 2.16.

Remark The function $f$ defined by $f(x) = mx + c$,
$x \in \mathbf{R}$, is called linear function, where $m$ and $c$ are
constants. Above function is an example of a linear
function.

<!-- page 108 -->
Example 19 Let $\mathrm{R}$ be a relation from $\mathbf{Q}$ to $\mathbf{Q}$ defined by $\mathrm{R} = \{(a,b): a,b \in \mathbf{Q} \text{ and}$
$a - b \in \mathbf{Z}\}$. Show that
(i) $(a,a) \in \mathrm{R}$ for all $a \in \mathbf{Q}$
(ii) $(a,b) \in \mathrm{R}$ implies that $(b, a) \in \mathrm{R}$
(iii) $(a,b) \in \mathrm{R}$ and $(b,c) \in \mathrm{R}$ implies that $(a,c) \in \mathrm{R}$

Solution (i) Since, $a - a = 0 \in \mathbf{Z}$, if follows that $(a, a) \in \mathrm{R}$.
(ii) $(a,b) \in \mathrm{R}$ implies that $a - b \in \mathbf{Z}$. So, $b - a \in \mathbf{Z}$. Therefore,
$(b, a) \in \mathrm{R}$
(iii) $(a, b)$ and $(b, c) \in \mathrm{R}$ implies that $a - b \in \mathbf{Z}$. $b - c \in \mathbf{Z}$. So,
$a - c = (a - b) + (b - c) \in \mathbf{Z}$. Therefore, $(a,c) \in \mathrm{R}$

Example 20 Let $f = \{(1,1), (2,3), (0, -1), (-1, -3)\}$ be a linear function from $\mathbf{Z}$ into $\mathbf{Z}$.
Find $f(x)$.

Solution Since $f$ is a linear function, $f(x) = mx + c$. Also, since $(1, 1), (0, -1) \in \mathrm{R}$,
$f(1) = m + c = 1$ and $f(0) = c = -1$. This gives $m = 2$ and $f(x) = 2x - 1$.

Example 21 Find the domain of the function $f(x) = \frac{x^2 + 3x + 5}{x^2 - 5x + 4}$

Solution Since $x^2 - 5x + 4 = (x - 4) (x - 1)$, the function $f$ is defined for all real numbers
except at $x = 4$ and $x = 1$. Hence the domain of $f$ is $\mathbf{R} - \{1, 4\}$.

Example 22 The function $f$ is defined by

$$f(x) = \begin{cases} 1 - x, & x < 0 \\ 1 & , x = 0 \\ x + 1, & x > 0 \end{cases}$$

Draw the graph of $f(x)$.

Solution Here, $f(x) = 1 - x, x < 0$, this gives

$$f(-4) = 1 - (-4) = 5;$$

$$f(-3) = 1 - (-3) = 4,$$

$$f(-2) = 1 - (-2) = 3$$

$$f(-1) = 1 - (-1) = 2; \text{ etc,}$$

and $f(1) = 2, f(2) = 3, f(3) = 4$

$f(4) = 5$ and so on for $f(x) = x + 1, x > 0$.

Thus, the graph of $f$ is as shown in Fig 2.17

Fig 2.17

<!-- page 109 -->
Miscellaneous Exercise on Chapter 2

1. The relation $f$ is defined by $f(x) = \begin{cases} x^2, 0 \le x \le 3 \\ 3x, 3 \le x \le 10 \end{cases}$


The relation $g$ is defined by $g(x) = \begin{cases} x^2, 0 \le x \le 2 \\ 3x, 2 \le x \le 10 \end{cases}$


Show that $f$ is a function and $g$ is not a function.


2. If $f(x) = x^2$, find $\frac{f(1.1) - f(1)}{(1.1 - 1)}$.


3. Find the domain of the function $f(x) = \frac{x^2 + 2x + 1}{x^2 - 8x + 12}$.


4. Find the domain and the range of the real function $f$ defined by $f(x) = \sqrt{(x - 1)}$.


5. Find the domain and the range of the real function $f$ defined by $f(x) = |x - 1|$.


6. Let $f = \left\{ \left( x, \frac{x^2}{1 + x^2} \right) : x \in \mathbf{R} \right\}$ be a function from $\mathbf{R}$ into $\mathbf{R}$. Determine the range
of $f$.


7. Let $f, g : \mathbf{R} \to \mathbf{R}$ be defined, respectively by $f(x) = x + 1$, $g(x) = 2x - 3$. Find
$f + g, f - g$ and $\frac{f}{g}$.


8. Let $f = \{(1,1), (2,3), (0,-1), (-1,-3)\}$ be a function from $\mathbf{Z}$ to $\mathbf{Z}$ defined by
$f(x) = ax + b$, for some integers $a, b$. Determine $a, b$.


9. Let $\mathbf{R}$ be a relation from $\mathbf{N}$ to $\mathbf{N}$ defined by $\mathbf{R} = \{(a,b) : a, b \in \mathbf{N} \text{ and } a = b^2\}$. Are
the following true?
(i) $(a,a) \in \mathbf{R}$, for all $a \in \mathbf{N}$ (ii) $(a,b) \in \mathbf{R}$, implies $(b,a) \in \mathbf{R}$
(iii) $(a,b) \in \mathbf{R}$, $(b,c) \in \mathbf{R}$ implies $(a,c) \in \mathbf{R}$.
Justify your answer in each case.


10. Let $\mathbf{A} = \{1,2,3,4\}$, $\mathbf{B} = \{1,5,9,11,15,16\}$ and $f = \{(1,5), (2,9), (3,1), (4,5), (2,11)\}$
Are the following true?
(i) $f$ is a relation from $\mathbf{A}$ to $\mathbf{B}$ (ii) $f$ is a function from $\mathbf{A}$ to $\mathbf{B}$.
Justify your answer in each case.

<!-- page 110 -->
11. Let $f$ be the subset of $\mathbf{Z} \times \mathbf{Z}$ defined by $f = \{(ab, a + b) : a, b \in \mathbf{Z}\}$. Is $f$ a
function from $\mathbf{Z}$ to $\mathbf{Z}$? Justify your answer.
12. Let $\mathrm{A} = \{9, 10, 11, 12, 13\}$ and let $f : \mathrm{A} \rightarrow \mathbf{N}$ be defined by $f(n) =$ the highest prime
factor of $n$. Find the range of $f$.

Summary

In this Chapter, we studied about relations and functions.The main features of
this Chapter are as follows:

$\diamond$ **Ordered pair** A pair of elements grouped together in a particular order.

$\diamond$ **Cartesian product** $\text{A} \times \text{B}$ of two sets $\text{A}$ and $\text{B}$ is given by
$\text{A} \times \text{B} = \{(a, b): a \in \text{A}, b \in \text{B}\}$
In particular $\mathbf{R} \times \mathbf{R} = \{(x, y): x, y \in \mathbf{R}\}$
and $\mathbf{R} \times \mathbf{R} \times \mathbf{R} = (x, y, z): x, y, z \in \mathbf{R}\}$

$\diamond$ If $(a, b) = (x, y)$, then $a = x$ and $b = y$.

$\diamond$ If $n(\text{A}) = p$ and $n(\text{B}) = q$, then $n(\text{A} \times \text{B}) = pq$.

$\diamond$ $\text{A} \times \phi = \phi$

$\diamond$ In general, $\text{A} \times \text{B} \neq \text{B} \times \text{A}$.

$\diamond$ **Relation** A relation $\text{R}$ from a set $\text{A}$ to a set $\text{B}$ is a subset of the cartesian
product $\text{A} \times \text{B}$ obtained by describing a relationship between the first element
$x$ and the second element $y$ of the ordered pairs in $\text{A} \times \text{B}$.

$\diamond$ The **image** of an element $x$ under a relation $\text{R}$ is given by $y$, where $(x, y) \in \text{R}$,

$\diamond$ The **domain** of $\text{R}$ is the set of all first elements of the ordered pairs in a
relation $\text{R}$.

$\diamond$ The **range** of the relation $\text{R}$ is the set of all second elements of the ordered
pairs in a relation $\text{R}$.

$\diamond$ **Function** A function $f$ from a set $\text{A}$ to a set $\text{B}$ is a specific type of relation for
which every element $x$ of set $\text{A}$ has one and only one image $y$ in set $\text{B}$.

We write $f: \text{A} \rightarrow \text{B}$, where $f(x) = y$.

$\diamond$ $\text{A}$ is the domain and $\text{B}$ is the codomain of $f$.

<!-- page 111 -->
The range of the function is the set of images.
A real function has the set of real numbers or one of its subsets both as its
domain and as its range.
Algebra of functions For functions $f : \mathbf{X} \rightarrow \mathbf{R}$ and $g : \mathbf{X} \rightarrow \mathbf{R}$, we have
$$(f + g) (x) = f (x) + g(x), x \in \mathbf{X}$$
$$(f - g) (x) = f (x) - g(x), x \in \mathbf{X}$$
$$(f,g) (x) \quad = f (x) . g (x), x \in \mathbf{X}$$
$$(kf) (x) \quad = k (f (x) ), x \in \mathbf{X}, \text{ where } k \text{ is a real number.}$$
$$\left(\frac{f}{g}\right)(x) = \frac{f (x)}{g (x)}, x \in \mathbf{X}, g(x) \neq 0$$

Historical Note

The word FUNCTION first appears in a Latin manuscript “Methodus
tangentiumversa, seu de fuctionibus” written by Gottfried Wilhelm Leibnitz
(1646-1716) in 1673; Leibnitz used the word in the non-analytical sense. He
considered a function in terms of “mathematical job” – the “employee” being
just a curve.
On July 5, 1698, Johan Bernoulli, in a letter to Leibnitz, for the first time
deliberately assigned a specialised use of the term function in the analytical
sense. At the end of that month, Leibnitz replied showing his approval.
Function is found in English in 1779 in Chambers’ Cyclopaedia: “The
term function is used in algebra, for an analytical expression any way compounded
of a variable quantity, and of numbers, or constant quantities”.

<!-- page 112 -->
TRIGONOMETRICFUNCTIONS

❖ A mathematician knows how to solve a problem,
he can not solve it. – MILNE ❖

3.1 Introduction

The word ‘trigonometry’ is derived from the Greek words
‘trigon’ and ‘metron’ and it means ‘measuring the sides of
a triangle’. The subject was originally developed to solve
geometric problems involving triangles. It was studied by
sea captains for navigation, surveyor to map out the new
lands, by engineers and others. Currently, trigonometry is
used in many areas such as the science of seismology,
designing electric circuits, describing the state of an atom,
predicting the heights of tides in the ocean, analysing a
musical tone and in many other areas.

In earlier classes, we have studied the trigonometric
ratios of acute angles as the ratio of the sides of a right
angled triangle. We have also studied the trigonometric identities and application of
trigonometric ratios in solving the problems related to heights and distances. In this
Chapter, we will generalise the concept of trigonometric ratios to trigonometric functions
and study their properties.

Arya Bhatt
(476-550)

3.2 Angles

Angle is a measure of rotation of a given ray about its initial point. The original ray is

(i)Positive angle

Fig 3.1 (ii) Negative angle

<!-- page 113 -->
called the *initial side* and the final position of the ray after rotation is called the
*terminal side* of the angle. The point of rotation is called the *vertex*. If the direction of
rotation is anticlockwise, the angle is said to be positive and if the direction of rotation
is clockwise, then the angle is *negative* (Fig 3.1).

The measure of an angle is the amount of
rotation performed to get the terminal side from
the initial side. There are several units for
measuring angles. The definition of an angle
suggests a unit, viz. *one complete revolution* from the position of the initial side as
indicated in Fig 3.2.

This is often convenient for large angles. For example, we can say that a rapidly
spinning wheel is making an angle of say 15 revolution per second. We shall describe
two other units of measurement of an angle which are most commonly used, viz.
degree measure and radian measure.

3.2.1 *Degree measure* If a rotation from the initial side to terminal side is $\left( \frac{1}{360} \right)^{\text{th}}$ of

a revolution, the angle is said to have a measure of one \textit{degree}, written as $1^\circ$. A degree is
divided into 60 minutes, and a minute is divided into 60 seconds . One sixtieth of a degree is
called a \textit{minute}, written as $1'$, and one sixtieth of a minute is called a \textit{second}, written as $1''$.
Thus,        $1^\circ = 60'$,        $1' = 60''$

Some of the angles whose measures are $360^{\circ}, 180^{\circ}, 270^{\circ}, 420^{\circ}, -30^{\circ}, -420^{\circ}$ are
shown in Fig 3.3.

Fig 3.3

<!-- page 114 -->
3.2.2 *Radian measure* There is another unit for measurement of an angle, called
the *radian* measure. Angle subtended at the centre by an arc of length 1 unit in a
unit circle (circle of radius 1 unit) is said to have a measure of 1 radian. In the Fig
3.4(i) to (iv), OA is the initial side and OB is the terminal side. The figures show the

angles whose measures are $1$ radian, $-1$ radian, $1\frac{1}{2}$ radian and $-1\frac{1}{2}$ radian.

Fig 3.4 (i) to (iv)

We know that the circumference of a circle of radius $1$ unit is $2\pi$. Thus, one
complete revolution of the initial side subtends an angle of $2\pi$ radian.

More generally, in a circle of radius $r$, an arc of length $r$ will subtend an angle of
1 radian. It is well-known that equal arcs of a circle subtend equal angle at the centre.
Since in a circle of radius $r$, an arc of length $r$ subtends an angle whose measure is 1
radian, an arc of length $l$ will subtend an angle whose measure is $\frac{l}{r}$ radian. Thus, if in
a circle of radius $r$, an arc of length $l$ subtends an angle $\theta$ radian at the centre, we have
$\theta = \frac{l}{r}$ or $l = r \theta$.

<!-- page 115 -->
3.2.3 Relation between radian and real numbers

Consider the unit circle with centre O. Let A be any point
on the circle. Consider OA as initial side of an angle.
Then the length of an arc of the circle will give the radian
measure of the angle which the arc will subtend at the
centre of the circle. Consider the line PAQ which is
tangent to the circle at A. Let the point A represent the
real number zero, AP represents positive real number and
AQ represents negative real numbers (Fig 3.5). If we
rope the line AP in the anticlockwise direction along the
circle, and AQ in the clockwise direction, then every real
number will correspond to a radian measure and
conversely. Thus, radian measures and real numbers can
be considered as one and the same.

Fig 3.5

**3.2.4 *Relation between degree and radian*** Since a circle subtends at the centre
an angle whose radian measure is $2\pi$ and its degree measure is $360^\circ$, it follows that

$$2\pi \text{ radian} = 360^\circ \quad \text{or} \quad \pi \text{ radian} = 180^\circ$$

The above relation enables us to express a radian measure in terms of degree
measure and a degree measure in terms of radian measure. Using approximate value
of $\pi$ as $\frac{22}{7}$, we have

$$1 \text{ radian} = \frac{180^\circ}{\pi} = 57^\circ \ 16' \text{ approximately.}$$

Also $1^{\circ} = \frac{\pi}{180}$ radian $= 0.01746$ radian approximately.

The relation between degree measures and radian measure of some common angles
are given in the following table:

<table>
<thead>
<tr>
<th>Degree</th>
<th>30°</th>
<th>45°</th>
<th>60°</th>
<th>90°</th>
<th>180°</th>
<th>270°</th>
<th>360°</th>
</tr>
</thead>
<tbody>
<tr>
<td>Radian</td>
<td>$\frac{\pi}{6}$</td>
<td>$\frac{\pi}{4}$</td>
<td>$\frac{\pi}{3}$</td>
<td>$\frac{\pi}{2}$</td>
<td>$\pi$</td>
<td>$\frac{3\pi}{2}$</td>
<td>$2\pi$</td>
</tr>
</tbody>
</table>

<!-- page 116 -->
Notational Convention

Since angles are measured either in degrees or in radians, we adopt the convention
that whenever we write angle $\theta^\circ$, we mean the angle whose degree measure is $\theta$ and
whenever we write angle $\beta$, we mean the angle whose radian measure is $\beta$.

Note that when an angle is expressed in radians, the word ‘radian’ is frequently

omitted. Thus, $\pi = 180^\circ$ and $\frac{\pi}{4} = 45^\circ$ are written with the understanding that $\pi$ and $\frac{\pi}{4}$
are radian measures. Thus, we can say that

$$\text{Radian measure} = \frac{\pi}{180} \times \text{Degree measure}$$

$$\text{Degree measure} = \frac{180}{\pi} \times \text{Radian measure}$$

Example 1 Convert $40^{\circ} 20'$ into radian measure.

Solution We know that $180^{\circ} = \pi$ radian.

Hence $40^{\circ} 20' = 40 \frac{1}{3}$ degree $= \frac{\pi}{180} \times \frac{121}{3}$ radian $= \frac{121\pi}{540}$ radian.

Therefore $40^{\circ} 20' = \frac{121\pi}{540}$ radian.

Example 2 Convert 6 radians into degree measure.

Solution We know that $\pi$ radian $= 180^{\circ}$.

Hence $6 \text{ radians} = \frac{180}{\pi} \times 6 \text{ degree} = \frac{1080 \times 7}{22} \text{ degree}$

$= 343 \frac{7}{11} \text{ degree} \quad = 343^{\circ} + \frac{7 \times 60}{11} \text{ minute} \quad [\text{as } 1^{\circ} = 60']$

$= 343^{\circ} + 38' + \frac{2}{11} \text{ minute} \quad [\text{as } 1' = 60'']$

$= 343^{\circ} + 38' + 10.9'' \quad = 343^{\circ} 38' 11'' \text{ approximately.}$

Hence $6 \text{ radians} = 343^{\circ} 38' 11'' \text{ approximately.}$

Hence $6 \text{ radians} = 343^\circ 38' 11''$ approximately.

Example 3 Find the radius of the circle in which a central angle of $60^{\circ}$ intercepts an
arc of length $37.4 \text{ cm}$ (use $\pi = \frac{22}{7}$).

<!-- page 117 -->
Solution Here $l = 37.4$ cm and $\theta = 60^\circ = \frac{60\pi}{180}$ radian $= \frac{\pi}{3}$

Hence, by $r = \frac{l}{\theta}$, we have

$$r = \frac{37.4 \times 3}{\pi} = \frac{37.4 \times 3 \times 7}{22} = 35.7 \text{ cm}$$

Example 4 The minute hand of a watch is 1.5 cm long. How far does its tip move in
40 minutes? (Use $\pi = 3.14$).

Solution In 60 minutes, the minute hand of a watch completes one revolution. Therefore,
in 40 minutes, the minute hand turns through $\frac{2}{3}$ of a revolution. Therefore, $\theta = \frac{2}{3} \times 360^{\circ}$

or $\frac{4\pi}{3}$ radian. Hence, the required distance travelled is given by

$$l = r \theta = 1.5 \times \frac{4\pi}{3} \text{ cm} = 2\pi \text{ cm} = 2 \times 3.14 \text{ cm} = 6.28 \text{ cm}.$$

Example 5 If the arcs of the same lengths in two circles subtend angles $65^{\circ}$and $110^{\circ}$
at the centre, find the ratio of their radii.

Solution Let $r_1$ and $r_2$ be the radii of the two circles. Given that

$$\theta_1 = 65^{\circ} = \frac{\pi}{180} \times 65 = \frac{13\pi}{36} \text{ radian}$$

and $\theta_2 = 110^{\circ} = \frac{\pi}{180} \times 110 = \frac{22\pi}{36} \text{ radian}$

Let $l$ be the length of each of the arc. Then $l = r_1\theta_1 = r_2\theta_2$, which gives

$$\frac{13\pi}{36} \times r_1 = \frac{22\pi}{36} \times r_2, \text{ i.e., } \frac{r_1}{r_2} = \frac{22}{13}$$

Hence $r_1 : r_2 = 22 : 13.$

EXERCISE 3.1

1. Find the radian measures corresponding to the following degree measures:
(i) $25^{\circ}$ (ii) $-47^{\circ}30'$ (iii) $240^{\circ}$ (iv) $520^{\circ}$

<!-- page 118 -->
2. Find the degree measures corresponding to the following radian measures
(Use $\pi = \frac{22}{7}$).

(i) $\frac{11}{16}$ (ii) $-4$ (iii) $\frac{5\pi}{3}$ (iv) $\frac{7\pi}{6}$

3. A wheel makes 360 revolutions in one minute. Through how many radians does
it turn in one second?

4. Find the degree measure of the angle subtended at the centre of a circle of
radius 100 cm by an arc of length 22 cm (Use $\pi = \frac{22}{7}$).

5. In a circle of diameter 40 cm, the length of a chord is 20 cm. Find the length of
minor arc of the chord.

6. If in two circles, arcs of the same length subtend angles $60^{\circ}$ and $75^{\circ}$ at the
centre, find the ratio of their radii.

7. Find the angle in radian through which a pendulum swings if its length is 75 cm
and th e tip describes an arc of length
(i) 10 cm (ii) 15 cm (iii) 21 cm

3.3 Trigonometric Functions

In earlier classes, we have studied trigonometric ratios for acute angles as the ratio of
sides of a right angled triangle. We will now extend the definition of trigonometric
ratios to any angle in terms of radian measure and study them as trigonometric functions.

Consider a unit circle with centre
at origin of the coordinate axes. Let
$\mathrm{P} (a, b)$ be any point on the circle with
angle $\mathrm{AOP} = x$ radian, i.e., length of arc
$\mathrm{AP} = x$ (Fig 3.6).

We define $\cos x = a$ and $\sin x = b$
Since $\Delta$OMP is a right triangle, we have
$$\text{OM}^2 + \text{MP}^2 = \text{OP}^2 \text{ or } a^2 + b^2 = 1$$
Thus, for every point on the unit circle,
we have

Fig 3.6

$$a^2 + b^2 = 1 \text{ or } \cos^2 x + \sin^2 x = 1$$

Since one complete revolution
subtends an angle of $2\pi$ radian at the

centre of the circle, $\angle AOB = \frac{\pi}{2}$,

<!-- page 119 -->
$\angle \mathrm{AOC}=\pi$ and $\angle \mathrm{AOD}=\frac{3 \pi}{2}$. All angles which are integral multiples of $\frac{\pi}{2}$ are called
quadrantal angles. The coordinates of the points A, B, C and D are, respectively,
$(1, 0), (0, 1), (-1, 0)$ and $(0, -1)$. Therefore, for quadrantal angles, we have

$$\cos 0^{\circ} = 1 \qquad \sin 0^{\circ} = 0,$$

$$\cos \frac{\pi}{2} = 0 \qquad \sin \frac{\pi}{2} = 1$$

$$\cos\pi = -1 \qquad \sin\pi = 0$$

$$\cos \frac{3\pi}{2} = 0 \qquad \sin \frac{3\pi}{2} = -1$$

$$\cos 2\pi = 1 \qquad \sin 2\pi = 0$$

Now, if we take one complete revolution from the point P, we again come back to
same point P. Thus, we also observe that if $x$ increases (or decreases) by any integral
multiple of $2\pi$, the values of sine and cosine functions do not change. Thus,

$$\sin (2n\pi + x) = \sin x, n \in \mathbf{Z} , \cos (2n\pi + x) = \cos x, n \in \mathbf{Z}$$

Further, $\sin x = 0$, if $x = 0, \pm \pi, \pm 2\pi, \pm 3\pi, ..., \text{ i.e.,}$ when $x$ is an integral multiple of $\pi$

and $\cos x = 0$, if $x = \pm \frac{\pi}{2}$, $\pm \frac{3\pi}{2}$, $\pm \frac{5\pi}{2}$, ... i.e., $\cos x$ vanishes when $x$ is an odd

multiple of $\frac{\pi}{2}$. Thus

$\sin x = 0$ implies $x = n\pi$, where $n$ is any integer

$\cos x = 0$ implies $x = (2n + 1) \frac{\pi}{2}$, where $n$ is any integer.

We now define other trigonometric functions in terms of sine and cosine functions:

$\sec x = \frac{1}{\sin x}, x \neq n\pi$, where $n$ is any integer.

$\sec x = \frac{1}{\cos x}, x \neq (2n + 1)\frac{\pi}{2}$, where $n$ is any integer.

$\tan x = \frac{\sin x}{\cos x}, x \neq (2n + 1)\frac{\pi}{2}$, where $n$ is any integer.

$\cot x = \frac{\cos x}{\sin x}, x \neq n\pi$, where $n$ is any integer.

<!-- page 120 -->
We have shown that for all real $x$, $\sin^2 x + \cos^2 x = 1$

It follows that

$$1 + \tan^2 x = \sec^2 x \qquad (\text{why?})$$

$$1 + \cot^2 x = \csc^2 x \qquad (\text{why?})$$

In earlier classes, we have discussed the values of trigonometric ratios for $0^{\circ}$,
$30^{\circ}$, $45^{\circ}$, $60^{\circ}$ and $90^{\circ}$. The values of trigonometric functions for these angles are same
as that of trigonometric ratios studied in earlier classes. Thus, we have the following
table:

<table>
<thead>
<tr>
<th></th>
<th>0°</th>
<th>\frac{\pi}{6}</th>
<th>\frac{\pi}{4}</th>
<th>\frac{\pi}{3}</th>
<th>\frac{\pi}{2}</th>
<th>\pi</th>
<th>\frac{3\pi}{2}</th>
<th>2\pi</th>
</tr>
</thead>
<tbody>
<tr>
<td>sin</td>
<td>0</td>
<td>\frac{1}{2}</td>
<td>\frac{1}{\sqrt{2}}</td>
<td>\frac{\sqrt{3}}{2}</td>
<td>1</td>
<td>0</td>
<td>- 1</td>
<td>0</td>
</tr>
<tr>
<td>cos</td>
<td>1</td>
<td>\frac{\sqrt{3}}{2}</td>
<td>\frac{1}{\sqrt{2}}</td>
<td>\frac{1}{2}</td>
<td>0</td>
<td>- 1</td>
<td>0</td>
<td>1</td>
</tr>
<tr>
<td>tan</td>
<td>0</td>
<td>\frac{1}{\sqrt{3}}</td>
<td>1</td>
<td>\sqrt{3}</td>
<td>not<br/>defined</td>
<td>0</td>
<td>not<br/>defined</td>
<td>0</td>
</tr>
</tbody>
</table>

The values of cosec $x$, sec $x$ and cot $x$
are the reciprocal of the values of $\sin x$,
$\cos x$ and $\tan x$, respectively.

3.3.1 Sign of trigonometric functions

Let P $(a, b)$ be a point on the unit circle
with centre at the origin such that
$\angle AOP = x$. If $\angle AOQ = -x$, then the
coordinates of the point Q will be $(a, -b)$
(Fig 3.7). Therefore

$$\cos (-x) = \cos x$$
and $$\sin (-x) = -\sin x$$

Fig 3.7

Since for every point P $(a, b)$ on
the unit circle, $-1 \leq a \leq 1$ and

<!-- page 121 -->
$-1 \le b \le 1$, we have $-1 \le \cos x \le 1$ and $-1 \le \sin x \le 1$ for all $x$. We have learnt in

previous classes that in the first quadrant $(0 < x < \frac{\pi}{2})$ $a$ and $b$ are both positive, in the

second quadrant $(\frac{\pi}{2} < x < \pi)$ $a$ is negative and $b$ is positive, in the third quadrant

$(\pi < x < \frac{3\pi}{2})$ $a$ and $b$ are both negative and in the fourth quadrant $(\frac{3\pi}{2} < x < 2\pi)$ $a$ is

positive and $b$ is negative. Therefore, $\sin x$ is positive for $0 < x < \pi$, and negative for

$\pi < x < 2\pi$. Similarly, $\cos x$ is positive for $0 < x < \frac{\pi}{2}$, negative for $\frac{\pi}{2} < x < \frac{3\pi}{2}$ and also

positive for $\frac{3\pi}{2} < x < 2\pi$. Likewise, we can find the signs of other trigonometric

functions in different quadrants. In fact, we have the following table.

functions in different quadrants. In fact, we have the following table.

<table>
<thead>
<tr>
<th></th>
<th>I</th>
<th>II</th>
<th>III</th>
<th>IV</th>
</tr>
</thead>
<tbody>
<tr>
<td>\sin x</td>
<td>+</td>
<td>+</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>\cos x</td>
<td>+</td>
<td>-</td>
<td>-</td>
<td>+</td>
</tr>
<tr>
<td>\tan x</td>
<td>+</td>
<td>-</td>
<td>+</td>
<td>-</td>
</tr>
<tr>
<td>\csc x</td>
<td>+</td>
<td>+</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>\sec x</td>
<td>+</td>
<td>-</td>
<td>-</td>
<td>+</td>
</tr>
<tr>
<td>\cot x</td>
<td>+</td>
<td>-</td>
<td>+</td>
<td>-</td>
</tr>
</tbody>
</table>

3.3.2 Domain and range of trigonometric functions From the definition of sine
and cosine functions, we observe that they are defined for all real numbers. Further,
we observe that for each real number $x$,

$$-1 \leq \sin x \leq 1 \text{ and } -1 \leq \cos x \leq 1$$

Thus, domain of $y = \sin x$ and $y = \cos x$ is the set of all real numbers and range
is the interval $[-1, 1]$, i.e., $- 1 \le y \le 1$.

<!-- page 122 -->
Since cosec $x = \frac{1}{\sin x}$, the domain of $y = \operatorname{cosec} x$ is the set $\{ x : x \in \mathbf{R} \text{ and }$
$x \neq n \pi, n \in \mathbf{Z} \}$ and range is the set $\{y : y \in \mathbf{R}, y \geq 1 \text{ or } y \leq -1\}$. Similarly, the domain
of $y = \sec x$ is the set $\{x : x \in \mathbf{R} \text{ and } x \neq (2n + 1) \frac{\pi}{2}, n \in \mathbf{Z}\}$ and range is the set
$\{y : y \in \mathbf{R}, y \leq -1 \text{ or } y \geq 1\}$. The domain of $y = \tan x$ is the set $\{x : x \in \mathbf{R} \text{ and }$
$x \neq (2n + 1) \frac{\pi}{2}, n \in \mathbf{Z}\}$ and range is the set of all real numbers. The domain of
$y = \cot x$ is the set $\{x : x \in \mathbf{R} \text{ and } x \neq n \pi, n \in \mathbf{Z}\}$ and the range is the set of all real
numbers.

We further observe that in the first quadrant, as $x$ increases from $0$ to $\frac{\pi}{2}$, $\sin x$
increases from $0$ to $1$, as $x$ increases from $\frac{\pi}{2}$ to $\pi$, $\sin x$ decreases from $1$ to $0$. In the
third quadrant, as $x$ increases from $\pi$ to $\frac{3\pi}{2}$, $\sin x$ decreases from $0$ to $-1$and finally, in
the fourth quadrant, $\sin x$ increases from $-1$ to $0$ as $x$ increases from $\frac{3\pi}{2}$ to $2\pi$.
Similarly, we can discuss the behaviour of other trigonometric functions. In fact, we
have the following table:

<table>
<thead>
<tr>
<th></th>
<th>I quadrant</th>
<th>II quadrant</th>
<th>III quadrant</th>
<th>IV quadrant</th>
</tr>
</thead>
<tbody>
<tr>
<td>sin</td>
<td>increases from 0 to 1</td>
<td>decreases from 1 to 0</td>
<td>decreases from 0 to -1</td>
<td>increases from -1 to 0</td>
</tr>
<tr>
<td>cos</td>
<td>decreases from 1 to 0</td>
<td>decreases from 0 to -1</td>
<td>increases from -1 to 0</td>
<td>increases from 0 to 1</td>
</tr>
<tr>
<td>tan</td>
<td>increases from 0 to \infty</td>
<td>increases from -\infty to 0</td>
<td>increases from 0 to \infty</td>
<td>increases from -\infty to 0</td>
</tr>
<tr>
<td>cot</td>
<td>decreases from \infty to 0</td>
<td>decreases from 0 to-\infty</td>
<td>decreases from \infty to 0</td>
<td>decreases from 0to -\infty</td>
</tr>
<tr>
<td>sec</td>
<td>increases from 1 to \infty</td>
<td>increases from -\infty to -1</td>
<td>decreases from -1to-\infty</td>
<td>decreases from \infty to 1</td>
</tr>
<tr>
<td>cosec</td>
<td>decreases from \infty to 1</td>
<td>increases from 1 to \infty</td>
<td>increases from -\infty to -1</td>
<td>decreases from -1to-\infty</td>
</tr>
</tbody>
</table>

Remark In the above table, the statement $\tan x$ increases from $0$ to $\infty$ (infinity) for


$0 < x < \frac{\pi}{2}$ simply means that $\tan x$ increases as $x$ increases for $0 < x < \frac{\pi}{2}$ and

<!-- page 123 -->
assumes arbitrarily large positive values as $x$ approaches to $\frac{\pi}{2}$. Similarly, to say that
cosec $x$ decreases from $-1$ to $-\infty$ (minus infinity) in the fourth quadrant means that
cosec $x$ decreases for $x \in \left(\frac{3\pi}{2}, 2\pi\right)$ and assumes arbitrarily large negative values as
$x$ approaches to $2\pi$. The symbols $\infty$ and $-\infty$ simply specify certain types of behaviour
of functions and variables.

We have already seen that values of $\sin x$ and $\cos x$ repeats after an interval of
$2\pi$. Hence, values of $\operatorname{cosec} x$ and $\sec x$ will also repeat after an interval of $2\pi$. We

Fig 3.8

$$y = \cos x$$

Fig 3.9

$$y = \tan x$$

Fig 3.10

$$y = \cot x$$

Fig 3.11

<!-- page 124 -->
Fig 3.12

Fig 3.13

shall see in the next section that $\tan (\pi + x) = \tan x$. Hence, values of $\tan x$ will repeat
after an interval of $\pi$. Since $\cot x$ is reciprocal of $\tan x$, its values will also repeat after
an interval of $\pi$. Using this knowledge and behaviour of trigonometric functions, we can
sketch the graph of these functions. The graph of these functions are given above:

Example 6 If $\cos x = - \frac{3}{5}$ , $x$ lies in the third quadrant, find the values of other five
trigonometric functions.

Solution Since $\cos x = -\frac{3}{5}$ , we have $\sec x = -\frac{5}{3}$

Now $\sin^2 x + \cos^2 x = 1$, i.e., $\sin^2 x = 1 - \cos^2 x$

or $\sin^2 x = 1 - \frac{9}{25} = \frac{16}{25}$

Hence $\sin x = \pm \frac{4}{5}$

Since $x$ lies in third quadrant, $\sin x$ is negative. Therefore

$\sin x = - \frac{4}{5}$

which also gives

$\text{cosec } x = - \frac{5}{4}$

<!-- page 125 -->
Further, we have

$$\tan x = \frac{\sin x}{\cos x} = \frac{4}{3} \quad \text{and} \quad \cot x = \frac{\cos x}{\sin x} = \frac{3}{4}.$$

Example 7 If $\cot x = -\frac{5}{12}$, $x$ lies in second quadrant, find the values of other five
trigonometric functions.

Solution Since $\cot x = -\frac{5}{12}$, we have $\tan x = -\frac{12}{5}$

Now $\sec^2 x = 1 + \tan^2 x = 1 + \frac{144}{25} = \frac{169}{25}$

Hence $\sec x = \pm \frac{13}{5}$

Since $x$ lies in second quadrant, $\sec x$ will be negative. Therefore

$$\sec x = - \frac{13}{5},$$

which also gives

$$\cos x = -\frac{5}{13}$$

Further, we have

$$\sin x = \tan x \cos x = (-\frac{12}{5}) \times (-\frac{5}{13}) = \frac{12}{13}$$

and $\operatorname{cosec} x=\frac{1}{\sin x}=\frac{13}{12}$.

Example 8 Find the value of $\sin \frac{31\pi}{3}$.


Solution We know that values of $\sin x$ repeats after an interval of $2\pi$. Therefore


$$\sin \frac{31\pi}{3} = \sin (10\pi + \frac{\pi}{3}) = \sin \frac{\pi}{3} = \frac{\sqrt{3}}{2}.$$

<!-- page 126 -->
Example 9 Find the value of $\cos (-1710^{\circ})$.

Solution We know that values of $\cos x$ repeats after an interval of $2\pi$ or $360^\circ$.
Therefore, $\cos (-1710^\circ) = \cos (-1710^\circ + 5 \times 360^\circ)$
$= \cos (-1710^\circ + 1800^\circ) = \cos 90^\circ = 0.$

EXERCISE 3.2

Find the values of other five trigonometric functions in Exercises 1 to 5.

1. $\cos x = -\frac{1}{2}$, $x$ lies in third quadrant.

2. $\sin x = \frac{3}{5}$, $x$ lies in second quadrant.

3. $\cot x = \frac{3}{4}$, $x$ lies in third quadrant.

4. $\sec x = \frac{13}{5}$, $x$ lies in fourth quadrant.

5. $\tan x = -\frac{5}{12}$, $x$ lies in second quadrant.

Find the values of the trigonometric functions in Exercises 6 to 10.

6. $\sin 765^{\circ}$                                                               7. $\text{cosec} (-\ 1410^{\circ})$

8. $\tan \frac{19\pi}{3}$                                                               9. $\sin (-\ \frac{11\pi}{3})$

10. $\cot (-\ \frac{15\pi}{4})$

3.4 Trigonometric Functions of Sum and Difference of Two Angles

In this Section, we shall derive expressions for trigonometric functions of the sum and
difference of two numbers (angles) and related expressions. The basic results in this
connection are called *trigonometric identities*. We have seen that

1. $\sin (-x) = -\sin x$

2. $\cos (-x) = \cos x$

We shall now prove some more results:

<!-- page 127 -->
3. $\cos (x + y) = \cos x \cos y - \sin x \sin y$

Consider the unit circle with centre at the origin. Let $x$ be the angle $\mathrm{P}_4\mathrm{OP}_1$and $y$ be
the angle $\mathrm{P}_1\mathrm{OP}_2$. Then $(x+y)$ is the angle $\mathrm{P}_4\mathrm{OP}_2$. Also let $(-y)$ be the angle $\mathrm{P}_4\mathrm{OP}_3$.
Therefore, $\mathrm{P}_1$, $\mathrm{P}_2$, $\mathrm{P}_3$ and $\mathrm{P}_4$ will have the coordinates $\mathrm{P}_1(\cos x, \sin x)$,
$\mathrm{P}_2 [\cos (x+y), \sin (x+y)]$, $\mathrm{P}_3 [\cos (-y), \sin (-y)]$ and $\mathrm{P}_4 (1, 0)$ (Fig 3.14).

Fig 3.14

Consider the triangles $P_1OP_3$ and $P_2OP_4$. They are congruent (Why?). Therefore,
$P_1P_3$ and $P_2P_4$ are equal. By using distance formula, we get

$$\mathrm{P}_{1} \mathrm{P}_{3}^{2} = [\cos x - \cos (-y)]^{2} + [\sin x - \sin(-y)]^{2}$$
$$= (\cos x - \cos y)^{2} + (\sin x + \sin y)^{2}$$
$$= \cos^{2} x + \cos^{2} y - 2 \cos x \cos y + \sin^{2} x + \sin^{2} y + 2 \sin x \sin y$$
$$= 2 - 2 (\cos x \cos y - \sin x \sin y) \quad \text{(Why?)}$$

Also, $\quad \mathrm{P}_{2} \mathrm{P}_{4}^{2} \quad=[1-\cos (x+y)]^{2}+[0-\sin (x+y)]^{2}$
$\quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \

<!-- page 128 -->
Since $\mathrm{P}_{1} \mathrm{P}_{3}=\mathrm{P}_{2} \mathrm{P}_{4}$, we have $\mathrm{P}_{1} \mathrm{P}_{3}^{2}=\mathrm{P}_{2} \mathrm{P}_{4}^{2}$.

Therefore, $2 -2 (\cos x \cos y - \sin x \sin y) = 2 - 2 \cos (x + y)$.

Hence $\cos (x + y) = \cos x \cos y - \sin x \sin y$

4. $\cos (x - y) = \cos x \cos y + \sin x \sin y$
Replacing $y$ by $-y$ in identity 3, we get
$$\cos (x + (-y)) = \cos x \cos (-y) - \sin x \sin (-y)$$
or $\cos (x - y) = \cos x \cos y + \sin x \sin y$

5. $\cos \left(\frac{\pi}{2}-x\right)=\sin x$

If we replace $x$ by $\frac{\pi}{2}$ and $y$ by $x$ in Identity (4), we get

$$\cos \left( \frac{\pi}{2} - x \right) = \cos \frac{\pi}{2} \cos x + \sin \frac{\pi}{2} \sin x = \sin x.$$

6. $\sin \left( \frac{\pi}{2} - x \right) = \cos x$

Using the Identity 5, we have

$$\sin \left( \frac{\pi}{2} - x \right) = \cos \left[ \frac{\pi}{2} - \left( \frac{\pi}{2} - x \right) \right] = \cos x.$$

7. $\sin (x + y) = \sin x \cos y + \cos x \sin y$
We know that

$$\sin (x + y) = \cos \left( \frac{\pi}{2} - (x + y) \right) = \cos \left( \left( \frac{\pi}{2} - x \right) - y \right)$$
$$= \cos \left( \frac{\pi}{2} - x \right) \cos y + \sin \left( \frac{\pi}{2} - x \right) \sin y$$
$$= \sin x \cos y + \cos x \sin y$$

8. $\sin (x - y) = \sin x \cos y - \cos x \sin y$
If we replace $y$ by $-y$, in the Identity 7, we get the result.

9. By taking suitable values of $x$ and $y$ in the identities 3, 4, 7 and 8, we get the
following results:

$$\cos \left(\frac{\pi}{2}+x\right)=-\sin x \quad \sin \left(\frac{\pi}{2}+x\right)=\cos x$$
$$\cos (\pi-x)=-\cos x \quad \sin (\pi-x)=\sin x$$

<!-- page 129 -->
$$\cos (\pi + x) = -\cos x \qquad \sin (\pi + x) = -\sin x$$
$$\cos (2\pi - x) = \cos x \qquad \sin (2\pi - x) = -\sin x$$

Similar results for $\tan x$, $\cot x$, $\sec x$ and $\csc x$ can be obtained from the results of $\sin$
$x$ and $\cos x$.

10. If none of the angles $x$, $y$ and $(x + y)$ is an odd multiple of $\frac{\pi}{2}$, then

$$\tan (x + y) = \frac{\tan x + \tan y}{1 - \tan x \tan y}$$

Since none of the $x$, $y$ and $(x + y)$ is an odd multiple of $\frac{\pi}{2}$, it follows that $\cos x$,
$\cos y$ and $\cos (x + y)$ are non-zero. Now

$$\tan (x+y) = \frac{\sin (x+y)}{\cos (x+y)} = \frac{\sin x \cos y + \cos x \sin y}{\cos x \cos y - \sin x \sin y}.$$

Dividing numerator and denominator by $\cos x \cos y$, we have

$$\tan (x+y) = \frac{\frac{\sin x \cos y}{\cos x \cos y} + \frac{\cos x \sin y}{\cos x \cos y}}{\frac{\cos x \cos y}{\cos x \cos y} - \frac{\sin x \sin y}{\cos x \cos y}}$$

$$= \frac{\tan x + \tan y}{1 - \tan x \tan y}$$

11. $\tan (x-y)=\frac{\tan x-\tan y}{1+\tan x \tan y}$

If we replace $y$ by $-y$ in Identity 10, we get

$$\tan (x-y) = \tan [x + (-y)]$$
$$= \frac{\tan x + \tan (-y)}{1 - \tan x \tan (-y)} = \frac{\tan x - \tan y}{1 + \tan x \tan y}$$

12. If none of the angles $x$, $y$ and $(x + y)$ is a multiple of $\pi$, then

$$\cot (x+y) = \frac{\cot x \cot y - 1}{\cot y + \cot x}$$

<!-- page 130 -->
Since, none of the $x$, $y$ and $(x + y)$ is multiple of $\pi$, we find that $\sin x \sin y$ and
$\sin (x + y)$ are non-zero. Now,

$$\cot (x+y) = \frac{\cos (x+y)}{\sin (x+y)} = \frac{\cos x \cos y - \sin x \sin y}{\sin x \cos y + \cos x \sin y}$$

Dividing numerator and denominator by $\sin x \sin y$, we have

$$\cot (x + y) = \frac{\cot x \cot y - 1}{\cot y + \cot x}$$

13. $\mathbf{cot} (x - y) = \frac{\mathbf{cot} x \mathbf{cot} y + 1}{\mathbf{cot} y - \mathbf{cot} x}$ if none of angles $x$, $y$ and $x-y$ is a multiple of $\pi$

If we replace $y$ by $-y$ in identity 12, we get the result

14. $\cos 2x = \cos^2 x - \sin^2 x = 2 \cos^2 x - 1 = 1 - 2 \sin^2 x = \frac{1 - \tan^2 x}{1 + \tan^2 x}$

We know that

$$\cos (x + y) = \cos x \cos y - \sin x \sin y$$

Replacing $y$ by $x$, we get

$$\cos 2x = \cos^2 x - \sin^2 x$$
$$= \cos^2 x - (1 - \cos^2 x) = 2 \cos^2 x - 1$$

Again, $\cos 2x = \cos^2 x - \sin^2 x$
$= 1 - \sin^2 x - \sin^2 x = 1 - 2 \sin^2 x.$

We have $\cos 2x = \cos^2 x - \sin^2 x = \frac{\cos^2 x - \sin^2 x}{\cos^2 x + \sin^2 x}$

Dividing numerator and denominator by $\cos^2 x$, we get

$$\cos 2x = \frac{1 - \tan^2 x}{1 + \tan^2 x}, \quad x \neq n\pi + \frac{\pi}{2}, \text{ where } n \text{ is an integer}$$

15. $\sin 2x = 2 \sin x \cos x = \frac{2 \tan x}{1 + \tan^2 x} \quad x \neq n\pi + \frac{\pi}{2}$, where n is an integer

We have

$$\sin (x + y) = \sin x \cos y + \cos x \sin y$$

Replacing $y$ by $x$, we get $\sin 2x = 2 \sin x \cos x$.

Again $\sin 2x = \frac{2\sin x\cos x}{\cos^2 x + \sin^2 x}$

<!-- page 131 -->
Dividing each term by $\cos^2 x$, we get

$$\sin 2x = \frac{2\tan x}{1+\tan^2 x}$$

16. $\tan 2x = \frac{2\tan x}{1 - \tan^2 x}$ if $2x \neq n\pi + \frac{\pi}{2}$, where n is an integer

We know that

$$\tan (x + y) = \frac{\tan x + \tan y}{1 - \tan x \tan y}$$

Replacing $y$ by $x$ , we get $\tan 2x = \frac{2 \tan x}{1 - \tan^2 x}$

17. $\sin 3x = 3 \sin x - 4 \sin^3 x$

We have,

$\sin 3x = \sin (2x + x)$
$= \sin 2x \cos x + \cos 2x \sin x$
$= 2 \sin x \cos x \cos x + (1 - 2\sin^2 x) \sin x$
$= 2 \sin x (1 - \sin^2 x) + \sin x - 2 \sin^3 x$
$= 2 \sin x - 2 \sin^3 x + \sin x - 2 \sin^3 x$
$= 3 \sin x - 4 \sin^3 x$

18. $\cos 3x = 4 \cos^3 x - 3 \cos x$

We have,

$$\cos 3x = \cos (2x +x)$$
$$= \cos 2x \cos x - \sin 2x \sin x$$
$$= (2\cos^2 x - 1) \cos x - 2\sin x \cos x \sin x$$
$$= (2\cos^2 x - 1) \cos x - 2\cos x (1 - \cos^2 x)$$
$$= 2\cos^3 x - \cos x - 2\cos x + 2 \cos^3 x$$
$$= 4\cos^3 x - 3\cos x.$$

19. $\tan 3x = \frac{3 \tan x - \tan^3 x}{1 - 3 \tan^2 x}$ if $3x \neq n\pi + \frac{\pi}{2}$, where n is an integer

We have $\tan 3x = \tan (2x + x)$

$$= \frac{\tan 2x + \tan x}{1 - \tan 2x \tan x} = \frac{\frac{2\tan x}{1 - \tan^2 x} + \tan x}{1 - \frac{2\tan x . \tan x}{1 - \tan^2 x}}$$

<!-- page 132 -->
$$= \frac{2\tan x + \tan x - \tan^3 x}{1 - \tan^2 x - 2\tan^2 x} = \frac{3 \tan x - \tan^3 x}{1 - 3\tan^2 x}$$

20. (i) $\cos x + \cos y = 2\cos \frac{x+y}{2} \cos \frac{x-y}{2}$

(ii) $\cos x - \cos y = - 2\sin \frac{x+y}{2} \sin \frac{x-y}{2}$

(iii) $\sin x + \sin y = 2\sin \frac{x+y}{2} \cos \frac{x-y}{2}$

(iv) $\sin x - \sin y = 2\cos \frac{x+y}{2} \sin \frac{x-y}{2}$

We know that

$$\cos (x + y) = \cos x \cos y - \sin x \sin y \qquad \dots (1)$$

and $\cos (x-y) = \cos x \cos y + \sin x \sin y$ ... (2)

Adding and subtracting (1) and (2), we get

$$\cos (x + y) + \cos(x - y) = 2 \cos x \cos y \quad ... (3)$$

and $\cos (x+y)-\cos (x-y)=-2 \sin x \sin y$ ... (4)

Further $\quad \sin (x+y)=\sin x \cos y+\cos x \sin y \quad \ldots(5)$

and $\quad \sin (x-y)=\sin x \cos y-\cos x \sin y \quad \dots(6)$

Adding and subtracting (5) and (6), we get

$$\sin (x + y) + \sin (x - y) = 2 \sin x \cos y \qquad \dots (7)$$

$$\sin (x + y) - \sin (x - y) = 2 \cos x \sin y \qquad \dots (8)$$

Let $x + y = \theta$ and $x - y = \phi$. Therefore

$$x = \left( \frac{\theta + \phi}{2} \right) \text{and } y = \left( \frac{\theta - \phi}{2} \right)$$

Substituting the values of $x$ and $y$ in (3), (4), (7) and (8), we get

$$\cos \theta + \cos \phi = 2 \cos \left( \frac{\theta + \phi}{2} \right) \cos \left( \frac{\theta - \phi}{2} \right)$$

$$\cos \theta - \cos \phi = -2 \sin \left( \frac{\theta + \phi}{2} \right) \sin \left( \frac{\theta - \phi}{2} \right)$$

$$\sin \theta + \sin \phi = 2 \sin \left( \frac{\theta + \phi}{2} \right) \cos \left( \frac{\theta - \phi}{2} \right)$$

<!-- page 133 -->
$$\sin \theta - \sin \phi = 2 \cos \left( \frac{\theta + \phi}{2} \right) \sin \left( \frac{\theta - \phi}{2} \right)$$

Since $\theta$ and $\phi$ can take any real values, we can replace $\theta$ by $x$ and $\phi$ by $y$.
Thus, we get

$$\cos x + \cos y = 2 \cos \frac{x+y}{2} \cos \frac{x-y}{2} ; \cos x - \cos y = -2 \sin \frac{x+y}{2} \sin \frac{x-y}{2} ,$$

$$\sin x + \sin y = 2 \sin \frac{x+y}{2} \cos \frac{x-y}{2} ; \sin x - \sin y = 2 \cos \frac{x+y}{2} \sin \frac{x-y}{2} .$$

Remark As a part of identities given in 20, we can prove the following results:

21. (i) $2 \cos x \cos y = \cos (x + y) + \cos (x - y)$
(ii) $-2 \sin x \sin y = \cos (x + y) - \cos (x - y)$
(iii) $2 \sin x \cos y = \sin (x + y) + \sin (x - y)$
(iv) $2 \cos x \sin y = \sin (x + y) - \sin (x - y).$

Example 10 Prove that

$$3 \sin \frac{\pi}{6} \sec \frac{\pi}{3} - 4 \sin \frac{5\pi}{6} \cot \frac{\pi}{4} = 1$$

Solution We have

$$\text{L.H.S.} = 3 \sin \frac{\pi}{6} \sec \frac{\pi}{3} - 4 \sin \frac{5\pi}{6} \cot \frac{\pi}{4}$$

$$= 3 \times \frac{1}{2} \times 2 - 4 \sin \left( \pi - \frac{\pi}{6} \right) \times 1 = 3 - 4 \sin \frac{\pi}{6}$$

$$= 3 - 4 \times \frac{1}{2} = 1 = \text{R.H.S.}$$

Example 11 Find the value of $\sin 15^{\circ}$.

Solution We have
$$\sin 15^{\circ} = \sin (45^{\circ} - 30^{\circ})$$
$$= \sin 45^{\circ} \cos 30^{\circ} - \cos 45^{\circ} \sin 30^{\circ}$$
$$= \frac{1}{\sqrt{2}} \times \frac{\sqrt{3}}{2} - \frac{1}{\sqrt{2}} \times \frac{1}{2} = \frac{\sqrt{3} - 1}{2\sqrt{2}} .$$

Example 12 Find the value of $\tan \frac{13\pi}{12}$.

<!-- page 134 -->
Solution We have

$$\tan \frac{13\pi}{12} = \tan \left( \pi + \frac{\pi}{12} \right) = \tan \frac{\pi}{12} = \tan \left( \frac{\pi}{4} - \frac{\pi}{6} \right)$$

$$= \frac{\tan \frac{\pi}{4} - \tan \frac{\pi}{6}}{1 + \tan \frac{\pi}{4} \tan \frac{\pi}{6}} = \frac{1 - \frac{1}{\sqrt{3}}}{1 + \frac{1}{\sqrt{3}}} = \frac{\sqrt{3} - 1}{\sqrt{3} + 1} = 2 - \sqrt{3}$$

Example 13 Prove that

$$\frac{\sin(x+y)}{\sin(x-y)} = \frac{\tan x + \tan y}{\tan x - \tan y} \text{ .}$$

Solution We have

$$\text{L.H.S.} \quad = \frac{\sin(x+y)}{\sin(x-y)} = \frac{\sin x \cos y + \cos x \sin y}{\sin x \cos y - \cos x \sin y}$$

Dividing the numerator and denominator by $\cos x \cos y$, we get

$$\frac{\sin(x+y)}{\sin(x-y)} = \frac{\tan x + \tan y}{\tan x - \tan y} \text{ .}$$

Example 14 Show that
$$\tan 3 \ x \tan 2 \ x \tan x = \tan 3x - \tan 2 \ x - \tan x$$

Solution We know that $3x = 2x + x$

Therefore, $\tan 3x = \tan (2x + x)$

or $\tan 3x = \frac{\tan 2x + \tan x}{1 - \tan 2x \tan x}$

or $\tan 3x - \tan 3x \tan 2x \tan x = \tan 2x + \tan x$

or $\tan 3x - \tan 2x - \tan x = \tan 3x \tan 2x \tan x$

or $\tan 3x \tan 2x \tan x = \tan 3x - \tan 2x - \tan x.$

Example 15 Prove that

$$\cos \left( \frac{\pi}{4} + x \right) + \cos \left( \frac{\pi}{4} - x \right) = \sqrt{2} \cos x$$

Solution Using the Identity 20(i), we have

<!-- page 135 -->
L.H.S. $\quad = \cos \left( \frac{\pi}{4} + x \right) + \cos \left( \frac{\pi}{4} - x \right)$

$= 2 \cos \left( \frac{\frac{\pi}{4} + x + \frac{\pi}{4} - x}{2} \right) \cos \left( \frac{\frac{\pi}{4} + x - \left( \frac{\pi}{4} - x \right)}{2} \right)$

$= 2 \cos \frac{\pi}{4} \cos x = 2 \times \frac{1}{\sqrt{2}} \cos x = \sqrt{2} \cos x = \text{R.H.S.}$

Example 16 Prove that $\frac{\cos 7x + \cos 5x}{\sin 7x - \sin 5x} = \cot x$


Solution Using the Identities 20 (i) and 20 (iv), we get


$$\text{L.H.S.} \quad = \frac{2\cos \frac{7x + 5x}{2} \cos \frac{7x - 5x}{2}}{2\cos \frac{7x + 5x}{2} \sin \frac{7x - 5x}{2}} = \frac{\cos x}{\sin x} = \cot x = \text{R.H.S.}$$

Example 17 Prove that $= \frac{\sin 5x - 2\sin 3x + \sin x}{\cos 5x - \cos x} = \tan x$

Solution We have

$$\text{L.H.S.} = \frac{\sin 5x - 2\sin 3x + \sin x}{\cos 5x - \cos x} = \frac{\sin 5x + \sin x - 2\sin 3x}{\cos 5x - \cos x}$$

$$= \frac{2\sin 3x \cos 2x - 2\sin 3x}{-2\sin 3x \sin 2x} = -\frac{\sin 3x (\cos 2x - 1)}{\sin 3x \sin 2x}$$

$$= \frac{1 - \cos 2x}{\sin 2x} = \frac{2\sin^2 x}{2\sin x \cos x} = \tan x = \text{R.H.S.}$$

<!-- page 136 -->
EXERCISE 3.3

Prove that:

1. $\sin^2 \frac{\pi}{6} + \cos^2 \frac{\pi}{3} - \tan^2 \frac{\pi}{4} = -\frac{1}{2}$
2. $2\sin^2 \frac{\pi}{6} + \text{cosec}^2 \frac{7\pi}{6} \cos^2 \frac{\pi}{3} = \frac{3}{2}$
3. $\cot^2 \frac{\pi}{6} + \text{cosec}^2 \frac{5\pi}{6} + 3\tan^2 \frac{\pi}{6} = 6$
4. $2\sin^2 \frac{3\pi}{4} + 2\cos^2 \frac{\pi}{4} + 2\sec^2 \frac{\pi}{3} = 10$
5. Find the value of:
(i) $\sin 75^\circ$
(ii) $\tan 15^\circ$

Prove the following:

6. $\cos \left(\frac{\pi}{4}-x\right) \cos \left(\frac{\pi}{4}-y\right)-\sin \left(\frac{\pi}{4}-x\right) \sin \left(\frac{\pi}{4}-y\right)=\sin (x+y)$

7. $\frac{\tan \left(\frac{\pi}{4}+x\right)}{\tan \left(\frac{\pi}{4}-x\right)}=\left(\frac{1+\tan x}{1-\tan x}\right)^{2}$

8. $\frac{\cos (\pi+x) \cos (-x)}{\sin (\pi-x) \cos \left(\frac{\pi}{2}+x\right)}=\cot ^{2} x$

9. $\cos \left(\frac{3 \pi}{2}+x\right) \cos (2 \pi+x)\left[\cot \left(\frac{3 \pi}{2}-x\right)+\cot (2 \pi+x)\right]=1$

10. $\sin (n+1)x \sin (n+2)x + \cos (n+1)x \cos (n+2)x = \cos x$

11. $\cos \left( \frac{3\pi}{4} + x \right) - \cos \left( \frac{3\pi}{4} - x \right) = -\sqrt{2} \sin x$

12. $\sin^2 6x - \sin^2 4x = \sin 2x \sin 10x$

13. $\cos^2 2x - \cos^2 6x = \sin 4x \sin 8x$

14. $\sin 2 x + 2 \sin 4x + \sin 6x = 4 \cos^2 x \sin 4x$

15. $\cot 4x (\sin 5x + \sin 3x) = \cot x (\sin 5x - \sin 3x)$

16. $\frac{\cos 9x - \cos 5x}{\sin 17x - \sin 3x} = -\frac{\sin 2x}{\cos 10x}$

17. $\frac{\sin 5x + \sin 3x}{\cos 5x + \cos 3x} = \tan 4x$

18. $\frac{\sin x - \sin y}{\cos x + \cos y} = \tan \frac{x - y}{2}$

19. $\frac{\sin x + \sin 3x}{\cos x + \cos 3x} = \tan 2x$

20. $\frac{\sin x - \sin 3x}{\sin^2 x - \cos^2 x} = 2 \sin x$

21. $\frac{\cos 4x + \cos 3x + \cos 2x}{\sin 4x + \sin 3x + \sin 2x} = \cot 3x$

<!-- page 137 -->
22. $\cot x \cot 2x - \cot 2x \cot 3x - \cot 3x \cot x = 1$

23. $\tan 4x = \frac{4\tan x (1 - \tan^2 x)}{1 - 6 \tan^2 x + \tan^4 x}$          24. $\cos 4x = 1 - 8\sin^2 x \cos^2 x$

25. $\cos 6x = 32 \cos^6 x - 48\cos^4 x + 18 \cos^2 x - 1$

3.5 Trigonometric Equations

Equations involving trigonometric functions of a variable are called *trigonometric*
*equations*. In this Section, we shall find the solutions of such equations. We have
already learnt that the values of $\sin x$ and $\cos x$ repeat after an interval of $2\pi$ and the
values of $\tan x$ repeat after an interval of $\pi$. The solutions of a trigonometric equation
for which $0 \le x < 2\pi$ are called *principal solutions*. The expression involving integer
‘$n$’ which gives all solutions of a trigonometric equation is called the *general solution*.
We shall use ‘$\mathbf{Z}$’ to denote the set of integers.

The following examples will be helpful in solving trigonometric equations:

Example 18 Find the principal solutions of the equation $\sin x = \frac{\sqrt{3}}{2}$.


Solution We know that, $\sin \frac{\pi}{3} = \frac{\sqrt{3}}{2}$ and $\sin \frac{2\pi}{3} = \sin \left( \pi - \frac{\pi}{3} \right) = \sin \frac{\pi}{3} = \frac{\sqrt{3}}{2}$.


Therefore, principal solutions are $x = \frac{\pi}{3}$ and $\frac{2\pi}{3}$.

Example 19 Find the principal solutions of the equation $\tan x = -\frac{1}{\sqrt{3}}$.


Solution We know that, $\tan \frac{\pi}{6} = \frac{1}{\sqrt{3}}$. Thus, $\tan \left( \pi - \frac{\pi}{6} \right) = -\tan \frac{\pi}{6} = -\frac{1}{\sqrt{3}}$


and $\tan \left( 2\pi - \frac{\pi}{6} \right) = -\tan \frac{\pi}{6} = -\frac{1}{\sqrt{3}}$


Thus $\tan \frac{5\pi}{6} = \tan \frac{11\pi}{6} = -\frac{1}{\sqrt{3}}$.


Therefore, principal solutions are $\frac{5\pi}{6}$ and $\frac{11\pi}{6}$.


We will now find the general solutions of trigonometric equations. We have already

We will now find the general solutions of trigonometric equations. We have already

<!-- page 138 -->
seen that:

$\sin x = 0$ gives $x = n\pi$, where $n \in \mathbb{Z}$

$\cos x = 0$ gives $x = (2n + 1)\frac{\pi}{2}$, where $n \in \mathbb{Z}$.

We shall now prove the following results:

Theorem 1 For any real numbers $x$ and $y$,
$$\sin x = \sin y \text{ implies } x = n\pi + (-1)^n y, \text{ where } n \in \mathbf{Z}$$
Proof If $\sin x = \sin y$, then
$$\sin x - \sin y = 0 \text{ or } 2\cos \frac{x+y}{2} \sin \frac{x-y}{2} = 0$$
which gives $\cos \frac{x+y}{2} = 0 \text{ or } \sin \frac{x-y}{2} = 0$
Therefore $\frac{x+y}{2} = (2n+1)\frac{\pi}{2} \text{ or } \frac{x-y}{2} = n\pi$, where $n \in \mathbf{Z}$
i.e. $x = (2n+1)\pi - y \text{ or } x = 2n\pi + y$, where $n \in \mathbf{Z}$
Hence $x = (2n+1)\pi + (-1)^{2n+1} y \text{ or } x = 2n\pi + (-1)^{2n} y$, where $n \in \mathbf{Z}$.
Combining these two results, we get
$x = n\pi + (-1)^n y$, where $n \in \mathbf{Z}$.

Theorem 2 For any real numbers $x$ and $y$, $\cos x = \cos y$, implies $x = 2n\pi \pm y$,
where $n \in \mathbf{Z}$

Proof If $\cos x = \cos y$, then

$$\cos x - \cos y = 0 \quad \text{i.e.,} \quad -2 \sin \frac{x + y}{2} \sin \frac{x - y}{2} = 0$$

Thus $\sin \frac{x + y}{2} = 0 \quad \text{or} \quad \sin \frac{x - y}{2} = 0$

Therefore $\frac{x + y}{2} = n\pi$ or $\frac{x - y}{2} = n\pi$, where $n \in \mathbf{Z}$

i.e. $x = 2n\pi - y$ or $x = 2n\pi + y$, where $n \in \mathbf{Z}$

Hence $x = 2n\pi \pm y$, where $n \in \mathbf{Z}$

Theorem 3 Prove that if $x$ and $y$ are not odd mulitple of $\frac{\pi}{2}$, then

$$\tan x = \tan y \text{ implies } x = n\pi + y, \text{ where } n \in \mathbf{Z}$$

$$\tan x = \tan y \text{ implies } x = n\pi + y, \text{ where } n \in \mathbb{Z}$$

<!-- page 139 -->
Proof If $\tan x = \tan y$, then $\tan x - \tan y = 0$

or $$\frac{\sin x \cos y - \cos x \sin y}{\cos x \cos y} = 0$$

which gives $$\sin (x - y) = 0 \quad \text{(Why?)}$$

Therefore $$x - y = n\pi, \text{ i.e., } x = n\pi + y, \text{ where } n \in \mathbf{Z}$$

Example 20 Find the solution of $\sin x = -\frac{\sqrt{3}}{2}$.


Solution We have $\sin x = -\frac{\sqrt{3}}{2} = -\sin \frac{\pi}{3} = \sin \left( \pi + \frac{\pi}{3} \right) = \sin \frac{4\pi}{3}$


Hence $\sin x = \sin \frac{4\pi}{3}$, which gives


$$x = n\pi + (-1)^n \frac{4\pi}{3}, \text{ where } n \in \mathbf{Z}.$$

Note $\frac{4\pi}{3}$ is one such value of $x$ for which $\sin x = -\frac{\sqrt{3}}{2}$. One may take any
other value of $x$ for which $\sin x = -\frac{\sqrt{3}}{2}$. The solutions obtained will be the same
although these may apparently look different.

Example 21 Solve $\cos x = \frac{1}{2}$.

Example 21 Solve $\cos x = \frac{1}{2}$.


Solution We have, $\cos x = \frac{1}{2} = \cos \frac{\pi}{3}$


Therefore $x = 2n\pi \pm \frac{\pi}{3}$, where $n \in \mathbf{Z}$.


Example 22 Solve $\tan 2x = -\cot \left( x + \frac{\pi}{3} \right)$.


Solution We have, $\tan 2x = -\cot \left( x + \frac{\pi}{3} \right) = \tan \left( \frac{\pi}{2} + x + \frac{\pi}{3} \right)$

<!-- page 140 -->
or $\tan 2x = \tan \left( x + \frac{5\pi}{6} \right)$

Therefore $2x = n\pi + x + \frac{5\pi}{6}$, where $n \in \mathbf{Z}$

or $x = n\pi + \frac{5\pi}{6}$, where $n \in \mathbb{Z}$.

Example 23 Solve $\sin 2x - \sin 4x + \sin 6x = 0$.

Example 23 Solve $\sin 2x - \sin 4x + \sin 6x = 0$.

Solution The equation can be written as
$$\sin 6x + \sin 2x - \sin 4x = 0$$
or $$2 \sin 4x \cos 2x - \sin 4x = 0$$
i.e. $$\sin 4x(2 \cos 2x - 1) = 0$$

Therefore $$\sin 4x = 0 \quad \text{or} \quad \cos 2x = \frac{1}{2}$$

i.e. $$\sin 4x = 0 \quad \text{or} \quad \cos 2x = \cos \frac{\pi}{3}$$

Hence $$4x = n\pi \quad \text{or} \quad 2x = 2n\pi \pm \frac{\pi}{3}, \text{ where } n \in \mathbf{Z}$$

i.e. $$x = \frac{n\pi}{4} \quad \text{or} \quad x = n\pi \pm \frac{\pi}{6}, \text{ where } n \in \mathbf{Z}.$$

Example 24 Solve $2 \cos^2 x + 3 \sin x = 0$

Solution The equation can be written as

$$2(1 - \sin^2 x) + 3 \sin x = 0$$

or $$2 \sin^2 x - 3 \sin x - 2 = 0$$

or $$(2\sin x + 1) (\sin x - 2) = 0$$

Hence $\sin x = -\frac{1}{2}$ or $\sin x = 2$

But $\sin x = 2$ is not possible (Why?)

Therefore $\sin x = -\frac{1}{2} = \sin \frac{7\pi}{6}$ .

<!-- page 141 -->
Hence, the solution is given by

$$x = n\pi + (-1)^n \frac{7\pi}{6}, \text{ where } n \in \mathbf{Z}.$$

EXERCISE 3.4

Find the principal and general solutions of the following equations:

1. $\tan x = \sqrt{3}$                                     2. $\sec x = 2$

3. $\cot x = -\sqrt{3}$                                     4. $\text{cosec } x = -2$

Find the general solution for each of the following equations:

5. $\cos 4 x = \cos 2 x$                                     6. $\cos 3x + \cos x - \cos 2x = 0$
7. $\sin 2x + \cos x = 0$                                      8. $\sec^2 2x = 1 - \tan 2x$
9. $\sin x + \sin 3x + \sin 5x = 0$

Miscellaneous Examples

Example 25 If $\sin x = \frac{3}{5}$, $\cos y = -\frac{12}{13}$, where $x$ and $y$ both lie in second quadrant,
find the value of $\sin (x + y)$.
Solution We know that
$\sin (x + y) = \sin x \cos y + \cos x \sin y$ ... (1)
Now $\cos^2 x = 1 - \sin^2 x = 1 - \frac{9}{25} = \frac{16}{25}$
Therefore $\cos x = \pm \frac{4}{5}$.
Since $x$ lies in second quadrant, $\cos x$ is negative.
Hence $\cos x = -\frac{4}{5}$
Now $\sin^2 y = 1 - \cos^2 y = 1 - \frac{144}{169} = \frac{25}{169}$
i.e. $\sin y = \pm \frac{5}{13}$.
Since $y$ lies in second quadrant, hence $\sin y$ is positive. Therefore, $\sin y = \frac{5}{13}$. Substituting
the values of $\sin x$, $\sin y$, $\cos x$ and $\cos y$ in (1), we get

<!-- page 142 -->
$$\sin(x+y) = \frac{3}{5} \times \left( -\frac{12}{13} \right) + \left( -\frac{4}{5} \right) \times \frac{5}{13} \quad = -\frac{36}{65} - \frac{20}{65} = -\frac{56}{65}.$$

Example 26 Prove that

$$\cos 2x \cos \frac{x}{2} - \cos 3x \cos \frac{9x}{2} = \sin 5x \sin \frac{5x}{2}.$$

Solution We have

$$\text{L.H.S.} = \frac{1}{2} \left[ 2\cos 2x \cos \frac{x}{2} - 2\cos \frac{9x}{2} \cos 3x \right]$$

$$= \frac{1}{2} \left[ \cos \left( 2x + \frac{x}{2} \right) + \cos \left( 2x - \frac{x}{2} \right) - \cos \left( \frac{9x}{2} + 3x \right) - \cos \left( \frac{9x}{2} - 3x \right) \right]$$

$$= \frac{1}{2} \left[ \cos \frac{5x}{2} + \cos \frac{3x}{2} - \cos \frac{15x}{2} - \cos \frac{3x}{2} \right] = \frac{1}{2} \left[ \cos \frac{5x}{2} - \cos \frac{15x}{2} \right]$$

$$= \frac{1}{2} \left[ -2\sin \left\{ \frac{\frac{5x}{2} + \frac{15x}{2}}{2} \right\} \sin \left\{ \frac{\frac{5x}{2} - \frac{15x}{2}}{2} \right\} \right]$$

$$= -\sin 5x \sin \left( -\frac{5x}{2} \right) = \sin 5x \sin \frac{5x}{2} = \text{R.H.S.}$$

Example 27 Find the value of $\tan \frac{\pi}{8}$.


Solution Let $x = \frac{\pi}{8}$. Then $2x = \frac{\pi}{4}$.


Now $\tan 2x = \frac{2 \tan x}{1 - \tan^2 x}$


or $\tan \frac{\pi}{4} = \frac{2 \tan \frac{\pi}{8}}{1 - \tan^2 \frac{\pi}{8}}$


Let $y = \tan \frac{\pi}{8}$. Then $1 = \frac{2y}{1 - y^2}$

<!-- page 143 -->
or $y^2 + 2y - 1 = 0$

Therefore $y = \frac{-2 \pm 2\sqrt{2}}{2} = -1 \pm \sqrt{2}$

Since $\frac{\pi}{8}$ lies in the first quadrant, $y = \tan \frac{\pi}{8}$ is positve. Hence

$$\tan \frac{\pi}{8} = \sqrt{2} - 1.$$

Example 28 If $\tan x = \frac{3}{4}, \pi < x < \frac{3\pi}{2}$, find the value of $\sin \frac{x}{2}$, $\cos \frac{x}{2}$ and $\tan \frac{x}{2}$.

Solution Since $\pi < x < \frac{3\pi}{2}$, $\cos x$ is negative.

Also $\frac{\pi}{2} < \frac{x}{2} < \frac{3\pi}{4}.$

Therefore, $\sin \frac{x}{2}$ is positive and $\cos \frac{x}{2}$ is negative.

Now $\sec^2 x = 1 + \tan^2 x = 1 + \frac{9}{16} = \frac{25}{16}$

Therefore $\cos^2 x = \frac{16}{25}$ or $\cos x = -\frac{4}{5}$ (Why?)

Now $2 \sin^2 \frac{x}{2} = 1 - \cos x = 1 + \frac{4}{5} = \frac{9}{5}.$

Therefore $\sin^2 \frac{x}{2} = \frac{9}{10}$

or $\sin \frac{x}{2} = \frac{3}{\sqrt{10}}$ (Why?)

Again $2\cos^2 \frac{x}{2} = 1 + \cos x = 1 - \frac{4}{5} = \frac{1}{5}$

Therefore $\cos^2 \frac{x}{2} = \frac{1}{10}$

<!-- page 144 -->
or $$\cos \frac{x}{2} = -\frac{1}{\sqrt{10}} \text{ (Why?)}$$

Hence $\tan \frac{x}{2}=\frac{\sin \frac{x}{2}}{\cos \frac{x}{2}}=\frac{3}{\sqrt{10}} \times\left(\frac{-\sqrt{10}}{1}\right)=-3$.

Example 29 Prove that $\cos^2 x + \cos^2 \left( x + \frac{\pi}{3} \right) + \cos^2 \left( x - \frac{\pi}{3} \right) = \frac{3}{2}$.

Solution We have

$$\text{L.H.S.} = \frac{1+\cos 2x}{2} + \frac{1+\cos \left( 2x + \frac{2\pi}{3} \right)}{2} + \frac{1+\cos \left( 2x - \frac{2\pi}{3} \right)}{2} .$$

$$= \frac{1}{2} \left[ 3 + \cos 2x + \cos \left( 2x + \frac{2\pi}{3} \right) + \cos \left( 2x - \frac{2\pi}{3} \right) \right]$$

$$= \frac{1}{2} \left[ 3 + \cos 2x + 2\cos 2x \cos \frac{2\pi}{3} \right]$$

$$= \frac{1}{2} \left[ 3 + \cos 2x + 2\cos 2x \cos \left( \pi - \frac{\pi}{3} \right) \right]$$

$$= \frac{1}{2} \left[ 3 + \cos 2x - 2\cos 2x \cos \frac{\pi}{3} \right]$$

$$= \frac{1}{2} [3 + \cos 2x - \cos 2x] = \frac{3}{2} = \text{R.H.S.}$$

Miscellaneous Exercise on Chapter 3

Prove that:

1. $2\cos \frac{\pi}{13} \cos \frac{9\pi}{13} + \cos \frac{3\pi}{13} + \cos \frac{5\pi}{13} = 0$

2. $(\sin 3x + \sin x) \sin x + (\cos 3x - \cos x) \cos x = 0$

<!-- page 145 -->
3. $(\cos x + \cos y)^2 + (\sin x - \sin y)^2 = 4 \cos^2 \frac{x + y}{2}$

4. $(\cos x - \cos y)^2 + (\sin x - \sin y)^2 = 4 \sin^2 \frac{x - y}{2}$

5. $\sin x + \sin 3x + \sin 5x + \sin 7x = 4 \cos x \cos 2x \sin 4x$

6. $\frac{(\sin 7x + \sin 5x) + (\sin 9x + \sin 3x)}{(\cos 7x + \cos 5x) + (\cos 9x + \cos 3x)} = \tan 6x$

7. $\sin 3x + \sin 2x - \sin x = 4\sin x \cos \frac{x}{2} \cos \frac{3x}{2}$

Find $\sin \frac{x}{2}$, $\cos \frac{x}{2}$ and $\tan \frac{x}{2}$ in each of the following :

8. $\tan x = -\frac{4}{3}, x$ in quadrant II

9. $\cos x = -\frac{1}{3}$, $x$ in quadrant III

10. $\sin x = \frac{1}{4}$ , $x$ in quadrant II

Summary

If in a circle of radius $r$, an arc of length $l$ subtends an angle of $\theta$ radians, then
$l = r \theta$

$\diamond$ Radian measure $= \frac{\pi}{180} \times$ Degree measure

$\diamond$ Degree measure $= \frac{180}{\pi} \times$ Radian measure

$\diamond$ $\cos^2 x + \sin^2 x = 1$

$\diamond$ $1 + \tan^2 x = \sec^2 x$

$\diamond$ $1 + \cot^2 x = \text{cosec}^2 x$

$\diamond$ $\cos (2n\pi + x) = \cos x$

$\diamond$ $\sin (2n\pi + x) = \sin x$

$\diamond$ $\sin (-x) = - \sin x$

$\diamond$ $\cos (-x) = \cos x$

<!-- page 146 -->
$\diamond \cos (x + y) = \cos x \cos y - \sin x \sin y$
$\diamond \cos (x - y) = \cos x \cos y + \sin x \sin y$

$\diamond \cos \left( \frac{\pi}{2} - x \right) = \sin x$

$\diamond \sin \left( \frac{\pi}{2} - x \right) = \cos x$

$\diamond \sin (x + y) = \sin x \cos y + \cos x \sin y$
$\diamond \sin (x - y) = \sin x \cos y - \cos x \sin y$

$\diamond \cos \left( \frac{\pi}{2} + x \right) = - \sin x \quad \quad \quad \quad \sin \left( \frac{\pi}{2} + x \right) = \cos x$
$\cos (\pi - x) = - \cos x \quad \quad \quad \quad \sin (\pi - x) = \sin x$
$\cos (\pi + x) = - \cos x \quad \quad \quad \quad \sin (\pi + x) = - \sin x$
$\cos (2\pi - x) = \cos x \quad \quad \quad \quad \sin (2\pi - x) = - \sin x$

$\diamond$ If none of the angles $x$, $y$ and $(x \pm y)$ is an odd multiple of $\frac{\pi}{2}$, then

$$\tan (x + y) = \frac{\tan x + \tan y}{1 - \tan x \tan y}$$

$\diamond \tan (x - y) = \frac{\tan x - \tan y}{1 + \tan x \tan y}$$$\diamond$ If none of the angles $x$, $y$ and $(x \pm y)$ is a multiple of $\pi$, then$$\cot (x + y) = \frac{\cot x \cot y - 1}{\cot y + \cot x}$$$\diamond \cot (x - y) = \frac{\cot x \cot y + 1}{\cot y - \cot x}$$

$\diamond \cos 2x = \cos^2 x - \sin^2 x = 2\cos^2 x - 1 = 1 - 2 \sin^2 x = \frac{1 - \tan^2 x}{1 + \tan^2 x}$$

<!-- page 147 -->
$\diamond \sin 2x = 2 \sin x \cos x = \frac{2 \tan x}{1 + \tan^2 x}$


$\diamond \tan 2x = \frac{2 \tan x}{1 - \tan^2 x}$


$\diamond \sin 3x = 3 \sin x - 4 \sin^3 x$


$\diamond \cos 3x = 4 \cos^3 x - 3 \cos x$


$\diamond \tan 3x = \frac{3 \tan x - \tan^3 x}{1 - 3 \tan^2 x}$


$\diamond$ (i) $\cos x + \cos y = 2 \cos \frac{x + y}{2} \cos \frac{x - y}{2}$


(ii) $\cos x - \cos y = - 2 \sin \frac{x + y}{2} \sin \frac{x - y}{2}$


(iii) $\sin x + \sin y = 2 \sin \frac{x + y}{2} \cos \frac{x - y}{2}$


(iv) $\sin x - \sin y = 2 \cos \frac{x + y}{2} \sin \frac{x - y}{2}$


$\diamond$ (i) $2 \cos x \cos y = \cos (x + y) + \cos (x - y)$


(ii) $- 2 \sin x \sin y = \cos (x + y) - \cos (x - y)$


(iii) $2 \sin x \cos y = \sin (x + y) + \sin (x - y)$


(iv) $2 \cos x \sin y = \sin (x + y) - \sin (x - y)$.


$\diamond \sin x = 0$ gives $x = n\pi$, where $n \in \mathbf{Z}$.


$\diamond \cos x = 0$ gives $x = (2n + 1) \frac{\pi}{2}$, where $n \in \mathbf{Z}$.


$\diamond \sin x = \sin y$ implies $x = n\pi + (- 1)^n y$, where $n \in \mathbf{Z}$.


$\diamond \cos x = \cos y$, implies $x = 2n\pi \pm y$, where $n \in \mathbf{Z}$.


$\diamond \tan x = \tan y$ implies $x = n\pi + y$, where $n \in \mathbf{Z}$.

<!-- page 148 -->
Historical Note

The study of trigonometry was first started in India. The ancient Indian
Mathematicians, Aryabhatta (476), Brahmagupta (598), Bhaskara I (600) and
Bhaskara II (1114) got important results. All this knowledge first went from
India to middle-east and from there to Europe. The Greeks had also started the
study of trigonometry but their approach was so clumsy that when the Indian
approach became known, it was immediately adopted throughout the world.
In India, the predecessor of the modern trigonometric functions, known as
the sine of an angle, and the introduction of the sine function represents the main
contribution of the $siddhantas$ (Sanskrit astronomical works) to the history of
mathematics.
Bhaskara I (about 600) gave formulae to find the values of sine functions
for angles more than $90^\circ$. A sixteenth century Malayalam work $Yuktibhasa$
(period) contains a proof for the expansion of $\sin (\text{A} + \text{B})$. Exact expression for
sines or cosines of $18^\circ$, $36^\circ$, $54^\circ$, $72^\circ$, etc., are given by
Bhaskara II.
The symbols $\sin^{-1} x$, $\cos^{-1} x$, etc., for $\text{arc sin } x$, $\text{arc cos } x$, etc., were
suggested by the astronomer Sir John F.W. Hersehel (1813) The names of Thales
(about 600 B.C.) is invariably associated with height and distance problems. He
is credited with the determination of the height of a great pyramid in Egypt by
measuring shadows of the pyramid and an auxiliary staff (or gnomon) of known
height, and comparing the ratios:
$$\frac{\text{H}}{\text{S}} = \frac{h}{s} = \tan \text{ (sun's altitude)}$$
Thales is also said to have calculated the distance of a ship at sea through
the proportionality of sides of similar triangles. Problems on height and distance
using the similarity property are also found in ancient Indian works.

<!-- page 149 -->
PRINCIPLE OF
MATHEMATICAL INDUCTION

❖ *Analysis and natural philosophy owe their most important discoveries to*
*this fruitful means, which is called induction. Newton was indebted*
*to it for his theorem of the binomial and the principle of*
*universal gravity. – LAPLACE*

4.1 Introduction

One key basis for mathematical thinking is deductive reasoning. An informal, and example of deductive reasoning,
borrowed from the study of logic, is an argument expressed
in three statements:

(a) Socrates is a man.
(b) All men are mortal, therefore,
(c) Socrates is mortal.

If statements (a) and (b) are true, then the truth of (c) is
established. To make this simple mathematical example,
we could write:

G. Peano
(1858-1932)

(i) Eight is divisible by two.
(ii) Any number divisible by two is an even number,
therefore,
(iii) Eight is an even number.

Thus, deduction in a nutshell is given a statement to be proven, often called a
conjecture or a theorem in mathematics, valid deductive steps are derived and a
proof may or may not be established, i.e., deduction is the application of a general
case to a particular case.

In contrast to deduction, inductive reasoning depends on working with each case,
and developing a conjecture by observing incidences till we have observed each and
every case. It is frequently used in mathematics and is a key aspect of scientific
reasoning, where collecting and analysing data is the norm. Thus, in simple language,
we can say the word induction means the generalisation from particular cases or facts.

<!-- page 150 -->
In algebra or in other discipline of mathematics, there are certain results or statements that are formulated in terms of $n$, where $n$ is a positive integer. To prove such
statements the well-suited principle that is used–based on the specific technique, is
known as the \textit{principle of mathematical induction}.

4.2 Motivation

In mathematics, we use a form of complete induction called mathematical induction.
To understand the basic principles of mathematical induction, suppose a set of thin
rectangular tiles are placed as shown in Fig 4.1.

Fig 4.1

When the first tile is pushed in the indicated direction, all the tiles will fall. To be
absolutely sure that all the tiles will fall, it is sufficient to know that

(a) The first tile falls, and
(b) In the event that any tile falls its successor necessarily falls.

This is the underlying principle of mathematical induction.

We know, the set of natural numbers $\mathbf{N}$ is a special ordered subset of the real
numbers. In fact, $\mathbf{N}$ is the smallest subset of $\mathbf{R}$ with the following property:

A set $S$ is said to be an inductive set if $1 \in S$ and $x + 1 \in S$ whenever $x \in S$. Since
$\mathbf{N}$ is the smallest subset of $\mathbf{R}$ which is an inductive set, it follows that any subset of $\mathbf{R}$
that is an inductive set must contain $\mathbf{N}$.

Illustration

Suppose we wish to find the formula for the sum of positive integers $1, 2, 3,...,n$, that is,
a formula which will give the value of $1 + 2 + 3$ when $n = 3$, the value $1 + 2 + 3 + 4$,
when $n = 4$ and so on and suppose that in some manner we are led to believe that the

formula $1 + 2 + 3+...+ n = \frac{n(n+1)}{2}$ is the correct one.

How can this formula actually be proved? We can, of course, verify the statement
for as many positive integral values of $n$ as we like, but this process will not prove the
formula for all values of $n$. What is needed is some kind of chain reaction which will

<!-- page 151 -->
have the effect that once the formula is proved for a particular positive integer the
formula will automatically follow for the next positive integer and the next indefinitely.
Such a reaction may be considered as produced by the method of mathematical induction.

4.3 The Principle of Mathematical Induction

Suppose there is a given statement P($n$) involving the natural number $n$ such that

(i) The statement is true for $n = 1$, i.e., $P(1)$ is true, and
(ii) If the statement is true for $n = k$ (where $k$ is some positive integer), then
the statement is also true for $n = k + 1$, i.e., truth of $P(k)$ implies the
truth of $P$ $(k + 1)$.

Then, $P(n)$ is true for all natural numbers $n$.

Property (i) is simply  a statement of fact. There may be situations when a
statement is true for all $n \ge 4$. In this case, step 1 will start from $n = 4$ and we shall
verify the result for $n = 4$, i.e., P(4).

Property (ii) is a conditional property. It does not assert that the given statement
is true for $n = k$, but only that if it is true for $n = k$, then it is also true for $n = k + 1$. So,
to prove that the property holds , only prove that conditional proposition:

If the statement is true for $n = k$, then it is also true for $n = k + 1$.

This is sometimes referred to as the inductive step. The assumption that the given
statement is true for $n = k$ in this inductive step is called the inductive hypothesis.

For example, frequently in mathematics, a formula will be discovered that appears
to fit a pattern like

$1 = 1^2 = 1$
$4 = 2^2 = 1 + 3$
$9 = 3^2 = 1 + 3 + 5$
$16 = 4^2 = 1 + 3 + 5 + 7$, etc.

It is worth to be noted that the sum of the first two odd natural numbers is the
square of second natural number, sum of the first three odd natural numbers is the
square of third natural number and so on.Thus, from this pattern it appears that

$$1 + 3 + 5 + 7 + ... + (2n - 1) = n^2, \text{ i.e,}$$

the sum of the first $n$ odd natural numbers is the square of $n$.

Let us write

$$P(n): 1 + 3 + 5 + 7 + ... + (2n - 1) = n^2.$$

We wish to prove that $\mathrm{P}(n)$ is true for all $n$.

The first step in a proof that uses mathematical induction is to prove that
P (1) is true. This step is called the basic step. Obviously

$1 = 1^2$, i.e., $P(1)$ is true.

The next step is called the inductive step. Here, we suppose that $\mathrm{P} (k)$ is true for some

<!-- page 152 -->
positive integer $k$ and we need to prove that $\mathrm{P} (k + 1)$ is true. Since $\mathrm{P} (k)$ is true, we
have

$$1 + 3 + 5 + 7 + ... + (2k - 1) = k^2 \quad ... (1)$$
Consider

Consider

$$1 + 3 + 5 + 7 + ... + (2k - 1) + \{2(k + 1) - 1\} \quad \dots (2)$$
$$= k^2 + (2k + 1) = (k + 1)^2 \quad \text{[Using (1)]}$$

Therefore, P $(k+1)$ is true and the inductive proof is now completed.
Hence P$(n)$ is true for all natural numbers $n$.

Example 1 For all $n \geq 1$, prove that

$$1^2 + 2^2 + 3^2 + 4^2 + ... + n^2 = \frac{n(n+1)(2n+1)}{6}.$$

Solution Let the given statement be $P(n)$, i.e.,

$$\mathrm{P}(n) : \quad 1^2 + 2^2 + 3^2 + 4^2 + \dots + n^2 \quad = \quad \frac{n(n+1)(2n+1)}{6}$$

For $n=1$, P(1): $1 = \frac{1(1+1)(2\times1+1)}{6} = \frac{1\times2\times3}{6} = 1$ which is true.

Assume that $\mathrm{P}(k)$ is true for some positive integer $k$, i.e.,

$$1^2 + 2^2 + 3^2 + 4^2 + \dots + k^2 = \frac{k(k+1)(2k+1)}{6} \dots (1)$$

We shall now prove that $P(k + 1)$ is also true. Now, we have

$$(1^2 + 2^2 + 3^2 + 4^2 + \dots + k^2 ) + (k + 1)^2$$

$$= \frac{k(k+1)(2k+1)}{6} + (k+1)^2 \qquad \qquad \qquad \qquad \text{[Using (1)]}$$

$$= \frac{k(k+1)(2k+1) + 6(k+1)^2}{6}$$

$$= \frac{(k+1)(2k^2 + 7k + 6)}{6}$$

$$= \frac{(k+1)(k+1+1)\{2(k+1)+1\}}{6}$$

Thus $\mathrm{P}(k+1)$ is true, whenever $\mathrm{P}(k)$ is true.

Hence, from the principle of mathematical induction, the statement $\mathrm{P}(n)$ is true
for all natural numbers $n$.

<!-- page 153 -->
Example 2 Prove that $2^n > n$ for all positive integers $n$.

Solution Let $P(n): 2^n > n$

When $n=1$, $2^1 > 1$. Hence P(1) is true.

Assume that $\mathrm{P}(k)$ is true for any positive integer $k$, i.e.,

$$2^k > k \hfill ... (1)$$

We shall now prove that $\mathrm{P}(k+1)$ is true whenever $\mathrm{P}(k)$ is true.

Multiplying both sides of (1) by 2, we get

$$2. 2^k > 2k$$

i.e., $2^{k+1} > 2k = k + k > k + 1$

Therefore, $\mathrm{P}(k+1)$ is true when $\mathrm{P}(k)$ is true. Hence, by principle of mathematical
induction, $\mathrm{P}(n)$ is true for every positive integer $n$.

Example 3 For all $n \geq 1$, prove that

$$\frac{1}{1.2} + \frac{1}{2.3} + \frac{1}{3.4} + ... + \frac{1}{n(n+1)} = \frac{n}{n+1}.$$

Solution We can write

$$\mathrm{P}(n): \frac{1}{1.2} + \frac{1}{2.3} + \frac{1}{3.4} + ... + \frac{1}{n(n+1)} = \frac{n}{n+1}$$

We note that $P(1): \frac{1}{1.2} = \frac{1}{2} = \frac{1}{1+1}$ , which is true. Thus, $P(n)$ is true for $n = 1$.

Assume that $\mathrm{P}(k)$ is true for some natural number $k$,

i.e., $\frac{1}{1.2} + \frac{1}{2.3} + \frac{1}{3.4} + ... + \frac{1}{k(k+1)} = \frac{k}{k+1}$ ... (1)

We need to prove that $\mathrm{P}(k+1)$ is true whenever $\mathrm{P}(k)$ is true. We have

$$\frac{1}{1.2}+\frac{1}{2.3}+\frac{1}{3.4}+\ldots+\frac{1}{k(k+1)}+\frac{1}{(k+1)(k+2)}$$

$$=\left[\frac{1}{1.2}+\frac{1}{2.3}+\frac{1}{3.4}+\ldots+\frac{1}{k(k+1)}\right]+\frac{1}{(k+1)(k+2)}$$

$$=\frac{k}{k+1}+\frac{1}{(k+1)(k+2)}$$

<!-- page 154 -->
$$= \frac{k(k+2)+1}{(k+1)(k+2)} = \frac{(k^2+2k+1)}{(k+1)(k+2)} = \frac{(k+1)^2}{(k+1)(k+2)} = \frac{k+1}{k+2} = \frac{k+1}{(k+1)+1}$$

Thus $\mathrm{P}(k+1)$ is true whenever $\mathrm{P}(k)$ is true. Hence, by the principle of mathematical
induction, $\mathrm{P}(n)$ is true for all natural numbers.

Example 4 For every positive integer $n$, prove that $7^n - 3^n$ is divisible by 4.

Solution We can write
P(n) : $7^n - 3^n$ is divisible by 4.
We note that
P(1): $7^1 - 3^1 = 4$ which is divisible by 4. Thus P(n) is true for $n = 1$
Let P(k) be true for some natural number $k$,
i.e., P(k) : $7^k - 3^k$ is divisible by 4.
We can write $7^k - 3^k = 4d$, where $d \in \mathbf{N}$.
Now, we wish to prove that P(k + 1) is true whenever P(k) is true.
Now $7^{(k+1)} - 3^{(k+1)} = 7^{(k+1)} - 7.3^k + 7.3^k - 3^{(k+1)}$
$= 7(7^k - 3^k) + (7 - 3)3^k = 7(4d) + (7 - 3)3^k$
$= 7(4d) + 4.3^k = 4(7d + 3^k)$
From the last line, we see that $7^{(k+1)} - 3^{(k+1)}$ is divisible by 4. Thus, P(k + 1) is true
when P(k) is true. Therefore, by principle of mathematical induction the statement is
true for every positive integer $n$.

Example 5 Prove that $(1 + x)^n \geq (1 + nx)$, for all natural number $n$, where $x > -1$.

Solution Let $P(n)$ be the given statement,
i.e., $P(n): (1 + x)^n \ge (1 + nx)$, for $x > -1$.

We note that $\mathrm{P}(n)$ is true when $n=1$, since $(1+x) \geq(1+x)$ for $x>-1$

Assume that

P(k): $(1 + x)^k \geq (1 + kx), x > -1$ is true.                                     $(1)$

We want to prove that $\mathrm{P}(k+1)$ is true for $x>-1$ whenever $\mathrm{P}(k)$ is true. ... (2)

Consider the identity

$$(1 + x)^{k + 1} = (1 + x)^k (1 + x)$$

Given that $x > -1$, so $(1+x) > 0$.

Therefore , by using $(1 + x)^k \geq (1 + kx)$, we have

$$(1 + x)^{k+1} \geq (1 + kx)(1 + x)$$

i.e. $\qquad (1+x)^{k+1} \geq (1+x+kx+kx^2). \qquad \dots (3)$

<!-- page 155 -->
Here $k$ is a natural number and $x^2 \ge 0$ so that $kx^2 \ge 0$. Therefore

$$(1 + x + kx + kx^2) \geq (1 + x + kx),$$

and so we obtain

$$(1+x)^{k+1} \geq (1+x+kx)$$

i.e. $(1+x)^{k+1} \geq [1+(1+k)x]$

Thus, the statement in (2) is established. Hence, by the principle of mathematical
induction, $\mathrm{P}(n)$ is true for all natural numbers.

Example 6 Prove that
$$2.7^n + 3.5^n - 5 \text{ is divisible by } 24, \text{ for all } n \in \mathbf{N}.$$

Solution Let the statement $P(n)$ be defined as

$\mathrm{P}(n) : 2.7^n + 3.5^n - 5$ is divisible by 24.

We note that $\mathrm{P}(n)$ is true for $n = 1$, since $2.7 + 3.5 - 5 = 24$, which is divisible by $24$.

Assume that $\mathrm{P}(k)$ is true

i.e. $2.7^k + 3.5^k - 5 = 24q$, when $q \in \mathbb{N}$ ... (1)

Now, we wish to prove that $\mathrm{P}(k+1)$ is true whenever $\mathrm{P}(k)$ is true.

We have

$$2.7^{k+1} + 3.5^{k+1} - 5 = 2.7^k . 7^1 + 3.5^k . 5^1 - 5$$
$$= 7 [2.7^k + 3.5^k - 5 - 3.5^k + 5] + 3.5^k . 5 - 5$$
$$= 7 [24q - 3.5^k + 5] + 15.5^k - 5$$
$$= 7 \times 24q - 21.5^k + 35 + 15.5^k - 5$$
$$= 7 \times 24q - 6.5^k + 30$$
$$= 7 \times 24q - 6 (5^k - 5)$$
$$= 7 \times 24q - 6 (4p) [(5^k - 5) \text{ is a multiple of } 4 \text{ (why?)]}$$
$$= 7 \times 24q - 24p$$
$$= 24 (7q - p)$$
$$= 24 \times r; r = 7q - p, \text{ is some natural number.} \quad \dots (2)$$

The expression on the R.H.S. of (1) is divisible by 24. Thus $P(k + 1)$ is true whenever
$P(k)$ is true.

Hence, by principle of mathematical induction, $\mathrm{P}(n)$ is true for all $n \in \mathrm{N}$.

<!-- page 156 -->
Example 7 Prove that

$$1^2 + 2^2 + ... + n^2 > \frac{n^3}{3}, n \in \mathbf{N}$$

Solution Let $P(n)$ be the given statement.

i.e., $\mathrm{P}(n) : 1^2 + 2^2 + ... + n^2 > \frac{n^3}{3}, \ n \in \mathbf{N}$

We note that $\mathrm{P}(n)$ is true for $n=1$ since $1^2 > \frac{1^3}{3}$

Assume that $P(k)$ is true

i.e. $\quad \mathrm{P}(k): 1^{2}+2^{2}+\ldots+k^{2}>\frac{k^{3}}{3} \quad \ldots(1)$

We shall now prove that $\mathrm{P}(k+1)$ is true whenever $\mathrm{P}(k)$ is true.

We have $1^2 + 2^2 + 3^2 + ... + k^2 + (k + 1)^2$

$$= \left(1^2 + 2^2 + ... + k^2\right) + (k + 1)^2 > \frac{k^3}{3} + (k + 1)^2 \quad \text{[by (1)]}$$

$$= \frac{1}{3} \left[k^3 + 3k^2 + 6k + 3\right]$$

$$= \frac{1}{3} \left[(k + 1)^3 + 3k + 2\right] > \frac{1}{3} (k + 1)^3$$

Therefore, $\mathrm{P}(k+1)$ is also true whenever $\mathrm{P}(k)$ is true. Hence, by mathematical induction
$\mathrm{P}(n)$ is true for all $n \in \mathbf{N}$.

Example 8 Prove the rule of exponents $(ab)^n = a^n b^n$
by using principle of mathematical induction for every natural number.

Solution Let $\mathrm{P}(n)$ be the given statement
i.e. $\mathrm{P}(n) : (ab)^n = a^n b^n$.
    We note that $\mathrm{P}(n)$ is true for $n = 1$ since $(ab)^1 = a^1 b^1$.
Let $\mathrm{P}(k)$ be true, i.e.,
    $$(ab)^k = a^k b^k \qquad \qquad \qquad \qquad \qquad \qquad \dots (1)$$
We shall now prove that $\mathrm{P}(k + 1)$ is true whenever $\mathrm{P}(k)$ is true.
    Now, we have
    $$(ab)^{k+1} = (ab)^k (ab)$$

<!-- page 157 -->
$$= (a^k \ b^k) \ (ab) \tag{by (1)}$$

$$= (a^k \ . \ a^1) \ (b^k \ . \ b^1) = a^{k+1} \ . \ b^{k+1}$$

Therefore, $\mathrm{P}(k+1)$ is also true whenever $\mathrm{P}(k)$ is true. Hence, by principle of mathematical induction, $\mathrm{P}(n)$ is true for all $n \in \mathrm{N}$.

EXERCISE 4.1

Prove the following by using the principle of mathematical induction for all $n \in \mathbf{N}$:

1. $1 + 3 + 3^2 + ... + 3^{n-1} = \frac{(3^n - 1)}{2}$.


2. $1^3 + 2^3 + 3^3 + ... + n^3 = \left( \frac{n(n+1)}{2} \right)^2$.


3. $1 + \frac{1}{(1+2)} + \frac{1}{(1+2+3)} + ... + \frac{1}{(1+2+3+...n)} = \frac{2n}{(n+1)}$.


4. $1.2.3 + 2.3.4 + ... + n(n+1)(n+2) = \frac{n(n+1)(n+2)(n+3)}{4}$.


5. $1.3 + 2.3^2 + 3.3^3 + ... + n.3^n = \frac{(2n-1)3^{n+1} + 3}{4}$.


6. $1.2 + 2.3 + 3.4 + ... + n.(n+1) = \left[ \frac{n(n+1)(n+2)}{3} \right]$.


7. $1.3 + 3.5 + 5.7 + ... + (2n-1)(2n+1) = \frac{n(4n^2 + 6n-1)}{3}$.


8. $1.2 + 2.2^2 + 3.2^3 + ... + n.2^n = (n-1)2^{n+1} + 2$.


9. $\frac{1}{2} + \frac{1}{4} + \frac{1}{8} + ... + \frac{1}{2^n} = 1 - \frac{1}{2^n}$.


10. $\frac{1}{2.5} + \frac{1}{5.8} + \frac{1}{8.11} + ... + \frac{1}{(3n-1)(3n+2)} = \frac{n}{(6n+4)}$.


11. $\frac{1}{1.2.3} + \frac{1}{2.3.4} + \frac{1}{3.4.5} + ... + \frac{1}{n(n+1)(n+2)} = \frac{n(n+3)}{4(n+1)(n+2)}$.

<!-- page 158 -->
12. $a + ar + ar^2 + \dots + ar^{n-1} = \frac{a(r^n - 1)}{r - 1}$.

13. $\left(1+\frac{3}{1}\right)\left(1+\frac{5}{4}\right)\left(1+\frac{7}{9}\right)\dots\left(1+\frac{(2n+1)}{n^2}\right)=(n+1)^2.$

14. $\left(1+\frac{1}{1}\right)\left(1+\frac{1}{2}\right)\left(1+\frac{1}{3}\right)\dots\left(1+\frac{1}{n}\right)=(n+1).$

15. $1^2 + 3^2 + 5^2 + ... + (2n-1)^2 = \frac{n(2n-1)(2n+1)}{3}$.

16. $\frac{1}{1.4} + \frac{1}{4.7} + \frac{1}{7.10} + ... + \frac{1}{(3n-2)(3n+1)} = \frac{n}{(3n+1)}.$

17. $\frac{1}{3.5} + \frac{1}{5.7} + \frac{1}{7.9} + ... + \frac{1}{(2n+1)(2n+3)} = \frac{n}{3(2n+3)}.$

18. $1 + 2 + 3 + \dots + n < \frac{1}{8}(2n + 1)^2.$

19. $n(n+1)(n+5)$ is a multiple of 3.

20. $10^{2n-1} + 1$ is divisible by 11.

21. $x^{2n} - y^{2n}$ is divisible by $x + y$.

22. $3^{2n+2} - 8n - 9$ is divisible by 8.

23. $41^n - 14^n$ is a multiple of 27.

24. $(2n + 7) < (n + 3)^2$.

Summary

$\diamond$ One key basis for mathematical thinking is deductive reasoning. In contrast to
deduction, inductive reasoning depends on working with different cases and
developing a conjecture by observing incidences till we have observed each
and every case. Thus, in simple language we can say the word ‘induction’
means the generalisation from particular cases or facts.
$\diamond$ The principle of mathematical induction is one such tool which can be used to
prove a wide variety of mathematical statements. Each such statement is
assumed as $P(n)$ associated with positive integer $n$, for which the correctness

<!-- page 159 -->
for the case $n=1$ is examined. Then assuming the truth of $\mathrm{P}(k)$ for some
positive integer $k$, the truth of $\mathrm{P}(k+1)$ is established.

Historical Note

Unlike other concepts and methods, proof by mathematical induction is not
the invention of a particular individual at a fixed moment. It is said that the principle
of mathematical induction was known by the Pythagoreans.
The French mathematician Blaise Pascal is credited with the origin of the
principle of mathematical induction.
The name induction was used by the English mathematician John Wallis.
Later the principle was employed to provide a proof of the binomial theorem.
De Morgan contributed many accomplishments in the field of mathematics
on many different subjects. He was the first person to define and name
“mathematical induction” and developed De Morgan’s rule to determine the
convergence of a mathematical series.
G. Peano undertook the task of deducing the properties of natural numbers
from a set of explicitly stated assumptions, now known as Peano’s axioms.The
principle of mathematical induction is a restatement of one of the Peano’s axioms.

<!-- page 160 -->
Chapter 5

COMPLEX NUMBERS AND
QUADRATIC EQUATIONS

❖ Mathematics is the Queen of Sciences and Arithmetic is the Queen of
Mathematics. – GAUSS ❖

5.1 Introduction

In earlier classes, we have studied linear equations in one
and two variables and quadratic equations in one variable.
We have seen that the equation $x^2 + 1 = 0$ has no real
solution as $x^2 + 1 = 0$ gives $x^2 = - 1$ and square of every
real number is non-negative. So, we need to extend the
real number system to a larger system so that we can
find the solution of the equation $x^2 = - 1$. In fact, the main
objective is to solve the equation $ax^2 + bx + c = 0$, where
$D = b^2 - 4ac < 0$, which is not possible in the system of
real numbers.

W. R. Hamilton
(1805-1865)

5.2 Complex Numbers

Let us denote $\sqrt{-1}$ by the symbol $i$. Then, we have $i^2 = -1$. This means that $i$ is a
solution of the equation $x^2 + 1 = 0$.

A number of the form $a + ib$, where $a$ and $b$ are real numbers, is defined to be a

complex number. For example, $2 + i3$, $(-1) + i\sqrt{3}$ , $4 + i\left(\frac{-1}{11}\right)$ are complex numbers.

For the complex number $z = a + ib$, $a$ is called the \textit{real part}, denoted by $\text{Re } z$ and
$b$ is called the \textit{imaginary part} denoted by $\text{Im } z$ \textit{of the complex number} $z$. For example,
if $z = 2 + i5$, then $\text{Re } z = 2$ and $\text{Im } z = 5$.

Two complex numbers $z_1 = a + ib$ and $z_2 = c + id$ are equal if $a = c$ and $b = d$.

<!-- page 161 -->
Example 1 If $4x + i(3x - y) = 3 + i (- 6)$, where $x$ and $y$ are real numbers, then find
the values of $x$ and $y$.

Solution We have

$$4x + i (3x - y) = 3 + i (-6) \qquad \dots (1)$$

Equating the real and the imaginary parts of (1), we get

$$4x = 3, 3x - y = -6,$$

which, on solving simultaneously, give $x = \frac{3}{4}$ and $y = \frac{33}{4}$.

5.3 Algebra of Complex Numbers

In this Section, we shall develop the algebra of complex numbers.

**5.3.1  Addition of two complex numbers** Let $z_1 = a + ib$ and $z_2 = c + id$ be any two
complex numbers. Then, the sum $z_1 + z_2$ is defined as follows:

$$z_1 + z_2 = (a + c) + i (b + d), \text{ which is again a complex number.}$$
For example, $(2 + i3) + (- 6 +i5) = (2 - 6) + i (3 + 5) = - 4 + i 8$

The addition of complex numbers satisfy the following properties:

(i) The closure law The sum of two complex numbers is a complex
number, i.e., $z_1 + z_2$ is a complex number for all complex numbers
$z_1$ and $z_2$.
(ii) The commutative law For any two complex numbers $z_1$ and $z_2$,
$z_1 + z_2 = z_2 + z_1$
(iii) The associative law For any three complex numbers $z_1$, $z_2$, $z_3$,
$(z_1 + z_2) + z_3 = z_1 + (z_2 + z_3)$.
(iv) The existence of additive identity There exists the complex number
$0 + i \ 0$ (denoted as $0$), called the additive identity or the zero complex
number, such that, for every complex number $z$, $z + 0 = z$.
(v) The existence of additive inverse To every complex number
$z = a + ib$, we have the complex number $- a + i(- b)$ (denoted as $- z$),
called the additive inverse or negative of $z$. We observe that $z + (-z) = 0$
(the additive identity).

**5.3.2 Difference of two complex numbers** Given any two complex numbers $z_1$ and
$z_2$, the difference $z_1 - z_2$ is defined as follows:

$$z_1 - z_2 = z_1 + (- z_2).$$
For example,
$$(6 + 3i) - (2 - i) = (6 + 3i) + (- 2 + i) = 4 + 4i$$
and
$$(2 - i) - (6 + 3i) = (2 - i) + (- 6 - 3i) = - 4 - 4i$$

<!-- page 162 -->
**5.3.3 Multiplication of two complex numbers** Let $z_1 = a + ib$ and $z_2 = c + id$ be any
two complex numbers. Then, the product $z_1 z_2$ is defined as follows:

$$z_1 z_2 = (ac - bd) + i(ad + bc)$$

For example, $(3 + i5) (2 + i6) = (3 \times 2 - 5 \times 6) + i(3 \times 6 + 5 \times 2) = - 24 + i28$

The multiplication of complex numbers possesses the following properties, which
we state without proofs.

(i) The closure law The product of two complex numbers is a complex number,
the product $z_1 z_2$ is a complex number for all complex numbers $z_1$ and $z_2$.
(ii) The commutative law For any two complex numbers $z_1$ and $z_2$,
$$z_1 z_2 = z_2 z_1$$
(iii) The associative law For any three complex numbers $z_1$, $z_2$, $z_3$,
$$(z_1 z_2) z_3 = z_1 (z_2 z_3).$$
(iv) The existence of multiplicative identity There exists the complex number
$1 + i 0$ (denoted as 1), called the multiplicative identity such that $z.1 = z$,
for every complex number $z$.
(v) The existence of multiplicative inverse For every non-zero complex
number $z = a + ib$ or $a + bi (a \neq 0, b \neq 0)$, we have the complex number
$$\frac{a}{a^2 + b^2} + i \frac{-b}{a^2 + b^2} \text{ (denoted by } \frac{1}{z} \text{ or } z^{-1} \text{), called the multiplicative inverse}$$
of $z$ such that
$$\frac{1}{z} \cdot \frac{-}{= 1} \text{ (the multiplicative identity).}$$
(vi) The distributive law For any three complex numbers $z_1$, $z_2$, $z_3$,
(a) $z_1 (z_2 + z_3) = z_1 z_2 + z_1 z_3$
(b) $(z_1 + z_2) z_3 = z_1 z_3 + z_2 z_3$

5.3.4 *Division of two complex numbers* Given any two complex numbers $z_1$ and $z_2$,

where $z_2 \neq 0$, the quotient $\frac{z_1}{z_2}$ is defined by

$$\frac{z_1}{z_2} = z_1 \frac{1}{z_2}$$

For example, let $z_1 = 6 + 3i$ and $z_2 = 2 - i$

Then $$\frac{z_1}{z_2} = \left( (6+3i) \times \frac{1}{2-i} \right) = (6+3i) \left( \frac{2}{2^2 + (-1)^2} + i \frac{-(-1)}{2^2 + (-1)^2} \right)$$

<!-- page 163 -->
$$= (6+3i) \left( \frac{2+i}{5} \right) = \frac{1}{5} [12 - 3 + i(6+6)] = \frac{1}{5} (9+12i)$$

5.3.5 Power of $i$ we know that

$$i^3 = i^2 i = (-1) i = -i, \qquad i^4 = \left(i^2\right)^2 = (-1)^2 = 1$$

$$i^5 = \left(i^2\right)^2 i = (-1)^2 i = i, \quad i^6 = \left(i^2\right)^3 = (-1)^3 = -1, \text{ etc.}$$

Also, we have $i^{-1} = \frac{1}{i} \times \frac{i}{i} = \frac{i}{-1} = -i, \quad i^{-2} = \frac{1}{i^2} = \frac{1}{-1} = -1,$

$$i^{-3} = \frac{1}{i^3} = \frac{1}{-i} \times \frac{i}{i} = \frac{i}{1} = i, \quad i^{-4} = \frac{1}{i^4} = \frac{1}{1} = 1$$

In general, for any integer $k$, $i^{4k} = 1$, $i^{4k+1} = i$, $i^{4k+2} = -1$, $i^{4k+3} = -i$

5.3.6 The square roots of a negative real number

Note that $i^2 = -1$ and $(-i)^2 = i^2 = -1$

Therefore, the square roots of $-1$ are $i, -i$. However, by the symbol $\sqrt{-1}$, we would
mean $i$ only.

Now, we can see that $i$ and $-i$ both are the solutions of the equation $x^2 + 1 = 0$ or
$x^2 = -1$.

Similarly $(\sqrt{3} i)^2 = (\sqrt{3})^2 i^2 = 3 (- 1) = - 3$

$$\left(-\sqrt{3} i\right)^2 = \left(-\sqrt{3}\right)^2 \ i^2 = -3$$

Therefore, the square roots of $-3$ are $\sqrt{3} \ i$ and $-\sqrt{3}i$.

Again, the symbol $\sqrt{-3}$ is meant to represent $\sqrt{3}i$ only, i.e., $\sqrt{-3} = \sqrt{3}i$.

Generally, if $a$ is a positive real number, $\sqrt{-a} = \sqrt{a} \sqrt{-1} = \sqrt{a} i$,

We already know that $\sqrt{a} \times \sqrt{b} = \sqrt{ab}$ for all positive real number $a$ and $b$. This
result also holds true when either $a > 0$, $b < 0$ or $a < 0$, $b > 0$. What if $a < 0$, $b < 0$?
Let us examine.

Note that

<!-- page 164 -->
$i^2 = \sqrt{-1} \sqrt{-1} = \sqrt{(-1)} (-1)$ (by assuming $\sqrt{a} \times \sqrt{b} = \sqrt{ab}$ for all real numbers)

$= \sqrt{1} = 1$, which is a contradiction to the fact that $i^2 = -1$.

Therefore, $\sqrt{a} \times \sqrt{b} \neq \sqrt{ab}$ if both $a$ and $b$ are negative real numbers.

Further, if any of $a$ and $b$ is zero, then, clearly, $\sqrt{a} \times \sqrt{b} = \sqrt{ab} = 0$.

5.3.7 Identities We prove the following identity

$(z_1 + z_2)^2 = z_1^2 + z_2^2 + 2z_1z_2$, for all complex numbers $z_1$ and $z_2$.

Proof We have, $(z_1 + z_2)^2 = (z_1 + z_2) (z_1 + z_2)$,
$= (z_1 + z_2) z_1 + (z_1 + z_2) z_2$ (Distributive law)
$= z_1^2 + z_2 z_1 + z_1 z_2 + z_2^2$ (Distributive law)
$= z_1^2 + z_1 z_2 + z_1 z_2 + z_2^2$ (Commutative law of multiplication)
$= z_1^2 + 2 z_1 z_2 + z_2^2$

Similarly, we can prove the following identities:

(i) $(z_1 - z_2)^2 = z_1^2 - 2 z_1 z_2 + z_2^2$

(ii) $(z_1 + z_2)^3 = z_1^3 + 3 z_1^2 z_2 + 3 z_1 z_2^2 + z_2^3$

(iii) $(z_1 - z_2)^3 = z_1^3 - 3 z_1^2 z_2 + 3 z_1 z_2^2 - z_2^3$

(iv) $z_1^2 - z_2^2 = (z_1 + z_2)(z_1 - z_2)$

In fact, many other identities which are true for all real numbers, can be proved
to be true for all complex numbers.

Example 2 Express the following in the form of $a + bi$:

(i) $(-5i)\left(\frac{1}{8}i\right)$                                     (ii) $(-i)(2i)\left(-\frac{1}{8}i\right)^3$


Solution (i) $(-5i)\left(\frac{1}{8}i\right) = \frac{-5}{8}i^2 = \frac{-5}{8}(-1) = \frac{5}{8} = \frac{5}{8} + i0$


(ii) $(-i)(2i)\left(-\frac{1}{8}i\right)^3 = 2 \times \frac{1}{8 \times 8 \times 8} \times i^5 = \frac{1}{256}(i^2)^2 \quad i = \frac{1}{256}i.$

<!-- page 165 -->
Example 3 Express $(5 - 3i)^3$ in the form $a + ib$.

Solution We have, $(5 - 3i)^3 = 5^3 - 3 \times 5^2 \times (3i) + 3 \times 5 (3i)^2 - (3i)^3$
$= 125 - 225i - 135 + 27i = - 10 - 198i.$

Example 4 Express $(-\sqrt{3}+\sqrt{-2})(2\sqrt{3}-i)$ in the form of $a+ib$

Solution We have, $(-\sqrt{3}+\sqrt{-2})(2\sqrt{3}-i) = (-\sqrt{3}+\sqrt{2}i)(2\sqrt{3}-i)$

$$= -6+\sqrt{3}i+2\sqrt{6}i-\sqrt{2}i^2 = (-6+\sqrt{2})+\sqrt{3}(1+2\sqrt{2})i$$

5.4 The Modulus and the Conjugate of a Complex Number

Let $z = a + ib$ be a complex number. Then, the modulus of $z$, denoted by $| z |$, is defined
to be the non-negative real number $\sqrt{a^2 + b^2}$ , i.e., $| z | = \sqrt{a^2 + b^2}$ and the conjugate
of $z$, denoted as $\overline{z}$ , is the complex number $a - ib$, i.e., $\overline{z} = a - ib$.

For example, $|3+i|=\sqrt{3^{2}+1^{2}}=\sqrt{10},|2-5 i|=\sqrt{2^{2}+(-5)^{2}}=\sqrt{29}$,

and $\overline{3+i}=3-i, \quad \overline{2-5i}=2+5i, \quad \overline{-3i-5}=3i-5$

Observe that the multiplicative inverse of the non-zero complex number $z$ is
given by

$$z^{-1} = \frac{1}{a+ib} = \frac{a}{a^2+b^2} + i \frac{-b}{a^2+b^2} = \frac{a-ib}{a^2+b^2} = \frac{\bar{z}}{|z|^2}$$

or $z \bar{z} = |z|^2$

Furthermore, the following results can easily be derived.
For any two compex numbers $z_1$ and $z_2$ , we have

(i) $|z_1 z_2| = |z_1| |z_2|$ (ii) $\left| \frac{z_1}{z_2} \right| = \left| \frac{z_1}{|z_2|} \right|$ provided $|z_2| \neq 0$


(iii) $\overline{z_1 z_2} = \overline{z_1} \overline{z_2}$ (iv) $\overline{z_1 \pm z_2} = \overline{z_1} \pm \overline{z_2}$ (v) $\left( \overline{\frac{z_1}{z_2}} \right) = \overline{\frac{z_1}{\overline{z}_2}}$ provided $z_2 \neq 0$.

<!-- page 166 -->
Example 5 Find the multiplicative inverse of $2-3i$.

Solution Let $z = 2 - 3i$

Then $\bar{z} = 2 + 3i$ and $|z|^2 = 2^2 + (-3)^2 = 13$

Therefore, the multiplicative inverse of $2 - 3i$ is given by

$$z^{-1} = \frac{\bar{z}}{|z|^2} = \frac{2 + 3i}{13} = \frac{2}{13} + \frac{3}{13}i$$

The above working can be reproduced in the following manner also,

$$z^{-1} = \frac{1}{2 - 3i} = \frac{2 + 3i}{(2 - 3i)(2 + 3i)}$$

$$= \frac{2 + 3i}{2^2 - (3i)^2} = \frac{2 + 3i}{13} = \frac{2}{13} + \frac{3}{13}i$$

Example 6 Express the following in the form $a + ib$

(i) $\frac{5 + \sqrt{2}i}{1 - \sqrt{2}i}$                                                                                              (ii) $i^{-35}$

Solution (i) We have, $\frac{5+\sqrt{2}i}{1-\sqrt{2}i} = \frac{5+\sqrt{2}i}{1-\sqrt{2}i} \times \frac{1+\sqrt{2}i}{1+\sqrt{2}i} = \frac{5+5\sqrt{2}i+\sqrt{2}i-2}{1-(\sqrt{2}i)^2}$


$$= \frac{3+6\sqrt{2}i}{1+2} = \frac{3(1+2\sqrt{2}i)}{3} = 1+2\sqrt{2}i.$$


(ii) $i^{-35} = \frac{1}{i^{35}} = \frac{1}{\left(i^2\right)^{17} i} = \frac{1}{-i} \times \frac{i}{i} = \frac{i}{-i^2} = i$

EXERCISE 5.1

Express each of the complex number given in the Exercises 1 to 10 in the
form $a + ib$.

1. $(5i)\left(-\frac{3}{5}i\right)$ 2. $i^9 + i^{19}$ 3. $i^{-39}$

<!-- page 167 -->
4. $3(7 + i7) + i(7 + i7)$

5. $(1 - i) - (-1 + i6)$

6. $\left(\frac{1}{5}+i\frac{2}{5}\right)-\left(4+i\frac{5}{2}\right)$

7. $\left[\left(\frac{1}{3}+i\frac{7}{3}\right)+\left(4+i\frac{1}{3}\right)\right]-\left(-\frac{4}{3}+i\right)$

8. $(1-i)^4$          9. $\left(\frac{1}{3}+3i\right)^3$          10. $\left(-2-\frac{1}{3}i\right)^3$

Find the multiplicative inverse of each of the complex numbers given in the
Exercises 11 to 13.

11. $4-3i$          12. $\sqrt{5}+3i$          13. $-i$

14. Express the following expression in the form of $a + ib$ :

$$\frac{(3+i\sqrt{5})(3-i\sqrt{5})}{(\sqrt{3}+\sqrt{2}i)-(\sqrt{3}-i\sqrt{2})}$$

5.5 Argand Plane and Polar Representation

We already know that corresponding to
each ordered pair of real numbers
$(x, y)$, we get a unique point in the XYplane and vice-versa with reference to a
set of mutually perpendicular lines known
as the $x$-axis and the $y$-axis. The complex
number $x + iy$ which corresponds to the
ordered pair $(x, y)$ can be represented
geometrically as the unique point $\mathrm{P}(x, y)$
in the XY-plane and vice-versa.

Some complex numbers such as
$2+4i, -2+3i, 0+1i, 2+0i, -5-2i$ and
$1-2i$ which correspond to the ordered
pairs $(2, 4), (-2, 3), (0, 1), (2, 0), (-5, -2)$, and $(1, -2)$, respectively, have been
represented geometrically by the points A, B, C, D, E, and F, respectively in
the Fig 5.1.

The plane having a complex number assigned to each of its point is called the
$complex$ $plane$ or the $Argand$ $plane$.

<!-- page 168 -->
Obviously, in the Argand plane, the modulus of the complex number
$x + iy = \sqrt{x^2 + y^2}$ is the distance between the point P$(x, y)$ and the origin O $(0, 0)$
(Fig 5.2). The points on the $x$-axis corresponds to the complex numbers of the form
$a + i 0$ and the points on the $y$-axis corresponds to the complex numbers of the form

Fig 5.2

$0 + i \ b$. The $x$-axis and $y$-axis in the Argand plane are called, respectively, the $real \ axis$
and the $imaginary \ axis$.

The representation of a complex number $z = x + iy$ and its conjugate
$z = x - iy$ in the Argand plane are, respectively, the points P $(x, y)$ and Q $(x, -y)$.

Geometrically, the point $(x, -y)$ is the mirror image of the point $(x, y)$ on the real
axis (Fig 5.3).

Fig 5.3

<!-- page 169 -->
5.5.1 Polar representation of a complex

5.5.1 Polar representation of a complex
number Let the point P represent the nonzero complex number $z = x + iy$. Let the
directed line segment OP be of length $r$ and
$\theta$ be the angle which OP makes with the
positive direction of $x$-axis (Fig 5.4).

We may note that the point P is
uniquely determined by the ordered pair of
real numbers $(r, \theta)$, called the polar
coordinates of the point P. We consider
the origin as the pole and the positive
direction of the $x$ axis as the initial line.

Fig 5.4

We have, $x = r \cos \theta$, $y = r \sin \theta$ and therefore, $z = r (\cos \theta + i \sin \theta)$. The latter
is said to be the polar form of the complex number. Here $r = \sqrt{x^2 + y^2} = |z|$ is the
modulus of $z$ and $\theta$ is called the argument (or amplitude) of $z$ which is denoted by $\arg z$.

For any complex number $z \neq 0$, there corresponds only one value of $\theta$ in
$0 \leq \theta < 2\pi$. However, any other interval of length $2\pi$, for example $-\pi < \theta \leq \pi$, can be
such an interval.We shall take the value of $\theta$ such that $-\pi < \theta \leq \pi$, called **principal**
**argument** of $z$ and is denoted by $\arg z$, unless specified otherwise. (Figs. 5.5 and 5.6)

Fig 5.5 $(0 \leq \theta < 2\pi)$

Fig 5.6 $(-\pi < \theta \le \pi)$

<!-- page 170 -->
Example 7 Represent the complex number $z=1+i\sqrt{3}$ in the polar form.
Solution Let $1=r\cos\theta$, $\sqrt{3}=r\sin\theta$
By squaring and adding, we get
$$r^2\left(\cos^2\theta + \sin^2\theta\right)=4$$
i.e., $r=\sqrt{4}=2$ (conventionally, $r>0$)
Therefore, $\cos\theta=\frac{1}{2}$, $\sin\theta=\frac{\sqrt{3}}{2}$, which gives $\theta=\frac{\pi}{3}$
Therefore, required polar form is $z=2\left(\cos\frac{\pi}{3}+i\sin\frac{\pi}{3}\right)$
The complex number $z=1+i\sqrt{3}$ is represented as shown in Fig 5.7.

The complex number $z = 1 + i\sqrt{3}$ is represented as shown in Fig 5.7.

Example 8 Convert the complex number $\frac{-16}{1+i\sqrt{3}}$ into polar form.

Solution The given complex number $\frac{-16}{1+i\sqrt{3}} = \frac{-16}{1+i\sqrt{3}} \times \frac{1-i\sqrt{3}}{1-i\sqrt{3}}$

$$= \frac{-16(1-i\sqrt{3})}{1-(i\sqrt{3})^2} = \frac{-16(1-i\sqrt{3})}{1+3} = -4(1-i\sqrt{3}) = -4 + i4\sqrt{3} \text{ (Fig 5.8).}$$

Let $-4 = r \cos \theta$, $4\sqrt{3} = r \sin \theta$

By squaring and adding, we get

$$16 + 48 = r^2 (\cos^2 \theta + \sin^2 \theta)$$

which gives

$$r^2 = 64, \text{ i.e., } r = 8$$

Hence

$$\cos \theta = -\frac{1}{2}, \sin \theta = \frac{\sqrt{3}}{2}$$

$$\theta = \pi - \frac{\pi}{3} = \frac{2\pi}{3}$$

Thus, the required polar form is $8 \left( \cos \frac{2\pi}{3} + i \sin \frac{2\pi}{3} \right)$

<!-- page 171 -->
EXERCISE 5.2

Find the modulus and the arguments of each of the complex numbers in
Exercises 1 to 2.

1. $z = -1 - \mathrm{i}\sqrt{3}$      2. $z = -\sqrt{3} + \mathrm{i}$

Convert each of the complex numbers given in Exercises 3 to 8 in the polar form:

**3.** $1-i$                                     **4.** $-1+i$                                     **5.** $-1-i$
**6.** $-3$                                       **7.** $\sqrt{3}+i$                                     **8.** $i$

5.6 Quadratic Equations

We are already familiar with the quadratic equations and have solved them in the set
of real numbers in the cases where discriminant is non-negative, i.e., $\ge 0$,

Let us consider the following quadratic equation:

$$ax^2 + bx + c = 0 \text{ with real coefficients } a, b, c \text{ and } a \neq 0.$$

Also, let us assume that the $b^2 - 4ac < 0$.

Now, we know that we can find the square root of negative real numbers in the
set of complex numbers. Therefore, the solutions to the above equation are available in
the set of complex numbers which are given by

$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a} = \frac{-b \pm \sqrt{4ac - b^2} i}{2a}$$

**Note** At this point of time, some would be interested to know as to how many
roots does an equation have? In this regard, the following theorem known as the
*Fundamental theorem of Algebra* is stated below (without proof).

“A polynomial equation has at least one root.”

As a consequence of this theorem, the following result, which is of immense
importance, is arrived at:

“A polynomial equation of degree $n$ has $n$ roots.”

Example 9 Solve $x^2 + 2 = 0$

Solution We have, $x^2 + 2 = 0$

or $x^2 = -2$ i.e., $x = \pm \sqrt{-2} = \pm \sqrt{2} i$

Example 10 Solve $x^2 + x + 1 = 0$

Solution Here, $b^2 - 4ac = 1^2 - 4 \times 1 \times 1 = 1 - 4 = -3$

<!-- page 172 -->
Therefore, the solutions are given by $x = \frac{-1 \pm \sqrt{-3}}{2 \times 1} = \frac{-1 \pm \sqrt{3}i}{2}$

Example 11 Solve $\sqrt{5}x^2 + x + \sqrt{5} = 0$

Solution Here, the discriminant of the equation is

$$1^2 - 4 \times \sqrt{5} \times \sqrt{5} = 1 - 20 = -19$$

Therefore, the solutions are

$$\frac{-1 \pm \sqrt{-19}}{2\sqrt{5}} = \frac{-1 \pm \sqrt{19}i}{2\sqrt{5}}.$$

EXERCISE 5.3

Solve each of the following equations:

1. $x^2 + 3 = 0$
2. $2x^2 + x + 1 = 0$
3. $x^2 + 3x + 9 = 0$
4. $-x^2 + x - 2 = 0$
5. $x^2 + 3x + 5 = 0$
6. $x^2 - x + 2 = 0$
7. $\sqrt{2}x^2 + x + \sqrt{2} = 0$
8. $\sqrt{3}x^2 - \sqrt{2}x + 3\sqrt{3} = 0$

9. $x^2 + x + \frac{1}{\sqrt{2}} = 0$
10. $x^2 + \frac{x}{\sqrt{2}} + 1 = 0$

Miscellaneous Examples

Example 12 Find the conjugate of $\frac{(3-2i)(2+3i)}{(1+2i)(2-i)}$.


Solution We have , $\frac{(3-2i)(2+3i)}{(1+2i)(2-i)}$


$$= \frac{6+9i-4i+6}{2-i+4i+2} = \frac{12+5i}{4+3i} \times \frac{4-3i}{4-3i}$$


$$= \frac{48-36i+20i+15}{16+9} = \frac{63-16i}{25} = \frac{63}{25} - \frac{16}{25}i$$


Therefore, conjugate of $\frac{(3-2i)(2+3i)}{(1+2i)(2-i)}$ is $\frac{63}{25} + \frac{16}{25}i$.

<!-- page 173 -->
Example 13 Find the modulus and argument of the complex numbers:

(i) $\frac{1+i}{1-i}$, (ii) $\frac{1}{1+i}$

Solution (i) We have, $\frac{1+i}{1-i} = \frac{1+i}{1-i} \times \frac{1+i}{1+i} = \frac{1-1+2i}{1+1} = i = 0 + i$

Now, let us put $0 = r \cos \theta$, $1 = r \sin \theta$
Squaring and adding, $r^2 = 1$ i.e., $r = 1$ so that
$$\cos \theta = 0, \sin \theta = 1$$

Therefore, $\theta = \frac{\pi}{2}$

Hence, the modulus of $\frac{1+i}{1-i}$ is $1$ and the argument is $\frac{\pi}{2}$.

(ii) We have $\frac{1}{1+i} = \frac{1-i}{(1+i)(1-i)} = \frac{1-i}{1+1} = \frac{1}{2} - \frac{i}{2}$

Let $\frac{1}{2} = r \cos \theta, -\frac{1}{2} = r \sin \theta$

Proceeding as in part (i) above, we get $r = \frac{1}{\sqrt{2}}$; $\cos \theta = \frac{1}{\sqrt{2}}$, $\sin \theta = \frac{-1}{\sqrt{2}}$

Therefore $\theta = \frac{-\pi}{4}$

Hence, the modulus of $\frac{1}{1+i}$ is $\frac{1}{\sqrt{2}}$, argument is $\frac{-\pi}{4}$.

Example 14 If $x + iy = \frac{a+ib}{a-ib}$, prove that $x^2 + y^2 = 1$.


Solution We have,


$$x + iy = \frac{(a+ib)(a+ib)}{(a-ib)(a+ib)} = \frac{a^2-b^2+2abi}{a^2+b^2} = \frac{a^2-b^2}{a^2+b^2} + \frac{2ab}{a^2+b^2}i$$

<!-- page 174 -->
So that, $x - iy = \frac{a^2 - b^2}{a^2 + b^2} - \frac{2ab}{a^2 + b^2}i$

Therefore,

$$x^2 + y^2 = (x + iy) (x - iy) = \frac{(a^2 - b^2)^2}{(a^2 + b^2)^2} + \frac{4a^2b^2}{(a^2 + b^2)^2} = \frac{(a^2 + b^2)^2}{(a^2 + b^2)^2} = 1$$

Example 15 Find real $\theta$ such that

$$\frac{3+2i\sin\theta}{1-2i\sin\theta}$$ is purely real.

Solution We have,

$$\frac{3+2i \sin\theta}{1-2i \sin\theta} = \frac{(3+2i \sin\theta)(1+2i \sin\theta)}{(1-2i \sin\theta)(1+2i \sin\theta)}$$

$$= \frac{3+6i \sin\theta + 2i \sin\theta - 4 \sin^2\theta}{1+4 \sin^2\theta} = \frac{3-4\sin^2\theta}{1+4\sin^2\theta} + \frac{8i \sin\theta}{1+4\sin^2\theta}$$

We are given the complex number to be real. Therefore

$$\frac{8\sin\theta}{1+4\sin^2\theta} = 0, \text{ i.e., } \sin\theta = 0$$

Thus $\theta = n\pi, n \in \mathbb{Z}.$

Example 16 Convert the complex number $z = \frac{i-1}{\cos \frac{\pi}{3} + i \sin \frac{\pi}{3}}$ in the polar form.


Solution We have, $z = \frac{i-1}{\frac{1}{2} + \frac{\sqrt{3}}{2} i}$


$$= \frac{2(i-1)}{1+\sqrt{3}i} \times \frac{1-\sqrt{3}i}{1-\sqrt{3}i} = \frac{2(i+\sqrt{3}-1+\sqrt{3}i)}{1+3} = \frac{\sqrt{3}-1}{2} + \frac{\sqrt{3}+1}{2} i$$


Now, put $\frac{\sqrt{3}-1}{2} = r \cos \theta$, $\frac{\sqrt{3}+1}{2} = r \sin \theta$

<!-- page 175 -->
Squaring and adding, we obtain

$$r^2 = \left( \frac{\sqrt{3}-1}{2} \right)^2 + \left( \frac{\sqrt{3}+1}{2} \right)^2 = \frac{2 \left( (\sqrt{3})^2 + 1 \right)}{4} = \frac{2 \times 4}{4} = 2$$

Hence, $r = \sqrt{2}$ which gives $\cos\theta = \frac{\sqrt{3}-1}{2\sqrt{2}}$, $\sin\theta = \frac{\sqrt{3}+1}{2\sqrt{2}}$

Therefore, $\theta = \frac{\pi}{4} + \frac{\pi}{6} = \frac{5\pi}{12}$ (Why?)

Hence, the polar form is

$$\sqrt{2} \left( \cos \frac{5\pi}{12} + i \sin \frac{5\pi}{12} \right)$$

Miscellaneous Exercise on Chapter 5

1. Evaluate: $\left[i^{18}+\left(\frac{1}{i}\right)^{25}\right]^3$.


2. For any two complex numbers $z_1$ and $z_2$, prove that
$\operatorname{Re}\left(z_1 z_2\right)=\operatorname{Re} z_1 \operatorname{Re} z_2-\operatorname{Im} z_1 \operatorname{Im} z_2$.


3. Reduce $\left(\frac{1}{1-4 i}-\frac{2}{1+i}\right)\left(\frac{3-4 i}{5+i}\right)$ to the standard form .


4. If $x-i y=\sqrt{\frac{a-i b}{c-i d}}$ prove that $\left(x^2+y^2\right)^2=\frac{a^2+b^2}{c^2+d^2}$.


5. Convert the following in the polar form:


(i) $\frac{1+7 i}{(2-i)^2}$, (ii) $\frac{1+3 i}{1-2 i}$

Solve each of the equation in Exercises 6 to 9.

6. $3x^2 - 4x + \frac{20}{3} = 0$
7. $x^2 - 2x + \frac{3}{2} = 0$
8. $27x^2 - 10x + 1 = 0$

<!-- page 176 -->
9. $21x^2 - 28x + 10 = 0$

10. If $z_1 = 2 - i, z_2 = 1 + i$, find $\left| \frac{z_1 + z_2 + 1}{z_1 - z_2 + 1} \right|$.

11. If $a + ib = \frac{(x+i)^2}{2x^2+1}$, prove that $a^2 + b^2 = \frac{(x^2+1)^2}{(2x^2+1)^2}$.

12. Let $z_1 = 2 - i$, $z_2 = -2 + i$. Find

(i) $\text{Re}\left(\frac{z_1 z_2}{\bar{z}_1}\right)$, \qquad (ii) $\text{Im}\left(\frac{1}{z_1 \bar{z}_1}\right)$.

13. Find the modulus and argument of the complex number $\frac{1+2i}{1-3i}$.

14. Find the real numbers $x$ and $y$ if $(x - iy) (3 + 5i)$ is the conjugate of $-6 - 24i$.

15. Find the modulus of $\frac{1+i}{1-i} - \frac{1-i}{1+i}$.

16. If $(x + iy)^3 = u + iv$, then show that $\frac{u}{x} + \frac{v}{y} = 4(x^2 - y^2)$.

17. If $\alpha$ and $\beta$ are different complex numbers with $|\beta|=1$, then find $\left|\frac{\beta-\alpha}{1-\bar{\alpha}\beta}\right|$.

18. Find the number of non-zero integral solutions of the equation $|1-i|^x = 2^x$.

19. If $(a + ib) (c + id) (e + if) (g + ih) = \mathrm{A} + i\mathrm{B}$, then show that
$$(a^2 + b^2) (c^2 + d^2) (e^2 + f^2) (g^2 + h^2) = \mathrm{A}^2 + \mathrm{B}^2$$

20. If $\left(\frac{1+i}{1-i}\right)^m = 1$, then find the least positive integral value of $m$.

<!-- page 177 -->
Summary

A number of the form $a+ib$, where $a$ and $b$ are real numbers, is called a
complex number, $a$ is called the real part and $b$ is called the imaginary part
of the complex number.
Let $z_{1}=a+ib$ and $z_{2}=c+id$. Then
(i) $z_{1}+z_{2}=(a+c)+i(b+d)$
(ii) $z_{1} z_{2}=(a c-b d)+i(a d+b c)$
For any non-zero complex number $z=a+i b(a \neq 0, b \neq 0)$, there exists the
complex number $\frac{a}{a^{2}+b^{2}}+i \frac{-b}{a^{2}+b^{2}}$, denoted by $\frac{1}{z}$ or $z^{-1}$, called the
multiplicative inverse of $z$ such that $(a+i b)\left(\frac{a^{2}}{a^{2}+b^{2}}+i \frac{-b}{a^{2}+b^{2}}\right)=1+i 0=1$
For any integer $k, i^{4 k}=1, i^{4 k+1}=i, i^{4 k+2}=-1, i^{4 k+3}=-i$
The conjugate of the complex number $z=a+i b$, denoted by $\bar{z}$, is given by
$\bar{z}=a-i b$.
The polar form of the complex number $z=x+i y$ is $r(\cos \theta+i \sin \theta)$, where
$r=\sqrt{x^{2}+y^{2}}$ (the modulus of $z$) and $\cos \theta=\frac{x}{r}, \sin \theta=\frac{y}{r}$. ($\theta$ is known as the
argument of $z$. The value of $\theta$, such that $-\pi<\theta \leq \pi$, is called the principal
argument of $z$.
A polynomial equation of $n$ degree has $n$ roots.
The solutions of the quadratic equation $a x^{2}+b x+c=0$, where $a, b, c \in \mathbb{R}$,
$a \neq 0, b^{2}-4 a c<0$, are given by $x=\frac{-b \pm \sqrt{4 a c-b^{2} i}}{2 a}$.

<!-- page 178 -->
Historical Note

The fact that square root of a negative number does not exist in the real number
system was recognised by the Greeks. But the credit goes to the Indian
mathematician Mahavira (850) who first stated this difficulty clearly. “He mentions
in his work ‘Ganitasara Sangraha’ as in the nature of things a negative (quantity)
is not a square (quantity)’, it has, therefore, no square root”. Bhaskara, another
Indian mathematician, also writes in his work Bijaganita, written in 1150. “There
is no square root of a negative quantity, for it is not a square.” Cardan (1545)
considered the problem of solving
$$x + y = 10, xy = 40.$$
He obtained $x = 5 + \sqrt{-15}$ and $y = 5 - \sqrt{-15}$ as the solution of it, which
was discarded by him by saying that these numbers are ‘useless’. Albert Girard
(about 1625) accepted square root of negative numbers and said that this will
enable us to get as many roots as the degree of the polynomial equation. Euler
was the first to introduce the symbol $i$ for $\sqrt{-1}$ and W.R. Hamilton (about
1830) regarded the complex number $a + ib$ as an ordered pair of real numbers
$(a, b)$ thus giving it a purely mathematical definition and avoiding use of the so
called ‘imaginary numbers’.

<!-- page 179 -->
Chapter 6

LINEAR EQUIVALITIES

***Mathematics is the art of saying many things in many***
***different ways. – MAXWELL***

6.1 Introduction

In earlier classes, we have studied equations in one variable and two variables and also
solved some statement problems by translating them in the form of equations. Now a
natural question arises: ‘Is it always possible to translate a statement problem in the
form of an equation? For example, the height of all the students in your class is less
than 160 cm. Your classroom can occupy atmost 60 tables or chairs or both. Here we
get certain statements involving a sign ‘$<$’ (less than), ‘$>$’ (greater than), ‘$\le$’ (less than
or equal) and $\ge$ (greater than or equal) which are known as inequalities.

In this Chapter, we will study linear inequalities in one and two variables. The
study of inequalities is very useful in solving problems in the field of science, mathematics,
statistics, economics, psychology, etc.

6.2 Inequalities

Let us consider the following situations:

(i) Ravi goes to market with $₹200$ to buy rice, which is available in packets of $1\text{kg}$. The
price of one packet of rice is $₹30$. If $x$ denotes the number of packets of rice, which he
buys, then the total amount spent by him is $₹30x$. Since, he has to buy rice in packets
only, he may not be able to spend the entire amount of $₹200$. (Why?) Hence

$$30x < 200$$

$$... (1)$$

Clearly the statement (i) is not an equation as it does not involve the sign of equality.

(ii) Reshma has ₹ 120 and wants to buy some registers and pens. The cost of one
register is ₹ 40 and that of a pen is ₹ 20. In this case, if $x$ denotes the number of
registers and $y$, the number of pens which Reshma buys, then the total amount spent by
her is ₹ $(40x + 20y)$ and we have

$$40x + 20y \leq 120 \qquad \dots (2)$$

<!-- page 180 -->
Since in this case the total amount spent may be upto ₹ 120. Note that the statement (2)
consists of two statements

$$40x + 20y < 120 \quad \dots (3)$$
and $$40x + 20y = 120 \quad \dots (4)$$

Statement (3) is not an equation, i.e., it is an inequality while statement (4) is an equation.

Definition 1 Two real numbers or two algebraic expressions related by the symbol
‘<’, ‘$>$’, ‘$\le$’ or ‘$\ge$’ form an inequality.
Statements such as (1), (2) and (3) above are inequalities.

$3 < 5$; $7 > 5$ are the examples of numerical inequalities while

$x < 5$; $y > 2$; $x \ge 3$, $y \le 4$ are some examples of literal inequalities.

$3 < 5 < 7$ (read as 5 is greater than 3 and less than 7), $3 \le x < 5$ (read as $x$ is greater
than or equal to 3 and less than 5) and $2 < y \le 4$ are the examples of double inequalities.

Some more examples of inequalities are:

$$NCKER \\ REQUIR \\ ... (5) \\ ... (6) \\ ... (7) \\ ... (8) \\ ... (9) \\ ... (10) \\ ... (11) \\ ... (12) \\ ... (13) \\ ... (14)$$

Inequalities (5), (6), (9), (10) and (14) are *strict inequalities* while inequalities (7), (8),
(11), (12), and (13) are *slack inequalities*. Inequalities from (5) to (8) are *linear*
*inequalities* in one variable $x$ when $a \neq 0$, while inequalities from (9) to (12) are *linear*
*inequalities in two variables* $x$ and $y$ when $a \neq 0$, $b \neq 0$.

Inequalities (13) and (14) are not linear (in fact, these are quadratic inequalities
in one variable $x$ when $a \neq 0$).

In this Chapter, we shall confine ourselves to the study of linear inequalities in one
and two variables only.

<!-- page 181 -->
6.3 Algebraic Solutions of Linear Inequalities in One Variable and their
Graphical Representation

Let us consider the inequality (1) of Section 6.2, viz, $30x < 200$
Note that here $x$ denotes the number of packets of rice.

Obviously, $x$ cannot be a negative integer or a fraction. Left hand side (L.H.S.) of this
inequality is $30x$ and right hand side (RHS) is 200. Therefore, we have

For $x = 0$, L.H.S. $= 30$ $(0) = 0 < 200$ (R.H.S.), which is true.
For $x = 1$, L.H.S. $= 30$ $(1) = 30 < 200$ (R.H.S.), which is true.
For $x = 2$, L.H.S. $= 30$ $(2) = 60 < 200$, which is true.
For $x = 3$, L.H.S. $= 30$ $(3) = 90 < 200$, which is true.
For $x = 4$, L.H.S. $= 30$ $(4) = 120 < 200$, which is true.
For $x = 5$, L.H.S. $= 30$ $(5) = 150 < 200$, which is true.
For $x = 6$, L.H.S. $= 30$ $(6) = 180 < 200$, which is true.
For $x = 7$, L.H.S. $= 30$ $(7) = 210 < 200$, which is false.

In the above situation, we find that the values of $x$, which makes the above
inequality a true statement, are 0,1,2,3,4,5,6. These values of $x$, which make above
inequality a true statement, are called \textit{solutions} of inequality and the set $\{0,1,2,3,4,5,6\}$
is called its \textit{solution set}.

Thus, any solution of an inequality in one variable is a value of the variable
which makes it a true statement.

We have found the solutions of the above inequality by $trial$ $and$ $error$ method
which is not very efficient. Obviously, this method is time consuming and sometimes
not feasible. We must have some better or systematic techniques for solving inequalities.
Before that we should go through some more properties of numerical inequalities and
follow them as rules while solving the inequalities.

You will recall that while solving linear equations, we followed the following rules:

Rule 1 Equal numbers may be added to (or subtracted from) both sides of an equation.

Rule 2 Both sides of an equation may be multiplied (or divided) by the same non-zero
number.

In the case of solving inequalities, we again follow the same rules except with a
difference that in Rule 2, the sign of inequality is reversed (i.e., ‘$<$ becomes ‘$>$’, $\leq$
becomes ‘$\geq$’ and so on) whenever we multiply (or divide) both sides of an inequality by
a negative number. It is evident from the facts that

$3 > 2$ while $-3 < -2,$
$-8 < -7$ while $(-8) (-2) > (-7) (-2)$ , i.e., $16 > 14.$

<!-- page 182 -->
Thus, we state the following rules for solving an inequality:

Rule 1 Equal numbers may be added to (or subtracted from) both sides of an inequality
without affecting the sign of inequality.

Rule 2 Both sides of an inequality can be multiplied (or divided) by the same positive
number. But when both sides are multiplied or divided by a negative number, then the
sign of inequality is $reversed$.

Now, let us consider some examples.

Example 1 Solve $30\ x < 200$ when
(i) $x$ is a natural number, (ii) $x$ is an integer.

Solution We are given $30 x < 200$

or $\frac{30x}{30} < \frac{200}{30}$ (Rule 2), i.e., $x < 20 / 3$.

(i) When $x$ is a natural number, in this case the following values of $x$ make the
statement true.

$1, 2, 3, 4, 5, 6.$

The solution set of the inequality is $\{1,2,3,4,5,6\}$.

(ii) When $x$ is an integer, the solutions of the given inequality are
$$..., -3, -2, -1, 0, 1, 2, 3, 4, 5, 6$$

The solution set of the inequality is $\{...,-3, -2,-1, 0, 1, 2, 3, 4, 5, 6\}$

Example 2 Solve $5x - 3 < 3x + 1$ when
(i) $x$ is an integer,
(ii) $x$ is a real number.
Solution We have, $5x - 3 < 3x + 1$
or $5x - 3 + 3 < 3x + 1 + 3$ (Rule 1)
or $5x < 3x + 4$
or $5x - 3x < 3x + 4 - 3x$ (Rule 1)
or $2x < 4$
or $x < 2$ (Rule 2)
(i) When $x$ is an integer, the solutions of the given inequality are
..., $- 4, - 3, - 2, - 1, 0, 1$
(ii) When $x$ is a real number, the solutions of the inequality are given by $x < 2$,
i.e., all real numbers $x$ which are less than 2. Therefore, the solution set of
the inequality is $x \in (-\infty, 2)$.
We have considered solutions of inequalities in the set of natural numbers, set of
integers and in the set of real numbers. Henceforth, unless stated otherwise, we shall
solve the inequalities in this Chapter in the set of real numbers.

<!-- page 183 -->
Example 3 Solve $4x + 3 < 6x + 7$.

Solution We have, $4x + 3 < 6x + 7$
or $4x - 6x < 6x + 4 - 6x$
or $-2x < 4$ or $x > -2$
i.e., all the real numbers which are greater than $-2$, are the solutions of the given
inequality. Hence, the solution set is $(-2, \infty)$.

Example 4 Solve $\frac{5-2x}{3} \leq \frac{x}{6}-5$.

Solution We have

$$\frac{5-2x}{3} \leq \frac{x}{6}-5$$

or $2(5-2x) \leq x-30$.
or $10-4x \leq x-30$
or $-5x \leq -40$, i.e., $x \geq 8$

Thus, all real numbers $x$ which are greater than or equal to 8 are the solutions of the
given inequality, i.e., $x \in [8, \infty)$.

Example 5 Solve $7x + 3 < 5x + 9$. Show the graph of the solutions on number line.

Solution We have $7x + 3 < 5x + 9$ or
$2x < 6$ or $x < 3$
The graphical representation of the solutions are given in Fig 6.1.

Fig 6.1

Example 6 Solve $\frac{3x-4}{2} \geq \frac{x+1}{4} - 1$. Show the graph of the solutions on number line.

Solution We have

$$\frac{3x-4}{2} \geq \frac{x+1}{4} - 1$$

or

$$\frac{3x-4}{2} \geq \frac{x-3}{4}$$

or

$$2(3x-4) \geq (x-3)$$

<!-- page 184 -->
or $6x - 8 \ge x - 3$
or $5x \ge 5$ or $x \ge 1$

The graphical representation of solutions is given in Fig 6.2.

Fig 6.2

Example 7 The marks obtained by a student of Class XI in first and second terminal
examination are 62 and 48, respectively. Find the minimum marks he should get in the
annual examination to have an average of at least 60 marks.

Solution Let $x$ be the marks obtained by student in the annual examination. Then

$$\frac{62+48+x}{3} \geq 60$$

or $110 + x \geq 180$

or $x \geq 70$

Thus, the student must obtain a minimum of 70 marks to get an average of at least
60 marks.

Thus, the student must obtain a minimum of 70 marks to get an average of at least
60 marks.

Example 8 Find all pairs of consecutive odd natural numbers, both of which are larger
than 10, such that their sum is less than 40.

Solution Let $x$ be the smaller of the two consecutive odd natural number, so that the
other one is $x + 2$. Then, we should have
$$x > 10 \quad \dots \quad (1)$$
and $$x + (x + 2) < 40 \quad \dots \quad (2)$$
Solving (2), we get
$$2x + 2 < 40$$
i.e., $x < 19 \quad \dots \quad (3)$
From (1) and (3), we get
$$10 < x < 19$$

Since $x$ is an odd number, $x$ can take the values 11, 13, 15, and 17. So, the required
possible pairs will be
$$(11, 13), (13, 15), (15, 17), (17, 19)$$

<!-- page 185 -->
EXERCISE 6.1

1.  Solve $24x < 100$, when
    (i)   $x$ is a natural number.                 (ii)  $x$ is an integer.
2.  Solve $- 12x > 30$, when
    (i)   $x$ is a natural number.                 (ii)  $x$ is an integer.
3.  Solve $5x - 3 < 7$, when
    (i)   $x$ is an integer.                 (ii)  $x$ is a real number.
4.  Solve $3x + 8 > 2$, when
    (i)   $x$ is an integer.                 (ii)  $x$ is a real number.

Solve the inequalities in Exercises 5 to 16 for real $x$.

5. $4x + 3 < 5x + 7$

6. $3x - 7 > 5x - 1$

7. $3(x-1) \leq 2(x-3)$

8. $3(2-x) \geq 2(1-x)$

9. $x+\frac{x}{2}+\frac{x}{3}<11$

10. $\frac{x}{3} > \frac{x}{2} + 1$

11. $\frac{3(x-2)}{5} \leq \frac{5(2-x)}{3}$

12. $\frac{1}{2}\left(\frac{3x}{5}+4\right)\ge\frac{1}{3}(x-6)$

13. $2(2x+3)-10<6(x-2)$

14. $37 - (3x + 5) \geq 9x - 8 (x - 3)$

15. $\frac{x}{4} < \frac{(5x-2)}{3} - \frac{(7x-3)}{5}$

16. $\frac{(2x-1)}{3} \geq \frac{(3x-2)}{4} - \frac{(2-x)}{5}$

Solve the inequalities in Exercises 17 to 20 and show the graph of the solution in each
case on number line

17. $3x - 2 < 2x + 1$                                   18. $5x - 3 \ge 3x - 5$

19. $3(1 - x) < 2(x + 4)$                                 20. $\frac{x}{2} \ge \frac{(5x - 2)}{3} - \frac{(7x - 3)}{5}$

21. Ravi obtained 70 and 75 marks in first two unit test. Find the minimum marks he
should get in the third test to have an average of at least 60 marks.

22. To receive Grade ‘A’ in a course, one must obtain an average of 90 marks or
more in five examinations (each of 100 marks). If Sunita’s marks in first four
examinations are 87, 92, 94 and 95, find minimum marks that Sunita must obtain
in fifth examination to get grade ‘A’ in the course.

23. Find all pairs of consecutive odd positive integers both of which are smaller than
10 such that their sum is more than 11.

24. Find all pairs of consecutive even positive integers, both of which are larger than
5 such that their sum is less than 23.

<!-- page 186 -->
25. The longest side of a triangle is 3 times the shortest side and the third side is 2 cm
shorter than the longest side. If the perimeter of the triangle is at least 61 cm, find
the minimum length of the shortest side.

26. A man wants to cut three lengths from a single piece of board of length $91\text{cm}$.
The second length is to be $3\text{cm}$ longer than the shortest and the third length is to
be twice as long as the shortest. What are the possible lengths of the shortest
board if the third piece is to be at least $5\text{cm}$ longer than the second?

[Hint: If $x$ is the length of the shortest board, then $x$ , $(x + 3)$ and $2x$ are the
lengths of the second and third piece, respectively. Thus, $x + (x + 3) + 2x \le 91$ and
$2x \ge (x + 3) + 5$].

6.4 Graphical Solution of Linear Inequalities in Two Variables

In earlier section, we have seen that a graph of an inequality in one variable is a visual
representation and is a convenient way to represent the solutions of the inequality.
Now, we will discuss graph of a linear inequality in two variables.

We know that a line divides the Cartesian plane into two parts. Each part is
known as a half plane. A vertical line will divide the plane in left and right half planes
and a non-vertical line will divide the plane into lower and upper half planes
(Figs. 6.3 and 6.4).

Fig 6.3                                                                 Fig 6.4

A point in the Cartesian plane will either lie on a line or will lie in either of the half
planes I or II. We shall now examine the relationship, if any, of the points in the plane
and the inequalities $ax + by < c$ or $ax + by > c$.

Let us consider the line

$$ax + by = c, \quad a \neq 0, \quad b \neq 0 \quad ... \ (1)$$

<!-- page 187 -->
There are three possibilities namely:

(i) $ax + by = c$ (ii) $ax + by > c$ (iii) $ax + by < c.$

In case (i), clearly, all points $(x, y)$ satisfying (i) lie on the line it represents and
conversely. Consider case (ii), let us first assume that $b > 0$. Consider a point P $(\alpha, \beta)$
on the line $ax + by = c$, $b > 0$, so that
$a\alpha + b\beta = c$.Take an arbitrary point
Q $(\alpha, \gamma)$ in the half plane II (Fig 6.5).

Now, from Fig 6.5, we interpret,

$$\gamma > \beta \quad (\text{Why?})$$

or $b\gamma > b\beta$ or $a\alpha + b\gamma > a\alpha + b\beta$
(Why?)

or $a\alpha + b\gamma > c$

i.e., $Q(\alpha, \gamma)$ satisfies the inequality
$ax + by > c$.

Thus, all the points lying in the half
plane II above the line $ax + by = c$ satisfies
the inequality $ax + by > c$. Conversely, let $(\alpha, \beta)$ be a point on line $ax + by = c$ and an
arbitrary point $Q(\alpha, \gamma)$ satisfying

$$ax + by > c$$
so that $$a\alpha + b\gamma > c$$
$$\Rightarrow \quad a\alpha + b\gamma > a\alpha + b\beta \text{ (Why?)}$$
$$\Rightarrow \quad \gamma > \beta \quad \text{(as } b > 0\text{)}$$

This means that the point $(\alpha, \gamma)$ lies in the half plane II.

Thus, any point in the half plane II satisfies $ax + by > c$, and conversely any point
satisfying the inequality $ax + by > c$ lies in half plane II.

In case $b < 0$, we can similarly prove that any point satisfying $ax + by > c$ lies in
the half plane I, and conversely.

Hence, we deduce that all points satisfying $ax + by > c$ lies in one of the half
planes II or I according as $b > 0$ or $b < 0$, and conversely.

Thus, graph of the inequality $ax + by > c$ will be one of the half plane (called
solution region) and represented by shading in the corresponding half plane.

Note 1 The region containing all the solutions of an inequality is called the
solution region.
2. In order to identify the half plane represented by an inequality, it is just sufficient
to take any point $(a, b)$ (not online) and check whether it satisfies the inequality or
not. If it satisfies, then the inequality represents the half plane and shade the region

<!-- page 188 -->
which contains the point, otherwise, the inequality represents that half plane which
does not contain the point within it. For convenience, the point $(0, 0)$ is preferred.
3. If an inequality is of the type $ax + by \ge c$ or $ax + by \le c$, then the points on the
line $ax + by = c$ are also included in the solution region. So draw a dark line in the
solution region.
4. If an inequality is of the form $ax + by > c$ or $ax + by < c$, then the points on the
line $ax + by = c$ are not to be included in the solution region. So draw a broken or
dotted line in the solution region.

In Section 6.2, we obtained the following linear inequalities in two variables
$x$ and $y$: $40x + 20y \le 120$ ... (1)

while translating the word problem of purchasing of registers and pens by Reshma.

Let us now solve this inequality keeping in mind that $x$ and $y$ can be only whole
numbers, since the number of articles cannot be a fraction or a negative number. In
this case, we find the pairs of values of $x$ and $y$, which make the statement (1) true. In
fact, the set of such pairs will be the \textit{solution set} of the inequality (1).

To start with, let $x = 0$. Then L.H.S. of (1) is

$$40x + 20y = 40 (0) + 20y = 20y.$$

Thus, we have

$20y \le 120 \text{ or } y \le 6 \dots (2)$

For $x = 0$, the corresponding values of $y$ can be $0, 1, 2, 3, 4, 5, 6$ only. In this case, the
solutions of $(1)$ are $(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),$
$(0, 5)$ and $(0, 6)$.

Similarly, other solutions of (1), when
$x = 1, 2$ and $3$ are:      $(1, 0), (1, 1), (1, 2), (1,$
$3), \quad (1, 4), \quad (2, 0), (2, 1), (2, 2), (3, 0)$
This is shown in Fig 6.6.

Let us now extend the domain of $x$ and $y$
from whole numbers to real numbers, and see
what will be the solutions of (1) in this case.
You will see that the graphical method of solution
will be very convenient in this case. For this
purpose, let us consider the (corresponding)
equation and draw its graph.

$$40x + 20y = 120 \quad \dots (3)$$

In order to draw the graph of the inequality
(1), we take one point say (0, 0), in half plane I
and check whether values of $x$ and $y$ satisfy the
inequality or not.

Fig 6.6

<!-- page 189 -->
We observe that $x = 0$, $y = 0$ satisfy the
inequality. Thus, we say that the half plane I is the
graph (Fig 6.7) of the inequality. Since the points on
the line also satisfy the inequality (1) above, the line
is also a part of the graph.

Thus, the graph of the given inequality is half
plane I including the line itself. Clearly half plane II
is not the part of the graph. Hence, \textit{solutions} of
inequality (1) will consist of all the points of its graph
(half plane I including the line).

We shall now consider some examples to
explain the above procedure for solving a linear
inequality involving two variables.

Fig 6.7

Example 9 Solve $3x + 2y > 6$ graphically.

Solution Graph of $3x + 2y = 6$ is given as dotted line in the Fig 6.8.

This line divides the $xy$-plane in two half
planes I and II. We select a point (not on the
line), say $(0, 0)$, which lies in one of the half
planes (Fig 6.8) and determine if this point
satisfies the given inequality, we note that

$$3 (0) + 2 (0) > 6$$
or $0 > 6$, which is false.

Fig 6.8

Hence, half plane I is not the solution region of
the given inequality. Clearly, any point on the
line does not satisfy the given strict inequality.
In other words, the shaded half plane II
excluding the points on the line is the solution
region of the inequality.

Example 10 Solve $3x - 6 \ge 0$ graphically in
two dimensional plane.

Solution Graph of $3x - 6 = 0$ is given in the
Fig 6.9.
We select a point, say $(0, 0)$ and substituting it in
given inequality, we see that:
$3(0) - 6 \ge 0$ or $-6 \ge 0$ which is false.
Thus, the solution region is the shaded region on
the right hand side of the line $x = 2$.

Fig 6.9

<!-- page 190 -->
Example 11 Solve $y < 2$ graphically.
Solution Graph of $y = 2$ is given in the Fig 6.10.
Let us select a point, $(0, 0)$ in lower half
plane I and putting $y = 0$ in the given inequality,
we see that
$1 \times 0 < 2$ or $0 < 2$ which is true.
Thus, the solution region is the shaded region
below the line $y = 2$. Hence, every point below
the line (excluding all the points on the line)
determines the solution of the given inequality.

Fig 6.10

EXERCISE 6.2

Solve the following inequalities graphically in two-dimensional plane:

1. $x + y < 5$
2. $2x + y \ge 6$
3. $3x + 4y \le 12$
4. $y + 8 \ge 2x$
5. $x - y \le 2$
6. $2x - 3y > 6$
7. $-3x + 2y \ge -6$
8. $3y - 5x < 30$
9. $y < -2$
10. $x > -3.$

6.5 Solution of System of Linear Inequalities in Two Variables

In previous Section, you have learnt how to solve linear inequality in one or two variables
graphically. We will now illustrate the method for solving a system of linear inequalities
in two variables graphically through some
examples.

Example 12 Solve the following system
of linear inequalities graphically.
$$x + y \ge 5 \quad \dots \quad (1)$$
$$x - y \le 3 \quad \dots \quad (2)$$

Solution The graph of linear equation
$$x + y = 5$$
is drawn in Fig 6.11.
We note that solution of inequality
(1) is represented by the shaded region
above the line $x + y = 5$, including the
points on the line.
On the same set of axes, we draw
the graph of the equation $x - y = 3$ as
shown in Fig 6.11. Then we note that inequ

On the same set of axes, we draw
the graph of the equation $x - y = 3$ as
shown in Fig 6.11. Then we note that inequality (2) represents the shaded region above
Y'
Fig 6.11

<!-- page 191 -->
the line $x - y = 3$, including the points on the line.

Clearly, the double shaded region, common to the above two shaded regions is
the required solution region of the given system of inequalities.

Example 13 Solve the following system
of inequalities graphically

$$5x + 4y \leq 40 \qquad \dots (1)$$
$$x \geq 2 \qquad \dots (2)$$
$$y \geq 3 \qquad \dots (3)$$

Solution We first draw the graph of
the line

$$5x + 4y = 40, \quad x = 2 \text{ and } y = 3$$

Then we note that the inequality (1)
represents shaded region below the line
$5x + 4y = 40$ and inequality (2) represents
the shaded region right of line $x = 2$ but
inequality (3) represents the shaded region
above the line $y = 3$. Hence, shaded region
(Fig 6.12) including all the point on the lines
are also the solution of the given system
of the linear inequalities.

Fig 6.12

In many practical situations involving
system of inequalities the variable $x$ and $y$
often represent quantities that cannot have
negative values, for example, number of
units produced, number of articles
purchased, number of hours worked, etc.
Clearly, in such cases, $x \geq 0$, $y \geq 0$ and the
solution region lies only in the first quadrant.

Example 14 Solve the following system
of inequalities
$$8x + 3y \le 100 \quad \dots \quad (1)$$
$$x \ge 0 \quad \dots \quad (2)$$
$$y \ge 0 \quad \dots \quad (3)$$

Solution We draw the graph of the line
$$8x + 3y = 100$$
The inequality $8x + 3y \le 100$ represents the
shaded region below the line, including the
points on the line $8x + 3y = 100$ (Fig 6.13).

Fig 6.13

<!-- page 192 -->
Since $x \geq 0, y \geq 0$, every point in the
shaded region in the first quadrant,
including the points on the line and
the axes, represents the solution of
the given system of inequalities.

Example 15 Solve the following
system of inequalities graphically

$$x + 2y \le 8 \quad \dots (1)$$
$$2x + y \le 8 \quad \dots (2)$$
$$x \ge 0 \quad \dots (3)$$
$$y \ge 0 \quad \dots (4)$$

Solution We draw the graphs of
the lines $x + 2y = 8$ and $2x + y = 8$.
The inequality (1) and (2) represent
the region below the two lines,
including the point on the respective lines.
Since $x \ge 0, y \ge 0$, every point in the shaded region in the first quadrant represent
a solution of the given system of inequalities (Fig 6.14).

EXERCISE 6.3

Solve the following system of inequalities graphically:

1. $x \geq 3, y \geq 2$
2. $3x + 2y \leq 12, x \geq 1, y \geq 2$
3. $2x + y \geq 6, 3x + 4y \leq 12$
4. $x + y \geq 4, 2x - y < 0$
5. $2x - y > 1, x - 2y < -1$
6. $x + y \leq 6, x + y \geq 4$
7. $2x + y \geq 8, x + 2y \geq 10$
8. $x + y \leq 9, y > x, x \geq 0$
9. $5x + 4y \leq 20, x \geq 1, y \geq 2$
10. $3x + 4y \leq 60, x + 3y \leq 30, x \geq 0, y \geq 0$
11. $2x + y \geq 4, x + y \leq 3, 2x - 3y \leq 6$
12. $x - 2y \leq 3, 3x + 4y \geq 12, x \geq 0, y \geq 1$
13. $4x + 3y \leq 60, y \geq 2x, x \geq 3, x, y \geq 0$
14. $3x + 2y \leq 150, x + 4y \leq 80, x \leq 15, y \geq 0, x \geq 0$
15. $x + 2y \leq 10, x + y \geq 1, x - y \leq 0, x \geq 0, y \geq 0$

<!-- page 193 -->
Miscellaneous Examples

Example 16 Solve $-8 \leq 5x - 3 < 7$.

Solution In this case, we have two inequalities, $-8 \le 5x - 3$ and $5x - 3 < 7$, which we
will solve simultaneously. We have $-8 \le 5x - 3 < 7$
or $-5 \le 5x < 10$ or $-1 \le x < 2$

Example 17 Solve $-5 \leq \frac{5-3x}{2} \leq 8$.


Solution We have $-5 \leq \frac{5-3x}{2} \leq 8$


or $-10 \leq 5-3x \leq 16$ or $-15 \leq -3x \leq 11$


or $5 \geq x \geq -\frac{11}{3}$


which can be written as $-\frac{-11}{3} \leq x \leq 5$

which can be written as $\frac{-11}{3} \leq x \leq 5$

Example 18 Solve the system of inequalities:
$$3x - 7 < 5 + x \quad \dots (1)$$
$$11 - 5 \ x \le 1 \quad \dots (2)$$
and represent the solutions on the number line.

Solution From inequality (1), we have
$$3x - 7 < 5 + x$$
or $$x < 6$$
... (3)
Also, from inequality (2), we have
$$11 - 5 \ x \le 1$$
or $-5 \ x \le -10 \quad \text{i.e., } x \ge 2 \quad \dots (4)$$If we draw the graph of inequalities (3) and (4) on the number line, we see that the \\ values of $x$, which are common to both, are shown by bold line in Fig 6.15. \\ Fig 6.15 \\ Thus, solution of the system are real numbers $x$ lying between 2 and 6 including 2, i.e.,$$2 \le x < 6$$

<!-- page 194 -->
Example 19 In an experiment, a solution of hydrochloric acid is to be kept between
$30^{\circ}$ and $35^{\circ}$ Celsius. What is the range of temperature in degree Fahrenheit if conversion

formula is given by $\text{C} = \frac{5}{9}$ (F – 32), where C and F represent temperature in degree

Celsius and degree Fahrenheit, respectively.

Solution It is given that $30 < \text{C} < 35$.

Putting $\text{C} = \frac{5}{9}$ (F – 32), we get

$$30 < \frac{5}{9} (\text{F} – 32) < 35,$$

or $$\frac{9}{5} \times (30) < (\text{F} – 32) < \frac{9}{5} \times (35)$$

or $$54 < (\text{F} – 32) < 63$$

or $$86 < \text{F} < 95.$$

Thus, the required range of temperature is between $86^{\circ}$ F and $95^{\circ}$ F.

Thus, the required range of temperature is between $86^{\circ}$ F and $95^{\circ}$ F.

Example 20 A manufacturer has 600 litres of a 12% solution of acid. How many litres
of a 30% acid solution must be added to it so that acid content in the resulting mixture
will be more than 15% but less than 18%?

Solution Let $x$ litres of 30% acid solution is required to be added. Then
Total mixture = $(x + 600)$ litres
Therefore $30\% x + 12\%$ of $600 > 15\%$ of $(x + 600)$
and $30\% x + 12\%$ of $600 < 18\%$ of $(x + 600)$

or $$\frac{30x}{100} + \frac{12}{100} (600) > \frac{15}{100} (x + 600)$$

and $$\frac{30x}{100} + \frac{12}{100} (600) < \frac{18}{100} (x + 600)$$

or $30x + 7200 > 15x + 9000$
and $30x + 7200 < 18x + 10800$
or $15x > 1800$ and $12x < 3600$
or $x > 120$ and $x < 300$,
i.e. $120 < x < 300$

<!-- page 195 -->
Thus, the number of litres of the $30\%$ solution of acid will have to be more than
$120$ litres but less than $300$ litres.

Miscellaneous Exercise on Chapter 6

Solve the inequalities in Exercises 1 to 6.

1. $2 \le 3x - 4 \le 5$
2. $6 \le -3 (2x - 4) < 12$
3. $-3 \le 4 - \frac{7x}{2} \le 18$
4. $-15 < \frac{3(x - 2)}{5} \le 0$
5. $-12 < 4 - \frac{3x}{-5} \le 2$
6. $7 \le \frac{(3x + 11)}{2} \le 11.$

Solve the inequalities in Exercises 7 to 10 and represent the solution graphically on
number line.

7. $5x + 1 > -24, \quad 5x - 1 < 24$
8. $2(x - 1) < x + 5, \quad 3(x + 2) > 2 - x$
9. $3x - 7 > 2(x - 6), \quad 6 - x > 11 - 2x$
10. $5(2x - 7) - 3(2x + 3) \le 0, \quad 2x + 19 \le 6x + 47.$

11. A solution is to be kept between $68^\circ$ F and $77^\circ$ F. What is the range in temperature
in degree Celsius (C) if the Celsius / Fahrenheit (F) conversion formula is given by

$$F = \frac{9}{5} C + 32 ?$$

12. A solution of 8% boric acid is to be diluted by adding a 2% boric acid solution to
it. The resulting mixture is to be more than 4% but less than 6% boric acid. If we have
640 litres of the 8% solution, how many litres of the 2% solution will have to be added?

13. How many litres of water will have to be added to 1125 litres of the 45% solution
of acid so that the resulting mixture will contain more than 25% but less than 30% acid
content?

14. IQ of a person is given by the formula

$$\text{IQ} = \frac{\text{MA}}{\text{CA}} \times 100,$$

where MA is mental age and CA is chronological age. If $80 \le IQ \le 140$ for a group of
12 years old children, find the range of their mental age.

<!-- page 196 -->
Summary

◆ Two real numbers or two algebraic expressions related by the symbols $<, >, \le$
or $\ge$ form an inequality.
◆ Equal numbers may be added to (or subtracted from ) both sides of an inequality.
◆ Both sides of an inequality can be multiplied (or divided ) by the same positive
number. But when both sides are multiplied (or divided) by a negative number,
then the inequality is reversed.
◆ The values of $x$, which make an inequality a true statement, are called *solutions*
*of the inequality*.
◆ To represent $x < a$ (or $x > a$) on a number line, put a circle on the number $a$ and
dark line to the left (or right) of the number $a$.
◆ To represent $x \le a$ (or $x \ge a$) on a number line, put a dark circle on the number
$a$ and dark the line to the left (or right) of the number $x$.
◆ If an inequality is having $\le$ or $\ge$ symbol, then the points on the line are also
included in the solutions of the inequality and the graph of the inequality lies left
(below) or right (above) of the graph of the equality represented by dark line
that satisfies an arbitrary point in that part.
◆ If an inequality is having $<$ or $>$ symbol, then the points on the line are not
included in the solutions of the inequality and the graph of the inequality lies to
the left (below) or right (above) of the graph of the corresponding equality
represented by dotted line that satisfies an arbitrary point in that part.
◆ The solution region of a system of inequalities is the region which satisfies all
the given inequalities in the system simultaneously.

<!-- page 197 -->
PERMUTATIONS AND COMBINATIONS

❖ Every body of discovery is mathematical in form because there is no
other guidance we can have – DARWIN

7.1 Introduction

Suppose you have a suitcase with a number lock. The number
lock has 4 wheels each labelled with 10 digits from 0 to 9.
The lock can be opened if 4 specific digits are arranged in a
particular sequence with no repetition. Some how, you have
forgotten this specific sequence of digits. You remember only
the first digit which is 7. In order to open the lock, how
many sequences of 3-digits you may have to check with? To
answer this question, you may, immediately, start listing all
possible arrangements of 9 remaining digits taken 3 at a
time. But, this method will be tedious, because the number
of possible sequences may be large. Here, in this Chapter,
we shall learn some basic counting techniques which will enable us to answer this
question without actually listing 3-digit arrangements. In fact, these techniques will be
useful in determining the number of different ways of arranging and selecting objects
without actually listing them. As a first step, we shall examine a principle which is most
fundamental to the learning of these techniques.

Jacob Bernoulli
(1654-1705)

7.2 Fundamental Principle of Counting

Let us consider the following problem. Mohan has 3 pants and 2 shirts. How many
different pairs of a pant and a shirt, can he dress up with? There are 3 ways in which
a pant can be chosen, because there are 3 pants available. Similarly, a shirt can be
chosen in 2 ways. For every choice of a pant, there are 2 choices of a shirt. Therefore,
there are $3 \times 2 = 6$ pairs of a pant and a shirt.

<!-- page 198 -->
Let us name the three pants as $P_1$, $P_2$, $P_3$ and the two shirts as $S_1$, $S_2$. Then,
these six possibilities can be illustrated in the Fig. 7.1.

Let us consider another problem
of the same type.
Sabnam has 2 school bags, 3 tiffin boxes
and 2 water bottles. In how many ways
can she carry these items (choosing one
each).

A school bag can be chosen in 2
different ways. After a school bag is
chosen, a tiffin box can be chosen in 3
different ways. Hence, there are
$2 \times 3 = 6$ pairs of school bag and a tiffin
box. For each of these pairs a water
bottle can be chosen in 2 different ways.
Hence, there are $6 \times 2 = 12$ different ways in which, Sabnam can carry these items to
school. If we name the 2 school bags as $\text{B}_1$, $\text{B}_2$, the three tiffin boxes as $\text{T}_1$, $\text{T}_2$, $\text{T}_3$ and
the two water bottles as $\text{W}_1$, $\text{W}_2$, these possibilities can be illustrated in the Fig. 7.2.

Fig 7.2

<!-- page 199 -->
In fact, the problems of the above types are solved by applying the following
principle known as the *fundamental principle of counting*, or, simply, the *multiplication*
*principle*, which states that

“If an event can occur in $m$ different ways, following which another event
can occur in $n$ different ways, then the total number of occurrence of the events
in the given order is $m \times n$.”

The above principle can be generalised for any finite number of events. For
example, for 3 events, the principle is as follows:

'If an event can occur in $m$ different ways, following which another event can
occur in $n$ different ways, following which a third event can occur in $p$ different ways,
then the total number of occurrence to 'the events in the given order is $m \times n \times p$.'

In the first problem, the required number of ways of wearing a pant and a shirt
was the number of different ways of the occurence of the following events in succession:

(i) the event of choosing a pant
(ii) the event of choosing a shirt.

In the second problem, the required number of ways was the number of different
ways of the occurence of the following events in succession:

(i) the event of choosing a school bag
(ii) the event of choosing a tiffin box
(iii) the event of choosing a water bottle.

Here, in both the cases, the events in each problem could occur in various possible
orders. But, we have to choose any one of the possible orders and count the number of
different ways of the occurence of the events in this chosen order.

Example 1 Find the number of 4 letter words, with or without meaning, which can be
formed out of the letters of the word ROSE, where the repetition of the letters is not
allowed.

Solution There are as many words as there are ways of filling in 4 vacant places
$\square$ $\square$ $\square$ $\square$ by the 4 letters, keeping in mind that the repetition is not allowed. The
first place can be filled in 4 different ways by anyone of the 4 letters R,O,S,E. Following
which, the second place can be filled in by anyone of the remaining 3 letters in 3
different ways, following which the third place can be filled in 2 different ways; following
which, the fourth place can be filled in 1 way. Thus, the number of ways in which the
4 places can be filled, by the multiplication principle, is $4 \times 3 \times 2 \times 1 = 24$. Hence, the
required number of words is 24.

<!-- page 200 -->
**Note** If the repetition of the letters was allowed, how many words can be formed?
One can easily understand that each of the 4 vacant places can be filled in succession
in 4 different ways. Hence, the required number of words $= 4 \times 4 \times 4 \times 4 = 256$.

Example 2 Given 4 flags of different colours, how many different signals can be
generated, if a signal requires the use of 2 flags one below the other?

Solution There will be as many signals as there are ways of filling in 2 vacant places
$\boxed{\phantom{\text{}}} \text{ in succession by the 4 flags of different colours. The upper vacant place can}$
$\text{be filled in 4 different ways by anyone of the 4 flags; following which, the lower vacant}$
$\text{place can be filled in 3 different ways by anyone of the remaining 3 different flags.}$
Hence, by the multiplication principle, the required number of signals $= 4 \times 3 = 12.$

Example 3 How many 2 digit even numbers can be formed from the digits
1, 2, 3, 4, 5 if the digits can be repeated?

Solution There will be as many ways as there are ways of filling 2 vacant places
$\square \square$ in succession by the five given digits. Here, in this case, we start filling in unit's
place, because the options for this place are 2 and 4 only and this can be done in 2
ways; following which the ten's place can be filled by any of the 5 digits in 5 different
ways as the digits can be repeated. Therefore, by the multiplication principle, the required
number of two digits even numbers is $2 \times 5$, i.e., 10.

Example 4 Find the number of different signals that can be generated by arranging at
least 2 flags in order (one below the other) on a vertical staff, if five different flags are
available.

Solution A signal can consist of either 2 flags, 3 flags, 4 flags or 5 flags. Now, let us
count the possible number of signals consisting of 2 flags, 3 flags, 4 flags and 5 flags
separately and then add the respective numbers.
There will be as many 2 flag signals as there are ways of filling in 2 vacant places
in succession by the 5 flags available. By Multiplication rule, the number of
ways is $5 \times 4 = 20$.
Similarly, there will be as many 3 flag signals as there are ways of filling in 3
vacant places in succession by the 5 flags.

<!-- page 201 -->
The number of ways is $5 \times 4 \times 3 = 60$.
Continuing the same way, we find that

The number of 4 flag signals $= 5 \times 4 \times 3 \times 2 = 120$
and the number of 5 flag signals $= 5 \times 4 \times 3 \times 2 \times 1 = 120$
Therefore, the required no of signals $= 20 + 60 + 120 + 120 = 320.$

EXERCISE 7.1

1. How many 3-digit numbers can be formed from the digits 1, 2, 3, 4 and 5
assuming that
(i) repetition of the digits is allowed?
(ii) repetition of the digits is not allowed?
2. How many 3-digit even numbers can be formed from the digits 1, 2, 3, 4, 5, 6 if the
digits can be repeated?
3. How many 4-letter code can be formed using the first 10 letters of the English
alphabet, if no letter can be repeated?
4. How many 5-digit telephone numbers can be constructed using the digits 0 to 9 if
each number starts with 67 and no digit appears more than once?
5. A coin is tossed 3 times and the outcomes are recorded. How many possible
outcomes are there?
6. Given 5 flags of different colours, how many different signals can be generated if
each signal requires the use of 2 flags, one below the other?

7.3 Permutations

In Example 1 of the previous Section, we are actually counting the different possible
arrangements of the letters such as ROSE, REOS, ..., etc. Here, in this list, each
arrangement is different from other. In other words, the order of writing the letters is
important. Each arrangement is called a permutation of 4 different letters taken all
at a time. Now, if we have to determine the number of 3-letter words, with or without
meaning, which can be formed out of the letters of the word NUMBER, where the
repetition of the letters is not allowed, we need to count the arrangements NUM,
NMU, MUN, NUB, ..., etc. Here, we are counting the permutations of 6 different
letters taken 3 at a time. The required number of words $= 6 \times 5 \times 4 = 120$ (by using
multiplication principle).

If the repetition of the letters was allowed, the required number of words would
be $6 \times 6 \times 6 = 216$.

<!-- page 202 -->
Definition 1 A permutation is an arrangement in a definite order of a number of
objects taken some or all at a time.
In the following sub-section, we shall obtain the formula needed to answer these
questions immediately.

7.3.1 Permutations when all the objects are distinct

Theorem 1 The number of permutations of $n$ different objects taken $r$ at a time,
where $0 < r \le n$ and the objects do not repeat is $n ( n - 1) ( n - 2) . . . ( n - r + 1)$,
which is denoted by ${}^n\mathrm{P}_r$.

Proof There will be as many permutations as there are ways of filling in $r$ vacant

places $\square$ $\square$ $\square$ ... $\square$ by

$$\leftarrow r \text{ vacant places } \rightarrow$$

the $n$ objects. The first place can be filled in $n$ ways; following which, the second place
can be filled in $(n-1)$ ways, following which the third place can be filled in $(n-2)$
ways,..., the $r$th place can be filled in $(n-(r-1))$ ways. Therefore, the number of
ways of filling in $r$ vacant places in succession is $n(n-1)(n-2)\dots(n-(r-1))$ or
$n(n-1)(n-2)\dots(n-r+1)$

This expression for $^nP_r$ is cumbersome and we need a notation which will help to
reduce the size of this expression. The symbol $n!$ (read as factorial $n$ or $n$ factorial )
comes to our rescue. In the following text we will learn what actually $n!$ means.

7.3.2 *Factorial notation* The notation $n!$ represents the product of first $n$ natural
numbers, i.e., the product $1 \times 2 \times 3 \times \dots \times (n-1) \times n$ is denoted as $n!$. We read this
symbol as ‘$n$ factorial’. Thus, $1 \times 2 \times 3 \times 4 \dots \times (n-1) \times n = n$

$1 = 1 !$
$1 \times 2 = 2 !$
$1 \times 2 \times 3 = 3 !$
$1 \times 2 \times 3 \times 4 = 4 !$ and so on.

We define $0 ! = 1$

We can write $5 ! = 5 \times 4 ! = 5 \times 4 \times 3 ! = 5 \times 4 \times 3 \times 2 !$
$= 5 \times 4 \times 3 \times 2 \times 1 !$

Clearly, for a natural number $n$

$$\begin{aligned} \\ n ! &= n (n - 1) ! \\ \\ &= n (n - 1) (n - 2) ! && \text{[provided } (n \geq 2) \text{]} \\ \\ &= n (n - 1) (n - 2) (n - 3) ! && \text{[provided } (n \geq 3) \text{]} \\ \end{aligned}$$

and so on.

<!-- page 203 -->
Example 5 Evaluate (i) 5 !      (ii) 7 !            (iii) 7 ! $- 5$ !

Solution      (i) 5 ! $= 1 \times 2 \times 3 \times 4 \times 5 = 120$
               (ii) 7 ! $= 1 \times 2 \times 3 \times 4 \times 5 \times 6 \times 7 = 5040$
and           (iii) 7 ! $- 5 ! = 5040 - 120 = 4920.$

Example 6 Compute (i) $\frac{7!}{5!}$ (ii) $\frac{12!}{(10!)(2!)}$


Solution (i) We have $\frac{7!}{5!} = \frac{7 \times 6 \times 5!}{5!} = 7 \times 6 = 42$


and (ii) $\frac{12!}{(10!)(2!)} = \frac{12 \times 11 \times (10!)}{(10!) \times (2)} = 6 \times 11 = 66.$

Example 7 Evaluate $\frac{n!}{r!(n-r)!}$, when $n=5$, $r=2$.

Solution We have to evaluate $\frac{5!}{2!(5-2)!}$ (since $n=5, r=2$)


We have $\frac{5!}{2!(5-2)!} = \frac{5!}{2! \times 3!} = \frac{5 \times 4}{2} = 10$.

Example 8 If $\frac{1}{8!} + \frac{1}{9!} = \frac{x}{10!}$, find $x$.


Solution We have $\frac{1}{8!} + \frac{1}{9 \times 8!} = \frac{x}{10 \times 9 \times 8!}$


Therefore $1 + \frac{1}{9} = \frac{x}{10 \times 9}$ or $\frac{10}{9} = \frac{x}{10 \times 9}$


So $x = 100$.

EXERCISE 7.2

1. Evaluate
(i) 8 !                                     (ii) 4 ! – 3 !

<!-- page 204 -->
2. Is $3! + 4! = 7!?$          3. Compute $\frac{8!}{6! \times 2!}$          4. If $\frac{1}{6!} + \frac{1}{7!} = \frac{x}{8!}$, find $x$

5. Evaluate $\frac{n!}{(n-r)!}$, when

(i) $n=6, r=2$ (ii) $n=9, r=5$.

7.3.3 Derivation of the formula for "$\text{P}_{\text{r}}$

$${}^nP_r = \frac{n!}{(n-r)!}, 0 \le r \le n$$

Let us now go back to the stage where we had determined the following formula:

$$^nP_r = n (n - 1) (n - 2) \dots (n - r + 1)$$

Multiplying numerator and denominator by $(n-r) (n-r-1) \dots 3 \times 2 \times 1$, we get

$$^n\mathrm{P}_r = \frac{n(n-1)(n-2)...(n-r+1)(n-r)(n-r-1)...3\times2\times1}{(n-r)(n-r-1)...3\times2\times1} = \frac{n!}{(n-r)!},$$

Thus $$\ ^n\mathrm{P}_r = \frac{n!}{(n-r)!}, \text{ where } 0 < r \le n$$

This is a much more convenient expression for ${}^n\mathrm{P}_r$ than the previous one.

In particular, when $r = n$, ${}^n\mathrm{P}_n = \frac{n!}{0!} = n!$

Counting permutations is merely counting the number of ways in which some or
all objects at a time are rearranged. Arranging no object at all is the same as leaving
behind all the objects and we know that there is only one way of doing so. Thus, we
can have

$$^n\mathrm{P}_0 = 1 = \frac{n!}{n!} = \frac{n!}{(n-0)!} \qquad \dots (1)$$

Therefore, the formula (1) is applicable for $r = 0$ also.

Thus $$\ ^n\mathrm{P}_r = \frac{n!}{(n-r)!}, 0 \le r \le n.$$

<!-- page 205 -->
Theorem 2 The number of permutations of $n$ different objects taken $r$ at a time,
where repetition is allowed, is $n^r$.

Proof is very similar to that of Theorem 1 and is left for the reader to arrive at.

Here, we are solving some of the problems of the pervious Section using the
formula for ${}^nP_r$ to illustrate its usefulness.

In Example 1, the required number of words = ${}^4\text{P}_4 = 4! = 24$. Here repetition is
not allowed. If repetition is allowed, the required number of words would be $4^4 = 256$.

The number of 3-letter words which can be formed by the letters of the word

NUMBER = ${}^6\text{P}_3 = \frac{6!}{3!} = 4 \times 5 \times 6 = 120$. Here, in this case also, the repetition is not

allowed. If the repetition is allowed,the required number of words would be $6^3 = 216$.

The number of ways in which a Chairman and a Vice-Chairman can be chosen
from amongst a group of 12 persons assuming that one person can not hold more than

one position, clearly ${}^{12}\mathrm{P}_{2} = \frac{12!}{10!} = 11 \times 12 = 132.$

7.3.4 *Permutations when all the objects are not distinct objects* Suppose we have

7.3.4 *Permutations when all the objects are not distinct objects* Suppose we have
to find the number of ways of rearranging the letters of the word ROOT. In this case,
the letters of the word are not all different. There are 2 Os, which are of the same kind.
Let us treat, temporarily, the 2 Os as different, say, $\text{O}_1$ and $\text{O}_2$. The number of
permutations of 4-different letters, in this case, taken all at a time
is 4!. Consider one of these permutations say, $\text{RO}_1\text{O}_2\text{T}$. Corresponding to this
permutation,we have 2 ! permutations $\text{RO}_1\text{O}_2\text{T}$ and $\text{RO}_2\text{O}_1\text{T}$ which will be exactly the
same permutation if $\text{O}_1$ and $\text{O}_2$ are not treated as different, i.e., if $\text{O}_1$ and $\text{O}_2$ are the
same O at both places.

Therefore, the required number of permutations = $\frac{4!}{2!} = 3 \times 4 = 12$.

Permutations when $O_1$, $O_2$ are
different.
$\begin{matrix} \text{RO}_1\text{O}_2\text{T} \\ \text{RO}_2\text{O}_1\text{T} \end{matrix} \xrightarrow{\text{R O O T}}$
$\begin{matrix} \text{TO}_1\text{O}_2\text{R} \\ \text{TO}_2\text{O}_1\text{R} \end{matrix} \xrightarrow{\text{T O O R}}$

<!-- page 206 -->
$$\left. \begin{matrix} \text{RO}_1\text{T} \text{O}_2 \\ \text{RO}_2\text{T} \text{O}_1 \end{matrix} \right] \xrightarrow{\hspace{3cm}} \text{R O T O}$$

$$\left. \begin{matrix} \text{T O}_1\text{R O}_2 \\ \text{T O}_2\text{R O}_1 \end{matrix} \right] \xrightarrow{\hspace{3cm}} \text{T O R O}$$

$$\begin{bmatrix} \text{RTO}_1\text{O}_2 \\ \text{RTO}_2\text{O}_1 \end{bmatrix} \xrightarrow{\hspace{3cm}} \text{RTOO}$$

$$\left. \begin{matrix} \text{T R O}_1 \text{ O}_2 \\ \text{T R O}_2 \text{ O}_1 \end{matrix} \right] \xrightarrow{\hspace{3cm}} \text{T R O O}$$

$$\begin{bmatrix} \\ O_1 & O_2 & R & T \\ \\ O_2 & O_1 & T & R \\ \end{bmatrix} \\ \xrightarrow{\hspace{3cm}} O O R T$$

$$\left. \begin{matrix} O_1 R O_2 T \\ O_2 R O_1 T \end{matrix} \right] \xrightarrow{\hspace{3cm}} O R O T$$

$$\begin{bmatrix} O_1 & T & O_2 & R \\ O_2 & T & O_1 & R \end{bmatrix} \xrightarrow{\hspace{3cm}} O T O R$$

$$\begin{bmatrix} O_1 & R & T & O_2 \\ O_2 & R & T & O_1 \end{bmatrix} \xrightarrow{\hspace{3cm}} O R T O$$

$$\begin{bmatrix} \\ O_1 T R O_2 \\ \\ O_2 T R O_1 \\ \end{bmatrix} \longrightarrow O T R O$$

$$\left. \begin{matrix} O_1 & O_2 T R \\ O_2 & O_1 T R \end{matrix} \right] \xrightarrow{\hspace{3cm}} O O T R$$

Let us now find the number of ways of rearranging the letters of the word
INSTITUTE. In this case there are 9 letters, in which I appears 2 times and T appears
3 times.

Temporarily, let us treat these letters different and name them as $I_1, I_2, T_1, T_2, T_3$.
The number of permutations of 9 different letters, in this case, taken all at a time is 9 !.
Consider one such permutation, say, $I_1 NT_1 SI_2 T_2 U E T_3$. Here if $I_1, I_2$ are not same

<!-- page 207 -->
and $T_1$, $T_2$, $T_3$ are not same, then $I_1$, $I_2$ can be arranged in $2!$ ways and $T_1$, $T_2$, $T_3$ can
be arranged in $3!$ ways. Therefore, $2! \times 3!$ permutations will be just the same permutation
corresponding to this chosen permutation $I_1NT_1SI_2T_2UET_3$. Hence, total number of

different permutations will be $\frac{9!}{2! 3!}$

We can state (without proof) the following theorems:

Theorem 3 The number of permutations of $n$ objects, where $p$ objects are of the


same kind and rest are all different $= \frac{n!}{p!}$.

In fact, we have a more general theorem.

Theorem 4 The number of permutations of $n$ objects, where $p_1$ objects are of one
kind, $p_2$ are of second kind, ..., $p_k$ are of $k^{\text{th}}$ kind and the rest, if any, are of different

kind is $\frac{n!}{p_1! \ p_2! \ ... \ p_k!}$.

Example 9 Find the number of permutations of the letters of the word ALLAHABAD.

Solution Here, there are 9 objects (letters) of which there are 4A's, 2 L's and rest are
all different.

Therefore, the required number of arrangements = $\frac{9!}{4!2!} = \frac{5 \times 6 \times 7 \times 8 \times 9}{2} = 7560$

Example 10 How many 4-digit numbers can be formed by using the digits 1 to 9 if
repetition of digits is not allowed?

Solution Here order matters for example 1234 and 1324 are two different numbers.
Therefore, there will be as many 4 digit numbers as there are permutations of 9 different
digits taken 4 at a time.

Therefore, the required 4 digit numbers $= {}^9\text{P}_4 = \frac{9!}{(9-4)!} = \frac{9!}{5!} = 9 \times 8 \times 7 \times 6 = 3024.$

Example 11 How many numbers lying between 100 and 1000 can be formed with the
digits 0, 1, 2, 3, 4, 5, if the repetition of the digits is not allowed?

Solution Every number between 100 and 1000 is a 3-digit number. We, first, have to

<!-- page 208 -->
count the permutations of 6 digits taken 3 at a time. This number would be ${}^6\text{P}_3$. But,
these permutations will include those also where 0 is at the 100's place. For example,
092, 042, . . ., etc are such numbers which are actually 2-digit numbers and hence the
number of such numbers has to be subtracted from ${}^6\text{P}_3$ to get the required number. To
get the number of such numbers, we fix 0 at the 100's place and rearrange the remaining
5 digits taking 2 at a time. This number is ${}^5\text{P}_2$. So

The required number $= ^6\text{P}_3 - ^5\text{P}_2 = \frac{6!}{3!} - \frac{5!}{3!}$
$= 4 \times 5 \times 6 - 4 \times 5 = 100$

Example 12 Find the value of $n$ such that

(i) $^n\mathrm{P}_5 = 42 \ ^n\mathrm{P}_3, \ n > 4$ (ii) $\frac{{}^nP_4}{{}^{n-1}\mathrm{P}_4} = \frac{5}{3}, \ n > 4$

Solution (i) Given that
$$^n\text{P}_5 = 42 \ ^n\text{P}_3$$
or $n(n-1)(n-2)(n-3)(n-4) = 42 \ n(n-1)(n-2)$
Since $n > 4$ so $n(n-1)(n-2) \neq 0$
Therefore, by dividing both sides by $n(n-1)(n-2)$, we get
$$(n-3)(n-4) = 42$$
or $n^2 - 7n - 30 = 0$
or $n^2 - 10n + 3n - 30$
or $(n-10)(n+3) = 0$
or $n - 10 = 0$ or $n + 3 = 0$
or $n = 10$ or $n = -3$
As $n$ cannot be negative, so $n = 10$.

(ii) Given that $\frac{^n\text{P}_4}{n-1\text{P}_4} = \frac{5}{3}$

Therefore $3n(n-1)(n-2)(n-3) = 5(n-1)(n-2)(n-3)(n-4)$
or $3n = 5(n-4)$ [as $(n-1)(n-2)(n-3) \neq 0, n > 4$]
or $n = 10$.

<!-- page 209 -->
Example 13 Find $r$, if $5 \ ^4\text{P}_r = 6 \ ^5\text{P}_{r-1}$ .

Solution We have $5 \ ^4\text{P}_r = 6 \ ^5\text{P}_{r-1}$

or $$5 \times \frac{4!}{(4-r)!} = 6 \times \frac{5!}{(5-r+1)!}$$

or $$\frac{5!}{(4-r)!} = \frac{6 \times 5!}{(5-r+1)(5-r)(5-r-1)!}$$

or $(6 - r)(5 - r) = 6$

or $$r^2 - 11r + 24 = 0$$

or $$r^2 - 8r - 3r + 24 = 0$$

or $$(r - 8)(r - 3) = 0$$

or $$r = 8 \quad \text{or} \quad r = 3.$$

Hence $$r = 8, 3.$$

Example 14 Find the number of different 8-letter arrangements that can be made
from the letters of the word DAUGHTER so that
(i) all vowels occur together (ii) all vowels do not occur together.

Solution (i) There are 8 different letters in the word DAUGHTER, in which there
are 3 vowels, namely, A, U and E. Since the vowels have to occur together, we can for
the time being, assume them as a single object (AUE). This single object together with
5 remaining letters (objects) will be counted as 6 objects. Then we count permutations
of these 6 objects taken all at a time. This number would be ${}^6\text{P}_6 = 6!$. Corresponding to
each of these permutations, we shall have 3! permutations of the three vowels A, U, E
taken all at a time . Hence, by the multiplication principle the required number of
permutations $= 6 ! \times 3 ! = 4320$.
(ii) If we have to count those permutations in which all vowels are never
together, we first have to find all possible arrangements of 8 letters taken all at a time,
which can be done in 8! ways. Then, we have to subtract from this number, the number
of permutations in which the vowels are always together.

Therefore, the required number $8 ! - 6 ! \times 3 ! = 6 ! (7 \times 8 - 6)$
$= 2 \times 6 ! (28 - 3)$
$= 50 \times 6 ! = 50 \times 720 = 36000$

Example 15 In how many ways can 4 red, 3 yellow and 2 green discs be arranged in
a row if the discs of the same colour are indistinguishable ?

Solution Total number of discs are $4 + 3 + 2 = 9$. Out of 9 discs, 4 are of the first kind

<!-- page 210 -->
(red), 3 are of the second kind (yellow) and 2 are of the third kind (green).

Therefore, the number of arrangements $\frac{9!}{4! 3! 2!} = 1260$.

Example 16 Find the number of arrangements of the letters of the word
INDEPENDENCE. In how many of these arrangements,
(i) do the words start with P
(ii) do all the vowels always occur together
(iii) do the vowels never occur together
(iv) do the words begin with I and end in P?

Solution There are 12 letters, of which N appears 3 times, E appears 4 times and D
appears 2 times and the rest are all different. Therefore

The required number of arrangements $= \frac{12!}{3! \ 4! \ 2!} = 1663200$

(i) Let us fix P at the extreme left position, we, then, count the arrangements of the
remaining 11 letters. Therefore, the required number of words starting with P
$$= \frac{11!}{3! 2! 4!} = 138600$$

(ii) There are 5 vowels in the given word, which are 4 Es and 1 I. Since, they have
to always occur together, we treat them as a single object $\boxed{\text{EEEI}}$ for the time
being. This single object together with 7 remaining objects will account for 8
objects. These 8 objects, in which there are 3Ns and 2 Ds, can be rearranged in

$\frac{8!}{3! \ 2!}$ ways. Corresponding to each of these arrangements, the 5 vowels E, E, E,

E and I can be rearranged in $\frac{5!}{4!}$ ways. Therefore, by multiplication principle,
the required number of arrangements

the required number of arrangements

$$= \frac{8!}{3! \, 2!} \times \frac{5!}{4!} = 16800$$

(iii) The required number of arrangements
= the total number of arrangements (without any restriction) – the number
of arrangements where all the vowels occur together.

<!-- page 211 -->
$$= 1663200 - 16800 = 1646400$$

(iv) Let us fix I and P at the extreme ends (I at the left end and P at the right end).
We are left with 10 letters.

Hence, the required number of arrangements

$$= \frac{10!}{3! 2! 4!} = 12600$$

EXERCISE 7.3

1. How many 3-digit numbers can be formed by using the digits 1 to 9 if no digit is
repeated?
2. How many 4-digit numbers are there with no digit repeated?
3. How many 3-digit even numbers can be made using the digits
1, 2, 3, 4, 6, 7, if no digit is repeated?
4. Find the number of 4-digit numbers that can be formed using the digits 1, 2, 3, 4,
5 if no digit is repeated. How many of these will be even?
5. From a committee of 8 persons, in how many ways can we choose a chairman
and a vice chairman assuming one person can not hold more than one position?
6. Find $n$ if ${}^{n-1}\mathrm{P}_3 : {}^{n}\mathrm{P}_4 = 1 : 9$.
7. Find $r$ if (i) ${}^5\mathrm{P}_r = 2{}^6\mathrm{P}_{r-1}$ (ii) ${}^5\mathrm{P}_r = {}^6\mathrm{P}_{r-1}$ .
8. How many words, with or without meaning, can be formed using all the letters of
the word EQUATION, using each letter exactly once?
9. How many words, with or without meaning can be made from the letters of the
word MONDAY, assuming that no letter is repeated, if.
(i) 4 letters are used at a time, (ii) all letters are used at a time,
(iii) all letters are used but first letter is a vowel?
10. In how many of the distinct permutations of the letters in MISSISSIPPI do the
four I's not come together?
11. In how many ways can the letters of the word PERMUTATIONS be arranged if the
(i) words start with P and end with S, (ii) vowels are all together,
(iii) there are always 4 letters between P and S?

7.4 Combinations

Let us now assume that there is a group of 3 lawn tennis players X, Y, Z. A team
consisting of 2 players is to be formed. In how many ways can we do so? Is the team
of X and Y different from the team of Y and X ? Here, order is not important.
In fact, there are only 3 possible ways in which the team could be constructed.

<!-- page 212 -->
Fig. 7.3

These are XY, YZ and ZX (Fig 7.3).

Here, each selection is called a combination of 3 different objects taken 2 at a time.
In a combination, the order is not important.

Now consider some more illustrations.

Twelve persons meet in a room and each shakes hand with all the others. How do
we determine the number of hand shakes. X shaking hands with Y and Y with X will
not be two different hand shakes. Here, order is not important. There will be as many
hand shakes as there are combinations of 12 different things taken 2 at a time.

Seven points lie on a circle. How many chords can be drawn by joining these
points pairwise? There will be as many chords as there are combinations of 7 different
things taken 2 at a time.

Now, we obtain the formula for finding the number of combinations of $n$ different
objects taken $r$ at a time, denoted by ${}^n\text{C}_r..$

Suppose we have 4 different objects A, B, C and D. Taking 2 at a time, if we have
to make combinations, these will be AB, AC, AD, BC, BD, CD. Here, AB and BA are
the same combination as order does not alter the combination. This is why we have not
included BA, CA, DA, CB, DB and DC in this list. There are as many as 6 combinations
of 4 different objects taken 2 at a time, i.e., $^4\text{C}_2 = 6$.

Corresponding to each combination in the list, we can arrive at $2!$ permutations as
2 objects in each combination can be rearranged in $2!$ ways. Hence, the number of
permutations $= ^4\text{C}_2 \times 2!$.

On the other hand, the number of permutations of 4 different things taken 2 at
a time $= ^4\text{P}_2$.

Therefore $^4\mathbf{P}_2 = ^4\mathbf{C}_2 \times 2!$ or $\frac{4!}{(4-2)!2!} = ^4\text{C}_2$

Now, let us suppose that we have 5 different objects A, B, C, D, E. Taking 3 at a
time, if we have to make combinations, these will be ABC, ABD, ABE, BCD, BCE,
CDE, ACE, ACD, ADE, BDE. Corresponding to each of these $^5\text{C}_3$ combinations, there
are 3! permutations, because, the three objects in each combination can be

<!-- page 213 -->
rearranged in 3 ! ways. Therefore, the total of permutations = $^5\text{C}_3 \times 3!$

Therefore $^5\mathbf{P}_3 = ^5\mathbf{C}_3 \times \mathbf{3}!$ or $\frac{5!}{(5-3)! \ 3!} = ^5\mathbf{C}_3$

These examples suggest the following theorem showing relationship between
permutaion and combination:

Theorem 5 $^n\mathrm{P}_r = ^n\mathrm{C}_r \ r!, 0 < r \le n.$

Proof Corresponding to each combination of ${}^n\text{C}_r$, we have $r$ ! permutations, because
$r$ objects in every combination can be rearranged in $r$ ! ways.
Hence, the total number of permutations of $n$ different things taken $r$ at a time

is ${}^n\text{C}_r \times r!$. On the other hand, it is ${}^n\text{P}_r$ . Thus

$${}^n\mathrm{P}_r = {}^n\mathrm{C}_r \times r!, \ 0 < r \le n.$$

Remarks 1. From above $$\frac{n!}{(n-r)!} = {}^{n}\mathrm{C}_{r} \times r!$, i.e., ${}^{n}\mathrm{C}_{r} = \frac{n!}{r!(n-r)!}$$

In particular, if $r = n$, ${}^{n}\mathrm{C}_{n} = \frac{n!}{n! \ 0!} = 1$.

2. We define $^n\text{C}_0 = 1$, i.e., the number of combinations of $n$ different things taken
nothing at all is considered to be 1. Counting combinations is merely counting the
number of ways in which some or all objects at a time are selected. Selecting
nothing at all is the same as leaving behind all the objects and we know that there
is only one way of doing so. This way we define $^n\text{C}_0 = 1$.

3. As $\frac{n!}{0!(n-0)!} = 1 = ^n\text{C}_0$, the formula $^n\text{C}_r = \frac{n!}{r!(n-r)!}$ is applicable for $r = 0$ also.

Hence

$$^n\text{C}_r = \frac{n!}{r!(n-r)!}, 0 \le r \le n.$$

4. $^n\text{C}_{n-r} = \frac{n!}{(n-r)!(n-(n-r))!} = \frac{n!}{(n-r)!r!} = ^n\text{C}_r$,

<!-- page 214 -->
i.e., selecting $r$ objects out of $n$ objects is same as rejecting $(n - r)$ objects.

\textbf{5.} ${}^n\mathrm{C}_a = {}^n\mathrm{C}_b \Rightarrow a = b$ or $a = n - b$, i.e., $n = a + b$

Theorem 6 $^n\mathrm{C}_r + ^n\mathrm{C}_{r-1} = ^{n+1}\mathrm{C}_r$

Proof We have $${}^n\text{C}_r + {}^n\text{C}_{r-1} = \frac{n!}{r!(n-r)!} + \frac{n!}{(r-1)!(n-r+1)!}$$

$$= \frac{n!}{r \times (r-1)!(n-r)!} + \frac{n!}{(r-1)!(n-r+1)(n-r)!}$$

$$= \frac{n!}{(r-1)!(n-r)!} \left[ \frac{1}{r} + \frac{1}{n-r+1} \right]$$

$$= \frac{n!}{(r-1)!(n-r)!} \times \frac{n-r+1+r}{r(n-r+1)} = \frac{(n+1)!}{r!(n+1-r)!} = {}^{n+1}\text{C}_r$$

Example 17 If $^n\text{C}_9 = ^n\text{C}_8$, find $^n\text{C}_{17}$.

Solution We have $^n\text{C}_9 = ^n\text{C}_8$

i.e., $\frac{n!}{9!(n-9)!} = \frac{n!}{(n-8)!8!}$

or $\frac{1}{9} = \frac{1}{n-8}$ or $n-8 = 9$ or $n = 17$

Therefore $^n\text{C}_{17} = ^{17}\text{C}_{17} = 1$.

Therefore $${}^{n}\mathrm{C}_{17} = {}^{17}\mathrm{C}_{17} = 1.$

Example 18 A committee of 3 persons is to be constituted from a group of 2 men and
3 women. In how many ways can this be done? How many of these committees would
consist of 1 man and 2 women?

Solution Here, order does not matter. Therefore, we need to count combinations.
There will be as many committees as there are combinations of 5 different persons

taken 3 at a time. Hence, the required number of ways = $^5\text{C}_3 = \frac{5!}{3! \ 2!} = \frac{4 \times 5}{2} = 10$ .

Now, 1 man can be selected from 2 men in $^2\text{C}_1$ ways and 2 women can be
selected from 3 women in $^3\text{C}_2$ ways. Therefore, the required number of committees

<!-- page 215 -->
$$= ^2\text{C}_1 \times ^3\text{C}_2 = \frac{2!}{1! \ 1!} \times \frac{3!}{2! \ 1!} = 6.$$

Example 19 What is the number of ways of choosing 4 cards from a pack of 52
playing cards? In how many of these

(i) four cards are of the same suit,
(ii) four cards belong to four different suits,
(iii) are face cards,
(iv) two are red cards and two are black cards,
(v) cards are of the same colour?

Solution There will be as many ways of choosing 4 cards from 52 cards as there are
combinations of 52 different things, taken 4 at a time. Therefore

The required number of ways = ${}^{52}\text{C}_4 = \frac{52!}{4! \ 48!} = \frac{49 \times 50 \times 51 \times 52}{2 \times 3 \times 4}$
$= 270725$

(i) There are four suits: diamond, club, spade, heart and there are 13 cards of each
suit. Therefore, there are $^{13}\text{C}_4$ ways of choosing 4 diamonds. Similarly, there are
$^{13}\text{C}_4$ ways of choosing 4 clubs, $^{13}\text{C}_4$ ways of choosing 4 spades and $^{13}\text{C}_4$ ways of
choosing 4 hearts. Therefore
The required number of ways $= ^{13}\text{C}_4 + ^{13}\text{C}_4 + ^{13}\text{C}_4 + ^{13}\text{C}_4$.
$$= 4 \times \frac{13!}{4! \ 9!} = 2860$$

(ii) There are13 cards in each suit.
Therefore, there are $^{13}\text{C}_1$ ways of choosing 1 card from 13 cards of diamond,
$^{13}\text{C}_1$ ways of choosing 1 card from 13 cards of hearts, $^{13}\text{C}_1$ ways of choosing 1
card from 13 cards of clubs, $^{13}\text{C}_1$ ways of choosing 1 card from 13 cards of
spades. Hence, by multiplication principle, the required number of ways
$$= ^{13}\text{C}_1 \times ^{13}\text{C}_1 \times ^{13}\text{C}_1 \times ^{13}\text{C}_1 = 13^4$$

(iii) There are 12 face cards and 4 are to be selected out of these 12 cards. This can be
done in $^{12}\text{C}_4$ ways. Therefore, the required number of ways $= \frac{12!}{4! \ 8!} = 495$.

<!-- page 216 -->
(iv) There are 26 red cards and 26 black cards. Therefore, the required number of
ways = $^{26}\text{C}_2 \times ^{26}\text{C}_2$

$$= \left( \frac{26!}{2! 24!} \right)^2 = (325)^2 = 105625$$

(v) 4 red cards can be selected out of 26 red cards in $^{26}\text{C}_4$ ways.
4 black cards can be selected out of 26 black cards in $^{26}\text{C}_4$ways.

Therefore, the required number of ways $= ^{26}\mathrm{C}_4 + ^{26}\mathrm{C}_4$
$= 2 \times \frac{26!}{4! \ 22!} = 29900.$

EXERCISE 7.4

1. If $^n\text{C}_8 = ^n\text{C}_2$, find $^n\text{C}_2$.
2. Determine $n$ if
(i) $^{2n}\text{C}_3 : ^n\text{C}_3 = 12 : 1$                                     (ii) $^{2n}\text{C}_3 : ^n\text{C}_3 = 11 : 1$
3. How many chords can be drawn through 21 points on a circle?
4. In how many ways can a team of 3 boys and 3 girls be selected from 5 boys and
4 girls?
5. Find the number of ways of selecting 9 balls from 6 red balls, 5 white balls and 5
blue balls if each selection consists of 3 balls of each colour.
6. Determine the number of 5 card combinations out of a deck of 52 cards if there
is exactly one ace in each combination.
7. In how many ways can one select a cricket team of eleven from 17 players in
which only 5 players can bowl if each cricket team of 11 must include exactly 4
bowlers?
8. A bag contains 5 black and 6 red balls. Determine the number of ways in which
2 black and 3 red balls can be selected.
9. In how many ways can a student choose a programme of 5 courses if 9 courses
are available and 2 specific courses are compulsory for every student?

Miscellaneous Examples

Example 20 How many words, with or without meaning, each of 3 vowels and 2
consonants can be formed from the letters of the word INVOLUTE ?

Solution In the word INVOLUTE, there are 4 vowels, namely, I,O,E,Uand 4
consonants, namely, N, V, L and T.

<!-- page 217 -->
The number of ways of selecting 3 vowels out of 4 = $^4\text{C}_3 = 4$.
The number of ways of selecting 2 consonants out of 4 = $^4\text{C}_2 = 6$.

Therefore, the number of combinations of 3 vowels and 2 consonants is
$4 \times 6 = 24$.

Now, each of these 24 combinations has 5 letters which can be arranged among
themselves in 5 ! ways. Therefore, the required number of different words is
$$24 \times 5 != 2880.$$

Example 21 A group consists of 4 girls and 7 boys. In how many ways can a team of
5 members be selected if the team has (i) no girl ? (ii) at least one boy and one girl ?
(iii) at least 3 girls ?

Solution (i) Since, the team will not include any girl, therefore, only boys are to be
selected. 5 boys out of 7 boys can be selected in $^7\text{C}_5$ ways. Therefore, the required

$$\text{number of ways} = {}^{7}\text{C}_{5} = \frac{7!}{5! \ 2!} = \frac{6 \times 7}{2} = 21$$

(ii) Since, at least one boy and one girl are to be there in every team. Therefore, the
team can consist of
(a) 1 boy and 4 girls
(b) 2 boys and 3 girls
(c) 3 boys and 2 girls
(d) 4 boys and 1 girl.

1 boy and 4 girls can be selected in $^7\text{C}_1 \times ^4\text{C}_4$ ways.
2 boys and 3 girls can be selected in $^7\text{C}_2 \times ^4\text{C}_3$ ways.
3 boys and 2 girls can be selected in $^7\text{C}_3 \times ^4\text{C}_2$ ways.
4 boys and 1 girl can be selected in $^7\text{C}_4 \times ^4\text{C}_1$ ways.

Therefore, the required number of ways

$$= {}^{7}\text{C}_{1} \times {}^{4}\text{C}_{4} + {}^{7}\text{C}_{2} \times {}^{4}\text{C}_{3} + {}^{7}\text{C}_{3} \times {}^{4}\text{C}_{2} + {}^{7}\text{C}_{4} \times {}^{4}\text{C}_{1}$$
$$= 7 + 84 + 210 + 140 = 441$$

(iii) Since, the team has to consist of at least 3 girls, the team can consist of
(a) 3 girls and 2 boys, or (b) 4 girls and 1 boy.

Note that the team cannot have all 5 girls, because, the group has only 4 girls.

3 girls and 2 boys can be selected in $^4\text{C}_3 \times ^7\text{C}_2$ ways.
4 girls and 1 boy can be selected in $^4\text{C}_4 \times ^7\text{C}_1$ ways.

Therefore, the required number of ways

$$= ^4\text{C}_3 \times ^7\text{C}_2 + ^4\text{C}_4 \times ^7\text{C}_1 = 84 + 7 = 91$$

<!-- page 218 -->
Example 22 Find the number of words with or without meaning which can be made
using all the letters of the word AGAIN. If these words are written as in a dictionary,
what will be the $50^{\text{th}}$ word?

Solution There are 5 letters in the word AGAIN, in which A appears 2 times. Therefore,

the required number of words = $\frac{5!}{2!} = 60$.

To get the number of words starting with A, we fix the letter A at the extreme left
position, we then rearrange the remaining 4 letters taken all at a time. There will be as
many arrangements of these 4 letters taken 4 at a time as there are permutations of 4
different things taken 4 at a time. Hence, the number of words starting with

$A = 4! = 24$. Then, starting with G, the number of words $= \frac{4!}{2!} = 12$ as after placing G

at the extreme left position, we are left with the letters A, A, I and N. Similarly, there
are 12 words starting with the next letter I. Total number of words so far obtained
$= 24 + 12 + 12 =48.$

The $49^{\text{th}}$ word is NAAGI. The $50^{\text{th}}$ word is NAAIG.

Example 23 How many numbers greater than 1000000 can be formed by using the
digits 1, 2, 0, 2, 4, 2, 4?

Solution Since, 1000000 is a 7-digit number and the number of digits to be used is also
7. Therefore, the numbers to be counted will be 7-digit only. Also, the numbers have to
be greater than 1000000, so they can begin either with 1, 2 or 4.

The number of numbers beginning with $1 = \frac{6!}{3! 2!} = \frac{4 \times 5 \times 6}{2} = 60$, as when 1 is

fixed at the extreme left position, the remaining digits to be rearranged will be $0, 2, 2, 2,$
$4, 4,$ in which there are $3, \ 2s$ and $2, 4s.$

Total numbers begining with 2

$$= \frac{6!}{2! \ 2!} = \frac{3 \times 4 \times 5 \times 6}{2} = 180$$

and total numbers begining with $4 = \frac{6!}{3!} = 4 \times 5 \times 6 = 120$

<!-- page 219 -->
Therefore, the required number of numbers $= 60 + 180 + 120 = 360.$

Alternative Method

The number of 7-digit arrangements, clearly, $\frac{7!}{3! \ 2!} = 420$ . But, this will include those
numbers also, which have 0 at the extreme left position. The number of such
arrangements $\frac{6!}{3! \ 2!}$ (by fixing 0 at the extreme left position) $= 60$.

Therefore, the required number of numbers $= 420 - 60 = 360.$

**Note** If one or more than one digits given in the list is repeated, it will be
understood that in any number, the digits can be used as many times as is given in
the list, e.g., in the above example 1 and 0 can be used only once whereas 2 and 4
can be used 3 times and 2 times, respectively.

Example 24 In how many ways can 5 girls and 3 boys be seated in a row so that no
two boys are together?

Solution Let us first seat the 5 girls. This can be done in $5!$ ways. For each such
arrangement, the three boys can be seated only at the cross marked places.
$$\times G \times G \times G \times G \times G \times$$
There are 6 cross marked places and the three boys can be seated in $^6\text{P}_3$ ways.
Hence, by multiplication principle, the total number of ways

$$= 5! \times ^6\text{P}_3 = 5! \times \frac{6!}{3!}$$

$$= 4 \times 5 \times 2 \times 3 \times 4 \times 5 \times 6 = 14400.$$

Miscellaneous Exercise on Chapter 7

1. How many words, with or without meaning, each of 2 vowels and 3 consonants
can be formed from the letters of the word DAUGHTER ?
2. How many words, with or without meaning, can be formed using all the letters of
the word EQUATION at a time so that the vowels and consonants occur together?
3. A committee of 7 has to be formed from 9 boys and 4 girls. In how many ways
can this be done when the committee consists of:
(i) exactly 3 girls ? (ii) atleast 3 girls ? (iii) atmost 3 girls ?
4. If the different permutations of all the letter of the word EXAMINATION are

<!-- page 220 -->
listed as in a dictionary, how many words are there in this list before the first
word starting with E ?

5. How many 6-digit numbers can be formed from the digits 0, 1, 3, 5, 7 and 9
which are divisible by 10 and no digit is repeated ?
6. The English alphabet has 5 vowels and 21 consonants. How many words with
two different vowels and 2 different consonants can be formed from the
alphabet ?
7. In an examination, a question paper consists of 12 questions divided into two
parts i.e., Part I and Part II, containing 5 and 7 questions, respectively. A student
is required to attempt 8 questions in all, selecting at least 3 from each part. In
how many ways can a student select the questions ?
8. Determine the number of 5-card combinations out of a deck of 52 cards if each
selection of 5 cards has exactly one king.
9. It is required to seat 5 men and 4 women in a row so that the women occupy the
even places. How many such arrangements are possible ?
10. From a class of 25 students, 10 are to be chosen for an excursion party. There
are 3 students who decide that either all of them will join or none of them will
join. In how many ways can the excursion party be chosen ?
11. In how many ways can the letters of the word ASSASSINATION be arranged
so that all the S's are together ?

Summary

$\diamond$ Fundamental principle of counting If an event can occur in $m$ different
ways, following which another event can occur in $n$ different ways, then the
total number of occurrence of the events in the given order is $m \times n$.
$\diamond$ The number of permutations of $n$ different things taken $r$ at a time, where

repetition is not allowed, is denoted by $^nP_r$ and is given by $^nP_r = \frac{n!}{(n-r)!}$,

where $0 \le r \le n$.
$\diamond$ $n! = 1 \times 2 \times 3 \times ... \times n$
$\diamond$ $n! = n \times (n-1)$ !
$\diamond$ The number of permutations of $n$ different things, taken $r$ at a time, where
repeation is allowed, is $n'$.
$\diamond$ The number of permutations of $n$ objects taken all at a time, where $p_1$ objects

<!-- page 221 -->
are of first kind, $p_2$ objects are of the second kind, ..., $p_k$ objects are of the $k^{\text{th}}$

kind and rest, if any, are all different is $\frac{n!}{p_1! \ p_2! \ ... \ p_k!}$.

The number of combinations of $n$ different things taken $r$ at a time, denoted by


${}^n\text{C}_r$, is given by ${}^n\text{C}_r = =\frac{n!}{r!(n-r)!}, 0 \le r \le n.$

Historical Note

The concepts of permutations and combinations can be traced back to the advent
of Jainism in India and perhaps even earlier. The credit, however, goes to the
Jains who treated its subject matter as a self-contained topic in mathematics,
under the name Vikalpa.
Among the Jains, Mahavira, (around 850) is perhaps the world’s first
mathematician credited with providing the general formulae for permutations and
combinations.
In the 6th century B.C., Sushruta, in his medicinal work, Sushruta Samhita,
asserts that 63 combinations can be made out of 6 different tastes, taken one at a
time, two at a time, etc. Pingala, a Sanskrit scholar around third century B.C.,
gives the method of determining the number of combinations of a given number
of letters, taken one at a time, two at a time, etc. in his work Chhanda Sutra.
Bhaskaracharya (born 1114) treated the subject matter of permutations and
combinations under the name Anka Pasha in his famous work Lilavati. In addition
to the general formulae for $^nC_r$ and $^nP_r$ already provided by Mahavira,
Bhaskaracharya gives several important theorems and results concerning the
subject.
Outside India, the subject matter of permutations and combinations had its
humble beginnings in China in the famous book I–King (Book of changes). It is
difficult to give the approximate time of this work, since in 213 B.C., the emperor
had ordered all books and manuscripts in the country to be burnt which fortunately
was not completely carried out. Greeks and later Latin writers also did some
scattered work on the theory of permutations and combinations.
Some Arabic and Hebrew writers used the concepts of permutations and
combinations in studying astronomy. Rabbi ben Ezra, for instance, determined
the number of combinations of known planets taken two at a time, three at a time
and so on. This was around 1140. It appears that Rabbi ben Ezra did not know

<!-- page 222 -->
the formula for $^n\text{C}_r$. However, he was aware that $^n\text{C}_r = ^n\text{C}_{n-r}$ for specific values
$n$ and $r$. In 1321, Levi Ben Gerson, another Hebrew writer came up with the
formulae for $^nP_r$, $^nP_n$ and the general formula for $^n\text{C}_r$.
    The first book which gives a complete treatment of the subject matter of
permutations and combinations is Ars Conjectandi written by a Swiss, Jacob
Bernoulli (1654 – 1705), posthumously published in 1713. This book contains
essentially the theory of permutations and combinations as is known today.

<!-- page 223 -->
Chapter 8

BINOMIALTHEOREM

❖Mathematics is a most exact science and its conclusions are capable of
absolute proofs. – C.P. STEINMETZ❖

8.1 Introduction

In earlier classes, we have learnt how to find the squares
and cubes of binomials like $a + b$ and $a - b$. Using them, we
could evaluate the numerical values of numbers like
$(98)^2 = (100 - 2)^2$, $(999)^3 = (1000 - 1)^3$, etc. However, for
higher powers like $(98)^5$, $(101)^6$, etc., the calculations become
difficult by using repeated multiplication. This difficulty was
overcome by a theorem known as binomial theorem. It gives
an easier way to expand $(a + b)^n$, where $n$ is an integer or a
rational number. In this Chapter, we study binomial theorem
for positive integral indices only.

Blaise Pascal
(1623-1662)

8.2 Binomial Theorem for Positive Integral Indices

Let us have a look at the following identities done earlier:

$(a+b)^0 = 1$                                     $a+b \neq 0$
$(a+b)^1 = a+b$
$(a+b)^2 = a^2 + 2ab + b^2$
$(a+b)^3 = a^3 + 3a^2b + 3ab^2 + b^3$
$(a+b)^4 = (a+b)^3 (a+b) = a^4 + 4a^3b + 6a^2b^2 + 4ab^3 + b^4$

In these expansions, we observe that

(i) The total number of terms in the expansion is one more than the index. For
example, in the expansion of $(a + b)^2$, number of terms is 3 whereas the index of
$(a + b)^2$ is 2.
(ii) Powers of the first quantity '$a$' go on decreasing by 1 whereas the powers of the
second quantity '$b$' increase by 1, in the successive terms.
(iii) In each term of the expansion, the sum of the indices of $a$ and $b$ is the same and
is equal to the index of $a + b$.

<!-- page 224 -->
We now arrange the coefficients in these expansions as follows (Fig 8.1):

<table>
<thead>
<tr>
<th>Index</th>
<th colspan="5">Coefficients</th>
</tr>
</thead>
<tbody>
<tr>
<td>0</td>
<td colspan="5">1</td>
</tr>
<tr>
<td>1</td>
<td colspan="2">1</td>
<td colspan="3">1</td>
</tr>
<tr>
<td>2</td>
<td colspan="2">1</td>
<td>2</td>
<td colspan="2">1</td>
</tr>
<tr>
<td>3</td>
<td>1</td>
<td>3</td>
<td>3</td>
<td colspan="2">1</td>
</tr>
<tr>
<td>4</td>
<td>1</td>
<td>4</td>
<td>6</td>
<td>4</td>
<td>1</td>
</tr>
</tbody>
</table>

Fig 8.1

Do we observe any pattern in this table that will help us to write the next row? Yes we
do. It can be seen that the addition of 1's in the row for index 1 gives rise to 2 in the row
for index 2. The addition of 1, 2 and 2, 1 in the row for index 2, gives rise to 3 and 3 in
the row for index 3 and so on. Also, 1 is present at the beginning and at the end of each
row. This can be continued till any index of our interest.

We can extend the pattern given in Fig 8.2 by writing a few more rows.

Fig 8.2

Pascal's Triangle

The structure given in Fig 8.2 looks like a triangle with 1 at the top vertex and running
down the two slanting sides. This array of numbers is known as Pascal's triangle,
after the name of French mathematician Blaise Pascal. It is also known as Meru
Prastara by Pingla.

Expansions for the higher powers of a binomial are also possible by using Pascal's
triangle. Let us expand $(2x + 3y)^5$ by using Pascal's triangle. The row for index 5 is

$$1 \quad 5 \quad 10 \quad 10 \quad 5 \quad 1$$

Using this row and our observations (i), (ii) and (iii), we get

$$\begin{aligned} \\ (2x + 3y)^5 &= (2x)^5 + 5(2x)^4 (3y) + 10(2x)^3 (3y)^2 + 10 (2x)^2 (3y)^3 + 5(2x)(3y)^4 +(3y)^5 \\ \\ &= 32x^5 + 240x^4y + 720x^3y^2 + 1080x^2y^3 + 810xy^4 + 243y^5. \\ \end{aligned}$$

<!-- page 225 -->
Now, if we want to find the expansion of $(2x + 3y)^{12}$, we are first required to get
the row for index 12. This can be done by writing all the rows of the Pascal's triangle
till index 12. This is a slightly lengthy process. The process, as you observe, will become
more difficult, if we need the expansions involving still larger powers.

We thus try to find a rule that will help us to find the expansion of the binomial for
any power without writing all the rows of the Pascal's triangle, that come before the
row of the desired index.

For this, we make use of the concept of combinations studied earlier to rewrite

the numbers in the Pascal's triangle. We know that ${}^n\mathrm{C}_r = \frac{n!}{r!(n-r)!}$ , $0 \le r \le n$ and

$n$ is a non-negative integer. Also, ${}^n\mathrm{C}_0 = 1 = {}^n\mathrm{C}_n$

The Pascal's triangle can now be rewritten as (Fig 8.3)

<table>
<thead>
<tr>
<th>Index</th>
<th>Coefficients</th>
</tr>
</thead>
<tbody>
<tr>
<td>0</td>
<td><sup>0</sup>C<sub>0</sub><br/>(=1)</td>
</tr>
<tr>
<td>1</td>
<td><sup>1</sup>C<sub>0</sub><sup>1</sup><br/>(=1)<sup>1</sup> C<sub>1</sub><br/>(=1)</td>
</tr>
<tr>
<td>2</td>
<td><sup>2</sup>C<sub>0</sub><sup>2</sup><br/>(=1)<sup>2</sup> C<sub>1</sub><sup>2</sup><br/>(=2)<sup>2</sup> C<sub>2</sub><br/>(=1)<sup>2</sup> C<sub>2</sub><br/>(=1)<sup>2</sup> C<sub>3</sub></td>
</tr>
<tr>
<td>3</td>
<td><sup>3</sup>C<sub>0</sub><sup>3</sup><br/>(=1)<sup>3</sup> C<sub>1</sub><sup>3</sup><br/>(=3)<sup>3</sup> C<sub>2</sub><sup>3</sup><br/>(=3)<sup>3</sup> C<sub>3</sub><br/>(=1)<sup>3</sup> C<sub>4</sub></td>
</tr>
<tr>
<td>4</td>
<td><sup>4</sup>C<sub>0</sub><sup>4</sup><br/>(=1)<sup>4</sup> C<sub>1</sub><sup>4</sup><br/>(=4)<sup>4</sup> C<sub>2</sub><sup>4</sup><br/>(=6)<sup>4</sup> C<sub>3</sub><sup>4</sup><br/>(=4)<sup>4</sup> C<sub>4</sub><sup>4</sup><br/>(=1)<sup>4</sup> C<sub>5</sub></td>
</tr>
<tr>
<td>5</td>
<td><sup>5</sup>C<sub>0</sub><sup>5</sup><br/>(=1)<sup>5</sup> C<sub>1</sub><sup>5</sup><br/>(=5)<sup>5</sup> C<sub>2</sub><sup>5</sup><br/>(=10)<sup>5</sup> C<sub>3</sub><sup>5</sup><br/>(=10)<sup>5</sup> C<sub>4</sub><sup>5</sup><br/>(=5)<sup>5</sup> C<sub>5</sub><sup>5</sup><br/>(=1)<sup>5</sup> C<sub>6</sub><sup>5</sup></td>
</tr>
</tbody>
</table>

Fig 8.3 Pascal's triangle

Observing this pattern, we can now write the row of the Pascal's triangle for any index
without writing the earlier rows. For example, for the index 7 the row would be

${}^7\text{C}_0 \ {}^7\text{C}_1 \ {}^7\text{C}_2 \ {}^7\text{C}_3 \ {}^7\text{C}_4 \ {}^7\text{C}_5 \ {}^7\text{C}_6 \ {}^7\text{C}_7.$

Thus, using this row and the observations (i), (ii) and (iii), we have

$$(a+b)^7 = ^7\text{C}_0 a^7 + ^7\text{C}_1 a^6 b + ^7\text{C}_2 a^5 b^2 + ^7\text{C}_3 a^4 b^3 + ^7\text{C}_4 a^3 b^4 + ^7\text{C}_5 a^2 b^5 + ^7\text{C}_6 a b^6 + ^7\text{C}_7 b^7$$

An expansion of a binomial to any positive integral index say $n$ can now be visualised
using these observations. We are now in a position to write the expansion of a binomial
to any positive integral index.

<!-- page 226 -->
8.2.1 Binomial theorem for any positive integer $n$,

$$(a + b)^n = {}^n\mathrm{C}_0 a^n + {}^n\mathrm{C}_1 a^{n-1} b + {}^n\mathrm{C}_2 a^{n-2} b^2 + ... + {}^n\mathrm{C}_{n-1} a . b^{n-1} + {}^n\mathrm{C}_n b^n$$

Proof The proof is obtained by applying principle of mathematical induction.

Let the given statement be

$$\mathrm{P}(n) : (a + b)^n = {}^n\mathrm{C}_0 a^n + {}^n\mathrm{C}_1 a^{n-1} b + {}^n\mathrm{C}_2 a^{n-2} b^2 + ... + {}^n\mathrm{C}_{n-1} a . b^{n-1} + {}^n\mathrm{C}_n b^n$$

For $n = 1$, we have

$$\mathrm{P} (1) : (a + b)^1 = {}^1\mathrm{C}_0 a^1 + {}^1\mathrm{C}_1 b^1 = a + b$$

Thus, P (1) is true.

Suppose P ($k$) is true for some positive integer $k$, i.e.

$$(a + b)^k = {}^k\text{C}_0 a^k + {}^k\text{C}_1 a^{k-1} b + {}^k\text{C}_2 a^{k-2} b^2 + ... + {}^k\text{C}_k b^k \qquad \dots (1)$$

We shall prove that $\mathrm{P}(k+1)$ is also true, i.e.,

$$(a+b)^{k+1} = {}^{k+1}\mathrm{C}_0 a^{k+1} + {}^{k+1}\mathrm{C}_1 a^k b + {}^{k+1}\mathrm{C}_2 a^{k-1} b^2 + ... + {}^{k+1}\mathrm{C}_{k+1} b^{k+1}$$

Now, $(a+b)^{k+1}=(a+b)(a+b)^{k}$

$=(a+b)\left({ }^{k}\mathrm{C}_{0}a^{k}+\{^{k}\mathrm{C}_{1}a^{k-1}b+{ }^{k}\mathrm{C}_{2}a^{k-2}b^{2}+\ldots+{ }^{k}\mathrm{C}_{k-1}ab^{k-1}+{^{k}\mathrm{C}_{k}b^{k}}\right)$

[from (1)]

$={}^{k}\mathrm{C}_{0}a^{k+1}+{^{k}\mathrm{C}_{1}a^{k}b+{ }^{k}\mathrm{C}_{2}a^{k-1}b^{2}+\ldots+{ }^{k}\mathrm{C}_{k-1}a^{2}b^{k-1}+{^{k}\mathrm{C}_{k}ab^{k}+{^{k}\mathrm{C}_{0}a^{k}b}$

$+{ }^{k}\mathrm{C}_{1}a^{k-1}b^{2}+{^{k}\mathrm{C}_{2}a^{k-2}b^{3}+\ldots+{ }^{k}\mathrm{C}_{k-1}ab^{k}+{^{k}\mathrm{C}_{k}b^{k+1}}$

[by actual multiplication]

$={}^{k}\mathrm{C}_{0}a^{k+1}+{{ }^{k}\mathrm{C}_{1}+{^{k}\mathrm{C}_{0}})a^{k}b+{ ({ }^{k}\mathrm{C}_{2}+{^{k}\mathrm{C}_{1}})a^{k-1}b^{2}+\ldots$

$+{ ({}^{k}\mathrm{C}_{k}+{^{k}\mathrm{C}_{k-1}})ab^{k}+{^{k}\mathrm{C}_{k}b^{k+1}}$

[grouping like terms]

$={}^{k+1}\mathrm{C}_{0}a^{k+1}+{^{k+1}\mathrm{C}_{1}a^{k}b+{ }^{k+1}\mathrm{C}_{2}a^{k-1}b^{2}+\ldots+{ }^{k+1}\mathrm{C}_{k}ab^{k}+{^{k+1}\mathrm{C}_{k+1}}b^{k+1}$

(by using ${ }^{k+1}\mathrm{C}_{0}=1$, ${}^{k}\mathrm{C}_{k}+{^{k}\mathrm{C}_{k-1}}={ }^{k+1}\mathrm{C}_{k}$ and ${}^{k}\mathrm{C}_{k}=1={}^{k+1}\mathrm{C}_{k+1}$)

Thus, it has been proved that $\mathrm{P} (k + 1)$ is true whenever $\mathrm{P}(k)$ is true. Therefore, by
principle of mathematical induction, $\mathrm{P}(n)$ is true for every positive integer $n$.

We illustrate this theorem by expanding $(x+2)^6$:

$$\begin{aligned} \\ (x+2)^{6} &= {}^{6}\mathrm{C}_{0}x^{6} + {}^{6}\mathrm{C}_{1}x^{5} \cdot 2 + {}^{6}\mathrm{C}_{2}x^{4}2^{2} + {}^{6}\mathrm{C}_{3}x^{3} \cdot 2^{3} + {}^{6}\mathrm{C}_{4}x^{2} \cdot 2^{4} + {}^{6}\mathrm{C}_{5}x \cdot 2^{5} + {}^{6}\mathrm{C}_{6} \cdot 2^{6} \\ \\ &= x^{6} + 12x^{5} + 60x^{4} + 160x^{3} + 240x^{2} + 192x + 64 \\ \end{aligned}$$

Thus $(x + 2)^6 = x^6 + 12x^5 + 60x^4 + 160x^3 + 240x^2 + 192x + 64.$

<!-- page 227 -->
Observations

1. The notation $\sum_{k=0}^{n} {}^{n}\mathrm{C}_{k} a^{n-k} b^{k}$ stands for

${}^{n}\mathrm{C}_{0} a^{n} b^{0} + {}^{n}\mathrm{C}_{1} a^{n-1} b^{1} + ... + {}^{n}\mathrm{C}_{r} a^{n-r} b^{r} + ... + {}^{n}\mathrm{C}_{n} a^{n-n} b^{n}$, where $b^{0} = 1 = a^{n-n}$.
Hence the theorem can also be stated as

$$(a+b)^n = \sum_{k=0}^n {}^n\mathrm{C}_k a^{n-k} b^k.$$

2. The coefficients ${}^nC_r$ occuring in the binomial theorem are known as binomial
coefficients.
3. There are $(n+1)$ terms in the expansion of $(a+b)^n$, i.e., one more than the index.
4. In the successive terms of the expansion the index of $a$ goes on decreasing by
unity. It is $n$ in the first term, $(n-1)$ in the second term, and so on ending with zero
in the last term. At the same time the index of $b$ increases by unity, starting with
zero in the first term, 1 in the second and so on ending with $n$ in the last term.
5. In the expansion of $(a+b)^n$, the sum of the indices of $a$ and $b$ is $n+0=n$ in the
first term, $(n-1)+1=n$ in the second term and so on $0+n=n$ in the last term.
Thus, it can be seen that the sum of the indices of $a$ and $b$ is $n$ in every term of the
expansion.

8.2.2 Some special cases In the expansion of $(a + b)^n$,

(i) Taking $a = x$ and $b = -y$, we obtain

$$\begin{aligned} \\ (x-y)^n &= [x+(-y)]^n \\ \\ &= {}^n\mathrm{C}_0x^n + {}^n\mathrm{C}_1x^{n-1}(-y) + {}^n\mathrm{C}_2x^{n-2}(-y)^2 + {}^n\mathrm{C}_3x^{n-3}(-y)^3 + ... + {}^n\mathrm{C}_n(-y)^n \\ \\ &= {}^n\mathrm{C}_0x^n - {}^n\mathrm{C}_1x^{n-1}y + {}^n\mathrm{C}_2x^{n-2}y^2 - {}^n\mathrm{C}_3x^{n-3}y^3 + ... + (-1)^n {}^n\mathrm{C}_n y^n \\ \end{aligned}$$

Thus $(x-y)^n = {}^nC_0x^n - {}^nC_1x^{n-1}y + {}^nC_2x^{n-2}y^2 + ... + (-1)^n {}^nC_ny^n$

Using this, we have
$$\begin{aligned} \\ (x-2y)^5 &= {}^5\text{C}_0x^5 - {}^5\text{C}_1x^4(2y) + {}^5\text{C}_2x^3(2y)^2 - {}^5\text{C}_3x^2(2y)^3 + \\ \\ &= {}^5\text{C}_4x(2y)^4 - {}^5\text{C}_5(2y)^5 \\ \\ &= x^5 - 10x^4y + 40x^3y^2 - 80x^2y^3 + 80xy^4 - 32y^5. \\ \end{aligned}$$

(ii) Taking $a=1$, $b=x$, we obtain

$$(1+x)^n = {}^n\text{C}_0(1)^n + {}^n\text{C}_1(1)^{n-1}x + {}^n\text{C}_2(1)^{n-2}x^2 + ... + {}^n\text{C}_nx^n$$
$$= {}^n\text{C}_0 + {}^n\text{C}_1x + {}^n\text{C}_2x^2 + {}^n\text{C}_3x^3 + ... + {}^n\text{C}_nx^n$$

Thus $\quad (1+x)^n = {}^n\mathrm{C}_0 + {}^n\mathrm{C}_1x + {}^n\mathrm{C}_2x^2 + {}^n\mathrm{C}_3x^3 + ... + {}^n\mathrm{C}_nx^n$

<!-- page 228 -->
In particular, for $x = 1$, we have

$$2^n = {}^nC_0 + {}^nC_1 + {}^nC_2 + ... + {}^nC_n.$$

(iii) Taking $a=1$, $b=-x$, we obtain

$$(1-x)^n = {}^nC_0 - {}^nC_1x + {}^nC_2x^2 - ... + (-1)^n {}^nC_nx^n$$

In particular, for $x = 1$, we get

$$0 = {}^nC_0 - {}^nC_1 + {}^nC_2 - ... + (-1)^n {}^nC_n$$

Example 1 Expand $\left(x^2 + \frac{3}{x}\right)^4, x \neq 0$

Solution By using binomial theorem, we have

$$x^2 + \frac{3}{x} = ^4\text{C}_0(x^2)^4 + ^4\text{C}_1(x^2)^3 \left(\frac{3}{x}\right) + ^4\text{C}_2(x^2)^2 \left(\frac{3}{x}\right)^2 + ^4\text{C}_3(x^2) \left(\frac{3}{x}\right)^3 + ^4\text{C}_4 \left(\frac{3}{x}\right)^4$$

$$= x^8 + 4 \cdot x^6 \cdot \frac{3}{x} + 6 \cdot x^4 \cdot \frac{9}{x^2} + 4 \cdot x^2 \cdot \frac{27}{x^3} + \frac{81}{x^4}$$

$$= x^8 + 12x^5 + 54x^2 + \frac{108}{x} + \frac{81}{x^4}.$$

Example 2 Compute $(98)^5$.

Example 2 Compute $(98)^5$.

Solution We express 98 as the sum or difference of two numbers whose powers are
easier to calculate, and then use Binomial Theorem.

Write $98 = 100 - 2$

Therefore, $(98)^5 = (100 - 2)^5$
$= ^5C_0 (100)^5 - ^5C_1 (100)^4.2 + ^5C_2 (100)^3 2^2$
$- ^5C_3 (100)^2 (2)^3 + ^5C_4 (100) (2)^4 - ^5C_5 (2)^5$
$= 10000000000 - 5 \times 100000000 \times 2 + 10 \times 1000000 \times 4 - 10 \times 10000$
$\times 8 + 5 \times 100 \times 16 - 32$

$= 10040008000 - 1000800032 = 9039207968.$

Example 3 Which is larger $(1.01)^{1000000}$ or $10,000$?

Solution Splitting $1.01$ and using binomial theorem to write the first few terms we
have

<!-- page 229 -->
$(1.01)^{1000000} = (1 + 0.01)^{1000000}$
$= ^{1000000}\text{C}_0 + ^{1000000}\text{C}_1(0.01) + \text{other positive terms}$
$= 1 + 1000000 \times 0.01 + \text{other positive terms}$
$= 1 + 10000 + \text{other positive terms}$
$> 10000$

Hence $(1.01)^{1000000} > 10000$

Example 4 Using binomial theorem, prove that $6^n-5n$ always leaves remainder
1 when divided by 25.

Solution For two numbers $a$ and $b$ if we can find numbers $q$ and $r$ such that
$a = bq + r$, then we say that $b$ divides $a$ with $q$ as quotient and $r$ as remainder. Thus, in
order to show that $6^n - 5n$ leaves remainder 1 when divided by 25, we prove that
$6^n - 5n = 25k + 1$, where $k$ is some natural number.

We have
$$(1 + a)^n = {}^n\text{C}_0 + {}^n\text{C}_1a + {}^n\text{C}_2a^2 + ... + {}^n\text{C}_na^n$$
For $a = 5$, we get
$$(1 + 5)^n = {}^n\text{C}_0 + {}^n\text{C}_15 + {}^n\text{C}_25^2 + ... + {}^n\text{C}_n5^n$$
i.e. $$(6)^n = 1 + 5n + 5^2. {}^n\text{C}_2 + 5^3. {}^n\text{C}_3 + ... + 5^n$$
i.e. $6^n - 5n = 1+5^2$ ($^n\text{C}_2 + {}^n\text{C}_35 + ... + 5^{n-2}$)
or $6^n - 5n = 1+ 25$ ($^n\text{C}_2 + 5. {}^n\text{C}_3 + ... + 5^{n-2}$)
or $6^n - 5n = 25k+1$ where $k = {}^n\text{C}_2 + 5. {}^n\text{C}_3 + ... + 5^{n-2}$.

This shows that when divided by 25, $6^n - 5n$ leaves remainder 1.

This shows that when divided by 25, $6^n - 5n$ leaves remainder 1.

EXERCISE 8.1

Expand each of the expressions in Exercises 1 to 5.

1. $(1-2x)^5$
2. $\left(\frac{2}{x} - \frac{x}{2}\right)^5$
3. $(2x - 3)^6$

<!-- page 230 -->
4. $\left(\frac{x}{3}+\frac{1}{x}\right)^5$                                     5. $\left(x+\frac{1}{x}\right)^6$

Using binomial theorem, evaluate each of the following:

6. $(96)^3$
7. $(102)^5$
8. $(101)^4$
9. $(99)^5$
10. Using Binomial Theorem, indicate which number is larger $(1.1)^{10000}$ or $1000$.
11. Find $(a+b)^4 - (a-b)^4$. Hence, evaluate $(\sqrt{3} + \sqrt{2})^4 - (\sqrt{3} - \sqrt{2})^4$.
12. Find $(x+1)^6 + (x-1)^6$. Hence or otherwise evaluate $(\sqrt{2} + 1)^6 + (\sqrt{2} - 1)^6$.
13. Show that $9^{n+1} - 8n - 9$ is divisible by $64$, whenever $n$ is a positive integer.
14. Prove that $\sum_{r=0}^n 3^r \text{ } ^n\text{C}_r = 4^n$.

8.3 General and Middle Terms

1. In the binomial expansion for $(a+b)^n$, we observe that the first term is
${}^n\text{C}_0a^n$, the second term is ${}^n\text{C}_1a^{n-1}b$, the third term is ${}^n\text{C}_2a^{n-2}b^2$, and so on. Looking
at the pattern of the successive terms we can say that the $(r+1)^{th}$ term is
${}^n\text{C}_ra^{n-r}b^r$. The $(r+1)^{th}$ term is also called the general term of the expansion
$(a+b)^n$. It is denoted by $\text{T}_{r+1}$. Thus $\text{T}_{r+1} = {}^n\text{C}_ra^{n-r}b^r$.
2. Regarding the middle term in the expansion $(a+b)^n$, we have
(i) If $n$ is even, then the number of terms in the expansion will be $n+1$. Since
$n$ is even so $n+1$ is odd. Therefore, the middle term is $\left( \frac{n+1+1}{2} \right)^{th}$, i.e.,
$\left( \frac{n}{2}+1 \right)^{th}$ term.
For example, in the expansion of $(x+2y)^8$, the middle term is $\left( \frac{8}{2}+1 \right)^{th}$ i.e.,
$5^{th}$ term.
(ii) If $n$ is odd, then $n+1$ is even, so there will be two middle terms in the

<!-- page 231 -->
expansion, namely, $\left(\frac{n+1}{2}\right)^{th}$ term and $\left(\frac{n+1}{2}+1\right)^{th}$ term. So in the expansion


$(2x-y)^7$, the middle terms are $\left(\frac{7+1}{2}\right)^{th}$, i.e., $4^{th}$ and $\left(\frac{7+1}{2}+1\right)^{th}$, i.e., $5^{th}$ term.

3. In the expansion of $\left(x+\frac{1}{x}\right)^{2n}$, where $x \neq 0$, the middle term is $\left(\frac{2n+1+1}{2}\right)^{th}$,
i.e., $(n+1)^{\text{th}}$ term, as $2n$ is even.

It is given by $^{2n}\mathrm{C}_n x^n \left( \frac{1}{x} \right)^n = ^{2n}\mathrm{C}_n$ (constant).

This term is called the term independent of $x$ or the constant term.

Example 5 Find $a$ if the $17^{th}$ and $18^{th}$ terms of the expansion $(2+a)^{50}$ are equal.

Solution The $(r+1)^{th}$ term of the expansion $(x+y)^n$ is given by $\mathrm{T}_{r+1} = ^n\mathrm{C}_r x^{n-r} y^r$.

For the $17^{th}$ term, we have, $r+1=17$, i.e., $r=16$

Therefore, $\mathrm{T}_{17} = \mathrm{T}_{16+1} = ^{50}\mathrm{C}_{16} (2)^{50-16} a^{16}$

$= ^{50}\mathrm{C}_{16} 2^{34} a^{16}$.

Similarly, $\mathrm{T}_{18} = ^{50}\mathrm{C}_{17} 2^{33} a^{17}$

Given that $\mathrm{T}_{17} = \mathrm{T}_{18}$

So $^{50}\mathrm{C}_{16} (2)^{34} a^{16} = ^{50}\mathrm{C}_{17} (2)^{33} a^{17}$

Therefore $\frac{^{50}\mathrm{C}_{16} \cdot 2^{34}}{{}^{50}\mathrm{C}_{17} \cdot 2^{33}} = \frac{a^{17}}{a^{16}}$

i.e., $a = \frac{^{50}\mathrm{C}_{16} \times 2}{{}^{50}\mathrm{C}_{17}} = \frac{50!}{16!34!} \times \frac{17! \cdot 33!}{50!} \times 2 = 1$

Example 6 Show that the middle term in the expansion of $(1+x)^{2n}$ is

$$\frac{1.3.5...(2n-1)}{n!} 2n x^n, \text{ where } n \text{ is a positive integer.}$$

<!-- page 232 -->
Solution As $2n$ is even, the middle term of the expansion $(1+x)^{2n}$ is $\left(\frac{2n}{2}+1\right)^{\text{th}}$,
i.e., $(n+1)^{\text{th}}$ term which is given by,

$$\text{T}_{n+1} = ^{2n}\text{C}_n(1)^{2n-n}(x)^n = ^{2n}\text{C}_n x^n = \frac{(2n)!}{n! \ n!} x^n$$

$$= \frac{2n(2n-1) \ (2n-2) \ ...4.3.2.1}{n! \ n!} x^n$$

$$= \frac{1.2.3.4...(2n- \ 2)(2n- \ 1)(2n)}{n!n!} x^n$$

$$= \frac{[1.3.5...(2n-1)][2.4.6...(2n)]}{n!n!} x^n$$

$$= \frac{[1.3.5...(2n-1)]2^n \ [1.2.3...n]}{n!n!} x^n$$

$$= \frac{[1.3.5...(2n-1)]n!}{n! \ n!} 2^n \cdot x^n$$

$$= \frac{1.3.5...(2n- \ 1)}{n!} 2^n \ x^n$$

Example 7 Find the coefficient of $x^6y^3$ in the expansion of $(x + 2y)^9$.

Solution Suppose $x^6y^3$ occurs in the $(r + 1)^{\text{th}}$ term of the expansion $(x + 2y)^9$.
Now $\text{T}_{r+1} = {}^9\text{C}_r x^{9-r} (2y)^r = {}^9\text{C}_r 2^r \cdot x^{9-r} \cdot y^r$.
Comparing the indices of $x$ as well as $y$ in $x^6y^3$ and in $\text{T}_{r+1}$, we get $r = 3$.
Thus, the coefficient of $x^6y^3$ is

$${}^9\text{C}_3 2^3 = \frac{9!}{3! 6!} \cdot 2^3 = \frac{9.8.7}{3.2} \cdot 2^3 = 672.$$

Example 8 The second, third and fourth terms in the binomial expansion $(x + a)^n$ are
240, 720 and 1080, respectively. Find $x$, $a$ and $n$.

Solution Given that second term $\text{T}_2 = 240$

<!-- page 233 -->
We have $\qquad \qquad \mathrm{T}_2 = {}^n\mathrm{C}_1 x^{n-1} \cdot a$

So $${}^{n}\mathrm{C}_{1}x^{n-1}$. $a = 240$ ... (1) \\ Similarly $^n\text{C}_2x^{n-2} a^2 = 720$ ... (2) \\ and$${}^{n}\mathrm{C}_{3}x^{n-3} a^{3} = 1080$ ... (3)

Dividing (2) by (1), we get

$$\frac{{}^nC_2x^{n-2}a^2}{{}^nC_1x^{n-1}a} = \frac{720}{240} \quad \text{i.e.,} \quad \frac{(n-1)!}{(n-2)!} \cdot \frac{a}{x} = 6$$

or $\frac{a}{x} = \frac{6}{(n-1)}$ ... (4)

Dividing (3) by (2), we have

$$\frac{a}{x} = \frac{9}{2(n-2)} \dots (5)$$

From (4) and (5),

$$\frac{6}{n-1} = \frac{9}{2(n-2)} \quad \text{Thus, } n = 5$$

Hence, from (1), $5x^4a = 240$, and from (4), $\frac{a}{x} = \frac{3}{2}$

Solving these equations for $a$ and $x$, we get $x = 2$ and $a = 3$.

Example 9 The coefficients of three consecutive terms in the expansion of $(1 + a)^n$
are in the ratio1: 7 : 42. Find $n$.

Solution Suppose the three consecutive terms in the expansion of $(1 + a)^n$ are
$(r - 1)^{\text{th}}$, $r^{\text{th}}$ and $(r + 1)^{\text{th}}$ terms.

The $(r-1)^{\text{th}}$ term is ${}^n\text{C}_{r-2} a^{r-2}$, and its coefficient is ${}^n\text{C}_{r-2}$. Similarly, the coefficients
of $r^{\text{th}}$ and $(r+1)^{\text{th}}$ terms are ${}^n\text{C}_{r-1}$ and ${}^n\text{C}_r$, respectively.

Since the coefficients are in the ratio $1 : 7 : 42$, so we have,

$$\frac{{}^nC_{r-2}}{{}^nC_{r-1}} = \frac{1}{7}, \text{ i.e., } n - 8r + 9 = 0 \qquad \dots (1)$$

and $$\frac{{}^nC_{r-1}}{{}^nC_r} = \frac{7}{42} \text{ , i.e., } n - 7r + 1 = 0 \quad \dots (2)$$

Solving equations(1) and (2), we get, $n = 55$.

<!-- page 234 -->
EXERCISE 8.2

Find the coefficient of

1. $x^5$ in $(x+3)^8$                                     2. $a^5b^7$ in $(a-2b)^{12}$.

Write the general term in the expansion of

3. $(x^2 - y)^6$                                   4. $(x^2 - yx)^{12}, x \neq 0.$

5. Find the $4^{\text{th}}$ term in the expansion of $(x-2y)^{12}$.

6. Find the $13^{\text{th}}$ term in the expansion of $\left(9x - \frac{1}{3\sqrt{x}}\right)^{18}$, $x \neq 0$.

Find the middle terms in the expansions of

7. $\left(3-\frac{x^3}{6}\right)^7$                                                                 8. $\left(\frac{x}{3}+9y\right)^{10}$

9. In the expansion of $(1+a)^{m+n}$, prove that coefficients of $a^m$ and $a^n$ are equal.

10. The coefficients of the $(r-1)^{\text{th}}$, $r^{\text{th}}$ and $(r+1)^{\text{th}}$ terms in the expansion of $(x+1)^n$
are in the ratio $1:3:5$. Find $n$ and $r$.

11. Prove that the coefficient of $x^n$ in the expansion of $(1+x)^{2n}$ is twice the coefficient
of $x^n$ in the expansion of $(1+x)^{2n-1}$.

12. Find a positive value of $m$ for which the coefficient of $x^2$ in the expansion
$(1+x)^m$ is 6.

Miscellaneous Examples

Example 10 Find the term independent of $x$ in the expansion of $\left( \frac{3}{2}x^2 - \frac{1}{3x} \right)^6$.


Solution We have $T_{r+1} = ^6C_r \left( \frac{3}{2}x^2 \right)^{6-r} \left( -\frac{1}{3x} \right)^r$


$$= ^6C_r \left( \frac{3}{2} \right)^{6-r} \left( x^2 \right)^{6-r} (-1)^r \left( \frac{1}{x} \right)^r \left( \frac{1}{3^r} \right)$$

<!-- page 235 -->
$$= (-1)^r \ ^6\text{C}_r \ \frac{(3)^{6-2r}}{(2)^{6-r}} \ x^{12-3r}$$

The term will be independent of $x$ if the index of $x$ is zero, i.e., $12 - 3r = 0$. Thus, $r = 4$

Hence $5^{\text{th}}$ term is independent of $x$ and is given by $(-1)^4 \ ^6\text{C}_4 \ \frac{(3)^{6-8}}{(2)^{6-4}} = \frac{5}{12}$.

Example 11 If the coefficients of $a^{r-1}$, $a^r$ and $a^{r+1}$ in the expansion of $(1+a)^n$ are in
arithmetic progression, prove that $n^2-n(4r+1)+4r^2-2=0$.

Solution The $(r+1)^{\text{th}}$ term in the expansion is $^n\text{C}_r a^r$. Thus it can be seen that $a^r$ occurs
in the $(r+1)^{\text{th}}$ term, and its coefficient is $^n\text{C}_r$. Hence the coefficients of $a^{r-1}$, $a^r$ and
$a^{r+1}$ are $^n\text{C}_{r-1}$, $^n\text{C}_r$ and $^n\text{C}_{r+1}$, respectively. Since these coefficients are in arithmetic
progression, so we have, $^n\text{C}_{r-1} + ^n\text{C}_{r+1} = 2$.$^n\text{C}_r$. This gives

$$\frac{n!}{(r-1)!(n-r+1)!} + \frac{n!}{(r+1)!(n-r-1)!} = 2 \times \frac{n!}{r!(n-r)!}$$

i.e. $$\frac{1}{(r-1)!(n-r+1)(n-r)(n-r-1)!} + \frac{1}{(r+1)(r)(r-1)!(n-r-1)!}$$

$$= 2 \times \frac{1}{r(r-1)!(n-r)(n-r-1)!}$$

or $\frac{1}{(r-1)!(n-r-1)!} \left[ \frac{1}{(n-r)(n-r+1)} + \frac{1}{(r+1)(r)} \right]$

$$= 2 \times \frac{1}{(r-1)! (n-r-1)![r(n-r)]}$$

i.e. $\frac{1}{(n-r+1)(n-r)} + \frac{1}{r(r+1)} = \frac{2}{r(n-r)},$

or $\frac{r(r+1)+(n-r)(n-r+1)}{(n-r)(n-r+1)r(r+1)}=\frac{2}{r(n-r)}$

or $r(r+1) + (n-r)(n-r+1) = 2(r+1)(n-r+1)$

or $r^2 + r + n^2 - nr + n - nr + r^2 - r = 2(nr - r^2 + r + n - r + 1)$

<!-- page 236 -->
or $n^2 - 4nr - n + 4r^2 - 2 = 0$
i.e., $n^2 - n (4r + 1) + 4r^2 - 2 = 0$

Example 12 Show that the coefficient of the middle term in the expansion of $(1+x)^{2n}$ is
equal to the sum of the coefficients of two middle terms in the expansion of $(1+x)^{2n-1}$.

Solution As $2n$ is even so the expansion $(1 + x)^{2n}$ has only one middle term which is

$$\left( \frac{2n}{2} + 1 \right)^{\text{th}} \quad \text{i.e., } (n + 1)^{\text{th}} \text{ term.}$$

The $(n+1)^{\text{th}}$ term is ${}^{2n}\text{C}_n x^n$. The coefficient of $x^n$ is ${}^{2n}\text{C}_n$
Similarly, $(2n-1)$ being odd, the other expansion has two middle terms,

$\left(\frac{2n-1+1}{2}\right)^{\text{th}}$ and $\left(\frac{2n-1+1}{2}+1\right)^{\text{th}}$ i.e., $n^{\text{th}}$ and $(n+1)^{\text{th}}$ terms. The coefficients of

these terms are $^{2n-1}\mathrm{C}_{n-1}$ and $^{2n-1}\mathrm{C}_{n}$, respectively.

Now

${}^{2n-1}\mathrm{C}_{n-1} + {}^{2n-1}\mathrm{C}_{n} = {}^{2n}\mathrm{C}_{n}$          [As ${}^{n}\mathrm{C}_{r-1} + {}^{n}\mathrm{C}_{r} = {}^{n+1}\mathrm{C}_{r}$]. as required.

Example 13 Find the coefficient of $a^4$ in the product $(1+2a)^4(2-a)^5$ using binomial
theorem.
Solution We first expand each of the factors of the given product using Binomial
Theorem. We have
$$(1+2a)^4 = ^4\text{C}_0 + ^4\text{C}_1(2a) + ^4\text{C}_2(2a)^2 + ^4\text{C}_3(2a)^3 + ^4\text{C}_4(2a)^4$$
$$= 1 + 4(2a) + 6(4a^2) + 4(8a^3) + 16a^4.$$
$$= 1 + 8a + 24a^2 + 32a^3 + 16a^4$$
and $(2-a)^5 = ^5\text{C}_0(2)^5 - ^5\text{C}_1(2)^4(a) + ^5\text{C}_2(2)^3(a)^2 - ^5\text{C}_3(2)^2(a)^3$
$$+ ^5\text{C}_4(2)(a)^4 - ^5\text{C}_5(a)^5$$
$$= 32 - 80a + 80a^2 - 40a^3 + 10a^4 - a^5$$
Thus $(1+2a)^4(2-a)^5$
$$= (1 + 8a + 24a^2 + 32a^3 + 16a^4)(32 - 80a + 80a^2 - 40a^3 + 10a^4 - a^5)$$
The complete multiplication of the two brackets need not be carried out. We write only
those terms which involve $a^4$. This can be done if we note that $a^r$. $a^{4-r} = a^4$. The terms
containing $a^4$ are
$1(10a^4) + (8a)(-40a^3) + (24a^2)(80a^2) + (32a^3)(-80a) + (16a^4)(32) = -438a^4$

<!-- page 237 -->
Thus, the coefficient of $a^4$ in the given product is $-438$.

Example 14 Find the $r^{\text{th}}$ term from the end in the expansion of $(x + a)^n$.

Solution There are $(n + 1)$ terms in the expansion of $(x + a)^n$. Observing the terms we
can say that the first term from the end is the last term, i.e., $(n + 1)^{\text{th}}$ term of the
expansion and $n + 1 = (n + 1) - (1 - 1)$. The second term from the end is the $n^{\text{th}}$ term
of the expansion, and $n = (n + 1) - (2 - 1)$. The third term from the end is the $(n - 1)^{\text{th}}$
term of the expansion and $n - 1 = (n + 1) - (3 - 1)$ and so on. Thus $r^{\text{th}}$ term from the
end will be term number $(n + 1) - (r - 1) = (n - r + 2)$ of the expansion. And the
$(n - r + 2)^{\text{th}}$ term is ${}^n\text{C}_{n - r + 1} x^{r - 1} a^{n - r + 1}$.

Example 15 Find the term independent of $x$ in the expansion of $\left( \sqrt[3]{x} + \frac{1}{2\sqrt[3]{x}} \right)^{18}, x > 0$.


Solution We have $T_{r+1} = {}^{18}C_r \left( \sqrt[3]{x} \right)^{18-r} \left( \frac{1}{2\sqrt[3]{x}} \right)^r$


$$= {}^{18}C_r x^{\frac{18-r}{3}} \cdot \frac{1}{2^r \cdot x^{\frac{r}{3}}} = {}^{18}C_r \frac{1}{2^r} \cdot x^{\frac{18-2r}{3}}$$


Since we have to find a term independent of $x$, i.e., term not having $x$, so take $\frac{18-2r}{3} = 0$.


We get $r = 9$. The required term is ${}^{18}C_9 \frac{1}{2^9}$.

We get $r = 9$. The required term is $^{18}\text{C}_9 \frac{1}{2^9}$.

Example 16 The sum of the coefficients of the first three terms in the expansion of
$$\left(x-\frac{3}{x^{2}}\right)^{m}, x \neq 0, m \text { being a natural number, is 559. Find the term of the expansion }$$
containing $x^{3}$.

Solution The coefficients of the first three terms of $\left(x-\frac{3}{x^{2}}\right)^{m}$ are ${ }^{m} \mathrm{C}_{0},(-3){ }^{m} \mathrm{C}_{1}$
and $9{ }^{m} \mathrm{C}_{2}$. Therefore, by the given condition, we have

${ }^{m} \mathrm{C}_{0}-3{ }^{m} \mathrm{C}_{1}+9{ }^{m} \mathrm{C}_{2}=559$, i.e., $1-3 m+\frac{9 m(m-1)}{2}=559$

<!-- page 238 -->
which gives $m = 12$ ($m$ being a natural number).

Now $\quad \mathrm{T}_{r+1}=\ ^{12}\mathrm{C}_{r}x^{12-r}\left(-\frac{3}{x^{2}}\right)^{r}=\ ^{12}\mathrm{C}_{r}(-3)^{r}\cdot x^{12-3r}$

Since we need the term containing $x^3$, so put $12 - 3r = 3$ i.e., $r = 3$.

Thus, the required term is ${}^{12}\mathrm{C}_3 (-3)^3 x^3$, i.e., $-5940 x^3$.

Example 17 If the coefficients of $(r-5)^{\text{th}}$ and $(2r-1)^{\text{th}}$ terms in the expansion of
$(1+x)^{34}$ are equal, find $r$.

Solution The coefficients of $(r-5)^{\text{th}}$ and $(2r-1)^{\text{th}}$ terms of the expansion $(1+x)^{34}$
are ${}^{34}\text{C}_{r-6}$ and ${}^{34}\text{C}_{2r-2}$, respectively. Since they are equal so ${}^{34}\text{C}_{r-6} = {}^{34}\text{C}_{2r-2}$

Therefore, either $r-6 = 2r-2$ or $r-6 = 34 - (2r-2)$

[Using the fact that if ${}^{n}\text{C}_{r} = {}^{n}\text{C}_{p}$, then either $r=p$ or $r=n-p$]

So, we get $r = -4$ or $r = 14$. $r$ being a natural number, $r = -4$ is not possible.
So, $r = 14$.

Miscellaneous Exercise on Chapter 8

1. Find $a, b$ and $n$ in the expansion of $(a + b)^n$ if the first three terms of the expansion
are 729, 7290 and 30375, respectively.
2. Find $a$ if the coefficients of $x^2$ and $x^3$ in the expansion of $(3 + ax)^9$ are equal.
3. Find the coefficient of $x^5$ in the product $(1 + 2x)^6 (1 - x)^7$ using binomial theorem.
4. If $a$ and $b$ are distinct integers, prove that $a - b$ is a factor of $a^n - b^n$, whenever
$n$ is a positive integer.
[Hint write $a^n = (a - b + b)^n$ and expand]

5. Evaluate $\left(\sqrt{3} + \sqrt{2}\right)^6 - \left(\sqrt{3} - \sqrt{2}\right)^6$ .

6. Find the value of $\left(a^2 + \sqrt{a^2 - 1}\right)^4 + \left(a^2 - \sqrt{a^2 - 1}\right)^4$ .

7. Find an approximation of $(0.99)^5$ using the first three terms of its expansion.
8. Find $n$, if the ratio of the fifth term from the beginning to the fifth term from the

end in the expansion of $\left(\sqrt[4]{2} + \frac{1}{\sqrt[4]{3}}\right)^n$ is $\sqrt{6} : 1$ .

<!-- page 239 -->
9. Expand using Binomial Theorem $\left(1 + \frac{x}{2} - \frac{2}{x}\right)^4, x \neq 0$.

10. Find the expansion of $(3x^2 - 2ax + 3a^2)^3$ using binomial theorem.

Summary

The expansion of a binomial for any positive integral $n$ is given by Binomial
Theorem, which is $(a + b)^n = {}^n\text{C}_0 a^n + {}^n\text{C}_1 a^{n-1} b + {}^n\text{C}_2 a^{n-2} b^2 + ... +$
${}^n\text{C}_{n-1} a . b^{n-1} + {}^n\text{C}_n b^n$.
The coefficients of the expansions are arranged in an array. This array is
called $Pascal's$ $triangle$.
The general term of an expansion $(a + b)^n$ is $\text{T}_{r+1} = {}^n\text{C}_r a^{n-r} . b^r$.

In the expansion $(a + b)^n$, if $n$ is even, then the middle term is the $\left( \frac{n}{2} + 1 \right)^{th}$

term.If $n$ is odd, then the middle terms are $\left( \frac{n+1}{2} \right)^{th}$ and $\left( \frac{n+1}{2} + 1 \right)^{th}$ terms.

Historical Note

The ancient Indian mathematicians knew about the coefficients in the
expansions of $(x + y)^n$, $0 \le n \le 7$. The arrangement of these coefficients was in
the form of a diagram called Meru-Prastara, provided by Pingla in his book
Chhanda shastra (200B.C.). This triangular arrangement is also found in the
work of Chinese mathematician Chu-shi-kie in 1303. The term binomial coefficients
was first introduced by the German mathematician, Michael Stipel (1486-1567) in
approximately 1544. Bombelli (1572) also gave the coefficients in the expansion of
$(a + b)^n$, for $n = 1,2 \dots,7$ and Oughtred (1631) gave them for $n = 1, 2, \dots, 10$. The
arithmetic triangle, popularly known as Pascal's triangle and similar to the MeruPrastara of Pingla was constructed by the French mathematician Blaise Pascal
(1623-1662) in 1665.
The present form of the binomial theorem for integral values of $n$ appeared in
Trate du triange arithmetic, written by Pascal and published posthumously in
1665.

<!-- page 240 -->
Chapter

SEQUENCES AND SERIES

$$\text{Natural numbers are the product of human spirit. } - \text{DEDEKIND}$$

9.1 Introduction

In mathematics, the word, “sequence” is used in much the
same way as it is in ordinary English. When we say that a
collection of objects is listed in a sequence, we usually mean
that the collection is ordered in such a way that it has an
identified first member, second member, third member and
so on. For example, population of human beings or bacteria
at different times form a sequence. The amount of money
deposited in a bank, over a number of years form a sequence.
Depreciated values of certain commodity occur in a
sequence. Sequences have important applications in several
spheres of human activities.

Fibonacci
(1175-1250)

Sequences, following specific patterns are called *progressions*. In previous class,
we have studied about *arithmetic progression* (A.P). In this Chapter, besides discussing
more about A.P.; *arithmetic mean*, *geometric mean*, *relationship between A.M.*
*and G.M.*, *special series in forms of sum to n terms of consecutive natural numbers*,
*sum to n terms of squares of natural numbers and sum to n terms of cubes of*
*natural numbers* will also be studied.

9.2 Sequences

Let us consider the following examples:

Assume that there is a generation gap of 30 years, we are asked to find the
number of ancestors, i.e., parents, grandparents, great grandparents, etc. that a person
might have over 300 years.

Here, the total number of generations $= \frac{300}{30} = 10$

<!-- page 241 -->
The number of person's ancestors for the first, second, third, ..., tenth generations are
2, 4, 8, 16, 32, ..., 1024. These numbers form what we call a $sequence$.

Consider the successive quotients that we obtain in the division of 10 by 3 at
different steps of division. In this process we get 3,3.3,3.33,3.333, ... and so on. These
quotients also form a sequence. The various numbers occurring in a sequence are
called its terms. We denote the terms of a sequence by $a_1, a_2, a_3, ..., a_n, ..., $ etc., the
subscripts denote the position of the term. The $n^{\text{th}}$ term is the number at the $n^{\text{th}}$ position
of the sequence and is denoted by $a_n$. The $n^{\text{th}}$ term is also called the general term of the
sequence.

Thus, the terms of the sequence of person's ancestors mentioned above are:

$$a_1 = 2, a_2 = 4, a_3 = 8, ..., a_{10} = 1024.$$

Similarly, in the example of successive quotients

$a_1 = 3, a_2 = 3.3, a_3 = 3.33, \dots, a_6 = 3.33333, \text{etc.}$

A sequence containing finite number of terms is called a finite sequence. For
example, sequence of ancestors is a finite sequence since it contains 10 terms (a fixed
number).

A sequence is called $infinite$, if it is not a finite sequence. For example, the
sequence of successive quotients mentioned above is an $infinite$ $sequence$, infinite in
the sense that it never ends.

Often, it is possible to express the rule, which yields the various terms of a sequence
in terms of algebraic formula. Consider for instance, the sequence of even natural
numbers $2, 4, 6, \dots$

Here $a_1 = 2 = 2 \times 1$ $a_2 = 4 = 2 \times 2$
$a_3 = 6 = 2 \times 3$ $a_4 = 8 = 2 \times 4$
.... .... .... .... .... ....
.... .... .... .... .... ....

$a_{23} = 46 = 2 \times 23$, $a_{24} = 48 = 2 \times 24$, and so on.

In fact, we see that the $n^{\text{th}}$ term of this sequence can be written as $a_n = 2n$,
where $n$ is a natural number. Similarly, in the sequence of odd natural numbers $1,3,5, \dots$,
the $n^{\text{th}}$ term is given by the formula, $a_n = 2n - 1$, where $n$ is a natural number.

In some cases, an arrangement of numbers such as 1, 1, 2, 3, 5, 8,... has no visible
pattern, but the sequence is generated by the recurrence relation given by

$$a_1 = a_2 = 1$$
$$a_3 = a_1 + a_2$$
$$a_n = a_{n-2} + a_{n-1}, n > 2$$

This sequence is called $Fibonacci$ $sequence$.

<!-- page 242 -->
In the sequence of primes $2,3,5,7,\dots$, we find that there is no formula for the $n^{\text{th}}$
prime. Such sequence can only be described by verbal description.

In every sequence, we should not expect that its terms will necessarily be given
by a specific formula. However, we expect a theoretical scheme or a rule for generating
the terms $a_1, a_2, a_3, \dots, a_n, \dots$ in succession.

In view of the above, a sequence can be regarded as a function whose domain
is the set of natural numbers or some subset of it. Sometimes, we use the functional
notation $a(n)$ for $a_n$.

9.3 Series

Let $a_1, a_2, a_3, \dots, a_n$, be a given sequence. Then, the expression

$$a_1 + a_2 + a_3 +, \dots + a_n + \dots$$

is called the $series$ $associated$ $with$ $the$ $given$ $sequence$ .The series is finite or infinite
according as the given sequence is finite or infinite. Series are often represented in

compact form, called $sigma$ $notation$, using the Greek letter $\sum$ (sigma) as means of
indicating the summation involved. Thus, the series $a_1 + a_2 + a_3 + ... + a_n$ is abbreviated

as $\sum_{k=1}^{n} a_{k}$ .

$\mathit{Remark}$ When the series is used, it refers to the indicated sum not to the sum itself.
For example, $1 + 3 + 5 + 7$ is a finite series with four terms. When we use the phrase
“$\mathit{sum\ of\ a\ series}$,” we will mean the number that results from adding the terms, the
sum of the series is 16.

We now consider some examples.

Example 1 Write the first three terms in each of the following sequences defined by
the following:

(i) $a_n = 2n + 5$,                                     (ii) $a_n = \frac{n-3}{4}$.

Solution (i) Here $a_n = 2n + 5$
Substituting $n = 1, 2, 3$, we get
$$a_1 = 2(1) + 5 = 7, a_2 = 9, a_3 = 11$$
Therefore, the required terms are 7, 9 and 11.

(ii) Here $a_n = \frac{n-3}{4}$. Thus, $a_1 = \frac{1-3}{4} = -\frac{1}{2}, a_2 = -\frac{1}{4}, a_3 = 0$

<!-- page 243 -->
Hence, the first three terms are $-\frac{1}{2}, -\frac{1}{4}$ and $0$.

Example 2 What is the $20^{\text{th}}$ term of the sequence defined by
$$a_n = (n - 1) (2 - n) (3 + n) ?$$

Solution Putting $n = 20$ , we obtain

$$a_{20} = (20 - 1) (2 - 20) (3 + 20)$$
$$= 19 \times (- 18) \times (23) = - 7866.$$

Example 3 Let the sequence $a_n$ be defined as follows:

$$a_1 = 1, \ a_n = a_{n-1} + 2 \text{ for } n \ge 2.$$

Find first five terms and write corresponding series.

Find first five terms and write corresponding series.

Solution We have

$a_1 = 1, a_2 = a_1 + 2 = 1 + 2 = 3, a_3 = a_2 + 2 = 3 + 2 = 5,$
$a_4 = a_3 + 2 = 5 + 2 = 7, a_5 = a_4 + 2 = 7 + 2 = 9.$

Hence, the first five terms of the sequence are 1,3,5,7 and 9. The corresponding series
is $1 + 3 + 5 + 7 + 9 +...$

EXERCISE 9.1

Write the first five terms of each of the sequences in Exercises 1 to 6 whose $n^{\text{th}}$
terms are:

1. $a_n = n (n + 2)$
2. $a_n = \frac{n}{n+1}$
3. $a_n = 2^n$

4. $a_n = \frac{2n-3}{6}$
5. $a_n = (-1)^{n-1} 5^{n+1}$
6. $a_n = n \frac{n^2+5}{4}$.

Find the indicated terms in each of the sequences in Exercises 7 to 10 whose $n^{\text{th}}$
terms are:


7. $a_n = 4n - 3; a_{17}, a_{24}$
8. $a_n = \frac{n^2}{2^n}; a_7$

9. $a_n = (-1)^{n-1} n^3; a_9$
10. $a_n = \frac{n(n-2)}{n+3}; a_{20}$.

<!-- page 244 -->
Write the first five terms of each of the sequences in Exercises 11 to 13 and obtain the
corresponding series:

11. $a_1 = 3, a_n = 3a_{n-1} + 2$ for all $n > 1$
12. $a_1 = -1, a_n = \frac{a_{n-1}}{n}, n \ge 2$

13. $a_1 = a_2 = 2, a_n = a_{n-1} - 1, n > 2$

14. The Fibonacci sequence is defined by

$$1 = a_1 = a_2 \text{ and } a_n = a_{n-1} + a_{n-2}, n > 2.$$

Find $\frac{a_{n+1}}{a_n}$, for $n = 1, 2, 3, 4, 5$

9.4 Arithmetic Progression (A.P.)

Let us recall some formulae and properties studied earlier.

A sequence $a_1, a_2, a_3, ..., a_n, ...$ is called *arithmetic sequence or arithmetic*
*progression* if $a_{n+1} = a_n + d, n \in \mathbf{N}$, where $a_1$ is called the *first term* and the constant
term $d$ is called the *common difference* of the A.P.

Let us consider an A.P. (in its standard form) with first term $a$ and common
difference $d$, i.e., $a, a + d, a + 2d, ...$

Then the $n^{\text{th}}$ term (general term) of the A.P. is $a_n = a + (n - 1) d$.

We can verify the following simple properties of an A.P. :

(i) If a constant is added to each term of an A.P., the resulting sequence is
also an A.P.
(ii) If a constant is subtracted from each term of an A.P., the resulting
sequence is also an A.P.
(iii) If each term of an A.P. is multiplied by a constant, then the resulting
sequence is also an A.P.
(iv) If each term of an A.P. is divided by a non-zero constant then the
resulting sequence is also an A.P.

Here, we shall use the following notations for an arithmetic progression:

$$a = \text{the first term, } l = \text{the last term, } d = \text{common difference,}$$

$$n = \text{ the number of terms.}$$

$\mathrm{S}_n =$ the sum to $n$ terms of A.P.

Let $a, a + d, a + 2d, ..., a + (n - 1) d$ be an A.P. Then

$$l = a + (n - 1) d$$

<!-- page 245 -->
$$S_n = \frac{n}{2} [2a + (n-1)d]$$

We can also write, $S_n = \frac{n}{2}[a+l]$

Let us consider some examples.

Example 4 In an A.P. if $m^{\text{th}}$ term is $n$ and the $n^{\text{th}}$ term is $m$, where $m \neq n$, find the $p$th
term.

Solution We have $a_m = a + (m - 1) d = n,$ ... (1)
and $a_n = a + (n - 1) d = m$ ... (2)
Solving (1) and (2), we get
$(m - n) d = n - m,$ or $d = -1,$ ... (3)
and $a = n + m - 1$ ... (4)
Therefore $a_p = a + (p - 1)d$
$= n + m - 1 + (p - 1) (-1) = n + m - p$
Hence, the $p^{\text{th}}$ term is $n + m - p.$

Hence, the $p^{\text{th}}$ term is $n + m - p$.

Example 5 If the sum of $n$ terms of an A.P. is $n\text{P} + \frac{1}{2}n(n-1)\text{Q}$ , where P and Q
are constants, find the common difference.
Solution Let $a_1, a_2, \dots a_n$ be the given A.P. Then

$$S_n = a_1 + a_2 + a_3 + \dots + a_{n-1} + a_n = n\text{P} + \frac{1}{2}n (n-1) \text{ Q}$$

Therefore $\quad S_1 = a_1 = \text{P}, S_2 = a_1 + a_2 = 2\text{P} + \text{Q}$
So that $\quad a_2 = S_2 - S_1 = \text{P} + \text{Q}$
Hence, the common difference is given by $d = a_2 - a_1 = (\text{P} + \text{Q}) - \text{P} = \text{Q}$.

Hence, the common difference is given by $d = a_2 - a_1 = (\mathrm{P} + \mathrm{Q}) - \mathrm{P} = \mathrm{Q}$.

Example 6 The sum of $n$ terms of two arithmetic progressions are in the ratio
$(3n + 8) : (7n + 15)$. Find the ratio of their $12^{\text{th}}$ terms.

Solution Let $a_1$, $a_2$ and $d_1$, $d_2$ be the first terms and common difference of the first
and second arithmetic progression, respectively. According to the given condition, we
have

$$\frac{\text{Sum ton terms of first A.P.}}{\text{Sum ton terms of second A.P.}} = \frac{3n+8}{7n+15}$$

<!-- page 246 -->
or $$\frac{\frac{n}{2}[2a_1+(n-1)d_1]}{\frac{n}{2}[2a_2+(n-1)d_2]}=\frac{3n+8}{7n+15}$$

or $\frac{2a_1+(n-1)d_1}{2a_2+(n-1)d_2}=\frac{3n+8}{7n+15}$ ... (1)

Now $\frac{12^{\text{th}}$ term of first A.P.}{12^{\text{th}}$ term of second A.P} = \frac{a_1 + 11d_1}{a_2 + 11d_2}$

$$\frac{2a_1+22d_1}{2a_2+22d_2} = \frac{3 \times 23+8}{7 \times 23+15} \qquad \text{[By putting } n = 23 \text{ in (1)]}$$

Therefore $\frac{a_1+11d_1}{a_2+11d_2} = \frac{12^{\text{th}} \text{ term of first A.P.}}{12^{\text{th}} \text{ term of second A.P.}} = \frac{7}{16}$

Hence, the required ratio is $7 : 16$.

Example 7 The income of a person is Rs. 3,00,000, in the first year and he receives an
increase of Rs.10,000 to his income per year for the next 19 years. Find the total
amount, he received in 20 years.

Solution Here, we have an A.P. with $a = 3,00,000$, $d = 10,000$, and $n = 20$.
Using the sum formula, we get,

$$S_{20} = \frac{20}{2} [600000 + 19 \times 10000] = 10 (790000) = 79,00,000.$$

Hence, the person received Rs. 79,00,000 as the total amount at the end of 20 years.

9.4.1 *Arithmetic mean* Given two numbers $a$ and $b$. We can insert a number A
between them so that $a, A, b$ is an A.P. Such a number A is called the *arithmetic mean*
(A.M.) of the numbers $a$ and $b$. Note that, in this case, we have

$$\mathrm{A} - a = b - \mathrm{A}, \quad \text{i.e., } \mathrm{A} = \frac{a+b}{2}$$

We may also interpret the A.M. between two numbers $a$ and $b$ as their
average $\frac{a+b}{2}$. For example, the A.M. of two numbers 4 and 16 is 10. We have, thus
constructed an A.P. 4, 10, 16 by inserting a number 10 between 4 and 16. The natural

<!-- page 247 -->
question now arises : Can we insert two or more numbers between given two numbers
so that the resulting sequence comes out to be an A.P. ? Observe that two numbers 8
and 12 can be inserted between 4 and 16 so that the resulting sequence 4, 8, 12, 16
becomes an A.P.

More generally, given any two numbers $a$ and $b$, we can insert as many numbers
as we like between them such that the resulting sequence is an A.P.

Let $\mathrm{A}_1, \mathrm{A}_2, \mathrm{A}_3, ..., \mathrm{A}_n$ be $n$ numbers between $a$ and $b$ such that $a, \mathrm{A}_1, \mathrm{A}_2, \mathrm{A}_3, ..., $
$\mathrm{A}_n, b$ is an A.P.

Here, $b$ is the $(n + 2)^{\text{th}}$ term, i.e., $b = a + [(n + 2) - 1]d = a + (n + 1) d.$

This gives $d = \frac{b-a}{n+1}$.

Thus, $n$ numbers between $a$ and $b$ are as follows:

$$A_1 = a + d = a + \frac{b-a}{n+1}$$

$$A_2 = a + 2d = a + \frac{2(b-a)}{n+1}$$

$$A_3 = a + 3d = a + \frac{3(b-a)}{n+1}$$

...... ...... ...... ......

...... ...... ...... ......

$$A_n = a + nd = a + \frac{n(b-a)}{n+1}$$

Example 8 Insert 6 numbers between 3 and 24 such that the resulting sequence is
an A.P.

Solution Let $A_1, A_2, A_3, A_4, A_5$ and $A_6$ be six numbers between 3 and 24 such that
$3, A_1, A_2, A_3, A_4, A_5, A_6, 24$ are in A.P. Here, $a = 3, b = 24, n = 8$.
Therefore, $24 = 3 + (8 - 1) d$, so that $d = 3$.
Thus $A_1 = a + d = 3 + 3 = 6$; $A_2 = a + 2d = 3 + 2 \times 3 = 9$;
$A_3 = a + 3d = 3 + 3 \times 3 = 12$; $A_4 = a + 4d = 3 + 4 \times 3 = 15$;
$A_5 = a + 5d = 3 + 5 \times 3 = 18$; $A_6 = a + 6d = 3 + 6 \times 3 = 21$.

Hence, six numbers between 3 and 24 are 6, 9, 12, 15, 18 and 21.

Hence, six numbers between 3 and 24 are 6, 9, 12, 15, 18 and 21.

<!-- page 248 -->
EXERCISE 9.2

1. Find the sum of odd integers from 1 to 2001.
2. Find the sum of all natural numbers lying between 100 and 1000, which are multiples of 5.
3. In an A.P., the first term is 2 and the sum of the first five terms is one-fourth of the next five terms. Show that $20^{\text{th}}$ term is $-112$.
4. How many terms of the A.P. $-6$, $-\frac{11}{2}$, $-5$, ... are needed to give the sum $-25$?

5. In an A.P., if $p^{\text{th}}$ term is $\frac{1}{q}$ and $q^{\text{th}}$ term is $\frac{1}{p}$, prove that the sum of first $pq$ terms is $\frac{1}{2}(pq+1)$, where $p \neq q$.
6. If the sum of a certain number of terms of the A.P. 25, 22, 19, ... is 116. Find the last term.
7. Find the sum to $n$ terms of the A.P., whose $k^{\text{th}}$ term is $5k+1$.
8. If the sum of $n$ terms of an A.P. is $(pn+qn^2)$, where $p$ and $q$ are constants, find the common difference.
9. The sums of $n$ terms of two arithmetic progressions are in the ratio $5n+4:9n+6$. Find the ratio of their $18^{\text{th}}$ terms.
10. If the sum of first $p$ terms of an A.P. is equal to the sum of the first $q$ terms, then find the sum of the first $(p+q)$ terms.
11. Sum of the first $p$, $q$ and $r$ terms of an A.P. are $a$, $b$ and $c$, respectively.

Prove that $\frac{a}{p}(q-r)+\frac{b}{q}(r-p)+\frac{c}{r}(p-q)=0$
12. The ratio of the sums of $m$ and $n$ terms of an A.P. is $m^2:n^2$. Show that the ratio of $m^{\text{th}}$ and $n^{\text{th}}$ term is $(2m-1):(2n-1)$.
13. If the sum of $n$ terms of an A.P. is $3n^2+5n$ and its $m^{\text{th}}$ term is 164, find the value of $m$.
14. Insert five numbers between 8 and 26 such that the resulting sequence is an A.P.

15. If $\frac{a^n+b^n}{a^{n-1}+b^{n-1}}$ is the A.M. between $a$ and $b$, then find the value of $n$.
16. Between 1 and 31, $m$ numbers have been inserted in such a way that the resulting sequence is an A. P. and the ratio of $7^{\text{th}}$ and $(m-1)^{\text{th}}$ numbers is $5:9$. Find the value of $m$.

<!-- page 249 -->
17. A man starts repaying a loan as first instalment of Rs. 100. If he increases the
instalment by Rs 5 every month, what amount he will pay in the $30^{\text{th}}$ instalment?
18. The difference between any two consecutive interior angles of a polygon is $5^{\circ}$.
If the smallest angle is $120^{\circ}$, find the number of the sides of the polygon.

9.5 Geometric Progression (G. P.)

Let us consider the following sequences:

(i) 2,4,8,16,..., (ii) $\frac{1}{9}$, $\frac{-1}{27}$, $\frac{1}{81}$, $\frac{-1}{243}$ ... (iii) .01,.0001,.000001,...

In each of these sequences, how their terms progress? We note that each term, except
the first progresses in a definite order.

In (i), we have $a_1 = 2$, $\frac{a_2}{a_1} = 2$, $\frac{a_3}{a_2} = 2$, $\frac{a_4}{a_3} = 2$ and so on.

In (ii), we observe, $a_1 = \frac{1}{9}$, $\frac{a_2}{a_1} = \frac{1}{3}$, $\frac{a_3}{a_2} = \frac{1}{3}$, $\frac{a_4}{a_3} = \frac{1}{3}$ and so on.

Similarly, state how do the terms in (iii) progress? It is observed that in each case,
every term except the first term bears a constant ratio to the term immediately preceding
it. In (i), this constant ratio is 2; in (ii), it is $-\frac{1}{3}$ and in (iii), the constant ratio is 0.01.
Such sequences are called *geometric sequence* or *geometric progression* abbreviated
as GP.

A sequence $a_1, a_2, a_3, ..., a_n, ...$ is called \textit{geometric progression}, if each term is

$\rightarrow$ For the $k \geq 1$ and $k \geq 2$ periods, the $k$th order polynomial is $k+1$ and $k+2$ periods.

By letting $a_1 = a$, we obtain a geometric progression, $a, ar, ar^2, ar^3, .....$, where $a$
is called the *first term* and $r$ is called the *common ratio* of the G.P. Common ratio in
geometric progression (i), (ii) and (iii) above are 2, $\frac{1}{3}$ and 0.01, respectively.

As in case of arithmetic progression, the problem of finding the $n^{\text{th}}$ term or sum of $n$
terms of a geometric progression containing a large number of terms would be difficult
without the use of the formulae which we shall develop in the next Section. We shall
use the following notations with these formulae:

$a =$ the first term, $r =$ the common ratio, $l =$ the last term,

$$n = \text{the numbers of terms,}$$

<!-- page 250 -->
$$n = \text{the numbers of terms,}$$

$$\text{S}_n = \text{the sum of first } n \text{ terms.}$$

9.5.1 General term of a G.P. Let us consider a G.P. with first non-zero term ‘$a$’ and
common ratio ‘$r$’. Write a few terms of it. The second term is obtained by multiplying
$a$ by $r$, thus $a_2 = ar$. Similarly, third term is obtained by multiplying $a_2$ by $r$. Thus,
$a_3 = a_2r = ar^2$, and so on.

We write below these and few more terms.

$1^{\text{st}} \text{ term } = a_1 = a = ar^{1-1}, 2^{\text{nd}} \text{ term } = a_2 = ar = ar^{2-1}, 3^{\text{rd}} \text{ term } = a_3 = ar^2 = ar^{3-1}$
$4^{\text{th}} \text{ term } = a_4 = ar^3 = ar^{4-1}, 5^{\text{th}} \text{ term } = a_5 = ar^4 = ar^{5-1}$

Do you see a pattern? What will be $16^{\text{th}}$ term?

$$a_{16} = ar^{16-1} = ar^{15}$$

Therefore, the pattern suggests that the $n^{\text{th}}$ term of a G.P. is given by
$$a_n = ar^{n-1}.$$

Thus, $a$, G.P. can be written as $a, ar, ar^2, ar^3, ... ar^{n-1}; a, ar, ar^2,...,ar^{n-1} ...$;according
as G.P. is $finite$ or $infinite$, respectively.

The series $a + ar + ar^2 + ... + ar^{n-1}$ or $a + ar + ar^2 + ... + ar^{n-1} +...$are called
finite or infinite geometric series, respectively.

9.5.2. Sum to $n$ terms of a G.P. Let the first term of a G.P. be $a$ and the common
ratio be $r$. Let us denote by $\mathrm{S}_n$ the sum to first $n$ terms of G.P. Then

$$S_n = a + ar + ar^2 + ... + ar^{n-1} \dots (1)$$

Case 1 If $r = 1$, we have $S_n = a + a + a + ... + a (n \text{ terms}) = na$

Case 2 If $r \neq 1$, multiplying (1) by $r$, we have
$$rS_n = ar + ar^2 + ar^3 + ... + ar^n \quad ... (2)$$

Subtracting (2) from (1), we get $(1 - r) S_n = a - ar^n = a(1 - r^n)$

This gives $S_n = \frac{a(1-r^n)}{1-r}$ or $S_n = \frac{a(r^n-1)}{r-1}$

Example 9 Find the $10^{\text{th}}$ and $n^{\text{th}}$ terms of the G.P. 5, 25,125,... .

Solution Here $a = 5$ and $r = 5$. Thus, $a_{10} = 5(5)^{10-1} = 5(5)^9 = 5^{10}$
and $a_n = ar^{n-1} = 5(5)^{n-1} = 5^n$.

Example10 Which term of the G.P., 2,8,32, ... up to $n$ terms is 131072?

Solution Let $131072$ be the $n^{\text{th}}$ term of the given G.P. Here $a = 2$ and $r = 4$.
Therefore $131072 = a_n = 2(4)^{n-1}$ or $65536 = 4^{n-1}$
This gives $4^8 = 4^{n-1}$.
So that $n - 1 = 8$, i.e., $n = 9$. Hence, $131072$ is the $9^{\text{th}}$ term of the G.P.

<!-- page 251 -->
Example11 In a G.P., the $3^{\text{rd}}$ term is 24 and the $6^{\text{th}}$ term is 192.Find the $10^{\text{th}}$ term.
Solution Here, $a_3 = ar^2 = 24$ ... (1)
and $a_6 = ar^5 = 192$ ... (2)
Dividing (2) by (1), we get $r = 2$. Substituting $r = 2$ in (1), we get $a = 6$.
Hence $a_{10} = 6$ $(2)^9 = 3072$.

Example12 Find the sum of first $n$ terms and the sum of first 5 terms of the geometric


series $1 + \frac{2}{3} + \frac{4}{9} + \dots$


Solution Here $a = 1$ and $r = \frac{2}{3}$. Therefore


$$S_n = \frac{a \left( 1 - r^n \right)}{1 - r} = \frac{\left[ 1 - \left( \frac{2}{3} \right)^n \right]}{1 - \frac{2}{3}} = 3 \left[ 1 - \left( \frac{2}{3} \right)^n \right]$$


In particular, $S_5 = 3 \left[ 1 - \left( \frac{2}{3} \right)^5 \right] = 3 \times \frac{211}{243} = \frac{211}{81}$.

Example 13 How many terms of the G.P. $3, \frac{3}{2}, \frac{3}{4}, ...$ are needed to give the

sum $\frac{3069}{512}$ ?

Solution Let $n$ be the number of terms needed. Given that $a = 3, r = \frac{1}{2}$ and $S_n = \frac{3069}{512}$

Since $S_n = \frac{a \left( 1 - r^n \right)}{1 - r}$

Therefore $\frac{3069}{512} = \frac{3 \left( 1 - \frac{1}{2^n} \right)}{1 - \frac{1}{2}} = 6 \left( 1 - \frac{1}{2^n} \right)$

<!-- page 252 -->
or $\frac{3069}{3072} = 1 - \frac{1}{2^n}$

or $$\frac{1}{2^n} = 1 - \frac{3069}{3072} = \frac{3}{3072} = \frac{1}{1024}$$

or $2^n = 1024 = 2^{10}$, which gives $n = 10$.

Example 14 The sum of first three terms of a G.P. is $\frac{13}{12}$ and their product is $-1$.

Find the common ratio and the terms.

Solution Let $\frac{a}{r}$, $a$, $ar$ be the first three terms of the G.P. Then

$$\frac{a}{r} + ar + a = \frac{13}{12} \qquad \dots (1)$$

and $\left(\frac{a}{r}\right)(a)(ar)=-1$ ... (2)

From (2), we get $a^3 = -1$, i.e., $a = -1$ (considering only real roots)

Substituting $a = -1$ in (1), we have

$$-\frac{1}{r}-1-r=\frac{13}{12} \text{ or } 12r^2+25r+12=0.$$

This is a quadratic in $r$, solving, we get $r = -\frac{3}{4}$ or $-\frac{4}{3}$.

Thus, the three terms of G.P. are : $\frac{4}{3}$, $-1$, $\frac{3}{4}$ for $r = \frac{-3}{4}$ and $\frac{3}{4}$, $-1$, $\frac{4}{3}$ for $r = \frac{-4}{3}$,

Example15 Find the sum of the sequence 7, 77, 777, 7777, ... to $n$ terms.

Solution This is not a G.P., however, we can relate it to a G.P. by writing the terms as

$$S_n = 7 + 77 + 777 + 7777 + ... \text{ to } n \text{ terms}$$

$$= \frac{7}{9} [9 + 99 + 999 + 9999 + ... \text{ to } n \text{ term}]$$

$$= \frac{7}{9} [(10 - 1) + (10^2 - 1) + (10^3 - 1) + (10^4 - 1) + ... n \text{ terms}]$$

<!-- page 253 -->
$$= \frac{7}{9} [(10 + 10^2 + 10^3 + ... n \text{ terms}) - (1 + 1 + 1 + ... n \text{ terms})]$$

$$= \frac{7}{9} \left[ \frac{10(10^n - 1)}{10 - 1} - n \right] = \frac{7}{9} \left[ \frac{10(10^n - 1)}{9} - n \right] .$$

Example 16 A person has 2 parents, 4 grandparents, 8 great grandparents, and so on.
Find the number of his ancestors during the ten generations preceding his own.

Solution Here $a = 2$, $r = 2$ and $n = 10$

Using the sum formula $S_n = \frac{a (r^n - 1)}{r - 1}$

We have $S_{10} = 2(2^{10} - 1) = 2046$

Hence, the number of ancestors preceding the person is 2046.

9.5.3 *Geometric Mean (G.M.)* The geometric mean of two positive numbers $a$

and $b$ is the number $\sqrt{ab}$. Therefore, the geometric mean of 2 and 8 is 4. We
observe that the three numbers 2,4,8 are consecutive terms of a G.P. This leads to a
generalisation of the concept of geometric means of two numbers.

Given any two positive numbers $a$ and $b$, we can insert as many numbers as
we like between them to make the resulting sequence in a G.P.

Let $G_1, G_2,...., G_n$ be $n$ numbers between positive numbers $a$ and $b$ such that
$a,G_1,G_2,G_3,...,G_n,b$ is a G.P. Thus, $b$ being the $(n + 2)^{\text{th}}$ term,we have

$$b = ar^{n+1}, \quad \text{or} \quad r = \left( \frac{b}{a} \right)^{\frac{1}{n+1}}.$$

Hence $\quad \mathrm{G}_{1}=a r=a\left(\frac{b}{a}\right)^{\frac{1}{n+1}}, \quad \mathrm{G}_{2}=a r^{2}=a\left(\frac{b}{a}\right)^{\frac{2}{n+1}}, \quad \mathrm{G}_{3}=a r^{3}=a\left(\frac{b}{a}\right)^{\frac{3}{n+1}},$

$$G_n = ar^n = a \left( \frac{b}{a} \right)^{\frac{n}{n+1}}$$

Example17 Insert three numbers between 1 and 256 so that the resulting sequence
is a G.P.
Solution Let $\text{G}_1$, $\text{G}_2$,$\text{G}_3$ be three numbers between 1 and 256 such that
1, $\text{G}_1$,$\text{G}_2$,$\text{G}_3$ ,256 is a G.P.

<!-- page 254 -->
Therefore      $256 = r^4$ giving $r = \pm 4$ (Taking real roots only)

For $r = 4$, we have $\mathrm{G}_1 = ar = 4$, $\mathrm{G}_2 = ar^2 = 16$, $\mathrm{G}_3 = ar^3 = 64$

Similarly, for $r = -4$, numbers are $-4, 16$ and $-64$.

Hence, we can insert 4, 16, 64 between 1 and 256 so that the resulting sequences are
in G.P.

9.6 Relationship Between A.M. and G.M.

Let A and G be A.M. and G.M. of two given positive real numbers $a$ and $b$, respectively.
Then

$$\mathrm{A} = \frac{a+b}{2} \quad \text{and} \quad \mathrm{G} = \sqrt{ab}$$

Thus, we have

$$A - G = \frac{a+b}{2} - \sqrt{ab} = \frac{a+b-2\sqrt{ab}}{2}$$

$$= \frac{(\sqrt{a}-\sqrt{b})^2}{2} \geq 0 \quad \dots (1)$$

From (1), we obtain the relationship $A \geq G$.

Example 18 If A.M. and G.M. of two positive numbers $a$ and $b$ are 10 and 8,
respectively, find the numbers.

Solution Given that      A.M. $=\frac{a+b}{2}=10$                               ... (1)

and                     G.M. $=\sqrt{ab}=8$                               ... (2)

From (1) and (2), we get
$$a+b=20$$                               ... (3)
$$ab=64$$                               ... (4)

Putting the value of $a$ and $b$ from (3), (4) in the identity $(a-b)^2 = (a+b)^2 - 4ab$,
we get
$$(a-b)^2 = 400 - 256 = 144$$
or                     $$a-b = \pm 12$$
... (5)

Solving (3) and (5), we obtain
$$a=4, b=16 \text{ or } a=16, b=4$$

Thus, the numbers $a$ and $b$ are 4, 16 or 16, 4 respectively.

Thus, the numbers $a$ and $b$ are $4$, $16$ or $16$, $4$ respectively.

<!-- page 255 -->
EXERCISE 9.3

1. Find the $20^{th}$ and $n^{th}$ terms of the G.P. $\frac{5}{2}, \frac{5}{4}, \frac{5}{8}, ...$

2. Find the $12^{th}$ term of a G.P. whose $8^{th}$ term is 192 and the common ratio is 2.
3. The $5^{th}, 8^{th}$ and $11^{th}$ terms of a G.P. are $p, q$ and $s$, respectively. Show
that $q^2 = ps$.
4. The $4^{th}$ term of a G.P. is square of its second term, and the first term is $-3$.
Determine its $7^{th}$ term.
5. Which term of the following sequences:
(a) $2, 2\sqrt{2}, 4, ...$ is 128 ? (b) $\sqrt{3}, 3, 3\sqrt{3}, ...$ is 729 ?

(c) $\frac{1}{3}, \frac{1}{9}, \frac{1}{27}, ...$ is $\frac{1}{19683}$ ?

6. For what values of $x$, the numbers $-\frac{2}{7}, x, -\frac{7}{2}$ are in G.P.?
Find the sum to indicated number of terms in each of the geometric progressions in
Exercises 7 to 10:
7. $0.15, 0.015, 0.0015, ...$ 20 terms.
8. $\sqrt{7}, \sqrt{21}, 3\sqrt{7}, ...$ $n$ terms.
9. $1, -a, a^2, -a^3, ...$ $n$ terms (if $a \neq -1$).
10. $x^3, x^5, x^7, ...$ $n$ terms (if $x \neq \pm 1$).

11. Evaluate $\sum_{k=1}^{11} (2 + 3^k)$

12. The sum of first three terms of a G.P. is $\frac{39}{10}$ and their product is 1. Find the
common ratio and the terms.
13. How many terms of G.P. $3, 3^2, 3^3, ...$ are needed to give the sum 120?
14. The sum of first three terms of a G.P. is 16 and the sum of the next three terms is
128. Determine the first term, the common ratio and the sum to $n$ terms of the G.P.
15. Given a G.P. with $a = 729$ and $7^{th}$ term 64, determine $S_7$.
16. Find a G.P. for which sum of the first two terms is $-4$ and the fifth term is
4 times the third term.
17. If the $4^{th}, 10^{th}$ and $16^{th}$ terms of a G.P. are $x, y$ and $z$, respectively. Prove that $x,$
$y, z$ are in G.P.

<!-- page 256 -->
18. Find the sum to $n$ terms of the sequence, 8, 88, 888, 8888....

19. Find the sum of the products of the corresponding terms of the sequences 2, 4, 8,

16, 32 and 128, 32, 8, 2, $\frac{1}{2}$.

20. Show that the products of the corresponding terms of the sequences $a, ar, ar^2,$
$...ar^{n-1}$ and A, AR, AR$^2, ...$ AR$^{n-1}$ form a G.P, and find the common ratio.

21. Find four numbers forming a geometric progression in which the third term is
greater than the first term by 9, and the second term is greater than the $4^{\text{th}}$ by 18.

22. If the $p^{\text{th}}$, $q^{\text{th}}$ and $r^{\text{th}}$ terms of a G.P. are $a$, $b$ and $c$, respectively. Prove that

$$a^{q-r} b^{r-p} c^{p-q} = 1.$$

23. If the first and the $n^{\text{th}}$ term of a G.P. are $a$ and $b$, respectively, and if P is the
product of $n$ terms, prove that $\text{P}^2 = (ab)^n$.

24. Show that the ratio of the sum of first $n$ terms of a G.P. to the sum of terms from


$(n+1)^{\text{th}}$ to $(2n)^{\text{th}}$ term is $\frac{1}{r^n}$.

25. If $a$, $b$, $c$ and $d$ are in G.P. show that
$$(a^2 + b^2 + c^2) (b^2 + c^2 + d^2) = (ab + bc + cd)^2 .$$

26. Insert two numbers between 3 and 81 so that the resulting sequence is G.P.

27. Find the value of $n$ so that $\frac{a^{n+1} + b^{n+1}}{a^n + b^n}$ may be the geometric mean between
$a$ and $b$.

28. The sum of two numbers is 6 times their geometric mean, show that numbers

are in the ratio $(3+2\sqrt{2}):(3-2\sqrt{2})$.

29. If A and G be A.M. and G.M., respectively between two positive numbers,

prove that the numbers are $A \pm \sqrt{(A+G)(A-G)}$.

30. The number of bacteria in a certain culture doubles every hour. If there were 30
bacteria present in the culture originally, how many bacteria will be present at the
end of $2^{\text{nd}}$ hour, $4^{\text{th}}$ hour and $n^{\text{th}}$ hour ?

31. What will Rs 500 amounts to in 10 years after its deposit in a bank which pays
annual interest rate of $10\%$ compounded annually?

32. If A.M. and G.M. of roots of a quadratic equation are 8 and 5, respectively, then
obtain the quadratic equation.

<!-- page 257 -->
9.7 Sum to $n$ Terms of Special Series

We shall now find the sum of first $n$ terms of some special series, namely;

(i) $1 + 2 + 3 +... \quad + n$ (sum of first $n$ natural numbers)
(ii) $1^2 + 2^2 + 3^2 +... + n^2$(sum of squares of the first $n$ natural numbers)
(iii) $1^3 + 2^3 + 3^3 +... + n^3$(sum of cubes of the first $n$ natural numbers).

Let us take them one by one.

(i) $S_n=1 + 2 + 3 + \ldots + n$, then $S_n = \frac{n (n+1)}{2}$ (See Section 9.4)
(ii) Here $S_n = 1^2 + 2^2 + 3^2 + \ldots + n^2$

We consider the identity $k^3 - (k - 1)^3 = 3k^2 - 3k + 1$

Putting $k = 1, 2..., n$ successively, we obtain

$1^3 - 0^3 = 3 (1)^2 - 3 (1) + 1$
$2^3 - 1^3 = 3 (2)^2 - 3 (2) + 1$
$3^3 - 2^3 = 3(3)^2 - 3 (3) + 1$
........................................................
........................................................
........................................................
$n^3 - (n - 1)^3 = 3 (n)^2 - 3 (n) + 1$

Adding both sides, we get

$$n^3 - 0^3 = 3 (1^2 + 2^2 + 3^2 + ... + n^2) - 3 (1 + 2 + 3 + ... + n) + n$$

$$n^3 = 3 \sum_{k=1}^{n} k^2 - 3 \sum_{k=1}^{n} k + n$$

By (i), we know that $\sum_{k=1}^{n} k=1+2+3+\ldots+n=\frac{n(n+1)}{2}$

Hence $S_n = \sum_{k=1}^n k^2 = \frac{1}{3} \left[ n^3 + \frac{3n(n+1)}{2} - n \right] = \frac{1}{6} (2n^3 + 3n^2 + n)$
$= \frac{n(n+1)(2n+1)}{6}$

(iii) Here $S_n = 1^3 + 2^3 + ...+n^3$

We consider the identity, $(k+1)^4 - k^4 = 4k^3 + 6k^2 + 4k + 1$
Putting $k = 1, 2, 3 \dots n$, we get

<!-- page 258 -->
$$2^4 - 1^4 = 4(1)^3 + 6(1)^2 + 4(1) + 1$$
$$3^4 - 2^4 = 4(2)^3 + 6(2)^2 + 4(2) + 1$$
$$4^4 - 3^4 = 4(3)^3 + 6(3)^2 + 4(3) + 1$$

$$................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................$$

$$(n-1)^4 - (n-2)^4 = 4(n-2)^3 + 6(n-2)^2 + 4(n-2) + 1$$
$$n^4 - (n-1)^4 = 4(n-1)^3 + 6(n-1)^2 + 4(n-1) + 1$$
$$(n+1)^4 - n^4 = 4n^3 + 6n^2 + 4n + 1$$

Adding both sides, we get

$$(n+1)^4 - 1^4 = 4(1^3 + 2^3 + 3^3 + ... + n^3) + 6(1^2 + 2^2 + 3^2 + ... + n^2) +$$
$$4(1 + 2 + 3 + ... + n) + n$$

$$= 4 \sum_{k=1}^{n} k^{3} + 6 \sum_{k=1}^{n} k^{2} + 4 \sum_{k=1}^{n} k + n \dots (1)$$

From parts (i) and (ii), we know that

$$\sum_{k=1}^{n} k = \frac{n(n+1)}{2} \quad \text{and} \quad \sum_{k=1}^{n} k^2 = \frac{n(n+1)(2n+1)}{6}$$

Putting these values in equation (1), we obtain

$$4 \sum_{k=1}^{n} k^{3}=n^{4}+4 n^{3}+6 n^{2}+4 n-\frac{6 n(n+1)(2 n+1)}{6}-\frac{4 n(n+1)}{2}-n$$

or $4\mathrm{S}_n = n^4 + 4n^3 + 6n^2 + 4n - n (2n^2 + 3n + 1) - 2n (n + 1) - n$
$= n^4 + 2n^3 + n^2$
$= \quad n^2(n + 1)^2.$

Hence, $S_{n}=\frac{n^{2}(n+1)^{2}}{4}=\frac{[n(n+1)]^{2}}{4}$

Example 19 Find the sum to $n$ terms of the series: $5 + 11 + 19 + 29 + 41...$

Solution Let us write
$$S_n = 5 + 11 + 19 + 29 + ... + a_{n-1} + a_n$$
or $$S_n = \quad 5 + 11 + 19 + ... + a_{n-2} + a_{n-1} + a_n$$
On subtraction, we get

<!-- page 259 -->
$$0 = 5 + [6 + 8 + 10 + 12 + ...(n - 1) \text{ terms}] - a_n$$

or $a_n = 5 + \frac{(n-1)[12+(n-2)\times 2]}{2}$
$= 5 + (n-1)(n+4) = n^2 + 3n + 1$

Hence $S_n = \sum_{k=1}^n a_k = \sum_{k=1}^n (k^2 + 3k + 1) = \sum_{k=1}^n k^2 + 3 \sum_1^n k + n$

$= \frac{n(n+1)(2n+1)}{6} + \frac{3n(n+1)}{2} + n = \frac{n(n+2)(n+4)}{3}.$

Example 20 Find the sum to $n$ terms of the series whose $n^{th}$ term is $n$ $(n+3)$.

Solution Given that $a_{n}=n(n+3)=n^{2}+3n$

Thus, the sum to $n$ terms is given by

$$S_{n}=\sum_{k=1}^{n} a_{k}=\sum_{k=1}^{n} k^{2}+3 \sum_{k=1}^{n} k$$

$$=\frac{n(n+1)(2 n+1)}{6}+\frac{3 n(n+1)}{2}=\frac{n(n+1)(n+5)}{3}$$

EXERCISE 9.4

Find the sum to $n$ terms of each of the series in Exercises 1 to 7.

1. $1 \times 2 + 2 \times 3 + 3 \times 4 + 4 \times 5 + \dots$    2. $1 \times 2 \times 3 + 2 \times 3 \times 4 + 3 \times 4 \times 5 + \dots$

3. $3 \times 1^2 + 5 \times 2^2 + 7 \times 3^2 + \dots$    4. $\frac{1}{1 \times 2} + \frac{1}{2 \times 3} + \frac{1}{3 \times 4} + \dots$

5. $5^2 + 6^2 + 7^2 + \dots + 20^2$    6. $3 \times 8 + 6 \times 11 + 9 \times 14 + \dots$

7. $1^2 + (1^2 + 2^2) + (1^2 + 2^2 + 3^2) + \dots$

Find the sum to $n$ terms of the series in Exercises 8 to 10 whose $n^{\text{th}}$ terms is given by

8. $n(n+1)(n+4)$.                                        9. $n^2 + 2^n$

10. $(2n-1)^2$

<!-- page 260 -->
Miscellaneous Examples

Example21 If $p^{\text{th}}$, $q^{\text{th}}$, $r^{\text{th}}$ and $s^{\text{th}}$ terms of an A.P. are in G.P, then show that
$(p-q), (q-r), (r-s)$ are also in G.P.

Solution Here

$$a_p = a + (p - 1) d \hfill ... (1)$$
$$a_q = a + (q - 1) d \hfill ... (2)$$

$$a_r = a + (r - 1) d \qquad \dots (3)$$

$$a_s = a + (s - 1) d \quad \dots (4)$$

Given that $a_p$, $a_q$, $a_r$ and $a_s$ are in G.P.

So $$\frac{a_q}{a_p} = \frac{a_r}{a_q} = \frac{a_q - a_r}{a_p - a_q} = \frac{q - r}{p - q} \text{ (why ?)} \quad \dots (5)$$

Similarly $\frac{a_r}{a_q} = \frac{a_s}{a_r} = \frac{a_r - a_s}{a_q - a_r} = \frac{r - s}{q - r}$ (why ?) ... (6)

Hence, by (5) and (6)

$\frac{q-r}{p-q} = \frac{r-s}{q-r}$, i.e., $p-q$, $q-r$ and $r-s$ are in G.P.

Example 22 If $a, b, c$ are in G.P. and $a^{\frac{1}{x}} = b^{\frac{1}{y}} = c^{\frac{1}{z}}$, prove that $x, y, z$ are in A.P.


Solution Let $a^{\frac{1}{x}} = b^{\frac{1}{y}} = c^{\frac{1}{z}} = k$ Then
$$a = k^x, b = k^y \text{ and } c = k^z. \dots (1)$$
Since $a, b, c$ are in G.P., therefore,
$$b^2 = ac \dots (2)$$
Using (1) in (2), we get
$$k^{2y} = k^{x+z}, \text{ which gives } 2y = x + z.$$
Hence, $x, y$ and $z$ are in A.P.

Hence, $x$, $y$ and $z$ are in A.P.

Example 23 If $a, b, c, d$ and $p$ are different real numbers such that
$(a^2 + b^2 + c^2)p^2 - 2(ab + bc + cd) p + (b^2 + c^2 + d^2) \le 0$, then show that $a, b, c$ and $d$
are in G.P.

Solution Given that
$$(a^2 + b^2 + c^2) p^2 - 2 (ab + bc + cd) p + (b^2 + c^2 + d^2) \le 0 \quad \dots (1)$$

<!-- page 261 -->
But L.H.S.

$$= (a^2p^2 - 2abp + b^2) + (b^2p^2 - 2bcp + c^2) + (c^2p^2 - 2cdp + d^2),$$

which gives $(ap - b)^2 + (bp - c)^2 + (cp - d)^2 \ge 0$
(2)

Since the sum of squares of real numbers is non negative, therefore, from (1) and (2),
we have, $(ap - b)^2 + (bp - c)^2 + (cp - d)^2 = 0$

or $ap - b = 0$, $bp - c = 0$, $cp - d = 0$

This implies that $\frac{b}{a} = \frac{c}{b} = \frac{d}{c} = p$

Hence $a$, $b$, $c$ and $d$ are in G.P.

Example 24 If $p,q,r$ are in G.P. and the equations, $px^2 + 2qx + r = 0$ and

$$dx^2 + 2ex + f = 0 \text{ have a common root, then show that } \frac{d}{p}, \frac{e}{q}, \frac{f}{r} \text{ are in A.P.}$$

Solution The equation $px^2 + 2qx + r = 0$ has roots given by

$$x = \frac{-2q \pm \sqrt{4q^2 - 4rp}}{2p}$$

Since $p, q, r$ are in G.P. $q^2 = pr$. Thus $x = \frac{-q}{p}$ but $\frac{-q}{p}$ is also root of
$dx^2 + 2ex + f = 0$ (Why ?). Therefore

$$dx^2 + 2ex + f = 0 \text{ (Why ?). Therefore}$$

$$d\left(\frac{-q}{p}\right)^2 + 2e\left(\frac{-q}{p}\right) + f = 0,$$

or $dq^2 - 2eqp + fp^2 = 0$ ... (1)

Dividing (1) by $pq^2$ and using $q^2 = pr$, we get

$$\frac{d}{p} - \frac{2e}{q} + \frac{fp}{pr} = 0, \text{ or } \quad \frac{2e}{q} = \frac{d}{p} + \frac{f}{r}$$

Hence $\frac{d}{p}, \frac{e}{q}, \frac{f}{r}$ are in A.P.

<!-- page 262 -->
Miscellaneous Exercise On Chapter 9

1. Show that the sum of $(m+n)^{th}$ and $(m-n)^{th}$ terms of an A.P. is equal to twice
the $m^{th}$ term.
2. If the sum of three numbers in A.P., is 24 and their product is 440, find the
numbers.
3. Let the sum of $n$, $2n$, $3n$ terms of an A.P. be $S_1$, $S_2$ and $S_3$, respectively, show that
$S_3 = 3(S_2 - S_1)$
4. Find the sum of all numbers between 200 and 400 which are divisible by 7.
5. Find the sum of integers from 1 to 100 that are divisible by 2 or 5.
6. Find the sum of all two digit numbers which when divided by 4, yields 1 as
remainder.
7. If $f$ is a function satisfying $f(x+y) = f(x)f(y)$ for all $x$, $y \in \mathbb{N}$ such that
$$f(1) = 3 \text{ and } \sum_{x=1}^{n} f(x) = 120 \text{ , find the value of } n.$$
8. The sum of some terms of G.P. is 315 whose first term and the common ratio are
5 and 2, respectively. Find the last term and the number of terms.
9. The first term of a G.P. is 1. The sum of the third term and fifth term is 90.
Find the common ratio of G.P.
10. The sum of three numbers in G.P. is 56. If we subtract 1, 7, 21 from these numbers
in that order, we obtain an arithmetic progression. Find the numbers.
11. A G.P. consists of an even number of terms. If the sum of all the terms is 5 times
the sum of terms occupying odd places, then find its common ratio.
12. The sum of the first four terms of an A.P. is 56. The sum of the last four terms is
112. If its first term is 11, then find the number of terms.

13. If $\frac{a+bx}{a-bx} = \frac{b+cx}{b-cx} = \frac{c+dx}{c-dx} (x \neq 0)$, then show that $a$, $b$, $c$ and $d$ are in G.P.
14. Let S be the sum, P the product and R the sum of reciprocals of $n$ terms in a G.P.
Prove that $\text{P}^2\text{R}^n = \text{S}^n$.
15. The $p^{th}$, $q^{th}$ and $r^{th}$ terms of an A.P. are $a$, $b$, $c$, respectively. Show that
$$(q-r)a + (r-p)b + (p-q)c = 0$$
16. If $a\left(\frac{1}{b} + \frac{1}{c}\right)$, $b\left(\frac{1}{c} + \frac{1}{a}\right)$, $c\left(\frac{1}{a} + \frac{1}{b}\right)$ are in A.P., prove that $a$, $b$, $c$ are in A.P.
17. If $a$, $b$, $c$, $d$ are in G.P, prove that $(a^n + b^n)$, $(b^n + c^n)$, $(c^n + d^n)$ are in G.P.
18. If $a$ and $b$ are the roots of $x^2 - 3x + p = 0$ and $c$, $d$ are roots of $x^2 - 12x + q = 0$,
where $a$, $b$, $c$, $d$ form a G.P. Prove that $(q+p) : (q-p) = 17:15$.

<!-- page 263 -->
19. The ratio of the A.M. and G.M. of two positive numbers $a$ and $b$, is $m : n$. Show


that $a : b = \left( m + \sqrt{m^2 - n^2} \right) : \left( m - \sqrt{m^2 - n^2} \right)$.

20. If $a, b, c$ are in A.P.; $b, c, d$ are in G.P. and $\frac{1}{c}, \frac{1}{d}, \frac{1}{e}$ are in A.P. prove that $a, c, e$
are in G.P.

21. Find the sum of the following series up to $n$ terms:
(i) $5 + 55 +555 + \dots$                                     (ii) $.6 + .66 + .666+\dots$

22. Find the $20^{\text{th}}$ term of the series $2 \times 4 + 4 \times 6 + 6 \times 8 + ... + n$ terms.

23. Find the sum of the first $n$ terms of the series: $3+ 7 +13 +21 +31 +...$

24. If $\text{S}_1$, $\text{S}_2$, $\text{S}_3$ are the sum of first $n$ natural numbers, their squares and their
cubes, respectively, show that $9\text{S}_2^2 = \text{S}_3 (1 + 8\text{S}_1)$.

25. Find the sum of the following series up to $n$ terms:

$$\frac{1^3}{1} + \frac{1^3 + 2^3}{1 + 3} + \frac{1^3 + 2^3 + 3^3}{1 + 3 + 5} + ...$$

26. Show that $\frac{1 \times 2^2 + 2 \times 3^2 + ... + n \times (n+1)^2}{1^2 \times 2 + 2^2 \times 3 + ... + n^2 \times (n+1)} = \frac{3n+5}{3n+1}$.

27. A farmer buys a used tractor for Rs 12000. He pays Rs 6000 cash and agrees to
pay the balance in annual instalments of Rs 500 plus 12% interest on the unpaid
amount. How much will the tractor cost him?

28. Shamshad Ali buys a scooter for Rs 22000. He pays Rs 4000 cash and agrees to
pay the balance in annual instalment of Rs 1000 plus 10% interest on the unpaid
amount. How much will the scooter cost him?

29. A person writes a letter to four of his friends. He asks each one of them to copy
the letter and mail to four different persons with instruction that they move the
chain similarly. Assuming that the chain is not broken and that it costs 50 paise to
mail one letter. Find the amount spent on the postage when $8^{\text{th}}$ set of letter is
mailed.

30. A man deposited Rs 10000 in a bank at the rate of 5% simple interest annually.
Find the amount in $15^{\text{th}}$ year since he deposited the amount and also calculate the
total amount after 20 years.

31. A manufacturer reckons that the value of a machine, which costs him Rs. 15625,
will depreciate each year by 20%. Find the estimated value at the end of 5 years.

32. 150 workers were engaged to finish a job in a certain number of days. 4 workers
dropped out on second day, 4 more workers dropped out on third day and so on.

<!-- page 264 -->
It took 8 more days to finish the work. Find the number of days in which the work
was completed.

Summary

◆ By a sequence, we mean an arrangement of number in definite order according
to some rule. Also, we define a sequence as a function whose domain is the
set of natural numbers or some subsets of the type $\{1, 2, 3, ...k\}$. A sequence
containing a finite number of terms is called a finite sequence. A sequence is
called infinite if it is not a finite sequence.

◆ Let $a_1, a_2, a_3, ...$ be the sequence, then the sum expressed as $a_1 + a_2 + a_3 + ...$
is called series. A series is called finite series if it has got finite number of
terms.

◆ An arithmetic progression (A.P.) is a sequence in which terms increase or
decrease regularly by the same constant. This constant is called common
difference of the A.P. Usually, we denote the first term of A.P. by $a$, the
common difference by $d$ and the last term by $l$. The general term or the $n^{th}$
term of the A.P. is given by $a_n = a + (n - 1) d$.

The sum $S_n$ of the first $n$ terms of an A.P. is given by

$$S_n = \frac{n}{2} [2a + (n - 1)d] = \frac{n}{2} (a + l).$$

◆ The arithmetic mean A of any two numbers $a$ and $b$ is given by $\frac{a + b}{2}$ i.e., the

sequence $a, A, b$ is in A.P.

◆ A sequence is said to be a geometric progression or G.P., if the ratio of any
term to its preceding term is same throughout. This constant factor is called
the common ratio. Usually, we denote the first term of a G.P. by $a$ and its
common ratio by $r$. The general or the $n^{th}$ term of G.P. is given by $a_n = ar^{n-1}$.
The sum $S_n$ of the first $n$ terms of G.P. is given by

<!-- page 265 -->
$$S_n = \frac{a(r^n - 1)}{r - 1} \ or \ \frac{a(1 - r^n)}{1 - r}, \ if \ r \neq 1$$


The geometric mean (G.M.) of any two positive numbers $a$ and $b$ is given by


$$\sqrt{ab} \text{ i.e., the sequence } a, \text{ G, } b \text{ is G.P.}$$

Historical Note

Evidence is found that Babylonians, some 4000 years ago, knew of arithmetic and
geometric sequences. According to Boethius (510), arithmetic and geometric
sequences were known to early Greek writers. Among the Indian mathematician,
Aryabhatta (476) was the first to give the formula for the sum of squares and cubes
of natural numbers in his famous work Aryabhatiyam, written around
499. He also gave the formula for finding the sum to $n$ terms of an arithmetic
sequence starting with $p^{\text{th}}$ term. Noted Indian mathematicians Brahmgupta
(598), Mahavira (850) and Bhaskara (1114-1185) also considered the sum of squares
and cubes. Another specific type of sequence having important applications in
mathematics, called Fibonacci sequence, was discovered by Italian mathematician
Leonardo Fibonacci (1170-1250). Seventeenth century witnessed the classification
of series into specific forms. In 1671 James Gregory used the term infinite series in
connection with infinite sequence. It was only through the rigorous development of
algebraic and set theoretic tools that the concepts related to sequence and series
could be formulated suitably.

<!-- page 266 -->
Chapter

STRAIGHT LINES

❖ *Geometry*, as a logical system, is a means and even the most powerful
means to make children feel the strength of the human spirit that is
of their own spirit. – H. FREUDENTHAL❖

10.1 Introduction

We are familiar with two-dimensional coordinate geometry
from earlier classes. Mainly, it is a combination of algebra
and geometry. A systematic study of geometry by the use
of algebra was first carried out by celebrated French
philosopher and mathematician René Descartes, in his book
‘La Géométrie, published in 1637. This book introduced the
notion of the equation of a curve and related analytical
methods into the study of geometry. The resulting
combination of analysis and geometry is referred now as
analytical geometry. In the earlier classes, we initiated
the study of coordinate geometry, where we studied about
coordinate axes, coordinate plane, plotting of points in a
plane, distance between two points, section formulae, etc. All these concepts are the
basics of coordinate geometry.

René Descartes
(1596 -1650)

Let us have a brief recall of coordinate geometry done in earlier classes. To
recapitulate, the location of the points $(6, -4)$ and
$(3, 0)$ in the XY-plane is shown in Fig 10.1.

We may note that the point $(6, -4)$ is at 6 units
distance from the $y$-axis measured along the positive
$x$-axis and at 4 units distance from the $x$-axis
measured along the negative $y$-axis. Similarly, the
point $(3, 0)$ is at 3 units distance from the $y$-axis
measured along the positive $x$-axis and has zero
distance from the $x$-axis.

Fig 10.1

We also studied there following important
formulae:

<!-- page 267 -->
I. Distance between the points P $(x_1, y_1)$ and Q $(x_2, y_2)$ is

$$PQ=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}$$

For example, distance between the points $(6, -4)$ and $(3, 0)$ is

$$\sqrt{(3-6)^2 + (0+4)^2} = \sqrt{9+16} = 5 \text{ units.}$$

II. The coordinates of a point dividing the line segment joining the points $(x_1, y_1)$

and $(x_2, y_2)$ internally, in the ratio $m$: $n$ are $\left( \frac{m x_2 + n x_1}{m + n}, \frac{m y_2 + n y_1}{m + n} \right)$.

For example, the coordinates of the point which divides the line segment joining

A $(-1, -3)$ and B $(-3, 9)$ internally, in the ratio 1:3 are given by $x = \frac{1.(-3) + 3.1}{1+3} = 0$

and $y = \frac{1.9 + 3.(-3)}{1 + 3} = 0.$

III. In particular, if $m = n$, the coordinates of the mid-point of the line segment

joining the points $(x_1, y_1)$ and $(x_2, y_2)$ are $\left( \frac{x_1 + x_2}{2}, \frac{y_1 + y_2}{2} \right)$.

IV. Area of the triangle whose vertices are $(x_1, y_1), (x_2, y_2)$ and $(x_3, y_3)$ is

$$\frac{1}{2} \left| x_1(y_2 - y_3) + x_2(y_3 - y_1) + x_3(y_1 - y_2) \right| \text{ .}$$

For example, the area of the triangle, whose vertices are $(4, 4)$, $(3, -2)$ and $(-3, 16)$ is

$$\frac{1}{2} | 4(-2 - 16) + 3(16 - 4) + (-3)(4 + 2) | = \frac{|-54|}{2} = 27.$$

$\mathit{Remark}$ If the area of the triangle ABC is zero, then three points A, B and C lie on
a line, i.e., they are collinear.
$\quad$ In the this Chapter, we shall continue the study of coordinate geometry to study
properties of the simplest geometric figure – $\mathit{straight\ line}$. Despite its simplicity, the
line is a vital concept of geometry and enters into our daily experiences in numerous
interesting and useful ways. Main focus is on representing the line algebraically, for
which $\mathit{slope}$ is most essential.

10.2 Slope of a Line

A line in a coordinate plane forms two angles with the $x$-axis, which are supplementary.

<!-- page 268 -->
The angle (say) $\theta$ made by the line $l$ with positive
direction of $x$-axis and measured anti clockwise
is called the $inclination$ $of$ $the$ $line$. Obviously
$0^{\circ} \leq \theta \leq 180^{\circ}$ (Fig 10.2).

We observe that lines parallel to $x$-axis, or
coinciding with $x$-axis, have inclination of $0^{\circ}$. The
inclination of a vertical line (parallel to or
coinciding with $y$-axis) is $90^{\circ}$.

**Definition 1** If $\theta$ is the inclination of a line
$l$, then $\tan \theta$ is called the *slope* or *gradient* of
the line $l$.
The slope of a line whose inclination is $90^\circ$ is not
defined.
The slope of a line is denoted by $m$.
Thus, $m = \tan \theta$, $\theta \neq 90^\circ$
It may be observed that the slope of $x$-axis is zero and slope of $y$-axis is not defined.

10.2.1 Slope of a line when coordinates of any two points on the line are given

We know that a line is completely determined when we are given two points on it.
Hence, we proceed to find the slope of a
line in terms of the coordinates of two points
on the line.

Let $P(x_1, y_1)$ and $Q(x_2, y_2)$ be two
points on non-vertical line $l$ whose inclination
is $\theta$. Obviously, $x_1 \neq x_2$, otherwise the line
will become perpendicular to $x$-axis and its
slope will not be defined. The inclination of
the line $l$ may be acute or obtuse. Let us
take these two cases.

Fig 10. 3 (i)

Draw perpendicular QR to $x$-axis and
PM perpendicular to RQ as shown in
Figs. 10.3 (i) and (ii).

Case 1 When angle $\theta$ is acute:
In Fig 10.3 (i), $\angle MPQ = \theta$.
Therefore, slope of line $l = m = \tan \theta$.

But in $\Delta MPQ$, we have $\tan \theta = \frac{MQ}{MP} = \frac{y_2 - y_1}{x_2 - x_1}$.
... (1)
... (2)

<!-- page 269 -->
From equations (1) and (2), we have

$$m = \frac{y_2 - y_1}{x_2 - x_1}.$$

Fig 10. 3 (ii)

Case II When angle $\theta$ is obtuse:
In Fig 10.3 (ii), we have
$\angle MPQ = 180^\circ - \theta$.

Therefore, $\theta = 180^\circ - \angle MPQ$.

Now, slope of the line $l$

$$m = \tan \theta$$
$$= \tan ( 180^\circ - \angle MPQ) = - \tan \angle MPQ$$
$$= -\frac{MQ}{MP} = -\frac{y_2 - y_1}{x_1 - x_2} = \frac{y_2 - y_1}{x_2 - x_1}.$$

Consequently, we see that in both the cases the slope $m$ of the line through the points

$(x_1, y_1)$ and $(x_2, y_2)$ is given by $m = \frac{y_2 - y_1}{x_2 - x_1}$.

10.2.2 Conditions for parallelism and perpendicularity of lines in terms of their
slopes In a coordinate plane, suppose that non-vertical lines $l_1$ and $l_2$ have slopes $m_1$
and $m_2$, respectively. Let their inclinations be $\alpha$ and
$\beta$, respectively.

If the line $l_1$ is parallel to $l_2$ (Fig 10.4), then their
inclinations are equal, i.e.,

$\alpha = \beta$, and hence, $\tan \alpha = \tan \beta$

Therefore $m_1 = m_2$, i.e., their slopes are equal.
Conversely, if the slope of two lines $l_1$ and $l_2$
is same, i.e.,

Fig 10. 4

$$m_1 = m_2.$$
Then $\tan \alpha = \tan \beta.$

By the property of tangent function (between $0^{\circ}$ and $180^{\circ}$), $\alpha = \beta$.
Therefore, the lines are parallel.

<!-- page 270 -->
Hence, two non vertical lines $l_1$ and $l_2$ are parallel if and only if their slopes
are equal.

If the lines $l_1$ and $l_2$ are perpendicular (Fig 10.5), then $\beta = \alpha + 90^\circ$.

Therefore, $\tan \quad \beta = \tan (\alpha + 90^\circ)$

$$= -\cot \alpha = -\frac{1}{\tan \alpha}$$

Fig 10.5

i.e., $m_2 = -\frac{1}{m_1}$ or $m_1 m_2 = -1$

Conversely, if $m_1 \ m_2 = -1$, i.e., $\tan \alpha \tan \beta = -1$.
Then $\tan \alpha = -\cot \beta = \tan (\beta + 90^\circ)$ or $\tan (\beta - 90^\circ)$
Therefore, $\alpha$ and $\beta$ differ by $90^\circ$.
Thus, lines $l_1$ and $l_2$ are perpendicular to each other.

Thus, lines $l_1$ and $l_2$ are perpendicular to each other.

Hence, two non-vertical lines are perpendicular to each other if and only if
their slopes are negative reciprocals of each other,

i.e., $m_2 = -\frac{1}{m_1}$ or, $m_1 m_2 = -1$.

Let us consider the following example.

Example 1 Find the slope of the lines:

(a)   Passing through the points $(3, -2)$ and $(-1, 4)$,

(b)   Passing through the points $(3, -2)$ and $(7, -2)$,

(c)   Passing through the points $(3, -2)$ and $(3, 4)$,

(d)   Making inclination of $60^{\circ}$ with the positive direction of $x$-axis.

Solution (a) The slope of the line through $(3, -2)$ and $(-1, 4)$ is

$$m = \frac{4 - (-2)}{-1 - 3} = \frac{6}{-4} = -\frac{3}{2} .$$

(b) The slope of the line through the points $(3, -2)$ and $(7, -2)$ is

$$m = \frac{-2 - (-2)}{7 - 3} = \frac{0}{4} = 0 .$$

(c) The slope of the line through the points $(3, -2)$ and $(3, 4)$ is

<!-- page 271 -->
$$m = \frac{4 - (-2)}{3 - 3} = \frac{6}{0}, \text{ which is not defined.}$$

(d) Here inclination of the line $\alpha = 60^{\circ}$. Therefore, slope of the line is
$$m = \tan 60^{\circ} = \sqrt{3} \text{ .}$$

10.2.3 Angle between two lines When we think about more than one line in a plane,
then we find that these lines are either intersecting or parallel. Here we will discuss the
angle between two lines in terms of their slopes.

Let $\mathrm{L}_1$ and $\mathrm{L}_2$ be two non-vertical lines with slopes $m_1$ and $m_2$, respectively. If $\alpha_1$
and $\alpha_2$ are the inclinations of lines $\mathrm{L}_1$ and $\mathrm{L}_2$, respectively. Then

$$m_1 = \tan \alpha_1 \text{ and } m_2 = \tan \alpha_2 .$$

We know that when two lines intersect each other, they make two pairs of
vertically opposite angles such that sum of any two adjacent angles is $180^{\circ}$. Let $\theta$ and
$\phi$ be the adjacent angles between the lines $\mathrm{L}_{1}$ and $\mathrm{L}_{2}$ (Fig10.6). Then

$\theta = \alpha_2 - \alpha_1$ and $\alpha_1, \alpha_2 \neq 90^\circ$.

Therefore $\tan \theta = \tan (\alpha_2 - \alpha_1) = \frac{\tan \alpha_2 - \tan \alpha_1}{1 + \tan \alpha_1 \tan \alpha_2} = \frac{m_2 - m_1}{1 + m_1 m_2} \quad (\text{as } 1 + m_1 m_2 \neq 0)$

and $\phi = 180^\circ - \theta$ so that

$$\tan \phi = \tan (180^\circ - \theta) = -\tan \theta = -\frac{m_2 - m_1}{1 + m_1 m_2}, \text{ as } 1 + m_1 m_2 \neq 0$$

Fig 10. 6

Now, there arise two cases:

<!-- page 272 -->
Case I If $\frac{m_2 - m_1}{1 + m_1 m_2}$ is positive, then $\tan \theta$ will be positive and $\tan \phi$ will be negative,

which means $\theta$ will be acute and $\phi$ will be obtuse.

Case II If $\frac{m_2 - m_1}{1 + m_1 m_2}$ is negative, then $\tan \theta$ will be negative and $\tan \phi$ will be positive,

which means that $\theta$ will be obtuse and $\phi$ will be acute.

Thus, the acute angle (say $\theta$) between lines $\mathrm{L}_1$ and $\mathrm{L}_2$ with slopes $m_1$ and $m_2$,
respectively, is given by

$$\tan \theta = \left| \frac{m_2 - m_1}{1 + m_1 m_2} \right|, \text{ as } 1 + m_1 m_2 \neq 0 \quad \dots (1)$$

The obtuse angle (say $\phi$) can be found by using $\phi = 180^0 - \theta$.

Example 2 If the angle between two lines is $\frac{\pi}{4}$ and slope of one of the lines is $\frac{1}{2}$, find
the slope of the other line.

Solution We know that the acute angle $\theta$ between two lines with slopes $m_1$ and $m_2$

is given by $\quad \tan \theta = \left| \frac{m_2 - m_1}{1 + m_1 m_2} \right| \quad \dots (1)$

Let $m_1 = \frac{1}{2}$, $m_2 = m$ and $\theta = \frac{\pi}{4}$.

Now, putting these values in (1), we get

$$\tan \frac{\pi}{4} = \left| \frac{m - \frac{1}{2}}{1 + \frac{1}{2} m} \right| \quad \text{or} \quad 1 = \left| \frac{m - \frac{1}{2}}{1 + \frac{1}{2} m} \right| ,$$

which gives $$\frac{m-\frac{1}{2}}{1+\frac{1}{2} m}=1 \quad \text { or } \quad \frac{m-\frac{1}{2}}{1+\frac{1}{2} m}=-1$$

Therefore $m=3$ or $m=-\frac{1}{3}$.

<!-- page 273 -->
Hence, slope of the other line is


$3$ or $-\frac{1}{3}$. Fig 10.7 explains the


reason of two answers.

Fig 10. 7

Example 3 Line through the points $(-2, 6)$ and $(4, 8)$ is perpendicular to the line
through the points $(8, 12)$ and $(x, 24)$. Find the value of $x$.

Solution Slope of the line through the points $(-2, 6)$ and $(4, 8)$ is

$$m_1 = \frac{8-6}{4-(-2)} = \frac{2}{6} = \frac{1}{3}$$

Slope of the line through the points $(8, 12)$ and $(x, 24)$ is

$$m_2 = \frac{24 - 12}{x - 8} = \frac{12}{x - 8}$$

Since two lines are perpendicular,
$m_1 m_2 = -1$, which gives

$$\frac{1}{3} \times \frac{12}{x-8} = -1 \text{ or } x = 4.$$

10.2.4 Collinearity of three points We

know that slopes of two parallel lines are
equal. If two lines having the same slope
pass through a common point, then two
lines will coincide. Hence, if A, B and C
are three points in the XY-plane, then they
will lie on a line, i.e., three points are
collinear (Fig 10.8) if and only if slope of
AB = slope of BC.

Fig 10.8

<!-- page 274 -->
Example 4 Three points P $(h, k)$, Q $(x_1, y_1)$ and R $(x_2, y_2)$ lie on a line. Show that
$$(h - x_1) (y_2 - y_1) = (k - y_1) (x_2 - x_1).$$

Solution Since points P, Q and R are collinear, we have

Slope of PQ = Slope of QR, i.e., $\frac{y_1-k}{x_1-h} = \frac{y_2-y_1}{x_2-x_1}$

or $\frac{k - y_1}{h - x_1} = \frac{y_2 - y_1}{x_2 - x_1}$,

or $(h-x_1)(y_2-y_1) = (k-y_1)(x_2-x_1).$

Example 5 In Fig 10.9, time and
distance graph of a linear motion is given.
Two positions of time and distance are
recorded as, when $T = 0, D = 2$ and when
$T = 3, D = 8$. Using the concept of slope,
find law of motion, i.e., how distance
depends upon time.

Fig 10.9

Solution Let $(T, D)$ be any point on the
line, where $D$ denotes the distance at time
$T$. Therefore, points $(0, 2)$, $(3, 8)$ and
$(T, D)$ are collinear so that

$$\frac{8-2}{3-0}=\frac{\mathrm{D}-8}{\mathrm{T}-3} \quad \text { or } \quad 6(\mathrm{T}-3)=3(\mathrm{D}-8)$$

or $D = 2(T + 1),$

which is the required relation.

EXERCISE 10.1

1. Draw a quadrilateral in the Cartesian plane, whose vertices are $(-4, 5)$, $(0, 7)$,
$(5, -5)$ and $(-4, -2)$. Also, find its area.
2. The base of an equilateral triangle with side $2a$ lies along the $y$-axis such that the
mid-point of the base is at the origin. Find vertices of the triangle.
3. Find the distance between $\mathrm{P} \left(x_1, y_1\right)$ and $\mathrm{Q} \left(x_2, y_2\right)$ when : (i) $\mathrm{PQ}$ is parallel to the
$y$-axis, (ii) $\mathrm{PQ}$ is parallel to the $x$-axis.
4. Find a point on the $x$-axis, which is equidistant from the points $(7, 6)$ and $(3, 4)$.
5. Find the slope of a line, which passes through the origin, and the mid-point of the
line segment joining the points $\mathrm{P} \left(0, -4\right)$ and $\mathrm{B} \left(8, 0\right)$.

<!-- page 275 -->
6. Without using the Pythagoras theorem, show that the points $(4, 4)$, $(3, 5)$ and
$(-1, -1)$ are the vertices of a right angled triangle.
7. Find the slope of the line, which makes an angle of $30^{\circ}$ with the positive direction
of $y$-axis measured anticlockwise.
8. Find the value of $x$ for which the points $(x, -1)$, $(2, 1)$ and $(4, 5)$ are collinear.
9. Without using distance formula, show that points $(-2, -1)$, $(4, 0)$, $(3, 3)$ and $(-3, 2)$
are the vertices of a parallelogram.
10. Find the angle between the $x$-axis and the line joining the points $(3,-1)$ and $(4,-2)$.
11. The slope of a line is double of the slope of another line. If tangent of the angle
between them is $\frac{1}{3}$, find the slopes of the lines.
12. A line passes through $(x_1, y_1)$ and $(h, k)$. If slope of the line is $m$, show that
$$k - y_1 = m(h - x_1).$$
13. If three points $(h, 0)$, $(a, b)$ and $(0, k)$ lie on a line, show that $\frac{a}{h} + \frac{b}{k} = 1$.
14. Consider the following population and year graph (Fig 10.10), find the slope of the
line AB and using it, find what will be the population in the year 2010?

Fig 10.10

10.3 Various Forms of the Equation of a Line

We know that every line in a plane contains infinitely many points on it. This relationship
between line and points leads us to find the solution of the following problem:

<!-- page 276 -->
How can we say that a given point lies on the given line? Its answer may be that
for a given line we should have a definite condition on the points lying on the line.
Suppose P $(x, y)$ is an arbitrary point in the XY-plane and L is the given line. For the
equation of L, we wish to construct a statement or condition for the point P that is
true, when P is on L, otherwise false. Of course the statement is merely an algebraic
equation involving the variables $x$ and $y$. Now, we will discuss the equation of a line
under different conditions.

**10.3.1 Horizontal and vertical lines** If a horizontal line L is at a distance $a$ from the
$x$-axis then ordinate of every point lying on the line is either $a$ or $- a$ [Fig 10.11 (a)].
Therefore, equation of the line L is either $y = a$ or $y = - a$. Choice of sign will depend
upon the position of the line according as the line is above or below the $y$-axis. Similarly,
the equation of a vertical line at a distance $b$ from the $y$-axis is either $x = b$ or
$x = - b$ [Fig 10.11(b)].

Fig 10.11

Example 6 Find the equations of the lines
parallel to axes and passing through
$(-2, 3)$.

Solution Position of the lines is shown in the
Fig 10.12. The $y$-coordinate of every point on
the line parallel to $x$-axis is 3, therefore, equation
of the line parallel to $x$-axis and passing through
$(-2, 3)$ is $y = 3$. Similarly, equation of the line
parallel to $y$-axis and passing through $(-2, 3)$
is $x = -2$.

Fig 10.12

<!-- page 277 -->
10.3.2 *Point-slope form* Suppose that
$\mathrm{P}_0 (x_0, y_0)$ is a fixed point on a non-vertical
line L, whose slope is $m$. Let P $(x, y)$ be an
arbitrary point on L (Fig 10.13).
Then, by the definition, the slope of L is
given by

$$m = \frac{y - y_0}{x - x_0}, \text{ i.e., } y - y_0 = m(x - x_0)$$

Fig 10.13

$$...(1)$$

Since the point $\mathrm{P}_{0}\left(x_{0}, y_{0}\right)$ along with
all points $(x, y)$ on $\mathrm{L}$ satisfies (1) and no
other point in the plane satisfies (1). Equation
(1) is indeed the equation for the given line $\mathrm{L}$.

Thus, the point $(x, y)$ lies on the line with slope $m$ through the fixed point $(x_0, y_0)$,
if and only if, its coordinates satisfy the equation

$$y - y_0 = m(x - x_0)$$

Example 7 Find the equation of the line through $(- 2, 3)$ with slope $- 4$.

Solution Here $m = -4$ and given point $(x_0, y_0)$ is $(-2, 3)$.

By slope-intercept form formula
(1) above, equation of the given
line is

$$y - 3 = - 4 \ (x + 2) \text{ or}$$
$$4x + y + 5 = 0, \text{ which is the}$$
$$\text{required equation.}$$

10.3.3 Two-point form Let the
line L passes through two given
points $\mathrm{P}_1\left(x_1, y_1\right)$ and $\mathrm{P}_2\left(x_2, y_2\right)$.
Let $\mathrm{P}(x, y)$ be a general point
on $\mathrm{L}$ (Fig 10.14).

Fig 10.14

The three points $P_1$, $P_2$ and $P$ are
collinear, therefore, we have
slope of $P_1P =$ slope of $P_1P_2$

i.e., $\frac{y-y_{1}}{x-x_{1}}=\frac{y_{2}-y_{1}}{x_{2}-x_{1}}$, or $y-y_{1}=\frac{y_{2}-y_{1}}{x_{2}-x_{1}}(x-x_{1})$.

<!-- page 278 -->
Thus, equation of the line passing through the points $(x_1, y_1)$ and $(x_2, y_2)$ is given by

$$y - y_1 = \frac{y_2 - y_1}{x_2 - x_1}(x - x_1) \quad \dots (2)$$

Example 8 Write the equation of the line through the points $(1, -1)$ and $(3, 5)$.

Solution Here $x_1 = 1$, $y_1 = -1$, $x_2 = 3$ and $y_2 = 5$. Using two-point form (2) above
for the equation of the line, we have

$$y - (-1) = \frac{5 - (-1)}{3 - 1} (x - 1)$$

or $-3x + y + 4 = 0$, which is the required equation.

10.3.4 *Slope-intercept form* Sometimes a line is known to us with its slope and an
intercept on one of the axes. We will now find equations of such lines.

Case I Suppose a line L with slope $m$ cuts the y-axis at a distance $c$ from the origin
(Fig10.15). The distance $c$ is called the yintercept of the line L. Obviously,
coordinates of the point where the line meet
the y-axis are $(0, c)$. Thus, L has slope $m$
and passes through a fixed point $(0, c)$.
Therefore, by point-slope form, the equation
of L is

Fig 10.15

$$y-c=m(x-0) \quad \text{or} \quad y=mx+c$$

Thus, the point $(x, y)$ on the line with slope
$m$ and $y$-intercept $c$ lies on the line if and
only if

$$y = mx + c \tag{3}$$

Note that the value of $c$ will be positive or negative according as the intercept is made
on the positive or negative side of the $y$-axis, respectively.

Case II Suppose line L with slope $m$ makes $x$-intercept $d$. Then equation of L is
$$y = m(x - d) \hfill ... (4)$$
Students may derive this equation themselves by the same method as in Case I.

Students may derive this equation themselves by the same method as in Case I.

Example 9 Write the equation of the lines for which $\tan \theta = \frac{1}{2}$, where $\theta$ is the


inclination of the line and (i) $y$-intercept is $-\frac{3}{2}$ (ii) $x$-intercept is 4.

<!-- page 279 -->
Solution (i) Here, slope of the line is $m = \tan \theta = \frac{1}{2}$ and $y$ - intercept $c = -\frac{3}{2}$.

Therefore, by slope-intercept form (3) above, the equation of the line is

$$y = \frac{1}{2}x - \frac{3}{2} \text{ or } 2y - x + 3 = 0,$$

which is the required equation.

(ii) Here, we have $m = \tan \theta = \frac{1}{2}$ and $d = 4$.

Therefore, by slope-intercept form (4) above, the equation of the line is

$$y = \frac{1}{2}(x - 4) \text{ or } 2y - x + 4 = 0,$$

which is the required equation.

10.3.5 Intercept - form Suppose a line L makes $x$-intercept $a$ and $y$-intercept $b$ on the
axes. Obviously L meets $x$-axis at the point L Y
$(a, 0)$ and $y$-axis at the point $(0, b)$ (Fig .10.16).
By two-point form of the equation of the line,
we have
$\begin{pmatrix} \uparrow \\ (0, b) \\ \downarrow \end{pmatrix}$

$$y-0=\frac{b-0}{0-a}(x-a) \quad \text{or} \quad ay=-bx+ab,$$

i.e., $\frac{x}{a} + \frac{y}{b} = 1.$

Fig 10.16

Thus, equation of the line making intercepts
$a$ and $b$ on $x$-and $y$-axis, respectively, is

$$\frac{x}{a} + \frac{y}{b} = 1 \hfill ... (5)$$

Example 10 Find the equation of the line, which makes intercepts $-3$ and $2$ on the
$x$- and $y$-axes respectively.

Solution Here $a = -3$ and $b = 2$. By intercept form (5) above, equation of the line is

$$\frac{x}{-3} + \frac{y}{2} = 1 \quad \text{or} \quad 2x - 3y + 6 = 0$$

<!-- page 280 -->
10.3.6 Normal form Suppose a non-vertical line is known to us with following data:

(i) Length of the perpendicular (normal) from origin to the line.
(ii) Angle which normal makes with the positive direction of $x$-axis.

Let L be the line, whose perpendicular distance from origin O be OA $= p$ and the
angle between the positive $x$-axis and OA be $\angle XOA = \omega$. The possible positions of line
L in the Cartesian plane are shown in the Fig 10.17. Now, our purpose is to find slope
of L and a point on it. Draw perpendicular AM on the $x$-axis in each case.

Fig 10.17

In each case, we have $\mathrm{OM} = p \cos \omega$ and $\mathrm{MA} = p \sin \omega$, so that the coordinates of the
point A are $(p \cos \omega, p \sin \omega)$.

Further, line L is perpendicular to OA. Therefore

The slope of the line $L = -\frac{1}{\text{slope of OA}} = -\frac{1}{\tan \omega} = -\frac{\cos \omega}{\sin \omega}$.

Thus, the line L has slope $-\frac{\cos \omega}{\sin \omega}$ and point A $(p \cos \omega, p \sin \omega)$on it. Therefore, by

point-slope form, the equation of the line L is

<!-- page 281 -->
$$y - p \sin \omega = -\frac{\cos \omega}{\sin \omega} (x - p \cos \omega) \quad \text{or} \quad x \cos \omega + y \sin \omega = p(\sin^2 \omega + \cos^2 \omega)$$

or $x \cos \omega + y \sin \omega = p.$

Hence, the equation of the line having normal distance $p$ from the origin and angle $\omega$
which the normal makes with the positive direction of $x$-axis is given by

$$x \cos \omega + y \sin \omega = p \qquad \dots (6)$$

Example 11 Find the equation of the line whose perpendicular distance from the
origin is 4 units and the angle which the normal makes with positive direction of $x$-axis
is $15^\circ$.

Solution Here, we are given $p = 4$ and
$\omega = 15^0$ (Fig10.18).

Now $\cos 15^{\circ} = \frac{\sqrt{3}+1}{2\sqrt{2}}$

and $\sin 15^{\circ} = \frac{\sqrt{3}-1}{2\sqrt{2}}$ (Why?)

Fig 10.18

By the normal form (6) above, the equation of the
line is

$$x \cos 15^0 + y \sin 15^0 = 4 \text{ or } \frac{\sqrt{3}+1}{2\sqrt{2}}x + \frac{\sqrt{3}-1}{2\sqrt{2}}y = 4 \quad \text{or} \quad (\sqrt{3}+1)x + (\sqrt{3}-1)y = 8\sqrt{2}.$$

This is the required equation.

Example 12 The Fahrenheit temperature F and absolute temperature K satisfy a
linear equation. Given that K = 273 when F = 32 and that K = 373 when F = 212.
Express K in terms of F and find the value of F, when K = 0.

Solution Assuming F along $x$-axis and K along $y$-axis, we have two points (32, 273)
and (212, 373) in XY-plane. By two-point form, the point (F, K) satisfies the equation

$$K - 273 = \frac{373 - 273}{212 - 32} (F - 32) \quad \text{or} \quad K - 273 = \frac{100}{180} (F - 32)$$

or $$K = \frac{5}{9} (F - 32) + 273 \quad \dots (1)$$

which is the required relation.

<!-- page 282 -->
When $K = 0$, Equation (1) gives

$$0=\frac{5}{9}(F-32)+273 \quad \text{or} \quad F-32=-\frac{273\times9}{5}=-491.4 \quad \text{or} \quad F=-459.4.$$

Alternate method We know that simplest form of the equation of a line is $y = mx + c$.
Again assuming F along $x$-axis and K along $y$-axis, we can take equation in the form

$$K = mF + c \hspace{150pt} ... (1)$$

Equation (1) is satisfied by (32, 273) and (212, 373). Therefore

$$273 = 32m + c \hspace{12em} ... (2)$$

and $373 = 212m + c$ ... (3)

Solving (2) and (3), we get

$$m = \frac{5}{9} \text{ and } c = \frac{2297}{9}.$$

Putting the values of $m$ and $c$ in (1), we get

$$K = \frac{5}{9} F + \frac{2297}{9} \quad \dots (4)$$

which is the required relation. When $K = 0$, (4) gives $F = - 459.4$.

Note We know, that the equation $y = mx + c$, contains two constants, namely,
$m$ and $c$. For finding these two constants, we need two conditions satisfied by the
equation of line. In all the examples above, we are given two conditions to determine
the equation of the line.

EXERCISE 10.2

In Exercises 1 to 8, find the equation of the line which satisfy the given conditions:

1. Write the equations for the $x$-and $y$-axes.

2. Passing through the point $(-4, 3)$ with slope $\frac{1}{2}$.

3. Passing through $(0, 0)$ with slope $m$.

4. Passing through $(2, 2\sqrt{3})$and inclined with the $x$-axis at an angle of $75^{\circ}$.

5. Intersecting the $x$-axis at a distance of 3 units to the left of origin with slope $-2$.

6. Intersecting the $y$-axis at a distance of 2 units above the origin and making an
angle of $30^{\circ}$ with positive direction of the $x$-axis.

7. Passing through the points $(-1, 1)$ and $(2, -4)$.

<!-- page 283 -->
8. Perpendicular distance from the origin is 5 units and the angle made by the
perpendicular with the positive $x$-axis is $30^0$.
9. The vertices of $\Delta$ PQR are P (2, 1), Q ($-2$, 3) and R (4, 5). Find equation of the
median through the vertex R.
10. Find the equation of the line passing through ($-3$, 5) and perpendicular to the line
through the points (2, 5) and ($-3$, 6).
11. A line perpendicular to the line segment joining the points (1, 0) and (2, 3) divides
it in the ratio 1: $n$. Find the equation of the line.
12. Find the equation of a line that cuts off equal intercepts on the coordinate axes
and passes through the point (2, 3).
13. Find equation of the line passing through the point (2, 2) and cutting off intercepts
on the axes whose sum is 9.

14. Find equation of the line through the point (0, 2) making an angle $\frac{2\pi}{3}$ with the
positive $x$-axis. Also, find the equation of line parallel to it and crossing the $y$-axis
at a distance of 2 units below the origin.
15. The perpendicular from the origin to a line meets it at the point ($-2$, 9), find the
equation of the line.
16. The length L (in centimetre) of a copper rod is a linear function of its Celsius
temperature C. In an experiment, if L = 124.942 when C = 20 and L= 125.134
when C = 110, express L in terms of C.
17. The owner of a milk store finds that, he can sell 980 litres of milk each week at
Rs 14/litre and 1220 litres of milk each week at Rs 16/litre. Assuming a linear
relationship between selling price and demand, how many litres could he sell
weekly at Rs 17/litre?
18. P ($a$, $b$) is the mid-point of a line segment between axes. Show that equation
of the line is $\frac{x}{a} + \frac{y}{b} = 2$.
19. Point R ($h$, $k$) divides a line segment between the axes in the ratio 1: 2. Find
equation of the line.
20. By using the concept of equation of a line, prove that the three points (3, 0),
($-2$, $-2$) and (8, 2) are collinear.

10.4 General Equation of a Line

In earlier classes, we have studied general equation of first degree in two variables,
$Ax + By + C = 0$, where A, B and C are real constants such that A and B are not zero
simultaneously. Graph of the equation $Ax + By + C = 0$ is always a straight line.

<!-- page 284 -->
Therefore, any equation of the form $Ax + By + C = 0$, where A and B are not zero
simultaneously is called \textit{general linear equation} or \textit{general equation of a line}.

10.4.1 *Different forms of* $\mathbf{A}x + \mathbf{B}y + \mathbf{C} = \mathbf{0}$ The general equation of a line can be
reduced into various forms of the equation of a line, by the following procedures:

(a) Slope-intercept form If $B \neq 0$, then $Ax + By + C = 0$ can be written as

$$y = -\frac{\mathrm{A}}{\mathrm{B}}x - \frac{\mathrm{C}}{\mathrm{B}} \text{ or } y = mx + c \quad \dots (1)$$

where $m=-\frac{\mathrm{A}}{\mathrm{B}}$ and $c=-\frac{\mathrm{C}}{\mathrm{B}}$.

We know that Equation (1) is the slope-intercept form of the equation of a line

whose slope is $-\frac{\mathbf{A}}{\mathbf{B}}$, and $y$-intercept is $-\frac{\mathbf{C}}{\mathbf{B}}$.

If $B = 0$, then $x = -\frac{C}{A}$,which is a vertical line whose slope is undefined and

$x$-intercept is $-\frac{\mathbf{C}}{\mathbf{A}}$.

(b) Intercept form If $C \neq 0$, then $Ax + By + C = 0$ can be written as

$$\frac{x}{-\frac{C}{A}}+\frac{y}{-\frac{C}{B}}=1 \quad \text{or} \quad \frac{x}{a}+\frac{y}{b}=1 \quad \dots (2)$$

where $a = -\frac{\mathrm{C}}{\mathrm{A}}$ and $b = -\frac{\mathrm{C}}{\mathrm{B}}$.

We know that equation (2) is intercept form of the equation of a line whose

$x$-intercept is $-\frac{\mathbf{C}}{\mathbf{A}}$ and $y$-intercept is $-\frac{\mathbf{C}}{\mathbf{B}}$.

If $C = 0$, then $Ax + By + C = 0$ can be written as $Ax + By = 0$, which is a line
passing through the origin and, therefore, has zero intercepts on the axes.

(c) **Normal form** Let $x \cos \omega + y \sin \omega = p$ be the normal form of the line represented
by the equation $Ax + By + C = 0$ or $Ax + By = - C$. Thus, both the equations are

same and therefore, $\frac{\mathrm{A}}{\cos \omega}=\frac{\mathrm{B}}{\sin \omega}=-\frac{\mathrm{C}}{p}$

<!-- page 285 -->
which gives $\cos \omega = -\frac{Ap}{C}$ and $\sin \omega = -\frac{Bp}{C}$.

Now $\sin^2\omega + \cos^2\omega = \left(-\frac{Ap}{C}\right)^2 + \left(-\frac{Bp}{C}\right)^2 = 1$

or $p^2 = \frac{\mathrm{C}^2}{\mathrm{A}^2 + \mathrm{B}^2}$ or $p = \pm \frac{\mathrm{C}}{\sqrt{\mathrm{A}^2 + \mathrm{B}^2}}$

Therefore $\cos \omega = \pm \frac{\mathrm{A}}{\sqrt{\mathrm{A}^2 + \mathrm{B}^2}}$ and $\sin \omega = \pm \frac{\mathrm{B}}{\sqrt{\mathrm{A}^2 + \mathrm{B}^2}}$.

Thus, the normal form of the equation $Ax + By + C = 0$ is

$$x \cos \omega + y \sin \omega = p,$$

where $\cos \omega = \pm \frac{\mathrm{A}}{\sqrt{\mathrm{A}^2 + \mathrm{B}^2}}$, $\sin \omega = \pm \frac{\mathrm{B}}{\sqrt{\mathrm{A}^2 + \mathrm{B}^2}}$ and $p = \pm \frac{\mathrm{C}}{\sqrt{\mathrm{A}^2 + \mathrm{B}^2}}$.

Proper choice of signs is made so that $p$ should be positive.

Example 13 Equation of a line is $3x - 4y + 10 = 0$. Find its (i) slope, (ii) $x$ - and
$y$-intercepts.

Solution (i) Given equation $3x - 4y + 10 = 0$ can be written as

$$y = \frac{3}{4}x + \frac{5}{2} \quad ... \quad (1)$$

Comparing (1) with $y = mx + c$, we have slope of the given line as $m = \frac{3}{4}$.

(ii) Equation $3x - 4y + 10 = 0$ can be written as

$$3x - 4y = -10 \quad \text{or} \quad -\frac{x}{10} + \frac{y}{5} = 1 \quad ... \quad (2)$$

Comparing (2) with $\frac{x}{a} + \frac{y}{b} = 1$, we have $x$-intercept as $a = -\frac{10}{3}$ and

$y$-intercept as $b = \frac{5}{2}$.

<!-- page 286 -->
Example 14 Reduce the equation $\sqrt{3}x + y - 8 = 0$ into normal form. Find the values
of $p$ and $\omega$.

Solution Given equation is
$$\sqrt{3}x + y - 8 = 0 \quad ... \quad (1)$$
Dividing (1) by $\quad \sqrt{\left(\sqrt{3}\right)^2 + (1)^2} = 2$, we get
$$\frac{\sqrt{3}}{2}x + \frac{1}{2}y = 4 \quad \text{or} \quad \cos 30^\circ x + \sin 30^\circ y = 4 \quad ... \quad (2)$$
Comparing (2) with $x \cos \omega + y \sin \omega = p$, we get $p = 4$ and $\omega = 30^\circ$.

Comparing (2) with $x \cos \omega + y \sin \omega = p$, we get $p = 4$ and $\omega = 30^\circ$.

Example15 Find the angle between the lines $y - \sqrt{3}x - 5 = 0$ and $\sqrt{3}y - x + 6 = 0$.

Solution Given lines are

$$y - \sqrt{3}x - 5 = 0 \text{ or } y = \sqrt{3}x + 5 \quad \dots (1)$$

and $\sqrt{3}y - x + 6 = 0$ or $y = \frac{1}{\sqrt{3}}x - 2\sqrt{3}$ ... (2)

Slope of line (1) is $m_1 = \sqrt{3}$ and slope of line (2) is $m_2 = \frac{1}{\sqrt{3}}$.

The acute angle (say) $\theta$ between two lines is given by

$$\tan \theta = \left| \frac{m_2 - m_1}{1 + m_1 m_2} \right|$$

(3)

Putting the values of $m_1$ and $m_2$ in (3), we get

$$\tan \theta = \left| \frac{\frac{1}{\sqrt{3}} - \sqrt{3}}{1 + \sqrt{3} \times \frac{1}{\sqrt{3}}} \right| = \left| \frac{1 - 3}{2\sqrt{3}} \right| = \frac{1}{\sqrt{3}}$$

which gives $\theta = 30^{\circ}$. Hence, angle between two lines is either $30^{\circ}$ or $180^{\circ} - 30^{\circ} = 150^{\circ}$.

Example 16 Show that two lines $a_1x + b_1y + c_1 = 0$ and $a_2x + b_2y + c_2 = 0$,
where $b_1, b_2 \neq 0$ are:

<!-- page 287 -->
(i) Parallel if $\frac{a_1}{b_1} = \frac{a_2}{b_2}$, and (ii) Perpendicular if $a_1 a_2 + b_1 b_2 = 0$.

Solution Given lines can be written as

$$y = -\frac{a_1}{b_1}x - \frac{c_1}{b_1} \hspace{150pt} ... (1)$$

and $y = -\frac{a_2}{b_2}x - \frac{c_2}{b_2}$ ... (2)

Slopes of the lines (1) and (2) are $m_1 = -\frac{a_1}{b_1}$ and $m_2 = -\frac{a_2}{b_2}$, respectively. Now

(i) Lines are parallel, if $m_1 = m_2$, which gives


$$-\frac{a_1}{b_1} = -\frac{a_2}{b_2} \text{ or } \frac{a_1}{b_1} = \frac{a_2}{b_2}.$$


(ii) Lines are perpendicular, if $m_1, m_2 = -1$, which gives


$$\frac{a_1}{b_1} \cdot \frac{a_2}{b_2} = -1 \text{ or } a_1 a_2 + b_1 b_2 = 0$$

Example 17 Find the equation of a line perpendicular to the line $x - 2y - 3 = 0$ and
passing through the point $(1, -2)$.

Solution Given line $x - 2y - 3 = 0$ can be written as

$$y = \frac{1}{2}x + \frac{3}{2} \quad ...(1)$$

Slope of the line (1) is $m_1 = \frac{1}{2}$. Therefore, slope of the line perpendicular to line (1) is

$$m_2 = -\frac{1}{m_1} = -2$$

Equation of the line with slope $-2$ and passing through the point $(1, -2)$ is

$$y - (-2) = -2(x - 1) \quad \text{or} \quad y = -2x,$$

which is the required equation.

<!-- page 288 -->
10.5 Distance of a Point From a Line

The distance of a point from a line is the length of the perpendicular drawn from the
point to the line. Let L : $Ax + By + C = 0$ be a line, whose distance from the point
P $(x_1, y_1)$ is $d$. Draw a perpendicular PM from the point P to the line L (Fig10.19). If

Fig10.19

the line meets the $x$-and $y$-axes at the points Q and R, respectively. Then, coordinates

of the points are $Q\left(-\frac{C}{A}, \quad 0\right)$and $R\left(0, \quad -\frac{C}{B}\right)$. Thus, the area of the triangle PQR
is given by

area ($\Delta$PQR) = $\frac{1}{2}$ PM.QR , which gives PM = $\frac{2 \text{ area } (\Delta$PQR)}{QR}$ ... (1)

Also, area ($\Delta$PQR) = $\frac{1}{2}\left|x_{1}\left(0+\frac{\mathbf{C}}{\mathbf{B}}\right)+\left(-\frac{\mathbf{C}}{\mathbf{A}}\right)\left(-\frac{\mathbf{C}}{\mathbf{B}}-y_{1}\right)+0\left(y_{1}-0\right)\right|$

$$= \frac{1}{2} \left| x_1 \frac{\mathbf{C}}{\mathbf{B}} + y_1 \frac{\mathbf{C}}{\mathbf{A}} + \frac{\mathbf{C}^2}{\mathbf{AB}} \right|$$

or $2 \text{ area } (\Delta PQR) = \left| \frac{\text{C}}{\text{AB}} \right| \cdot |A_{x_1} + B y_1 + \text{C}|, \text{ and}$

$$QR = \sqrt{\left(0 + \frac{C}{A}\right)^2 + \left(\frac{C}{B} - 0\right)^2} = \left|\frac{C}{AB}\right| \sqrt{A^2 + B^2}$$

Substituting the values of area ($\Delta$PQR) and QR in (1), we get

<!-- page 289 -->
$$PM = \frac{| A_{x_1} + B_{y_1} + C |}{\sqrt{A^2 + B^2}}$$

or $d = \frac{| \mathrm{A}_{x_1} + \mathrm{B} y_1 + \mathrm{C}|}{\sqrt{\mathrm{A}^2 + \mathrm{B}^2}}.$

Thus, the perpendicular distance ($d$) of a line $Ax + By + C = 0$ from a point $(x_1, y_1)$
is given by

$$d = \frac{\left| \mathrm{A}_{x_1} + \mathrm{B} y_1 + \mathrm{C} \right|}{\sqrt{\mathrm{A}^2 + \mathrm{B}^2}}.$$

10.5.1 Distance between two

*parallel lines* We know that slopes
of two parallel lines are equal.
Therefore, two parallel lines can be
taken in the form

$$y = mx + c_1 \quad \dots (1)$$
and $$y = mx + c_2 \quad \dots (2)$$

Line (1) will intersect $x$-axis at the point $X' \leftarrow$

Fig10.20

$$\mathrm{A} \left( -\frac{c_1}{m}, \quad 0 \right) \text{as shown in Fig10.20.}$$

Distance between two lines is equal to the length of the perpendicular from point
A to line (2). Therefore, distance between the lines (1) and (2) is

$$\frac{\left|(-m)\left(-\frac{c_{1}}{m}\right)+\left(-c_{2}\right)\right|}{\sqrt{1+m^{2}}} \text { or } d=\frac{\left|c_{1}-c_{2}\right|}{\sqrt{1+m^{2}}} .$$

Thus, the distance $d$ between two parallel lines $y = mx + c_1$ and $y = mx + c_2$ is given by

$$d=\frac{|c_{1}-c_{2}|}{\sqrt{1+m^{2}}}.$$

If lines are given in general form, i.e., $Ax + By + C_1 = 0$ and $Ax + By + C_2 = 0$,

<!-- page 290 -->
then above formula will take the form $d = \frac{|\mathrm{C}_1 - \mathrm{C}_2|}{\sqrt{\mathrm{A}^2 + \mathrm{B}^2}}$

Students can derive it themselves.

Example 18 Find the distance of the point $(3, -5)$ from the line $3x - 4y -26 = 0$.

Solution Given line is $3x - 4y -26 = 0$ ... (1)

Comparing (1) with general equation of line $Ax + By + C = 0$, we get

$$A = 3, B = -4 \text{ and } C = -26.$$

Given point is $(x_1, y_1) = (3, -5)$. The distance of the given point from given line is

$$d = \frac{|Ax_1 + By_1 + C|}{\sqrt{A^2 + B^2}} = \frac{|3.3 + (-4)(-5) - 26|}{\sqrt{3^2 + (-4)^2}} = \frac{3}{5}.$$

Example 19 Find the distance between the parallel lines $3x - 4y + 7 = 0$ and
$$3x - 4y + 5 = 0$$
Solution Here A = 3, B = $-4$, C$_1$ = 7 and C$_2$ = 5. Therefore, the required distance is
$$d = \frac{|7 - 5|}{\sqrt{3^2 + (-4)^2}} = \frac{2}{5}.$$

EXERCISE 10.3

1. Reduce the following equations into slope - intercept form and find their slopes
and the y - intercepts.
(i) $x + 7y = 0$, (ii) $6x + 3y - 5 = 0$, (iii) $y = 0$.
2. Reduce the following equations into intercept form and find their intercepts on
the axes.
(i) $3x + 2y - 12 = 0$, (ii) $4x - 3y = 6$, (iii) $3y + 2 = 0$.
3. Reduce the following equations into normal form. Find their perpendicular distances
from the origin and angle between perpendicular and the positive $x$-axis.
(i) $x - \sqrt{3}y + 8 = 0$, (ii) $y - 2 = 0$, (iii) $x - y = 4$.
4. Find the distance of the point $(-1, 1)$ from the line $12(x + 6) = 5(y - 2)$.

5. Find the points on the $x$-axis, whose distances from the line $\frac{x}{3} + \frac{y}{4} = 1$ are 4 units.

6. Find the distance between parallel lines
(i) $15x + 8y - 34 = 0$ and $15x + 8y + 31 = 0$ (ii) $l(x + y) + p = 0$ and $l(x + y) - r = 0$.

<!-- page 291 -->
7. Find equation of the line parallel to the line $3x - 4y + 2 = 0$ and passing through
the point $(-2, 3)$.
8. Find equation of the line perpendicular to the line $x - 7y + 5 = 0$ and having
$x$ intercept $3$.
9. Find angles between the lines $\sqrt{3}x + y = 1$ and $x + \sqrt{3}y = 1$.
10. The line through the points $(h, 3)$ and $(4, 1)$ intersects the line $7x - 9y - 19 = 0$.
at right angle. Find the value of $h$.
11. Prove that the line through the point $(x_1, y_1)$ and parallel to the line $Ax + By + C = 0$ is
$$A(x - x_1) + B(y - y_1) = 0.$$
12. Two lines passing through the point $(2, 3)$ intersects each other at an angle of $60^\circ$.
If slope of one line is $2$, find equation of the other line.
13. Find the equation of the right bisector of the line segment joining the points $(3, 4)$
and $(-1, 2)$.
14. Find the coordinates of the foot of perpendicular from the point $(-1, 3)$ to the
line $3x - 4y - 16 = 0$.
15. The perpendicular from the origin to the line $y = mx + c$ meets it at the point
$(-1, 2)$. Find the values of $m$ and $c$.
16. If $p$ and $q$ are the lengths of perpendiculars from the origin to the
lines $x \cos \theta - y \sin \theta = k \cos 2\theta$ and $x \sec \theta + y \csc \theta = k$, respectively, prove
that $p^2 + 4q^2 = k^2$.
17. In the triangle ABC with vertices A $(2, 3)$, B $(4, -1)$ and C $(1, 2)$, find the equation
and length of altitude from the vertex A.
18. If $p$ is the length of perpendicular from the origin to the line whose intercepts on
the axes are $a$ and $b$, then show that $\frac{1}{p^2} = \frac{1}{a^2} + \frac{1}{b^2}$.

Miscellaneous Examples

Example 20 If the lines $2x + y - 3 = 0$, $5x + ky - 3 = 0$ and $3x - y - 2 = 0$ are
concurrent, find the value of $k$.

Solution Three lines are said to be concurrent, if they pass through a common point,
i.e., point of intersection of any two lines lies on the third line. Here given lines are
$$2x + y - 3 = 0 \qquad \dots (1)$$
$$5x + ky - 3 = 0 \qquad \dots (2)$$

<!-- page 292 -->
$$3x - y - 2 = 0 \qquad \dots (3)$$

Solving (1) and (3) by cross-multiplication method, we get

$$\frac{x}{-2-3} = \frac{y}{-9+4} = \frac{1}{-2-3} \quad \text{or} \quad x=1, y=1.$$

Therefore, the point of intersection of two lines is $(1, 1)$. Since above three lines are
concurrent, the point $(1, 1)$ will satisfy equation $(2)$ so that

$$5.1 + k . 1 - 3 = 0 \text{ or } k = -2.$$

Example 21 Find the distance of the line $4x - y = 0$ from the point P (4, 1) measured
along the line making an angle of $135^\circ$ with the positive $x$-axis.

Solution Given line is $4x - y = 0$
In order to find the distance of the
line (1) from the point P (4, 1) along
another line, we have to find the point
of intersection of both the lines. For
this purpose, we will first find the
equation of the second line
(Fig 10.21). Slope of second line is
$\tan 135^\circ = -1$. Equation of the line
with slope $- 1$ through the point
P (4, 1) is

Fig 10.21

$$y - 1 = -1 \ (x - 4) \text{ or } x + y - 5 = 0 \quad \dots (2)$$

Solving (1) and (2), we get $x = 1$ and $y = 4$ so that point of intersection of the two lines
is Q (1, 4). Now, distance of line (1) from the point P (4, 1) along the line (2)

= the distance between the points P (4, 1) and Q (1, 4).
$$= \sqrt{(1-4)^2 + (4-1)^2} = 3\sqrt{2} \text{ units.}$$

Example 22 Assuming that straight lines work as the plane mirror for a point, find
the image of the point $(1, 2)$ in the line $x - 3y + 4 = 0$.

Solution Let Q $(h, k)$ is the image of the point P $(1, 2)$ in the line
$$x - 3y + 4 = 0 \qquad \dots (1)$$

<!-- page 293 -->
Y' Fig10.22

Therefore, the line (1) is the perpendicular bisector of line segment PQ (Fig 10.22).

Hence Slope of line PQ = $\frac{-1}{\text{Slope of line } x - 3y + 4 = 0}$,

so that $\frac{k-2}{h-1} = \frac{-1}{\frac{1}{3}}$ or $3h+k=5$ ... (2)

and the mid-point of PQ, i.e., point $\left(\frac{h+1}{2}, \frac{k+2}{2}\right)$ will satisfy the equation (1) so that

$$\frac{h+1}{2} - 3 \left( \frac{k+2}{2} \right) + 4 = 0 \text{ or } h - 3k = -3 \tag{3}$$

Solving (2) and (3), we get $h = \frac{6}{5}$ and $k = \frac{7}{5}$.

Hence, the image of the point $(1, 2)$ in the line $(1)$ is $\left( \frac{6}{5}, \frac{7}{5} \right)$.

Example 23 Show that the area of the triangle formed by the lines


$$y = m_1x + c_1, y = m_2x + c_2 \text{ and } x = 0 \text{ is } \frac{\left(c_1 - c_2\right)^2}{2|m_1 - m_2|}.$$

<!-- page 294 -->
Solution Given lines are

$$y = m_1 x + c_1 \quad \dots (1)$$
$$y = m_2 x + c_2 \quad \dots (2)$$
$$x = 0 \quad \dots (3)$$

We know that line $y = mx + c$ meets
the line $x = 0$ (y-axis) at the point
$(0, c)$. Therefore, two vertices of the
triangle formed by lines (1) to (3) are
$\mathrm{P} (0, c_1)$ and $\mathrm{Q} (0, c_2)$ (Fig 10. 23).
Third vertex can be obtained by
solving equations (1) and (2). Solving
(1) and (2), we get

Fig 10.23

$$x = \frac{(c_2 - c_1)}{(m_1 - m_2)} \text{ and } y = \frac{(m_1 c_2 - m_2 c_1)}{(m_1 - m_2)}$$

Therefore, third vertex of the triangle is R $\left( \frac{(c_2 - c_1)}{(m_1 - m_2)}, \frac{(m_1 c_2 - m_2 c_1)}{(m_1 - m_2)} \right)$.

Now, the area of the triangle is

$$=\frac{1}{2}\left|0\left(\frac{m_{1} c_{2}-m_{2} c_{1}}{m_{1}-m_{2}}-c_{2}\right)+\frac{c_{2}-c_{1}}{m_{1}-m_{2}}\left(c_{2}-c_{1}\right)+0\left(c_{1}-\frac{m_{1} c_{2}-m_{2} c_{1}}{m_{1}-m_{2}}\right)=\frac{\left(c_{2}-c_{1}\right)^{2}}{2\left|m_{1}-m_{2}\right|}\right.$$

Example 24 A line is such that its segment
between the lines
$5x - y + 4 = 0$ and $3x + 4y - 4 = 0$ is bisected at the
point $(1, 5)$. Obtain its equation.

Solution Given lines are
$5x - y + 4 = 0$ ... (1)
$3x + 4y - 4 = 0$ ... (2)
Let the required line intersects the lines (1) and (2)
at the points, $(\alpha_1, \beta_1)$ and $(\alpha_2, \beta_2)$, respectively
(Fig10.24). Therefore
$5\alpha_1 - \beta_1 + 4 = 0$ and
$3 \alpha_2 + 4 \beta_2 - 4 = 0$

Fig 10.24

<!-- page 295 -->
or $\beta_1 = 5\alpha_1 + 4$ and $\beta_2 = \frac{4 - 3\alpha_2}{4}$.

We are given that the mid point of the segment of the required line between $(\alpha_1, \beta_1)$
and $(\alpha_2, \beta_2)$ is $(1, 5)$. Therefore

$$\frac{\alpha_1 + \alpha_2}{2} = 1 \text{ and } \frac{\beta_1 + \beta_2}{2} = 5,$$

or $\alpha_1 + \alpha_2 = 2$ and $\frac{5\alpha_1 + 4 + \frac{4 - 3\alpha_2}{4}}{2} = 5,$

or $\alpha_1 + \alpha_2 = 2$ and $20 \alpha_1 - 3 \alpha_2 = 20$ ... (3)

Solving equations in (3) for $\alpha_1$ and $\alpha_2$, we get

$\alpha_{1}=\frac{26}{23}$ and $\alpha_{2}=\frac{20}{23}$ and hence, $\beta_{1}=5.\frac{26}{23}+4=\frac{222}{23}$.

Equation of the required line passing through $(1, 5)$ and $(\alpha_1, \beta_1)$ is

$$y-5 = \frac{\beta_1 - 5}{\alpha_1 - 1} (x-1)_{\text{or}} \quad y-5 = \frac{\frac{222}{23} - 5}{\frac{26}{23} - 1} (x-1)$$

or $107x - 3y - 92 = 0,$

which is the equation of required line.

Example 25 Show that the path of a moving point such that its distances from two
lines $3x - 2y = 5$ and $3x + 2y = 5$ are equal is a straight line.

Solution Given lines are
$$3x - 2y = 5 \quad \dots (1)$$
and $$3x + 2y = 5 \quad \dots (2)$$
Let $(h, k)$ is any point, whose distances from the lines (1) and (2) are equal. Therefore
$$\frac{|3h - 2k - 5|}{\sqrt{9 + 4}} = \frac{|3h + 2k - 5|}{\sqrt{9 + 4}} \text{ or } |3h - 2k - 5| = |3h + 2k - 5|,$$
which gives $3h - 2k - 5 = 3h + 2k - 5$ or $- (3h - 2k - 5) = 3h + 2k - 5$.

<!-- page 296 -->
Solving these two relations we get $k = 0$ or $h = \frac{5}{3}$. Thus, the point $(h, k)$ satisfies the


equations $y = 0$ or $x = \frac{5}{3}$, which represent straight lines. Hence, path of the point


equidistant from the lines (1) and (2) is a straight line.

Miscellaneous Exercise on Chapter 10

1. Find the values of $k$ for which the line $(k-3)x - (4-k^2)y + k^2 - 7k + 6 = 0$ is
(a) Parallel to the $x$-axis,
(b) Parallel to the $y$-axis,
(c) Passing through the origin.
2. Find the values of $\theta$ and $p$, if the equation $x \cos \theta + y \sin \theta = p$ is the normal form
of the line $\sqrt{3}x + y + 2 = 0$.
3. Find the equations of the lines, which cut-off intercepts on the axes whose sum
and product are $1$ and $-6$, respectively.
4. What are the points on the $y$-axis whose distance from the line $\frac{x}{3} + \frac{y}{4} = 1$ is
$4$ units.
5. Find perpendicular distance from the origin to the line joining the points $(\cos \theta, \sin \theta)$
and $(\cos \phi, \sin \phi)$.
6. Find the equation of the line parallel to $y$-axis and drawn through the point of
intersection of the lines $x - 7y + 5 = 0$ and $3x + y = 0$.
7. Find the equation of a line drawn perpendicular to the line $\frac{x}{4} + \frac{y}{6} = 1$ through the
point, where it meets the $y$-axis.
8. Find the area of the triangle formed by the lines $y - x = 0$, $x + y = 0$ and $x - k = 0$.
9. Find the value of $p$ so that the three lines $3x + y - 2 = 0$, $px + 2y - 3 = 0$ and
$2x - y - 3 = 0$ may intersect at one point.
10. If three lines whose equations are $y = m_1x + c_1$, $y = m_2x + c_2$ and $y = m_3x + c_3$ are
concurrent, then show that $m_1(c_2 - c_3) + m_2(c_3 - c_1) + m_3(c_1 - c_2) = 0$.
11. Find the equation of the lines through the point $(3, 2)$ which make an angle of $45^\circ$
with the line $x - 2y = 3$.
12. Find the equation of the line passing through the point of intersection of the lines
$4x + 7y - 3 = 0$ and $2x - 3y + 1 = 0$ that has equal intercepts on the axes.

<!-- page 297 -->
13. Show that the equation of the line passing through the origin and making an angle
$\theta$ with the line $y = mx + c$ is $\frac{y}{x} = \frac{m \pm \tan}{1 \mp m \tan}$ .
14. In what ratio, the line joining $(-1, 1)$ and $(5, 7)$ is divided by the line $x + y = 4$?
15. Find the distance of the line $4x + 7y + 5 = 0$ from the point $(1, 2)$ along the line
$2x - y = 0$.
16. Find the direction in which a straight line must be drawn through the point $(-1, 2)$
so that its point of intersection with the line $x + y = 4$ may be at a distance of
3 units from this point.
17. The hypotenuse of a right angled triangle has its ends at the points $(1, 3)$ and
$(-4, 1)$. Find an equation of the legs (perpendicular sides) of the triangle.
18. Find the image of the point $(3, 8)$ with respect to the line $x + 3y = 7$ assuming the
line to be a plane mirror.
19. If the lines $y = 3x + 1$ and $2y = x + 3$ are equally inclined to the line $y = mx + 4$, find
the value of $m$.
20. If sum of the perpendicular distances of a variable point P $(x, y)$ from the lines
$x + y - 5 = 0$ and $3x - 2y + 7 = 0$ is always 10. Show that P must move on a line.
21. Find equation of the line which is equidistant from parallel lines $9x + 6y - 7 = 0$
and $3x + 2y + 6 = 0$.
22. A ray of light passing through the point $(1, 2)$ reflects on the $x$-axis at point A and the
reflected ray passes through the point $(5, 3)$. Find the coordinates of A.
23. Prove that the product of the lengths of the perpendiculars drawn from the
points $\left(\sqrt{a^2 - b^2}, 0\right)$ and $\left(-\sqrt{a^2 - b^2}, 0\right)$ to the line $\frac{x}{a} \cos \theta + \frac{y}{b} \sin \theta = 1$ is $b^2$.
24. A person standing at the junction (crossing) of two straight paths represented by
the equations $2x - 3y + 4 = 0$ and $3x + 4y - 5 = 0$ wants to reach the path whose
equation is $6x - 7y + 8 = 0$ in the least time. Find equation of the path that he
should follow.

24. A person standing at the junction (crossing) of two straight paths represented by
the equations $2x - 3y + 4 = 0$ and $3x + 4y - 5 = 0$ wants to reach the path whose
equation is $6x - 7y + 8 = 0$ in the least time. Find equation of the path that he
should follow.

Summary

$\diamond$ Slope ($m$) of a non-vertical line passing through the points $(x_1, y_1)$ and $(x_2, y_2)$

is given by $m = \frac{y_2 - y_1}{x_2 - x_1} = \frac{y_1 - y_2}{x_1 - x_2}, \quad x_1 \neq x_2.$

$\diamond$ If a line makes an angle á with the positive direction of $x$-axis, then the slope
of the line is given by $m = \tan \alpha, \alpha \neq 90^\circ.$
$\diamond$ Slope of horizontal line is zero and slope of vertical line is undefined.

<!-- page 298 -->
$\diamond$ An acute angle (say $\theta$) between lines $\text{L}_1$ and $\text{L}_2$ with slopes $m_1$ and $m_2$ is

given by $\tan\theta = \left| \frac{m_2 - m_1}{1 + m_1 m_2} \right|, 1 + m_1 m_2 \neq 0$.

$\diamond$ Two lines are $parallel$ if and only if their slopes are equal.
$\diamond$ Two lines are $perpendicular$ if and only if product of their slopes is $-1$.
$\diamond$ Three points A, B and C are collinear, if and only if slope of AB = slope of BC.
$\diamond$ Equation of the horizontal line having distance $a$ from the $x$-axis is either
$y = a$ or $y = -a$.
$\diamond$ Equation of the vertical line having distance $b$ from the $y$-axis is either
$x = b$ or $x = -b$.
$\diamond$ The point $(x, y)$ lies on the line with slope $m$ and through the fixed point $(x_o, y_o)$,
if and only if its coordinates satisfy the equation $y - y_o = m(x - x_o)$.
$\diamond$ Equation of the line passing through the points $(x_1, y_1)$ and $(x_2, y_2)$ is given by

$$y - y_1 = \frac{y_2 - y_1}{x_2 - x_1}(x - x_1).$$

$\diamond$ The point $(x, y)$ on the line with slope $m$ and $y$-intercept $c$ lies on the line if and
only if $y = mx + c$.
$\diamond$ If a line with slope $m$ makes $x$-intercept $d$. Then equation of the line is
$y = m(x - d)$.
$\diamond$ Equation of a line making intercepts $a$ and $b$ on the $x$-and $y$-axis,

respectively, is $\frac{x}{a} + \frac{y}{b} = 1$.
$\diamond$ The equation of the line having normal distance from origin $p$ and angle between
normal and the positive $x$-axis $\omega$ is given by $x \cos \omega - y \sin \omega = p$.
$\diamond$ Any equation of the form $Ax + By + C = 0$, with A and B are not zero,
simultaneously, is called the $general$ $linear$ $equation$ or $general$ $equation$ $of$
$a$ $line$.
$\diamond$ The perpendicular distance $(d)$ of a line $Ax + By + C = 0$ from a point $(x_1, y_1)$

is given by $d = \frac{|Ax_1 + By_1 + C|}{\sqrt{A^2 + B^2}}$.
$\diamond$ Distance between the parallel lines $Ax + By + C_1 = 0$ and $Ax + By + C_2 = 0$,

is given by $d = \frac{|C_1 - C_2|}{\sqrt{A^2 + B^2}}$.

<!-- page 299 -->
Chapter 11

CONICSECTIONS

❖ Let the relation of knowledge to real life be very visible to your pupils
and let them understand how by knowledge the world could be
transformed. – BERTRAND RUSSELL ❖

11.1 Introduction

In the preceding Chapter 10, we have studied various forms
of the equations of a line. In this Chapter, we shall study
about some other curves, viz., circles, ellipses, parabolas
and hyperbolas. The names parabola and hyperbola are
given by Apollonius. These curves are in fact, known as
*conic sections* or more commonly *conics* because they
can be obtained as intersections of a plane with a double
napped right circular cone. These curves have a very wide
range of applications in fields such as planetary motion,
design of telescopes and antennas, reflectors in flashlights
and automobile headlights, etc. Now, in the subsequent sections we will see how the
intersection of a plane with a double napped right circular cone
results in different types of curves.

11.2 Sections of a Cone

Let $l$ be a fixed vertical line and $m$ be another line intersecting it at
a fixed point V and inclined to it at an angle $\alpha$ (Fig11.1).

Fig 11. 1

Suppose we rotate the line $m$ around the line $l$ in such a way
that the angle $\alpha$ remains constant. Then the surface generated is
a double-napped right circular hollow cone herein after referred as

<!-- page 300 -->
Fig 11. 2

Fig 11. 3

cone and extending indefinitely far in both directions (Fig11.2).

The point V is called the vertex; the line $l$ is the axis of the cone. The rotating line
$m$ is called a generator of the cone. The vertex separates the cone into two parts
called nappes.

If we take the intersection of a plane with a cone, the section so obtained is called
a $conic$ $section$. Thus, conic sections are the curves obtained by intersecting a right
circular cone by a plane.

We obtain different kinds of conic sections depending on the position of the
intersecting plane with respect to the cone and by the angle made by it with the vertical
axis of the cone. Let $\beta$ be the angle made by the intersecting plane with the vertical
axis of the cone (Fig11.3).

The intersection of the plane with the cone can take place either at the vertex of
the cone or at any other part of the nappe either below or above the vertex.

11.2.1 Circle, ellipse, parabola and hyperbola When the plane cuts the nappe (other
than the vertex) of the cone, we have the following situations:

(a) When $\beta = 90^{\circ}$, the section is a $circle$ (Fig11.4).
(b) When $\alpha < \beta < 90^{\circ}$, the section is an $ellipse$ (Fig11.5).
(c) When $\beta = \alpha$; the section is a $parabola$ (Fig11.6).
(In each of the above three situations, the plane cuts entirely across one nappe of
the cone).

(d) When $0 \le \beta < \alpha$; the plane cuts through both the nappes and the curves of
intersection is a $hyperbola$ (Fig11.7).

<!-- page 301 -->
Fig 11. 4

Fig 11. 5

Fig 11. 6

Fig 11. 7

11.2.2 Degenerated conic sections

When the plane cuts at the vertex of the cone, we have the following different cases:
(a) When $\alpha < \beta \le 90^{\circ}$, then the section is a point (Fig11.8).

(b) When $\beta = \alpha$, the plane contains a generator of the cone and the section is a
straight line (Fig11.9).
It is the degenerated case of a parabola.

(c) When $0 \le \beta < \alpha$, the section is a pair of intersecting straight lines (Fig11.10). It is
the degenerated case of a $hyperbola$.

<!-- page 302 -->
In the following sections, we shall obtain the equations of each of these conic
sections in standard form by defining them based on geometric properties.

Fig 11. 8

Fig 11. 9

(a)

Fig 11. 10 (b)

11.3 Circle

Definition 1 A circle is the set of all points in a plane that are equidistant from a fixed
point in the plane.

The fixed point is called the centre of the circle and the distance from the centre
to a point on the circle is called the radius of the circle (Fig 11.11).

<!-- page 303 -->
Fig 11. 11

Fig 11. 12

The equation of the circle is simplest if the centre of the circle is at the origin.
However, we derive below the equation of the circle with a given centre and radius
(Fig 11.12).

Given C ($h, k$) be the centre and $r$ the radius of circle. Let P($x, y$) be any point on
the circle (Fig11.12). Then, by the definition, | CP | = $r$ . By the distance formula,
we have

$$\sqrt{(x-h)^2 + (y-k)^2} = r$$
$$(x-h)^2 + (y-k)^2 = r^2$$

i.e.                                                                 $(x - h)^2 + (y - k)^2 = r^2$

This is the required equation of the circle with centre at $(h,k)$ and radius $r$ .

Example 1 Find an equation of the circle with centre at $(0,0)$ and radius $r$.

Solution Here $h = k = 0$. Therefore, the equation of the circle is $x^2 + y^2 = r^2$.

Example 2 Find the equation of the circle with centre $(-3, 2)$ and radius 4.

Solution Here $h = -3$, $k = 2$ and $r = 4$. Therefore, the equation of the required circle is

$$(x + 3)^2 + (y - 2)^2 = 16$$

Example 3 Find the centre and the radius of the circle $x^2 + y^2 + 8x + 10y - 8 = 0$

Solution The given equation is

$$(x^2 + 8x) + (y^2 + 10y) = 8$$

Now, completing the squares within the parenthesis, we get

$$(x^2 + 8x + 16) + (y^2 + 10y + 25) = 8 + 16 + 25$$

i.e. $$(x + 4)^2 + (y + 5)^2 = 49$$

i.e. $\{x - (-4)\}^2 + \{y - (-5)\}^2 = 7^2$

Therefore, the given circle has centre at $(-4, -5)$ and radius $7$.

Therefore, the given circle has centre at $(-4, -5)$ and radius $7$.

<!-- page 304 -->
Example 4 Find the equation of the circle which passes through the points $(2, -2)$, and
$(3,4)$ and whose centre lies on the line $x + y = 2$.

Solution Let the equation of the circle be $(x - h)^2 + (y - k)^2 = r^2$.

Since the circle passes through $(2, -2)$ and $(3,4)$, we have
$$(2 - h)^2 + (-2 - k)^2 = r^2 \quad \dots (1)$$
and $(3 - h)^2 + (4 - k)^2 = r^2 \quad \dots (2)$$Also since the centre lies on the line $x + y = 2$, we have$$h + k = 2 \quad \dots (3)$$Solving the equations (1), (2) and (3), we get$$h = 0.7, \quad k = 1.3 \text{ and } r^2 = 12.58$$Hence, the equation of the required circle is$$(x - 0.7)^2 + (y - 1.3)^2 = 12.58.$$

EXERCISE 11.1

In each of the following Exercises 1 to 5, find the equation of the circle with

1. centre $(0,2)$ and radius 2
2. centre $(-2,3)$ and radius 4
3. centre $(\frac{1}{2}, \frac{1}{4})$ and radius $\frac{1}{12}$
4. centre $(1,1)$ and radius $\sqrt{2}$

5. centre $(-a, -b)$ and radius $\sqrt{a^2 - b^2}$.
In each of the following Exercises 6 to 9, find the centre and radius of the circles.
6. $(x + 5)^2 + (y - 3)^2 = 36$
7. $x^2 + y^2 - 4x - 8y - 45 = 0$
8. $x^2 + y^2 - 8x + 10y - 12 = 0$
9. $2x^2 + 2y^2 - x = 0$
10. Find the equation of the circle passing through the points $(4,1)$ and $(6,5)$ and
whose centre is on the line $4x + y = 16$.
11. Find the equation of the circle passing through the points $(2,3)$ and $(-1,1)$ and
whose centre is on the line $x - 3y - 11 = 0$.
12. Find the equation of the circle with radius 5 whose centre lies on $x$-axis and
passes through the point $(2,3)$.
13. Find the equation of the circle passing through $(0,0)$ and making intercepts $a$ and
$b$ on the coordinate axes.
14. Find the equation of a circle with centre $(2,2)$ and passes through the point $(4,5)$.
15. Does the point $(-2.5, 3.5)$ lie inside, outside or on the circle $x^2 + y^2 = 25$?

<!-- page 305 -->
11.4 Parabola

Definition 2 A parabola is the set of all points
in a plane that are equidistant from a fixed line
and a fixed point (not on the line) in the plane.

The fixed line is called the \textit{directrix} of
the parabola and the fixed point F is called the
\textit{focus} (Fig 11.13). (‘Para’ means ‘for’ and
‘bola’ means ‘throwing’, i.e., the shape
described when you throw a ball in the air).

Fig 11. 13

**Note** If the fixed point lies on the fixed
line, then the set of points in the plane, which
are equidistant from the fixed point and the
fixed line is the straight line through the fixed
point and perpendicular to the fixed line. We
call this straight line as *degenerate case* of
the parabola.

A line through the focus and perpendicular
to the $directrix$ is called the $axis$ of the
parabola. The point of intersection of parabola
with the axis is called the vertex of the parabola
(Fig11.14).

11.4.1 Standard equations of parabola The

11.4.1 Standard equations of parabola The                                     Fig 11.14
equation of a parabola is simplest if the vertex
is at the origin and the axis of symmetry is along the $x$-axis or $y$-axis. The four possible
such orientations of parabola are shown below in  Fig 11.15 (a) to (d).

(a)

(b)

<!-- page 306 -->
(c)                  Fig 11.15 (a) to (d)                  (d)

We will derive the equation for the parabola shown above in Fig 11.15 (a) with
$focus$ at $(a, 0) \ a > 0$; and directricx $x = - \ a$ as below:

Let F be the focus and $l$ the directrix. Let
FM be perpendicular to the directrix and bisect
FM at the point O. Produce MO to X. By the
definition of parabola, the mid-point O is on the
parabola and is called the vertex of the parabola.
Take O as origin, OX the $x$-axis and OY
perpendicular to it as the $y$-axis. Let the distance
from the directrix to the focus be $2a$. Then, the
coordinates of the focus are $(a, 0)$, and the
equation of the directrix is $x + a = 0$ as in Fig11.16.
Let P$(x, y)$ be any point on the parabola such that

Fig 11.16

... (1)

$$PF = PB,$$

where PB is perpendicular to $l$. The coordinates of B are $(- a, y)$. By the distance
formula, we have

$$PF = \sqrt{(x-a)^2 + y^2} \text{ and } PB = \sqrt{(x+a)^2}$$

Since $PF = PB$, we have

$$\sqrt{(x-a)^2 + y^2} = \sqrt{(x+a)^2}$$

i.e. $(x - a)^2 + y^2 = (x + a)^2$

or $x^2 - 2ax + a^2 + y^2 = x^2 + 2ax + a^2$

or $y^2 = 4ax \ ( \ a > 0).$

<!-- page 307 -->
Hence, any point on the parabola satisfies
$$y^2 = 4ax. \hfill ... (2)$$

Conversely, let $P(x, y)$ satisfy the equation (2)

$$\text{PF} \quad = \sqrt{(x-a)^2 + y^2} \quad = \sqrt{(x-a)^2 + 4ax}$$

$$= \sqrt{(x+a)^2} = \text{PB} \qquad \dots (3)$$

and so $P(x,y)$ lies on the parabola.

Thus, from (2) and (3) we have proved that the equation to the parabola with
vertex at the origin, focus at $(a,0)$ and directrix $x = - a$ is $y^2 = 4ax$.

**Discussion** In equation (2), since $a > 0$, $x$ can assume any positive value or zero but
no negative value and the curve extends indefinitely far into the first and the fourth
quadrants. The axis of the parabola is the positive $x$-axis.

Similarly, we can derive the equations of the parabolas in:

Fig 11.15 (b) as $y^2 = -4ax$,
Fig 11.15 (c) as $x^2 = 4ay$,
Fig 11.15 (d) as $x^2 = -4ay$,

These four equations are known as standard equations of parabolas.

Note The standard equations of parabolas have focus on one of the coordinate
axis; vertex at the origin and thereby the directrix is parallel to the other coordinate
axis. However, the study of the equations of parabolas with focus at any point and
any line as directrix is beyond the scope here.

From the standard equations of the parabolas, Fig11.15, we have the following
observations:

1. Parabola is symmetric with respect to the axis of the parabola.If the equation
has a $y^2$ term, then the axis of symmetry is along the $x$-axis and if the
equation has an $x^2$ term, then the axis of symmetry is along the $y$-axis.
2. When the axis of symmetry is along the $x$-axis the parabola opens to the
(a) right if the coefficient of $x$ is positive,
(b) left if the coefficient of $x$ is negative.
3. When the axis of symmetry is along the $y$-axis the parabola opens
(c) upwards if the coefficient of $y$ is positive.
(d) downwards if the coefficient of $y$ is negative.

<!-- page 308 -->
11.4.2 Latus rectum

Definition 3 Latus rectum of a parabola is a line segment perpendicular to the axis of
the parabola, through the focus and whose end points lie on the parabola (Fig11.17).

To find the Length of the latus rectum of the parabola $y^2 = 4ax$ (Fig 11.18).

By the definition of the parabola, $AF = AC$.

But $\mathrm{AC} = \mathrm{FM} = 2a$
Hence $\mathrm{AF} = 2a.$

And since the parabola is symmetric with respect to $x$-axis AF = FB and so

$$AB = \text{Length of the latus rectum} = 4a.$$

Fig 11.17

Fig 11.18

Example 5 Find the coordinates of the focus, axis,
the equation of the directrix and latus rectum of
the parabola $y^2 = 8x$.

Solution The given equation involves $y^2$, so the
axis of symmetry is along the $x$-axis.
The coefficient of $x$ is positive so the parabola opens
to the right. Comparing with the given equation
$y^2 = 4ax$, we find that $a = 2$.

Thus, the focus of the parabola is $(2, 0)$ and the equation of the directrix of the parabola
is $x = -2$ (Fig 11.19).

Length of the latus rectum is $4a = 4 \times 2 = 8$.

Length of the latus rectum is $4a = 4 \times 2 = 8.$

<!-- page 309 -->
Example 6 Find the equation of the parabola with focus $(2,0)$ and directrix $x = -2$.

Solution Since the focus $(2,0)$ lies on the $x$-axis, the $x$-axis itself is the axis of the
parabola. Hence the equation of the parabola is of the form either
$y^2 = 4ax$ or $y^2 = -4ax$. Since the directrix is $x = -2$ and the focus is $(2,0)$, the parabola
is to be of the form $y^2 = 4ax$ with $a = 2$. Hence the required equation is
$$y^2 = 4(2)x = 8x$$

Example 7 Find the equation of the parabola with vertex at $(0, 0)$ and focus at $(0, 2)$.

Solution Since the vertex is at $(0,0)$ and the focus is at $(0,2)$ which lies on $y$-axis, the
$y$-axis is the axis of the parabola. Therefore, equation of the parabola is of the form
$x^2 = 4ay$. thus, we have

$$x^2 = 4(2)y, \text{ i.e., } x^2 = 8y.$$

Example 8 Find the equation of the parabola which is symmetric about the y-axis, and
passes through the point $(2,-3)$.

Solution Since the parabola is symmetric about $y$-axis and has its vertex at the origin,
the equation is of the form $x^2 = 4ay$ or $x^2 = - 4ay$, where the sign depends on whether
the parabola opens upwards or downwards. But the parabola passes through $(2,-3)$
which lies in the fourth quadrant, it must open downwards. Thus the equation is of
the form $x^2 = - 4ay$.

Since the parabola passes through ( 2,−3), we have

$$2^2 = -4a (-3), \text{ i.e., } a = \frac{1}{3}$$

Therefore, the equation of the parabola is

$$x^2 = -4 \left( \frac{1}{3} \right) y, \text{ i.e., } 3x^2 = -4y.$$

EXERCISE 11.2

In each of the following Exercises 1 to 6, find the coordinates of the focus, axis of the
parabola, the equation of the directrix and the length of the latus rectum.

1. $y^2 = 12x$
2. $x^2 = 6y$
3. $y^2 = -8x$
4. $x^2 = -16y$
5. $y^2 = 10x$
6. $x^2 = -9y$

In each of the Exercises 7 to 12, find the equation of the parabola that satisfies the
given conditions:

<!-- page 310 -->
7. Focus $(6,0)$; directrix $x = -6$
9. Vertex $(0,0)$; focus $(3,0)$
10. Vertex $(0,0)$; focus $(-2,0)$
11. Vertex $(0,0)$ passing through $(2,3)$ and axis is along $x$-axis.
12. Vertex $(0,0)$, passing through $(5,2)$ and symmetric with respect to $y$-axis.

11.5 Ellipse

Definition 4 An $ellipse$ is the set of all points in
a plane, the sum of whose distances from two
fixed points in the plane is a constant.

The two fixed points are called the $foci$ (plural
of '$focus$') of the ellipse (Fig11.20).

Note The constant which is the sum of
the distances of a point on the ellipse from the
two fixed points is always greater than the
distance between the two fixed points.

$$\mathbf{P}_1\mathbf{F}_1 + \mathbf{P}_1\mathbf{F}_2 = \mathbf{P}_2\mathbf{F}_1 + \mathbf{P}_2\mathbf{F}_2 = \mathbf{P}_3\mathbf{F}_1 + \mathbf{P}_3\mathbf{F}_2$$
Fig 11.20

The mid point of the line segment joining the foci is called the $centre$ of the
ellipse. The line segment through the foci of the ellipse is called the $major$ $axis$ and the
line segment through the centre and perpendicular to the major axis is called the $minor$
$axis$. The end points of the major axis are called the $vertices$ of the ellipse(Fig 11.21).

Fig 11.21

Fig 11.22

We denote the length of the major axis by $2a$, the length of the minor axis by $2b$
and the distance between the foci by $2c$. Thus, the length of the semi major axis is $a$
and semi-minor axis is $b$ (Fig11.22).

<!-- page 311 -->
11.5.1 Relationship between semi-major
axis, semi-minor axis and the distance of
the focus from the centre of the ellipse
(Fig 11.23).

Fig 11.23

Take a point P at one end of the major axis. R
Sum of the distances of the point P to the
foci is $F_1 P + F_2 P = F_1 O + OP + F_2 P$

(Since, $F_1P = F_1O + OP$)
$= c + a + a - c = 2a$

Take a point Q at one end of the minor axis.
Sum of the distances from the point Q to the foci is

$$F_1Q + F_2Q = \sqrt{b^2 + c^2} + \sqrt{b^2 + c^2} = 2\sqrt{b^2 + c^2}$$

Since both $P$ and $Q$ lies on the ellipse.

By the definition of ellipse, we have

$$2\sqrt{b^2 + c^2} = 2a, \text{ i.e., } \quad a = \sqrt{b^2 + c^2}$$

$$a^2 = b^2 + c^2, \text{ i.e., } \quad c = \sqrt{a^2 - b^2}$$

11.5.2 Special cases of an ellipse In the equation
$c^2 = a^2 - b^2$ obtained above, if we keep $a$ fixed and
vary $c$ from $0$ to $a$, the resulting ellipses will vary in
shape.

Fig 11.24

Case (i) When $c = 0$, both foci merge together with
the centre of the ellipse and $a^2 = b^2$, i.e., $a = b$, and so
the ellipse becomes circle (Fig11.24). Thus, circle is a
special case of an ellipse which is dealt in Section 11.3.

Case (ii) When $c = a$, then $b = 0$. The ellipse reduces
to the line segment $\text{F}_1\text{F}_2$ joining the two foci (Fig11.25).

Fig 11.25

11.5.3 Eccentricity

Definition 5 The eccentricity of an ellipse is the ratio of the distances from the centre
of the ellipse to one of the foci and to one of the vertices of the ellipse (eccentricity is

denoted by $e$) i.e., $e = \frac{c}{a}$.

<!-- page 312 -->
Then since the focus is at a distance of $c$ from the centre, in terms of the eccentricity
the focus is at a distance of $ae$ from the centre.

11.5.4 *Standard equations of an ellipse* The equation of an ellipse is simplest if the
centre of the ellipse is at the origin and the foci are

Fig 11.26 (b)

on the $x$-axis or $y$-axis. The two such possible orientations are shown in Fig 11.26.

We will derive the equation for the ellipse shown above in Fig 11.26 (a) with foci
on the $x$-axis.

Let $\mathrm{F}_1$ and $\mathrm{F}_2$ be the foci and $\mathrm{O}$ be the midpoint of the line segment $\mathrm{F}_1\mathrm{F}_2$. Let $\mathrm{O}$ be the origin
and the line from $\mathrm{O}$ through $\mathrm{F}_2$ be the positive
$x$-axis and that through $\mathrm{F}_1$ as the negative $x$-axis.
Let, the line through $\mathrm{O}$ perpendicular to the
$x$-axis be the $y$-axis. Let the coordinates of $\mathrm{F}_1$ be
$(-c, 0)$ and $\mathrm{F}_2$ be $(c, 0)$ (Fig 11.27).

Let $P(x, y)$ be any point on the ellipse such
that the sum of the distances from $P$ to the two
foci be $2a$ so given

Fig 11.27

$$PF_1 + PF_2 = 2a. \dots (1)$$

Using the distance formula, we have

$$\sqrt{(x+c)^2 + y^2} + \sqrt{(x-c)^2 + y^2} = 2a$$

i.e., $\sqrt{(x+c)^2 + y^2} = 2a - \sqrt{(x-c)^2 + y^2}$

<!-- page 313 -->
Squaring both sides, we get

$$(x+c)^2 + y^2 = 4a^2 - 4a \sqrt{(x-c)^2 + y^2} + (x-c)^2 + y^2$$

which on simplification gives

$$\sqrt{(x-c)^2 + y^2} = a - \frac{c}{a} x$$

Squaring again and simplifying, we get

$$\frac{x^2}{a^2} + \frac{y^2}{a^2 - c^2} = 1$$

i.e., $\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1$ (Since $c^2 = a^2 - b^2$)

Hence any point on the ellipse satisfies

$$\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1. \qquad \dots (2)$$

Conversely, let $\mathrm{P} (x, y)$ satisfy the equation (2) with $0 < c < a$. Then

$$y^2 = b^2 \left( 1 - \frac{x^2}{a^2} \right)$$

Therefore, $PF_1$ $\quad = \sqrt{(x+c)^2 + y^2}$

$\quad \quad \quad \quad \quad = \sqrt{(x+c)^2 + b^2 \left( \frac{a^2 - x^2}{a^2} \right)}$

$\quad \quad \quad \quad \quad = \sqrt{(x+c)^2 + (a^2 - c^2) \left( \frac{a^2 - x^2}{a^2} \right)} \text{ (since } b^2 = a^2 - c^2)$

$\quad \quad \quad \quad \quad = \sqrt{\left( a + \frac{cx}{a} \right)^2} = a + \frac{c}{a}x$

Similarly $\text{PF}_2 = a - \frac{c}{a}x$

<!-- page 314 -->
Hence $\text{PF}_1 + \text{PF}_2 = a + \frac{c}{a}x + a - \frac{c}{a}x = 2a \quad \dots (3)$

So, any point that satisfies $\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1$, satisfies the geometric condition and so

$$\mathrm{P}(x, y) \text{ lies on the ellipse.}$$

Hence from (2) and (3), we proved that the equation of an ellipse with centre of
the origin and major axis along the $x$-axis is

$$\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1.$$

**Discussion** From the equation of the ellipse obtained above, it follows that for every
point P $(x, y)$ on the ellipse, we have

$$\frac{x^2}{a^2} = 1 - \frac{y^2}{b^2} \le 1, \text{ i.e., } x^2 \le a^2, \text{ so } -a \le x \le a.$$

Therefore, the ellipse lies between the lines $x = - a$ and $x = a$ and touches these lines.
Similarly, the ellipse lies between the lines $y = - b$ and $y = b$ and touches these
lines.

Similarly, we can derive the equation of the ellipse in Fig 11.26 (b) as $\frac{x^2}{b^2} + \frac{y^2}{a^2} = 1$.

These two equations are known as $standard$ $equations$ of the ellipses.

Note The standard equations of ellipses have centre at the origin and the
major and minor axis are coordinate axes. However, the study of the ellipses with
centre at any other point, and any line through the centre as major and the minor
axes passing through the centre and perpendicular to major axis are beyond the
scope here.

From the standard equations of the ellipses (Fig11.26), we have the following
observations:

1. Ellipse is symmetric with respect to both the coordinate axes since if $(x, y)$ is a
point on the ellipse, then $(-x, y)$, $(x, -y)$ and $(-x, -y)$ are also points on the ellipse.
2. The foci always lie on the major axis. The major axis can be determined by
finding the intercepts on the axes of symmetry. That is, major axis is along the $x$-axis
if the coefficient of $x^2$ has the larger denominator and it is along the $y$-axis if the
coefficient of $y^2$ has the larger denominator.

<!-- page 315 -->
11.5.5 Latus rectum

Definition 6 Latus rectum of an ellipse is a
line segment perpendicular to the major axis
through any of the foci and whose end points
lie on the ellipse (Fig 11.28).

Fig 11. 28

To find the length of the latus rectum

of the ellipse $\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1$

Let the length of $\text{AF}_2$ be $l$.

Then the coordinates of A are $(c, l)$,i.e.,
$(ae, l)$

Since A lies on the ellipse $\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1$, we have

$$\frac{(ae)^2}{a^2} + \frac{l^2}{b^2} = 1$$

$$\Rightarrow l^2 = b^2 (1 - e^2)$$

But $e^2 = \frac{c^2}{a^2} = \frac{a^2 - b^2}{a^2} = 1 - \frac{b^2}{a^2}$

Therefore $l^2 = \frac{b^4}{a^2}$, i.e., $l = \frac{b^2}{a}$

Since the ellipse is symmetric with respect to $y$-axis (of course, it is symmetric w.r.t.

both the coordinate axes), $\text{AF}_2 = \text{F}_2\text{B}$ and so length of the latus rectum is $\frac{2b^2}{a}$.

Example 9 Find the coordinates of the foci, the vertices, the length of major axis, the
minor axis, the eccentricity and the latus rectum of the ellipse

$$\frac{x^2}{25} + \frac{y^2}{9} = 1$$

Solution Since denominator of $\frac{x^2}{25}$ is larger than the denominator of $\frac{y^2}{9}$, the major

<!-- page 316 -->
axis is along the $x$-axis. Comparing the given equation with $\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1$, we get

$a = 5$ and $b = 3$. Also

$$c = \sqrt{a^2 - b^2} = \sqrt{25 - 9} = 4$$

Therefore, the coordinates of the foci are $(-4,0)$ and $(4,0)$, vertices are $(-5,0)$ and
$(5,0)$. Length of the major axis is 10 units length of the minor axis $2b$ is 6 units and the

eccentricity is $\frac{4}{5}$ and latus rectum is $\frac{2b^2}{a} = \frac{18}{5}$ .

Example 10 Find the coordinates of the foci, the vertices, the lengths of major and
minor axes and the eccentricity of the ellipse $9x^2 + 4y^2 = 36$.

Solution The given equation of the ellipse can be written in standard form as

$$\frac{x^2}{4} + \frac{y^2}{9} = 1$$

Since the denominator of $\frac{y^2}{9}$ is larger than the denominator of $\frac{x^2}{4}$, the major axis is
along the $y$-axis. Comparing the given equation with the standard equation

$\frac{x^2}{b^2} + \frac{y^2}{a^2} = 1$, we have $b = 2$ and $a = 3$.

Also $c = \sqrt{a^2 - b^2} = \sqrt{9 - 4} = \sqrt{5}$

and $e = \frac{c}{a} = \frac{\sqrt{5}}{3}$

Hence the foci are $(0, \sqrt{5})$ and $(0, -\sqrt{5})$, vertices are $(0,3)$ and $(0, -3)$, length of the
major axis is 6 units, the length of the minor axis is 4 units and the eccentricity of the
ellipse is $\frac{\sqrt{5}}{3}$.

Example 11 Find the equation of the ellipse whose vertices are $(\pm 13, 0)$ and foci are
$(\pm 5, 0)$.

Solution Since the vertices are on $x$-axis, the equation will be of the form

$$\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1, \text{ where } a \text{ is the semi-major axis.}$$

<!-- page 317 -->
Given that $a = 13$, $c = \pm 5$.

Therefore, from the relation $c^2 = a^2 - b^2$, we get

$$25 = 169 - b^2, \text{ i.e., } b = 12$$

Hence the equation of the ellipse is $\frac{x^2}{169} + \frac{y^2}{144} = 1.$

Example 12 Find the equation of the ellipse, whose length of the major axis is 20 and
foci are $(0, \pm 5)$.

Solution Since the foci are on y-axis, the major axis is along the y-axis. So, equation

of the ellipse is of the form $\frac{x^2}{b^2} + \frac{y^2}{a^2} = 1$.

Given that

$$a = \text{semi-major axis} = \frac{20}{2} = 10$$

and the relation $c^2 = a^2 - b^2$ gives
$5^2 = 10^2 - b^2$ i.e., $b^2 = 75$

Therefore, the equation of the ellipse is

$$\frac{x^2}{75} + \frac{y^2}{100} = 1$$

Example 13 Find the equation of the ellipse, with major axis along the $x$-axis and
passing through the points $(4, 3)$ and $(-1, 4)$.

Solution The standard form of the ellipse is $\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1$. Since the points $(4, 3)$
and $(-1, 4)$ lie on the ellipse, we have

$$\frac{16}{a^2} + \frac{9}{b^2} = 1 \qquad \dots (1)$$

and $$\frac{1}{a^2} + \frac{16}{b^2} = 1 \dots (2)$$

Solving equations (1) and (2), we find that $a^2 = \frac{247}{7}$ and $b^2 = \frac{247}{15}$ .

Hence the required equation is

<!-- page 318 -->
$$\frac{x^2}{\left(\frac{247}{7}\right)} + \frac{y^2}{15} = 1, \text{ i.e., } 7x^2 + 15y^2 = 247.$$

EXERCISE 11.3

In each of the Exercises 1 to 9, find the coordinates of the foci, the vertices, the length
of major axis, the minor axis, the eccentricity and the length of the latus rectum of the
ellipse.

1. $\frac{x^2}{36} + \frac{y^2}{16} = 1$
2. $\frac{x^2}{4} + \frac{y^2}{25} = 1$
3. $\frac{x^2}{16} + \frac{y^2}{9} = 1$

4. $\frac{x^2}{25} + \frac{y^2}{100} = 1$
5. $\frac{x^2}{49} + \frac{y^2}{36} = 1$
6. $\frac{x^2}{100} + \frac{y^2}{400} = 1$

7. $36x^2 + 4y^2 = 144$
8. $16x^2 + y^2 = 16$
9. $4x^2 + 9y^2 = 36$

In each of the following Exercises 10 to 20, find the equation for the ellipse that satisfies
the given conditions:

10. Vertices $(\pm 5, 0)$, foci $(\pm 4, 0)$
11. Vertices $(0, \pm 13)$, foci $(0, \pm 5)$
12. Vertices $(\pm 6, 0)$, foci $(\pm 4, 0)$
13. Ends of major axis $(\pm 3, 0)$, ends of minor axis $(0, \pm 2)$

14. Ends of major axis $(0, \pm \sqrt{5})$, ends of minor axis $(\pm 1, 0)$
15. Length of major axis 26, foci $(\pm 5, 0)$
16. Length of minor axis 16, foci $(0, \pm 6)$.
17. Foci $(\pm 3, 0)$, $a = 4$
18. $b = 3$, $c = 4$, centre at the origin; foci on the $x$ axis.
19. Centre at $(0,0)$, major axis on the $y$-axis and passes through the points $(3, 2)$ and
$(1,6)$.
20. Major axis on the $x$-axis and passes through the points $(4,3)$ and $(6,2)$.

11.6 Hyperbola

Definition 7 A hyperbola is the set of all points in a plane, the difference of whose
distances from two fixed points in the plane is a constant.

<!-- page 319 -->
$$\mathbf{P}_1\mathbf{F}_2 - \mathbf{P}_1\mathbf{F}_1 = \mathbf{P}_2\mathbf{F}_2 - \mathbf{P}_2\mathbf{F}_1 = \mathbf{P}_3\mathbf{F}_1 - \mathbf{P}_3\mathbf{F}_2$$

Fig 11.29

The term “difference” that is used in the definition means the distance to the
farther point minus the distance to the closer point. The two fixed points are called the
foci of the hyperbola. The mid-point of the line segment joining the foci is called the
centre of the hyperbola. The line through the foci is called the transverse axis and
the line through the centre and perpendicular to the transverse axis is called the conjugate
axis. The points at which the hyperbola
intersects the transverse axis are called the
vertices of the hyperbola (Fig 11.29).

We denote the distance between the
two foci by $2c$, the distance between two
vertices (the length of the transverse axis)
by $2a$ and we define the quantity $b$ as

Fig 11.30

$$b = \sqrt{c^2 - a^2}$$

Also $2b$ is the length of the conjugate axis
(Fig 11.30).

To find the constant $\mathrm{P}_1\mathrm{F}_2 - \mathrm{P}_1\mathrm{F}_1$ :

By taking the point P at A and B in the Fig 11.30, we have

$$BF_1 - BF_2 = AF_2 - AF_1 \text{ (by the definition of the hyperbola)}$$

$$BA + AF_1 - BF_2 = AB + BF_2 - AF_1$$

i.e., $AF_1 = BF_2$

So that, $BF_1 - BF_2 = BA + AF_1 - BF_2 = BA = 2a$

<!-- page 320 -->
11.6.1 Eccentricity

Definition 8 Just like an ellipse, the ratio $e = \frac{c}{a}$ is called the eccentricity of the
hyperbola. Since $c \ge a$, the eccentricity is never less than one. In terms of the
eccentricity, the foci are at a distance of $ae$ from the centre.

**11.6.2 *Standard equation of Hyperbola*** The equation of a hyperbola is simplest if
the centre of the hyperbola is at the origin and the foci are on the $x$-axis or $y$-axis. The
two such possible orientations are shown in Fig11.31.

Fig 11.31

We will derive the equation for the hyperbola shown in Fig 11.31(a) with $foci$ on
the $x$-axis.

Let $\mathrm{F}_1$ and $\mathrm{F}_2$ be the foci and $\mathrm{O}$ be the mid-point of the line segment $\mathrm{F}_1\mathrm{F}_2$. Let $\mathrm{O}$
be the origin and the line through $\mathrm{O}$
through $\mathrm{F}_2$ be the positive $x$-axis and
that through $\mathrm{F}_1$ as the negative
$x$-axis. The line through $\mathrm{O}$
perpendicular to the $x$-axis be the
$y$-axis. Let the coordinates of $\mathrm{F}_1$ be $\mathbf{X}'$
$(-c,0)$ and $\mathrm{F}_2$ be $(c,0)$ (Fig 11.32).
Let $\mathrm{P}(x,y)$ be any point on the
hyperbola such that the difference
of the distances from $\mathrm{P}$ to the farther
point minus the closer point be $2a$.
So given, $\mathrm{PF}_1 - \mathrm{PF}_2 = 2a$
Fig 11.32

<!-- page 321 -->
Using the distance formula, we have

$$\sqrt{(x+c)^2 + y^2} - \sqrt{(x-c)^2 + y^2} = 2a$$

i.e., $\sqrt{(x+c)^2 + y^2} = 2a + \sqrt{(x-c)^2 + y^2}$

Squaring both side, we get

$$(x + c)^2 + y^2 = 4a^2 + 4a \sqrt{(x - c)^2 + y^2} + (x - c)^2 + y^2$$

and on simplifying, we get

$$\frac{cx}{a} - a = \sqrt{(x-c)^2 + y^2}$$

On squaring again and further simplifying, we get

$$\frac{x^2}{a^2} - \frac{y^2}{c^2 - a^2} = 1$$

i.e., $\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1$ (Since $c^2 - a^2 = b^2$)

Hence any point on the hyperbola satisfies $\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1$ 1.

Conversely, let $P(x, y)$ satisfy the above equation with $0 < a < c$. Then

$$y^2 = b^2 \left( \frac{x^2 - a^2}{a^2} \right)$$

Therefore, $\quad \mathrm{PF}_{1}=+\sqrt{(x+c)^{2}+y^{2}}$

$\quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \

Similarly, $\text{PF}_2 = a - \frac{a}{c}x$

In hyperbola $c > a$; and since P is to the right of the line $x = a, x > a, \frac{c}{a}x > a$. Therefore,

$a - \frac{c}{a} x$ becomes negative. Thus, $\text{PF}_2 = \frac{c}{a} x - a$.

<!-- page 322 -->
Therefore $\text{PF}_1 - \text{PF}_2 = a + \frac{c}{a}x - \frac{cx}{a} + a = 2a$

Also, note that if P is to the left of the line $x = - a$, then

$$\text{PF}_1 = -\left( a + \frac{c}{a} x \right), \text{PF}_2 = a - \frac{c}{a} x.$$

In that case $\mathrm{P} \mathrm{F}_{2}-\mathrm{PF}_{1}=2 a$. So, any point that satisfies $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1$, lies on the
hyperbola.

Thus, we proved that the equation of hyperbola with origin $(0,0)$ and transverse axis

along $x$-axis is $\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1$.

Note A hyperbola in which $a = b$ is called an equilateral hyperbola.

**Discussion** From the equation of the hyperbola we have obtained, it follows that, we

have for every point $(x, y)$ on the hyperbola, $\frac{x^2}{a^2} = 1 + \frac{y^2}{b^2} \ge 1$.

i.e, $\left| \frac{x}{a} \right| \geq 1$, i.e., $x \leq -a$ or $x \geq a$. Therefore, no portion of the curve lies between the
lines $x = + a$ and $x = - a$, (i.e. no real intercept on the conjugate axis).

Similarly, we can derive the equation of the hyperbola in Fig 11.31 (b) as $\frac{y^2}{a^2} - \frac{x^2}{b^2} = 1$

These two equations are known as the \textit{standard equations} of \textit{hyperbolas}.

Note The standard equations of hyperbolas have transverse and conjugate
axes as the coordinate axes and the centre at the origin. However, there are
hyperbolas with any two perpendicular lines as transverse and conjugate axes, but
the study of such cases will be dealt in higher classes.

From the standard equations of hyperbolas (Fig11.29), we have the following
observations:

1. Hyperbola is symmetric with respect to both the axes, since if $(x, y)$ is a point on
the hyperbola, then $(-x, y)$, $(x, -y)$ and $(-x, -y)$ are also points on the hyperbola.

<!-- page 323 -->
2.    The foci are always on the transverse axis.  It is the positive term whose
denominator gives the transverse axis.  For example, $\frac{x^2}{9} - \frac{y^2}{16} = 1$
has transverse axis along $x$-axis of length 6, while $\frac{y^2}{25} - \frac{x^2}{16} = 1$
has transverse axis along y-axis of length 10.

11.6.3 Latus rectum

Definition 9 Latus rectum of hyperbola is a line segment perpendicular to the transverse
axis through any of the foci and whose end points lie on the hyperbola.

As in ellipse, it is easy to show that the length of the latus rectum in hyperbola is $\frac{2b^2}{a}$.

Example 14 Find the coordinates of the foci and the vertices, the eccentricity,the
length of the latus rectum of the hyperbolas:

(i) $\frac{x^2}{9} - \frac{y^2}{16} = 1$, (ii) $y^2 - 16x^2 = 16$

Solution (i) Comparing the equation $\frac{x^2}{9} - \frac{y^2}{16} = 1$ with the standard equation

$$\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1$$

Here, $a=3$, $b=4$ and $c = \sqrt{a^2 + b^2} = \sqrt{9 + 16} = 5$

Therefore, the coordinates of the foci are $(\pm 5, 0)$ and that of vertices are $(\pm 3, 0)$.Also,

The eccentricity $e = \frac{c}{a} = \frac{5}{3}$. The latus rectum $= \frac{2b^2}{a} = \frac{32}{3}$

(ii) Dividing the equation by 16 on both sides, we have $\frac{y^2}{16} - \frac{x^2}{1} = 1$

Comparing the equation with the standard equation $\frac{y^2}{a^2} - \frac{x^2}{b^2} = 1$, we find that

$$a=4, \ b=1 \text{ and } \ c=\sqrt{a^2+b^2} = \sqrt{16+1} = \sqrt{17}.$$

<!-- page 324 -->
Therefore, the coordinates of the foci are $(0, \pm \sqrt{17} )$ and that of the vertices are
$(0, \pm 4)$. Also,

The eccentricity $e = \frac{c}{a} = \frac{\sqrt{17}}{4}$. The latus rectum $= \frac{2b^2}{a} = \frac{1}{2}$.

Example 15 Find the equation of the hyperbola with foci $(0, \pm 3)$ and vertices

$(0, \pm \frac{\sqrt{11}}{2})$.

Solution Since the foci is on y-axis, the equation of the hyperbola is of the form

$$\frac{y^2}{a^2} - \frac{x^2}{b^2} = 1$$

Since vertices are $(0, \pm \frac{\sqrt{11}}{2}), \quad a = \frac{\sqrt{11}}{2}$

Also, since foci are $(0, \pm 3)$; $c = 3$ and $b^2 = c^2 - a^2 = \frac{25}{4}$.

Therefore, the equation of the hyperbola is

$$\frac{y^2}{\left(\frac{11}{4}\right)} - \frac{x^2}{\left(\frac{25}{4}\right)} = 1, \text{ i.e., } 100 \ y^2 - 44 \ x^2 = 275.$$

Example 16 Find the equation of the hyperbola where foci are $(0, \pm 12)$ and the length
of the latus rectum is 36.

Solution Since foci are $(0, \pm 12)$, it follows that $c = 12$.

Length of the latus rectum = $\frac{2b^2}{a} = 36$ or $b^2 = 18a$
Therefore $c^2 = a^2 + b^2$; gives
$144 = a^2 + 18a$
i.e., $a^2 + 18a - 144 = 0$,
So $a = - 24, 6$.
Since $a$ cannot be negative, we take $a = 6$ and so $b^2 = 108$.

Therefore, the equation of the required hyperbola is $\frac{y^2}{36} - \frac{x^2}{108} = 1$, i.e., $3y^2 - x^2 = 108$

<!-- page 325 -->
EXERCISE 11.4

In each of the Exercises 1 to 6, find the coordinates of the foci and the vertices, the
eccentricity and the length of the latus rectum of the hyperbolas.

1. $\frac{x^2}{16} - \frac{y^2}{9} = 1$
2. $\frac{y^2}{9} - \frac{x^2}{27} = 1$
3. $9y^2 - 4x^2 = 36$
4. $16x^2 - 9y^2 = 576$
5. $5y^2 - 9x^2 = 36$
6. $49y^2 - 16x^2 = 784.$

In each of the Exercises 7 to 15, find the equations of the hyperbola satisfying the given
conditions.

7. Vertices $(\pm 2, 0)$, foci $(\pm 3, 0)$
8. Vertices $(0, \pm 5)$, foci $(0, \pm 8)$
9. Vertices $(0, \pm 3)$, foci $(0, \pm 5)$
10. Foci $(\pm 5, 0)$, the transverse axis is of length 8.
11. Foci $(0, \pm 13)$, the conjugate axis is of length 24.
12. Foci $(\pm 3 \sqrt{5}, 0)$, the latus rectum is of length 8.
13. Foci $(\pm 4, 0)$, the latus rectum is of length 12

14. vertices $(\pm 7,0)$, $e = \frac{4}{3}$.

15. Foci $(0, \pm \sqrt{10})$, passing through $(2,3)$

Miscellaneous Examples

Example 17 The focus of a parabolic mirror as shown in Fig 11.33 is at a distance of
5 cm from its vertex. If the mirror is 45 cm deep, find
the distance AB (Fig 11.33).

Solution Since the distance from the focus to the
vertex is 5 cm. We have, $a = 5$. If the origin is taken at
the vertex and the axis of the mirror lies along the
positive $x$-axis, the equation of the parabolic section is
$$y^2 = 4 \ (5) \ x = 20 \ x$$
Note that $x = 45$. Thus
$$y^2 = 900$$
Therefore $y = \pm 30$
Hence $\text{AB} = 2y = 2 \times 30 = 60 \text{ cm}$.

Example 18 A beam is supported at its ends by $\mathbf{Fig}$ 11.33
supports which are 12 metres apart. Since the load is concentrated at its centre, there

<!-- page 326 -->
is a deflection of 3 cm at the centre and the deflected beam is in the shape of a
parabola. How far from the centre is the deflection 1 cm?

Solution Let the vertex be at the lowest point and the axis vertical. Let the coordinate
axis be chosen as shown in Fig 11.34.

Fig 11.34

The equation of the parabola takes the form $x^2 = 4ay$. Since it passes through
$\left(6, \frac{3}{100}\right)$, we have $(6)^2 = 4a \left(\frac{3}{100}\right)$, i.e., $a = \frac{36 \times 100}{12} = 300 \text{ m}$

Let AB be the deflection of the beam which is $\frac{1}{100}$ m. Coordinates of B are $(x, \frac{2}{100})$.

Therefore $x^2 = 4 \times 300 \times \frac{2}{100} = 24$

i.e. $x = \sqrt{24} = 2\sqrt{6}$ metres

**Example 19** A rod AB of length 15 cm rests in between two coordinate axes in such
a way that the end point A lies on $x$-axis and end point B lies on
$y$-axis. A point P$(x, y)$ is taken on the rod in such a way
that AP = 6 cm. Show that the locus of P is an ellipse.
Solution Let AB be the rod making an angle $\theta$ with
OX as shown in Fig 11.35 and P $(x, y)$ the point on it
such that $\quad$ AP = 6 cm.
Since $\quad$ AB = 15 cm, we have
$$PB = 9 \text{ cm}.$$
From P draw PQ and PR perpendiculars on $y$-axis and
$x$-axis, respectively.

**Fig 11.35**

<!-- page 327 -->
From $\Delta PBQ, \cos \theta = \frac{x}{9}$

From $\Delta$ PRA, $\sin \theta = \frac{y}{6}$

Since $\cos^2 \theta + \sin^2 \theta = 1$

$$\left(\frac{x}{9}\right)^2 + \left(\frac{y}{6}\right)^2 = 1$$

or $\frac{x^2}{81} + \frac{y^2}{36} = 1$

Thus the locus of $P$ is an ellipse.

Miscellaneous Exercise on Chapter 11

1. If a parabolic reflector is 20 cm in diameter and 5 cm deep, find the focus.
2. An arch is in the form of a parabola with its axis vertical. The arch is 10 m high
and 5 m wide at the base. How wide is it 2 m from the vertex of the parabola?
3. The cable of a uniformly loaded suspension bridge hangs in the form of a parabola.
The roadway which is horizontal and 100 m long is supported by vertical wires
attached to the cable, the longest wire being 30 m and the shortest being 6 m.
Find the length of a supporting wire attached to the roadway 18 m from the
middle.
4. An arch is in the form of a semi-ellipse. It is 8 m wide and 2 m high at the centre.
Find the height of the arch at a point 1.5 m from one end.
5. A rod of length 12 cm moves with its ends always touching the coordinate axes.
Determine the equation of the locus of a point P on the rod, which is 3 cm from
the end in contact with the $x$-axis.
6. Find the area of the triangle formed by the lines joining the vertex of the parabola
$x^2 = 12y$ to the ends of its latus rectum.
7. A man running a racecourse notes that the sum of the distances from the two flag
posts from him is always 10 m and the distance between the flag posts is 8 m.
Find the equation of the posts traced by the man.
8. An equilateral triangle is inscribed in the parabola $y^2 = 4 \ ax$, where one vertex is
at the vertex of the parabola. Find the length of the side of the triangle.

<!-- page 328 -->
Summary

In this Chapter the following concepts and generalisations are studied.

A circle is the set of all points in a plane that are equidistant from a fixed point
in the plane.
The equation of a circle with centre $(h, k)$ and the radius $r$ is
$$(x - h)^2 + (y - k)^2 = r^2.$$
A parabola is the set of all points in a plane that are equidistant from a fixed
line and a fixed point in the plane.
The equation of the parabola with focus at $(a, 0)$ $a > 0$ and directrix $x = -a$ is
$$y^2 = 4ax.$$
Latus rectum of a parabola is a line segment perpendicular to the axis of the
parabola, through the focus and whose end points lie on the parabola.
Length of the latus rectum of the parabola $y^2 = 4ax$ is $4a$.
An $ellipse$ is the set of all points in a plane, the sum of whose distances from
two fixed points in the plane is a constant.

The equation of an ellipse with foci on the $x$-axis is $\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1$.

Latus rectum of an ellipse is a line segment perpendicular to the major axis
through any of the foci and whose end points lie on the ellipse.

Length of the latus rectum of the ellipse $\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1$ is $\frac{2b^2}{a}$ .

The eccentricity of an ellipse is the ratio between the distances from the centre
of the ellipse to one of the foci and to one of the vertices of the ellipse.
A hyperbola is the set of all points in a plane, the difference of whose distances
from two fixed points in the plane is a constant.

The equation of a hyperbola with foci on the $x$-axis is : $\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1$

<!-- page 329 -->
$\diamond$ Latus rectum of hyperbola is a line segment perpendicular to the transverse
axis through any of the foci and whose end points lie on the hyperbola.


$\diamond$ Length of the latus rectum of the hyperbola : $\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1$ is : $\frac{2b^2}{a}$ .


$\diamond$ The eccentricity of a hyperbola is the ratio of the distances from the centre of
the hyperbola to one of the foci and to one of the vertices of the hyperbola.

\textit{Historical Note}

Geometry is one of the most ancient branches of mathematics. The Greek
geometers investigated the properties of many curves that have theoretical and
practical importance. Euclid wrote his treatise on geometry around 300 B.C. He
was the first who organised the geometric figures based on certain axioms
suggested by physical considerations. Geometry as initially studied by the ancient
Indians and Greeks, who made essentially no use of the process of algebra. The
synthetic approach to the subject of geometry as given by Euclid and in
\textit{Sulbasutras}, etc., was continued for some 1300 years. In the 200 B.C., Apollonius
wrote a book called ‘\textit{The Conic}’ which was all about conic sections with many
important discoveries that have remained unsurpassed for eighteen centuries.
Modern analytic geometry is called ‘\textit{Cartesian}’ after the name of Rene
Descartes (1596-1650) whose relevant ‘La Geometrie’ was published in 1637.
But the fundamental principle and method of analytical geometry were already
discovered by Pierre de Fermat (1601-1665). Unfortunately, Fermats treatise on
the subject, entitled \textit{Ad Locus Planos et So LIDOS Isagoge} (Introduction to
Plane and Solid Loci) was published only posthumously in
1679. So, Descartes came to be regarded as the unique inventor of the analytical
geometry.
Isaac Barrow avoided using cartesian method. Newton used method of
undetermined coefficients to find equations of curves. He used several types of
coordinates including polar and bipolar. Leibnitz used the terms ‘\textit{abscissa}’,
‘\textit{ordinate}’ and ‘\textit{coordinate}’. L’ Hospital (about 1700) wrote an important textbook
on analytical geometry.
Clairaut (1729) was the first to give the distance formula although in clumsy
form. He also gave the intercept form of the linear equation. Cramer (1750)

<!-- page 330 -->
made formal use of the two axes and gave the equation of a circle as
$$(y-a)^2 + (b-x)^2 = r$$
He gave the best exposition of the analytical geometry of his time. Monge
(1781) gave the modern ‘point-slope’ form of equation of a line as
$$y - y' = a(x-x')$$
and the condition of perpendicularity of two lines as $aa' + 1 = 0$.
S.F. Lacroix (1765–1843) was a prolific textbook writer, but his contributions
to analytical geometry are found scattered. He gave the ‘two-point’ form of
equation of a line as
$$y - \beta = \frac{\beta' - \beta}{\alpha' - \alpha}(x - \alpha)$$
and the length of the perpendicular from $(\alpha, \beta)$ on $y = ax + b$ as $\frac{(\beta - a - b)}{\sqrt{1 + a^2}}$.

His formula for finding angle between two lines was $\tan \theta = \left( \frac{a' - a}{1 + aa'} \right)$. It is, of
course, surprising that one has to wait for more than 150 years after the invention
of analytical geometry before finding such essential basic formula. In 1818, C.
Lame, a civil engineer, gave $m\text{E} + m'\text{E}' = 0$ as the curve passing through the
points of intersection of two loci $\text{E} = 0$ and $\text{E}' = 0$.
Many important discoveries, both in Mathematics and Science, have been
linked to the conic sections. The Greeks particularly Archimedes (287–212 B.C.)
and Apollonius (200 B.C.) studied conic sections for their own beauty. These
curves are important tools for present day exploration of outer space and also for
research into behaviour of atomic particles.

<!-- page 331 -->
Chapter 12

INTRODUCTION TO THREE
DIMENSIONAL GEOMETRY

❖ Mathematics is both the queen and the hand-maiden of
all sciences – E.T. BELL ❖

12.1 Introduction

You may recall that to locate the position of a point in a
plane, we need two intersecting mutually perpendicular lines
in the plane. These lines are called the \textit{coordinate axes}
and the two numbers are called the \textit{coordinates of the}
\textit{point with respect to the axes}. In actual life, we do not
have to deal with points lying in a plane only. For example,
consider the position of a ball thrown in space at different
points of time or the position of an aeroplane as it flies
from one place to another at different times during its flight.

Similarly, if we were to locate the position of the
lowest tip of an electric bulb hanging from the ceiling of a
room or the position of the central tip of the ceiling fan in a room, we will not only
require the perpendicular distances of the point to be located from two perpendicular
walls of the room but also the height of the point from the floor of the room. Therefore,
we need not only two but three numbers representing the perpendicular distances of
the point from three mutually perpendicular planes, namely the floor of the room and
two adjacent walls of the room. The three numbers representing the three distances
are called the coordinates of the point with reference to the three coordinate
planes. So, a point in space has three coordinates. In this Chapter, we shall study the
basic concepts of geometry in three dimensional space.$^*$

* For various activities in three dimensional geometry one may refer to the Book, “A Hand Book for
designing Mathematics Laboratory in Schools”, NCERT, 2005.

<!-- page 332 -->
12.2 Coordinate Axes and Coordinate Planes in Three Dimensional Space

Consider three planes intersecting at a point O
such that these three planes are mutually
perpendicular to each other (Fig 12.1). These
three planes intersect along the lines X'OX, Y'OY
and Z'OZ, called the $x$, $y$ and $z$-axes, respectively.
We may note that these lines are mutually
perpendicular to each other. These lines constitute
the rectangular coordinate system. The planes
XOY, YOZ and ZOX, called, respectively the
XY-plane, YZ-plane and the ZX-plane, are
known as the three coordinate planes. We take
the XOY plane as the plane of the paper and the
line Z'OZ as perpendicular to the plane XOY. If the plane of the paper is considered
as horizontal, then the line Z'OZ will be vertical. The distances measured from
XY-plane upwards in the direction of OZ are taken as positive and those measured
downwards in the direction of OZ' are taken as negative. Similarly, the distance
measured to the right of ZX-plane along OY are taken as positive, to the left of
ZX-plane and along OY' as negative, in front of the YZ-plane along OX as positive
and to the back of it along OX' as negative. The point O is called the origin of the
coordinate system. The three coordinate planes divide the space into eight parts known
as octants. These octants could be named as XOYZ, X'OYZ, X'OYZ', XOYZ',
XOYZ', X'OYZ', X'OYZ' and XOYZ'. and denoted by I, II, III, ..., VIII , respectively.

12.3 Coordinates of a Point in Space

Having chosen a fixed coordinate system in the
space, consisting of coordinate axes, coordinate
planes and the origin, we now explain, as to how,
given a point in the space, we associate with it three
coordinates $(x,y,z)$ and conversely, given a triplet
of three numbers $(x, y, z)$, how, we locate a point in
the space.

Given a point P in space, we drop a $\mathbf{X}$
perpendicular PM on the XY-plane with M as the
foot of this perpendicular (Fig 12.2). Then, from the point M, we draw a perpendicular
ML to the $x$-axis, meeting it at L. Let OL be $x$, LM be $y$ and MP be $z$. Then $x, y$ and $z$
are called the $x, y$ and $z$ coordinates, respectively, of the point P in the space. In
Fig 12.2, we may note that the point P $(x, y, z)$ lies in the octant XOYZ and so all $x, y,$
$z$ are positive. If P was in any other octant, the signs of $x, y$ and $z$ would change

<!-- page 333 -->
accordingly. Thus, to each point P in the space there corresponds an ordered triplet
$(x, y, z)$ of real numbers.

Conversely, given any triplet $(x, y, z)$, we would first fix the point L on the $x$-axis
corresponding to $x$, then locate the point M in the XY-plane such that $(x, y)$ are the
coordinates of the point M in the XY-plane. Note that LM is perpendicular to the
$x$-axis or is parallel to the $y$-axis. Having reached the point M, we draw a perpendicular
MP to the XY-plane and locate on it the point P corresponding to $z$. The point P so
obtained has then the coordinates $(x, y, z)$. Thus, there is a one to one correspondence
between the points in space and ordered triplet $(x, y, z)$ of real numbers.

Alternatively, through the point P in the
space, we draw three planes parallel to the
coordinate planes, meeting the $x$-axis, $y$-axis
and $z$-axis in the points A, B and C, respectively
(Fig 12.3). Let OA = $x$, OB = $y$ and OC = $z$.
Then, the point P will have the coordinates $x$, $y$
and $z$ and we write P $(x, y, z)$. Conversely, given
$x$, $y$ and $z$, we locate the three points A, B and
C on the three coordinate axes. Through the
points A, B and C we draw planes parallel to
the YZ-plane, ZX-plane and XY-plane,
respectively. The point of interesection of these three planes,
namely, ADPF, BDPE and CEPF is obviously the point P,
corresponding to the ordered triplet $(x, y, z)$. We
observe that if P $(x, y, z)$ is any point in the space, then $x$, $y$ and $z$ are perpendicular
distances from YZ, ZX and XY planes, respectively.

Note The coordinates of the origin O are $(0,0,0)$. The coordinates of any point
on the $x$-axis will be as $(x,0,0)$ and the coordinates of any point in the YZ-plane will
be as $(0, y, z)$.

$\mathit{Remark}$ The sign of the coordinates of a point determine the octant in which the
point lies. The following table shows the signs of the coordinates in eight octants.

Table 12.1

<table>
<thead>
<tr>
<th>Octants<br/>Coordinates</th>
<th>I</th>
<th>II</th>
<th>III</th>
<th>IV</th>
<th>V</th>
<th>VI</th>
<th>VII</th>
<th>VIII</th>
</tr>
</thead>
<tbody>
<tr>
<td>x</td>
<td>+</td>
<td>-</td>
<td>-</td>
<td>+</td>
<td>+</td>
<td>-</td>
<td>-</td>
<td>+</td>
</tr>
<tr>
<td>y</td>
<td>+</td>
<td>+</td>
<td>-</td>
<td>-</td>
<td>+</td>
<td>+</td>
<td>-</td>
<td>-</td>
</tr>
<tr>
<td>z</td>
<td>+</td>
<td>+</td>
<td>+</td>
<td>+</td>
<td>-</td>
<td>-</td>
<td>-</td>
<td>-</td>
</tr>
</tbody>
</table>

<!-- page 334 -->
Example 1 In Fig 12.3, if P is (2,4,5), find the coordinates of F.

**Solution** For the point F, the distance measured along OY is zero. Therefore, the
coordinates of F are (2,0,5).

Example 2 Find the octant in which the points $(-3,1,2)$ and $(-3,1,-2)$ lie.

**Solution** From the Table 12.1, the point $(-3,1, 2)$ lies in second octant and the point
$(-3, 1, -2)$ lies in octant VI.

EXERCISE 12.1

1. A point is on the $x$-axis. What are its $y$-coordinate and $z$-coordinates?
2. A point is in the XZ-plane. What can you say about its $y$-coordinate?
3. Name the octants in which the following points lie:
$(1, 2, 3), (4, -2, 3), (4, -2, -5), (4, 2, -5), (-4, 2, -5), (-4, 2, 5),$
$(-3, -1, 6) (-2, -4, -7).$
4. Fill in the blanks:
(i) The $x$-axis and $y$-axis taken together determine a plane known as ________.
(ii) The coordinates of points in the XY-plane are of the form ________.
(iii) Coordinate planes divide the space into ________ octants.

12.4 Distance between Two Points

We have studied about the distance
between two points in two-dimensional
coordinate system. Let us now extend this
study to three-dimensional system.

Let $P(x_1, y_1, z_1)$ and $Q$ ( $x_2, y_2, z_2$ )
be two points referred to a system of
rectangular axes OX, OY and OZ.
Through the points P and Q draw planes
parallel to the coordinate planes so as to
form a rectangular parallelopiped with one
diagonal PQ (Fig 12.4).

Fig 12.4

Now, since $\angle PAQ$ is a right
angle, it follows that, in triangle PAQ,

$$PQ^2 = PA^2 + AQ^2 \hspace{12em} \dots (1)$$

Also, triangle ANQ is right angle triangle with $\angle$ANQ a right angle.

<!-- page 335 -->
Therefore $AQ^2 = AN^2 + NQ^2$ ... (2)

From (1) and (2), we have

$$PQ^2 = PA^2 + AN^2 + NQ^2$$

Now $\quad \mathrm{PA}=y_{2}-y_{1}, \mathrm{AN}=x_{2}-x_{1}$ and $\mathrm{NQ}=z_{2}-z_{1}$

Hence $PQ^2 = (x_2 - x_1)^2 + (y_2 - y_1)^2 + (z_2 - z_1)^2$

Therefore $PQ = \sqrt{(x_2-x_1)^2+(y_2-y_1)^2+(z_2-z_1)^2}$

This gives us the distance between two points $(x_1, y_1, z_1)$ and $(x_2, y_2, z_2)$.

In particular, if $x_1 = y_1 = z_1 = 0$, i.e., point P is origin O, then OQ = $\sqrt{{x_2}^2 + {y_2}^2 + {z_2}^2}$ ,
which gives the distance between the origin O and any point Q ($x_2, y_2, z_2$).

which gives the distance between the origin O and any point Q $(x_2, y_2, z_2)$.

Example 3 Find the distance between the points P(1, $-3$, 4) and Q ($-4$, 1, 2).
Solution The distance PQ between the points P (1,$-3$, 4) and Q ($-4$, 1, 2) is
$$PQ = \sqrt{(-4-1)^2 + (1+3)^2 + (2-4)^2}$$
$$= \sqrt{25 + 16 + 4}$$
$$= \sqrt{45} = 3\sqrt{5} \text{ units}$$

Example 4 Show that the points P ($-2, 3, 5$), Q ($1, 2, 3$) and R ($7, 0, -1$) are collinear.

Solution We know that points are said to be collinear if they lie on a line.

Now,      PQ = $\sqrt{(1+2)^2 + (2-3)^2 + (3-5)^2} = \sqrt{9+1+4} = \sqrt{14}$

           QR = $\sqrt{(7-1)^2 + (0-2)^2 + (-1-3)^2} = \sqrt{36+4+16} = \sqrt{56} = 2\sqrt{14}$

and        PR = $\sqrt{(7+2)^2 + (0-3)^2 + (-1-5)^2} = \sqrt{81+9+36} = \sqrt{126} = 3\sqrt{14}$

Thus, PQ + QR = PR. Hence, P, Q and R are collinear.

Thus, $PQ + QR = PR$. Hence, $P$, $Q$ and $R$ are collinear.

Example 5 Are the points A (3, 6, 9), B (10, 20, 30) and C (25, $-41$, 5), the vertices
of a right angled triangle?

Solution By the distance formula, we have
$$AB^2 = (10 - 3)^2 + (20 - 6)^2 + (30 - 9)^2$$
$$= 49 + 196 + 441 = 686$$
$$BC^2 = (25 - 10)^2 + (-41 - 20)^2 + (5 - 30)^2$$
$$= 225 + 3721 + 625 = 4571$$

<!-- page 336 -->
$$CA^2 \quad = (3 - 25)^2 + (6 + 41)^2 + (9 - 5)^2$$
$$= 484 + 2209 + 16 = 2709$$

We find that $\text{CA}^2 + \text{AB}^2 \neq \text{BC}^2$.

Hence, the triangle ABC is not a right angled triangle.

Example 6 Find the equation of set of points P such that $PA^2 + PB^2 = 2k^2$, where
A and B are the points $(3, 4, 5)$ and $(-1, 3, -7)$, respectively.

Solution Let the coordinates of point P be $(x, y, z)$.
Here $PA^2 = (x - 3)^2 + (y - 4)^2 + (z - 5)^2$
$PB^2 = (x + 1)^2 + (y - 3)^2 + (z + 7)^2$
By the given condition $PA^2 + PB^2 = 2k^2$, we have
$$(x - 3)^2 + (y - 4)^2 + (z - 5)^2 + (x + 1)^2 + (y - 3)^2 + (z + 7)^2 = 2k^2$$
i.e., $2x^2 + 2y^2 + 2z^2 - 4x - 14y + 4z = 2k^2 - 109$.

EXERCISE 12.2

1. Find the distance between the following pairs of points:
(i) $(2, 3, 5)$ and $(4, 3, 1)$ (ii) $(-3, 7, 2)$ and $(2, 4, -1)$
(iii) $(-1, 3, -4)$ and $(1, -3, 4)$ (iv) $(2, -1, 3)$ and $(-2, 1, 3)$.
2. Show that the points $(-2, 3, 5), (1, 2, 3)$ and $(7, 0, -1)$ are collinear.
3. Verify the following:
(i) $(0, 7, -10), (1, 6, -6)$ and $(4, 9, -6)$ are the vertices of an isosceles triangle.
(ii) $(0, 7, 10), (-1, 6, 6)$ and $(-4, 9, 6)$ are the vertices of a right angled triangle.
(iii) $(-1, 2, 1), (1, -2, 5), (4, -7, 8)$ and $(2, -3, 4)$ are the vertices of a parallelogram.
4. Find the equation of the set of points which are equidistant from the points
$(1, 2, 3)$ and $(3, 2, -1)$.
5. Find the equation of the set of points P, the sum of whose distances from
A $(4, 0, 0)$ and B $(-4, 0, 0)$ is equal to 10.

12.5 Section Formula

In two dimensional geometry, we have learnt how to find the coordinates of a point
dividing a line segment in a given ratio internally. Now, we extend this to three dimensional
geometry as follows:

Let the two given points be $\mathrm{P}(x_1, y_1, z_1)$ and $\mathrm{Q}(x_2, y_2, z_2)$. Let the point $\mathrm{R}(x, y, z)$
divide $\mathrm{PQ}$ in the given ratio $m:n$ internally. Draw $\mathrm{PL}$, $\mathrm{QM}$ and $\mathrm{RN}$ perpendicular to

<!-- page 337 -->
the XY-plane. Obviously PL $\parallel$ RN $\parallel$ QM and feet
of these perpendiculars lie in a XY-plane. The
points L, M and N will lie on a line which is the
intersection of the plane containing PL, RN and
QM with the XY-plane. Through the point R draw
a line ST parallel to the line LM. Line ST will
intersect the line LP externally at the point S and
the line MQ at T, as shown in Fig 12.5.

Fig 12.5

Also note that quadrilaterals LNRS and
NMTR are parallelograms.

The triangles PSR and QTR are similar. Therefore, $X$

$$\frac{m}{n} = \frac{\text{PR}}{\text{QR}} = \frac{\text{SP}}{\text{QT}} = \frac{\text{SL} - \text{PL}}{\text{QM} - \text{TM}} = \frac{\text{NR} - \text{PL}}{\text{QM} - \text{NR}} = \frac{z - z_1}{z_2 - z}$$

This implies $z = \frac{mz_2 + nz_1}{m + n}$

Similarly, by drawing perpendiculars to the $XZ$ and $YZ$-planes, we get

$$y = \frac{my_2 + ny_1}{m + n} \text{ and } x = \frac{mx_2 + nx_1}{m + n}$$

Hence, the coordinates of the point R which divides the line segment joining two points
P $(x_1, y_1, z_1)$ and Q $(x_2, y_2, z_2)$ internally in the ratio $m : n$ are

$$\left( \frac{mx_2 + nx_1}{m + n}, \frac{my_2 + ny_1}{m + n}, \frac{mz_2 + nz_1}{m + n} \right)$$

If the point R divides PQ externally in the ratio $m : n$, then its coordinates are
obtained by replacing $n$ by $-n$ so that coordinates of point R will be

$$\left( \frac{mx_2 - nx_1}{m - n}, \frac{my_2 - ny_1}{m - n}, \frac{mz_2 - nz_1}{m - n} \right),$$

Case 1 Coordinates of the mid-point: In case R is the mid-point of PQ, then

$m : n = 1 : 1$ so that $x = \frac{x_1 + x_2}{2}, y = \frac{y_1 + y_2}{2}$ and $z = \frac{z_1 + z_2}{2}$.

These are the coordinates of the mid point of the segment joining P $(x_1, y_1, z_1)$
and Q $(x_2, y_2, z_2)$.

<!-- page 338 -->
Case 2 The coordinates of the point R which divides PQ in the ratio $k : 1$ are obtained

by taking $k = \frac{m}{n}$ which are as given below:

$$\left( \frac{kx_2+x_1}{1+k}, \frac{ky_2+y_1}{1+k}, \frac{kz_2+z_1}{1+k} \right)$$

Generally, this result is used in solving problems involving a general point on the line
passing through two given points.

Example 7 Find the coordinates of the point which divides the line segment joining
the points $(1, -2, 3)$ and $(3, 4, -5)$ in the ratio $2 : 3$ (i) internally, and (ii) externally.

Solution (i) Let $P(x, y, z)$ be the point which divides line segment joining $A(1, -2, 3)$
and $B(3, 4, -5)$ internally in the ratio $2:3$. Therefore

$$x = \frac{2(3) + 3(1)}{2 + 3} = \frac{9}{5}, \quad y = \frac{2(4) + 3(-2)}{2 + 3} = \frac{2}{5}, \quad z = \frac{2(-5) + 3(3)}{2 + 3} = \frac{-1}{5}$$

Thus, the required point is $\left( \frac{9}{5}, \frac{2}{5}, \frac{-1}{5} \right)$

(ii) Let P $(x, y, z)$ be the point which divides segment joining A $(1, -2, 3)$ and
B $(3, 4, -5)$ externally in the ratio $2 : 3$. Then

$$x = \frac{2(3) + (-3)(1)}{2 + (-3)} = -3, \quad y = \frac{2(4) + (-3)(-2)}{2 + (-3)} = -14, \quad z = \frac{2(-5) + (-3)(3)}{2 + (-3)} = 19$$

Therefore, the required point is $(-3, -14, 19)$.

Example 8 Using section formula, prove that the three points $(-4, 6, 10), (2, 4, 6)$
and $(14, 0, -2)$ are collinear.

Solution Let A $(-4, 6, 10)$, B $(2, 4, 6)$ and C$(14, 0, -2)$ be the given points. Let the
point P divides AB in the ratio $k : 1$. Then coordinates of the point P are

$$\frac{2k - 4}{k + 1}, \frac{4k + 6}{k + 1}, \frac{6k + 10}{k + 1}$$

Let us examine whether for some value of $k$, the point P coincides with point C.

On putting $\frac{2k - 4}{k + 1} = 14$, we get $k = -\frac{3}{2}$

<!-- page 339 -->
When $k=-\frac{3}{2}$, then $\frac{4k+6}{k+1}=\frac{4(-\frac{3}{2})+6}{-\frac{3}{2}+1}=0$

and $$\frac{6k+10}{k+1} = \frac{6(-\frac{3}{2})+10}{-\frac{3}{2}+1} = -2$$

Therefore, C (14, 0, $-2$) is a point which divides AB externally in the ratio $3 : 2$ and is
same as P.Hence A, B, C are collinear.

Example 9 Find the coordinates of the centroid of the triangle whose vertices are
$(x_1, y_1, z_1), (x_2, y_2, z_2)$ and $(x_3, y_3, z_3)$.

Solution Let ABC be the triangle. Let the coordinates of the vertices A, B,C be
$(x_1, y_1, z_1), (x_2, y_2, z_2)$ and $(x_3, y_3, z_3)$, respectively. Let D be the mid-point of BC.
Hence coordinates of D are

$$\left( \frac{x_2 + x_3}{2}, \frac{y_2 + y_3}{2}, \frac{z_2 + z_3}{2} \right)$$

Let G be the centroid of the triangle. Therefore, it divides the median AD in the ratio $2:1$.
Hence, the coordinates of G are

$$\left( \frac{2 \left( \frac{x_2 + x_3}{2} \right) + x_1}{2 + 1}, \frac{2 \left( \frac{y_2 + y_3}{2} \right) + y_1}{2 + 1}, \frac{2 \left( \frac{z_2 + z_3}{2} \right) + z_1}{2 + 1} \right)$$

or $\left( \frac{x_1 + x_2 + x_3}{3}, \frac{y_1 + y_2 + y_3}{3}, \frac{z_1 + z_2 + z_3}{3} \right)$

Example 10 Find the ratio in which the line segment joining the points $(4, 8, 10)$ and
$(6, 10, -8)$ is divided by the YZ-plane.

Solution Let YZ-plane divides the line segment joining A $(4, 8, 10)$ and B $(6, 10, -8)$
at P $(x, y, z)$ in the ratio $k : 1$. Then the coordinates of P are

$$\left( \frac{4 + 6k}{k + 1}, \frac{8 + 10k}{k + 1}, \frac{10 - 8k}{k + 1} \right)$$

<!-- page 340 -->
Since P lies on the YZ-plane, its $x$-coordinate is zero, i.e., $\frac{4 + 6k}{k + 1} = 0$

or $k=-\frac{2}{3}$

Therefore, YZ-plane divides AB externally in the ratio $2 : 3$.

EXERCISE 12.3

1. Find the coordinates of the point which divides the line segment joining the points
$(-2, 3, 5)$ and $(1, -4, 6)$ in the ratio (i) $2:3$ internally, (ii) $2:3$ externally.

2. Given that P $(3, 2, -4)$, Q $(5, 4, -6)$ and R $(9, 8, -10)$ are collinear. Find the ratio
in which Q divides PR.

3. Find the ratio in which the YZ-plane divides the line segment formed by joining
the points $(-2, 4, 7)$ and $(3, -5, 8)$.

4. Using section formula, show that the points A $(2, -3, 4)$, B $(-1, 2, 1)$ and
$C\left(0, \frac{1}{3}, 2\right)$ are collinear.

5. Find the coordinates of the points which trisect the line segment joining the points
P $(4, 2, -6)$ and Q $(10, -16, 6)$.

Miscellaneous Examples

Example 11 Show that the points A (1, 2, 3), B ($-1, -2, -1$), C (2, 3, 2) and
D (4, 7, 6) are the vertices of a parallelogram ABCD, but it is not a rectangle.

Solution To show ABCD is a parallelogram we need to show opposite side are equal
Note that.

$$AB = \sqrt{(-1-1)^2+(-2-2)^2+(-1-3)^2} = \sqrt{4+16+16} = 6$$
$$BC = \sqrt{(2+1)^2+(3+2)^2+(2+1)^2} = \sqrt{9+25+9} = \sqrt{43}$$
$$CD = \sqrt{(4-2)^2+(7-3)^2+(6-2)^2} = \sqrt{4+16+16} = 6$$
$$DA = \sqrt{(1-4)^2+(2-7)^2+(3-6)^2} = \sqrt{9+25+9}=\sqrt{43}$$

Since  $AB = CD$ and $BC = AD$, ABCD is a parallelogram.
Now, it is required to prove that ABCD is not a rectangle. For this, we show that
diagonals AC and BD are unequal. We have

<!-- page 341 -->
$$AC \quad = \sqrt{(2-1)^2+(3-2)^2+(2-3)^2} = \sqrt{1+1+1}=\sqrt{3}$$

$$\text{BD} \quad = \sqrt{(4+1)^2+(7+2)^2+(6+1)^2} = \sqrt{25+81+49}=\sqrt{155}.$$

Since $AC \neq BD$, ABCD is not a rectangle.

Note We can also show that ABCD is a parallelogram, using the property that
diagonals AC and BD bisect each other.

Example 12 Find the equation of the set of the points P such that its distances from
the points A $(3, 4, -5)$ and B $(- 2, 1, 4)$ are equal.

Solution If P $(x, y, z)$ be any point such that PA = PB.

Now $\sqrt{(x-3)^2 + (y-4)^2 + (z+5)^2} = \sqrt{(x+2)^2 + (y-1)^2 + (z-4)^2}$

or $(x-3)^2 + (y-4)^2 + (z+5)^2 = (x+2)^2 + (y-1)^2 + (z-4)^2$

or $10x + 6y - 18z - 29 = 0.$

or $10x + 6y - 18z - 29 = 0.$

Example 13 The centroid of a triangle ABC is at the point $(1, 1, 1)$. If the coordinates
of A and B are $(3, -5, 7)$ and $(-1, 7, -6)$, respectively, find the coordinates of the
point C.

Solution Let the coordinates of C be $(x, y, z)$ and the coordinates of the centroid G be
$(1, 1, 1)$. Then

$$\frac{x+3-1}{3} = 1, \text{ i.e., } x = 1; \frac{y-5+7}{3} = 1, \text{ i.e., } y = 1; \frac{z+7-6}{3} = 1, \text{ i.e., } z = 2.$$

Hence, coordinates of C are $(1, 1, 2)$.

Hence, coordinates of C are $(1, 1, 2)$.

Miscellaneous Exercise on Chapter 12

1. Three vertices of a parallelogram ABCD are A(3, $-1$, 2), B (1, 2, $-4$) and
C ($-1$, 1, 2). Find the coordinates of the fourth vertex.

2. Find the lengths of the medians of the triangle with vertices A (0, 0, 6), B (0,4, 0)
and (6, 0, 0).

3. If the origin is the centroid of the triangle PQR with vertices P ($2a$, 2, 6),
Q ($-4$, $3b$, $-10$) and R(8, 14, $2c$), then find the values of $a$, $b$ and $c$.

4. Find the coordinates of a point on $y$-axis which are at a distance of $5\sqrt{2}$ from
the point P (3, $-2$, 5).

<!-- page 342 -->
5. A point R with $x$-coordinate 4 lies on the line segment joining the points
P(2, $-3$, 4) and Q (8, 0, 10). Find the coordinates of the point R.

[Hint Suppose R divides PQ in the ratio $k : 1$. The coordinates of the point R are given

by $\left( \frac{8k+2}{k+1}, \frac{-3}{k+1}, \frac{10k+4}{k+1} \right) ]$.

6.If A and B be the points $(3, 4, 5)$ and $(-1, 3, -7)$, respectively, find the equation of the
set of points P such that $\text{PA}^2 + \text{PB}^2 = k^2$, where $k$ is a constant.

Summary

In three dimensions, the coordinate axes of a rectangular Cartesian coordinate
system are three mutually perpendicular lines. The axes are called the $x$, $y$
and $z$-axes.
The three planes determined by the pair of axes are the coordinate planes,
called XY, YZ and ZX-planes.
The three coordinate planes divide the space into eight parts known as octants.
The coordinates of a point P in three dimensional geometry is always written
in the form of triplet like $(x, y, z)$. Here $x$, $y$ and $z$ are the distances from the
YZ, ZX and XY-planes.
(i) Any point on $x$-axis is of the form $(x, 0, 0)$
(ii) Any point on $y$-axis is of the form $(0, y, 0)$
(iii) Any point on $z$-axis is of the form $(0, 0, z)$.
Distance between two points $\text{P}(x_1, y_1, z_1)$ and $\text{Q}(x_2, y_2, z_2)$ is given by

$$PQ = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2 + (z_2 - z_1)^2}$$

The coordinates of the point R which divides the line segment joining two
points $\text{P}(x_1 y_1 z_1)$ and $\text{Q}(x_2, y_2, z_2)$ internally and externally in the ratio $m : n$
are given by

$$\left( \frac{mx_2 + nx_1}{m + n}, \frac{my_2 + ny_1}{m + n}, \frac{mz_2 + nz_1}{m + n} \right) \text{ and } \left( \frac{mx_2 - nx_1}{m - n}, \frac{my_2 - ny_1}{m - n}, \frac{mz_2 - nz_1}{m - n} \right),$$

respectively.
The coordinates of the mid-point of the line segment joining two points

$\text{P}(x_1, y_1, z_1)$ and $\text{Q}(x_2, y_2, z_2)$ are $\left( \frac{x_1 + x_2}{2}, \frac{y_1 + y_2}{2}, \frac{z_1 + z_2}{2} \right)$.

<!-- page 343 -->
The coordinates of the centroid of the triangle, whose vertices are $(x_1, y_1, z_1)$

$(x_2, y_2, z_2)$ and $(x_3, y_3, z_3)$, are $\left( \frac{x_1 + x_2 + x_3}{3}, \frac{y_1 + y_2 + y_3}{3}, \frac{z_1 + z_2 + x_3}{3} \right)$.

Historical Note

Rene' Descartes (1596–1650), the father of analytical geometry, essentially dealt
with plane geometry only in 1637. The same is true of his co-inventor Pierre
Fermat (1601-1665) and La Hire (1640-1718). Although suggestions for the three
dimensional coordinate geometry can be found in their works but no details.
Descartes had the idea of coordinates in three dimensions but did not develop it.
J.Bernoulli (1667-1748) in a letter of 1715 to Leibnitz introduced the three coordinate planes which we use today. It was Antoinette Parent
(1666-1716), who gave a systematic development of analytical solid geometry
for the first time in a paper presented to the French Academy in 1700.
L.Euler (1707-1783) took up systematically the three dimensional coordinate geometry, in Chapter 5 of the appendix to the second volume of his “Introduction
to Geometry” in 1748.
It was not until the middle of the nineteenth century that geometry was extended
to more than three dimensions, the well-known application of which is in the
Space-Time Continuum of Einstein’s Theory of Relativity.

<!-- page 344 -->
Chapter

LIMITS AND DERIVATIVES

With the Calculus as a key, Mathematics can be successfully applied to the
explanation of the course of Nature – WHITEHEAD

13.1 Introduction

This chapter is an introduction to Calculus. Calculus is that
branch of mathematics which mainly deals with the study
of change in the value of a function as the points in the
domain change. First, we give an intuitive idea of derivative
(without actually defining it). Then we give a naive definition
of limit and study some algebra of limits. Then we come
back to a definition of derivative and study some algebra
of derivatives. We also obtain derivatives of certain
standard functions.

Sir Issac Newton
(1642-1727)

13.2 Intuitive Idea of Derivatives

Physical experiments have confirmed that the body dropped (1642-1727)
from a tall cliff covers a distance of $4.9t^2$ metres in $t$ seconds,
i.e., distance $s$ in metres covered by the body as a function of time $t$ in seconds is given
by $s = 4.9t^2$.

The adjoining Table 13.1 gives the distance travelled in metres at various intervals
of time in seconds of a body dropped from a tall cliff.

The objective is to find the veloctiy of the body at time $t = 2$ seconds from this
data. One way to approach this problem is to find the average velocity for various
intervals of time ending at $t = 2$ seconds and hope that these throw some light on the
velocity at $t = 2$ seconds.

Average velocity between $t = t_1$ and $t = t_2$ equals distance travelled between
$t = t_1$ and $t = t_2$ seconds divided by $(t_2 - t_1)$. Hence the average velocity in the first
two seconds

<!-- page 345 -->
$$= \frac{\text{Distance travelled between } t_2 = 2 \text{ and } t_1 = 0}{\text{Time interval } (t_2 - t_1)}$$

$$= \frac{(19.6 - 0)m}{(2 - 0)s} = 9.8 m/s.$$

Similarly, the average velocity between $t = 1$
and $t = 2$ is

$$\frac{(19.6 - 4.9)m}{(2 - 1)s} = 14.7 \ m/s$$

Likewise we compute the average velocitiy
between $t = t_1$ and $t = 2$ for various $t_1$. The following
Table 13.2 gives the average velocity ($v$), $t = t_1$
seconds and $t = 2$ seconds.

Table 13.1

<table>
<thead>
<tr>
<th>$t$</th>
<th>$s$</th>
</tr>
</thead>
<tbody>
<tr>
<td>0</td>
<td>0</td>
</tr>
<tr>
<td>1</td>
<td>4.9</td>
</tr>
<tr>
<td>1.5</td>
<td>11.025</td>
</tr>
<tr>
<td>1.8</td>
<td>15.876</td>
</tr>
<tr>
<td>1.9</td>
<td>17.689</td>
</tr>
<tr>
<td>1.95</td>
<td>18.63225</td>
</tr>
<tr>
<td>2</td>
<td>19.6</td>
</tr>
<tr>
<td>2.05</td>
<td>20.59225</td>
</tr>
<tr>
<td>2.1</td>
<td>21.609</td>
</tr>
<tr>
<td>2.2</td>
<td>23.716</td>
</tr>
<tr>
<td>2.5</td>
<td>30.625</td>
</tr>
<tr>
<td>3</td>
<td>44.1</td>
</tr>
<tr>
<td>4</td>
<td>78.4</td>
</tr>
</tbody>
</table>

Table 13.2

<table>
<thead>
<tr>
<th>$t_1$</th>
<th>0</th>
<th>1</th>
<th>1.5</th>
<th>1.8</th>
<th>1.9</th>
<th>1.95</th>
<th>1.99</th>
</tr>
</thead>
<tbody>
<tr>
<td>$v$</td>
<td>9.8</td>
<td>14.7</td>
<td>17.15</td>
<td>18.62</td>
<td>19.11</td>
<td>19.355</td>
<td>19.551</td>
</tr>
</tbody>
</table>

From Table 13.2, we observe that the average velocity is gradually increasing.
As we make the time intervals ending at $t = 2$ smaller, we see that we get a better idea
of the velocity at $t = 2$. Hoping that nothing really dramatic happens between 1.99
seconds and 2 seconds, we conclude that the average velocity at $t = 2$ seconds is just
above $19.551m/s$.

This conclusion is somewhat strengthened by the following set of computation.
Compute the average velocities for various time intervals starting at $t = 2$ seconds. As
before the average velocity $v$ between $t = 2$ seconds and $t = t_2$ seconds is

$$= \frac{\text{Distance travelled between 2 seconds and } t_2 \text{ seconds}}{t_2 - 2}$$

$$= \frac{\text{Distance travelled in } t_2 \text{ seconds } - \text{ Distance travelled in } 2 \text{ seconds}}{t_2 - 2}$$

<!-- page 346 -->
$$= \frac{\text{Distance travelled in } t_2 \text{ seconds } - 19.6}{t_2 - 2}$$

The following Table 13.3 gives the average velocity $v$ in metres per second
between $t = 2$ seconds and $t_2$ seconds.

Table 13.3

<table>
<thead>
<tr>
<th>$t_2$</th>
<th>4</th>
<th>3</th>
<th>2.5</th>
<th>2.2</th>
<th>2.1</th>
<th>2.05</th>
<th>2.01</th>
</tr>
</thead>
<tbody>
<tr>
<td>$v$</td>
<td>29.4</td>
<td>24.5</td>
<td>22.05</td>
<td>20.58</td>
<td>20.09</td>
<td>19.845</td>
<td>19.649</td>
</tr>
</tbody>
</table>

Here again we note that if we take smaller time intervals starting at $t = 2$, we get
better idea of the velocity at $t = 2$.

In the first set of computations, what we have done is to find average velocities
in increasing time intervals ending at $t = 2$ and then hope that nothing dramatic happens
just before $t = 2$. In the second set of computations, we have found the average velocities
decreasing in time intervals ending at $t = 2$ and then hope that nothing dramatic happens
just after $t = 2$. Purely on the physical grounds, both these sequences of average
velocities must approach a common limit. We can safely conclude that the velocity of
the body at $t = 2$ is between $19.551 m/s$ and $19.649 \ m/s$. Technically, we say that the
instantaneous velocity at $t = 2$ is between $19.551 \ m/s$ and $19.649 \ m/s$. As is
well-known, $velocity$ $is$ $the$ $rate$ $of$ $change$ $of$ $displacement$. Hence what we have
accomplished is the following. From the given data of distance covered at various time
instants we have estimated the rate of
change of the distance at a given instant
of time. We say that the $derivative$ of
the distance function $s = 4.9t^2$ at $t = 2$
is between $19.551$ and $19.649$.

An alternate way of viewing this
limiting process is shown in Fig 13.1.
This is a plot of distance $s$ of the body
from the top of the cliff versus the time
$t$ elapsed. In the limit as the sequence
of time intervals $h_1, h_2, ...,$ approaches
zero, the sequence of average velocities
approaches the same limit as does the
sequence of ratios

Fig 13.1

<!-- page 347 -->
$$\frac{\mathbf{C}_1\mathbf{B}_1}{\mathbf{AC}_1}, \frac{\mathbf{C}_2\mathbf{B}_2}{\mathbf{AC}_2}, \frac{\mathbf{C}_3\mathbf{B}_3}{\mathbf{AC}_3}, \dots$$

where $\mathrm{C}_1\mathrm{B}_1 = s_1 - s_0$ is the distance travelled by the body in the time interval $h_1 = \mathrm{AC}_1$,
etc. From the Fig 13.1 it is safe to conclude that this latter sequence approaches the
slope of the tangent to the curve at point A. In other words, the instantaneous velocity
$v(t)$ of a body at time $t = 2$ is equal to the slope of the tangent of the curve $s = 4.9t^2$ at
$t = 2$.

13.3 Limits

The above discussion clearly points towards the fact that we need to understand limiting
process in greater clarity. We study a few illustrative examples to gain some familiarity
with the concept of limits.

Consider the function $f(x) = x^2$. Observe that as $x$ takes values very close to 0,
the value of $f(x)$ also moves towards 0 (See Fig 2.10 Chapter 2). We say

$$\lim_{x \to 0} f(x) = 0$$

(to be read as limit of $f(x)$ as $x$ tends to zero equals zero). The limit of $f(x)$ as $x$ tends
to zero is to be thought of as the value $f(x)$ should assume at $x = 0$.

In general as $x \rightarrow a, f(x) \rightarrow l$, then $l$ is called limit of the function $f(x)$ which is
symbolically written as $\lim_{x \rightarrow a} f(x)=l$.

Consider the following function $g(x) = |x|, x \neq 0$. Observe that $g(0)$ is not defined.
Computing the value of $g(x)$ for values of $x$ very
near to 0, we see that the value of $g(x)$ moves
towards 0. So, $\lim_{x \to 0} g(x) = 0$. This is intuitively
clear from the graph of $y = |x|$ for $x \neq 0$.
(See Fig 2.13, Chapter 2).

Consider the following function.

$$h(x)=\frac{x^{2}-4}{x-2}, x \neq 2 .$$

Fig 13.2

Compute the value of $h(x)$ for values of
$x$ very near to 2 (but not at 2). Convince yourself
that all these values are near to 4. This is
somewhat strengthened by considering the graph
of the function $y = h(x)$ given here (Fig 13.2).

<!-- page 348 -->
In all these illustrations the value which the function should assume at a given
point $x = a$ did not really depend on how is $x$ tending to $a$. Note that there are essentially
two ways $x$ could approach a number $a$ either from left or from right, i.e., all the
values of $x$ near $a$ could be less than $a$ or could be greater than $a$. This naturally leads
to two limits – the \textit{right hand limit} and the \textit{left hand limit}. \textit{Right hand limit} of a
function $f(x)$ is that value of $f(x)$ which is dictated by the values of $f(x)$ when $x$ tends
to $a$ from the right. Similarly, the \textit{left hand limit}. To illustrate this, consider the function

$$f(x)=\begin{cases}1, & x\le0\\2, & x>0\end{cases}$$

Graph of this function is shown in the Fig 13.3. It is
clear that the value of $f$ at 0 dictated by values of $f(x)$ with
$x \leq 0$ equals 1, i.e., the left hand limit of $f(x)$ at 0 is

$$\lim_{x \to 0} f(x) = 1.$$

Fig 13.3

Similarly, the value of $f$ at 0 dictated by values of
$f(x)$ with $x > 0$ equals 2, i.e., the right hand limit of $f(x)$
at 0 is

$$\lim_{x \to 0^+} f(x) = 2.$$

In this case the right and left hand limits are different, and hence we say that the
limit of $f(x)$ as $x$ tends to zero does not exist (even though the function is defined at 0).

Summary

We say $\lim_{x \to a^-} f(x)$ is the expected value of $f$ at $x = a$ given the values of $f$ near
$x$ to the left of $a$. This value is called the left hand limit of $f$ at $a$.

We say $\lim_{x \to a^+} f(x)$ is the expected value of $f$ at $x = a$ given the values of
$f$ near $x$ to the right of $a$. This value is called the right hand limit of $f(x)$ at $a$.
If the right and left hand limits coincide, we call that common value as the limit
of $f(x)$ at $x = a$ and denote it by $\lim_{x \to a} f(x)$.

Illustration 1 Consider the function $f(x) = x + 10$. We want to find the limit of this
function at $x = 5$. Let us compute the value of the function $f(x)$ for $x$ very near to 5.
Some of the points near and to the left of 5 are 4.9, 4.95, 4.99, 4.995. . . , etc. Values
of the function at these points are tabulated below. Similarly, the real number 5.001,

<!-- page 349 -->
5.01, 5.1 are also points near and to the right of 5. Values of the function at these points
are also given in the Table 13.4.

Table 13.4

<table>
<thead>
<tr>
<th>x</th>
<th>4.9</th>
<th>4.95</th>
<th>4.99</th>
<th>4.995</th>
<th>5.001</th>
<th>5.01</th>
<th>5.1</th>
</tr>
</thead>
<tbody>
<tr>
<td>f(x)</td>
<td>14.9</td>
<td>14.95</td>
<td>14.99</td>
<td>14.995</td>
<td>15.001</td>
<td>15.01</td>
<td>15.1</td>
</tr>
</tbody>
</table>

From the Table 13.4, we deduce that value of $f(x)$ at $x = 5$ should be greater than
14.995 and less than 15.001 assuming nothing dramatic happens between $x = 4.995$
and 5.001. It is reasonable to assume that the value of the $f(x)$ at $x = 5$ as dictated by
the numbers to the left of 5 is 15, i.e.,

$$\lim_{x \to 5^-} f(x) = 15.$$

Similarly, when $x$ approaches 5 from the right, $f(x)$ should be taking value 15, i.e.,

$$\lim_{x \to 5^+} f(x) = 15.$$

Hence, it is likely that the left hand limit of $f(x)$ and the right hand limit of $f(x)$ are
both equal to 15. Thus,

$$\lim_{x \to 5^-} f(x) = \lim_{x \to 5^+} f(x) = \lim_{x \to 5} f(x) = 15 .$$

This conclusion about the limit being equal to 15 is somewhat strengthened by
seeing the graph of this function which is given in Fig 2.16, Chapter 2. In this figure, we
note that as $x$ approaches 5 from either right or left, the graph of the function
$f(x) = x +10$ approaches the point $(5, 15)$.

We observe that the value of the function at $x = 5$ also happens to be equal to 15.

Illustration 2 Consider the function $f(x) = x^3$. Let us try to find the limit of this
function at $x = 1$. Proceeding as in the previous case, we tabulate the value of $f(x)$ at
$x$ near 1. This is given in the Table 13.5.

Table 13.5

<table>
<thead>
<tr>
<th>$x$</th>
<th>0.9</th>
<th>0.99</th>
<th>0.999</th>
<th>1.001</th>
<th>1.01</th>
<th>1.1</th>
</tr>
</thead>
<tbody>
<tr>
<td>$f(x)$</td>
<td>0.729</td>
<td>0.970299</td>
<td>0.997002999</td>
<td>1.003003001</td>
<td>1.030301</td>
<td>1.331</td>
</tr>
</tbody>
</table>

From this table, we deduce that value of $f(x)$ at $x = 1$ should be greater than
0.997002999 and less than 1.003003001 assuming nothing dramatic happens between

<!-- page 350 -->
$x = 0.999$ and $1.001$. It is reasonable to assume that the value of the $f(x)$ at $x = 1$ as
dictated by the numbers to the left of $1$ is $1$, i.e.,

$$\lim_{x \to 1^-} f(x) = 1.$$

Similarly, when $x$ approaches 1 from the right, $f(x)$ should be taking value 1, i.e.,

$$\lim_{x \to 1^+} f(x) = 1.$$

Hence, it is likely that the left hand limit of $f(x)$ and the right hand limit of $f(x)$ are
both equal to 1. Thus,

$$\lim_{x \to 1^-} f(x) = \lim_{x \to 1^+} f(x) = \lim_{x \to 1} f(x) = 1.$$

This conclusion about the limit being equal to 1 is somewhat strengthened by
seeing the graph of this function which is given in Fig 2.11, Chapter 2. In this figure, we
note that as $x$ approaches 1 from either right or left, the graph of the function
$f(x) = x^3$ approaches the point $(1, 1)$.

We observe, again, that the value of the function at $x = 1$ also happens to be
equal to 1.

Illustration 3 Consider the function $f(x) = 3x$. Let us try to find the limit of this
function at $x = 2$. The following Table 13.6 is now self-explanatory.

Table 13.6

<table>
<thead>
<tr>
<th>$x$</th>
<th>1.9</th>
<th>1.95</th>
<th>1.99</th>
<th>1.999</th>
<th>2.001</th>
<th>2.01</th>
<th>2.1</th>
</tr>
</thead>
<tbody>
<tr>
<td>$f(x)$</td>
<td>5.7</td>
<td>5.85</td>
<td>5.97</td>
<td>5.997</td>
<td>6.003</td>
<td>6.03</td>
<td>6.3</td>
</tr>
</tbody>
</table>

As before we observe that as $x$ approaches 2
from either left or right, the value of $f(x)$ seem to
approach 6. We record this as

$$\lim_{x \to 2^-} f(x) = \lim_{x \to 2^+} f(x) = \lim_{x \to 2} f(x) = 6$$

Its graph shown in Fig 13.4 strengthens this
fact.

Here again we note that the value of the function
at $x = 2$ coincides with the limit at $x = 2$.

Fig 13.4

Illustration 4 Consider the constant function
$f(x) = 3$. Let us try to find its limit at $x = 2$. This
function being the constant function takes the same

<!-- page 351 -->
value (3, in this case) everywhere, i.e., its value at points close to 2 is 3. Hence

$$\lim_{x \to 2^-} f(x) = \lim_{x \to 2^+} f(x) = \lim_{x \to 2} f(x) = 3$$

Graph of $f(x) = 3$ is anyway the line parallel to $x$-axis passing through $(0, 3)$ and
is shown in Fig 2.9, Chapter 2. From this also it is clear that the required limit is 3. In
fact, it is easily observed that $\lim_{x \to a} f(x) = 3$ for any real number $a$.

Illustration 5 Consider the function $f(x) = x^2 + x$. We want to find $\lim_{x \to 1} f(x)$. We
tabulate the values of $f(x)$ near $x = 1$ in Table 13.7.

Table 13.7

<table>
<thead>
<tr>
<th>$x$</th>
<th>0.9</th>
<th>0.99</th>
<th>0.999</th>
<th>1.01</th>
<th>1.1</th>
<th>1.2</th>
</tr>
</thead>
<tbody>
<tr>
<td>$f(x)$</td>
<td>1.71</td>
<td>1.9701</td>
<td>1.997001</td>
<td>2.0301</td>
<td>2.31</td>
<td>2.64</td>
</tr>
</tbody>
</table>

From this it is reasonable to deduce that

$$\lim_{x \to 1^-} f(x) = \lim_{x \to 1^+} f(x) = \lim_{x \to 1} f(x) = 2.$$

From the graph of $f(x) = x^2 + x$
shown in the Fig 13.5, it is clear that as $x$
approaches 1, the graph approaches (1, 2).

Here, again we observe that the

$$\lim_{x \to 1} f(x) = f(1)$$

Y' Fig 13.5

Now, convince yourself of the
following three facts:

$$\lim_{x \to 1} x^2 = 1, \lim_{x \to 1} x = 1 \text{ and } \lim_{x \to 1} x + 1 = 2$$

Then $\lim_{x \to 1} x^2 + \lim_{x \to 1} x = 1 + 1 = 2 = \lim_{x \to 1} \left[ x^2 + x \right].$

Also $\lim_{x \to 1} x \cdot \lim_{x \to 1} (x+1) = 1.2 = 2 = \lim_{x \to 1} [x(x+1)] = \lim_{x \to 1} [x^2 + x].$

<!-- page 352 -->
Illustration 6 Consider the function $f(x) = \sin x$. We are interested in $\lim_{x \to \frac{\pi}{2}} \sin x$,

where the angle is measured in radians.

Here, we tabulate the (approximate) value of $f(x)$ near $\frac{\pi}{2}$ (Table 13.8). From
this, we may deduce that

$$\lim_{x \to \frac{\pi^-}{2}} f(x) = \lim_{x \to \frac{\pi^+}{2}} f(x) = \lim_{x \to \frac{\pi}{2}} f(x) = 1$$

Further, this is supported by the graph of $f(x) = \sin x$ which is given in the Fig 3.8

(Chapter 3). In this case too, we observe that $\lim_{x \to \frac{\pi}{2}} \sin x = 1$.

Table 13.8

<table>
<thead>
<tr>
<th>$x$</th>
<th>$\frac{\pi}{2}-0.1$</th>
<th>$\frac{\pi}{2}-0.01$</th>
<th>$\frac{\pi}{2}+0.01$</th>
<th>$\frac{\pi}{2}+0.1$</th>
</tr>
</thead>
<tbody>
<tr>
<td>$f(x)$</td>
<td>0.9950</td>
<td>0.9999</td>
<td>0.9999</td>
<td>0.9950</td>
</tr>
</tbody>
</table>

Illustration 7 Consider the function $f(x) = x + \cos x$. We want to find the $\lim_{x \to 0} f(x)$.

Here we tabulate the (approximate) value of $f(x)$ near 0 (Table 13.9).

Table 13.9

<table>
<thead>
<tr>
<th>$x$</th>
<th>$-0.1$</th>
<th>$-0.01$</th>
<th>$-0.001$</th>
<th>$0.001$</th>
<th>$0.01$</th>
<th>$0.1$</th>
</tr>
</thead>
<tbody>
<tr>
<td>$f(x)$</td>
<td>0.9850</td>
<td>0.98995</td>
<td>0.9989995</td>
<td>1.0009995</td>
<td>1.00995</td>
<td>1.0950</td>
</tr>
</tbody>
</table>

From the Table 13.9, we may deduce that

$$\lim_{x \to 0^-} f(x) = \lim_{x \to 0^+} f(x) = \lim_{x \to 0} f(x) = 1$$

In this case too, we observe that $\lim_{x \to 0} f(x) = f(0) = 1.$

Now, can you convince yourself that

$$\lim_{x \to 0} [x + \cos x] = \lim_{x \to 0} x + \lim_{x \to 0} \cos x \text{ is indeed true?}$$

<!-- page 353 -->
Illustration 8 Consider the function $f(x)=\frac{1}{x^{2}}$ for $x>0$. We want to know $\lim _{x \rightarrow 0} f(x)$.

Here, observe that the domain of the function is given to be all positive real
numbers. Hence, when we tabulate the values of $f(x)$, it does not make sense to talk of
$x$ approaching $0$ from the left. Below we tabulate the values of the function for positive
$x$ close to $0$ (in this table $n$ denotes any positive integer).

From the Table 13.10 given below, we see that as $x$ tends to 0, $f(x)$ becomes
larger and larger. What we mean here is that the value of $f(x)$ may be made larger than
any given number.

Table 13.10

<table>
<tbody>
<tr>
<td>$x$</td>
<td>1</td>
<td>0.1</td>
<td>0.01</td>
<td>$10^{-n}$</td>
</tr>
<tr>
<td>$f(x)$</td>
<td>1</td>
<td>100</td>
<td>10000</td>
<td>$10^{2n}$</td>
</tr>
</tbody>
</table>

Mathematically, we say

$$\lim_{x \to 0} f(x) = +\infty$$

We also remark that we will not come across such limits in this course.

Illustration 9 We want to find $\lim_{x \to 0} f(x)$, where

$$f(x)=\begin{cases}x-2, & x<0\\0,&x=0\\x+2, & x>0\end{cases}$$

As usual we make a table of $x$ near 0 with $f(x)$. Observe that for negative values of $x$
we need to evaluate $x-2$ and for positive values, we need to evaluate $x+2$.

Table 13.11

<table>
<thead>
<tr>
<th>x</th>
<th>- 0.1</th>
<th>- 0.01</th>
<th>- 0.001</th>
<th>0.001</th>
<th>0.01</th>
<th>0.1</th>
</tr>
</thead>
<tbody>
<tr>
<td>f(x)</td>
<td>- 2.1</td>
<td>- 2.01</td>
<td>- 2.001</td>
<td>2.001</td>
<td>2.01</td>
<td>2.1</td>
</tr>
</tbody>
</table>

From the first three entries of the Table 13.11, we deduce that the value of the
function is decreasing to $-2$ and hence.

$$\lim_{x \to 0^-} f(x) = -2$$

<!-- page 354 -->
From the last three entires of the table we deduce that the value of the function
is increasing from 2 and hence

$$\lim_{x \to 0^+} f(x) = 2$$

Since the left and right hand limits at 0 do not coincide,
we say that the limit of the function at 0 does not exist.
Graph of this function is given in the Fig13.6. Here,
we remark that the value of the function at $x = 0$ is well
defined and is, indeed, equal to 0, but the limit of the function
at $x = 0$ is not even defined.

Fig 13.6

Illustration 10 As a final illustration, we find $\lim_{x \to 1} f(x)$,

where

$$f(x) = \begin{cases} x + 2 & x \neq 1 \\ 0 & x = 1 \end{cases}$$

Table 13.12

<table>
<thead>
<tr>
<th>$x$</th>
<th>0.9</th>
<th>0.99</th>
<th>0.999</th>
<th>1.001</th>
<th>1.01</th>
<th>1.1</th>
</tr>
</thead>
<tbody>
<tr>
<td>$f(x)$</td>
<td>2.9</td>
<td>2.99</td>
<td>2.999</td>
<td>3.001</td>
<td>3.01</td>
<td>3.1</td>
</tr>
</tbody>
</table>

As usual we tabulate the values of $f(x)$ for $x$ near 1. From the values of $f(x)$ for
$x$ less than 1, it seems that the function should take value 3 at $x = 1.$, i.e.,

$$\lim_{x \to 1^-} f(x) = 3.$$

Similarly, the value of $f(x)$ should be 3 as dictated by values of $f(x)$ at $x$ greater than 1. i.e.

$$\lim_{x \to 1^+} f(x) = 3.$$

But then the left and right hand limits coincide
and hence

Fig 13.7

$$\lim_{x \to 1^-} f(x) = \lim_{x \to 1^+} f(x) = \lim_{x \to 1} f(x) = 3.$$

Graph of function given in Fig 13.7 strengthens
our deduction about the limit. Here, we

<!-- page 355 -->
note that in general, at a given point the value of the function and its limit may be
different (even when both are defined).

13.3.1 *Algebra of limits* In the above illustrations, we have observed that the limiting
process respects addition, subtraction, multiplication and division as long as the limits
and functions under consideration are well defined. This is not a coincidence. In fact,
below we formalise these as a theorem without proof.

Theorem 1 Let $f$ and $g$ be two functions such that both $\lim_{x \to a} f(x)$ and $\lim_{x \to a} g(x)$ exist.

Then

(i) Limit of sum of two functions is sum of the limits of the functions, i.e.,
$$\lim_{x \to a} [f(x) + g(x)] = \lim_{x \to a} f(x) + \lim_{x \to a} g(x).$$
(ii) Limit of difference of two functions is difference of the limits of the functions, i.e.,
$$\lim_{x \to a} [f(x) - g(x)] = \lim_{x \to a} f(x) - \lim_{x \to a} g(x).$$
(iii) Limit of product of two functions is product of the limits of the functions, i.e.,
$$\lim_{x \to a} [f(x) \cdot g(x)] = \lim_{x \to a} f(x) \cdot \lim_{x \to a} g(x).$$
(iv) Limit of quotient of two functions is quotient of the limits of the functions (whenever
the denominator is non zero), i.e.,

$$\lim_{x \to a} \frac{f(x)}{g(x)} = \frac{\lim_{x \to a} f(x)}{\lim_{x \to a} g(x)}$$

Note In particular as a special case of (iii), when $g$ is the constant function
such that $g(x) = \lambda$, for some real number $\lambda$, we have

$$\lim_{x \to a} [(\lambda.f)(x)] = \lambda. \lim_{x \to a} f(x).$$

In the next two subsections, we illustrate how to exploit this theorem to evaluate
limits of special types of functions.

13.3.2 *Limits of polynomials and rational functions* A function $f$ is said to be a
polynomial function of degree $n$ $f(x) = a_0 + a_1x + a_2x^2 + \dots + a_nx^n$, where $a_1s$ are real
numbers such that $a_n \neq 0$ for some natural number $n$.

We know that $\lim_{x \to a} x = a$. Hence

<!-- page 356 -->
$$\lim_{x \to a} x^2 = \lim_{x \to a} (x.x) = \lim_{x \to a} x. \lim_{x \to a} x = a. a = a^2$$

An easy exercise in induction on $n$ tells us that

$$\lim_{x \to a} x^n = a^n$$

Now, let $f(x)=a_{0}+a_{1}x+a_{2}x^{2}+\ldots+a_{n}x^{n}$ be a polynomial function. Thinking
of each of $a_{0}, a_{1}x, a_{2}x^{2},...,a_{n}x^{n}$ as a function, we have

$$\lim_{x \to a} f(x) = \lim_{x \to a} \left[ a_0 + a_1 x + a_2 x^2 + ... + a_n x^n \right]$$

$$= \lim_{x \to a} a_0 + \lim_{x \to a} a_1 x + \lim_{x \to a} a_2 x^2 + ... + \lim_{x \to a} a_n x^n$$

$$= a_0 + a_1 \lim_{x \to a} x + a_2 \lim_{x \to a} x^2 + ... + a_n \lim_{x \to a} x^n$$

$$= a_0 + a_1 a + a_2 a^2 + ... + a_n a^n$$

$$= f(a)$$

(Make sure that you understand the justification for each step in the above!)

A function $f$ is said to be a rational function, if $f(x) = \frac{g(x)}{h(x)}$, where $g(x)$ and $h(x)$

are polynomials such that $h(x) \neq 0$. Then

are polynomials such that $h(x) \neq 0$. Then

$$\lim_{x \to a} f(x) = \lim_{x \to a} \frac{g(x)}{h(x)} = \frac{\lim_{x \to a} g(x)}{\lim_{x \to a} h(x)} = \frac{g(a)}{h(a)}$$

However, if $h(a) = 0$, there are two scenarios – (i) when $g(a) \neq 0$ and (ii) when
$g(a) = 0$. In the former case we say that the limit does not exist. In the latter case we
can write $g(x) = (x - a)^k g_1(x)$, where $k$ is the maximum of powers of $(x - a)$ in $g(x)$
Similarly, $h(x) = (x - a)^l h_1(x)$ as $h(a) = 0$. Now, if $k > l$, we have

$$\lim_{x \to a} f(x) = \frac{\lim_{x \to a} g(x)}{\lim_{x \to a} h(x)} = \frac{\lim_{x \to a} (x - a)^k g_1(x)}{\lim_{x \to a} (x - a)^l h_1(x)}$$

<!-- page 357 -->
$$= \frac{\lim_{x \to a} (x - a)^{(k-l)} g_1(x)}{\lim_{x \to a} h_1(x)} = \frac{0 \cdot g_1(a)}{h_1(a)} = 0$$

If $k < l$, the limit is not defined.

Example 1 Find the limits: (i) $\lim_{x \to 1} \left[ x^3 - x^2 + 1 \right]$ (ii) $\lim_{x \to 3} \left[ x(x+1) \right]$


(iii) $\lim_{x \to -1} \left[ 1 + x + x^2 + ... + x^{10} \right]$.


Solution The required limits are all limits of some polynomial functions. Hence the
limits are the values of the function at the prescribed points. We have


(i) $\lim_{x \to 1} \left[ x^3 - x^2 + 1 \right] = 1^3 - 1^2 + 1 = 1$


(ii) $\lim_{x \to 3} \left[ x(x+1) \right] = 3(3+1) = 3(4) = 12$


(iii) $\lim_{x \to -1} \left[ 1 + x + x^2 + ... + x^{10} \right] = 1 + (-1) + (-1)^2 + ... + (-1)^{10}$
$= 1 - 1 + 1 ... + 1 = 1.$

Example 2 Find the limits:

(i) $$\lim_{x \to 1} \left[ \frac{x^2 + 1}{x + 100} \right]$$

(ii) $$\lim_{x \to 2} \left[ \frac{x^3 - 4x^2 + 4x}{x^2 - 4} \right]$$

(iii) $$\lim_{x \to 2} \left[ \frac{x^2 - 4}{x^3 - 4x^2 + 4x} \right]$$

(iv) $$\lim_{x \to 2} \left[ \frac{x^3 - 2x^2}{x^2 - 5x + 6} \right]$$

(v) $$\lim_{x \to 1} \left[ \frac{x - 2}{x^2 - x} - \frac{1}{x^3 - 3x^2 + 2x} \right]$$

Solution All the functions under consideration are rational functions. Hence, we first


evaluate these functions at the prescribed points. If this is of the form $\frac{0}{0}$, we try to


rewrite the function cancelling the factors which are causing the limit to be of


the form $\frac{0}{0}$.

<!-- page 358 -->
(i) We have $\lim_{x \to 1} \frac{x^2 + 1}{x + 100} = \frac{1^2 + 1}{1 + 100} = \frac{2}{101}$

(ii) Evaluating the function at 2, it is of the form $\frac{0}{0}$.

Hence $\lim_{x \to 2} \frac{x^3 - 4x^2 + 4x}{x^2 - 4} = \lim_{x \to 2} \frac{x(x-2)^2}{(x+2)(x-2)}$

$= \lim_{x \to 2} \frac{x(x-2)}{(x+2)}$ as $x \neq 2$

$= \frac{2(2-2)}{2+2} = \frac{0}{4} = 0.$

(iii) Evaluating the function at 2, we get it of the form $\frac{0}{0}$.

Hence $\lim_{x\to2}\frac{x^2-4}{x^3-4x^2+4x}=\lim_{x\to2}\frac{(x+2)(x-2)}{x(x-2)^2}$
$=\lim_{x\to2}\frac{(x+2)}{x(x-2)}=\frac{2+2}{2(2-2)}=\frac{4}{0}$

which is not defined.

(iv) Evaluating the function at 2, we get it of the form $\frac{0}{0}$.

Hence $\lim_{x \to 2} \frac{x^3 - 2x^2}{x^2 - 5x + 6} = \lim_{x \to 2} \frac{x^2(x - 2)}{(x - 2)(x - 3)}$

$= \lim_{x \to 2} \frac{x^2}{(x - 3)} = \frac{(2)^2}{2 - 3} = \frac{4}{-1} = -4.$

<!-- page 359 -->
(v) First, we rewrite the function as a rational function.

$$\left[ \frac{x-2}{x^2-x} - \frac{1}{x^3-3x^2+2x} \right] = \left[ \frac{x-2}{x(x-1)} - \frac{1}{x(x^2-3x+2)} \right]$$


$$= \left[ \frac{x-2}{x(x-1)} - \frac{1}{x(x-1)(x-2)} \right]$$


$$= \left[ \frac{x^2-4x+4-1}{x(x-1)(x-2)} \right]$$


$$= \frac{x^2-4x+3}{x(x-1)(x-2)}$$

Evaluating the function at 1, we get it of the form $\frac{0}{0}$.

Hence $\lim_{x \to 1} \left[ \frac{x^2 - 2}{x^2 - x} - \frac{1}{x^3 - 3x^2 + 2x} \right] = \lim_{x \to 1} \frac{x^2 - 4x + 3}{x(x-1)(x-2)}$
$= \lim_{x \to 1} \frac{(x-3)(x-1)}{x(x-1)(x-2)}$
$= \lim_{x \to 1} \frac{x-3}{x(x-2)} = \frac{1-3}{1(1-2)} = 2.$

We remark that we could cancel the term $(x - 1)$ in the above evaluation because
$x \neq 1$.

Evaluation of an important limit which will be used in the sequel is given as a
theorem below.

Theorem 2 For any positive integer $n$,

$$\lim_{x \to a} \frac{x^n - a^n}{x - a} = n a^{n-1}.$$

Remark The expression in the above theorem for the limit is true even if $n$ is any
rational number and $a$ is positive.

<!-- page 360 -->
Proof Dividing $(x^n - a^n)$ by $(x - a)$, we see that

$$x^n - a^n = (x-a) \ (x^{n-1} + x^{n-2} a + x^{n-3} a^2 + ... + x a^{n-2} + a^{n-1})$$

Thus, $\lim_{x \to a} \frac{x^n - a^n}{x - a} = \lim_{x \to a} (x^{n-1} + x^{n-2} a + x^{n-3} a^2 + ... + x a^{n-2} + a^{n-1})$

$$= a^{n - 1} + a a^{n-2} + ... + a^{n-2} (a) + a^{n-1}$$

$$= a^{n-1} + a^{n - 1} +...+a^{n-1} + a^{n-1} \ (n \text{ terms})$$

$$= na^{n-1}$$

Example 3 Evaluate:

(i) $\lim_{x \to 1} \frac{x^{15} - 1}{x^{10} - 1}$ (ii) $\lim_{x \to 0} \frac{\sqrt{1+x} - 1}{x}$

Solution (i) We have

$$\lim_{x \to 1} \frac{x^{15} - 1}{x^{10} - 1} = \lim_{x \to 1} \left[ \frac{x^{15} - 1}{x - 1} \div \frac{x^{10} - 1}{x - 1} \right]$$

$$= \lim_{x \to 1} \left[ \frac{x^{15} - 1}{x - 1} \right] \div \lim_{x \to 1} \left[ \frac{x^{10} - 1}{x - 1} \right]$$

$$= 15(1)^{14} \div 10(1)^9 \text{ (by the theorem above)}$$

$$= 15 \div 10 = \frac{3}{2}$$

(ii) Put $y = 1 + x$, so that $y \rightarrow 1$ as $x \rightarrow 0$.

Then $\lim_{x \to 0} \frac{\sqrt{1+x}-1}{x} = \lim_{y \to 1} \frac{\sqrt{y}-1}{y-1}$

$= \lim_{y \to 1} \frac{y^{\frac{1}{2}}-1^{\frac{1}{2}}}{y-1}$

$= \frac{1}{2}(1)^{\frac{1}{2}-1}$ (by the remark above) $= \frac{1}{2}$

<!-- page 361 -->
13.4 Limits of Trigonometric Functions

The following facts (stated as theorems) about functions in general come in handy in
calculating limits of some trigonometric functions.

Theorem 3 Let $f$ and $g$ be two real valued functions with the same domain such that


$f(x) \leq \text{g}(x)$ for all $x$ in the domain of definition, For some $a$, if both $\lim_{x \to a} f(x)$ and


$\lim_{x \to a} g(x)$ exist, then $\lim_{x \to a} f(x) \leq \lim_{x \to a} g(x)$. This is illustrated in Fig 13.8.

Fig 13.8

Theorem 4 (Sandwich Theorem) Let $f$, $g$ and $h$ be real functions such that
$f(x) \leq g(x) \leq h(x)$ for all $x$ in the common domain of definition. For some real number

$a$, if $\lim_{x \to a} f(x) = l = \lim_{x \to a} h(x)$, then $\lim_{x \to a} g(x) = l$. This is illustrated in Fig 13.9.

Fig 13.9

Given below is a beautiful geometric proof of the following important
inequality relating trigonometric functions.

$$\cos x < \frac{\sin x}{x} < 1 \quad \text{for } 0 < |x| < \frac{\pi}{2} \tag{*}$$

<!-- page 362 -->
Proof We know that $\sin (-x) = -\sin x$ and $\cos(-x) = \cos x$. Hence, it is sufficient

to prove the inequality for $0 < x < \frac{\pi}{2}$.

In the Fig 13.10, O is the centre of the unit circle such that

Fig 13.10

the angle AOC is $x$ radians and $0 < x < \frac{\pi}{2}$. Line segments B A and

CD are perpendiculars to OA. Further, join AC. Then

Area of $\Delta OAC <$ Area of sector $OAC <$ Area of $\Delta OAB$.

i.e., $\frac{1}{2}\text{OA.CD} < \frac{x}{2\pi}.\pi.(\text{OA})^2 < \frac{1}{2}\text{OA.AB}.$

i.e., CD $< x$. OA $< AB$.

From $\Delta$ OCD,

$\sin x = \frac{\mathrm{CD}}{\mathrm{OA}}$ (since $\mathrm{OC} = \mathrm{OA}$) and hence $\mathrm{CD} = \mathrm{OA} \sin x$. Also $\tan x = \frac{\mathrm{AB}}{\mathrm{OA}}$ and

hence $\quad \mathrm{AB} = \mathrm{OA} . \tan x$. Thus
$\mathrm{OA} \sin x < \mathrm{OA} . x < \mathrm{OA} . \tan x$.
Since length $\mathrm{OA}$ is positive, we have
$\sin x < x < \tan x$.

Since $0 < x < \frac{\pi}{2}$, $\sin x$ is positive and thus by dividing throughout by $\sin x$, we have

$1 < \frac{x}{\sin x} < \frac{1}{\cos x}$. Taking reciprocals throughout, we have

$$\cos x < \frac{\sin x}{x} < 1$$

which complete the proof.

Theorem 5 The following are two important limits.


(i) $\lim_{x \to 0} \frac{\sin x}{x} = 1$. \qquad (ii) $\lim_{x \to 0} \frac{1 - \cos x}{x} = 0$.


Proof (i) The inequality in (*) says that the function $\frac{\sin x}{x}$ is sandwiched between the


function $\cos x$ and the constant function which takes value 1.

<!-- page 363 -->
Further, since $\lim_{x \to 0} \cos x = 1$, we see that the proof of (i) of the theorem is
complete by sandwich theorem.

To prove (ii), we recall the trigonometric identity $1 - \cos x = 2 \sin^2 \left( \frac{x}{2} \right)$.

Then

$$\lim_{x \to 0} \frac{1 - \cos x}{x} = \lim_{x \to 0} \frac{2 \sin^2 \left( \frac{x}{2} \right)}{x} = \lim_{x \to 0} \frac{\sin \left( \frac{x}{2} \right)}{\frac{x}{2}} \cdot \sin \left( \frac{x}{2} \right)$$

Observe that we have implicitly used the fact that $x \rightarrow 0$ is equivalent to $\frac{x}{2} \rightarrow 0$. This


may be justified by putting $y = \frac{x}{2}$.

Example 4 Evaluate:
(i) $\lim_{x \to 0} \frac{\sin 4x}{\sin 2x}$
(ii) $\lim_{x \to 0} \frac{\tan x}{x}$

Solution (i) $\lim_{x \to 0} \frac{\sin 4x}{\sin 2x} = \lim_{x \to 0} \left[ \frac{\sin 4x}{4x} \cdot \frac{2x}{\sin 2x} . 2 \right]$

$= 2 \cdot \lim_{x \to 0} \left[ \frac{\sin 4x}{4x} \right] \div \left[ \frac{\sin 2x}{2x} \right]$

$= 2 \cdot \lim_{4x \to 0} \left[ \frac{\sin 4x}{4x} \right] \div \lim_{2x \to 0} \left[ \frac{\sin 2x}{2x} \right]$

$= 2 \cdot 1.1 = 2$ (as $x \to 0$, $4x \to 0$ and $2x \to 0$)

<!-- page 364 -->
(ii) We have $\lim_{x \to 0} \frac{\tan x}{x} = \lim_{x \to 0} \frac{\sin x}{x \cos x} = \lim_{x \to 0} \frac{\sin x}{x} \cdot \lim_{x \to 0} \frac{1}{\cos x} = 1.1 = 1$

A general rule that needs to be kept in mind while evaluating limits is the following.

Say, given that the limit $\lim_{x \to a} \frac{f(x)}{g(x)}$ exists and we want to evaluate this. First we check

the value of $f(a)$ and $g(a)$. If both are 0, then we see if we can get the factor which
is causing the terms to vanish, i.e., see if we can write $f(x) = f_1 (x) f_2(x)$ so that
$f_1 (a) = 0$ and $f_2 (a) \neq 0$. Similarly, we write $g(x) = g_1 (x) g_2(x)$, where $g_1(a) = 0$ and
$g_2(a) \neq 0$. Cancel out the common factors from $f(x)$ and $g(x)$ (if possible) and write

$$\frac{f(x)}{g(x)} = \frac{p(x)}{q(x)} \text{ , where } q(x) \neq 0.$$

Then $\lim_{x \to a} \frac{f(x)}{g(x)} = \frac{p(a)}{q(a)}.$

EXERCISE 13.1

Evaluate the following limits in Exercises 1 to 22.

1. $\lim_{x \to 3} x + 3$
2. $\lim_{x \to \pi} \left( x - \frac{22}{7} \right)$
3. $\lim_{r \to 1} \pi r^2$

4. $\lim_{x \to 4} \frac{4x + 3}{x - 2}$
5. $\lim_{x \to -1} \frac{x^{10} + x^5 + 1}{x - 1}$
6. $\lim_{x \to 0} \frac{(x + 1)^5 - 1}{x}$

7. $\lim_{x \to 2} \frac{3x^2 - x - 10}{x^2 - 4}$
8. $\lim_{x \to 3} \frac{x^4 - 81}{2x^2 - 5x - 3}$
9. $\lim_{x \to 0} \frac{ax + b}{cx + 1}$

10. $\lim_{z \to 1} \frac{z^{\frac{1}{3}} - 1}{\frac{1}{z^6} - 1}$
11. $\lim_{x \to 1} \frac{ax^2 + bx + c}{cx^2 + bx + a}, a + b + c \neq 0$

12. $\lim_{x \to -2} \frac{\frac{1}{x} + \frac{1}{2}}{x + 2}$
13. $\lim_{x \to 0} \frac{\sin ax}{bx}$
14. $\lim_{x \to 0} \frac{\sin ax}{\sin bx}, a, b \neq 0$

<!-- page 365 -->
15. $\lim_{x \to \pi} \frac{\sin(\pi - x)}{\pi(\pi - x)}$

16. $\lim_{x \to 0} \frac{\cos x}{\pi - x}$

17. $\lim_{x \to 0} \frac{\cos 2x - 1}{\cos x - 1}$

18. $\lim_{x \to 0} \frac{ax + x \cos x}{b \sin x}$

19. $\lim_{x \to 0} x \sec x$

20. $\lim_{x \to 0} \frac{\sin ax + bx}{ax + \sin bx} a, b, a + b \neq 0,$

21. $\lim_{x \to 0} (\csc x - \cot x)$

$$\lim_{x \to \frac{\pi}{2}} \frac{\tan 2x}{x - \frac{\pi}{2}}$$
22.

23. Find $\lim_{x \to 0} f(x)$ and $\lim_{x \to 1} f(x)$, where $f(x) = \begin{cases} 2x + 3, & x \le 0 \\ 3(x + 1), & x > 0 \end{cases}$

24. Find $\lim_{x \to 1} f(x)$, where $f(x) = \begin{cases} x^2 - 1, & x \le 1 \\ -x^2 - 1, & x > 1 \end{cases}$

25. Evaluate $\lim_{x \to 0} f(x)$, where $f(x) = \begin{cases} \frac{|x|}{x}, & x \neq 0 \\ 0, & x = 0 \end{cases}$

26. Find $\lim_{x \to 0} f(x)$, where $f(x) = \begin{cases} \frac{x}{|x|}, & x \neq 0 \\ 0, & x = 0 \end{cases}$

27. Find $\lim_{x \to 5} f(x)$, where $f(x)=|x|-5$

28. Suppose $f(x)=\begin{cases}a+bx, & x<1\\4, & x=1\\b-ax, & x>1\end{cases}$

and if $\lim_{x \to 1} f(x) = f(1)$ what are possible values of $a$ and $b$?

<!-- page 366 -->
29. Let $a_1, a_2, \dots, a_n$ be fixed real numbers and define a function

$$f(x) = (x - a_1)(x - a_2) \dots (x - a_n).$$

What is $\lim_{x \to a_1} f(x)$ ? For some $a \neq a_1, a_2, ..., a_n$, compute $\lim_{x \to a} f(x)$.

30. If $f(x) = \begin{cases} |x| + 1, & x < 0 \\ 0, & x = 0 \\ |x| - 1, & x > 0 \end{cases}$.

For what value (s) of $a$ does $\lim_{x \to a} f(x)$ exists?

31. If the function $f(x)$ satisfies $\lim_{x \to 1} \frac{f(x)-2}{x^2-1} = \pi$, evaluate $\lim_{x \to 1} f(x)$.

32. If $f(x) = \begin{cases} mx^2 + n, & x < 0 \\ nx + m, & 0 \le x \le 1 \\ nx^3 + m, & x > 1 \end{cases}$. For what integers $m$ and $n$ does both $\lim_{x \to 0} f(x)$


and $\lim_{x \to 1} f(x)$ exist?

13.5 Derivatives

We have seen in the Section 13.2, that by knowing the position of a body at various
time intervals it is possible to find the rate at which the position of the body is changing.
It is of very general interest to know a certain parameter at various instants of time and
try to finding the rate at which it is changing. There are several real life situations
where such a process needs to be carried out. For instance, people maintaining a
reservoir need to know when will a reservoir overflow knowing the depth of the water
at several instances of time, Rocket Scientists need to compute the precise velocity
with which the satellite needs to be shot out from the rocket knowing the height of the
rocket at various times. Financial institutions need to predict the changes in the value of
a particular stock knowing its present value. In these, and many such cases it is desirable
to know how a particular parameter is changing with respect to some other parameter.
The heart of the matter is derivative of a function at a given point in its domain
of definition.

<!-- page 367 -->
Definition 1 Suppose $f$ is a real valued function and $a$ is a point in its domain of
definition. The derivative of $f$ at $a$ is defined by

$$\lim_{h \to 0} \frac{f(a+h) - f(a)}{h}$$

provided this limit exists. Derivative of $f(x)$ at $a$ is denoted by $f'(a)$.
Observe that $f'(a)$ quantifies the change in $f(x)$ at $a$ with respect to $x$.

Example 5 Find the derivative at $x = 2$ of the function $f(x) = 3x$.

Solution We have

$$f'(2) = \lim_{h \to 0} \frac{f(2+h) - f(2)}{h} = \lim_{h \to 0} \frac{3(2+h) - 3(2)}{h}$$

$$= \lim_{h \to 0} \frac{6 + 3h - 6}{h} = \lim_{h \to 0} \frac{3h}{h} = \lim_{h \to 0} 3 = 3.$$

The derivative of the function $3x$ at $x = 2$ is 3.

Example 6 Find the derivative of the function $f(x) = 2x^2 + 3x - 5$ at $x = -1$. Also prove
that $f'(0) + 3f'(-1) = 0$.

Solution We first find the derivatives of $f(x)$ at $x = -1$ and at $x = 0$. We have

$$f'(-1) = \lim_{h \to 0} \frac{f(-1+h) - f(-1)}{h}$$

$$= \lim_{h \to 0} \frac{\left[ 2(-1+h)^2 + 3(-1+h) - 5 \right] - \left[ 2(-1)^2 + 3(-1) - 5 \right]}{h}$$

$$= \lim_{h \to 0} \frac{2h^2 - h}{h} = \lim_{h \to 0} (2h - 1) = 2(0) - 1 = -1$$

and

$$f'(0) = \lim_{h \to 0} \frac{f(0+h) - f(0)}{h}$$

$$= \lim_{h \to 0} \frac{\left[ 2(0+h)^2 + 3(0+h) - 5 \right] - \left[ 2(0)^2 + 3(0) - 5 \right]}{h}$$

<!-- page 368 -->
$$= \lim_{h \to 0} \frac{2h^2 + 3h}{h} = \lim_{h \to 0} (2h + 3) = 2(0) + 3 = 3$$

Clearly $f'(0)+3f'(-1)=0$

$\underline{\text{Remark}}$ At this stage note that evaluating derivative at a point involves effective use
of various rules, limits are subjected to. The following illustrates this.

Example 7 Find the derivative of $\sin x$ at $x = 0$.


Solution Let $f(x) = \sin x$. Then


$$f'(0) = \lim_{h \to 0} \frac{f(0+h) - f(0)}{h}$$


$$= \lim_{h \to 0} \frac{\sin(0+h) - \sin(0)}{h} = \lim_{h \to 0} \frac{\sin h}{h} = 1$$

Example 8 Find the derivative of $f(x) = 3$ at $x = 0$ and at $x = 3$.

Solution Since the derivative measures the change in function, intuitively it is clear
that the derivative of the constant function must be zero at every point. This is indeed,
supported by the following computation.

$$f'(0) = \lim_{h \to 0} \frac{f(0+h) - f(0)}{h} = \lim_{h \to 0} \frac{3-3}{h} = \lim_{h \to 0} \frac{0}{h} = 0.$$

Similarly $f'(3) = \lim_{h \to 0} \frac{f(3+h) - f(3)}{h} = \lim_{h \to 0} \frac{3-3}{h} = 0.$

We now present a geometric interpretation of derivative of a
function at a point. Let $y = f(x)$ be
a function and let $\mathrm{P} = (a, f(a))$ and
$\mathrm{Q} = (a + h, f(a + h)$ be two points
close to each other on the graph
of this function. The Fig 13.11 is
now self explanatory.

Fig 13.11

<!-- page 369 -->
$$\text{We know that } f'(a) = \lim_{h \to 0} \frac{f(a+h) - f(a)}{h}$$

From the triangle PQR, it is clear that the ratio whose limit we are taking is
precisely equal to $\tan(\text{QPR})$ which is the slope of the chord PQ. In the limiting process,
as $h$ tends to 0, the point Q tends to P and we have

$$\lim_{h \to 0} \frac{f(a+h) - f(a)}{h} = \lim_{\mathrm{Q} \to \mathrm{P}} \frac{\mathrm{QR}}{\mathrm{PR}}$$

This is equivalent to the fact that the chord PQ tends to the tangent at P of the
curve $y = f(x)$. Thus the limit turns out to be equal to the slope of the tangent. Hence

$$f'(a) = \tan \psi.$$

For a given function $f$ we can find the derivative at every point. If the derivative
exists at every point, it defines a new function called the derivative of $f$. Formally, we
define derivative of a function as follows.

Definition 2 Suppose $f$ is a real valued function, the function defined by

$$\lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$$

wherever the limit exists is defined to be the derivative of $f$ at $x$ and is denoted by
$f'(x)$. This definition of derivative is also called the first principle of derivative.

Thus $f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$

Clearly the domain of definition of $f'(x)$ is wherever the above limit exists. There
are different notations for derivative of a function. Sometimes $f'(x)$ is denoted by

$\frac{d}{dx}(f(x))$ or if $y=f(x)$, it is denoted by $\frac{dy}{dx}$. This is referred to as derivative of $f(x)$
or $y$ with respect to $x$. It is also denoted by D ($f(x)$ ). Further, derivative of $f$ at $x=a$

is also denoted by $\left.\frac{d}{dx} f(x)\right|_a$ or $\left.\frac{df}{dx}\right|_a$ or even $\left.\left(\frac{df}{dx}\right)\right|_{x=a}$.

Example 9 Find the derivative of $f(x) = 10x$.


Solution Since $f' ( x) = \lim_{h \to 0} \frac{f (x + h) - f (x)}{h}$

<!-- page 370 -->
$$= \lim_{h \to 0} \frac{10(x+h) - 10(x)}{h}$$

$$= \lim_{h \to 0} \frac{10h}{h} = \lim_{h \to 0} (10) = 10.$$

Example 10 Find the derivative of $f(x) = x^2$.

Solution We have, $f^{\prime}(x)=\lim _{h \rightarrow 0} \frac{f(x+h)-f(x)}{h}$


$$=\lim _{h \rightarrow 0} \frac{(x+h)^{2}-(x)^{2}}{h}=\lim _{h \rightarrow 0}(h+2 x)=2 x$$

Example 11 Find the derivative of the constant function $f(x) = a$ for a fixed real
number $a$.

Solution We have, $f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$

$$= \lim_{h \to 0} \frac{a - a}{h} = \lim_{h \to 0} \frac{0}{h} = 0 \text{ as } h \neq 0$$

Example 12 Find the derivative of $f(x) = \frac{1}{x}$


Solution We have $f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$


$$= \lim_{h \to 0} \frac{\frac{1}{(x+h)} - \frac{1}{x}}{h}$$


$$= \lim_{h \to 0} \frac{1}{h} \left[ \frac{x - (x+h)}{x(x+h)} \right]$$


$$= \lim_{h \to 0} \frac{1}{h} \left[ \frac{-h}{x(x+h)} \right] = \lim_{h \to 0} \frac{-1}{x(x+h)} = -\frac{1}{x^2}$$

<!-- page 371 -->
13.5.1 Algebra of derivative of functions Since the very definition of derivatives
involve limits in a rather direct fashion, we expect the rules for derivatives to follow
closely that of limits. We collect these in the following theorem.

Theorem 5 Let $f$ and $g$ be two functions such that their derivatives are defined in a
common domain. Then

(i) Derivative of sum of two functions is sum of the derivatives of the
functions.

$$\frac{d}{dx}[f(x)+g(x)]=\frac{d}{dx}f(x)+\frac{d}{dx}g(x).$$

(ii) Derivative of difference of two functions is difference of the derivatives of
the functions.

$$\frac{d}{dx}[f(x)-g(x)]=\frac{d}{dx}f(x)-\frac{d}{dx}g(x).$$

(iii) Derivative of product of two functions is given by the following $product$
$rule.$

$$\frac{d}{dx}[f(x).g(x)]=\frac{d}{dx}f(x).g(x)+f(x).\frac{d}{dx}g(x)$$

(iv) Derivative of quotient of two functions is given by the following $quotient$
$rule$ (whenever the denominator is non-zero).

$$\frac{d}{dx}\left(\frac{f(x)}{g(x)}\right)=\frac{\frac{d}{dx}f(x).g(x)-f(x)\frac{d}{dx}g(x)}{(g(x))^{2}}$$

The proofs of these follow essentially from the analogous theorem for limits. We
will not prove these here. As in the case of limits this theorem tells us how to compute
derivatives of special types of functions. The last two statements in the theorem may
be restated in the following fashion which aids in recalling them easily:

Let $u = f(x)$ and $v = g(x)$. Then

$$(uv)' = u'v + uv'$$

This is referred to a Leibnitz rule for differentiating product of functions or the
product rule. Similarly, the quotient rule is

<!-- page 372 -->
$$\left( \frac{u}{v} \right)' = \frac{u'v - uv'}{v^2}$$

Now, let us tackle derivatives of some standard functions.

It is easy to see that the derivative of the function $f(x) = x$ is the constant

function 1. This is because $f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}{h}=\lim_{h\to0}\frac{x+h-x}{h}$

$$= \lim_{h \to 0} 1 = 1 .$$

We use this and the above theorem to compute the derivative of
$$f(x) = 10x = x + .... + x \text{ (ten terms). By } (i) \text{ of the above theorem}$$

$$\frac{df(x)}{dx} = \frac{d}{dx} (x + ... + x) \text{ (ten terms)}$$

$$= \frac{d}{dx} x + ... + \frac{d}{dx} x \text{ (ten terms)}$$

$$= 1 + ... + 1 \text{ (ten terms)} = 10.$$

We note that this limit may be evaluated using product rule too. Write
$f(x) = 10x = uv$, where $u$ is the constant function taking value 10 everywhere and
$v(x) = x$. Here, $f(x) = 10x = uv$ we know that the derivative of $u$ equals 0. Also
derivative of $v(x) = x$ equals 1. Thus by the product rule we have

$$f'(x) = (10x)' = (uv)' = u'v + uv' = 0.x + 10.1 = 10$$

On similar lines the derivative of $f(x) = x^2$ may be evaluated. We have
$f(x) = x^2 = x \ .x$ and hence

$$\frac{df}{dx} = \frac{d}{dx}(x.x) = \frac{d}{dx}(x).x + x.\frac{d}{dx}(x)$$
$$= 1.x + x.1 = 2x .$$

More generally, we have the following theorem.

Theorem 6 Derivative of $f(x) = x^n$ is $nx^{n-1}$ for any positive integer $n$.

Proof By definition of the derivative function, we have

$$f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h} = \lim_{h \to 0} \frac{(x+h)^n - x^n}{h} .$$

<!-- page 373 -->
Binomial theorem tells that $(x+h)^n = \left( ^n\text{C}_0 \right)x^n + \left( ^n\text{C}_1 \right)x^{n-1}h + ... + \left( ^n\text{C}_n \right)h^n$ and
hence $(x+h)^n - x^n = h(nx^{n-1} + ... + h^{n-1})$. Thus

$$\frac{df(x)}{dx} = \lim_{h \to 0} \frac{(x+h)^n - x^n}{h}$$

$$= \lim_{h \to 0} \frac{h(nx^{n-1} + ... + h^{n-1})}{h}$$

$$= \lim_{h \to 0} (nx^{n-1} + ... + h^{n-1}) = nx^{n-1}.$$

Alternatively, we may also prove this by induction on $n$ and the product rule as
follows. The result is true for $n = 1$, which has been proved earlier. We have

$\frac{d}{dx}\left(x^{n}\right)=\frac{d}{dx}\left(x.x^{n-1}\right)$

$=\frac{d}{dx}(x).\left(x^{n-1}\right)+x.\frac{d}{dx}\left(x^{n-1}\right)$ (by product rule)

$=1.x^{n-1}+x.\left((n-1)x^{n-2}\right)$ (by induction hypothesis)

$=x^{n-1}+(n-1)x^{n-1}=nx^{n-1}.$

Remark The above theorem is true for all powers of $x$, i.e., $n$ can be any real number
(but we will not prove it here).

13.5.2 Derivative of polynomials and trigonometric functions We start with the
following theorem which tells us the derivative of a polynomial function.

Theorem 7 Let $f(x) = a_n x^n + a_{n-1} x^{n-1} + .... + a_1 x + a_0$ be a polynomial function, where
$a_i s$ are all real numbers and $a_n \neq 0$. Then, the derivative function is given by

$$\frac{df(x)}{dx} = n a_n x^{n-1} + (n-1) a_{n-1} x^{x-2} + ... + 2 a_2 x + a_1 .$$

Proof of this theorem is just putting together part (i) of Theorem 5 and Theorem 6.

Example 13 Compute the derivative of $6x^{100} - x^{55} + x$.

Solution A direct application of the above theorem tells that the derivative of the

above function is $600x^{99} - 55x^{54} + 1$.

<!-- page 374 -->
Example 14 Find the derivative of $f(x) = 1 + x + x^2 + x^3 +... + x^{50}$ at $x = 1$.

Solution A direct application of the above Theorem 6 tells that the derivative of the
above function is $1 + 2x + 3x^2 + \dots + 50x^{49}$. At $x = 1$ the value of this function equals

$$1 + 2(1) + 3(1)^2 + \dots + 50(1)^{49} = 1 + 2 + 3 + \dots + 50 = \frac{(50)(51)}{2} = 1275.$$

Example 15 Find the derivative of $f(x) = \frac{x+1}{x}$

Solution Clearly this function is defined everywhere except at $x = 0$. We use the
quotient rule with $u = x + 1$ and $v = x$. Hence $u' = 1$ and $v' = 1$. Therefore

$$\frac{df(x)}{dx} = \frac{d}{dx} \left( \frac{x+1}{x} \right) = \frac{d}{dx} \left( \frac{u}{v} \right) = \frac{u'v - uv'}{v^2} = \frac{1(x) - (x+1)1}{x^2} = -\frac{1}{x^2}$$

Example 16 Compute the derivative of $\sin x$.

Solution Let $f(x) = \sin x$. Then

$$\frac{df(x)}{dx} = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h} = \lim_{h \to 0} \frac{\sin(x+h) - \sin(x)}{h}$$

$$= \lim_{h \to 0} \frac{2 \cos \left( \frac{2x+h}{2} \right) \sin \left( \frac{h}{2} \right)}{h} \text{ (using formula for } \sin A - \sin B)$$

$$= \lim_{h \to 0} \cos \left( x + \frac{h}{2} \right) \lim_{h \to 0} \frac{\sin \frac{h}{2}}{\frac{h}{2}} = \cos x.1 = \cos x.$$

Example 17 Compute the derivative of $\tan x$.

Solution Let $f(x) = \tan x$. Then

$$\frac{df(x)}{dx} = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h} = \lim_{h \to 0} \frac{\tan(x+h) - \tan(x)}{h}$$

$$= \lim_{h \to 0} \frac{1}{h} \left[ \frac{\sin(x+h)}{\cos(x+h)} - \frac{\sin x}{\cos x} \right]$$

<!-- page 375 -->
$$= \lim_{h \to 0} \left[ \frac{\sin(x+h)\cos x - \cos(x+h)\sin x}{h\cos(x+h)\cos x} \right]$$

$$= \lim_{h \to 0} \frac{\sin(x+h-x)}{h\cos(x+h)\cos x} \text{ (using formula for } \sin (A + B))$$

$$= \lim_{h \to 0} \frac{\sin h}{h} . \lim_{h \to 0} \frac{1}{\cos(x+h)\cos x}$$

$$= 1 . \frac{1}{\cos^2 x} = \sec^2 x .$$

Example 18 Compute the derivative of $f(x) = \sin^2 x$.

Solution We use the Leibnitz product rule to evaluate this.

$$\frac{df(x)}{dx} = \frac{d}{dx} (\sin x \sin x)$$

$$= (\sin x)' \sin x + \sin x (\sin x)'$$

$$= (\cos x) \sin x + \sin x (\cos x)$$

$$= 2 \sin x \cos x = \sin 2x \text{ .}$$

EXERCISE 13.2

1. Find the derivative of $x^2 - 2$ at $x = 10$.
2. Find the derivative of $x$ at $x = 1$.
3. Find the derivative of $99x$ at $x = 100$.
4. Find the derivative of the following functions from first principle.

(i) $x^3 - 27$                                     (ii) $(x - 1)(x - 2)$

(iii) $\frac{1}{x^2}$                                     (iv) $\frac{x + 1}{x - 1}$

5. For the function

$$f(x) = \frac{x^{100}}{100} + \frac{x^{99}}{99} + \dots + \frac{x^2}{2} + x + 1.$$

<!-- page 376 -->
Prove that $f'(1)=100f'(0)$.

6. Find the derivative of $x^n + ax^{n-1} + a^2x^{n-2} + \dots + a^{n-1}x + a^n$ for some fixed real
number $a$.

7. For some constants $a$ and $b$, find the derivative of

(i) $(x-a)(x-b)$ (ii) $(ax^2+b)^2$ (iii) $\frac{x-a}{x-b}$

8. Find the derivative of $\frac{x^n - a^n}{x - a}$ for some constant $a$.

9. Find the derivative of

(i) $2x - \frac{3}{4}$                                     (ii) $(5x^3 + 3x - 1)(x - 1)$

(iii) $x^{-3}(5 + 3x)$                                (iv) $x^5(3 - 6x^{-9})$

(v) $x^{-4}(3 - 4x^{-5})$                                (vi) $\frac{2}{x + 1} - \frac{x^2}{3x - 1}$

10. Find the derivative of $\cos x$ from first principle.

11. Find the derivative of the following functions:

(i) $\sin x \cos x$
(ii) $\sec x$
(iii) $5 \sec x + 4 \cos x$
(iv) $\operatorname{cosec} x$
(v) $3 \cot x + 5 \operatorname{cosec} x$
(vi) $5 \sin x - 6 \cos x + 7$
(vii) $2 \tan x - 7 \sec x$

Miscellaneous Examples

Example 19 Find the derivative of $f$ from the first principle, where $f$ is given by


(i) $f(x) = \frac{2x + 3}{x - 2}$ (ii) $f(x) = x + \frac{1}{x}$


Solution (i) Note that function is not defined at $x = 2$. But, we have


$$f'(x) = \lim_{h \to 0} \frac{f(x + h) - f(x)}{h} = \lim_{h \to 0} \frac{\frac{2(x + h) + 3}{x + h - 2} - \frac{2x + 3}{x - 2}}{h}$$

<!-- page 377 -->
$$= \lim_{h \to 0} \frac{(2x + 2h + 3)(x - 2) - (2x + 3)(x + h - 2)}{h(x - 2)(x + h - 2)}$$

$$= \lim_{h \to 0} \frac{(2x+3)(x-2)+2h(x-2)-(2x+3)(x-2)-h(2x+3)}{h(x-2)(x+h-2)}$$

$$= \lim_{h \to 0} \frac{-7}{(x-2)(x+h-2)} = -\frac{7}{(x-2)^2}$$

Again, note that the function $f'$ is also not defined at $x = 2$.

(ii) The function is not defined at $x = 0$. But, we have

$$f^{\prime}(x)=\lim _{h \rightarrow 0} \frac{f(x+h)-f(x)}{h}=\lim _{h \rightarrow 0}\left(\frac{x+h+\frac{1}{x+h}\right)-\left(x+\frac{1}{x}\right)\right)$$

$$=\lim _{h \rightarrow 0} \frac{1}{h}\left[h+\frac{1}{x+h}-\frac{1}{x}\right]$$

$$=\lim _{h \rightarrow 0} \frac{1}{h}\left[h+\frac{x-x-h}{x(x+h)}\right]=\lim _{h \rightarrow 0} \frac{1}{h}\left[h\left(1-\frac{1}{x(x+h)}\right)\right]$$

$$=\lim _{h \rightarrow 0}\left[1-\frac{1}{x(x+h)}\right]=1-\frac{1}{x^{2}}$$

Again, note that the function $f'$ is not defined at $x = 0$.

Example 20 Find the derivative of $f(x)$ from the first principle, where $f(x)$ is
(i) $\sin x + \cos x$                                     (ii) $x \sin x$

Solution (i) we have $f'(x) = \frac{f(x+h) - f(x)}{h}$

$$= \lim_{h \to 0} \frac{\sin(x+h) + \cos(x+h) - \sin x - \cos x}{h}$$

$$= \lim_{h \to 0} \frac{\sin x \cos h + \cos x \sin h + \cos x \cos h - \sin x \sin h - \sin x - \cos x}{h}$$

<!-- page 378 -->
$$= \lim_{h \to 0} \frac{\sin h(\cos x - \sin x) + \sin x(\cos h - 1) + \cos x(\cos h - 1)}{h}$$

$$= \lim_{h \to 0} \frac{\sin h}{h} (\cos x - \sin x) + \lim_{h \to 0} \sin x \frac{(\cos h - 1)}{h} + \lim_{h \to 0} \cos x \frac{(\cos h - 1)}{h}$$

$$= \cos x - \sin x$$

(ii) $f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h} = \lim_{h \to 0} \frac{(x+h)\sin(x+h) - x\sin x}{h}$

$= \lim_{h \to 0} \frac{(x+h)(\sin x \cos h + \sin h \cos x) - x\sin x}{h}$

$= \lim_{h \to 0} \frac{x\sin x(\cos h - 1) + x\cos x\sin h + h(\sin x\cos h + \sin h \cos x)}{h}$

$= \lim_{h \to 0} \frac{x\sin x(\cos h - 1)}{h} + \lim_{h \to 0} x\cos x\frac{\sin h}{h} + \lim_{h \to 0} (\sin x\cos h + \sin h \cos x)$

$= x\cos x + \sin x$

Example 21 Compute derivative of
(i) $f(x) = \sin 2x$ (ii) $g(x) = \cot x$

Solution (i) Recall the trigonometric formula $\sin 2x = 2 \sin x \cos x$. Thus

$$\frac{df(x)}{dx} = \frac{d}{dx}(2 \sin x \cos x) = 2 \frac{d}{dx}(\sin x \cos x)$$

$$= 2 \left[ (\sin x)' \cos x + \sin x (\cos x)' \right]$$

$$= 2 \left[ (\cos x) \cos x + \sin x (-\sin x) \right]$$

$$= 2 \left( \cos^2 x - \sin^2 x \right)$$

(ii) By definition, $g(x) = \cot x = \frac{\cos x}{\sin x}$. We use the quotient rule on this function

$$\text{wherever it is defined. } \frac{dg}{dx} = \frac{d}{dx} (\cot x) = \frac{d}{dx} \left( \frac{\cos x}{\sin x} \right)$$

<!-- page 379 -->
$$= \frac{(\cos x)'(\sin x)-(\cos x)(\sin x)'}{(\sin x)^2}$$

$$= \frac{(-\sin x)(\sin x)-(\cos x)(\cos x)}{(\sin x)^2}$$

$$= -\frac{\sin^2 x + \cos^2 x}{\sin^2 x} = -\csc^2 x$$

Alternatively, this may be computed by noting that $\cot x = \frac{1}{\tan x}$. Here, we use the fact
that the derivative of $\tan x$ is $sec^2 x$ which we saw in Example 17 and also that the
derivative of the constant function is 0.

$$\frac{dg}{dx} = \frac{d}{dx}(\cot x) = \frac{d}{dx}\left(\frac{1}{\tan x}\right)$$

$$= \frac{(1)'(\tan x) - (1)(\tan x)'}{(\tan x)^2}$$

$$= \frac{(0)(\tan x) - (\sec x)^2}{(\tan x)^2}$$

$$= \frac{-\sec^2 x}{\tan^2 x} = -\csc^2 x$$

Example 22 Find the derivative of


$$\text{(i)} \quad \frac{x^5 - \cos x}{\sin x} \qquad \qquad \qquad \text{(ii)} \quad \frac{x + \cos x}{\tan x}$$


Solution (i) Let $h(x) = \frac{x^5 - \cos x}{\sin x}$ . We use the quotient rule on this function wherever
it is defined.


$$h'(x) = \frac{(x^5 - \cos x)' \sin x - (x^5 - \cos x)(\sin x)'}{(\sin x)^2}$$

<!-- page 380 -->
$$= \frac{(5x^4 + \sin x) \sin x - (x^5 - \cos x) \cos x}{\sin^2 x}$$

$$= \frac{-x^5 \cos x + 5x^4 \sin x + 1}{(\sin x)^2}$$

(ii) We use quotient rule on the function $\frac{x + \cos x}{\tan x}$ wherever it is defined.

$$h'(x) = \frac{(x + \cos x)' \tan x - (x + \cos x) (\tan x)'}{(\tan x)^2}$$

$$= \frac{(1 - \sin x) \tan x - (x + \cos x) \sec^2 x}{(\tan x)^2}$$

Miscellaneous Exercise on Chapter 13

1. Find the derivative of the following functions from first principle:

(i) $-x$ (ii) $(-x)^{-1}$ (iii) $\sin (x+1)$ (iv) $\cos \left(x-\frac{\pi}{8}\right)$

Find the derivative of the following functions (it is to be understood that $a, b, c, d,$
$p, q, r$ and $s$ are fixed non-zero constants and $m$ and $n$ are integers):

2. $(x + a)$ 3. $(px + q) \left( \frac{r}{x} + s \right)$ 4. $(ax + b)(cx + d)^2$

2. $(x+a)$
3. $(px+q)\left(\frac{r}{x}+s\right)$
4. $(ax+b)(cx+d)^2$

5. $\frac{ax+b}{cx+d}$
6. $\frac{1+\frac{1}{x}}{1-\frac{1}{x}}$
7. $\frac{1}{ax^2+bx+c}$

8. $\frac{ax+b}{px^2+qx+r}$
9. $\frac{px^2+qx+r}{ax+b}$
10. $\frac{a}{x^4}-\frac{b}{x^2}+\cos x$

11. $4\sqrt{x}-2$
12. $(ax+b)^n$
13. $(ax+b)^n(cx+d)^m$

14. $\sin(x+a)$
15. $\text{cosec } x \cot x$
16. $\frac{\cos x}{1+\sin x}$

<!-- page 381 -->
17. $\frac{\sin x + \cos x}{\sin x - \cos x}$

18. $\frac{\sec x - 1}{\sec x + 1}$

19. $\sin^n x$

20. $\frac{a + b \sin x}{c + d \cos x}$

21. $\frac{\sin(x+a)}{\cos x}$

22. $x^4(5\sin x - 3\cos x)$

23. $(x^2 + 1)\cos x$

24. $(ax^2 + \sin x)(p + q \cos x)$

25. $(x + \cos x)(x - \tan x)$

26. $\frac{4x + 5\sin x}{3x + 7\cos x}$

27. $\frac{x^2 \cos \left( \frac{\pi}{4} \right)}{\sin x}$

28. $\frac{x}{1 + \tan x}$

29. $(x + \sec x)(x - \tan x)$

$$30. \quad \frac{x}{\sin^n x}$$

Summary

The expected value of the function as dictated by the points to the left of a
point defines the left hand limit of the function at that point. Similarly the right
hand limit.
Limit of a function at a point is the common value of the left and right hand
limits, if they coincide.

For a function $f$ and a real number $a$, $\lim_{x \to a} f(x)$ and $f(a)$ may not be same (In
fact, one may be defined and not the other one).
For functions $f$ and $g$ the following holds:

$$\lim_{x \to a} [f(x) \pm g(x)] = \lim_{x \to a} f(x) \pm \lim_{x \to a} g(x)$$

$$\lim_{x \to a} [f(x) \cdot g(x)] = \lim_{x \to a} f(x) \cdot \lim_{x \to a} g(x)$$

$$\lim_{x \to a} \left[ \frac{f(x)}{g(x)} \right] = \frac{\lim_{x \to a} f(x)}{\lim_{x \to a} g(x)}$$

Following are some of the standard limits

$$\lim_{x \to a} \frac{x^n - a^n}{x - a} = n a^{n-1}$$

<!-- page 382 -->
$$\lim_{x \to 0} \frac{\sin x}{x} = 1$$

$$\lim_{x \to 0} \frac{1 - \cos x}{x} = 0$$

The derivative of a function $f$ at $a$ is defined by

$$f'(a) = \lim_{h \to 0} \frac{f(a+h) - f(a)}{h}$$

$\diamond$ Derivative of a function $f$ at any point $x$ is defined by

$$f'(x) = \frac{df(x)}{dx} = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$$

$\diamond$ For functions $u$ and $v$ the following holds:

$$(u \pm v)' = u' \pm v'$$

$$(uv)'=u'v+uv'$$

$$\left( \frac{u}{v} \right)' = \frac{u'v - uv'}{v^2} \text{ provided all are defined.}$$

$\diamond$ Following are some of the standard derivatives.

$$\frac{d}{dx}(x^n) = nx^{n-1}$$

$$\frac{d}{dx}(\sin x) = \cos x$$

$$\frac{d}{dx}(\cos x) = -\sin x$$

Historical Note

In the history of mathematics two names are prominent to share the credit for
inventing calculus, Issac Newton (1642 – 1727) and G.W. Leibnitz (1646 – 1717).
Both of them independently invented calculus around the seventeenth century.
After the advent of calculus many mathematicians contributed for further
development of calculus. The rigorous concept is mainly attributed to the great

<!-- page 383 -->
mathematicians, A.L. Cauchy, J.L.Lagrange and Karl Weierstrass. Cauchy gave
the foundation of calculus as we have now generally accepted in our textbooks.
Cauchy used D’ Alembert’s limit concept to define the derivative of a function.
Starting with definition of a limit, Cauchy gave examples such as the limit of

$$\frac{\sin \alpha}{\alpha} \text{ for } \alpha = 0. \text{ He wrote } \frac{\Delta y}{\Delta x} = \frac{f(x+i) - f(x)}{i}, \text{ and called the limit for}$$

$i \rightarrow 0$, the “function derive’e, $y'$ for $f'(x)$”.

Before 1900, it was thought that calculus is quite difficult to teach. So calculus
became beyond the reach of youngsters. But just in 1900, John Perry and others
in England started propagating the view that essential ideas and methods of calculus
were simple and could be taught even in schools. F.L. Griffin, pioneered the
teaching of calculus to first year students. This was regarded as one of the most
daring act in those days.

Today not only the mathematics but many other subjects such as Physics,
Chemistry, Economics and Biological Sciences are enjoying the fruits of calculus.

<!-- page 384 -->
Chapter

MATHEMATICAL REASONING

❖ There are few things which we know which are not capable of
mathematical reasoning and when these can not, it is a sign that our
knowledge of them is very small and confused and where a mathematical
reasoning can be had, it is as great a folly to make use of another,
as to grope for a thing in the dark when you have a candle stick
standing by you. – ARTHENBOT ❖

14.1 Introduction

In this Chapter, we shall discuss about some basic ideas of
Mathematical Reasoning. All of us know that human beings
evolved from the lower species over many millennia. The
main asset that made humans “$superior$” to other species
was the ability to reason. How well this ability can be used
depends on each person’s power of reasoning. How to
develop this power? Here, we shall discuss the process of
reasoning especially in the context of mathematics.

George Boole
(1815 - 1864)

In mathematical language, there are two kinds of
reasoning – inductive and deductive. We have already
discussed the inductive reasoning in the context of
mathematical induction. In this Chapter, we shall discuss
some fundamentals of deductive reasoning.

14.2 Statements

The basic unit involved in mathematical reasoning is a mathematical statement.
Let us start with two sentences:

In 2003, the president of India was a woman.
An elephant weighs more than a human being.

<!-- page 385 -->
When we read these sentences, we immediately decide that the first sentence is
false and the second is correct. There is no confusion regarding these. In mathematics
such sentences are called \textit{statements}.

On the other hand, consider the sentence:

Women are more intelligent than men.

Some people may think it is true while others may disagree. Regarding this sentence
we cannot say whether it is always true or false . That means this sentence is ambiguous.
Such a sentence is not acceptable as a statement in mathematics.

A sentence is called a mathematically acceptable statement if it is either
true or false but not both. Whenever we mention a statement here, it is a
“mathematically acceptable” statement.

While studying mathematics, we come across many such sentences. Some examples
are:

Two plus two equals four.

The sum of two positive numbers is positive.

All prime numbers are odd numbers.

Of these sentences, the first two are $true$ and the third one is $false$. There is no
ambiguity regarding these sentences. Therefore, they are statements.

Can you think of an example of a sentence which is vague or ambiguous? Consider
the sentence:

The sum of $x$ and $y$ is greater than $0$

Here, we are not in a position to determine whether it is true or false, unless we
know what $x$ and $y$ are. For example, it is false where $x = 1$, $y = -3$ and true when
$x = 1$ and $y = 0$. Therefore, this sentence is not a statement. But the sentence:

For any natural numbers $x$ and $y$, the sum of $x$ and $y$ is greater than $0$
is a statement.

Now, consider the following sentences :

How beautiful!

Open the door.

Where are you going?

Are they statements? No, because the first one is an exclamation, the second
an order and the third a question. None of these is considered as a statement in
mathematical language. Sentences involving variable time such as “today”, “tomorrow”
or “yesterday” are not statements. This is because it is not known what time is referred
here. For example, the sentence

Tomorrow is Friday

<!-- page 386 -->
is not a statement. The sentence is correct (true) on a Thursday but not on other
days. The same argument holds for sentences with pronouns unless a particular
person is referred to and for variable places such as “here”, “there” etc., For
example, the sentences

She is a mathematics graduate.
Kashmir is far from here.

are not statements.

Here is another sentence

There are 40 days in a month.

Would you call this a statement? Note that the period mentioned in the sentence
above is a “variable time” that is any of 12 months. But we know that the sentence is
always false (irrespective of the month) since the maximum number of days in a month
can never exceed 31. Therefore, this sentence is a statement. So, what makes a sentence
a statement is the fact that the sentence is either true or false but not both.

While dealing with statements, we usually denote them by small letters $p, q, r,...$
For example, we denote the statement “*Fire is always hot*” by $p$. This is also written
as

$p$: Fire is always hot.

Example 1 Check whether the following sentences are statements. Give reasons for
your answer.

(i) 8 is less than 6.                                     (ii) Every set is a finite set.
(iii) The sun is a star.                                     (iv) Mathematics is fun.
(v) There is no rain without clouds.                  (vi) How far is Chennai from here?

Solution (i) This sentence is false because 8 is greater than 6. Hence it is a statement.

(ii) This sentence is also false since there are sets which are not finite. Hence it is
a statement.

(iii) It is a scientifically established fact that sun is a star and, therefore, this sentence
is always true. Hence it is a statement.

(iv) This sentence is subjective in the sense that for those who like mathematics, it
may be fun but for others it may not be. This means that this sentence is not always
true. Hence it is not a statement.

<!-- page 387 -->
(v) It is a scientifically established natural phenomenon that cloud is formed before it
rains. Therefore, this sentence is always true. Hence it is a statement.

(vi) This is a question which also contains the word “Here”. Hence it is not a statement.

The above examples show that whenever we say that a sentence is a statement
we should always say why it is so. This “why” of it is more important than the answer.

EXERCISE 14.1

1. Which of the following sentences are statements? Give reasons for your answer.

(i) There are 35 days in a month.
(ii) Mathematics is difficult.
(iii) The sum of 5 and 7 is greater than 10.
(iv) The square of a number is an even number.
(v) The sides of a quadrilateral have equal length.
(vi) Answer this question.
(vii) The product of $(-1)$ and $8$ is $8$.
(viii) The sum of all interior angles of a triangle is $180^{\circ}$.
(ix) Today is a windy day.
(x) All real numbers are complex numbers.

2. Give three examples of sentences which are not statements. Give reasons for the
answers.

14.3 New Statements from Old

We now look into method for producing new statements from those that we already
have. An English mathematician, “George Boole” discussed these methods in his book
“The laws of Thought” in 1854. Here, we shall discuss two techniques.

As a first step in our study of statements, we look at an important technique that
we may use in order to deepen our understanding of mathematical statements. This
technique is to ask not only what it means to say that a given statement is true but also
what it would mean to say that the given statement is not true.

14.3.1 Negation of a statement The denial of a statement is called the negation of
the statement.

Let us consider the statement:

$p: New Delhi is a city$
The negation of this statement is

<!-- page 388 -->
It is not the case that New Delhi is a city

This can also be written as

It is false that New Delhi is a city.

This can simply be expressed as

New Delhi is not a city.

Definition 1 If $p$ is a statement, then the negation of $p$ is also a statement and is
denoted by $\sim p$, and read as ‘not $p$’.

Note While forming the negation of a statement, phrases like, “It is not the
case” or “It is false that” are also used.

Here is an example to illustrate how, by looking at the negation of a statement, we
may improve our understanding of it.
Let us consider the statement

$p$: Everyone in Germany speaks German.

The denial of this sentence tells us that not everyone in Germany speaks German.
This does not mean that no person in Germany speaks German. It says merely that at
least one person in Germany does not speak German.

We shall consider more examples.

Example 2 Write the negation of the following statements.
(i) Both the diagonals of a rectangle have the same length.
(ii) $\sqrt{7}$ is rational.

Solution (i) This statement says that in a rectangle, both the diagonals have the same
length. This means that if you take any rectangle, then both the diagonals have the
same length. The negation of this statement is

It is false that both the diagonals in a rectangle have the same length
This means the statement

There is atleast one rectangle whose both diagonals do not
have the same length.

(ii) The negation of the statement in (ii) may also be written as

It is not the case that $\sqrt{7}$ is rational.

This can also be rewritten as

$$\sqrt{7} \ is \ not \ rational.$$

<!-- page 389 -->
Example 3 Write the negation of the following statements and check whether the
resulting statements are true,
(i) Australia is a continent.
(ii) There does not exist a quadrilateral which has all its sides equal.
(iii) Every natural number is greater than 0.
(iv) The sum of 3 and 4 is 9.

Solution (i) The negation of the statement is

It is false that Australia is a continent.

This can also be rewritten as

Australia is not a continent.

We know that this statement is false.

(ii) The negation of the statement is

It is not the case that there does not exist a quadrilateral which has all its sides
equal.

This also means the following:

There exists a quadrilateral which has all its sides equal.

This statement is true because we know that square is a quadrilateral such that its four
sides are equal.

(iii) The negation of the statement is

It is false that every natural number is greater than 0.

This can be rewritten as

There exists a natural number which is not greater than $0$.

This is a false statement.

(iv) The negation is

It is false that the sum of $3$ and $4$ is $9$.

This can be written as

The sum of $3$ and $4$ is not equal to $9$.

This statement is true.

14.3.2 *Compound statements* Many mathematical statements are obtained by
combining one or more statements using some connecting words like “and”, “or”, etc.
Consider the following statement

$p$: There is something wrong with the bulb or with the wiring.
This statement tells us that there is something wrong with the bulb or there is

<!-- page 390 -->
something wrong with the wiring. That means the given statement is actually made up
of two smaller statements:

$q$: There is something wrong with the bulb.
$r$: There is something wrong with the wiring.

connected by “or”

Now, suppose two statements are given as below:

$p: 7$ is an odd number.
$q: 7$ is a prime number.

These two statements can be combined with “and”

$r$: 7 is both odd and prime number.

This is a compound statement.

This leads us to the following definition:

Definition 2 A Compound Statement is a statement which is made up of two or
more statements. In this case, each statement is called a component statement.
Let us consider some examples.

Example 4 Find the component statements of the following compound statements.
(i) The sky is blue and the grass is green.
(ii) It is raining and it is cold.
(iii) All rational numbers are real and all real numbers are complex.
(iv) 0 is a positive number or a negative number.

Solution Let us consider one by one
(i) The component statements are
$$p: \text{The sky is blue.}$$
$$q: \text{The grass is green.}$$
The connecting word is ‘and’.
(ii) The component statements are
$$p: \text{It is raining.}$$
$$q: \text{It is cold.}$$
The connecting word is ‘and’.
(iii) The component statements are
$$p: \text{All rational numbers are real.}$$
$$q: \text{All real numbers are complex.}$$
The connecting word is ‘and’.
(iv) The component statements are

<!-- page 391 -->
$p: 0$ is a positive number.
$q: 0$ is a negative number.

The connecting word is ‘or’.

Example 5 Find the component statements of the following and check whether they
are true or not.
(i) A square is a quadrilateral and its four sides equal.
(ii) All prime numbers are either even or odd.
(iii) A person who has taken Mathematics or Computer Science can go for
MCA.
(iv) Chandigarh is the capital of Haryana and UP.
(v) $\sqrt{2}$ is a rational number or an irrational number.
(vi) 24 is a multiple of 2, 4 and 8.

Solution (i) The component statements are
$$p: A \ square \ is \ a \ quadrilateral.$$
$$q: A \ square \ has \ all \ its \ sides \ equal.$$

We know that both these statements are true. Here the connecting word is ‘and’.

(ii) The component statements are
$p$: All prime numbers are odd numbers.
$q$: All prime numbers are even numbers.

Both these statements are false and the connecting word is ‘or’.

(iii) The component statements are
$p$: A person who has taken Mathematics can go for MCA.
$q$: A person who has taken computer science can go for MCA.
Both these statements are true. Here the connecting word is ‘or’.

(iv) The component statements are
$$p: Chandigarh \ is \ the \ capital \ of \ Haryana.$$
$$q: Chandigarh \ is \ the \ capital \ of \ UP.$$

The first statement is true but the second is false. Here the connecting word is ‘and’.

(v) The component statements are

<!-- page 392 -->
$p: \sqrt{2}$ is a rational number.

$q$: $\sqrt{2}$ is an irrational number.

The first statement is false and second is true. Here the connecting word is ‘or’.
(vi) The component statements are

$p: 24$ is a multiple of $2$.

$q$: 24 is a multiple of 4.

$r$: 24 is a multiple of 8.

All the three statements are true. Here the connecting words are ‘and’.
Thus, we observe that compound statements are actually made-up of two or more
statements connected by the words like “and”, “or”, etc. These words have special
meaning in mathematics. We shall discuss this matter in the following section.

EXERCISE 14.2

1. Write the negation of the following statements:
(i) Chennai is the capital of Tamil Nadu.
(ii) $\sqrt{2}$ is not a complex number
(iii) All triangles are not equilateral triangle.
(iv) The number 2 is greater than 7.
(v) Every natural number is an integer.
2. Are the following pairs of statements negations of each other:
(i) The number $x$ is not a rational number.
The number $x$ is not an irrational number.
(ii) The number $x$ is a rational number.
The number $x$ is an irrational number.
3. Find the component statements of the following compound statements and check
whether they are true or false.
(i) Number 3 is prime or it is odd.
(ii) All integers are positive or negative.
(iii) 100 is divisible by 3, 11 and 5.

14.4 Special Words/Phrases

Some of the connecting words which are found in compound statements like “And”,

<!-- page 393 -->
“**Or**”, **etc.** are often used in Mathematical Statements. These are called connectives.
When we use these compound statements, it is necessary to understand the role of
these words. We discuss this below.

14.4.1 *The word “And”* Let us look at a compound statement with “And”.

$p$: A point occupies a position and its location can be determined.

The statement can be broken into two component statements as

$q$: A point occupies a position.

$r$: Its location can be determined.

Here, we observe that both statements are true.
Let us look at another statement.

$p: 42$ is divisible by $5$, $6$ and $7$.

This statement has following component statements

$q$: 42 is divisible by 5.

$r$: 42 is divisible by 6.

$s$: 42 is divisible by 7.

Here, we know that the first is false while the other two are true.

We have the following rules regarding the connective “And”

1. The compound statement with ‘And’ is true if all its component
   statements are true.
2. The component statement with ‘And’ is false if any of its component
   statements is false (this includes the case that some of its component
   statements are false or all of its component statements are false).

Example 6 Write the component statements of the following compound statements
and check whether the compound statement is true or false.

(i) A line is straight and extends indefinitely in both directions.

(ii) 0 is less than every positive integer and every negative integer.

(iii) All living things have two legs and two eyes.

Solution (i) The component statements are
$$p: A \ line \ is \ straight.$$
$$q: A \ line \ extends \ indefinitely \ in \ both \ directions.$$

<!-- page 394 -->
Both these statements are true, therefore, the compound statement is true.

(ii)   The component statements are
$$p: 0 \text{ is less than every positive integer.}$$
$$q: 0 \text{ is less than every negative integer.}$$

The second statement is false. Therefore, the compound statement is false.

(iii) The two component statements are

$p$: All living things have two legs.
$q$: All living things have two eyes.

Both these statements are false. Therefore, the compound statement is false.
     Now, consider the following statement.

$p$: A mixture of alcohol and water can be separated by chemical methods.

This sentence cannot be considered as a compound statement with “And”. Here the
word “And” refers to two things – alcohol and water.

This leads us to an important note.

Note Do not think that a statement with “And” is always a compound statement
as shown in the above example. Therefore, the word “And” is not used as a connective.

14.4.2 *The word “Or”* Let us look at the following statement.

$p$: Two lines in a plane either intersect at one point or they are parallel.

We know that this is a true statement. What does this mean? This means that if two
lines in a plane intersect, then they are not parallel. Alternatively, if the two lines are not
parallel, then they intersect at a point. That is this statement is true in both the situations.

In order to understand statements with “Or” we first notice that the word “Or” is
used in two ways in English language. Let us first look at the following statement.

$p$: An ice cream or pepsi is available with a Thali in a restaurant.

This means that a person who does not want ice cream can have a pepsi along
with $Thali$ or one does not want pepsi can have an ice cream along with $Thali$. That is,
who do not want a pepsi can have an ice cream. A person cannot have both ice cream
and pepsi. This is called an $exclusive$ “$Or$”.
Here is another statement.

Here is another statement.

A student who has taken biology or chemistry can apply for M.Sc.
microbiology programme.

Here we mean that the students who have taken both biology and chemistry can
apply for the microbiology programme, as well as the students who have taken only
one of these subjects. In this case, we are using **inclusive “Or”**.
It is important to note the difference between these two ways because we require this
when we check whether the statement is true or not.

<!-- page 395 -->
Let us look at an example.

Example 7 For each of the following statements, determine whether an **inclusive**
**“Or”** or **exclusive “Or”** is used. Give reasons for your answer.

(i) To enter a country, you need a passport or a voter registration card.

(ii) The school is closed if it is a holiday or a Sunday.

(iii) Two lines intersect at a point or are parallel.

(iv) Students can take French or Sanskrit as their third language.

Solution (i)Here “Or” is inclusive since a person can have both a passport and a
voter registration card to enter a country.

(ii) Here also “Or” is inclusive since school is closed on holiday as well as on
Sunday.
(iii) Here “Or” is exclusive because it is not possible for two lines to intersect
and parallel together.
(iv) Here also “Or” is exclusive because a student cannot take both French and
Sanskrit.

Rule for the compound statement with ‘Or’

1.  A compound statement with an ‘Or’ is true when one component
    statement is true or both the component statements are true.

2.  A compound statement with an ‘Or’ is false when both the component
    statements are false.

For example, consider the following statement.

$p$: Two lines intersect at a point or they are parallel

The component statements are

$q$: Two lines intersect at a point.
$r$: Two lines are parallel.

Then, when $q$ is true $r$ is false and when $r$ is true $q$ is false. Therefore, the
compound statement $p$ is true.
Consider another statement.

$p$: 125 is a multiple of 7 or 8.

Its component statements are

$q$: $125$ is a multiple of $7$.

r: 125 is a multiple of 8.

Both $q$ and $r$ are false. Therefore, the compound statement $p$ is false.

<!-- page 396 -->
Again, consider the following statement:

$p$: The school is closed, if there is a holiday or Sunday.

The component statements are

$q$: $School$ $is$ $closed$ $if$ $there$ $is$ $a$ $holiday$.
$r$: $School$ $is$ $closed$ $if$ $there$ $is$ $a$ $Sunday$.

Both $q$ and $r$ are true, therefore, the compound statement is true.
Consider another statement.

$p$: Mumbai is the capital of Kolkata or Karnataka.

The component statements are

$q$: $Mumbai$ $is$ $the$ $capital$ $of$ $Kolkata$.
$r$: $Mumbai$ $is$ $the$ $capital$ $of$ $Karnataka$.

Both these statements are false. Therefore, the compound statement is false.
Let us consider some examples.

Example 8 Identify the type of “Or” used in the following statements and check
whether the statements are true or false:
(i) $\sqrt{2}$ is a rational number or an irrational number.
(ii) To enter into a public library children need an identity card from the school
or a letter from the school authorities.
(iii) A rectangle is a quadrilateral or a 5-sided polygon.

Solution (i) The component statements are

$p: \sqrt{2}$ is a rational number.
$q: \sqrt{2}$ is an irrational number.

Here, we know that the first statement is false and the second is true and “Or” is
exclusive. Therefore, the compound statement is true.

(ii) The component statements are

$p$: To get into a public library children need an identity card.

$q$: To get into a public library children need a letter from the school authorities.

Children can enter the library if they have either of the two, an identity card or the
letter, as well as when they have both. Therefore, it is inclusive “Or” the compound
statement is also true when children have both the card and the letter.

(iii) Here “Or” is exclusive. When we look at the component statements, we get that
the statement is true.

<!-- page 397 -->
14.4.3 Quantifiers Quantifiers are phrases like, “There exists” and “For all”.
Another phrase which appears in mathematical statements is “there exists”. For example,
consider the statement. $p$: There exists a rectangle whose all sides are equal. This
means that there is atleast one rectangle whose all sides are equal.

A word closely connected with “there exists” is “for every” (or for all). Consider
a statement.

$p$: For every prime number $p$, $\sqrt{p}$ is an irrational number.

This means that if S denotes the set of all prime numbers, then for all the members $p$ of
the set S, $\sqrt{p}$ is an irrational number.

In general, a mathematical statement that says “for every” can be interpreted as
saying that all the members of the given set S where the property applies must satisfy
that property.

We should also observe that it is important to know precisely where in the sentence
a given connecting word is introduced. For example, compare the following two
sentences:

1. For every positive number $x$ there exists a positive number $y$ such that
$y < x$.
2. There exists a positive number $y$ such that for every positive number $x$, we
have $y < x$.

Although these statements may look similar, they do not say the same thing. As a
matter of fact, (1) is true and (2) is false. Thus, in order for a piece of mathematical
writing to make sense, all of the symbols must be carefully introduced and each symbol
must be introduced precisely at the right place – not too early and not too late.

The words “And” and “Or” are called connectives and “There exists” and “For
all” are called quantifiers.

Thus, we have seen that many mathematical statements contain some special words
and it is important to know the meaning attached to them, especially when we have to
check the validity of different statements.

EXERCISE 14.3

1. For each of the following compound statements first identify the connecting words
and then break it into component statements.
(i) All rational numbers are real and all real numbers are not complex.
(ii) Square of an integer is positive or negative.
(iii) The sand heats up quickly in the Sun and does not cool down fast at night.
(iv) $x = 2$ and $x = 3$ are the roots of the equation $3x^2 - x - 10 = 0$.

<!-- page 398 -->
2. Identify the quantifier in the following statements and write the negation of the
statements.
(i) There exists a number which is equal to its square.
(ii) For every real number $x$, $x$ is less than $x + 1$.
(iii) There exists a capital for every state in India.

3. Check whether the following pair of statements are negation of each other. Give
reasons for your answer.
(i) $x + y = y + x$ is true for every real numbers $x$ and $y$.
(ii) There exists real numbers $x$ and $y$ for which $x + y = y + x$.

4. State whether the “Or” used in the following statements is “exclusive “or” inclusive.
Give reasons for your answer.
(i) Sun rises or Moon sets.
(ii) To apply for a driving licence, you should have a ration card or a passport.
(iii) All integers are positive or negative.

14.5 Implications

In this Section, we shall discuss the implications of “if-then”, “only if” and “if and only if”.

The statements with “if-then” are very common in mathematics. For example,
consider the statement.

$r$: If you are born in some country, then you are a citizen of that country.
When we look at this statement, we observe that it corresponds to two statements $p$
and $q$ given by

$p : \text{you are born in some country.}$
$q : \text{you are citizen of that country.}$

Then the sentence “if $p$ then $q$” says that in the event if $p$ is true, then $q$ must be true.

One of the most important facts about the sentence “if $p$ then $q$” is that it does
not say any thing (or places no demand) on $q$ when $p$ is false. For example, if you are
not born in the country, then you cannot say anything about $q$. To put it in other words”
not happening of $p$ has no effect on happening of $q$.

Another point to be noted for the statement “if $p$ then $q$” is that the statement
does not imply that $p$ happens.

There are several ways of understanding “if $p$ then $q$” statements. We shall
illustrate these ways in the context of the following statement.

$r$: If a number is a multiple of $9$, then it is a multiple of $3$.

Let $p$ and $q$ denote the statements

$p : a\ number\ is\ a\ multiple\ of\ 9.$
$q:\ a\ number\ is\ a\ multiple\ of\ 3.$

<!-- page 399 -->
Then, if $p$ then $q$ is the same as the following:

1.  $p$ **implies** $q$ is denoted by $p \Rightarrow q$. The symbol $\Rightarrow$ stands for implies.
This says that a number is a multiple of 9 implies that it is a multiple of 3.
2.  $p$ is a sufficient condition for $q$.
This says that knowing that a number as a multiple of 9 is sufficient to conclude
that it is a multiple of 3.
3.  $p$ only if $q$.
This says that a number is a multiple of 9 only if it is a multiple of 3.
4.  $q$ is a necessary condition for $p$.
This says that when a number is a multiple of 9, it is necessarily a multiple of 3.
5.  $\sim q$ implies $\sim p$.
This says that if a number is not a multiple of 3, then it is not a multiple of 9.

14.5.1 *Contrapositive and converse* Contrapositive and converse are certain
other statements which can be formed from a given statement with “if-then”.

For example, let us consider the following “if-then” statement.

If the physical environment changes, then the biological environment changes.

Then the contrapositive of this statement is

If the biological environment does not change, then the physical environment
does not change.

Note that both these statements convey the same meaning.
To understand this, let us consider more examples.

Example 9 Write the contrapositive of the following statement:
(i) If a number is divisible by 9, then it is divisible by 3.
(ii) If you are born in India, then you are a citizen of India.
(iii) If a triangle is equilateral, it is isosceles.

Solution The contrapositive of the these statements are
(i) If a number is not divisible by 3, it is not divisible by 9.
(ii) If you are not a citizen of India, then you were not born in India.
(iii) If a triangle is not isosceles, then it is not equilateral.
The above examples show the contrapositive of the statement if $p$, then $q$ is “if $\sim q$,
then $\sim p$”.
Next, we shall consider another term called converse.
The converse of a given statement “if $p$, then $q$” is if $q$, then $p$.

<!-- page 400 -->
For example, the converse of the statement

$p$: If a number is divisible by $10$, it is divisible by $5$ is
$q$: If a number is divisible by $5$, then it is divisible by $10$.

Example 10 Write the converse of the following statements.

(i) If a number $n$ is even, then $n^2$ is even.
(ii) If you do all the exercises in the book, you get an A grade in the class.
(iii) If two integers $a$ and $b$ are such that $a > b$, then $a - b$ is always a positive
integer.

Solution The converse of these statements are

(i) If a number $n^2$ is even, then $n$ is even.
(ii) If you get an A grade in the class, then you have done all the exercises of
the book.
(iii) If two integers $a$ and $b$ are such that $a-b$ is always a positive integer, then
$a > b$.
Let us consider some more examples.

Let us consider some more examples.

Example 11 For each of the following compound statements, first identify the
corresponding component statements. Then check whether the statements are
true or not.
(i) If a triangle ABC is equilateral, then it is isosceles.
(ii) If $a$ and $b$ are integers, then $ab$ is a rational number.

Solution (i) The component statements are given by

$p : \mathit{Triangle\ ABC\ is\ equilateral.}$
$q : \mathit{Triangle\ ABC\ is\ Isosceles.}$

Since an equilateral triangle is isosceles, we infer that the given compound statement
is true.

(ii) The component statements are given by
$$p : a \text{ and } b \text{ are integers.}$$
$$q : ab \text{ is a rational number.}$$

since the product of two integers is an integer and therefore a rational number, the
compound statement is true.

‘***If and only if***’, represented by the symbol ‘$\Leftrightarrow$’ means the following equivalent forms
for the given statements $p$ and $q$.

(i) $p$ if and only if $q$
(ii) $q$ if and only if $p$

<!-- page 401 -->
(iii) $p$ is necessary and sufficient condition for $q$ and vice-versa
(iv) $p \Leftrightarrow q$
Consider an example.

Consider an example.

Example 12 Given below are two pairs of statements. Combine these two statements
using “if and only if”.
(i) $p$: If a rectangle is a square, then all its four sides are equal.
$q$: If all the four sides of a rectangle are equal, then the rectangle is a
square.
(ii) $p$: If the sum of digits of a number is divisible by 3, then the number is
divisible by 3.

$q$: If a number is divisible by 3, then the sum of its digits is divisible by 3.

Solution (i) A rectangle is a square if and only if all its four sides are equal.

(ii) A number is divisible by 3 if and only if the sum of its digits is divisible by 3.

EXERCISE 14.4

1. Rewrite the following statement with “if-then” in five different ways conveying
the same meaning.

$$If\ a\ natural\ number\ is\ odd,\ then\ its\ square\ is\ also\ odd.$$

2. Write the contrapositive and converse of the following statements.

(i) If $x$ is a prime number, then $x$ is odd.

(ii) If the two lines are parallel, then they do not intersect in the same plane.

(iii) Something is cold implies that it has low temperature.

(iv) You cannot comprehend geometry if you do not know how to reason
deductively.

(v) $x$ is an even number implies that $x$ is divisible by 4.

3. Write each of the following statements in the form “if-then”

(i) You get a job implies that your credentials are good.

(ii) The Bannana trees will bloom if it stays warm for a month.

(iii) A quadrilateral is a parallelogram if its diagonals bisect each other.

(iv) To get an $A^+$ in the class, it is necessary that you do all the exercises of
the book.

<!-- page 402 -->
4. Given statements in (a) and (b). Identify the statements given below as
contrapositive or converse of each other.

(a) If you live in Delhi, then you have winter clothes.

(i) If you do not have winter clothes, then you do not live in Delhi.

(ii) If you have winter clothes, then you live in Delhi.

(b) If a quadrilateral is a parallelogram, then its diagonals bisect each other.

(i) If the diagonals of a quadrilateral do not bisect each other, then the
quadrilateral is not a parallelogram.

(ii) If the diagonals of a quadrilateral bisect each other, then it is a parallelogram.

14.6 Validating Statements

In this Section, we will discuss when a statement is true. To answer this question, one
must answer all the following questions.

What does the statement mean? What would it mean to say that this statement is
true and when this statement is not true?

The answer to these questions depend upon which of the special words and
phrases “and”, “or”, and which of the implications “if and only”, “if-then”, and which
of the quantifiers “for every”, “there exists”, appear in the given statement.

Here, we shall discuss some techniques to find when a statement is valid.

We shall list some general rules for checking whether a statement is true or not.

Rule 1 If $p$ and $q$ are mathematical statements, then in order to show that the
statement “$p$ and $q$” is true, the following steps are followed.

Step-1 Show that the statement $p$ is true.

Step-2 Show that the statement $q$ is true.

Rule 2 Statements with “Or”

If $p$ and $q$ are mathematical statements , then in order to show that the statement
“$p$ or $q$” is true, one must consider the following.

Case 1 By assuming that $p$ is false, show that $q$ must be true.

Case 2 By assuming that $q$ is false, show that $p$ must be true.

Rule 3 Statements with “If-then”

<!-- page 403 -->
In order to prove the statement “if $p$ then $q$” we need to show that any one of the
following case is true.

Case 1 By assuming that $p$ is true, prove that $q$ must be true.(Direct method)

Case 2 By assuming that $q$ is false, prove that $p$ must be false.(Contrapositive
method)

Rule 4 Statements with “if and only if”

In order to prove the statement “$p$ if and only if $q$”, we need to show.

(i) If $p$ is true, then $q$ is true and (ii) If $q$ is true, then $p$ is true
Now we consider some examples.

Example 13 Check whether the following statement is true or not.
If $x, y \in \mathbf{Z}$ are such that $x$ and $y$ are odd, then $xy$ is odd.

Solution Let $p : x, y \in \mathbb{Z}$ such that $x$ and $y$ are odd

$q : xy$ is odd

To check the validity of the given statement, we apply Case 1 of Rule 3. That is
assume that if $p$ is true, then $q$ is true.

$p$ is true means that $x$ and $y$ are odd integers. Then

$x = 2m + 1$, for some integer $m$. $y = 2n + 1$, for some integer $n$. Thus
$xy = (2m + 1) (2n + 1)$
$= 2(2mn + m + n) + 1$

This shows that $xy$ is odd. Therefore, the given statement is true.

Suppose we want to check this by using Case 2 of Rule 3, then we will proceed
as follows.

We assume that $q$ is not true. This implies that we need to consider the negation
of the statement $q$. This gives the statement

~q : Product $xy$ is even.

This is possible only if either $x$ or $y$ is even. This shows that $p$ is not true. Thus we
have shown that

$$\sim q \Rightarrow \sim p$$

Note The above example illustrates that to prove $p \Rightarrow q$, it is enough to show
$\sim q \Rightarrow \sim p$ which is the contrapositive of the statement $p \Rightarrow q$.

Example 14 Check whether the following statement is true or false by proving its
contrapositive. If $x, y \in \mathbf{Z}$ such that $xy$ is odd, then both $x$ and $y$ are odd.

Solution Let us name the statements as below

<!-- page 404 -->
$p : xy$ is odd.

$$q : both \ x \ and \ y \ are \ odd.$$

We have to check whether the statement $p \Rightarrow q$ is true or not, that is, by checking
its contrapositive statement i.e., $\sim q \Rightarrow \sim p$

Now $\sim q$ : It is false that both $x$ and $y$ are odd. This implies that $x$ (or $y$) is even.

Then $x = 2n$ for some integer $n$.

Therefore, $xy = 2ny$ for some integer $n$. This shows that $xy$ is even. That is $\sim p$ is true.
Thus, we have shown that $\sim q \Rightarrow \sim p$ and hence the given statement is true.

Now what happens when we combine an implication and its converse? Next, we
shall discuss this.

Let us consider the following statements.

$p$ : A tumbler is half empty.

$q$ : A tumbler is half full.

We know that if the first statement happens, then the second happens and also if
the second happens, then the first happens. We can express this fact as

If a tumbler is half empty, then it is half full.

If a tumbler is half full, then it is half empty.

We combine these two statements and get the following:

A tumbler is half empty if and only if it is half full.
Now, we discuss another method.

14.6.1 *By Contradiction* Here to check whether a statement $p$ is true, we assume
that $p$ is not true i.e. $\sim p$ is true. Then, we arrive at some result which contradicts our
assumption. Therefore, we conclude that $p$ is true.

Example 15 Verify by the method of contradiction.

$$p: \sqrt{7} \text{ is irrational}$$

Solution In this method, we assume that the given statement is false. That is
we assume that $\sqrt{7}$ is rational. This means that there exists positive integers $a$ and $b$

such that $\sqrt{7} = \frac{a}{b}$, where $a$ and $b$ have no common factors. Squaring the equation,

<!-- page 405 -->
we get $7 = \frac{a^2}{b^2} \Rightarrow a^2 = 7b^2 \Rightarrow 7$ divides $a$. Therefore, there exists an integer $c$ such

that $a = 7c$. Then $a^2 = 49c^2$ and $a^2 = 7b^2$

that $a = 7c$. Then $a^2 = 49c^2$ and $a^2 = 7b^2$
Hence, $7b^2 = 49c^2 \Rightarrow b^2 = 7c^2 \Rightarrow 7$ divides $b$. But we have already shown that
$7$ divides $a$. This implies that $7$ is a common factor of both of $a$ and $b$ which contradicts
our earlier assumption that $a$ and $b$ have no common factors. This shows that the
assumption $\sqrt{7}$ is rational is wrong. Hence, the statement $\sqrt{7}$ is irrational is true.

Next, we shall discuss a method by which we may show that a statement is false.
The method involves giving an \textbf{\textit{example of a situation where the statement is not}}
\textbf{\textit{valid}}. Such an example is called a \textbf{\textit{counter example}}. The name itself suggests that
this is an example to counter the given statement.

Example 16 By giving a counter example, show that the following statement is false.
If $n$ is an odd integer, then $n$ is prime.

**Solution** The given statement is in the form “if $p$ then $q$” we have to show that this is
false. For this purpose we need to show that if $p$ then $\sim q$. To show this we look for an
odd integer $n$ which is not a prime number. $9$ is one such number. So $n = 9$ is a counter
example. Thus, we conclude that the given statement is false.

In the above, we have discussed some techniques for checking whether a statement
is true or not.

Note In mathematics, counter examples are used to disprove the statement.
However, generating examples in favour of a statement do not provide validity of
the statement.

EXERCISE 14.5

1. Show that the statement
   $p$: “If $x$ is a real number such that $x^3 + 4x = 0$, then $x$ is $0$” is true by
   (i) direct method,      (ii) method of contradiction, (iii) method of contrapositive
2. Show that the statement “For any real numbers $a$ and $b$, $a^2 = b^2$ implies that
   $a = b$” is not true by giving a counter-example.
3. Show that the following statement is true by the method of contrapositive.
   $p$: If $x$ is an integer and $x^2$ is even, then $x$ is also even.
4. By giving a counter example, show that the following statements are not true.
   (i)   $p$: If all the angles of a triangle are equal, then the triangle is an obtuse
      angled triangle.
   (ii)   $q$: The equation $x^2 - 1 = 0$ does not have a root lying between $0$ and $2$.

<!-- page 406 -->
5. Which of the following statements are true and which are false? In each case
give a valid reason for saying so.
(i) $p$: Each radius of a circle is a chord of the circle.
(ii) $q$: The centre of a circle bisects each chord of the circle.
(iii) $r$: Circle is a particular case of an ellipse.
(iv) $s$: If $x$ and $y$ are integers such that $x > y$, then $-x < -y$.
(v) $t$: $\sqrt{11}$ is a rational number.

Miscellaneous Examples

Example 17 Check whether “Or” used in the following compound statement is exclusive
or inclusive? Write the component statements of the compound statements and use
them to check whether the compound statement is true or not. Justify your answer.
$t$: you are wet when it rains or you are in a river.

Solution “Or” used in the given statement is inclusive because it is possible that it rains
and you are in the river.
The component statements of the given statement are
$$p : you are wet when it rains.$$
$$q : You are wet when you are in a river.$$
Here both the component statements are true and therefore, the compound statement
is true.

Example 18 Write the negation of the following statements:
(i) $p$: For every real number $x$, $x^2 > x$.
(ii) $q$: There exists a rational number $x$ such that $x^2 = 2$.
(iii) $r$: All birds have wings.
(iv) $s$: All students study mathematics at the elementary level.

Solution (i) The negation of $p$ is “It is false that $p$ is” which means that the condition
$x^2 > x$ does not hold for all real numbers. This can be expressed as
$\sim p$: There exists a real number $x$ such that $x^2 < x$.
(ii) Negation of $q$ is “it is false that $q$”, Thus $\sim q$ is the statement.
$\sim q$: There does not exist a rational number $x$ such that $x^2 = 2$.
This statement can be rewritten as
$\sim q$: For all real numbers $x$, $x^2 \neq 2$
(iii) The negation of the statement is
$\sim r$: There exists a bird which have no wings.

<!-- page 407 -->
(iv) The negation of the given statement is $\sim s$: There exists a student who does not
study mathematics at the elementary level.

Example 19 Using the words “necessary and sufficient” rewrite the statement “The
integer $n$ is odd if and only if $n^2$ is odd”. Also check whether the statement is true.

Solution The necessary and sufficient condition that the integer $n$ be odd is $n^2$ must be
odd. Let $p$ and $q$ denote the statements

$p$ : the integer $n$ is odd.

$$q : n^2 \text{ is odd.}$$

To check the validity of “$p$ if and only if $q$”, we have to check whether “if $p$ then $q$”
and “if $q$ then $p$” is true.

Case 1 If $p$, then $q$

If $p$, then $q$ is the statement:

If the integer $n$ is odd, then $n^2$ is odd. We have to check whether this statement is
true. Let us assume that $n$ is odd. Then $n = 2k + 1$ when $k$ is an integer. Thus

$$n^2 = (2k + 1)^2$$
$$= 4k^2 + 4k + 1$$

Therefore, $n^2$ is one more than an even number and hence is odd.

Case 2 If $q$, then $p$

If $q$, then $p$ is the statement

If $n$ is an integer and $n^2$ is odd, then $n$ is odd.

We have to check whether this statement is true. We check this by contrapositive
method. The contrapositive of the given statement is:

If $n$ is an even integer, then $n^2$ is an even integer

$n$ is even implies that $n = 2k$ for some $k$. Then $n^2 = 4k^2$. Therefore, $n^2$ is even.

Example 20 For the given statements identify the necessary and sufficient conditions.
$t$: If you drive over 80 km per hour, then you will get a fine.

Solution Let $p$ and $q$ denote the statements:

$p$ : you drive over 80 km per hour.

$q$ : you will get a fine.

The implication if $p$, then $q$ indicates that $p$ is sufficient for $q$. That is driving over
80 km per hour is sufficient to get a fine.
Here the sufficient condition is “driving over 80 km per hour”:
Similarly, if $p$, then $q$ also indicates that $q$ is necessary for $p$. That is

<!-- page 408 -->
When you drive over 80 km per hour, you will necessarily get a fine.
Here the necessary condition is “getting a fine”.

Miscellaneous Exercise on Chapter 14

1. Write the negation of the following statements:
(i) $p$: For every positive real number $x$, the number $x - 1$ is also positive.
(ii) $q$: All cats scratch.
(iii) $r$: For every real number $x$, either $x > 1$ or $x < 1$.
(iv) $s$: There exists a number $x$ such that $0 < x < 1$.

2. State the converse and contrapositive of each of the following statements:
(i) $p$: A positive integer is prime only if it has no divisors other than 1 and itself.
(ii) $q$: I go to a beach whenever it is a sunny day.
(iii) $r$: If it is hot outside, then you feel thirsty.

3. Write each of the statements in the form "if $p$, then $q$"
(i) $p$: It is necessary to have a password to log on to the server.
(ii) $q$: There is traffic jam whenever it rains.
(iii) $r$: You can access the website only if you pay a subscription fee.

4. Rewrite each of the following statements in the form "$p$ if and only if $q$"
(i) $p$: If you watch television, then your mind is free and if your mind is free,
then you watch television.
(ii) $q$: For you to get an A grade, it is necessary and sufficient that you do all
the homework regularly.
(iii) $r$: If a quadrilateral is equiangular, then it is a rectangle and if a quadrilateral
is a rectangle, then it is equiangular.

5. Given below are two statements
$$p : 25 \ is \ a \ multiple \ of \ 5.$$
$$q : 25 \ is \ a \ multiple \ of \ 8.$$
Write the compound statements connecting these two statements with "And" and
"Or". In both cases check the validity of the compound statement.

6. Check the validity of the statements given below by the method given against it.
(i) $p$: The sum of an irrational number and a rational number is irrational (by
contradiction method).
(ii) $q$: If $n$ is a real number with $n > 3$, then $n^2 > 9$ (by contradiction method).

7. Write the following statement in five different ways, conveying the same meaning.
$p$: If a triangle is equiangular, then it is an obtuse angled triangle.

<!-- page 409 -->
Summary

◆ A mathematically acceptable statement is a sentence which is either true or
false.
◆ Explained the terms:
– Negation of a statement $p$: If $p$ denote a statement, then the negation of $p$ is
denoted by $\sim p$.
– Compound statements and their related component statements:
A statement is a compound statement if it is made up of two or more smaller
statements. The smaller statements are called component statements of the
compound statement.
– The role of “And”, “Or”, “There exists” and “For every” in compound
statements.
– The meaning of implications “If”, “only if”, “if and only if”.
A sentence with if $p$, then $q$ can be written in the following ways.
– $p$ implies $q$ (denoted by $p \Rightarrow q$)
– $p$ is a sufficient condition for $q$
– $q$ is a necessary condition for $p$
– $p$ only if $q$
– $\sim q$ implies $\sim p$
– The contrapositive of a statement $p \Rightarrow q$ is the statement $\sim q \Rightarrow \sim p$ . The
converse of a statement $p \Rightarrow q$ is the statement $q \Rightarrow p$.
$p \Rightarrow q$ together with its converse, gives $p$ if and only if $q$.
◆ The following methods are used to check the validity of statements:
(i) direct method
(ii) contrapositive method
(iii) method of contradiction
(iv) using a counter example.

Historical Note

The first treatise on logic was written by Aristotle (384 B.C.-322 B.C.). It
was a collection of rules for deductive reasoning which would serve as a basis
for the study of every branch of knowledge. Later, in the seventeenth century,
German mathematician G. W. Leibnitz (1646 – 1716) conceived the idea of using
symbols in logic to mechanise the process of deductive reasoning. His idea was
realised in the nineteenth century by the English mathematician George Boole
(1815–1864) and Augustus De Morgan (1806–1871) , who founded the modern
subject of symbolic logic.

<!-- page 410 -->
Chapter 15

STATISTICS

❖ "Statistics may be rightly called the science of averages and their
estimates." – A.L.BOWLEY & A.L. BODDINGTON ❖

15.1 Introduction

We know that statistics deals with data collected for specific
purposes. We can make decisions about the data by
analysing and interpreting it. In earlier classes, we have
studied methods of representing data graphically and in
tabular form. This representation reveals certain salient
features or characteristics of the data. We have also studied
the methods of finding a representative value for the given
data. This value is called the measure of central tendency.
Recall mean (arithmetic mean), median and mode are three
measures of central tendency. A $measure$ $of$ $central$
$tendency$ gives us a rough idea where data points are
centred. But, in order to make better interpretation from the
data, we should also have an idea how the data are scattered or how much they are
bunched around a measure of central tendency.

Karl Pearson
(1857-1936)

Consider now the runs scored by two batsmen in their last ten matches as follows:

Batsman A : 30, 91, 0, 64, 42, 80, 30, 5, 117, 71
Batsman B : 53, 46, 48, 50, 53, 53, 58, 60, 57, 52

Clearly, the mean and median of the data are

<table>
<thead>
<tr>
<th></th>
<th>Batsman A</th>
<th>Batsman B</th>
</tr>
</thead>
<tbody>
<tr>
<td>Mean</td>
<td>53</td>
<td>53</td>
</tr>
<tr>
<td>Median</td>
<td>53</td>
<td>53</td>
</tr>
</tbody>
</table>

Recall that, we calculate the mean of a data (denoted by $\bar{x}$ ) by dividing the sum
of the observations by the number of observations, i.e.,

<!-- page 411 -->
$$\overline{x} = \frac{1}{n} \sum_{i=1}^{n} x_i$$

Also, the median is obtained by first arranging the data in ascending or descending
order and applying the following rule.

If the number of observations is odd, then the median is $\left( \frac{n+1}{2} \right)^{\text{th}}$ observation.

If the number of observations is even, then median is the mean of $\left(\frac{n}{2}\right)^{\text{th}}$ and

$$\left( \frac{n}{2} + 1 \right)^{\text{th}} \text{ observations.}$$

We find that the mean and median of the runs scored by both the batsmen A and
B are same i.e., 53. Can we say that the performance of two players is same? Clearly
No, because the variability in the scores of batsman A is from 0 (minimum) to 117
(maximum). Whereas, the range of the runs scored by batsman B is from 46 to 60.

Let us now plot the above scores as dots on a number line. We find the following
diagrams:

For batsman A

For batsman B

Fig 15.1

Fig 15.2

We can see that the dots corresponding to batsman B are close to each other and
are clustering around the measure of central tendency (mean and median), while those
corresponding to batsman A are scattered or more spread out.

Thus, the measures of central tendency are not sufficient to give complete
information about a given data. Variability is another factor which is required to be
studied under statistics. Like ‘$measures\ of\ central\ tendency$’ we want to have a
single number to describe variability. This single number is called a ‘$measure\ of$
$dispersion$’. In this Chapter, we shall learn some of the important measures of dispersion
and their methods of calculation for ungrouped and grouped data.

<!-- page 412 -->
15.2 Measures of Dispersion

The dispersion or scatter in a data is measured on the basis of the observations and the
types of the measure of central tendency, used there. There are following measures of
dispersion:

(i) Range, (ii) Quartile deviation, (iii) Mean deviation, (iv) Standard deviation.

In this Chapter, we shall study all of these measures of dispersion except the
quartile deviation.

15.3 Range

Recall that, in the example of runs scored by two batsmen A and B, we had some idea
of variability in the scores on the basis of minimum and maximum runs in each series.
To obtain a single number for this, we find the difference of maximum and minimum
values of each series. This difference is called the ‘Range’ of the data.

In case of batsman A, Range $= 117 - 0 = 117$ and for batsman B, Range $= 60 - 46 = 14$.
Clearly, Range of A $>$ Range of B. Therefore, the scores are scattered or dispersed in
case of A while for B these are close to each other.

Thus, Range of a series = Maximum value – Minimum value.

The range of data gives us a rough idea of variability or scatter but does not tell
about the dispersion of the data from a measure of central tendency. For this purpose,
we need some other measure of variability. Clearly, such measure must depend upon
the difference (or deviation) of the values from the central tendency.

The important measures of dispersion, which depend upon the deviations of the
observations from a central tendency are mean deviation and standard deviation. Let
us discuss them in detail.

15.4 Mean Deviation

Recall that the deviation of an observation $x$ from a fixed value '$a$' is the difference
$x-a$. In order to find the dispersion of values of $x$ from a central value '$a$', we find the
deviations about $a$. An absolute measure of dispersion is the mean of these deviations.
To find the mean, we must obtain the sum of the deviations. But, we know that a
measure of central tendency lies between the maximum and the minimum values of
the set of observations. Therefore, some of the deviations will be negative and some
positive. Thus, the sum of deviations may vanish. Moreover, the sum of the deviations
from mean ( $\bar{x}$ ) is zero.

$$\text{Also} \qquad \text{Mean of deviations} = \frac{\text{Sum of deviations}}{\text{Number of observations}} = \frac{0}{n} = 0$$

Thus, finding the mean of deviations about mean is not of any use for us, as far
as the measure of dispersion is concerned.

<!-- page 413 -->
Remember that, in finding a suitable measure of dispersion, we require the distance
of each value from a central tendency or a fixed number ‘$a$’. Recall, that the absolute
value of the difference of two numbers gives the distance between the numbers when
represented on a number line. Thus, to find the measure of dispersion from a fixed
number ‘$a$’ we may take the mean of the absolute values of the deviations from the
central value. This mean is called the ‘$mean$ $deviation$’. Thus mean deviation about a
central value ‘$a$’ is the mean of the absolute values of the deviations of the observations
from ‘$a$’. The mean deviation from ‘$a$’ is denoted as M.D. ($a$). Therefore,

$$\text{M.D.}(a) = \frac{\text{Sum of absolute values of deviations from } 'a'}{\text{Number of observations}}.$$

$\textit{Remark}$ Mean deviation may be obtained from any measure of central tendency.
However, mean deviation from mean and median are commonly used in statistical
studies.

Let us now learn how to calculate mean deviation about mean and mean deviation
about median for various types of data

15.4.1 *Mean deviation for ungrouped data* Let $n$ observations be $x_1, x_2, x_3, ....., x_n$.
The following steps are involved in the calculation of mean deviation about mean or
median:

Step 1 Calculate the measure of central tendency about which we are to find the mean
deviation. Let it be '$a$'.

Step 2 Find the deviation of each $x_i$ from $a$, i.e., $x_1 - a$, $x_2 - a$, $x_3 - a$, . . . , $x_n - a$

Step 3 Find the absolute values of the deviations, i.e., drop the minus sign $(-)$, if it is

there, i.e., $|x_1 - a|, |x_2 - a|, |x_3 - a|, ....., |x_n - a|$

Step 4 Find the mean of the absolute values of the deviations. This mean is the mean
deviation about $a$, i.e.,

$$\text{M.D.}(a) = \frac{\sum_{i=1}^{n} |x_i - a|}{n}$$

Thus $\quad \text{M.D. ( } \bar{x} \text{ ) } = \frac{1}{n} \sum_{i=1}^{n} |x_i - \bar{x}|, \text{ where } \bar{x} = \text{Mean}$

and $\qquad \mathrm{M.D. (M)} = \frac{1}{n} \sum_{i=1}^{n} |x_i - \mathrm{M}|$, where $\mathrm{M} = \mathrm{Median}$

<!-- page 414 -->
Note In this Chapter, we shall use the symbol M to denote median unless stated
otherwise.Let us now illustrate the steps of the above method in following examples.

Example 1 Find the mean deviation about the mean for the following data:

$6, 7, 10, 12, 13, 4, 8, 12$

Solution We proceed step-wise and get the following:

Step 1 Mean of the given data is

$$\bar{x} = \frac{6+7+10+12+13+4+8+12}{8} = \frac{72}{8} = 9$$

Step 2 The deviations of the respective observations from the mean $\bar{x}$, i.e., $x_i - \bar{x}$ are
$$6 - 9, 7 - 9, 10 - 9, 12 - 9, 13 - 9, 4 - 9, 8 - 9, 12 - 9,$$
or $-3, -2, 1, 3, 4, -5, -1, 3$$Step 3 The absolute values of the deviations, i.e., $|x_i - \overline{x}|$ are$$3, 2, 1, 3, 4, 5, 1, 3$$Step 4 The required mean deviation about the mean is \\ M.D. ($\bar{x}$) = $\frac{\sum_{i=1}^{8} |x_i - \bar{x}|}{8}$ \\ $= \frac{3 + 2 + 1 + 3 + 4 + 5 + 1 + 3}{8} = \frac{22}{8} = 2.75$ \\ $\rightarrow$ **Note** Instead of carrying out the steps every time, we can carry on calculation, \\ step-wise without referring to steps. \\ Example 2 Find the mean deviation about the mean for the following data :$$12, 3, 18, 17, 4, 9, 17, 19, 20, 15, 8, 17, 2, 3, 16, 11, 3, 1, 0, 5$$Solution We have to first find the mean ( $\bar{x}$ ) of the given data$$\bar{x} = \frac{1}{20} \sum_{i=1}^{20} x_i = \frac{200}{20} = 10$$The respective absolute values of the deviations from mean, i.e., $|x_i - \bar{x}|$ are$$2, 7, 8, 7, 6, 1, 7, 9, 10, 5, 2, 7, 8, 7, 6, 1, 7, 9, 10, 5$$

<!-- page 415 -->
Therefore $\sum_{i=1}^{20} |x_i - \bar{x}| = 124$

and M.D. ( $\bar{x}$ ) = $\frac{124}{20} = 6.2$

Example 3 Find the mean deviation about the median for the following data:
$$3, 9, 5, 3, 12, 10, 18, 4, 7, 19, 21.$$

Solution Here the number of observations is 11 which is odd. Arranging the data into
ascending order, we have $3, 3, 4, 5, 7, 9, 10, 12, 18, 19, 21$

Now $\text{Median} = \left( \frac{11 + 1}{2} \right)^{\text{th}} \text{ or } 6^{\text{th}} \text{ observation} = 9$

The absolute values of the respective deviations from the median, i.e., $|x_i - M|$ are
$$6, 6, 5, 4, 2, 0, 1, 3, 9, 10, 12$$

Therefore $$\sum_{i=1}^{11} |x_i - M| = 58$$

and $\text{M.D. (M)} = \frac{1}{11} \sum_{i=1}^{11} |x_i - \text{M}| = \frac{1}{11} \times 58 = 5.27$

15.4.2 Mean deviation for grouped data We know that data can be grouped into
two ways :

(a) Discrete frequency distribution,
(b) Continuous frequency distribution.

Let us discuss the method of finding mean deviation for both types of the data.

(a) **Discrete frequency distribution** Let the given data consist of $n$ distinct values
$x_1, x_2, ..., x_n$ occurring with frequencies $f_1, f_2, ..., f_n$ respectively. This data can be
represented in the tabular form as given below, and is called *discrete frequency*
*distribution*:

$$x : x_1 \quad x_2 \quad x_3 \dots x_n$$
$$f : f_1 \quad f_2 \quad f_3 \dots f_n$$

(i) Mean deviation about mean

First of all we find the mean $\bar{x}$ of the given data by using the formula

<!-- page 416 -->
$$\bar{x} = \frac{\displaystyle\sum_{i=1}^{n} x_i f_i}{\displaystyle\sum_{i=1}^{n} f_i} = \frac{1}{N} \sum_{i=1}^{n} x_i f_i ,$$

where $\sum_{i=1}^{n} x_{i} f_{i}$ denotes the sum of the products of observations $x_{i}$ with their respective

$$f_{i}$$ frequency frequencies $f_{i}$ and $\mathrm{N}=\sum_{i=1}^{n} f_{i}$ is the sum of the frequencies.

Then, we find the deviations of observations $x_i$ from the mean $\bar{x}$ and take their
absolute values, i.e., $|x_i - \bar{x}|$ for all $i = 1, 2, ..., n$.

After this, find the mean of the absolute values of the deviations, which is the
required mean deviation about the mean. Thus

$$\text{M.D. } (\overline{x}) = \frac{\sum_{i=1}^{n} f_i |x_i - \overline{x}|}{\sum_{i=1}^{n} f_i} = \frac{1}{\text{N}} \sum_{i=1}^{n} f_i |x_i - \overline{x}|$$

(ii) Mean deviation about median To find mean deviation about median, we find the
median of the given discrete frequency distribution. For this the observations are arranged
in ascending order. After this the cumulative frequencies are obtained. Then, we identify

the observation whose cumulative frequency is equal to or just greater than $\frac{N}{2}$, where

N is the sum of frequencies. This value of the observation lies in the middle of the data,
therefore, it is the required median. After finding median, we obtain the mean of the
absolute values of the deviations from median.Thus,

$$\text{M.D.(M)} = \frac{1}{\text{N}} \sum_{i=1}^{n} f_i |x_i - \text{M}|$$

Example 4 Find mean deviation about the mean for the following data :
$$x_i \quad 2 \quad 5 \quad 6 \quad 8 \quad 10 \quad 12$$
$$f_i \quad 2 \quad 8 \quad 10 \quad 7 \quad 8 \quad 5$$
Solution Let us make a Table 15.1 of the given data and append other columns after
calculations.

<!-- page 417 -->
Table 15.1

<table>
<thead>
<tr>
<th>$x_i$</th>
<th>$f_i$</th>
<th>$f_i x_i$</th>
<th>$|x_i - \bar{x}|$</th>
<th>$f_i |x_i - \bar{x}|$</th>
</tr>
</thead>
<tbody>
<tr>
<td>2</td>
<td>2</td>
<td>4</td>
<td>5.5</td>
<td>11</td>
</tr>
<tr>
<td>5</td>
<td>8</td>
<td>40</td>
<td>2.5</td>
<td>20</td>
</tr>
<tr>
<td>6</td>
<td>10</td>
<td>60</td>
<td>1.5</td>
<td>15</td>
</tr>
<tr>
<td>8</td>
<td>7</td>
<td>56</td>
<td>0.5</td>
<td>3.5</td>
</tr>
<tr>
<td>10</td>
<td>8</td>
<td>80</td>
<td>2.5</td>
<td>20</td>
</tr>
<tr>
<td>12</td>
<td>5</td>
<td>60</td>
<td>4.5</td>
<td>22.5</td>
</tr>
</tbody>
<tfoot>
<tr>
<td></td>
<td>40</td>
<td>300</td>
<td></td>
<td>92</td>
</tr>
</tfoot>
</table>

$$\mathrm{N} = \sum_{i=1}^{6} f_i = 40 \ , \ \sum_{i=1}^{6} f_i x_i = 300 \ , \ \sum_{i=1}^{6} f_i |x_i - \bar{x}| = 92$$

Therefore $\bar{x} = \frac{1}{N} \sum_{i=1}^{6} f_i x_i = \frac{1}{40} \times 300 = 7.5$

and M.D. $(\bar{x}) = \frac{1}{N} \sum_{i=1}^{6} f_i \left| x_i - \bar{x} \right| = \frac{1}{40} \times 92 = 2.3$

Example 5 Find the mean deviation about the median for the following data:

<table>
  <tbody>
    <tr>
      <td>$x_i$</td>
      <td>3</td>
      <td>6</td>
      <td>9</td>
      <td>12</td>
      <td>13</td>
      <td>15</td>
      <td>21</td>
      <td>22</td>
    </tr>
    <tr>
      <td>$f_i$</td>
      <td>3</td>
      <td>4</td>
      <td>5</td>
      <td>2</td>
      <td>4</td>
      <td>5</td>
      <td>4</td>
      <td>3</td>
    </tr>
  </tbody>
</table>

**Solution** The given observations are already in ascending order. Adding a row
corresponding to cumulative frequencies to the given data, we get (Table 15.2).

Table 15.2

<table>
<thead>
<tr>
<th>$x_i$</th>
<th>3</th>
<th>6</th>
<th>9</th>
<th>12</th>
<th>13</th>
<th>15</th>
<th>21</th>
<th>22</th>
</tr>
</thead>
<tbody>
<tr>
<td>$f_i$</td>
<td>3</td>
<td>4</td>
<td>5</td>
<td>2</td>
<td>4</td>
<td>5</td>
<td>4</td>
<td>3</td>
</tr>
<tr>
<td>c.f.</td>
<td>3</td>
<td>7</td>
<td>12</td>
<td>14</td>
<td>18</td>
<td>23</td>
<td>27</td>
<td>30</td>
</tr>
</tbody>
</table>

Now, $N=30$ which is even.

<!-- page 418 -->
Median is the mean of the $15^{\text{th}}$ and $16^{\text{th}}$ observations. Both of these observations
lie in the cumulative frequency 18, for which the corresponding observation is 13.

Therefore, Median M = $\frac{15^{\text{th}} \text{ observation} + 16^{\text{th}} \text{ observation}}{2} = \frac{13+13}{2} = 13$

Now, absolute values of the deviations from median, i.e., $|x_i - \text{M}|$ are shown in
Table 15.3.

Table 15.3

<table>
<thead>
<tr>
<th>|x_i - M|</th>
<th>10</th>
<th>7</th>
<th>4</th>
<th>1</th>
<th>0</th>
<th>2</th>
<th>8</th>
<th>9</th>
</tr>
</thead>
<tbody>
<tr>
<td>f_i</td>
<td>3</td>
<td>4</td>
<td>5</td>
<td>2</td>
<td>4</td>
<td>5</td>
<td>4</td>
<td>3</td>
</tr>
<tr>
<td>f_i|x_i - M|</td>
<td>30</td>
<td>28</td>
<td>20</td>
<td>2</td>
<td>0</td>
<td>10</td>
<td>32</td>
<td>27</td>
</tr>
</tbody>
</table>

We have $\qquad \qquad \sum_{i=1}^{8} f_{i}=30 \quad \text { and } \sum_{i=1}^{8} f_{i}\left|x_{i}-\mathrm{M}\right|=149$

Therefore $\qquad \text{M.D.(M)} = \frac{1}{\text{N}} \sum_{i=1}^{8} f_i |x_i - \text{M}|$
$\qquad \qquad \qquad \quad = \frac{1}{30} \times 149 = 4.97.$

(b) Continuous frequency distribution A continuous frequency distribution is a series
in which the data are classified into different class-intervals without gaps alongwith
their respective frequencies.

For example, marks obtained by 100 students are presented in a continuous
frequency distribution as follows :

<table>
<thead>
<tr>
<th>Marks obtained</th>
<th>0-10</th>
<th>10-20</th>
<th>20-30</th>
<th>30-40</th>
<th>40-50</th>
<th>50-60</th>
</tr>
</thead>
<tbody>
<tr>
<td>Number of Students</td>
<td>12</td>
<td>18</td>
<td>27</td>
<td>20</td>
<td>17</td>
<td>6</td>
</tr>
</tbody>
</table>

(i) Mean deviation about mean While calculating the mean of a continuous frequency
distribution, we had made the assumption that the frequency in each class is centred at
its mid-point. Here also, we write the mid-point of each given class and proceed further
as for a discrete frequency distribution to find the mean deviation.

Let us take the following example.

<!-- page 419 -->
Example 6 Find the mean deviation about the mean for the following data.

<table>
<thead>
<tr>
<th>Marks obtained</th>
<th>10-20</th>
<th>20-30</th>
<th>30-40</th>
<th>40-50</th>
<th>50-60</th>
<th>60-70</th>
<th>70-80</th>
</tr>
</thead>
<tbody>
<tr>
<td>Number of students</td>
<td>2</td>
<td>3</td>
<td>8</td>
<td>14</td>
<td>8</td>
<td>3</td>
<td>2</td>
</tr>
</tbody>
</table>

Solution We make the following Table 15.4 from the given data :

Table 15.4

<table>
<thead>
<tr>
<th>Marks<br/>obtained</th>
<th>Number of<br/>students<br/>$f_i$</th>
<th>Mid-points<br/>$x_i$</th>
<th>$f_i x_i$</th>
<th>$|x_i - \bar{x}|$</th>
<th>$f_i |x_i - \bar{x}|$</th>
</tr>
</thead>
<tbody>
<tr>
<td>10-20</td>
<td>2</td>
<td>15</td>
<td>30</td>
<td>30</td>
<td>60</td>
</tr>
<tr>
<td>20-30</td>
<td>3</td>
<td>25</td>
<td>75</td>
<td>20</td>
<td>60</td>
</tr>
<tr>
<td>30-40</td>
<td>8</td>
<td>35</td>
<td>280</td>
<td>10</td>
<td>80</td>
</tr>
<tr>
<td>40-50</td>
<td>14</td>
<td>45</td>
<td>630</td>
<td>0</td>
<td>0</td>
</tr>
<tr>
<td>50-60</td>
<td>8</td>
<td>55</td>
<td>440</td>
<td>10</td>
<td>80</td>
</tr>
<tr>
<td>60-70</td>
<td>3</td>
<td>65</td>
<td>195</td>
<td>20</td>
<td>60</td>
</tr>
<tr>
<td>70-80</td>
<td>2</td>
<td>75</td>
<td>150</td>
<td>30</td>
<td>60</td>
</tr>
</tbody>
<tfoot>
<tr>
<td></td>
<td>40</td>
<td></td>
<td>1800</td>
<td></td>
<td>400</td>
</tr>
</tfoot>
</table>

Here $\qquad \qquad \qquad \mathrm{N} = \sum_{i=1}^{7} f_{i} = 40, \sum_{i=1}^{7} f_{i} x_{i} = 1800, \sum_{i=1}^{7} f_{i} |x_{i} - \bar{x}| = 400$

Therefore $$\bar{x} = \frac{1}{N} \sum_{i=1}^{7} f_i x_i = \frac{1800}{40} = 45$$

and $\text{M.D.}(\bar{x}) = \frac{1}{\text{N}} \sum_{i=1}^{7} f_i |x_i - \bar{x}| = \frac{1}{40} \times 400 = 10$

Shortcut method for calculating mean deviation about mean We can avoid the
tedious calculations of computing $\bar{x}$ by following step-deviation method. Recall that in
this method, we take an assumed mean which is in the middle or just close to it in the
data. Then deviations of the observations (or mid-points of classes) are taken from the

<!-- page 420 -->
assumed mean. This is nothing but the shifting of origin from zero to the assumed mean
on the number line, as shown in Fig 15.3

Fig 15.3

If there is a common factor of all the deviations, we divide them by this common
factor to further simplify the deviations. These are known as step-deviations. The
process of taking step-deviations is the change of scale on the number line as shown in
Fig 15.4

Fig 15.4

The deviations and step-deviations reduce the size of the observations, so that the
computations viz. multiplication, etc., become simpler. Let, the new variable be denoted

by $d_i = \frac{x_i - a}{h}$, where '$a$' is the assumed mean and $h$ is the common factor. Then, the

mean $\bar{x}$ by step-deviation method is given by

$$\bar{x} = a + \frac{\sum_{i=1}^{n} f_i d_i}{N} \times h$$

Let us take the data of Example 6 and find the mean deviation by using stepdeviation method.

<!-- page 421 -->
Take the assumed mean $a = 45$ and $h = 10$, and form the following Table 15.5.

Table 15.5

<table>
<thead>
<tr>
<th>Marks<br/>obtained</th>
<th>Number of<br/>students</th>
<th>Mid-points</th>
<th>$d_i = \frac{x_i - 45}{10}$</th>
<th>$f_i d_i$</th>
<th>$|x_i - \bar{x}|$</th>
<th>$f_i |x_i - \bar{x}|$</th>
</tr>
</thead>
<tbody>
<tr>
<td></td>
<td>$f_i$</td>
<td>$x_i$</td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>10-20</td>
<td>2</td>
<td>15</td>
<td>– 3</td>
<td>– 6</td>
<td>30</td>
<td>60</td>
</tr>
<tr>
<td>20-30</td>
<td>3</td>
<td>25</td>
<td>– 2</td>
<td>– 6</td>
<td>20</td>
<td>60</td>
</tr>
<tr>
<td>30-40</td>
<td>8</td>
<td>35</td>
<td>– 1</td>
<td>– 8</td>
<td>10</td>
<td>80</td>
</tr>
<tr>
<td>40-50</td>
<td>14</td>
<td>45</td>
<td>0</td>
<td>0</td>
<td>0</td>
<td>0</td>
</tr>
<tr>
<td>50-60</td>
<td>8</td>
<td>55</td>
<td>1</td>
<td>8</td>
<td>10</td>
<td>80</td>
</tr>
<tr>
<td>60-70</td>
<td>3</td>
<td>65</td>
<td>2</td>
<td>6</td>
<td>20</td>
<td>60</td>
</tr>
<tr>
<td>70-80</td>
<td>2</td>
<td>75</td>
<td>3</td>
<td>6</td>
<td>30</td>
<td>60</td>
</tr>
<tr>
<td></td>
<td>40</td>
<td></td>
<td></td>
<td>0</td>
<td></td>
<td>400</td>
</tr>
</tbody>
</table>

Therefore $$\bar{x} = a + \frac{\sum_{i=1}^{7} f_i d_i}{N} \times h$$

$$= 45 + \frac{0}{40} \times 10 = 45$$

and M.D. $(\bar{x}) = \frac{1}{N} \sum_{i=1}^{7} f_i |x_i - \bar{x}| = \frac{400}{40} = 10$

Note The step deviation method is applied to compute $\bar{x}$ . Rest of the procedure
is same.

(ii) Mean deviation about median The process of finding the mean deviation about
median for a continuous frequency distribution is similar as we did for mean deviation
about the mean. The only difference lies in the replacement of the mean by median
while taking deviations.

Let us recall the process of finding median for a continuous frequency distribution.
The data is first arranged in ascending order. Then, the median of continuous
frequency distribution is obtained by first identifying the class in which median lies
(median class) and then applying the formula

<!-- page 422 -->
$$\text{Median} = l + \frac{\frac{\text{N}}{2} - \text{C}}{f} \times h$$

where median class is the class interval whose cumulative frequency is just greater

than or equal to $\frac{\mathrm{N}}{2}$, $\mathrm{N}$ is the sum of frequencies, $l, f, h$ and $\mathrm{C}$ are, respectively the lower
limit , the frequency, the width of the median class and $\mathrm{C}$ the cumulative frequency of
the class just preceding the median class. After finding the median, the absolute values
of the deviations of mid-point $x_i$ of each class from the median i.e., $|x_i - \mathrm{M}|$ are obtained.

Then $\text{M.D. (M)} = \frac{1}{\text{N}} \sum_{i=1}^{n} f_i |x_i - \text{M}|$

The process is illustrated in the following example:

Example 7 Calculate the mean deviation about median for the following data :

<table>
<thead>
<tr>
<th>Class</th>
<th>0-10</th>
<th>10-20</th>
<th>20-30</th>
<th>30-40</th>
<th>40-50</th>
<th>50-60</th>
</tr>
</thead>
<tbody>
<tr>
<td>Frequency</td>
<td>6</td>
<td>7</td>
<td>15</td>
<td>16</td>
<td>4</td>
<td>2</td>
</tr>
</tbody>
</table>

Solution Form the following Table 15.6 from the given data :

Table 15.6

<table>
<thead>
<tr>
<th>Class</th>
<th>Frequency</th>
<th>Cumulative<br/>frequency</th>
<th>Mid-points</th>
<th>$|x_i - \text{Med.}|$</th>
<th>$f_i | x_i - \text{Med.}|$</th>
</tr>
</thead>
<tbody>
<tr>
<td></td>
<td>$f_i$</td>
<td>$(c.f.)$</td>
<td>$x_i$</td>
<td></td>
<td></td>
</tr>
<tr>
<td>0-10</td>
<td>6</td>
<td>6</td>
<td>5</td>
<td>23</td>
<td>138</td>
</tr>
<tr>
<td>10-20</td>
<td>7</td>
<td>13</td>
<td>15</td>
<td>13</td>
<td>91</td>
</tr>
<tr>
<td>20-30</td>
<td>15</td>
<td>28</td>
<td>25</td>
<td>3</td>
<td>45</td>
</tr>
<tr>
<td>30-40</td>
<td>16</td>
<td>44</td>
<td>35</td>
<td>7</td>
<td>112</td>
</tr>
<tr>
<td>40-50</td>
<td>4</td>
<td>48</td>
<td>45</td>
<td>17</td>
<td>68</td>
</tr>
<tr>
<td>50-60</td>
<td>2</td>
<td>50</td>
<td>55</td>
<td>27</td>
<td>54</td>
</tr>
<tr>
<td></td>
<td>50</td>
<td></td>
<td></td>
<td></td>
<td>508</td>
</tr>
</tbody>
</table>

<!-- page 423 -->
The class interval containing $\frac{\mathrm{N}^{\mathrm{th}}}{2}$ or $25^{\mathrm{th}}$ item is 20-30. Therefore, 20–30 is the median
class. We know that

$$\text{Median} = l + \frac{\frac{\text{N}}{2} - \text{C}}{f} \times h$$

Here $l = 20$, $C = 13$, $f = 15$, $h = 10$ and $N = 50$

Therefore, $\text{Median} = 20 + \frac{25 - 13}{15} \times 10 = 20 + 8 = 28$

Thus, Mean deviation about median is given by

$$\text{M.D. (M)} = \frac{1}{\text{N}} \sum_{i=1}^{6} f_i |x_i - \text{M}| = \frac{1}{50} \times 508 = 10.16$$

EXERCISE 15.1

Find the mean deviation about the mean for the data in Exercises 1 and 2.

1. $4, 7, 8, 9, 10, 12, 13, 17$
2. $38, 70, 48, 40, 42, 55, 63, 46, 54, 44$

Find the mean deviation about the median for the data in Exercises 3 and 4.

3. $13, 17, 16, 14, 11, 13, 10, 16, 11, 18, 12, 17$
4. $36, 72, 46, 42, 60, 45, 53, 46, 51, 49$

Find the mean deviation about the mean for the data in Exercises 5 and 6.

5. $x_i$ 5 10 15 20 25
$f_i$ 7 4 6 3 5
6. $x_i$ 10 30 50 70 90
$f_i$ 4 24 28 16 8

Find the mean deviation about the median for the data in Exercises 7 and 8.

7. $x_i$ 5 7 9 10 12 15
$f_i$ 8 6 2 2 2 6
8. $x_i$ 15 21 27 30 35
$f_i$ 3 5 6 7 8

<!-- page 424 -->
Find the mean deviation about the mean for the data in Exercises 9 and 10.

<table>
<thead>
<tr>
<th>Income per<br/>day in ₹</th>
<th>0-100</th>
<th>100-200</th>
<th>200-300</th>
<th>300-400</th>
<th>400-500</th>
<th>500-600</th>
<th>600-700</th>
<th>700-800</th>
</tr>
</thead>
<tbody>
<tr>
<td>Number<br/>of persons</td>
<td>4</td>
<td>8</td>
<td>9</td>
<td>10</td>
<td>7</td>
<td>5</td>
<td>4</td>
<td>3</td>
</tr>
</tbody>
</table>

10. |

<table>
<thead>
<tr>
<th>Height<br/>in cms</th>
<th>95-105</th>
<th>105-115</th>
<th>115-125</th>
<th>125-135</th>
<th>135-145</th>
<th>145-155</th>
</tr>
</thead>
<tbody>
<tr>
<td>Number of<br/>boys</td>
<td>9</td>
<td>13</td>
<td>26</td>
<td>30</td>
<td>12</td>
<td>10</td>
</tr>
</tbody>
</table>

11. Find the mean deviation about median for the following data :

<table>
<thead>
<tr>
<th>Marks</th>
<th>0-10</th>
<th>10-20</th>
<th>20-30</th>
<th>30-40</th>
<th>40-50</th>
<th>50-60</th>
</tr>
</thead>
<tbody>
<tr>
<td>Number of<br/>Girls</td>
<td>6</td>
<td>8</td>
<td>14</td>
<td>16</td>
<td>4</td>
<td>2</td>
</tr>
</tbody>
</table>

12. Calculate the mean deviation about median age for the age distribution of 100
persons given below:

<table>
<thead>
<tr>
<th>Age<br/>(in years)</th>
<th>16-20</th>
<th>21-25</th>
<th>26-30</th>
<th>31-35</th>
<th>36-40</th>
<th>41-45</th>
<th>46-50</th>
<th>51-55</th>
</tr>
</thead>
<tbody>
<tr>
<td>Number</td>
<td>5</td>
<td>6</td>
<td>12</td>
<td>14</td>
<td>26</td>
<td>12</td>
<td>16</td>
<td>9</td>
</tr>
</tbody>
</table>

[Hint Convert the given data into continuous frequency distribution by subtracting 0.5
from the lower limit and adding 0.5 to the upper limit of each class interval]

15.4.3 *Limitations of mean deviation* In a series, where the degree of variability is
very high, the median is not a representative central tendency. Thus, the mean deviation
about median calculated for such series can not be fully relied.

The sum of the deviations from the mean (minus signs ignored) is more than the
sum of the deviations from median. Therefore, the mean deviation about the mean is
not very scientific.Thus, in many cases, mean deviation may give unsatisfactory results.
Also mean deviation is calculated on the basis of absolute values of the deviations and
therefore, cannot be subjected to further algebraic treatment. This implies that we
must have some other measure of dispersion. Standard deviation is such a measure of
dispersion.

15.5 Variance and Standard Deviation

Recall that while calculating mean deviation about mean or median, the absolute values
of the deviations were taken. The absolute values were taken to give meaning to the
mean deviation, otherwise the deviations may cancel among themselves.

Another way to overcome this difficulty which arose due to the signs of deviations,
is to take squares of all the deviations. Obviously all these squares of deviations are

<!-- page 425 -->
non-negative. Let $x_1, x_2, x_3, ..., x_n$ be $n$ observations and $\bar{x}$ be their mean. Then

$$(x_1 - \bar{x})^2 + (x_2 - \bar{x})^2 + ...... + (x_n - \bar{x})^2 = \underset{i=1}{^n} (x_i - \bar{x})^2.$$

If this sum is zero, then each $(x_i - \bar{x})$ has to be zero. This implies that there is no
dispersion at all as all observations are equal to the mean $\bar{x}$ .

If $\sum_{i=1}^{n}(x_{i}-\bar{x})^{2}$ is small , this indicates that the observations $x_{1}, x_{2}, x_{3},...,x_{n}$ are
close to the mean $\bar{x}$ and therefore, there is a lower degree of dispersion. On the
contrary, if this sum is large, there is a higher degree of dispersion of the observations

from the mean $\bar{x}$ . Can we thus say that the sum $\sum_{i=1}^{n}(x_{i}-\bar{x})^{2}$ is a reasonable indicator

of the degree of dispersion or scatter?

Let us take the set A of six observations 5, 15, 25, 35, 45, 55. The mean of the
observations is $\bar{x} = 30$. The sum of squares of deviations from $\bar{x}$ for this set is

$$\sum_{i=1}^{6}(x_{i}-\bar{x})^{2}=(5-30)^{2}+(15-30)^{2}+(25-30)^{2}+(35-30)^{2}+(45-30)^{2}+(55-30)^{2}$$
$$=625+225+25+25+225+625=1750$$

Let us now take another set B of 31 observations 15, 16, 17, 18, 19, 20, 21, 22, 23,
24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45. The
mean of these observations is $\bar{y} = 30$

Note that both the sets A and B of observations have a mean of 30.

Now, the sum of squares of deviations of observations for set B from the mean $\bar{y}$ is
given by

$$\sum_{i=1}^{31} (y_i - \bar{y})^2 = (15-30)^2 + (16-30)^2 + (17-30)^2 + ... + (44-30)^2 + (45-30)^2$$
$$= (-15)^2 + (-14)^2 + ... + (-1)^2 + 0^2 + 1^2 + 2^2 + 3^2 + ... + 14^2 + 15^2$$
$$= 2 [15^2 + 14^2 + ... + 1^2]$$
$$= 2 \times \frac{15 \times (15+1) (30+1)}{6} = 5 \times 16 \times 31 = 2480$$

(Because sum of squares of first $n$ natural numbers = $\frac{n(n+1)(2n+1)}{6}$. Here $n=15$)

<!-- page 426 -->
If $\sum_{i=1}^{n}(x_{i}-\bar{x})^{2}$ is simply our measure of dispersion or scatter about mean, we

will tend to say that the set A of six observations has a lesser dispersion about the mean
than the set B of 31 observations, even though the observations in set A are more
scattered from the mean (the range of deviations being from $-25$ to $25$) than in the set
B (where the range of deviations is from $-15$ to $15$).

This is also clear from the following diagrams.

For the set A, we have

Fig 15.5

For the set B, we have

Fig 15.6

Thus, we can say that the sum of squares of deviations from the mean is not a proper
measure of dispersion. To overcome this difficulty we take the mean of the squares of

the deviations, i.e., we take $\frac{1}{n} \sum_{i=1}^{n}(x_{i}-\bar{x})^{2}$. In case of the set A, we have

Mean = $\frac{1}{6} \times 1750 = 291.67$ and in case of the set B, it is $\frac{1}{31} \times 2480 = 80$.

This indicates that the scatter or dispersion is more in set A than the scatter or dispersion
in set B, which confirms with the geometrical representation of the two sets.

Thus, we can take $\frac{1}{n} \sum (x_i - \bar{x})^2$ as a quantity which leads to a proper measure

of dispersion. This number, i.e., mean of the squares of the deviations from mean is

called the \textbf{\textit{variance}} and is denoted by $\sigma^2$ (read as sigma square). Therefore, the

variance of $n$ observations $x_1, x_2, ..., x_n$ is given by

<!-- page 427 -->
$$\sigma^2 = \frac{1}{n} \sum_{i=1}^{n} (x_i - \bar{x})^2$$

15.5.1 *Standard Deviation* In the calculation of variance, we find that the units of
individual observations $x_i$ and the unit of their mean $\bar{x}$ are different from that of variance,
since variance involves the sum of squares of $(x_i - \bar{x})$. For this reason, the proper
measure of dispersion about the mean of a set of observations is expressed as positive
square-root of the variance and is called *standard deviation*. Therefore, the standard
deviation, usually denoted by $c$, is given by

$$\sigma = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (x_i - \bar{x})^2} \dots (1)$$

Let us take the following example to illustrate the calculation of variance and
hence, standard deviation of ungrouped data.

Example 8 Find the variance of the following data:
$$6, 8, 10, 12, 14, 16, 18, 20, 22, 24$$

Solution From the given data we can form the following Table 15.7. The mean is
calculated by step-deviation method taking 14 as assumed mean. The number of
observations is $n = 10$

Table 15.7

<table>
<thead>
<tr>
<th>$x_i$</th>
<th>$d_i = \frac{x_i - 14}{2}$</th>
<th>Deviations from mean<br/>$(x_i - \bar{x})$</th>
<th>$(x_i - \bar{x})$</th>
</tr>
</thead>
<tbody>
<tr>
<td>6</td>
<td>-4</td>
<td>-9</td>
<td>81</td>
</tr>
<tr>
<td>8</td>
<td>-3</td>
<td>-7</td>
<td>49</td>
</tr>
<tr>
<td>10</td>
<td>-2</td>
<td>-5</td>
<td>25</td>
</tr>
<tr>
<td>12</td>
<td>-1</td>
<td>-3</td>
<td>9</td>
</tr>
<tr>
<td>14</td>
<td>0</td>
<td>-1</td>
<td>1</td>
</tr>
<tr>
<td>16</td>
<td>1</td>
<td>1</td>
<td>1</td>
</tr>
<tr>
<td>18</td>
<td>2</td>
<td>3</td>
<td>9</td>
</tr>
<tr>
<td>20</td>
<td>3</td>
<td>5</td>
<td>25</td>
</tr>
<tr>
<td>22</td>
<td>4</td>
<td>7</td>
<td>49</td>
</tr>
<tr>
<td>24</td>
<td>5</td>
<td>9</td>
<td>81</td>
</tr>
</tbody>
<tfoot>
<tr>
<td></td>
<td>5</td>
<td></td>
<td>330</td>
</tr>
</tfoot>
</table>

<!-- page 428 -->
Therefore $\text{Mean } \bar{x} = \text{assumed mean} + \frac{\sum_{i=1}^{n} d_i}{n} \times h = 14 + \frac{5}{10} \times 2 = 15$

and $\qquad \text{Variance } (\sigma^2) = \frac{1}{n} \sum_{i=1}^{10} (x_i - \bar{x})^2 = \frac{1}{10} \times 330 = 33$

Thus Standard deviation ( $\sigma$ ) = $\sqrt{33} = 5.74$

15.5.2 *Standard deviation of a discrete frequency distribution* Let the given discrete
frequency distribution be

$x: \quad x_1, \quad x_2, \quad x_3, \dots, x_n$
$f: \quad f_1, \quad f_2, \quad f_3, \dots, f_n$

In this case standard deviation $(\sigma) = \sqrt{\frac{1}{\mathrm{N}} \sum_{i=1}^{n} f_{i}(x_{i} - \bar{x})^{2}}$ ... (2)

where $N = \sum_{i=1}^{n} f_i$.

Let us take up following example.

Example 9 Find the variance and standard deviation for the following data:

<table>
<thead>
<tr>
<th>$x_i$</th>
<th>4</th>
<th>8</th>
<th>11</th>
<th>17</th>
<th>20</th>
<th>24</th>
<th>32</th>
</tr>
</thead>
<tbody>
<tr>
<td>$f_i$</td>
<td>3</td>
<td>5</td>
<td>9</td>
<td>5</td>
<td>4</td>
<td>3</td>
<td>1</td>
</tr>
</tbody>
</table>

Solution Presenting the data in tabular form (Table 15.8), we get

Table 15.8

<table>
<thead>
<tr>
<th>$x_i$</th>
<th>$f_i$</th>
<th>$f_i x_i$</th>
<th>$x_i - \bar{x}$</th>
<th>$(x_i - \bar{x})^2$</th>
<th>$f_i(x_i - \bar{x})^2$</th>
</tr>
</thead>
<tbody>
<tr>
<td>4</td>
<td>3</td>
<td>12</td>
<td>-10</td>
<td>100</td>
<td>300</td>
</tr>
<tr>
<td>8</td>
<td>5</td>
<td>40</td>
<td>-6</td>
<td>36</td>
<td>180</td>
</tr>
<tr>
<td>11</td>
<td>9</td>
<td>99</td>
<td>-3</td>
<td>9</td>
<td>81</td>
</tr>
<tr>
<td>17</td>
<td>5</td>
<td>85</td>
<td>3</td>
<td>9</td>
<td>45</td>
</tr>
<tr>
<td>20</td>
<td>4</td>
<td>80</td>
<td>6</td>
<td>36</td>
<td>144</td>
</tr>
<tr>
<td>24</td>
<td>3</td>
<td>72</td>
<td>10</td>
<td>100</td>
<td>300</td>
</tr>
<tr>
<td>32</td>
<td>1</td>
<td>32</td>
<td>18</td>
<td>324</td>
<td>324</td>
</tr>
</tbody>
<tfoot>
<tr>
<td></td>
<td>30</td>
<td>420</td>
<td></td>
<td></td>
<td>1374</td>
</tr>
</tfoot>
</table>

<!-- page 429 -->
$$\mathrm{N} = 30, \sum_{i=1}^{7} f_i x_i = 420, \sum_{i=1}^{7} f_i (x_i - \bar{x})^2 = 1374$$

Therefore $$\bar{x} = \frac{\sum_{i=1}^{7} f_i x_i}{\text{N}} = \frac{1}{30} \times 420 = 14$$

Hence $\text{variance } (\sigma^2) = \frac{1}{\text{N}} \sum_{i=1}^7 f_i(x_i - \bar{x})^2$

$$= \frac{1}{30} \times 1374 = 45.8$$

and Standard deviation $(\sigma)=\sqrt{45.8}=6.77$

15.5.3 *Standard deviation of a continuous frequency distribution* The given
continuous frequency distribution can be represented as a discrete frequency distribution
by replacing each class by its mid-point. Then, the standard deviation is calculated by
the technique adopted in the case of a discrete frequency distribution.

If there is a frequency distribution of $n$ classes each class defined by its mid-point
$x_i$ with frequency $f_i$, the standard deviation will be obtained by the formula

$$\sigma = \sqrt{\frac{1}{N} \sum_{i=1}^{n} f_i(x_i - \bar{x})^2},$$

where $\bar{x}$ is the mean of the distribution and $\mathrm{N}=\sum_{i=1}^{n} f_{i}$.

Another formula for standard deviation We know that

$$\text{Variance } (\sigma^2) = \frac{1}{N} \sum_{i=1}^n f_i(x_i - \bar{x})^2 = \frac{1}{N} \sum_{i=1}^n f_i(x_i^2 + \bar{x}^2 - 2\bar{x} x_i)$$

$$= \frac{1}{N} \left[ \sum_{i=1}^n f_i x_i^2 + \sum_{i=1}^n \bar{x}^2 f_i - \sum_{i=1}^n 2\bar{x} f_i x_i \right]$$

$$= \frac{1}{N} \left[ \sum_{i=1}^n f_i x_i^2 + \bar{x}^2 \sum_{i=1}^n f_i - 2\bar{x} \sum_{i=1}^n x_i f_i \right]$$

<!-- page 430 -->
$$= \frac{1}{\mathrm{N}} \sum_{i=1}^{n} f_i x_i^2 + \bar{x}^2 \mathrm{N} - 2\bar{x} \cdot \mathrm{N} \bar{x} \quad \left[ \text{Here } \frac{1}{\mathrm{N}} \sum_{i=1}^{n} x_i f_i = \bar{x} \text{ or } \sum_{i=1}^{n} x_i f_i = \mathrm{N} \bar{x} \right]$$

$$= \frac{1}{N} \sum_{i=1}^{n} f_i x_i^2 + \bar{x}^2 - 2\bar{x}^2 = \frac{1}{N} \sum_{i=1}^{n} f_i x_i^2 - \bar{x}^2$$

or $\quad \sigma^{2}=\frac{1}{\mathrm{N}} \sum_{i-1}^{n} f_{i} x_{i}^{2}-\left(\frac{\sum_{i=1}^{n} f_{i} x_{i}}{\mathrm{N}}\right)^{2}=\frac{1}{\mathrm{N}^{2}}\left[\mathrm{N} \sum_{i=1}^{n} f_{i} x_{i}^{2}-\left(\sum_{i=1}^{n} f_{i} x_{i}\right)^{2}\right]$

Thus, standard deviation $(\sigma)=\frac{1}{\mathrm{N}} \sqrt{\mathrm{N} \sum_{i=1}^{n} f_{i} x_{i}^{2}-\left(\sum_{i=1}^{n} f_{i} x_{i}\right)^{2}}$ ... (3)

Example 10 Calculate the mean, variance and standard deviation for the following
distribution :

<table>
<thead>
<tr>
<th>Class</th>
<th>30-40</th>
<th>40-50</th>
<th>50-60</th>
<th>60-70</th>
<th>70-80</th>
<th>80-90</th>
<th>90-100</th>
</tr>
</thead>
<tbody>
<tr>
<td>Frequency</td>
<td>3</td>
<td>7</td>
<td>12</td>
<td>15</td>
<td>8</td>
<td>3</td>
<td>2</td>
</tr>
</tbody>
</table>

Solution From the given data, we construct the following Table 15.9.

Table 15.9

<table>
<thead>
<tr>
<th>Class</th>
<th>Frequency<br/>($f_i$)</th>
<th>Mid-point<br/>($x_i$)</th>
<th>$f_i x_i$</th>
<th>$(x_i - \bar{x})^2$</th>
<th>$f_i (x_i - \bar{x})^2$</th>
</tr>
</thead>
<tbody>
<tr>
<td>30-40</td>
<td>3</td>
<td>35</td>
<td>105</td>
<td>729</td>
<td>2187</td>
</tr>
<tr>
<td>40-50</td>
<td>7</td>
<td>45</td>
<td>315</td>
<td>289</td>
<td>2023</td>
</tr>
<tr>
<td>50-60</td>
<td>12</td>
<td>55</td>
<td>660</td>
<td>49</td>
<td>588</td>
</tr>
<tr>
<td>60-70</td>
<td>15</td>
<td>65</td>
<td>975</td>
<td>9</td>
<td>135</td>
</tr>
<tr>
<td>70-80</td>
<td>8</td>
<td>75</td>
<td>600</td>
<td>169</td>
<td>1352</td>
</tr>
<tr>
<td>80-90</td>
<td>3</td>
<td>85</td>
<td>255</td>
<td>529</td>
<td>1587</td>
</tr>
<tr>
<td>90-100</td>
<td>2</td>
<td>95</td>
<td>190</td>
<td>1089</td>
<td>2178</td>
</tr>
<tr>
<td></td>
<td>50</td>
<td></td>
<td>3100</td>
<td></td>
<td>10050</td>
</tr>
</tbody>
</table>

<!-- page 431 -->
Thus $\text{Mean } \bar{x} = \frac{1}{\text{N}} \sum_{i=1}^{7} f_i x_i = \frac{3100}{50} = 62$


$\text{Variance } (\sigma^2) = \frac{1}{\text{N}} \sum_{i=1}^{7} f_i (x_i - \bar{x})^2$


$= \frac{1}{50} \times 10050 = 201$


and $\text{Standard deviation } (\sigma) = \sqrt{201} = 14.18$

Example 11 Find the standard deviation for the following data :

<table>
  <tbody>
    <tr>
      <td>$x_i$</td>
      <td>3</td>
      <td>8</td>
      <td>13</td>
      <td>18</td>
      <td>23</td>
    </tr>
    <tr>
      <td>$f_i$</td>
      <td>7</td>
      <td>10</td>
      <td>15</td>
      <td>10</td>
      <td>6</td>
    </tr>
  </tbody>
</table>

Solution Let us form the following Table 15.10:

Table 15.10

<table>
<thead>
<tr>
<th>$x_i$</th>
<th>$f_i$</th>
<th>$f_i x_i$</th>
<th>$x_i^2$</th>
<th>$f_i x_i^2$</th>
</tr>
</thead>
<tbody>
<tr>
<td>3</td>
<td>7</td>
<td>21</td>
<td>9</td>
<td>63</td>
</tr>
<tr>
<td>8</td>
<td>10</td>
<td>80</td>
<td>64</td>
<td>640</td>
</tr>
<tr>
<td>13</td>
<td>15</td>
<td>195</td>
<td>169</td>
<td>2535</td>
</tr>
<tr>
<td>18</td>
<td>10</td>
<td>180</td>
<td>324</td>
<td>3240</td>
</tr>
<tr>
<td>23</td>
<td>6</td>
<td>138</td>
<td>529</td>
<td>3174</td>
</tr>
<tr>
<td></td>
<td>48</td>
<td>614</td>
<td></td>
<td>9652</td>
</tr>
</tbody>
</table>

Now, by formula (3), we have

$$\sigma = \frac{1}{N} \sqrt{N \sum f_i x_i^2 - \left( \sum f_i x_i \right)^2}$$

$$= \frac{1}{48} \sqrt{48 \times 9652 - (614)^2}$$

$$= \frac{1}{48} \sqrt{463296 - 376996}$$

<!-- page 432 -->
$$= \frac{1}{48} \times 293.77 = 6.12$$

Therefore, Standard deviation ( $c$ ) = 6.12

15.5.4. *Shortcut method to find variance and standard deviation* Sometimes the
values of $x_i$ in a discrete distribution or the mid points $x_i$ of different classes in a
continuous distribution are large and so the calculation of mean and variance becomes
tedious and time consuming. By using step-deviation method, it is possible to simplify
the procedure.

Let the assumed mean be ‘A’ and the scale be reduced to $\frac{1}{h}$ times ($h$ being the
width of class-intervals). Let the step-deviations or the new values be $y_i$.

i.e. $y_i = \frac{x_i - A}{h}$ or $x_i = A + hy_i$ ... (1)

$$\text{We know that} \qquad \bar{x} = \frac{\sum_{i=1}^{n} f_i x_i}{N} \qquad \dots (2)$$

Replacing $x_i$ from (1) in (2), we get

$$\overline{x} = \frac{\sum_{i=1}^{n} f_i (\text{A} + h y_i)}{\text{N}}$$

$$= \frac{1}{\mathrm{N}} \left( \sum_{i=1}^{n} f_i \mathrm{A} + \sum_{i=1}^{n} h f_i y_i \right) = \frac{1}{\mathrm{N}} \left( \mathrm{A} \sum_{i=1}^{n} f_i + h \sum_{i=1}^{n} f_i y_i \right)$$

$$= A \cdot \frac{N}{N} + h \frac{\sum_{i=1}^{n} f_i y_i}{N} \quad \left( \text{because } \sum_{i=1}^{n} f_i = N \right)$$

Thus $\quad \bar{x} = A + h \quad \bar{y} \quad \dots (3)$

Now $\quad \text{Variance of the variable } x, \quad \sigma_x^2 = \frac{1}{\text{N}} \sum_{i=1}^n f_i(x_i - \bar{x})^2$

$$= \frac{1}{N} \sum_{i=1}^{n} f_{i} (\mathrm{A} + h y_{i} - \mathrm{A} - h \bar{y})^{2} \qquad \text{(Using (1) and (3))}$$

<!-- page 433 -->
$$= \frac{1}{N} \sum_{i=1}^{n} f_i h^2 (y_i - \bar{y})^2$$

$$= \frac{h^2}{N} \sum_{i=1}^{n} f_i (y_i - \overline{y})^2 = h^2 \times \text{variance of the variable } y_i$$

i.e. $\sigma_x^2 = h^2 \sigma_y^2$

or $\qquad \sigma_x = h\sigma_y \qquad \dots (4)$

From (3) and (4), we have

$$\sigma_x = \frac{h}{\mathrm{N}} \sqrt{\mathrm{N} \sum_{i=1}^n f_i y_i^2 - \left( \sum_{i=1}^n f_i y_i \right)^2} \dots (5)$$

Let us solve Example 11 by the short-cut method and using formula (5)

Examples 12 Calculate mean, variance and standard deviation for the following
distribution.

<table>
<thead>
<tr>
<th>Classes</th>
<th>30-40</th>
<th>40-50</th>
<th>50-60</th>
<th>60-70</th>
<th>70-80</th>
<th>80-90</th>
<th>90-100</th>
</tr>
</thead>
<tbody>
<tr>
<td>Frequency</td>
<td>3</td>
<td>7</td>
<td>12</td>
<td>15</td>
<td>8</td>
<td>3</td>
<td>2</td>
</tr>
</tbody>
</table>

Solution Let the assumed mean A = 65. Here $h = 10$
We obtain the following Table 15.11 from the given data :

Table 15.11

<table>
<thead>
<tr>
<th>Class</th>
<th>Frequency</th>
<th>Mid-point</th>
<th>$y_i = \frac{x_i - 65}{10}$</th>
<th>$y_i^2$</th>
<th>$f_i y_i$</th>
<th>$f_i y_i^2$</th>
</tr>
</thead>
<tbody>
<tr>
<td></td>
<td>$f_i$</td>
<td>$x_i$</td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>30-40</td>
<td>3</td>
<td>35</td>
<td>- 3</td>
<td>9</td>
<td>- 9</td>
<td>27</td>
</tr>
<tr>
<td>40-50</td>
<td>7</td>
<td>45</td>
<td>- 2</td>
<td>4</td>
<td>- 14</td>
<td>28</td>
</tr>
<tr>
<td>50-60</td>
<td>12</td>
<td>55</td>
<td>- 1</td>
<td>1</td>
<td>- 12</td>
<td>12</td>
</tr>
<tr>
<td>60-70</td>
<td>15</td>
<td>65</td>
<td>0</td>
<td>0</td>
<td>0</td>
<td>0</td>
</tr>
<tr>
<td>70-80</td>
<td>8</td>
<td>75</td>
<td>1</td>
<td>1</td>
<td>8</td>
<td>8</td>
</tr>
<tr>
<td>80-90</td>
<td>3</td>
<td>85</td>
<td>2</td>
<td>4</td>
<td>6</td>
<td>12</td>
</tr>
<tr>
<td>90-100</td>
<td>2</td>
<td>95</td>
<td>3</td>
<td>9</td>
<td>6</td>
<td>18</td>
</tr>
<tr>
<td></td>
<td>N=50</td>
<td></td>
<td></td>
<td></td>
<td>- 15</td>
<td>105</td>
</tr>
</tbody>
</table>

<!-- page 434 -->
Therefore $\bar{x} = A + \frac{\sum f_i y_i}{50} \times h = 65 - \frac{15}{50} \times 10 = 62$

$$\text{Variance} \qquad \sigma^2 = \frac{h^2}{\text{N}^2} \left[ \text{N} \Sigma f_i y_i^2 - \left( \Sigma f_i y_i \right)^2 \right]$$

$$= \frac{(10)^2}{(50)^2} \left[ 50 \times 105 - (-15)^2 \right]$$

$$= \frac{1}{25}[5250 - 225] = 201$$

and standard deviation $(\sigma)=\sqrt{201}=14.18$

EXERCISE 15.2

Find the mean and variance for each of the data in Exercises 1 to 5.

1. $6, 7, 10, 12, 13, 4, 8, 12$
2. First $n$ natural numbers
3. First 10 multiples of 3
4. $\begin{array}{|c|c|c|c|c|c|c|c|} \hline x_i & 6 & 10 & 14 & 18 & 24 & 28 & 30 \\ \hline f_i & 2 & 4 & 7 & 12 & 8 & 4 & 3 \\ \hline \end{array}$

5. $\begin{array}{|c|c|c|c|c|c|c|c|} \hline x_i & 92 & 93 & 97 & 98 & 102 & 104 & 109 \\ \hline f_i & 3 & 2 & 3 & 2 & 6 & 3 & 3 \\ \hline \end{array}$

6. Find the mean and standard deviation using short-cut method.
$\begin{array}{|c|c|c|c|c|c|c|c|c|} \hline x_i & 60 & 61 & 62 & 63 & 64 & 65 & 66 & 67 & 68 \\ \hline f_i & 2 & 1 & 12 & 29 & 25 & 12 & 10 & 4 & 5 \\ \hline \end{array}$

Find the mean and variance for the following frequency distributions in Exercises
7 and 8.

7.

<table>
<thead>
<tr>
<th>Classes</th>
<th>0-30</th>
<th>30-60</th>
<th>60-90</th>
<th>90-120</th>
<th>120-150</th>
<th>150-180</th>
<th>180-210</th>
</tr>
</thead>
<tbody>
<tr>
<td>Frequencies</td>
<td>2</td>
<td>3</td>
<td>5</td>
<td>10</td>
<td>3</td>
<td>5</td>
<td>2</td>
</tr>
</tbody>
</table>

<!-- page 435 -->
8.

<table>
<thead>
<tr>
<th>Classes</th>
<th>0-10</th>
<th>10-20</th>
<th>20-30</th>
<th>30-40</th>
<th>40-50</th>
</tr>
</thead>
<tbody>
<tr>
<td>Frequencies</td>
<td>5</td>
<td>8</td>
<td>15</td>
<td>16</td>
<td>6</td>
</tr>
</tbody>
</table>

9. Find the mean, variance and standard deviation using short-cut method

<table>
<thead>
<tr>
<th>Height<br/>in cms</th>
<th>70-75</th>
<th>75-80</th>
<th>80-85</th>
<th>85-90</th>
<th>90-95</th>
<th>95-100</th>
<th>100-105</th>
<th>105-110</th>
<th>110-115</th>
</tr>
</thead>
<tbody>
<tr>
<td>No. of<br/>children</td>
<td>3</td>
<td>4</td>
<td>7</td>
<td>7</td>
<td>15</td>
<td>9</td>
<td>6</td>
<td>6</td>
<td>3</td>
</tr>
</tbody>
</table>

10. The diameters of circles (in mm) drawn in a design are given below:

<table>
<thead>
<tr>
<th>Diameters</th>
<th>33-36</th>
<th>37-40</th>
<th>41-44</th>
<th>45-48</th>
<th>49-52</th>
</tr>
</thead>
<tbody>
<tr>
<td>No. of circles</td>
<td>15</td>
<td>17</td>
<td>21</td>
<td>22</td>
<td>25</td>
</tr>
</tbody>
</table>

Calculate the standard deviation and mean diameter of the circles.

[ Hint First make the data continuous by making the classes as 32.5-36.5, 36.5-40.5,
40.5-44.5, 44.5 - 48.5, 48.5 - 52.5 and then proceed.]

15.6 Analysis of Frequency Distributions

In earlier sections, we have studied about some types of measures of dispersion. The
mean deviation and the standard deviation have the same units in which the data are
given. Whenever we want to compare the variability of two series with same mean,
which are measured in different units, we do not merely calculate the measures of
dispersion but we require such measures which are independent of the units. The
measure of variability which is independent of units is called coefficient of variation
(denoted as C.V.)

The coefficient of variation is defined as

$$\text{C.V.} = \frac{\sigma}{\bar{x}} \times 100 \ , \ \bar{x} \neq 0,$$

where $\sigma$ and $\overline{x}$ are the standard deviation and mean of the data.

For comparing the variability or dispersion of two series, we calculate the coefficient
of variance for each series. The series having greater C.V. is said to be more variable
than the other. The series having lesser C.V. is said to be more consistent than the
other.

<!-- page 436 -->
15.6.1 Comparison of two frequency distributions with same mean Let $\bar{x}_1$ and $\sigma_1$

be the mean and standard deviation of the first distribution, and $\bar{x}_2$ and $\sigma_2$ be the
mean and standard deviation of the second distribution.

Then C.V. (1st distribution) = $\frac{\sigma_1}{\bar{x}_1} \times 100$

and C.V. (2nd distribution) = $\frac{\sigma_2}{\bar{x}_2} \times 100$

Given $\bar{x}_1 = \bar{x}_2 = \bar{x}$ (say)

Therefore $\quad$ C.V. (1st distribution) $= \frac{\sigma_1}{\bar{x}} \times 100 \quad \dots (1)$

and C.V. (2nd distribution) $= \frac{\sigma_2}{\bar{x}} \times 100$ ... (2)

It is clear from (1) and (2) that the two C.Vs. can be compared on the basis of values
of $\sigma_1$ and $\sigma_2$ only.

Thus, we say that for two series with equal means, the series with greater standard
deviation (or variance) is called more variable or dispersed than the other. Also, the
series with lesser value of standard deviation (or variance) is said to be more consistent
than the other.

Let us now take following examples:

Example 13 Two plants A and B of a factory show following results about the number
of workers and the wages paid to them.

<table>
<tr>
<td></td>
<td>A</td>
<td>B</td>
</tr>
<tr>
<td>No. of workers</td>
<td>5000</td>
<td>6000</td>
</tr>
<tr>
<td>Average monthly wages</td>
<td>Rs 2500</td>
<td>Rs 2500</td>
</tr>
<tr>
<td>Variance of distribution
of wages</td>
<td>81</td>
<td>100</td>
</tr>
</table>

In which plant, A or B is there greater variability in individual wages?

Solution The variance of the distribution of wages in plant A ( $\sigma_1^2$ ) = 81

Therefore, standard deviation of the distribution of wages in plant A ( $\sigma_1$ ) = 9

<!-- page 437 -->
Also, the variance of the distribution of wages in plant B ( $\sigma_2^2$ ) = 100

Therefore, standard deviation of the distribution of wages in plant B ( $\sigma_2$ ) = 10

Since the average monthly wages in both the plants is same, i.e., Rs.2500, therefore,
the plant with greater standard deviation will have more variability.
Thus, the plant B has greater variability in the individual wages.

Example 14 Coefficient of variation of two distributions are 60 and 70, and their
standard deviations are 21 and 16, respectively. What are their arithmetic means.

Solution Given
C.V. (1st distribution) = 60, $\sigma_1 = 21$

C.V. (2nd distribution) = 70, $\sigma_2 = 16$

Let $\bar{x}_1$ and $\bar{x}_2$ be the means of 1st and 2nd distribution, respectively. Then

$$\text{C.V. (1st distribution)} = \frac{C_1}{\bar{x}_1} \times 100$$

Therefore $60 = \frac{21}{\bar{x}_1} \times 100$ or $\bar{x}_1 = \frac{21}{60} \times 100 = 35$

and C.V. (2nd distribution) = $\frac{C_2}{\bar{x}_2} \times 100$

i.e. $70 = \frac{16}{\bar{x}_2} \times 100$ or $\bar{x}_2 = \frac{16}{70} \times 100 = 22.85$

Example 15 The following values are calculated in respect of heights and weights of
the students of a section of Class XI :
<table>
<tr>
<td></td>
<td>Height</td>
<td>Weight</td>
</tr>
<tr>
<td>Mean</td>
<td>162.6 cm</td>
<td>52.36 kg</td>
</tr>
<tr>
<td>Variance</td>
<td>127.69 cm$^2$</td>
<td>23.1361 kg$^2$</td>
</tr>
</table>
Can we say that the weights show greater variation than the heights?
Solution To compare the variability, we have to calculate their coefficients of variation.
Given Variance of height = 127.69cm$^2$
Therefore Standard deviation of height = $\sqrt{127.69}$ cm = 11.3 cm
Also Variance of weight = 23.1361 kg$^2$

<!-- page 438 -->
Therefore Standard deviation of weight = $\sqrt{23.1361}$ kg = 4.81 kg
Now, the coefficient of variations (C.V.) are given by

$$\text{(C.V.) in heights} = \frac{\text{Standard Deviation}}{\text{Mean}} \times 100$$

$$= \frac{11.3}{162.6} \times 100 = 6.95$$

and (C.V.) in weights = $\frac{4.81}{52.36} \times 100 = 9.18$

Clearly C.V. in weights is greater than the C.V. in heights
Therefore, we can say that weights show more variability than heights.

EXERCISE 15.3

1. From the data given below state which group is more variable, A or B?

<table>
<thead>
<tr>
<th>Marks</th>
<th>10-20</th>
<th>20-30</th>
<th>30-40</th>
<th>40-50</th>
<th>50-60</th>
<th>60-70</th>
<th>70-80</th>
</tr>
</thead>
<tbody>
<tr>
<td>Group A</td>
<td>9</td>
<td>17</td>
<td>32</td>
<td>33</td>
<td>40</td>
<td>10</td>
<td>9</td>
</tr>
<tr>
<td>Group B</td>
<td>10</td>
<td>20</td>
<td>30</td>
<td>25</td>
<td>43</td>
<td>15</td>
<td>7</td>
</tr>
</tbody>
</table>

2. From the prices of shares X and Y below, find out which is more stable in value:

<table>
<tbody>
<tr>
<td>X</td>
<td>35</td>
<td>54</td>
<td>52</td>
<td>53</td>
<td>56</td>
<td>58</td>
<td>52</td>
<td>50</td>
<td>51</td>
<td>49</td>
</tr>
<tr>
<td>Y</td>
<td>108</td>
<td>107</td>
<td>105</td>
<td>105</td>
<td>106</td>
<td>107</td>
<td>104</td>
<td>103</td>
<td>104</td>
<td>101</td>
</tr>
</tbody>
</table>

3. An analysis of monthly wages paid to workers in two firms A and B, belonging to
the same industry, gives the following results:

<table>
<thead>
<tr>
<th></th>
<th>Firm A</th>
<th>Firm B</th>
</tr>
</thead>
<tbody>
<tr>
<td>No. of wage earners</td>
<td>586</td>
<td>648</td>
</tr>
<tr>
<td>Mean of monthly wages</td>
<td>Rs 5253</td>
<td>Rs 5253</td>
</tr>
<tr>
<td>Variance of the distribution</td>
<td>100</td>
<td>121</td>
</tr>
</tbody>
</table>

of wages

(i) Which firm A or B pays larger amount as monthly wages?

(ii) Which firm, A or B, shows greater variability in individual wages?

<!-- page 439 -->
4. The following is the record of goals scored by team A in a football session:

<table>
<thead>
<tr>
<th>No. of goals scored</th>
<th>0</th>
<th>1</th>
<th>2</th>
<th>3</th>
<th>4</th>
</tr>
</thead>
<tbody>
<tr>
<td>No. of matches</td>
<td>1</td>
<td>9</td>
<td>7</td>
<td>5</td>
<td>3</td>
</tr>
</tbody>
</table>

For the team B, mean number of goals scored per match was 2 with a standard
deviation 1.25 goals. Find which team may be considered more consistent?

5. The sum and sum of squares corresponding to length $x$ (in cm) and weight $y$
(in gm) of 50 plant products are given below:

$$\sum_{i=1}^{50} x_i = 212 \text{ , } \sum_{i=1}^{50} x_i^2 = 902.8 \text{ , } \sum_{i=1}^{50} y_i = 261 \text{ , } \sum_{i=1}^{50} y_i^2 = 1457.6$$

Which is more varying, the length or weight?

Miscellaneous Examples

Example 16 The variance of 20 observations is 5. If each observation is multiplied by
2, find the new variance of the resulting observations.

Solution Let the observations be $x_1, x_2, ..., x_{20}$ and $\overline{x}$ be their mean. Given that
variance $= 5$ and $n = 20$. We know that

$$\text{Variance} \left( \sigma^2 \right) = \frac{1}{n} \sum_{i=1}^{20} (x_i - \bar{x})^2 \text{ , i.e., } 5 = \frac{1}{20} \sum_{i=1}^{20} (x_i - \bar{x})^2$$

or $$\sum_{i=1}^{20}(x_i - \bar{x})^2 = 100 \quad \dots (1)$$

If each observation is multiplied by 2, and the new resulting observations are $y_i$, then

$$y_i = 2x_i \text{ i.e., } x_i = \frac{1}{2} y_i$$

Therefore $$\bar{y} = \frac{1}{n} \sum_{i=1}^{20} y_i = \frac{1}{20} \sum_{i=1}^{20} 2x_i = 2 \cdot \frac{1}{20} \sum_{i=1}^{20} x_i$$

i.e. $\bar{y}=2\bar{x}$ or $\bar{x}=\frac{1}{2}\bar{y}$

Substituting the values of $x_i$ and $\overline{x}$ in (1), we get

<!-- page 440 -->
$$\sum_{i=1}^{20}\left(\frac{1}{2}y_{i}-\frac{1}{2}\bar{y}\right)^{2}=100,\text{ i.e., }\sum_{i=1}^{20}(y_{i}-\bar{y})^{2}=400$$

Thus the variance of new observations $= \frac{1}{20} \times 400 = 20 = 2^2 \times 5$

Note The reader may note that if each observation is multiplied by a constant
$k$, the variance of the resulting observations becomes $k^2$ times the original variance.

Example17 The mean of 5 observations is 4.4 and their variance is 8.24. If three of
the observations are 1, 2 and 6, find the other two observations.

Solution Let the other two observations be $x$ and $y$.
Therefore, the series is $1, 2, 6, x, y$.

$$\text{Now} \quad \text{Mean } \bar{x} = 4.4 = \frac{1 + 2 + 6 + x + y}{5}$$

or $22 = 9 + x + y$
Therefore $x + y = 13$ ... (1)

Also $\text{variance} = 8.24 = \frac{1}{n} \sum_{i=1}^{5} (x_i - \bar{x})^2$

i.e. $8.24 = \frac{1}{5} \left[ (3.4)^2 + (2.4)^2 + (1.6)^2 + x^2 + y^2 - 2 \times 4.4 (x + y) + 2 \times (4.4)^2 \right]$

or $41.20 = 11.56 + 5.76 + 2.56 + x^2 + y^2 - 8.8 \times 13 + 38.72$

Therefore $x^2 + y^2 = 97$ ... (2)

But from (1), we have

But from (1), we have
$$x^2 + y^2 + 2xy = 169 \qquad \dots (3)$$

From (2) and (3), we have
$$2xy = 72 \qquad \dots (4)$$

Subtracting (4) from (2), we get

Subtracting (4) from (2), we get
$$x^2 + y^2 - 2xy = 97 - 72 \text{ i.e. } (x - y)^2 = 25$$
or
$$x - y = \pm 5$$

... (5)

So, from (1) and (5), we get

$x=9, y=4$ when $x-y=5$

or $x=4$, $y=9$ when $x-y=-5$

Thus, the remaining observations are 4 and 9.

Example 18 If each of the observation $x_1, x_2, ..., x_n$ is increased by '$a$', where $a$ is a
negative or positive number, show that the variance remains unchanged.

<!-- page 441 -->
Solution Let $\bar{x}$ be the mean of $x_1, x_2, ..., x_n$. Then the variance is given by

$$\sigma_1^2 = \frac{1}{n} \sum_{i=1}^n (x_i - \bar{x})^2$$

If '$a$ is added to each observation, the new observations will be

$$y_i = x_i + a \quad ... \quad (1)$$

Let the mean of the new observations be $\bar{y}$. Then

$$\bar{y} = \frac{1}{n} \sum_{i=1}^{n} y_i = \frac{1}{n} \sum_{i=1}^{n} (x_i + a)$$

$$= \frac{1}{n} \left[ \sum_{i=1}^{n} x_i + \sum_{i=1}^{n} a \right] = \frac{1}{n} \sum_{i=1}^{n} x_i + \frac{na}{n} = \bar{x} + a$$

i.e. $\qquad \qquad \qquad \bar{y} = \bar{x} + a \qquad \qquad \qquad \dots (2)$

Thus, the variance of the new observations

$$\sigma_2^2 = \frac{1}{n} \sum_{i=1}^n (y_i - \bar{y})^2 = \frac{1}{n} \sum_{i=1}^n (x_i + a - \bar{x} - a)^2 \quad \text{[Using (1) and (2)]}$$

$$= \frac{1}{n} \sum_{i=1}^{n} (x_i - \bar{x})^2 = \sigma_1^2$$

Thus, the variance of the new observations is same as that of the original observations.

Note We may note that adding (or subtracting) a positive number to (or from)
each observation of a group does not affect the variance.

Example 19 The mean and standard deviation of 100 observations were calculated as
40 and 5.1, respectively by a student who took by mistake 50 instead of 40 for one
observation. What are the correct mean and standard deviation?

Solution Given that number of observations $(n) = 100$

$$Incorrect \text{ mean } (\bar{x}) = 40,$$
$$Incorrect \text{ standard deviation } (\sigma) = 5.1$$

We know that $$\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i$$

i.e. $$\begin{aligned} 40 &= \frac{1}{100} \sum_{i=1}^{100} x_i \quad \text{or} \quad \sum_{i=1}^{100} x_i = 4000 \end{aligned}$$

<!-- page 442 -->
$$i.e.          Incorrect sum of observations = 4000$$

$$Thus the correct sum of observations = Incorrect sum – 50 + 40 \\ = 4000 – 50 + 40 = 3990$$

Hence $\text{Correct mean} = \frac{\text{correct sum}}{100} = \frac{3990}{100} = 39.9$

Also $\text{Standard deviation } \sigma = \sqrt{\frac{1}{n} \sum_{i=1}^{n} x_{i}^{2} - \frac{1}{n^{2}} \left( \sum_{i=1}^{n} x_{i} \right)^{2}}$

$$= \sqrt{\frac{1}{n} \sum_{i=1}^{n} x_{i}^{2} - (\bar{x})^{2}}$$

i.e. $5.1 = \sqrt{\frac{1}{100} \times \text{Incorrect } \sum_{i=1}^{n} x_i^2 - (40)^2}$

or $26.01 = \frac{1}{100} \times \text{Incorrect } \sum_{i=1}^{n} x_i^2 - 1600$

Therefore $\qquad \text{Incorrect } \sum_{i=1}^{n} x_{i}^{2} = 100 (26.01 + 1600) = 162601$

Now $\qquad \qquad \qquad$ Correct $\sum_{i=1}^{n} {x_i}^2 = \text{Incorrect } \sum_{i=1}^{n} {x_i}^2 - (50)^2 + (40)^2$
$\qquad \qquad \qquad \qquad \qquad \quad = 162601 - 2500 + 1600 = 161701$

Therefore Correct standard deviation

$$= \sqrt{\frac{\text{Correct } \sum x_i^2}{n} - (\text{Correct mean})^2}$$

$$= \sqrt{\frac{161701}{100} - (39.9)^2}$$

$$= \sqrt{1617.01 - 1592.01} = \sqrt{25} = 5$$

<!-- page 443 -->
Miscellaneous Exercise On Chapter 15

1. The mean and variance of eight observations are 9 and 9.25, respectively. If six
of the observations are 6, 7, 10, 12, 12 and 13, find the remaining two observations.
2. The mean and variance of 7 observations are 8 and 16, respectively. If five of the
observations are 2, 4, 10, 12, 14. Find the remaining two observations.
3. The mean and standard deviation of six observations are 8 and 4, respectively. If
each observation is multiplied by 3, find the new mean and new standard deviation
of the resulting observations.
4. Given that $\bar{x}$ is the mean and $\sigma^2$ is the variance of $n$ observations $x_1, x_2, ..., x_n$.
Prove that the mean and variance of the observations $ax_1, ax_2, ax_3, ...., ax_n$ are
$a \bar{x}$ and $a^2 \sigma^2$, respectively, $(a \neq 0)$.
5. The mean and standard deviation of 20 observations are found to be 10 and 2,
respectively. On rechecking, it was found that an observation 8 was incorrect.
Calculate the correct mean and standard deviation in each of the following cases:
(i) If wrong item is omitted. (ii) If it is replaced by 12.
6. The mean and standard deviation of marks obtained by 50 students of a class in
three subjects, Mathematics, Physics and Chemistry are given below:

<table>
<thead>
<tr>
<th>Subject</th>
<th>Mathematics</th>
<th>Physics</th>
<th>Chemistry</th>
</tr>
</thead>
<tbody>
<tr>
<td>Mean</td>
<td>42</td>
<td>32</td>
<td>40.9</td>
</tr>
<tr>
<td>Standard<br>deviation</td>
<td>12</td>
<td>15</td>
<td>20</td>
</tr>
</tbody>
</table>

Which of the three subjects shows the highest variability in marks and which
shows the lowest?
7. The mean and standard deviation of a group of 100 observations were found to
be 20 and 3, respectively. Later on it was found that three observations were
incorrect, which were recorded as 21, 21 and 18. Find the mean and standard
deviation if the incorrect observations are omitted.

7. The mean and standard deviation of a group of 100 observations were found to
be 20 and 3, respectively. Later on it was found that three observations were
incorrect, which were recorded as 21, 21 and 18. Find the mean and standard
deviation if the incorrect observations are omitted.

Summary

$\diamond$ Measures of dispersion Range, Quartile deviation, mean deviation, variance,
standard deviation are measures of dispersion.
Range = Maximum Value – Minimum Value
$\diamond$ Mean deviation for ungrouped data

$$\text{M.D. } (\overline{x}) = \frac{\sum |x_i - \overline{x}|}{n}, \quad \text{M.D. } (M) = \frac{\sum |x_i - M|}{n}$$

<!-- page 444 -->
$\diamond$ Mean deviation for grouped data

$$\text{M.D. } (\bar{x}) = \frac{\sum f_i |x_i \quad \bar{x}|}{\text{N}}, \quad \text{M.D. } (\text{M}) = \frac{\sum f_i |x_i \quad \text{M}|}{\text{N}}, \text{ where } \text{N} = \sum f_i$$

$\diamond$ Variance and standard deviation for ungrouped data

$$\sigma^2 = \frac{1}{n} \sum (x_i - \bar{x})^2, \quad \sigma = \sqrt{\frac{1}{n} \sum (x_i - \bar{x})^2}$$

$\diamond$ Variance and standard deviation of a discrete frequency distribution

$$\sigma^2 = \frac{1}{N} \sum f_i(x_i - \bar{x})^2, \quad \sigma = \sqrt{\frac{1}{N} \sum f_i(x_i - \bar{x})^2}$$

$\diamond$ Variance and standard deviation of a continuous frequency distribution

$$\sigma^2 = \frac{1}{N} \sum f_i (x_i - \bar{x})^2, \quad \sigma = \frac{1}{N} \sqrt{N \sum f_i x_i^2 - (\sum f_i x_i)^2}$$

$\diamond$ Shortcut method to find variance and standard deviation.

$$\sigma^2 = \frac{h^2}{N^2} \left[ N \sum f_i y_i^2 - \left( \sum f_i y_i \right)^2 \right], \sigma = \frac{h}{N} \sqrt{N \sum f_i y_i^2 - \left( \sum f_i y_i \right)^2},$$

where $y_i = \frac{x_i - A}{h}$

Coefficient of variation (C.V.) $= \frac{\sigma}{\bar{x}} \times 100, \bar{x} \neq 0.$

For series with equal means, the series with lesser standard deviation is more consistent
or less scattered.

Historical Note

‘Statistics’ is derived from the Latin word ‘status’ which means a political
state. This suggests that statistics is as old as human civilisation. In the year 3050
B.C., perhaps the first census was held in Egypt. In India also, about 2000 years
ago, we had an efficient system of collecting administrative statistics, particularly,
during the regime of Chandra Gupta Maurya (324-300 B.C.). The system of
collecting data related to births and deaths is mentioned in Kautilya’s $Arthshastra$
(around 300 B.C.) A detailed account of administrative surveys conducted during
Akbar’s regime is given in $Ain$-$I$-$Akbari$ written by Abul Fazl.

<!-- page 445 -->
Captain John Graunt of London (1620-1674) is known as father of vital
statistics due to his studies on statistics of births and deaths. Jacob Bernoulli
(1654-1705) stated the Law of Large numbers in his book “Ars Conjectandi’,
published in 1713.
The theoretical development of statistics came during the mid seventeenth
century and continued after that with the introduction of theory of games and
chance (i.e., probability). Francis Galton (1822-1921), an Englishman, pioneered
the use of statistical methods, in the field of Biometry. Karl Pearson (1857-1936)
contributed a lot to the development of statistical studies with his discovery
of $Chi$ $square$ $test$ and foundation of $statistical$ $laboratory$ in England (1911).
Sir Ronald A. Fisher (1890-1962), known as the Father of modern statistics,
applied it to various diversified fields such as Genetics, Biometry, Education,
Agriculture, etc.

<!-- page 446 -->
Chapter

PROBABILITY

❖Where a mathematical reasoning can be had, it is as great a folly to
make use of any other, as to grope for a thing in the dark, when
you have a candle in your hand. – JOHN ARBUTHNOT ❖

16.1 Introduction

In earlier classes, we studied about the concept of
probability as a measure of uncertainty of various
phenomenon. We have obtained the probability of getting

an even number in throwing a die as $\frac{3}{6}$ i.e., $\frac{1}{2}$. Here the
total possible outcomes are 1,2,3,4,5 and 6 (six in number).
The outcomes in favour of the event of ‘getting an even
number’ are 2,4,6 (i.e., three in number). In general, to
obtain the probability of an event, we find the ratio of the
number of outcomes favourable to the event, to the total
number of equally likely outcomes. This theory of probability
is known as classical theory of probability.

Kolmogorov
(1903-1987)

In Class IX, we learnt to find the probability on the basis of observations and
collected data. This is called $statistical$ $approach$ $of$ $probability$.

Both the theories have some serious difficulties. For instance, these theories can
not be applied to the activities/experiments which have infinite number of outcomes. In
classical theory we assume all the outcomes to be equally likely. Recall that the outcomes
are called equally likely when we have no reason to believe that one is more likely to
occur than the other. In other words, we assume that all outcomes have equal chance
(probability) to occur. Thus, to define probability, we used equally likely or equally
probable outcomes. This is logically not a correct definition. Thus, another theory of
probability was developed by A.N. Kolmogorov, a Russian mathematician, in 1933. He

<!-- page 447 -->
laid down some axioms to interpret probability, in his book ‘Foundation of Probability’
published in 1933. In this Chapter, we will study about this approach called *axiomatic*
*approach of probability*. To understand this approach we must know about few basic
terms viz. random experiment, sample space, events, etc. Let us learn about these all,
in what follows next.

16.2 Random Experiments

In our day to day life, we perform many activities which have a fixed result no matter
any number of times they are repeated. For example given any triangle, without knowing
the three angles, we can definitely say that the sum of measure of angles is $180^{\circ}$.

We also perform many experimental activities, where the result may not be same,
when they are repeated under identical conditions. For example, when a coin is tossed
it may turn up a head or a tail, but we are not sure which one of these results will
actually be obtained. Such experiments are called $random$ $experiments$.

An experiment is called random experiment if it satisfies the following two
conditions:

(i) It has more than one possible outcome.
(ii) It is not possible to predict the outcome in advance.

Check whether the experiment of tossing a die is random or not?

In this chapter, we shall refer the random experiment by experiment only unless
stated otherwise.

16.2.1 *Outcomes and sample space* A possible result of a random experiment is
called its *outcome*.

Consider the experiment of rolling a die. The outcomes of this experiment are 1,
2, 3, 4, 5, or 6, if we are interested in the number of dots on the upper face of the die.

The set of outcomes $\{1, 2, 3, 4, 5, 6\}$ is called the sample space of the experiment.

Thus, the set of all possible outcomes of a random experiment is called the $sample$
$space$ associated with the experiment. Sample space is denoted by the symbol S.

Each element of the sample space is called a $sample$ $point$. In other words, each
outcome of the random experiment is also called $sample$ $point$.

Let us now consider some examples.

Example 1 Two coins (a one rupee coin and a two rupee coin) are tossed once. Find
a sample space.

Solution Clearly the coins are distinguishable in the sense that we can speak of the
first coin and the second coin. Since either coin can turn up Head (H) or Tail(T), the
possible outcomes may be

<!-- page 448 -->
Heads on both coins = (H,H) = HH

Head on first coin and Tail on the other $= (H,T) = HT$

Tail on first coin and Head on the other $= (T,H) = TH$

$$Tail\ on\ both\ coins = (T,T) = TT$$

Thus, the sample space is $S = \{HH, HT, TH, TT\}$

Note The outcomes of this experiment are ordered pairs of H and T. For the
sake of simplicity the commas are omitted from the ordered pairs.

Example 2 Find the sample space associated with the experiment of rolling a pair of
dice (one is blue and the other red) once. Also, find the number of elements of this
sample space.

**Solution** Suppose 1 appears on blue die and 2 on the red die. We denote this outcome
by an ordered pair $(1,2)$. Similarly, if ‘3’ appears on blue die and ‘5’ on red, the outcome
is denoted by the ordered pair $(3,5)$.

In general each outcome can be denoted by the ordered pair $(x, y)$, where $x$ is
the number appeared on the blue die and $y$ is the number appeared on the red die.
Therefore, this sample space is given by

$$S = \{(x, y): x \text{ is the number on the blue die and } y \text{ is the number on the red die}\}.$$

The number of elements of this sample space is $6 \times 6 = 36$ and the sample space is
given below:

$$\{(1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6)$$
$$(3,1), (3,2), (3,3), (3,4), (3,5), (3,6), (4,1), (4,2), (4,3), (4,4), (4,5), (4,6)$$
$$(5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (6,1), (6,2), (6,3), (6,4), (6,5), (6,6)\}$$

Example 3 In each of the following experiments specify appropriate sample space

(i) A boy has a 1 rupee coin, a 2 rupee coin and a 5 rupee coin in his pocket. He
takes out two coins out of his pocket, one after the other.
(ii) A person is noting down the number of accidents along a busy highway
during a year.

**Solution** (i) Let $Q$ denote a 1 rupee coin, $H$ denotes a 2 rupee coin and $R$ denotes a 5
rupee coin. The first coin he takes out of his pocket may be any one of the three coins
$Q$, $H$ or $R$. Corresponding to $Q$, the second draw may be $H$ or $R$. So the result of two
draws may be $QH$ or $QR$. Similarly, corresponding to $H$, the second draw may be
$Q$ or $R$.
Therefore, the outcomes may be $HQ$ or $HR$. Lastly, corresponding to $R$, the second
draw may be $H$ or $Q$.
So, the outcomes may be $RH$ or $RQ$.

So, the outcomes may be RH or RQ.

<!-- page 449 -->
Thus, the sample space is $S=\{QH, QR, HQ, HR, RH, RQ\}$

(ii) The number of accidents along a busy highway during the year of observation
can be either 0 (for no accident ) or 1 or 2, or some other positive integer.
Thus, a sample space associated with this experiment is $S= \{0,1,2,...\}$

Example 4 A coin is tossed. If it shows head, we draw a ball from a bag consisting of
3 blue and 4 white balls; if it shows tail we throw a die. Describe the sample space of
this experiment.

Solution Let us denote blue balls by $\text{B}_1$, $\text{B}_2$, $\text{B}_3$ and the white balls by $\text{W}_1$, $\text{W}_2$, $\text{W}_3$, $\text{W}_4$.
Then a sample space of the experiment is

$$S = \{ HB_1, HB_2, HB_3, HW_1, HW_2, HW_3, HW_4, T1, T2, T3, T4, T5, T6 \}.$$

Here $\text{HB}_i$ means head on the coin and ball $\text{B}_i$ is drawn, $\text{HW}_i$ means head on the coin
and ball $\text{W}_i$ is drawn. Similarly, $Ti$ means tail on the coin and the number $i$ on the die.

Example 5 Consider the experiment in which a coin is tossed repeatedly until a head
comes up. Describe the sample space.

Solution In the experiment head may come up on the first toss, or the 2nd toss, or the
3rd toss and so on till head is obtained. Hence, the desired sample space is

$$S= \{H, TH, TTH, TTTH, TTTTH,...\}$$

EXERCISE 16.1

In each of the following Exercises 1 to 7, describe the sample space for the indicated
experiment.

1. A coin is tossed three times.
2. A die is thrown two times.
3. A coin is tossed four times.
4. A coin is tossed and a die is thrown.
5. A coin is tossed and then a die is rolled only in case a head is shown on the coin.
6. 2 boys and 2 girls are in Room X, and 1 boy and 3 girls in Room Y. Specify the
sample space for the experiment in which a room is selected and then a person.
7. One die of red colour, one of white colour and one of blue colour are placed in a
bag. One die is selected at random and rolled, its colour and the number on its
uppermost face is noted. Describe the sample space.
8. An experiment consists of recording boy–girl composition of families with 2
children.
(i) What is the sample space if we are interested in knowing whether it is a boy
or girl in the order of their births?

<!-- page 450 -->
(ii) What is the sample space if we are interested in the number of girls in the
family?

9. A box contains 1 red and 3 identical white balls. Two balls are drawn at random
in succession without replacement. Write the sample space for this experiment.
10. An experiment consists of tossing a coin and then throwing it second time if a
head occurs. If a tail occurs on the first toss, then a die is rolled once. Find the
sample space.
11. Suppose 3 bulbs are selected at random from a lot. Each bulb is tested and
classified as defective (D) or non – defective(N). Write the sample space of this
experiment.
12. A coin is tossed. If the out come is a head, a die is thrown. If the die shows up
an even number, the die is thrown again. What is the sample space for the
experiment?
13. The numbers 1, 2, 3 and 4 are written separatly on four slips of paper. The slips
are put in a box and mixed thoroughly. A person draws two slips from the box,
one after the other, without replacement. Describe the sample space for the
experiment.
14. An experiment consists of rolling a die and then tossing a coin once if the number
on the die is even. If the number on the die is odd, the coin is tossed twice. Write
the sample space for this experiment.
15. A coin is tossed. If it shows a tail, we draw a ball from a box which contains 2 red
and 3 black balls. If it shows head, we throw a die. Find the sample space for this
experiment.
16. A die is thrown repeatedly untill a six comes up. What is the sample space for
this experiment?

16. A die is thrown repeatedly untill a six comes up. What is the sample space for
this experiment?

16.3 Event

We have studied about random experiment and sample space associated with an
experiment. The sample space serves as an universal set for all questions concerned
with the experiment.

Consider the experiment of tossing a coin two times. An associated sample space
is $S = \{HH, HT, TH, TT\}$.

Now suppose that we are interested in those outcomes which correspond to the
occurrence of exactly one head. We find that HT and TH are the only elements of S
corresponding to the occurrence of this happening (event). These two elements form
the set $E = \{ HT, TH \}$

We know that the set E is a subset of the sample space S . Similarly, we find the
following correspondence between events and subsets of S.

<!-- page 451 -->
<table>
<thead>
<tr>
<th>Description of events</th>
<th>Corresponding subset of ‘S’</th>
</tr>
</thead>
<tbody>
<tr>
<td>Number of tails is exactly 2</td>
<td>A = {TT}</td>
</tr>
<tr>
<td>Number of tails is atleast one</td>
<td>B = {HT, TH, TT}</td>
</tr>
<tr>
<td>Number of heads is atmost one</td>
<td>C = {HT, TH, TT}</td>
</tr>
<tr>
<td>Second toss is not head</td>
<td>D = { HT, TT}</td>
</tr>
<tr>
<td>Number of tails is atmost two</td>
<td>S = {HH, HT, TH, TT}</td>
</tr>
<tr>
<td>Number of tails is more than two</td>
<td>$\phi$</td>
</tr>
</tbody>
</table>

The above discussion suggests that a subset of sample space is associated with
an event and an event is associated with a subset of sample space. In the light of this
we define an event as follows.

Definition Any subset E of a sample space S is called an event.

**16.3.1** *Occurrence of an event* Consider the experiment of throwing a die. Let E
denotes the event “ a number less than 4 appears”. If actually ‘1’ had appeared on the
die then we say that event E has occurred. As a matter of fact if outcomes are 2 or 3,
we say that event E has occurred

Thus, the event E of a sample space S is said to have occurred if the outcome
$\omega$ of the experiment is such that $\omega \in \text{E}$. If the outcome $\omega$ is such that $\omega \notin \text{E}$, we say
that the event E has not occurred.

16.3.2 Types of events Events can be classified into various types on the basis of the
elements they have.

1. **Impossible and Sure Events** The empty set $\phi$ and the sample space S describe
events. In fact $\phi$ is called an *impossible event* and S, i.e., the whole sample space is
called the *sure event*.

To understand these let us consider the experiment of rolling a die. The associated
sample space is

$$S = \{1, 2, 3, 4, 5, 6\}$$

Let E be the event “ the number appears on the die is a multiple of 7”. Can you
write the subset associated with the event E?

Clearly no outcome satisfies the condition given in the event, i.e., no element of
the sample space ensures the occurrence of the event E. Thus, we say that the empty
set only correspond to the event E. In other words we can say that it is impossible to
have a multiple of 7 on the upper face of the die. Thus, the event E = $\phi$ is an impossible
event.

Now let us take up another event F “the number turns up is odd or even”. Clearly

<!-- page 452 -->
$$F = \{1, 2, 3, 4, 5, 6, \} = S, \text{ i.e., all outcomes of the experiment ensure the occurrence of}$$
$$\text{the event F. Thus, the event } F = S \text{ is a sure event.}$$

2. Simple Event If an event E has only one sample point of a sample space, it is
called a simple (or elementary) event.

In a sample space containing $n$ distinct elements, there are exactly $n$ simple
events.

For example in the experiment of tossing two coins, a sample space is
$$S=\{HH, HT, TH, TT\}$$

There are four simple events corresponding to this sample space. These are

$E_1=\{HH\}$, $E_2=\{HT\}$, $E_3=\{ TH \}$ and $E_4=\{TT\}$.

3. **Compound Event** If an event has more than one sample point, it is called a
*Compound event*.

For example, in the experiment of “tossing a coin thrice” the events

E: ‘Exactly one head appeared’
F: ‘Atleast one head appeared’
G: ‘Atmost one head appeared’ etc.

are all compound events. The subsets of S associated with these events are

$$E=\{HTT,THT,TTH\}$$

F={HTT,THT, TTH, HHT, HTH, THH, HHH}

$$G = \{ TTT, THT, HTT, TTH \}$$

Each of the above subsets contain more than one sample point, hence they are all
compound events.

16.3.3 Algebra of events In the Chapter on Sets, we have studied about different
ways of combining two or more sets, viz, union, intersection, difference, complement
of a set etc. Like-wise we can combine two or more events by using the analogous set
notations.

Let A, B, C be events associated with an experiment whose sample space is S.

1. Complementary Event For every event A, there corresponds another event

A' called the complementary event to A. It is also called the event ‘not A’.

For example, take the experiment ‘of tossing three coins’. An associated sample
space is

$$S = \{HHH, HHT, HTH, THH, HTT, THT, TTH, TTT\}$$

Let $A=\{HTH, HHT, THH\}$ be the event ‘only one tail appears’

Clearly for the outcome HTT, the event A has not occurred. But we may say that
the event ‘not A’ has occurred. Thus, with every outcome which is not in A, we say
that ‘not A’ occurs.

<!-- page 453 -->
Thus the complementary event ‘not A’ to the event A is

$$A' = \{HHH, HTT, THT, TTH, TTT\}$$

or $A' = \{\omega : \omega \in S \text{ and } \omega \notin A\} = S - A.$

2. The Event ‘A or B’ Recall that union of two sets A and B denoted by $A \cup B$
contains all those elements which are either in A or in B or in both.

When the sets A and B are two events associated with a sample space, then
‘A $\cup$ B’ is the event ‘either A or B or both’. This event ‘A $\cup$ B’ is also called ‘A or B’.

Therefore      Event ‘A or B’ = A $\cup$ B
                  = { $\omega$ : $\omega \in$ A or $\omega \in$ B }

3. The Event ‘A and B’ We know that intersection of two sets A $\cap$ B is the set of
those elements which are common to both A and B. i.e., which belong to both
‘A and B’.

If A and B are two events, then the set A $\cap$ B denotes the event ‘A and B’.

Thus, $A \cap B = \{\omega : \omega \in A \text{ and } \omega \in B\}$

For example, in the experiment of ‘throwing a die twice’ Let A be the event
‘score on the first throw is six’ and B is the event ‘sum of two scores is atleast 11’ then

$$A = \{(6,1), (6,2), (6,3), (6,4), (6,5), (6,6)\}, \text{ and } B = \{(5,6), (6,5), (6,6)\}$$
so $A \cap B = \{(6,5), (6,6)\}$

Note that the set $A \cap B = \{(6,5), (6,6)\}$ may represent the event ‘the score on the first
throw is six and the sum of the scores is atleast 11’.

4. The Event ‘A but not B’ We know that A–B is the set of all those elements
which are in A but not in B. Therefore, the set A–B may denote the event ‘A but not
B’.We know that

$$A - B = A \cap B'$$

Example 6 Consider the experiment of rolling a die. Let A be the event ‘getting a
prime number’, B be the event ‘getting an odd number’. Write the sets representing
the events (i) Aor B (ii) A and B (iii) A but not B (iv) ‘not A’.

Solution Here $S = \{1, 2, 3, 4, 5, 6\}, A = \{2, 3, 5\}$ and $B = \{1, 3, 5\}$

Obviously

(i) ‘A or B’ = $A \cup B = \{1, 2, 3, 5\}$

(ii) ‘A and B’ = $A \cap B = \{3,5\}$

(iii) ‘A but not B’ = $A - B = \{2\}$

(iv) ‘not A’ = $A’ = \{1,4,6\}$

<!-- page 454 -->
16.3.4 Mutually exclusive events In the experiment of rolling a die, a sample space is
$S = \{1, 2, 3, 4, 5, 6\}$. Consider events, A ‘an odd number appears’ and B ‘an even
number appears’

Clearly the event A excludes the event B and vice versa. In other words, there is
no outcome which ensures the occurrence of events A and B simultaneously. Here

$$A = \{1, 3, 5\} \text{ and } B = \{2, 4, 6\}$$

Clearly $A \cap B = \phi$, i.e., $A$ and $B$ are disjoint sets.

In general, two events A and B are called mutually exclusive events if the
occurrence of any one of them excludes the occurrence of the other event, i.e., if they
can not occur simultaneously. In this case the sets A and B are disjoint.

Again in the experiment of rolling a die, consider the events A ‘an odd number
appears’ and event B ‘a number less than 4 appears’

Obviously $A = \{1, 3, 5\}$ and $B = \{1, 2, 3\}$

Now $3 \in A$ as well as $3 \in B$

Therefore, A and B are not mutually exclusive events.

$Remark$ Simple events of a sample space are always mutually exclusive.

16.3.5 Exhaustive events Consider the experiment of throwing a die. We have
$S = \{1, 2, 3, 4, 5, 6\}$. Let us define the following events

A: ‘a number less than 4 appears’,

B: ‘a number greater than 2 but less than 5 appears’

and C: ‘a number greater than 4 appears’.

Then $A = \{1, 2, 3\}$, $B = \{3,4\}$ and $C = \{5, 6\}$. We observe that

$$A \cup B \cup C = \{1, 2, 3\} \cup \{3, 4\} \cup \{5, 6\} = S.$$

Such events A, B and C are called exhaustive events. In general, if $E_1, E_2, ..., E_n$ are $n$
events of a sample space S and if

$$\mathrm{E}_1 \cup \mathrm{E}_2 \cup \mathrm{E}_3 \cup ... \cup \mathrm{E}_n = \bigcup_{i=1}^n \mathrm{E}_i = \mathrm{S}$$

then $E_1, E_2, ...., E_n$ are called *exhaustive events*.In other words, events $E_1, E_2, ...., E_n$
are said to be exhaustive if atleast one of them necessarily occurs whenever the
experiment is performed.

Further, if $\mathrm{E}_i \cap \mathrm{E}_j = \phi$ for $i \neq j$ i.e., events $\mathrm{E}_i$ and $\mathrm{E}_j$ are pairwise disjoint and

$\bigcup_{i=1}^{n} \mathrm{E}_{i} = \mathrm{S}$, then events $\mathrm{E}_{1}, \mathrm{E}_{2}, ..., \mathrm{E}_{n}$ are called *mutually exclusive and exhaustive*
*events*.

<!-- page 455 -->
We now consider some examples.

Example 7 Two dice are thrown and the sum of the numbers which come up on the
dice is noted. Let us consider the following events associated with this experiment

A: ‘the sum is even’.
B: ‘the sum is a multiple of 3’.
C: ‘the sum is less than 4’.
D: ‘the sum is greater than 11’.

Which pairs of these events are mutually exclusive?

Solution There are 36 elements in the sample space $S = \{(x, y): x, y = 1, 2, 3, 4, 5, 6\}$.
Then

$A = \{(1, 1), (1, 3), (1, 5), (2, 2), (2, 4), (2, 6), (3, 1), (3, 3), (3, 5), (4, 2), (4, 4),$
$(4, 6), (5, 1), (5, 3), (5, 5), (6, 2), (6, 4), (6, 6)\}$
$B = \{(1, 2), (2, 1), (1, 5), (5, 1), (3, 3), (2, 4), (4, 2), (3, 6), (6, 3), (4, 5), (5, 4),$
$(6, 6)\}$
$C = \{(1, 1), (2, 1), (1, 2)\}$ and $D = \{(6, 6)\}$

We find that

$$A \cap B = \{(1, 5), (2, 4), (3, 3), (4, 2), (5, 1), (6, 6)\} \neq \phi$$

Therefore, A and B are not mutually exclusive events.

Similarly $A \cap C \neq \phi$, $A \cap D \neq \phi$, $B \cap C \neq \phi$ and $B \cap D \neq \phi$.

Thus, the pairs of events, (A, C), (A, D), (B, C), (B, D) are not mutually exclusive
events.

Also $C \cap D = \phi$ and so $C$ and $D$ are mutually exclusive events.

Example 8 A coin is tossed three times, consider the following events.
A: ‘No head appears’, B: ‘Exactly one head appears’ and C: ‘Atleast two heads
appear’.
Do they form a set of mutually exclusive and exhaustive events?

Solution The sample space of the experiment is
$$S = \{HHH, HHT, HTH, THH, HTT, THT, TTH, TTT\}$$
and $A = \{TTT\}, B = \{HTT, THT, TTH\}, C = \{HHT, HTH, THH, HHH\}$
Now
$$A \cup B \cup C = \{TTT, HTT, THT, TTH, HHT, HTH, THH, HHH\} = S$$
Therefore, $A, B$ and $C$ are exhaustive events.
Also, $A \cap B = \phi, A \cap C = \phi$ and $B \cap C = \phi$
Therefore, the events are pair-wise disjoint, i.e., they are mutually exclusive.
Hence, $A, B$ and $C$ form a set of mutually exclusive and exhaustive events.

<!-- page 456 -->
EXERCISE 16.2

1. A die is rolled. Let E be the event “die shows 4” and F be the event “die shows
even number”. Are E and F mutually exclusive?

2. A die is thrown. Describe the following events:
(i) A: a number less than 7 (ii) B: a number greater than 7
(iii) C: a multiple of 3 (iv) D: a number less than 4
(v) E: an even number greater than 4 (vi) F: a number not less than 3

Also find $A \cup B, A \cap B, B \cup C, E \cap F, D \cap E, A - C, D - E, E \cap F', F'$

3. An experiment involves rolling a pair of dice and recording the numbers that
come up. Describe the following events:
A: the sum is greater than 8, B: 2 occurs on either die
C: the sum is at least 7 and a multiple of 3.
Which pairs of these events are mutually exclusive?

4. Three coins are tossed once. Let A denote the event ‘three heads show’, B
denote the event “two heads and one tail show”, C denote the event” three tails
show and D denote the event ‘a head shows on the first coin”. Which events are
(i) mutually exclusive? (ii) simple? (iii) Compound?

5. Three coins are tossed. Describe

(i) Two events which are mutually exclusive.
(ii) Three events which are mutually exclusive and exhaustive.
(iii) Two events, which are not mutually exclusive.
(iv) Two events which are mutually exclusive but not exhaustive.
(v) Three events which are mutually exclusive but not exhaustive.

6. Two dice are thrown. The events A, B and C are as follows:
A: getting an even number on the first die.
B: getting an odd number on the first die.
C: getting the sum of the numbers on the dice $\le 5$.
Describe the events
(i) $A'$
(ii) not B
(iii) A or B
(iv) A and B
(v) A but not C
(vi) B or C
(vii) B and C
(viii) $A \cap B' \cap C'$

7. Refer to question 6 above, state true or false: (give reason for your answer)
(i) A and B are mutually exclusive
(ii) A and B are mutually exclusive and exhaustive
(iii) $A = B'$

<!-- page 457 -->
(iv) A and C are mutually exclusive
(v) A and B' are mutually exclusive.
(vi) A', B', C are mutually exclusive and exhaustive.

16.4 Axiomatic Approach to Probability

In earlier sections, we have considered random experiments, sample space and
events associated with these experiments. In our day to day life we use many words
about the chances of occurrence of events. Probability theory attempts to quantify
these chances of occurrence or non occurrence of events.

In earlier classes, we have studied some methods of assigning probability to an
event associated with an experiment having known the number of total outcomes.

Axiomatic approach is another way of describing probability of an event. In this
approach some axioms or rules are depicted to assign probabilities.

Let $S$ be the sample space of a random experiment. The probability $P$ is a real
valued function whose domain is the power set of $S$ and range is the interval $[0,1]$
satisfying the following axioms

(i) For any event E, $P(E) \geq 0$ (ii) $P(S) = 1$
(iii) If E and F are mutually exclusive events, then $P(E \cup F) = P(E) + P(F)$.

It follows from (iii) that $P(\phi) = 0$. To prove this, we take $F = \phi$ and note that $E$ and $\phi$
are disjoint events. Therefore, from axiom (iii), we get

$$P(E \cup \phi) = P(E) + P(\phi) \text{ or } \quad P(E) = P(E) + P(\phi) \text{ i.e. } P(\phi) = 0.$$

Let S be a sample space containing outcomes $\omega_1, \omega_2, ..., \omega_n$, i.e.,

$$S = \{\omega_1, \omega_2, ..., \omega_n\}$$

It follows from the axiomatic definition of probability that

(i) $0 \leq P\left(\omega_{i}\right) \leq 1$ for each $\omega_{i} \in S$
(ii) $P\left(\omega_{1}\right)+P\left(\omega_{2}\right)+\ldots+P\left(\omega_{n}\right)=1$
(iii) For any event A, $P(A)=\sum P\left(\omega_{i}\right), \omega_{i} \in A$.

Note It may be noted that the singleton $\{\omega_i\}$ is called elementary event and
for notational convenience, we write $\mathrm{P}(\omega_i)$ for $\mathrm{P}(\{\omega_i\})$.

For example, in ‘a coin tossing’ experiment we can assign the number $\frac{1}{2}$ to each
of the outcomes H and T.

i.e. $P(H) = \frac{1}{2}$ and $P(T) = \frac{1}{2}$ (1)

Clearly this assignment satisfies both the conditions i.e., each number is neither
less than zero nor greater than 1 and

<!-- page 458 -->
$$P(H) + P(T) = \frac{1}{2} + \frac{1}{2} = 1$$

Therefore, in this case we can say that probability of $H = \frac{1}{2}$, and probability of $T = \frac{1}{2}$

If we take $\quad \mathrm{P}(\mathrm{H})=\frac{1}{4}$ and $\mathrm{P}(\mathrm{T})=\frac{3}{4}$ \hfill ... (2)

Does this assignment satisfy the conditions of axiomatic approach?

Yes, in this case, probability of $H = \frac{1}{4}$ and probability of $T = \frac{3}{4}$.

We find that both the assignments (1) and (2) are valid for probability of
H and T.

In fact, we can assign the numbers $p$ and $(1 - p)$ to both the outcomes such that
$$0 \le p \le 1 \text{ and } \mathrm{P}(\mathrm{H}) + \mathrm{P}(\mathrm{T}) = p + (1 - p) = 1$$

This assignment, too, satisfies both conditions of the axiomatic approach of
probability. Hence, we can say that there are many ways (rather infinite) to assign
probabilities to outcomes of an experiment. We now consider some examples.

Example 9 Let a sample space be $S = \{\omega_1, \omega_2, ..., \omega_6\}$.Which of the following
assignments of probabilities to each outcome are valid?
$\begin{array}{ccccccc} \text{Outcomes} & \omega_1 & \omega_2 & \omega_3 & \omega_4 & \omega_5 & \omega_6 \\ \text{(a)} & \frac{1}{6} & \frac{1}{6} & \frac{1}{6} & \frac{1}{6} & \frac{1}{6} & \frac{1}{6} \\ \text{(b)} & 1 & 0 & 0 & 0 & 0 & 0 \\ \text{(c)} & \frac{1}{8} & \frac{2}{3} & \frac{1}{3} & \frac{1}{3} & -\frac{1}{4} & -\frac{1}{3} \\ \text{(d)} & \frac{1}{12} & \frac{1}{12} & \frac{1}{6} & \frac{1}{6} & \frac{1}{6} & \frac{3}{2} \\ \text{(e)} & 0.1 & 0.2 & 0.3 & 0.4 & 0.5 & 0.6 \end{array}$

Solution (a) Condition (i): Each of the number $p(\omega_i)$ is positive and less than one.
Condition (ii): Sum of probabilities
$$= \frac{1}{6} + \frac{1}{6} + \frac{1}{6} + \frac{1}{6} + \frac{1}{6} + \frac{1}{6} = 1$$

<!-- page 459 -->
Therefore, the assignment is valid

(b) Condition (i): Each of the number $p(\omega_i)$ is either 0 or 1.
Condition (ii) Sum of the probabilities $= 1 + 0 + 0 + 0 + 0 + 0 = 1$
Therefore, the assignment is valid
(c) Condition (i) Two of the probabilities $p(\omega_5)$ and $p(\omega_6)$ are negative, the assignment
is not valid

(d) Since $p(\omega_6) = \frac{3}{2} > 1$, the assignment is not valid

(e) Since, sum of probabilities $= 0.1 + 0.2 + 0.3 + 0.4 + 0.5 + 0.6 = 2.1$, the assignment
is not valid.

16.4.1 *Probability of an event* Let S be a sample space associated with the experiment
‘examining three consecutive pens produced by a machine and classified as Good
(non-defective) and bad (defective)’. We may get 0, 1, 2 or 3 defective pens as result
of this examination.

A sample space associated with this experiment is

$$S = \{BBB, BBG, BGB, GBB, BGG, GBG, GGB, GGG\},$$

where B stands for a defective or bad pen and G for a non – defective or good pen.

Let the probabilities assigned to the outcomes be as follows

Sample point: BBB BBG BGB GBB BGG GBG GGB GGG

Probability: $\frac{1}{8}$ $\frac{1}{8}$ $\frac{1}{8}$ $\frac{1}{8}$ $\frac{1}{8}$ $\frac{1}{8}$ $\frac{1}{8}$ $\frac{1}{8}$

Let event A: there is exactly one defective pen and event B: there are atleast two
defective pens.

Hence $A = \{BGG, GBG, GGB\}$ and $B = \{BBG, BGB, GBB, BBB\}$

Now $\quad \mathrm{P}(\mathrm{A})=\sum \mathrm{P}\left(\omega_{i}\right), \forall \omega_{i} \in \mathrm{A}$
$\quad \quad \quad \quad \quad \quad =\mathrm{P}(\mathrm{BGG})+\mathrm{P}(\mathrm{GBG})+\mathrm{P}(\mathrm{GGB})=\frac{1}{8}+\frac{1}{8}+\frac{1}{8}=\frac{3}{8}$

and $\quad \mathrm{P}(\mathrm{B})=\sum \mathrm{P}\left(\omega_{i}\right), \forall \omega_{i} \in \mathrm{B}$

$\quad \quad \quad \quad \quad \quad =\mathrm{P}(\mathrm{BBG})+\mathrm{P}(\mathrm{BGB})+\mathrm{P}(\mathrm{GBB})+\mathrm{P}(\mathrm{BBB})=\frac{1}{8}+\frac{1}{8}+\frac{1}{8}+\frac{1}{8}=\frac{4}{8}=\frac{1}{2}$

Let us consider another experiment of ‘tossing a coin “twice”

The sample space of this experiment is $S = \{HH, HT, TH, TT\}$

Let the following probabilities be assigned to the outcomes

<!-- page 460 -->
$$P(HH) = \frac{1}{4}, P(HT) = \frac{1}{7}, P(TH) = \frac{2}{7}, P(TT) = \frac{9}{28}$$

Clearly this assignment satisfies the conditions of axiomatic approach. Now, let
us find the probability of the event E: ‘Both the tosses yield the same result’.

Here $\qquad \mathrm{E} = \{\mathrm{HH}, \mathrm{TT}\}$

Now $\quad \mathrm{P}(\mathrm{E})=\Sigma \mathrm{P}\left(w_{i}\right)$, for all $w_{i} \in \mathrm{E}$

$$= \mathrm{P}(\mathrm{HH}) + \mathrm{P}(\mathrm{TT}) = \frac{1}{4} + \frac{9}{28} = \frac{4}{7}$$

For the event F: ‘exactly two heads’, we have $F = \{HH\}$

and $P(F) = P(HH) = \frac{1}{4}$

16.4.2 *Probabilities of equally likely outcomes* Let a sample space of an
experiment be

$$S = \{\omega_1, \omega_2, ..., \omega_n\}.$$

Let all the outcomes are equally likely to occur, i.e., the chance of occurrence of each
simple event must be same.

i.e. $\qquad \qquad \qquad \mathrm{P}(\omega_i) = p$, for all $\omega_i \in S$ where $0 \le p \le 1$

Since $\sum_{i=1}^{n} \mathrm{P}(\omega_{i})=1$ i.e., $p+p+\ldots+p$ ($n$ times) $=1$

or $np = 1$ i.e., $p = \frac{1}{n}$

Let S be a sample space and E be an event, such that $n(\text{S}) = n$ and $n(\text{E}) = m$. If
each out come is equally likely, then it follows that

$$\mathrm{P}(\mathrm{E})=\frac{m}{n}=\frac{\text{Number of outcomes favourable to E}}{\text{Total possible outcomes}}$$

16.4.3 *Probability of the event ‘A or B’* Let us now find the probability of event
‘A or B’, i.e., P (A $\cup$ B)

Let $A = \{HHT, HTH, THH\}$ and $B = \{HTH, THH, HHH\}$ be two events associated
with ‘tossing of a coin thrice’

Clearly $\quad \mathrm{A} \cup \mathrm{B} = \{\mathrm{HHT}, \mathrm{HTH}, \mathrm{THH}, \mathrm{HHH}\}$

Now $\qquad \mathrm{P} (\mathrm{A} \cup \mathrm{B}) = \mathrm{P}(\mathrm{HHT}) + \mathrm{P}(\mathrm{HTH}) + \mathrm{P}(\mathrm{THH}) + \mathrm{P}(\mathrm{HHH})$

<!-- page 461 -->
If all the outcomes are equally likely, then

$$P(A \cup B) = \frac{1}{8} + \frac{1}{8} + \frac{1}{8} + \frac{1}{8} = \frac{4}{8} = \frac{1}{2}$$

Also $P(A) = P(HHT) + P(HTH) + P(THH) = \frac{3}{8}$

and $P(B) = P(HTH) + P(THH) + P(HHH) = \frac{3}{8}$

Therefore $P(A) + P(B) = \frac{3}{8} + \frac{3}{8} = \frac{6}{8}$

It is clear that      $P(A \cup B) \neq P(A) + P(B)$

The points HTH and THH are common to both A and B. In the computation of
$P(A) + P(B)$ the probabilities of points HTH and THH, i.e., the elements of $A \cap B$ are
included twice. Thus to get the probability $P(A \cup B)$ we have to subtract the probabilities
of the sample points in $A \cap B$ from $P(A) + P(B)$

i.e. $\quad \mathrm{P}(\mathrm{A} \cup \mathrm{B})=\mathrm{P}(\mathrm{A})+\mathrm{P}(\mathrm{B})-\sum \mathrm{P}\left(\omega_{i}\right), \forall \omega_{i} \in \mathrm{A} \cap \mathrm{B}$
$\quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad

Thus we observe that, $P(A \cup B) = P(A) + P(B) - P(A \cap B)$

In general, if A and B are any two events associated with a random experiment,
then by the definition of probability of an event, we have

$$P(A \cup B) = \sum p(\omega_i), \forall \omega_i \in A \cup B.$$

Since $A \cup B = (A-B) \cup (A \cap B) \cup (B-A),$

we have

$$P(A \cup B) = [\Sigma P(\omega_i) \forall \omega_i \in (A-B)] + [\Sigma P(\omega_i) \forall \omega_i \in A \cap B] + [\Sigma P(\omega_i) \forall \omega_i \in B - A]$$

(because A–B, A $\cap$ B and B – A are mutually exclusive) ... (1)

Also $P(A) + P(B) = [\sum p(\omega_i) \forall \omega_i \in A] + [\sum p(\omega_i) \forall \omega_i \in B]$

$= [\sum P(\omega_i) \forall \omega_i \in (A-B) \cup (A \cap B)] + [\sum P(\omega_i) \forall \omega_i \in (B - A) \cup (A \cap B)]$

$= [\sum P(\omega_i) \forall \omega_i \in (A - B)] + [\sum P(\omega_i) \forall \omega_i \in (A \cap B)] + [\sum P(\omega_i) \forall \omega_i \in (B-A)] +$

$[\sum P(\omega_i) \forall \omega_i \in (A \cap B)]$

$= P(A \cup B) + [\sum P(\omega_i) \forall \omega_i \in A \cap B]$ [using (1)]

$= P(A \cup B) + P(A \cap B).$

<!-- page 462 -->
Hence $P(A \cup B)=P(A)+P(B)-P(A \cap B).$

Alternatively, it can also be proved as follows:

$$A \cup B = A \cup (B - A), \text{ where } A \text{ and } B - A \text{ are mutually exclusive,}$$
$$\text{and } B = (A \cap B) \cup (B - A), \text{ where } A \cap B \text{ and } B - A \text{ are mutually exclusive.}$$
Using Axiom (iii) of probability, we get

$$P (A \cup B) = P (A) + P (B - A) \quad \dots (2)$$
and $$P(B) = P ( A \cap B) + P (B - A) \quad \dots (3)$$

Subtracting (3) from (2) gives

$$P(A \cup B) - P(B) = P(A) - P(A \cap B)$$
or $$P(A \cup B) = P(A) + P(B) - P(A \cap B)$$

The above result can further be verified by observing the Venn Diagram (Fig 16.1)

Fig 16.1

If $A$ and $B$ are disjoint sets, i.e., they are mutually exclusive events, then $A \cap B = \phi$

Therefore $P(A \cap B) = P(\phi) = 0$

Thus, for mutually exclusive events A and B, we have

$$P(A \cup B) = P(A) + P(B),$$

which is Axiom (iii) of probability.

16.4.4 *Probability of event ‘not A’* Consider the event $A = \{2, 4, 6, 8\}$ associated
with the experiment of drawing a card from a deck of ten cards numbered from
1 to 10. Clearly the sample space is $S = \{1, 2, 3, ..., 10\}$

If all the outcomes $1, 2, ..., 10$ are considered to be equally likely, then the probability

of each outcome is $\frac{1}{10}$

<!-- page 463 -->
Now $P(A) = P(2) + P(4) + P(6) + P(8)$
$= \frac{1}{10} + \frac{1}{10} + \frac{1}{10} + \frac{1}{10} = \frac{4}{10} = \frac{2}{5}$

Also event ‘not A’ = $A'$ = $\{1, 3, 5, 7, 9, 10\}$

Now $P(A') = P(1) + P(3) + P(5) + P(7) + P(9) + P(10)$
$= \frac{6}{10} = \frac{3}{5}$

Thus, $P(A') = \frac{3}{5} = 1 - \frac{2}{5} = 1 - P(A)$

Also, we know that $A'$ and $A$ are mutually exclusive and exhaustive events i.e.,

$$A \cap A' = \phi \text{ and } A \cup A' = S$$
or $$P(A \cup A') = P(S)$$
Now $$P(A) + P(A') = 1, \quad \text{by using axioms (ii) and (iii).}$$
or $$P(A') = P(\text{not } A) = 1 - P(A)$$

We now consider some examples and exercises having equally likely outcomes
unless stated otherwise.

Example 10 One card is drawn from a well shuffled deck of 52 cards. If each outcome
is equally likely, calculate the probability that the card will be
(i) a diamond (ii) not an ace
(iii) a black card (i.e., a club or, a spade) (iv) not a diamond
(v) not a black card.

**Solution** When a card is drawn from a well shuffled deck of 52 cards, the number of
possible outcomes is 52.

(i) Let A be the event 'the card drawn is a diamond'
Clearly the number of elements in set A is 13.

Therefore, $P(A) = \frac{13}{52} = \frac{1}{4}$

i.e. probability of a diamond card = $\frac{1}{4}$

(ii) We assume that the event ‘Card drawn is an ace’ is B
Therefore ‘Card drawn is not an ace’ should be B’.

$$\text{We know that } P(B') = 1 - P(B) = 1 - \frac{4}{52} = 1 - \frac{1}{13} = \frac{12}{13}$$

<!-- page 464 -->
(iii) Let C denote the event ‘card drawn is black card’
Therefore, number of elements in the set C = 26

i.e. $P(C) = \frac{26}{52} = \frac{1}{2}$

Thus, probability of a black card = $\frac{1}{2}$.

(iv) We assumed in (i) above that A is the event ‘card drawn is a diamond’,
so the event ‘card drawn is not a diamond’ may be denoted as A’ or ‘not A’

Now $P(\text{not } A) = 1 - P(A) = 1 - \frac{1}{4} = \frac{3}{4}$

(v) The event ‘card drawn is not a black card’ may be denoted as $C'$ or ‘not $C$’.

We know that $P(\text{not } C) = 1 - P(C) = 1 - \frac{1}{2} = \frac{1}{2}$

Therefore, probability of not a black card = $\frac{1}{2}$

Example 11 A bag contains 9 discs of which 4 are red, 3 are blue and 2 are yellow.
The discs are similar in shape and size. A disc is drawn at random from the bag.
Calculate the probability that it will be (i) red, (ii) yellow, (iii) blue, (iv) not blue,
(v) either red or blue.

Solution There are 9 discs in all so the total number of possible outcomes is 9.
Let the events A, B, C be defined as

A: ‘the disc drawn is red’
B: ‘the disc drawn is yellow’
C: ‘the disc drawn is blue’.

(i) The number of red discs $= 4$, i.e., $n (\mathrm{A}) = 4$

Hence $P(A) = \frac{4}{9}$

(ii) The number of yellow discs $= 2$, i.e., $n$ (B) $= 2$

Therefore, $P(B) = \frac{2}{9}$

(iii) The number of blue discs = 3, i.e., $n(\mathrm{C}) = 3$

<!-- page 465 -->
Therefore, $P(C) = \frac{3}{9} = \frac{1}{3}$

(iv) Clearly the event ‘not blue’ is ‘not C’. We know that $P(\text{not } C) = 1 - P(C)$

Therefore $P(\text{not } C) = 1 - \frac{1}{3} = \frac{2}{3}$

(v) The event ‘either red or blue’ may be described by the set ‘A or C’

Since, A and C are mutually exclusive events, we have

$$P(A \text{ or } C) = P(A \cup C) = P(A) + P(C) = \frac{4}{9} + \frac{1}{3} = \frac{7}{9}$$

Example 12 Two students Anil and Ashima appeared in an examination. The probability
that Anil will qualify the examination is 0.05 and that Ashima will qualify the examination
is 0.10. The probability that both will qualify the examination is 0.02. Find the
probability that

(a) Both Anil and Ashima will not qualify the examination.
(b) Atleast one of them will not qualify the examination and
(c) Only one of them will qualify the examination.

Solution Let E and F denote the events that Anil and Ashima will qualify the examination,
respectively. Given that

$P(E) = 0.05$, $P(F) = 0.10$ and $P(E \cap F) = 0.02$.

Then

(a) The event ‘both Anil and Ashima will not qualify the examination’ may be
expressed as $E^{'} \cap F^{'}$.

Since, $E^{'}$ is ‘not $E^{'}$, i.e., Anil will not qualify the examination and $F^{'}$ is ‘not $F^{'}$, i.e.,
Ashima will not qualify the examination.

Also $\quad \mathrm{E}^{\prime} \cap \mathrm{F}^{\prime}=(\mathrm{E} \cup \mathrm{F})^{\prime}$ (by Demorgan's Law)

Now $\quad \mathrm{P}(\mathrm{E} \cup \mathrm{F})=\mathrm{P}(\mathrm{E})+\mathrm{P}(\mathrm{F})-\mathrm{P}(\mathrm{E} \cap \mathrm{F})$

or $\quad \mathrm{P}(\mathrm{E} \cup \mathrm{F})=0.05+0.10-0.02=0.13$

Therefore $\mathrm{P}\left(\mathrm{E}^{\prime} \cap \mathrm{F}^{\prime}\right)=\mathrm{P}(\mathrm{E} \cup \mathrm{F})^{\prime}=1-\mathrm{P}(\mathrm{E} \cup \mathrm{F})=1-0.13=0.87$

(b) P (atleast one of them will not qualify)
$$= 1 - \text{P}(\text{both of them will qualify})$$
$$= 1 - 0.02 = 0.98$$

<!-- page 466 -->
(c) The event only one of them will qualify the examination is same as the event
either (Anil will qualify, and Ashima will not qualify) or (Anil will not qualify and Ashima
will qualify) i.e., $E \cap F'$ or $E' \cap F$, where $E \cap F'$ and $E' \cap F$ are mutually exclusive.

Therefore, $P(\text{only one of them will qualify}) = P(E \cap F^{'} \text{ or } E^{'} \cap F)$

$$= \mathrm{P}(\mathrm{E} \cap \mathrm{F}') + \mathrm{P}(\mathrm{E}' \cap \mathrm{F}) = \mathrm{P} (\mathrm{E}) - \mathrm{P}(\mathrm{E} \cap \mathrm{F}) + \mathrm{P}(\mathrm{F}) - \mathrm{P} (\mathrm{E} \cap \mathrm{F})$$
$$= 0.05 - 0.02 + 0.10 - 0.02 = 0.11$$

Example 13 A committee of two persons is selected from two men and two women.
What is the probability that the committee will have (a) no man? (b) one man? (c) two
men?

Solution The total number of persons $= 2 + 2 = 4$. Out of these four person, two can
be selected in $^4\text{C}_2$ ways.

(a) No men in the committee of two means there will be two women in the committee.
Out of two women, two can be selected in $^2\text{C}_2 = 1$ way.

Therefore $P(\text{no man}) = \frac{{}^2C_2}{{}^4C_2} = \frac{1 \times 2 \times 1}{4 \times 3} = \frac{1}{6}$

(b) One man in the committee means that there is one woman. One man out of 2
can be selected in $^2\text{C}_1$ ways and one woman out of 2 can be selected in $^2\text{C}_1$ ways.

Together they can be selected in $^2\text{C}_1 \times ^2\text{C}_1$ ways.

Therefore $P(\text{One man}) = \frac{{}^2C_1 \times {}^2C_1}{{}^4C_2} = \frac{2 \times 2}{2 \times 3} = \frac{2}{3}$

(c) Two men can be selected in $^2\text{C}_2$ way.

Hence $P(\text{Two men}) = \frac{^2C_2}{^4C_2} = \frac{1}{^4C_2} = \frac{1}{6}$

EXERCISE 16.3

1. Which of the following can not be valid assignment of probabilities for outcomes
of sample Space $S = \{\omega_1, \omega_2, \omega_3, \omega_4, \omega_5, \omega_6, \omega_7\}$

<!-- page 467 -->
<table>
<thead>
<tr>
<th>Assignment</th>
<th>\omega_1</th>
<th>\omega_2</th>
<th>\omega_3</th>
<th>\omega_4</th>
<th>\omega_5</th>
<th>\omega_6</th>
<th>\omega_7</th>
</tr>
</thead>
<tbody>
<tr>
<td>(a)</td>
<td>0.1</td>
<td>0.01</td>
<td>0.05</td>
<td>0.03</td>
<td>0.01</td>
<td>0.2</td>
<td>0.6</td>
</tr>
<tr>
<td>(b)</td>
<td>\frac{1}{7}</td>
<td>\frac{1}{7}</td>
<td>\frac{1}{7}</td>
<td>\frac{1}{7}</td>
<td>\frac{1}{7}</td>
<td>\frac{1}{7}</td>
<td>\frac{1}{7}</td>
</tr>
<tr>
<td>(c)</td>
<td>0.1</td>
<td>0.2</td>
<td>0.3</td>
<td>0.4</td>
<td>0.5</td>
<td>0.6</td>
<td>0.7</td>
</tr>
<tr>
<td>(d)</td>
<td>- 0.1</td>
<td>0.2</td>
<td>0.3</td>
<td>0.4</td>
<td>- 0.2</td>
<td>0.1</td>
<td>0.3</td>
</tr>
<tr>
<td>(e)</td>
<td>\frac{1}{14}</td>
<td>\frac{2}{14}</td>
<td>\frac{3}{14}</td>
<td>\frac{4}{14}</td>
<td>\frac{5}{14}</td>
<td>\frac{6}{14}</td>
<td>\frac{15}{14}</td>
</tr>
</tbody>
</table>

2. A coin is tossed twice, what is the probability that atleast one tail occurs?

3. A die is thrown, find the probability of following events:

(i) A prime number will appear,
(ii) A number greater than or equal to 3 will appear,
(iii) A number less than or equal to one will appear,
(iv) A number more than 6 will appear,
(v) A number less than 6 will appear.

4. A card is selected from a pack of 52 cards.

(a) How many points are there in the sample space?
(b) Calculate the probability that the card is an ace of spades.
(c) Calculate the probability that the card is (i) an ace (ii) black card.

5. A fair coin with 1 marked on one face and 6 on the other and a fair die are both
tossed. find the probability that the sum of numbers that turn up is (i) 3 (ii) 12

6. There are four men and six women on the city council. If one council member is
selected for a committee at random, how likely is it that it is a woman?

7. A fair coin is tossed four times, and a person win Re 1 for each head and lose
Rs 1.50 for each tail that turns up.
From the sample space calculate how many different amounts of money you can
have after four tosses and the probability of having each of these amounts.

8. Three coins are tossed once. Find the probability of getting

(i) 3 heads
(ii) 2 heads
(iii) atleast 2 heads
(iv) atmost 2 heads
(v) no head
(vi) 3 tails
(vii) exactly two tails
(viii) no tail
(ix) atmost two tails

9. If $\frac{2}{11}$ is the probability of an event, what is the probability of the event ‘not A’.

10. A letter is chosen at random from the word ‘ASSASSINATION’. Find the
probability that letter is (i) a vowel (ii) a consonant

<!-- page 468 -->
11. In a lottery, a person choses six different natural numbers at random from 1 to 20,
and if these six numbers match with the six numbers already fixed by the lottery
committee, he wins the prize. What is the probability of winning the prize in the
game? [Hint order of the numbers is not important.]

12. Check whether the following probabilities $P(A)$ and $P(B)$ are consistently defined
(i) $P(A) = 0.5$, $P(B) = 0.7$, $P(A \cap B) = 0.6$
(ii) $P(A) = 0.5$, $P(B) = 0.4$, $P(A \cup B) = 0.8$

13. Fill in the blanks in following table:
$$\begin{array}{cccc} \\ & \mathbf{P(A)} & \mathbf{P(B)} & \mathbf{P(A \cap B)} & \mathbf{P(A \cup B)} \\ \\ (i) & \dfrac{1}{3} & \dfrac{1}{5} & \dfrac{1}{15} & \dots \\ \\ (ii) & 0.35 & \dots & 0.25 & 0.6 \\ \\ (iii) & 0.5 & 0.35 & \dots & 0.7 \\ \end{array}$$

14. Given $P(A) = \frac{3}{5}$ and $P(B) = \frac{1}{5}$. Find $P(A \text{ or } B)$, if $A$ and $B$ are mutually exclusive
events.

15. If E and F are events such that $P(E) = \frac{1}{4}$, $P(F) = \frac{1}{2}$ and $P(E \text{ and } F) = \frac{1}{8}$, find

(i) $P(E \text{ or } F)$, (ii) $P(\text{not } E \text{ and not } F)$.

16. Events E and F are such that P(not E or not F) = 0.25, State whether E and F are
mutually exclusive.

17. A and B are events such that $P(A) = 0.42$, $P(B) = 0.48$ and $P(A \text{ and } B) = 0.16$.
Determine (i) $P(\text{not } A)$, (ii) $P(\text{not } B)$ and (iii) $P(A \text{ or } B)$

18. In Class XI of a school 40% of the students study Mathematics and 30% study
Biology. 10% of the class study both Mathematics and Biology. If a student is
selected at random from the class, find the probability that he will be studying
Mathematics or Biology.

19. In an entrance test that is graded on the basis of two examinations, the probability
of a randomly chosen student passing the first examination is 0.8 and the probability
of passing the second examination is 0.7. The probability of passing atleast one of
them is 0.95. What is the probability of passing both?

20. The probability that a student will pass the final examination in both English and
Hindi is 0.5 and the probability of passing neither is 0.1. If the probability of
passing the English examination is 0.75, what is the probability of passing the
Hindi examination?

<!-- page 469 -->
21. In a class of 60 students, 30 opted for NCC, 32 opted for NSS and 24 opted for
both NCC and NSS. If one of these students is selected at random, find the
probability that

(i) The student opted for NCC or NSS.
(ii) The student has opted neither NCC nor NSS.
(iii) The student has opted NSS but not NCC.

Miscellaneous Examples

Example 14 On her vacations Veena visits four cities (A, B, C and D) in a random
order. What is the probability that she visits

(i) A before B? (ii) A before B and B before C?
(iii) A first and B last? (iv) A either first or second?
(v) A just before B?

Solution The number of arrangements (orders) in which Veena can visit four cities A,
B, C, or D is 4! i.e., 24.Therefore, $n$ (S) = 24.
Since the number of elements in the sample space of the experiment is 24 all of these
outcomes are considered to be equally likely. A sample space for the
experiment is

$$\begin{aligned} \\ S = \{ & ABCD, ABDC, ACBD, ACDB, ADBC, ADCB \\ \\ & BACD, BADC, BDAC, BDCA, BCAD, BCDA \\ \\ & CADB, CADB, CBDA, CBAD, CDAB, CDBA \\ \\ & DABC, DACB, DBCA, DBAC, DCAB, DCBA \} \\ \end{aligned}$$

(i) Let the event ‘she visits A before B’ be denoted by E
Therefore, $E = \{ \text{ABCD}, \text{CABD}, \text{DABC}, \text{ABDC}, \text{CADB}, \text{DACB}$
$\text{ACBD}, \text{ACDB}, \text{ADBC}, \text{CDAB}, \text{DCAB}, \text{ADCB} \}$

Thus $P(E)=\frac{n(E)}{n(S)}=\frac{12}{24}=\frac{1}{2}$

(ii) Let the event ‘Veena visits A before B and B before C’ be denoted by F.
Here $F = \{ABCD, DABC, ABDC, ADBC\}$

Therefore, $P(F) = \frac{n(F)}{n(S)} = \frac{4}{24} = \frac{1}{6}$

Students are advised to find the probability in case of (iii), (iv) and (v).

<!-- page 470 -->
Example 15 Find the probability that when a hand of 7 cards is drawn from a well
shuffled deck of 52 cards, it contains (i) all Kings (ii) 3 Kings (iii) atleast 3 Kings.

Solution Total number of possible hands = $^{52}\text{C}_7$

(i) Number of hands with 4 Kings = $^4\text{C}_4 \times ^{48}\text{C}_3$ (other 3 cards must be chosen
from the rest 48 cards)

Hence $P$ (a hand will have 4 Kings) = $\frac{{}^4C_4 \times ^{48}C_3}{{}^{52}C_7} = \frac{1}{7735}$

(ii) Number of hands with 3 Kings and 4 non-King cards = $^4\text{C}_3 \times ^{48}\text{C}_4$

Therefore $P(3 \text{ Kings}) = \frac{{}^4C_3 \times ^{48}C_4}{{}^{52}C_7} = \frac{9}{1547}$

(iii) $P(atleast\ 3\ King) = P(3\ Kings\ or\ 4\ Kings)$
$= P(3\ Kings) + P(4\ Kings)$
$= \frac{9}{1547} + \frac{1}{7735} = \frac{46}{7735}$

Example 16 If A, B, C are three events associated with a random experiment,
prove that
$$P(A \cup B \cup C) = P(A) + P(B) + P(C) - P(A \cap B) - P(A \cap C)$$
$$- P(B \cap C) + P(A \cap B \cap C)$$
Solution Consider $E = B \cup C$ so that
$$P(A \cup B \cup C) = P(A \cup E)$$
$$= P(A) + P(E) - P(A \cap E)$$ ... (1)
Now
$$P(E) = P(B \cup C)$$
$$= P(B) + P(C) - P(B \cap C)$$ ... (2)
Also $A \cap E = A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$ [using distribution property of
intersection of sets over the union]. Thus
$$P(A \cap E) = P(A \cap B) + P(A \cap C) - P[(A \cap B) \cap (A \cap C)]$$

<!-- page 471 -->
$$= \mathrm{P}(\mathrm{A} \cap \mathrm{B})+\mathrm{P}(\mathrm{A} \cap \mathrm{C})-\mathrm{P}[\mathrm{A} \cap \mathrm{B} \cap \mathrm{C}] \quad \dots (3)$$

Using (2) and (3) in (1), we get

$$P[A \cup B \cup C] = P(A) + P(B) + P(C) - P(B \cap C)$$

$$- \mathrm{P}(\mathrm{A} \cap \mathrm{B}) - \mathrm{P}(\mathrm{A} \cap \mathrm{C}) + \mathrm{P}(\mathrm{A} \cap \mathrm{B} \cap \mathrm{C})$$

Example 17 In a relay race there are five teams A, B, C, D and E.

(a) What is the probability that A, B and C finish first, second and third,
respectively.
(b) What is the probability that A, B and C are first three to finish (in any order)
(Assume that all finishing orders are equally likely)

Solution If we consider the sample space consisting of all finishing orders in the first

three places, we will have $^5\text{P}_3$, i.e., $\frac{5!}{(5-3)!} = 5 \times 4 \times 3 = 60$ sample points, each with

a probability of $\frac{1}{60}$.

(a) A, B and C finish first, second and third, respectively. There is only one finishing
order for this, i.e., ABC.

Thus P(A, B and C finish first, second and third respectively) = $\frac{1}{60}$.

(b) A, B and C are the first three finishers. There will be 3! arrangements for A, B
and C. Therefore, the sample points corresponding to this event will be 3! in
number.

So $P$ (A, B and C are first three to finish) $= \frac{3!}{60} = \frac{6}{60} = \frac{1}{10}$

Miscellaneous Exercise on Chapter 16

1. A box contains 10 red marbles, 20 blue marbles and 30 green marbles. 5 marbles
are drawn from the box, what is the probability that
(i) all will be blue? (ii) atleast one will be green?
2. 4 cards are drawn from a well – shuffled deck of 52 cards. What is the probability
of obtaining 3 diamonds and one spade?

<!-- page 472 -->
3. A die has two faces each with number ‘1’, three faces each with number ‘2’ and
one face with number ‘3’. If die is rolled once, determine

(i) P(2)      (ii) P(1 or 3)      (iii) P(not 3)

4. In a certain lottery 10,000 tickets are sold and ten equal prizes are awarded.
What is the probability of not getting a prize if you buy (a) one ticket (b) two
tickets (c) 10 tickets.

5. Out of 100 students, two sections of 40 and 60 are formed. If you and your friend
are among the 100 students, what is the probability that

(a) you both enter the same section?
(b) you both enter the different sections?

6. Three letters are dictated to three persons and an envelope is addressed to each
of them, the letters are inserted into the envelopes at random so that each envelope
contains exactly one letter. Find the probability that at least one letter is in its
proper envelope.

7. A and B are two events such that $P(A) = 0.54$, $P(B) = 0.69$ and $P(A \cap B) = 0.35$.
Find (i) $P(A \cup B)$ (ii) $P(A^{'} \cap B^{'})$ (iii) $P(A \cap B^{'})$ (iv) $P(B \cap A^{'})$

8. From the employees of a company, 5 persons are selected to represent them in
the managing committee of the company. Particulars of five persons are as follows:

<table>
<thead>
<tr>
<th>S. No.</th>
<th>Name</th>
<th>Sex</th>
<th>Age in years</th>
</tr>
</thead>
<tbody>
<tr>
<td>1.</td>
<td>Harish</td>
<td>M</td>
<td>30</td>
</tr>
<tr>
<td>2.</td>
<td>Rohan</td>
<td>M</td>
<td>33</td>
</tr>
<tr>
<td>3.</td>
<td>Sheetal</td>
<td>F</td>
<td>46</td>
</tr>
<tr>
<td>4.</td>
<td>Alis</td>
<td>F</td>
<td>28</td>
</tr>
<tr>
<td>5.</td>
<td>Salim</td>
<td>M</td>
<td>41</td>
</tr>
</tbody>
</table>

A person is selected at random from this group to act as a spokesperson. What is
the probability that the spokesperson will be either male or over 35 years?

9. If 4-digit numbers greater than 5,000 are randomly formed from the digits
0, 1, 3, 5, and 7, what is the probability of forming a number divisible by 5 when,
(i) the digits are repeated? (ii) the repetition of digits is not allowed?

10. The number lock of a suitcase has 4 wheels, each labelled with ten digits i.e.,
from 0 to 9. The lock opens with a sequence of four digits with no repeats. What
is the probability of a person getting the right sequence to open the suitcase?

<!-- page 473 -->
Summary

In this Chapter, we studied about the axiomatic approach of probability. The main
features of this Chapter are as follows:
$\blacklozenge$ Sample space: The set of all possible outcomes
$\blacklozenge$ Sample points: Elements of sample space
$\blacklozenge$ Event: A subset of the sample space
$\blacklozenge$ Impossible event : The empty set
$\blacklozenge$ Sure event: The whole sample space
$\blacklozenge$ Complementary event or ‘not event’ : The set $A'$ or $S - A$
$\blacklozenge$ Event $A$ or $B$: The set $A \cup B$
$\blacklozenge$ Event $A$ and $B$: The set $A \cap B$
$\blacklozenge$ Event $A$ and not $B$: The set $A - B$
$\blacklozenge$ Mutually exclusive event: $A$ and $B$ are mutually exclusive if $A \cap B = \phi$
$\blacklozenge$ Exhaustive and mutually exclusive events: Events $E_1, E_2, ..., E_n$ are mutually
exclusive and exhaustive if $E_1 \cup E_2 \cup ... \cup E_n = S$ and $E_i \cap E_j = \phi$ $\forall i \neq j$
$\blacklozenge$ Probability: Number $P(\omega_i)$ associated with sample point $\omega_i$ such that

(i) $0 \leq P(\omega_i) \leq 1$ (ii) $\sum P(\omega_i)$ for all $\omega_i \in S = 1$

(iii) $P(A) = \sum P(\omega_i)$ for all $\omega_i \in A$. The number $P(\omega_i)$ is called probability
of the outcome $\omega_i$.
$\blacklozenge$ Equally likely outcomes: All outcomes with equal probability
$\blacklozenge$ Probability of an event: For a finite sample space with equally likely outcomes

Probability of an event $P(A) = \frac{n(A)}{n(S)}$, where $n(A) =$ number of elements in

the set $A$, $n(S) =$ number of elements in the set $S$.
$\blacklozenge$ If $A$ and $B$ are any two events, then
$P(A \text{ or } B) = P(A) + P(B) - P(A \text{ and } B)$
equivalently, $P(A \cup B) = P(A) + P(B) - P(A \cap B)$
$\blacklozenge$ If $A$ and $B$ are mutually exclusive, then $P(A \text{ or } B) = P(A) + P(B)$
$\blacklozenge$ If $A$ is any event, then
$P(\text{not } A) = 1 - P(A)$

<!-- page 474 -->
Historical Note

Probability theory like many other branches of mathematics, evolved out of
practical consideration. It had its origin in the 16th century when an Italian physician
and mathematician Jerome Cardan (1501–1576) wrote the first book on the subject
“Book on Games of Chance” (Biber de Ludo Aleae). It was published in 1663
after his death.
In 1654, a gambler Chevalier de Metre approached the well known French
Philosopher and Mathematician Blaise Pascal (1623–1662) for certain dice
problem. Pascal became interested in these problems and discussed with famous
French Mathematician Pierre de Fermat (1601–1665). Both Pascal and Fermat
solved the problem independently. Besides, Pascal and Fermat, outstanding
contributions to probability theory were also made by Christian Huygenes (16291665), a Dutchman, J. Bernoulli (1654–1705), De Moivre (1667–1754), a
Frenchman Pierre Laplace (1749–1827), the Russian P.L Chebyshev (1821–1897),
A. A Markov (1856–1922) and A. N Kolmogorove (1903–1987). Kolmogorov is
credited with the axiomatic theory of probability. His book ‘Foundations of
Probability’ published in 1933, introduces probability as a set function and is
considered a classic.