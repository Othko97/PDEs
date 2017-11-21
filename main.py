"""Main program for solving 2D Galerkin problems, this handles user input etc"""

#########
#IMPORTS#
#########
from TwoDGalerkin import *
import userfuncs as uf
import importlib
import math

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
  with open("userfuncs.py", "w+") as usrfs:
    i = 1
    while i < len(lines):
      line = lines[i]
      if line != f"def {func}(x):\n":
        usrfs.write(line)
        i += 1
      else:
        i += 2



###########
#VARIABLES#
###########
with open("userfuncs.py", "r") as usrfs:
  user_funcs_init = usrfs.readlines()


########################
#DEFINING MAIN FUNCTION#
########################

def main():
  run = True
  step = 0.001
  acc = 4
  
  while run == True:
    command = input("> ").upper()

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
        print(f"\u03B2_{i+1}: {round(B[i][0], acc)}")

      print("\nSave solution as (leave blank to not save): ")
      name = input(">> ")
      if name != "":
        setattr(uf, name, sol_func_BC(n, rhs)) 
      
      print()
    
    elif command == "NEW":
      print("\nEnter function in the form 'f(x) = <algebraic expression>'")
      newfunc(input(">> "))

    elif command == "PLOT":
      print("\nEnter function: ")
      func = input(">> ")
      if not hasattr(uf, func):
        newfunc(f"temp(x) = {func}")
        temp = getattr(uf, "temp")
      else:
        temp = getattr(uf, func)
      plot(temp, step)
    
    elif command == "COMPARE":
      with open("userfuncs.py", "r") as usrfs:
        user_funcs_before = usrfs.readlines()
      print("\nEnter Functions separated by a comma (,):")
      funcs = input(">> ").split(',')
      temps = []
      for i in range(len(funcs)):
        funcs[i] = funcs[i].strip()
        if not hasattr(uf, funcs[i]):
          newfunc(f"temp{i}(x) = {funcs[i]}")
          temps.append(getattr(uf, f"temp{i}"))
        else:
          temps.append(getattr(uf, funcs[i]))
          setattr(uf, f"temp{i}", 0)
      compare_plot(temps, step)
      with open("userfuncs.py", "w+") as usrfs:
        for line in user_funcs_before:
          usrfs.write(line)
      for i in range(len(funcs)):
        delattr(uf, f"temp{i}")
      importlib.reload(uf)

    elif command == "DEL":
      delfunc(input(">> "))
    
    elif command == "EVAL":
      print("\nEnter Functions separated by a comma (,):")
      funcs = input(">> ").split(',')
      temps = []
      for i in range(len(funcs)):
        funcs[i] = funcs[i].strip()
        if not hasattr(uf, funcs[i]):
          newfunc(f"temp{i}(x) = {funcs[i]}")
          temps.append(getattr(uf, f"temp{i}"))
        else:
          temps.append(getattr(uf, funcs[i]))
          setattr(uf, f"temp{i}", 0)
      print(format_table(create_table(temps, step, acc)))
    
    elif command == "SETTINGS":
      print("Enter setting to change:")
      opt = input(">> ").upper()
      if opt == "ACC":
        acc = int(input(">>> "))
      elif opt == "STEP":
        step = float(input(">>> "))
      
      
main()