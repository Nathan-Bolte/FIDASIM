from numarray import *

def get_version(fidasim_dir):
#+#get_version
#+ Gets FIDASIM version number from git.
#+ Falls back to reading VERSION file when git is not available
#+***
#+##Input Arguments
#+    **fidasim_dir**: FIDASIM install directory
#+
#+##Example Usage
#+```idl
#+IDL> version = get_version(getenv("FIDASIM_DIR"))
#+```

   n_params = 1
   
   version = ''
   git_dir = fidasim_dir + '/.git'
   spawn('command -v git ', git_command, sh=True)
   if bitwise_and(file_test(git_command), file_test(git_dir, dir=True)):   
      spawn(git_command + ' --git-dir=' + git_dir + ' describe --tags --always --dirty', version, err_status)
   else:   
      version_file = fidasim_dir + '/VERSION'
      version = ''
      if file_test(version_file):   
         openr(lun, version_file, get_lun=True)
         readf(lun, version)
         free_lun(lun)
   
   return version
   


