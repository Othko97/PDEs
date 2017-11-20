"""Main program for solving 2D Galerkin problems, this handles user input etc"""

#########
#IMPORTS#
#########
from TwoDGalerkin import *
import userfuncs as uf
import importlib

###########
#FUNCTIONS#
###########

def newfunc(s):
  """Saves a newly inputted function to a userfuncs.py so it may be used"""
  lhs = s.split('=')[0].strip()
  func = s.split('=')[1].strip()
  name = s.split('(')[0].strip()

  with open("userfuncs.py", "a+") as usrfs:
    if not hasattr(uf, name):
      usrfs.write(f"\n\ndef {lhs}:\n  return {func}")

  importlib.reload(uf)
  

def main():
  run = True
  while run == True:
    command = input(">> ").upper()

    if command == "QUIT":
      run = False
    
    elif command == "APPROX":
      print("Finite Element Method Galerkin Approximation to -u''(x) = RHS on (0,1) with u(0)=0, u'(1)=0")
      RHSfunc = input("Enter RHS(x): ")
      if not hasattr(uf, RHSfunc):
        newfunc(f"RHS(x) = {RHSfunc}")
        rhs = getattr(uf, "RHS")
      else:
        rhs = getattr(uf, RHSfunc)
      
      n = input("Enter n: ")