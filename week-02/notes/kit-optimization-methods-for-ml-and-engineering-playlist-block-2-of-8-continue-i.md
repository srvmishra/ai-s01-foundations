# Playlist block 2 of 8 (continue in order)

- **Course:** KIT Optimization Methods for ML and Engineering (WS 20/21)
- **Source:** https://www.youtube.com/playlist?list=PLdkTDauaUnQpzuOCZyUUZc0lxf4-PXNR5
- **Date studied:** 17/10/2026

## Key ideas (in my own words)

1. Matrix multiplication can be viewed as the dot product of rows of first matrix with the columns of the second matrix. It is associative but not commutative.

2. **Distributions** - 
    - **Poisson**: Number of arrivals in a given interval
    - **Exponential**: Inter arrival time (if inter arrival time is exponentially distributed, then number of arrivals follows the Poisson distribution)
    - **Gaussian**: sum of a large number of random variables

3. **Regression** - 
    - **Parameteric** - limited parameters and expressivity
        - **Linear** (in model weights) - have closed form solution
        - **Non Linear** (in model weights) - no closed form solution, require numerical methods for optimization
    - **Non parametric** - parameters and expressivity grow with the available data

## Definitions and results

1. Linear Algebra Review using Fibonacci Series example:
    - **Recursive Computation** - *Exponential* time complexity
    - **Computation utilizing previous values using an array** - *Linear* time complexity
    - **Matrix Multiplication** - *Logarithmic* time complexity using stored results for matrix exponentiation
    - **Eigendecomposition** - *Constant* time complexity

3. **Eigen Decomposition** - Any **symmetric** matrix $A$ can be written as $A = C\Lambda C^{-1}$ where $\Lambda = diag(\lambda)$ is a diagonal matrix of eigenvalues and $C$ is the matrix of eigenvectors. 

4. Using eigen decomposition, matrix exponentiation can be written as $A^k = C\Lambda^k C^{-1}$. Since $\Lambda$ is a diagonal matrix, exponentiating it costs constant time complexity.

5. If a function $f: R^n \rightarrow R$ is differentiable everywhere, then at the extrema points $x^*$, $\nabla f(x^*) = 0$.
    - This holds in unconstrained optimization problems.
    - Only for strictly convex and concave functions.
    - In the constrained cases, the optimum can be on the edge of the domain $f$ and gradient is not necessarily zero there. The constraint set reduce the domain of $f$ to a subset of $R^n$.

6. **Newton's method** for root finding of a function (solve for $x$, $f(x)=0$):
    - $$x_{k+1} = x_k - \frac{f(x_k)}{\nabla f(x_k)}$$
    - *Newton's method can diverge*
    - if the function $f$ is differentiable, then Newton's method can be used to find the extrema (solve for $x$, $\nabla f(x)=0$).
    - $$x_{k+1} = x_k - [\nabla^2 f(x_k)]^{-1}\nabla f(x_k)$$
    - *Line search is required to ensure convergence.*
    - Newton's method converges in fewer iterations than Gradient descent. But each iteration is computationally expensive and does not scale to high dimensions.
    - Newton's method comes from iterative optimization of the *Taylor approximation* - 
        - **Root finding** - First order Taylor series
        - **Extrema finding** - Second order Taylor series

6. **Super Convergence of Newton's Method**:
    - Assume $f$ is twice differentiable in $R^n$.
    - Assume $\nabla^2f$ is positive definite and lipschitz for some $l>0$
        $$||\nabla^2 f(x) - \nabla^2 f(y)|| < l||x-y||$$
    - Assume the initial point $x_0$ is close to the optimum $||x^* - x_0|| < \frac{1}{2l}$.
    - then the Newton's method converges to $x^*$ with a runtime in the order of $O(\log\log\frac{1}{\epsilon})$ for the error $\epsilon$.

7. Fitting parameteric distributions is done through **likelihood maximization**: 
    - Given a parameteric distribution $p_{\theta}$ with **parameters** $\theta$ and a dataset $D = \{x_1, x_2, ..., x_n\}$ with **iid** samples, the **likelihood** function is defined as 
    $$l_{\theta}(D) = \prod_{i}^n p_{\theta}(x_i)$$
    - Likelihood is not a probability distribution. In some cases $\int_{\theta}l_{\theta}(D)d\theta \neq 1$.
    - **Maximizing likelihood**: parameters $\theta$ that best describe the data
    - Maximizing likelihood = Minimizing negative log likelihood

8. **Linear Regression** approach - 
    - Assume labeled dataset $D = \{(x_i, y_i)\}_{i=1}^n$.
    - Assume $n$ basis functions $\phi_i(x)$. These can be non linear in the data $x$.
    - The model $m_{\theta}$ has parameters $\theta_i$ for each basis function $\phi_i$. The model is given by $m_\theta(x_i) = \sum_i\theta_i\phi_i(x_i) \sim y_i$
    - Select a loss function (eg. MSE or MAE)
    - Optimize it

9. **Selecting Loss functions** - 
    - **MSE**: convex, sensitive to outliers, easy to optimize
    - **MAE**: not sensitive to outliers but requires linear programming to estimate gradients
    - **Huber**: combines outlier robustness of MAE with smoothness and differentiability of MSE. one additional hyperparameter needs to be tuned

10. **Model complexity** and **Regularization** - 
    - increasing parameters (basis functions) can lead to **overfitting**
    - split data into **training** and **testing** sets
    - as model complexity varies, the loss on the train set decreases. 
    - initially the loss on the test set also decreases. the point at which loss on test set starts increasing is the point where **overfitting** starts happening. 
    - having high complexity and avoiding overfitting together - do not let parameters grow too much - add **regularization** - a penalty on the model weights - it is added to the loss function. 
    

## Derivations I worked through

## What confused me (questions for the weekly oral)

- In case of repeated eigenvalues, how do we do the eigen decomposition?

- Can you give some cases where Newton's method will diverge (with and without step size tuning)? Why does this happen? 

- Can you explain how likelihood is not a probability? I got that line from the lecture slides. Why does its integral over all parameters need to be 1?

## Formula cheat sheet (only if you tested out of this item)

## Links to code or exercises
