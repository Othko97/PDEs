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
  lhs  = s.split('=')[0].strip()
  name = lhs.split('(')[0].strip()
  var  = lhs.split('(')[1].split(')')[0].strip()
  lhs  = lhs.replace(var, 'x')
  func = s.split('=')[1].strip().replace(var, 'x')


  with open("userfuncs.py", "a+") as usrfs:
    if not hasattr(uf, name):
      usrfs.write(f"\n\ndef {lhs}:\n  return {func}")
    else:
      delfunc(name)
      usrfs.write(f"\n\ndef {lhs}:\n  return {func}")

  importlib.reload(uf)

def delfunc(func):
  """Deletes a user defined function from userfuncs.py"""
  print("deleting??")
  with open("userfuncs.py", "r") as usrfs:
    lines = usrfs.readlines()
  with open("userfuncs.py", "w") as usrfs:
    count = 4
    for i in range(len(lines)-1):
      line = lines[i]
      if line != f"def {func}(x):\n":
        usrfs.write(line)
      else:
        i += 3



###########
#VARIABLES#
###########




########################
#DEFINING MAIN FUNCTION#
########################

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
      
      n = int(input("Enter n: "))
      
      B = solve_BC(n, rhs)

      print(u"\n Given basis functions h_i(x), u(x) = \u03A3(\u03B2_i * h_i)")

      for i in range(1, n+1):
        print(f"\u03B2_{i}: {B[i][0]}")
    
    elif command == "NEW":
      print("\nEnter function in the form 'f(x) = <algebraic expression>'")
      newfunc(input(">>> "))

    elif command == "PLOT":
      print("\nEnter function: ")
      func = input(">>> ")
      if not hasattr(uf, RHSfunc):
        newfunc(f"RHS(x) = {RHSfunc}")
        rhs = getattr(uf, "RHS")
      else:
        rhs = getattr(uf, RHSfunc)

main()