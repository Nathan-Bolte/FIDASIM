from numarray import *

def error(str, halt=None):
#+#error
#+Print a error message
#+***
#+##Arguments
#+     **str**: message
#+
#+##Keyword Arguments
#+     **halt**: Halt program execution
#+
#+##Example Usage
#+```idl
#+IDL> error, "=("
#+```
   n_params = 1
   _opt = (halt,)
   def _ret():
      _optrv = zip(_opt, [halt])
      _rv = [str]
      _rv += [_o[1] for _o in _optrv if _o[0] is not None]
      return tuple(_rv)
   
   if (halt is not None):   
      message(colored(str, c='r'), level=-1)
   else:   
      print colored('ERROR: ' + str, c='r')
   
   return _ret()

