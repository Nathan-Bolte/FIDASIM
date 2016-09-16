from numarray import *

def get_fidasim_dir():
#+#get_fidasim_dir
#+ Gets FIDASIM install directory
#+***
#+
#+##Example Usage
#+```idl
#+IDL> fida_dir = get_fidasim_dir()
#+```
   n_params = 0
   
   return file_dirname(file_dirname(source_file()))

