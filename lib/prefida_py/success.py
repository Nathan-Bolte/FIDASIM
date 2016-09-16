from numarray import *

def success(str):
#+##`success, str`
#+Print a success message
#+###Arguments
#+     **str**: message
#+
#+###Example Usage
#+```idl
#+IDL> success, "Yay!!!"
#+```
   n_params = 1
   def _ret():  return str
   
   print colored('SUCCESS: ' + str, c='g')
   
   return _ret()

