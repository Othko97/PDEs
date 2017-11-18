"""A program to give the Finite Element Method Galerkin Approximation to -u''(x)=x^3 on (0,1), u(0) = u(1) = 0
However hopefully in future this will become more general"""

#Imports
import math
import numpy as np
import scipy.integrate as intgr

#Functions
def prod(f, g):
  """Takes the product of two functions i.e fg = f(x)g(x)"""
  return lambda x: f(x) * g(x)

def innerprod(f, g):
  """Take the inner product of functions f, g on H^1_0(0,1)"""
  return intgr.quad(prod(f, g), 0, 1)[0]

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

def generate_galerkin_matrix(n):
  """Generate Galerkin Matrix"""
  dH = generate_dH(n)
  return np.array([([innerprod(dH[i], dH[j]) for j in range(n+1)]) for i in range(n+1)])