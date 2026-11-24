# Math background for snake gaits

This is an attempt to unify some of the math across various papers defining snake gaits and to give some intuition for how the math evolved. It's important to remember that there are many different ways to generate the same backbone curvature for a snake robot, and that this is document is not organized moving from basic->advanced. It's more a toolbox of methods for reasoning about snake gaits. You may notice changes in terminology, especially around the two backbones. $even$, $odd$, $lateral$, $dorsal$, $a$ and $b$ are all used fairly interchangably. It's important to remember that unlike a real snake, a snake robot doesn't really have an up, down left or right. I've tried to unify the terminology where I can without changing the meaning of the paper.

## 1. Serpenoid curve

Serpenoid curves were first described by Shigeo Hirose to control his Active Cord Mechanism (ACM) robots. [^SerpenoidCurve] You can read a detailed breakdown of how the original serpenoid function was derived [here](Hirose.md)

In the biorobotics lab we use a function derived from Hirose's work called the compound serpenoid function

```math
\begin{aligned}
angle(t, i) = \begin{cases}
offset_{even} + amplitude_{even} * sin(\theta), & i=even, \\
offset_{odd} + amplitude_{odd} * sin(\theta + \delta), & i=odd,
\end{cases} && \qquad\text{(1.2)}
\\
\\
\theta = \left(\frac{d \theta}{di} * i + \frac{d \theta}{dt} * t \right) && \qquad\text{(1.3)}
\end{aligned}
```

Where $i$ is the joint number, $\delta$ is the phase offset between the two orthogonal waves and $t$ is the gait phase. The terms $d \theta/di$ and $d \theta/dt$ are often referred to as the spatial frequency and time frequency.[^DifferentiableGaits]

## 2. Continous representations

When dealing with serpenoid curves it is often easier to do math on them if they are idealized continous curves instead of a collection of discrete joints.

### Frenet-Serret equations [^Frenet][^Serret]

The most common approach is to begin by using Frenet-Serret curves, which integrate curvature expressed as tangent, normal, and binormal unit vectors along the length of a curve. These were used in the original derivation of serpenoid gaits and lend themselves to modeling serpenoid curves, as joint angles can be mapped to continous curvatures along the backbone.

The Frenet-Serret equations define a non-degenerate (nonzero curvature) three dimensional curve as a moving frame composed of three vectors:

* $\mathbf{T}$ is the unit vector tangent to the curve,
* $\mathbf{N}$ is the normal unit vector, or the derivative of $\mathbf{T}$ with respect to the arc lenth of the curve. 
* $\mathbf{B}$ is the binormal unit vector, which is the cross product of $\mathbf{T}$ and $\mathbf{N}$

The Frenet–Serret formulas are:

$$
\begin{aligned}
\frac{d\mathbf{T}}{ds} &= \kappa(s)\mathbf{N}
\\
\\
\frac{d\mathbf{T}}{ds} &= -\kappa(s)\mathbf{N} + \tau(s)\mathbf{B},
\\
\\
\frac{d\mathbf{T}}{ds} &= - \tau(s)\mathbf{N},
\end{aligned}
$$

Where $\frac{d}{ds}$ is the derivative with respect to arc length $\kappa$ is curvature and $\tau$ is torsion. Since $\mathbf{T}$, $\mathbf{N}$ and $\mathbf{B}$ are orthonormal, you can imagine moving along the curve in time using these three vectors as a frame of reference, moving in the direction of $\mathbf{T}$ and steering by rotating the frame. In an arc, $\kappa(s)$ is constant and $\tau(s) = 0$. In a helix, both $\kappa(s)$ and $\tau(s)$ are constant.

Chirikjian and Burdick extended Frenet-Serret curves to model the motion of Variable Geometry Truss Structures (VGT), hyper-redundant manipulators that are composed of a cascade of parallel platforms. Since Frenet-Serret curves only specify a curve up to rigid-body displacement, they added another parameter called a backbone reference set, which defined a series of rotations around the backbone that allowed them to differentiate between two robot configurations that had identical backbone curves but different twists between each of the platforms. [^VGT]

This approach worked well for continous robots that could twist between joints but was not a good model for serpenoid robots such as Hirose's ACM. Snake robots like his and ours cannot twist freely between one joint and another, but can only rotate along one degree of freedom with respect to each other. Yamada and Hirose proposed a model called the Bellows Model, named after flexible ridged hose used in plumbing which can be bent but not twisted.

### Bellows Model [^Bellows]

The Bellows Model allows allows us to specify the rotation about the backbone while retaining the kinematic constraints of a snake robot. Instead of introducing a function to produce arbitrary rotations like Chirikjian and Burdick did, Yamada and Hirose instead propose adding a second backbone curvature term. 

If we write the Frenet-Serret formulas in their matrix form

$$
\begin{bmatrix}
\mathbf{T}'\\
\mathbf{N}'\\
\mathbf{B}'
\end{bmatrix} = 
\begin{bmatrix}
         0 & \kappa(s) & 0\\
-\kappa(s) &         0 & \tau(s) \\
         0 &  -\tau(s) & 0
\end{bmatrix}
\begin{bmatrix}
\mathbf{T}\\
\mathbf{N}\\
\mathbf{B}
\end{bmatrix}
$$

Yamada and Hirose propose the following change:

$$
\begin{bmatrix}
\mathbf{T}'\\
\mathbf{A}'\\
\mathbf{B}'
\end{bmatrix} = 
\begin{bmatrix}
         0 & \kappa_b(s) & -\kappa_a(s)\\
-\kappa_b(s) &         0 & \tau(s) \\
 \kappa_a(s) &  -\tau(s) & 0
\end{bmatrix}
\begin{bmatrix}
\mathbf{T}\\
\mathbf{A}\\
\mathbf{B}
\end{bmatrix}
$$

Notice that $\mathbf{A}$ and $\mathbf{B}$ are no longer the normal and binormal vectors, which are fixed for a given curve. Instead, these vectors can vary arbirtrarily, allowing us to specify a arbitrary curve with arbitrary frames along the length of S as well as represent curves with zero curvature. In terms of snake anatomy, one can think of $\mathbf{A}$ or $\mathbf{B}$ defining the back or belly of the snake, though the choice is arbitrary. In the bellows model, we do not twist along the backbone of the snake, so we can elimiate the $\tau(s)$ terms entirely.

$$
\begin{bmatrix}
\mathbf{T}'\\
\mathbf{A}'\\
\mathbf{B}'
\end{bmatrix} = 
\begin{bmatrix}
         0 & \kappa_b(s) & -\kappa_a(s)\\
-\kappa_b(s) &         0 & 0 \\
 \kappa_a(s) &         0 & 0
\end{bmatrix}
\begin{bmatrix}
\mathbf{T}\\
\mathbf{A}\\
\mathbf{B}
\end{bmatrix}
$$

Yamada and Hirose go on to prove that this bellows model can reproduce any curve that the Frenet-Serret mechanism is capable of producing as well as several that the Frenet-Serret mechanism cannot. It also perfectly reproduces the kinematics of our snake robots, since each joint has one degree of freedom in the lateral or dorsal direction.

### Rolling and helical Gaits [^ModelingRolling]

Our group also applied these continous curve methods to helical gaits. Starting from the Bellows Model, the curvature of the backbone curve $\kappa(s)$ where $s$ is arc length is split into dorsal curvature $\kappa_d(s)$ and lateral curvature $\kappa_l(s)$:

```math
\begin{aligned}
\kappa_d(s) = \kappa(s) \cos (\phi(s)) && \text{dorsal} && \qquad\text{(1)} \\
\kappa_l(s) = \kappa(s) \sin (\phi(s)) && \text{lateral} && \qquad\text{(2)} \\
\end{aligned}
```

Here $\phi(s)$ is the rolling offset defined as

```math
\phi(s) = \phi_0 + \int_0^s \tau(s)ds \qquad\text{(3)}
```

where $\phi_0$ is the initial angle offset and $\tau(s)$ is the torsion along the backbone curve. Using the Bellows Model, rolling along the curvature of the backbone (as is done in pipe climbing for example) can be acheived by defining the initial angle offset $\phi_0(t)$ as a function of time.

The corresponding joint angles for dorsal and lateral curvatures $\kappa_d(s)$ and $\kappa_l(s)$ can be computed by integrating each curvature over the length of two modules, since joints alternately rotate in the dorsal and lateral plane. Formally, let $m$ denote the length of one module and $i$ denote the index of a joint. The the $i$-th joint angle $\alpha_i$ can be computed by:

```math
\begin{aligned}
\alpha_d(i) = \int_{(i-1)m}^{(i+1)m} \kappa_d(s)ds && \text{dorsal} \\
\alpha_l(i) = \int_{(i-1)m}^{(i+1)m} \kappa_l(s)ds && \text{lateral} \\
\end{aligned} \qquad\text{(4)}
```

#### Computation reduction

Without loss of generality, we can set $\phi_0(t) = t$. Correspondingly, the dorsal and lateral curvatures $\kappa_d(s,t)$ and $\kappa_l(s,t)$ as well as the resulting joint angles $\alpha(i, t)$ are also time dependent. At each timestep the curvature integration  is computed and the joint angles are updated. Though the curvature integration is quite fast, it still slows down the generation of control inputs. The following steps allow us to simplify this computation and leads to some insights into compound serpenoid curves.


Substituting Eqn. 2 into Eqn. 1 results in:

```math
\begin{aligned}
\kappa_d(s,t) &= \kappa(s)\cos\Big(t + \smallint\nolimits_{0}^{s}\tau(s)ds\Big) \\
              &= \cos\Bigl(t\Bigr)\kappa(s)\cos\Bigl(\smallint\nolimits_{0}^{s}\tau(s)ds\Bigr) - \sin\Bigl(t\Bigr)\kappa(s)\sin\bigl(\smallint\nolimits_{0}^{s}\tau(s)ds\bigr)\Big)
\end{aligned} \qquad\text{(5)}
```

For clarity, we introduce two variables, $\alpha_{\sin}(i)$ and $\alpha_{\cos}(b)$:

```math
\begin{aligned}
\alpha_{\sin}(i) = \int_{(i-1)m}^{(i+1)m}\kappa(s)\sin\Bigl
(\smallint\nolimits_{0}^{s}\tau(s)ds\Bigr) ds && \qquad\text{(6)} \\
\\
\alpha_{\cos}(i) = \int_{(i-1)m}^{(i+1)m}\kappa(s)\cos\Bigl
(\smallint\nolimits_{0}^{s}\tau(s)ds\Bigr)ds && \qquad\text{(7)}\\
\end{aligned}
```

Subsituting Eqn. 4 into Eqn. 3 results in

```math
\alpha_d(t,i) = \cos(t) \alpha_{\cos}(i) - \sin(t) \alpha_{\sin}(i) \qquad\text{(8)}
```

We can similarly calculate the joint angles for the lateral backbone as

```math
\alpha_l(t,i) = \sin(t) \alpha_{\cos}(i) + \cos(t) \alpha_{\sin}(i) \qquad\text{(9)}
```

Notice first that the time dependent variable $t$ can be taken out of the integral since it does not depend on arc length $s$. This also means that we can pre-compute the necessary integrals and only have to calculate the $t$ terms every timestep.

#### Rolling

For rolling, we form the robot into an arc of radius $r$ and rotate along the backbone. The parameters of this are can be specified in terms of the curvature $\kappa(s) = 1 / r$ and torsion $\tau(s) = 0$. Substituting into Eqn. 6 and Eqn. 7 results in $\alpha_{\sin} = 0$ and $\alpha_{\cos} = 2m/r$. If we substitute those values into Eqn. 8 and Eqn. 9 we are left with $\alpha_d(t, i) = \frac{2m}{r} \cos(t)$ and $\alpha_l(t, i) = \frac{2m}{r} \sin(t)$ which perfectly match the compound serpenoid parameterization but have the benefit of being expressed in terms of the radius. The equivalent compound serpenid parameters are

$amplitude_{even} = amplitude_{odd} = \frac{2m}{r}$

$\frac{d\theta}{dn} = 0$

$\delta = \frac{\pi}{2}$

#### Rolling helix

For a rolling helix, let $r$ be the radius of the helix and $2\pi p$ be the axial pitch (distance between consecutive arcs of the spiral). The curvature of the helix is:

```math
\kappa(s) = \frac{r}{r^2 + p^2} = \bar{\kappa}
```

and the torsion is

```math
\tau(s) = \frac{p}{r^2 + p^2} = \bar{\tau}
```

substituting these into  Eqn. 6:

```math
\begin{aligned}
\alpha_{\sin}(i) =& \int_{(i-1)m}^{(i+1)m}\kappa(s)\sin(\bar{\tau} s)ds
\\
\\
                 =& \frac{\bar{\kappa}}{\bar{\tau}}\Big(\cos(\bar{\tau}m \cdot (i+1)) - \cos(\bar{\tau}m \cdot (i-1))\Big)
\\
\\
                 =& \frac{2\bar{\kappa}}{\bar{\tau}}\sin(\bar{\tau}m)\sin(\bar{\tau}mi) \\
\end{aligned}
```

Similarly for Eqn. 7

```math
\alpha_{\cos}(i) = \frac{2\bar{\kappa}}{\bar{\tau}}\sin(\bar{\tau}m)\cos(\bar{\tau}mi)
```

Which if substituted into Eqn. 8 and Eqn. 9 results in

```math
\begin{aligned}
\alpha_d(t,i) = \frac{2\bar{\kappa}}{\bar{\tau}}\sin(\bar{\tau}m)\cos(t + \bar{\tau}mi)
\\
\\
\alpha_l(t,i) = \frac{2\bar{\kappa}}{\bar{\tau}}\sin(\bar{\tau}m)\sin(t + \bar{\tau}mi)
\end{aligned}
```

which perfectly match the compound serpenoid parameterization but have the benefit of being expressed in terms of the radius and axial pitch. The equivalent compound serpenoid parameters are

$amplitude_{even} = amplitude_{odd} = \frac{2\bar{\kappa}}{\bar{\tau}}\sin(\bar{\tau}m)$

$\frac{d\theta}{dn} = \bar{\tau}m$

$\delta = \frac{\pi}{2}$

## 3. Curve fitting

Once we have idealized smooth curves, it might be tempting to go the other way and fit a discrete robot to an idealized curve. This paper by Hatton and Choset [^ChainFitting] uses annealed chain fitting to find a set of joint angles that fit an arbitrary curve and then tries to extract backbone curve parameters from a sequence of fitted curves. This allows the authors to derive parameters for gaits such as helical rolling or sidewinding without an exact analytical solution. Later, the chain fitting portion of this approach was used to derive joint angles for conical sidewinding, in which the robot is able to turn while moving laterally.[^ConicalSidewinding]

## 3. Extended gait equation [^ExtendedGaitEq]

If we allow amplitude to be a function of $i$ we can produce conical sidewinding without having to do expensive curve fitting operations and control the radius of turning with a single parameter.

## 2. Virtual Chassis [^VirtualChassis]

We start with 3D module positions $\mathbf{p}_i$ measured from the center of mass $\bar{\mathbf{p}}$

```math
\begin{aligned}
\bar{\mathbf{p}} = \begin{bmatrix}\bar{x} & \bar{y} & \bar{z}\end{bmatrix} && \qquad\text{(3.1)}
\\
\\
\mathbf{p}_i = \begin{bmatrix}x_i -\bar{x} & y_i - \bar{y} & z_i - \bar{z}\end{bmatrix}^T \in \mathbb{R}^3  && \qquad\text{(3.2)}
\\
\\
\mathbf{P} = \begin{bmatrix} \mathbf{p}_1^T \\ \vdots \\~ \mathbf{p}_n^T ~\end{bmatrix} && \qquad\text{(3.3)}
\\
\end{aligned}
```
We then calculate the singular value decomposition of $\mathbf{P}$
```math
\begin{aligned}
\mathbf{USV} = \mathbf{P}  && \qquad\text{(3.4)}
\\
\end{aligned}
```

We stablilize $\mathbf{V}$ to create $\hat{\mathbf{V}}$ by enforcing positive dot products in first and second singular vectors across consecutive time steps to calculate the homogeneous transform that describes the pose of the virtual chassis in the initial coordinate frame.

```math
\begin{aligned}
\mathbf{T} = \begin{bmatrix}\hat{\mathbf{V}} & \bar{\mathbf{p}} \\ 0 & 1\end{bmatrix}  && \qquad\text{(3.5)}
\end{aligned}
```

This works for gaits such as sidewinding where the 'center' of the robot is relatively well defined, but for gaits such as rolling helix, we need a better estimate of the centerline of the robot. In order to do so we use the solution from SVD as a starting point for a Nelder-Mead simplex search. Intuitively, we would like to minimize the difference of the distances of all the modules in snake to some centerline. The distance $d_i$ of a point $\mathbf{p}_i$ to a line defined by $\mathbf{a}+\mathbf{v}s$ is defined as:

## Bibliography

[^SerpenoidCurve]: S. Hirose. 1993. _Biologically Inspired Robots: Serpentile Locomotors and Manipulators_. Oxford University Press, Inc., USA, doi: [10.5555/562623](https://doi.org/10.5555/562623).

[^DifferentiableGaits]: K. Lipkin et al., "Differentiable and piecewise differentiable gaits for snake robots," 2007 IEEE/RSJ International Conference on Intelligent Robots and Systems, San Diego, CA, USA, 2007, pp. 1864-1869, doi: [10.1109/IROS.2007.4399638](https://doi.org/10.1109/IROS.2007.4399638).

[^Frenet]: F. Frenet, "Sur les courbes à double courbure," Journal de Mathématiques Pures et Appliquées (1852), pp. 437-447. ISSN: [0021-7874](https://www.numdam.org/item/JMPA_1852_1_17__437_0.pdf)

[^Serret]: J. Serret, "Sur quelques formules relatives à la théorie des courbes à double courbure," Journal de Mathématiques Pures et Appliquées (1851), pp 193-207. ISSN: [0021-7874](https://www.numdam.org/item/JMPA_1851_1_16__193_0.pdf)

[^VGT]:G. S. Chirikjian and J. W. Burdick, "A modal approach to hyper-redundant manipulator kinematics," in IEEE Transactions on Robotics and Automation, vol. 10, no. 3, pp. 343-354, June 1994, doi: [10.1109/70.294209](https://doi.org/10.1109/70.294209).

[^Bellows]: H. Yamada and S. Hirose, "Study on the 3D shape of active cord mechanism," Proceedings 2006 IEEE International Conference on Robotics and Automation, 2006. ICRA 2006., Orlando, FL, USA, 2006, pp. 2890-2895, doi: [10.1109/ROBOT.2006.1642140](https://doi.org/10.1109/ROBOT.2006.1642140).

[^ModelingRolling]: W. Zhen, C. Gong and H. Choset, "Modeling rolling gaits of a snake robot," 2015 IEEE International Conference on Robotics and Automation (ICRA), Seattle, WA, USA, 2015, pp. 3741-3746, doi: [10.1109/ICRA.2015.7139719](https://doi.org/10.1109/ICRA.2015.7139719).

[^ChainFitting]: Hatton, R.L., Choset, H. Generating gaits for snake robots: annealed chain fitting and keyframe wave extraction. Auton Robot 28, 271–281 (2010). https://doi.org/10.1007/s10514-009-9175-2


[^ConicalSidewinding]: C. Gong, R. L. Hatton and H. Choset, "Conical sidewinding," 2012 IEEE International Conference on Robotics and Automation, Saint Paul, MN, USA, 2012, pp. 4222-4227, doi: [10.1109/ICRA.2012.6225377](https://doi.org/10.1109/ICRA.2012.6225377).

[^ExtendedGaitEq]: C. Gong, M. J. Travers, Xiaozhou Fu and H. Choset, "Extended gait equation for sidewinding," 2013 IEEE International Conference on Robotics and Automation, Karlsruhe, Germany, 2013, pp. 5162-5167, doi: [10.1109/ICRA.2013.6631315](https://doi.org/10.1109/ICRA.2013.6631315).



[^VirtualChassis]: D. Rollinson and H. Choset, "Virtual chassis for snake robots," 2011 IEEE/RSJ International Conference on Intelligent Robots and Systems, San Francisco, CA, USA, 2011, pp. 221-226, doi: [10.1109/IROS.2011.6094645](https://doi.org/10.1109/IROS.2011.6094645).
