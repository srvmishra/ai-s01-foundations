# Playlist block 1 of 8 (continue in order)

- **Course:** KIT Optimization Methods for ML and Engineering (WS 20/21)
- **Source:** https://www.youtube.com/results?search_query=KIT+Optimization+Methods+for+Machine+Learning+and+Engineering
- **Date studied:** 10/10/2026

## Key ideas (in my own words)

1. Fitting of model parameters to reduce the prediction error - Empirical Risk Minimization

2. Optimization techniques are used in - 
    - Machine Learning models
    - Control Theory - Model Predictive Control, Closed loop control
    - Computer Vision - Stereo matching, Denoising, Deblurring, etc.

3.  Optimization problems are broadly of 3 types - 
    - minimize cost subject to performance exceeding minimum requirements constraint
    - maximize performance subject to cost constraints
    - trade off performance and cost in a single objective

4. Subgradients are like local first order Taylor expansion.

5. For determining convexity of composition of functions, look at the individual functions - whether they are convex or not, and what position they are in the composition.

## Definitions and results

1. Important terms - 
    - Objective function
    - minimizer
    - domain
    - convex

2. Strictly convex functions have exactly one minima. 

3. **Schwarz's Theorem** - The order of differentiation in mixed partial derivatives does not matter. This implies the Hessian matrix is symmetric.

4. Derivatives - 
    - **Derivative**: For real valued functions of real numbers, it represents the slope of tangent at a point
    - **Gradient**: For scalar fields, it represents the normal vector at a point on its level curves. The components of the gradient at any point define the tangent plane to the surface at that point.

5. **Convex Set** - A set $X$ if convex iff for any two points $x$ and $y$ in it, all the points lying on the straight line joining $x$ and $y$ also lie in set.

$$\forall x, y \in X, \ \alpha x + (1 - \alpha)y \in X \ \forall \alpha \in [0, 1]$$

6. **Convex Hull** - The set of all convex combinations of the points in the set $X = \{x_1, x_2, ..., x_k\}$ is the convex hull of the set $X$.

$$conv X = \{\alpha_1x_1 + \alpha_2x_2 + ... + \alpha_kx_k | i = 1, ..., k, \alpha_i \geq 0, \sum_{i}\alpha_i = 1\}$$

7. $conv X$ is the smallest convex set that contains $X$.

8. **Convex function**: A function $f : X \rightarrow R$ is convex if $X$ is a convex set and (*the below definitions are equivalent*) - 
    - the **epigraph** of the function is a convex set
    $$epi f = \{(x, t) | x \in X, f(x) \leq t\}$$
    - **Jensen's inequality**: $\forall x, y \in X$ and $\alpha \in [0, 1]$
    $$f(\alpha x + (1 - \alpha) y) \leq \alpha f(x) + (1 - \alpha) f(y)$$
    - The function is twice differentiable and its Hessian is **positive semi-definite** for all points in $X$.

9. **Subgradients**:
    - Let $X \subset R^n$ be non-empty, open, and convex, and let $f: X \rightarrow R$ be differentiable everywhere on $X$.
    - Subgradient of $f$ at $x$ is the tangent line that touches $f$ at $x$

    $$\partial_xf(z) = f(x) + \nabla f(x)^T (z-x) \ \forall x, z \in X$$ 

10. **Convex functions and Subgradients**:
    - $f$ is convex over $X$ iff $\ \partial_xf(z) \leq f(z), \ \forall x, z \in X$.
    - $f$ is strictly convex over $X$ iff inequality holds only when $x \neq z$.
    - if $f$ is convex and not differentiable at a point, then $\partial_xf$ represents the set of all subgradients that lie below $f$ but touch $f$ at $x$.

11. $max(x_1, ..., x_n)$ is convex while $min(x_1, ..., x_n)$ is concave. All norms are convex. $||x||^3$ is neither convex nor concave.

12. We can take negative of a concave function and it will be convex.

13. **Composition of convex functions**: Let $f$ be **convex** on $X$ and $g_1, g_2, ..., g_n$ be functions on $X$. $F(g_1(x), g_2(x), ..., g_n(x))$ is convex on $X$ if:
    - $f$ is increasing in argument $i$ and $g_i$ is convex
    - $f$ is decreasing in argument $i$ and $g_i$ is concave
    - $g_i$ is linear
    - these rules are **sufficient but not necessary** for convexity

14. **Cauchy Schwarz inequality**:

    $$h^T\nabla f(x) \leq ||h||\cdot ||\nabla f(x)||$$

    - This gives us the direction of steepest descent as $-\frac{\nabla f(x)}{||\nabla f(x)||}$.

15. **Gradient Descent**:
    $$x^{(k+1)} = x^{(k)} - \alpha \nabla f(x^{(k)})$$

    - Repeat until $||\nabla f(x^{(k)})|| < \varepsilon$
    - Gradient descent alone does not guarantee convergence. A line search step is required to select the step size to avoid overstepping/understepping.
    - Works for differentiable strictly convex functions.

16. **Armijo Backtracking for Line Search**:
    - start with $\alpha = 1$ and a descent direction $d$.
    - while $f(x + \alpha d) > f(x) + \beta(\nabla f(x))^T(\alpha d)$, reduce $\alpha$ as $\alpha \leftarrow p\alpha$
    - stop when a minimum descent steepness is reached. 
    - $\beta = 10^{-4}$ generally. 

17. Parametric models have fixed number of parameters unlike non-parametric models.


## Derivations I worked through

## What confused me (questions for the weekly oral)

- Proof that $conv X$ is the smallest convex set containing $X$.

- Proof that the definitions of convex function are all equivalent.

- Are subgradients defined only for convex functions?

- If we apply concepts of limit and start with Jensen's inequality, then can we arrive at the subgradient definition of convex functions? How is the open set requirement necessary here?

- What are epigraphs? I want a better and a visual explanation? How can it be connected with Jensen's inequality?

- I want to visually understand the Armijo line search even though I got an intuitive feeling. I want a concrete mathematical and graphical perspective.

## Links to code or exercises
