"""A program to give the Finite Element Method Galerkin Approximation to -u''(x)=f(x) on (0,1), u(0) = u(1) = 0
However hopefully in future this will become more general"""


#########
#IMPORTS#
#########

import math
import numpy as np
import scipy.integrate as intgr
import matplotlib.pyplot as plt
import matplotlib.cm as cmx

###########
#FUNCTIONS#
###########


#Basic function operations, inner & scalar products 
def add(f, g):
  """Takes the sum of two functions i.e. f+g = f(x) + g(x)"""
  return lambda x: f(x) + g(x)

def prod(f, g):
  """Takes the product of two functions i.e fg = f(x)g(x)"""
  return lambda x: f(x) * g(x)

def innerprod(f, g):
  """Take the inner product of functions f, g on H^1_0(0,1)"""
  return intgr.quad(prod(f, g), 0, 1)[0]

def scalarprod(a, f):
  """Take scalar product of a scalar a and a function f i.e. af = af(x)"""
  return lambda x: a * f(x)

def compare(f, g, step):
  """Returns an array of the differences between f(x_i), g(x_i) where x_i= i * step"""
  return [abs((f(step*x) - g(step*x))) for x in range(0, int(1/step))]

#Functions on lists of functions (can be thought of as vectors in H_k)
def multiscalarprod(A, F):
  """Take dot product of a list of scalars and a list of functions"""
  return [scalarprod(a, f) for a,f in zip(A, F)]

def fsum(F):
  """Returns sum of functions in a list"""
  f = lambda x: 0
  for g in F:
    f = add(f, g)
  return f


#Generators for basis H_n
def generate_x_n(n):
  """Generate the values of x_n which space (0, 1) into n even intervals"""
  return [i/n for i in range(n+1)]

def generate_h_j(j, X_n):
  """Generate functions h_j, linear and continuous on (x_(j-1), x_(j+1))"""
  n = len(X_n)-1
  def h_j(x):
    if j == 0:
      if x >= X_n[0] and x < X_n[1]:
        return n*(X_n[1]-x)
      else:
        return 0

    elif j == n:
      if x > X_n[n-1] and x <= X_n[n]:
        return n*(x - X_n[n-1])
      else:
        return 0

    else:
      if x > X_n[j-1] and x < X_n[j]:
        return n*(x - X_n[j-1])
      elif x >= X_n[j] and x < X_n[j+1]:
        return n*(X_n[j+1] - x)
      else:
        return 0
  
  return h_j

def generate_dh_j(j, X_n):
  """Generate derivative of h_j"""
  n = len(X_n)-1
  def dh_j(x):
    if j == 0:
      if x >= X_n[0] and x < X_n[1]:
        return -n
      else:
        return 0

    elif j == n:
      if x > X_n[n-1] and x <= X_n[n]:
        return n
      else:
        return 0

    else:
      if x > X_n[j-1] and x < X_n[j]:
        return n
      elif x >= X_n[j] and x < X_n[j+1]:
        return -n
      else:
        return 0
    
  return dh_j

def generate_H(n):
  """Generate array of h_j for j = 0,1,...,n"""
  X_n = generate_x_n(n)
  return [generate_h_j(j, X_n) for j in range(n+1)]

def generate_dH(n):
  """Generate array of h_j for j = 0,1,...,n"""
  X_n = generate_x_n(n)
  return [generate_dh_j(j, X_n) for j in range(n+1)]


#Solving Equations without boundary conditions applied
def generate_gal_mat(n):
  """Generate Galerkin Matrix"""
  dH = generate_dH(n)
  return np.array([([innerprod(dH[i], dH[j]) for j in range(n+1)]) for i in range(n+1)])

def find_rhs(n, f):
  """Generate right hand side vector"""
  H = generate_H(n)
  return np.array([[innerprod(f, H[i])] for i in range(n+1)])

def solve(n, f):
  """Solves the System of Linear Equations generated by the Galerkin Matrix"""
  return np.dot(np.linalg.inv(generate_gal_mat(n)), find_rhs(n, f))

def sol_func(n, f):
  """Returns the approximation function obtained by multiplying basis by coefficients"""
  H = generate_H(n)
  betas = [i[0] for i in solve(n, f).tolist()]
  return fsum(multiscalarprod(betas, H))


#Solving Equations with boundary conditions applied
def generate_gal_mat_BC(n):
  """Generate Galerkin Matrix with u(0)=u'(1)=0 applied"""
  dH = generate_dH(n)
  return np.array([([innerprod(dH[i], dH[j]) for j in range(1, n+1)]) for i in range(1, n+1)])

def find_rhs_BC(n, f):
  """Generate right hand side vector with u(0)=u'(1)=0 applied"""
  H = generate_H(n)
  return np.array([[innerprod(f, H[i])] for i in range(1, n+1)])

def solve_BC(n, f):
  """Solves the System of Linear Equations generated by the Galerkin Matrix with u(0)=u'(1)=0 applied
  Returns array of coefficients of h_js"""
  return np.dot(np.linalg.inv(generate_gal_mat_BC(n)), find_rhs_BC(n, f))

def sol_func_BC(n, f):
  """Returns the approximation function obtained by multiplying basis by coefficients with u(0)=u'(1)=0 applied"""
  H = generate_H(n)[1:n+1]
  betas = [i[0] for i in solve_BC(n, f).tolist()]
  return fsum(multiscalarprod(betas, H))

#Plotting
def plot(f, step):
  X = [step*x for x in range(int(1/step)+1)]
  Y = [f(x) for x in X]

  plt.plot(X, Y)
  plt.show()

def compare_plot(F, step):
  X = [step*x for x in range(int(1/step)+1)]
  Y = []
  for f in F:
    Y.append([f(x) for x in X])
  for i in range(len(Y)):
    plt.plot(X, Y[i])

  plt.xlabel('x')
  plt.ylabel('y')
  plt.show()