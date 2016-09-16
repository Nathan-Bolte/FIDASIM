from numarray import *

def warn(str):
#+##`warn, str`
#+Print a warning message
#+###Arguments
#+     **str**: message
#+
#+###Example Usage
#+```idl
#+IDL> warn, "This may be a problem"
#+```
   n_params = 1
   def _ret():  return str
   
   print colored('WARNING: ' + str, c='y')
   
   return _ret()

