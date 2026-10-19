import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

'''
ROSENBROCK FUNCTION UTILITIES
'''
a = 1.0
b = 100.0

def rosenbrock(x):
    return (a - x[0]) ** 2 + b * (x[1] - x[0] ** 2) ** 2

def grad_rosenbrock(x):
    return np.array([-2.0 * (a - x[0]) - 4.0 * b * x[0] * (x[1] - x[0] ** 2), 
                     2.0 * b * (x[1] - x[0] ** 2)])

def hessian_rosenbrock(x):
    return np.array([[12.0*b*x[0]**2 - 4.0*b*x[1] + 2.0, -4.0*b*x[0]],
                    [-4.0*b*x[0], 2.0*b]])

'''
QUADRATIC FUNCTION UTILITIES
'''

def quad_fn(x, k=1.0):
    A = quad_hessian(x, k=k)
    return 0.5 * x @ A @ x

def quad_grad(x, k=1.0):
    A = quad_hessian(x, k=k)
    return A.dot(x)

def quad_hessian(x, k=1.0):
    return np.array([[1.0, 0.0], [0.0, k]])

'''
ARMIJO LINE SEARCH
'''
beta = 1e-4
p = 0.5

def linesearch(x, dir_, fn, grad, max_backtracks=60):
    alpha = 1.0
    val = fn(x)
    gd = grad(x).dot(dir_)
    if gd >= 0:
        raise ValueError("not a descent direction")
    for _ in range(max_backtracks):
        if fn(x + alpha * dir_) <= val + alpha * beta * gd:
            return alpha
        alpha *= p
    raise RuntimeError("line search failed")

'''
GRADIENT DESCENT
'''
min_grad_norm = 1e-6
gd_max_iter = 200000
newton_max_iter = 200
default_step_size = 1.0

def gradient_descent(x_init, fn, grad_fn, hess_fn, max_iter=gd_max_iter, 
                     min_grad_norm=min_grad_norm, default_step_size=default_step_size,
                     use_line_search=True):
    
    xs, fn_vals, grad_norms, step_sizes, condition_nos = [], [], [], [], []
    x = x_init
    
    for i in range(max_iter):
        fn_val = fn(x)
        grad_norm = np.linalg.norm(grad_fn(x))
        
        xs.append(x)
        fn_vals.append(fn_val)
        grad_norms.append(grad_norm)
        
        if grad_norm <= min_grad_norm:
            break  
        
        dir_ = -grad_fn(x)
        hess = hess_fn(x)
        cond_no = np.linalg.cond(hess)
        
        if use_line_search:
            step_size = linesearch(x, dir_, fn, grad_fn)
        else:
            step_size = default_step_size    
            
        step_sizes.append(step_size)
        condition_nos.append(cond_no)
        
        x = x + step_size * dir_
        
    else:
        xs.append(x)
        fn_vals.append(fn_val)
        grad_norms.append(grad_norm)
    
    return xs, fn_vals, grad_norms, step_sizes, condition_nos

'''
NEWTON METHOD WITH SAFEGUARD
'''
initial_mu = 1e-3
beta_1 = 2.0

def newton_method(x_init, fn, grad_fn, hess_fn, max_iter=newton_max_iter, 
                  min_grad_norm=min_grad_norm, default_step_size=default_step_size,
                  use_line_search=True, safeguard=True, get_slopes=False):
    
    xs, fn_vals, grad_norms, step_sizes, condition_nos, slopes = [], [], [], [], [], []
    x = x_init
    num_shifts = 0
    lambdas = []
    
    for i in range(max_iter):
        fn_val = fn(x)
        grad_norm = np.linalg.norm(grad_fn(x))
        hess = hess_fn(x)
        
        xs.append(x)
        fn_vals.append(fn_val)
        grad_norms.append(grad_norm)
        
        if grad_norm <= min_grad_norm:
            break
        
        if safeguard:
            hess_mod, mu = safeguard_hess(hess)
            cond_no = np.linalg.cond(hess_mod)
            dir_ = np.linalg.solve(hess_mod, -grad_fn(x))
            if mu > 0:
                num_shifts += 1
            lambdas.append(mu)
        else:
            cond_no = np.linalg.cond(hess)
            dir_ = np.linalg.solve(hess, -grad_fn(x))
            lambdas.append(0.0)
        
        if use_line_search:
            step_size = linesearch(x, dir_, fn, grad_fn)
        else:
            step_size = default_step_size
        
        step_sizes.append(step_size)
        condition_nos.append(cond_no)
        slopes.append(dir_.dot(grad_fn(x)))
        
        x = x + step_size * dir_
        
    else:
        xs.append(x)
        fn_vals.append(fn_val)
        grad_norms.append(grad_norm)
            
    if get_slopes:
        return xs, fn_vals, grad_norms, step_sizes, condition_nos, lambdas, num_shifts, slopes
    else:
        return xs, fn_vals, grad_norms, step_sizes, condition_nos, lambdas, num_shifts

def safeguard_hess(hess, min_eigenvalue=1e-4, initial_mu=initial_mu, beta=beta_1):
    n = hess.shape[0]
    I = np.eye(n)
    
    try:
        np.linalg.cholesky(hess - min_eigenvalue * I)
        return hess.copy(), 0.0
    except np.linalg.LinAlgError:
        pass
    
    mu = initial_mu
    while True:
        try:
            hess_mod = hess + mu * I
            np.linalg.cholesky(hess_mod - min_eigenvalue * I)
            return hess_mod, mu
        except np.linalg.LinAlgError:
            mu = max(initial_mu, mu * beta)