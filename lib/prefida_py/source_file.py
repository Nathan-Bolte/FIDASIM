from numarray import *

def source_file(name):
#+ Returns the source file of the routine `name`
#+ If name is not given then it returns the source file of caller routine
   n_params = 1
   
   if n_params == 0:   
      s = scope_traceback(structure=True)
      nlevels = array(s, copy=0).nelements()
      sfile = s[nlevels - 2].filename
      return file_expand_path(sfile)
   else:   
      help(source_files=True, output=csf) #all compiled source files
      nc = array(csf, copy=0).nelements()
      for i in arange(2, (nc - 1)+(1)):
         has_name = stregex(csf[i], name, fold_case=True) != -1
         if has_name:   
            sfile = stregex(csf[i], "(/[^/ ]*)+/?$", extract=True, fold_case=True)
            return file_expand_path(sfile)
   
   return ''
   

