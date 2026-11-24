
# An Excerpt from _Biologically Inspired Robots: Snake-Like Locomotors and Manipulators_

This is taken from 

Shigeo Hirose. 1993. _Biologically Inspired Robots: Serpentile Locomotors and Manipulators_. Oxford University Press, Inc., USA.

Which has become increasingly hard to find. If you are looking for a copy, the CMU engineering library has one. This excerpt concerns only the derivation of the serpenoid curve. The rest of the book is filled with really cool details about real snakes, backbone forces and torques, and several unique snake robot mechanisms.

## Nomenclature

This is a subset of the nomenclature used in the book.

| Variable | Definition|
| :---: | :--- |
| $i$   | Index number of joint |
| $l$   | Curve length over a quarter cycle |
| $L$   | Overall length of ACM body |
| $s$   | Distance along axis of ACM body |
| $x(s)$ | x-coordinate of an arbitrary point $\mathrm{Q}$ on the body axis measured from point $\mathrm{O}$|
| $y(s)$ | y-coordinate of an arbitrary point $\mathrm{Q}$ on the body axis measured from point $\mathrm{O}$|
| $J_i$   | Jonint number $i$ |
|$\mathrm{O}$, $\mathrm{P}$| Points on body axis at zero and maximum amplitude, respectively |
| $J_n(\alpha)$   | Bessel function of the first kind |
| $C(s) \\ S(s)$| Fresnel's Integrals |
| $\alpha$ | Winding angle |
| $\alpha_s$ | Angle formed at distance $s$ from point $\mathrm{O}$ beween body axis and direction of travel|
| $\theta_i$ | Angle at joint $J_i$ between adjacent links |
| $\theta(s)$ | Distribution of bending angle along body axis |
| $\delta s$ | Length of line element or of link |
| $\rho_i$ | Curvature at joint J_i |
| $\rho(s)$ | Curvature distribution along body axis |

## 3.3 Formulation of the creeping-gliding curve

In this section, I shall formulate the clothoid curve proposed by Umetani
(eqn (3.8)), and the serpenoid curve which I am newly proposing (eqn (3.17)).

### 3.3.1 Formulation for the clothoid curve

Let us formulate the proposed curve on the basis that the hypothesis that the antagonistic muscle alternately repeat contracting and relaxing movements of uniform speed when the snake is gliding steadily. First, we establish the quarter-cycle of this type of curve in a coordinate system, as in Fig. 3.4. When we make the curve consist of line elements of incremental length $\delta s$ (corresponding to snake vertebrae), as shown in Fig. 3.5, from the fact that the curvature change along the body axis is regular, the banding angle $\theta(s)$ shown in the Fig. 3.5 becomes zero at point $\mathrm{O}$ and a maximum at point $\mathrm{P}$, and at an arbitrary point $\mathrm{Q}$ on the body axis, we have $\theta(s) = A \cdot (s/l)$, where the constant $A$ is given by the fact that the summation of the bending angle $\theta(s)$ over the interval $\mathrm{O}\mathrm{P}$ is equal to the winding angle $\alpha$ of Fig. 3.4, that is,

|  |  |
| :--- | :--- |
|**Fig 3.4** Nomenclature of each section of gliding form, interval $\mathrm{O}\mathrm{P}$ | **Fig 3.5** Nomenclature of unit curve sections.$ |

```math
\alpha = \frac{1}{\delta s} \int_{0}^{l} \theta (s) ~ \mathrm{d}s. \qquad\text{(3.2)}
```

The bending angle $\theta(s)$ is given by

```math
\theta(s) = 2\alpha \left(\frac{\delta s}{l}\right)\left(\frac{s}{l}\right). \qquad\text{(3.3)}
```

Meanwhile, over the interval $\mathrm{O}\mathrm{Q}$, from the equation

```math
\alpha - \alpha_s = \frac{1}{\delta s} \int_0^s
 \theta(s) ~ \mathrm{d}s, \qquad\text{(3.4)}
```

When we substitute eqn (3.3) into eqn (3.4), the winding angle $\alpha_s$ at point $\mathrm{Q}$ expressed as follows:

```math
\alpha_s = \left\{ 1 - \left( \frac{s}{l} \right)^2 \right\} \alpha.  \qquad\text{(3.5)}
```

Since the coordinates $x(s), y(s)-$ the x- and y-coordinates of the arbitrary point $\mathrm{Q}-$ can be considered as integrals of the projected length of the line element of interval $\mathrm{O}\mathrm{Q}$ along the $x$-axis and the $y$-axis, we obtain

```math
\left. 
\begin{aligned}
x(s) &= \int_0^s \cos \alpha_s ~ \mathrm{d}s\\
y(s) &= \int_0^s \sin \alpha_s ~ \mathrm{d}s 
\end{aligned}
\right\}. \qquad\text{(3.6)}
```

When we subsitute eqn (3.5) into eqn (3.6) and expand, we have

```math
\begin{bmatrix}
x(s) \\
y(s)
\end{bmatrix} = 
\begin{bmatrix}
\cos \alpha & -\sin \alpha \\
\sin \alpha & \cos \alpha
\end{bmatrix}
\begin{bmatrix}
1 & 0 \\
0 & -1
\end{bmatrix}
\begin{bmatrix}
\int_0^s \cos \left\{ \left(\frac{u}{l}\right)^2 \alpha \right\} \mathrm{d} u \\
\int_0^s \sin \left\{ \left(\frac{u}{l}\right)^2 \alpha \right\} \mathrm{d} u
\end{bmatrix} \qquad\text{(3.7)}
```

Accordingly, if we transform the variable as $(u / l)^2 \alpha = (\pi/2) t^2$ and express the third tirm of the above equation, using the standard form of Fresnel's integrals of eqn (3.1), we obtain 

```math
\begin{bmatrix}
x(s) \\
y(s)
\end{bmatrix} = 
l \sqrt{\frac{\pi}{2\alpha}}
\begin{bmatrix}
\cos \alpha & -\sin \alpha \\
\sin \alpha & \cos \alpha
\end{bmatrix}
\begin{bmatrix}
1 & 0 \\
0 & -1
\end{bmatrix}
\begin{bmatrix}
C\left(\frac{1}{l}\sqrt{\frac{2\alpha}{\pi}} s\right) \\
C\left(\frac{1}{l}\sqrt{\frac{2\alpha}{\pi}} s\right) 
\end{bmatrix} \qquad\text{(3.8)}
```

Equation (3.8) expresses an operation to transform the portion over curve length $l$ from the origin of the clothoid spiral shown in fig 3.3 to the curve shown in 3.4. First it is turned back relative to the $x$-axis, next the $x, y$ coordinate system is rotated with angle $\alpha$, and finally normalization of the size is effected.

### 3.3.2 Formulation for the serpenoid curve

Let us now work out the formulation for the curve newly defined in Section 3.2, that is, the serpenoid curve whose curvature changes sinusoidally over its length. For the serpenoid curve, the bending angle $\theta(s)$ of Fig. 3.5 changes sinusoidally from zero at point $\mathrm{O}$ to a maximum at point $\mathrm{P}$, so $\theta(s)$ can be expressed as

```math
\theta(s) = A sin \left\{\left(\pi / 2\right) \cdot \left(s / l\right)\right\}
```

Accordingly the constant A follows from the substitution of this $\theta(s)$ into eqn (3.2), and the bending angle $\theta(s)$ of the serpenoid curve is finally expressed as follows:

```math
\theta(s) = \left(\frac{\pi}{2}\right) \alpha \left( \frac{\delta s}{l}\right) \sin \left(\frac{\pi s}{2 l}\right) \qquad\text{(3.9)}
```

If we substitute eqn (3.9) into eqn (3.4), the winding angle a, at the arbitrary point $\mathrm{Q}$ on the body axis of the serpenoid curve is expressed as follows:

```math
\alpha_s = \alpha\cos\left(\frac{\pi s}{2 l}\right) \qquad\text{(3.10)}
```

If we substitute eqn (3.10) into eqn (3.6), we can formulate $x(s)$ and $y(s)$. For simplicity, let us first make some observations about $x(s)$. Substituting eqn (3.10) into eqn (3.6),

```math
x(s) = \int_0^s \cos\left\{\cos\left(\frac{\pi s}{2 l}\right)\right\} \mathrm{d} u \qquad\text{(3.11)}
```

When we transform the integral variable as $v = (\pi/2)\cdot(u/l) + (\pi/2)$, we arrive at

```math
x(s) = \int_0^{\frac{\pi s}{2l} + \frac{\pi}{2}} \cos\left(\alpha \sin v\right) \mathrm{d} v \qquad\text{(3.12)}
```

In eqn (3.12), the following type of expansion is possible:

```math
\begin{align*}
\cos (a \sin v) =& J_o(\alpha) + 2J_2(\alpha) \cos 2v + ...\\
                 & ... + 2J_{2m}(\alpha)\cos 2 mv + ...
\end{align*} \qquad\text{(3.13)}
```

where $J_1(\alpha)$ $(n = 0, 1, 2,...)$ denotes a Bessel function of the first kind and is expressed as

```math
J_n(\alpha) = \left(\frac{\alpha}{2}\right)^n \sum_{m=0}^\infty \frac{(-1)^m}{m!\Gamma(n + m + 1)} \left(\frac{\alpha}{2}\right)^{2m} \qquad\text{(3.14)}
```

Therefore, if we substitute eqn (3.13) into eqn (3.11), we arrive at

```math
x(s) = sJ_0 (\alpha) + \frac{4l}{\pi} \sum_{m=0}^\infty J_{2m} (\alpha)\int_{\frac{\pi}{2}}^{\frac{\pi s}{2l} + \frac{\pi}{2}} \cos 2mv ~ \mathrm{d} v \qquad\text{(3.15)}
```

and from computation of the second term of the right-hand side of eqn (3.15), the Bessel function of $x(s)$ follows. Proceeding in the same way, we substitute eqn (3.10) into $y(s)$ of eqn (3.6), and if we adopt the relation


```math
\begin{align*}
\sin(\alpha \sin v) =& 2J_1 (\alpha) \sin v + ... \\
&... + 2J_{2m+1} (\alpha) ~ \sin (2m-1) v + ...
\end{align*} \qquad\text{(3.16)}
```

With the above transformation of variables, we also can formulate y(s). In other words, $x(s)$ and $y(s)$ are each expressed in the following way, using the curve length s as a parameter:

```math
\left.
\begin{aligned}
x(s) &= sJ_0(\alpha) + \frac{4l}{\pi} \sum _{m=1}^\infty \frac{(-1)^m}{2m} J_{2m}(\alpha) \sin \left(m \pi \frac{s}{l}\right)\\
y(s) &= \frac{4l}{\pi} \sum _{m=1}^\infty (-1)^{m-1} \frac{J_{2m-1}(\alpha)}{2m-1} \sin\left(\frac{2m-1}{2}\pi\frac{s}{l}\right)
\end{aligned}
\right\}\qquad\text{(3.17)}
```


The above equation is the function describing a serpenoid curve, and differs from eqn (3.8) in the previous section, representing a periodic function which describes the whole of a creeping gliding figure. Using eqn (3.14), we can obtain in terms of numerical value the Bessel function of the first kind $J_n(a)$ which occurs in eqn (3.17).
