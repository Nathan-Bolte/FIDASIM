from numarray import *

def aabb_intersect(rc, dr, r0, d0, intersect, r_enter, r_exit):
#+#aabb_intersect
#+Calculates intersection length of a ray and an axis aligned bounding box (AABB)
#+***
#+##Input Arguments
#+     **rc**: Center of AABB
#+
#+     **dr**: [length, width, height] of AABB
#+
#+     **r0**: starting point of ray
#+
#+     **d0**: direction of ray
#+
#+##Output Arguments
#+     **intersect**: Intersection length of ray and AABB
#+
#+     **ri**: Optional, ray enterence point
#+
#+     **rf**: Optional, ray exit point
#+
#+##Example Usage
#+```idl
#+IDL> aabb_intersect, [0,0,0], [1,1,1], [-1,0,0], [1,0,0], intersect, ri, rf
#+IDL> print, intersect
#+    1.0
#+IDL> print, ri
#+    -0.5  0.0  0.0
#+IDL> print, rf
#+     0.5  0.0  0.0
#+```

   n_params = 7
   def _ret():  return (rc, dr, r0, d0, intersect, r_enter, r_exit)
   
   v0 = d0 / sqrt(total(d0 * d0))
   
   #; There are 6 sides to a cube/grid
   side_inter = dblarr(6)
   #; Intersection points of ray with planes defined by grid
   ipnts = dblarr(3, 6)
   
   #; Find whether ray intersects each side
   for i in arange(0, 6):
      j = array(floor(i / 2), copy=0).astype(Int32)
      ind = where(ravel(concatenate([0, 1, 2]) != j))[0]
      if abs(v0[j]) > 0:   
         #; Intersection point with plane
         ipnts[i,:] = r0 + v0 * (((rc[j] + ((i % 2) - 0.5) * dr[j]) - r0[j]) / v0[j])
         #; Check if point on plane is within grid side
         if bitwise_and(abs(ipnts[i,ind[0]] - rc[ind[0]]) <= 0.5 * dr[ind[0]], abs(ipnts[i,ind[1]] - rc[ind[1]]) <= 0.5 * dr[ind[1]]):   
            side_inter[i] = 1
   
   intersect = 0.0
   r_enter = r0
   r_exit = r0
   w = where(ravel(side_inter != 0))[0]
   if nw >= 2:   
      #;Find two unique intersection points
      nunique = 0
      for i in arange(0, (nw - 2)+(1)):
         if total(ipnts[w[0],:] == ipnts[w[i + 1],:]) != 3:   
            w = concatenate([w[0], w[i + 1]])
            nunique = 2
            break
      
      if nunique == 2:   
         vi = ipnts[w[1],:] - ipnts[w[0],:]
         vi = vi / sqrt(total(vi * vi))
         dot_prod = total(v0 * vi)
         if dot_prod > 0.0:   
            r_enter = ipnts[w[0],:]
            r_exit = ipnts[w[1],:]
         else:   
            r_enter = ipnts[w[1],:]
            r_exit = ipnts[w[0],:]
         #; Calculate intersection length
         intersect = sqrt(total((r_exit - r_enter) ** 2.0))
   
   return _ret()


