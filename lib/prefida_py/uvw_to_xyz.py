from numarray import *

def uvw_to_xyz(alpha, beta, gamma, uvw, origin=None):
#+##`uvw_to_xyz(alpha, beta, gamma, uvw, origin=[0,0,0])`
#+ Express non-rotated coordinate `uvw` in rotated `xyz` coordinates
#+###Arguments
#+     **alpha**: Rotation angle about z [radians]
#+
#+     **beta**: Rotation angle about y' [radians]
#+
#+     **gamma**: Rotation angle about x" [radians]
#+
#+     **xyz**: Point in rotated coordinate system
#+
#+###Keyword Arguments
#+     **origin**: Origin of rotated coordinate system in non-rotated (uvw) coordinates.
#+
#+###Example Usage
#+```idl
#+IDL> xyz = uvw_to_xyz(!DPI/2,0.0,!DPI/3,uvw)
#+```
   n_params = 4
   
   if bitwise_not((origin is not None)):   
      origin = concatenate([0.0, 0.0, 0.0])
   s = size(uvw, dim=True)
   if array(s, copy=0).nelements() != 2:   
      s = concatenate([s, 1])
   uvw_shifted = transpose(uvw - tile_array(origin, 1, s[1]))
   
   r = transpose(tb_zyx(alpha, beta, gamma))
   
   xyz = matrixmultiply(r, uvw_shifted)
   
   return transpose(xyz)

