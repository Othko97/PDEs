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
with open("userfuncs.py", "r") as usrfs:
  user_funcs_init = usrfs.readlines()
step = 0.001

########################
#DEFINING MAIN FUNCTION#
########################

def main():
  run = True

  while run == True:
    command = input(">> ").upper()

    if command == "QUIT":
      run = False
      with open("userfuncs.py", "w+") as usrfs:
        for line in user_funcs_init:
          usrfs.write(line)
    
    elif command == "APPROX":
      print("\nFinite Element Method Galerkin Approximation to -u''(x) = RHS on (0,1) with u(0)=0, u'(1)=0")
      RHSfunc = input("Enter RHS(x): ")
      if not hasattr(uf, RHSfunc):
        newfunc(f"RHS(x) = {RHSfunc}")
        rhs = getattr(uf, "RHS")
      else:
        rhs = getattr(uf, RHSfunc)
      
      n = int(input("Enter n: "))
      
      B = solve_BC(n, rhs)

      print(u"\n Given basis functions h_i(x), u(x) = \u03A3(\u03B2_i * h_i)")

      for i in range(0, n):
        print(f"\u03B2_{i+1}: {B[i][0]}")

      print("\nSave solution as (leave blank to not save): ")
      name = input(">>> ")
      if name != "":
        setattr(uf, name, sol_func_BC(n, rhs)) 
      
      print()
    
    elif command == "NEW":
      print("\nEnter function in the form 'f(x) = <algebraic expression>'")
      newfunc(input(">>> "))

    elif command == "PLOT":
      print("\nEnter function: ")
      func = input(">>> ")
      if not hasattr(uf, func):
        newfunc(f"temp(x) = {func}")
        temp = getattr(uf, "temp")
      else:
        temp = getattr(uf, func)
      plot(temp, step)
    
    elif command == "COMPARE":
      print("\nEnter Functions separated by a comma (,):")
      funcs = input(">>> ").split(',')
      temps = [0,0]
      for i in range(2):
        funcs[i].strip()
        if not hasattr(uf, funcs[i]):
          newfunc(f"temp{i}(x) = {funcs[i]}")
          temps[i] = getattr(uf, f"temp{i}")
        else:
          temps[i] = getattr(uf, funcs[i])
      compare_plot(temps[0], temps[1], step)

      

main()