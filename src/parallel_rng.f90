!+This file contains routines for parallel random number generation
module parallel_rng
    !+ A basic parallel random number generator library
#ifdef _OMP
  use omp_lib
#endif

implicit none
private
public :: rng_type, rng_init, rng, rng_uniform, rng_normal, randu, randn, randind, ind2sub

integer, parameter :: Int32 = 4
integer, parameter :: Int64 = kind(int8(1))
integer, parameter :: Float32 = kind(1.e0)
integer, parameter :: Float64 = kind(1.d0)

integer(Int32), parameter :: IA = 16807
integer(Int32), parameter :: IM = 2147483647
integer(Int32), parameter :: IQ = 127773
integer(Int32), parameter :: IR = 2836
real(Float64), protected :: AM = nearest(1.0,-1.0)/IM

integer, parameter :: ns = 2

type :: rng_type
    !+ Random Number Generator Derived Type
    integer(Int32), dimension(ns) :: state
end type rng_type

type(rng_type), dimension(:), allocatable :: rng

interface randind
    !+ Procedure for generating a random array index/subscripts
    module procedure randind_n
    module procedure randind_w_1
    module procedure randind_w_2
end interface

contains

subroutine rng_init(self, seed)
    !+ Procedure to initialize a random number generator with a seed
    type(rng_type), intent(inout) :: self
        !+ Random Number Generator
    integer(Int32), intent(in)    :: seed
        !+ Initial Seed Value

    self%state(1) = ieor(777755555,abs(seed))
    self%state(2) = ior(ieor(888889999,abs(seed)),1)
  
end subroutine rng_init

function rng_uniform(self) result(u)
    !+ Generate a uniformally-distributed random number in the range [0,1)
    type(rng_type), intent(inout) :: self
        !+ Random Number Generator
    real(Float64)                 :: u
        !+ Uniform random deviate

    integer(Int32) :: ix,iy,k
  
    ix = self%state(1)
    iy = self%state(2)
  
    ix = ieor(ix,ishft(ix,13))
    ix = ieor(ix,ishft(ix,-17))
    ix = ieor(ix,ishft(ix,5))
    k=iy/IQ
    iy=IA*(iy - k*IQ) - IR*k
    if(iy.lt.0) iy = iy + IM
    self%state(1) = ix
    self%state(2) = iy
  
    u = am*ior(iand(IM,ieor(ix,iy)),1)

end function rng_uniform

function rng_normal(self) result(n)
    !+ Generate a normally-distributed random number with mean 0 and standard deviation 1
    type(rng_type), intent(inout) :: self
        !+ Random Number Generator
    real(Float64)                 :: n
        !+ Normal random deviate

    real(Float64), parameter :: s = 0.449871d0
    real(Float64), parameter :: t = 0.386595d0
    real(Float64), parameter :: a = 0.196000d0
    real(Float64), parameter :: b = 0.254720d0
    real(Float64), parameter :: r1 = 0.27597d0
    real(Float64), parameter :: r2 = 0.27846d0
    real(Float64) :: u, v, x, y, q
  
    do
        u = rng_uniform(self)
        v = rng_uniform(self)
        v = 1.7156d0 * (v - 0.5d0)
  
        x = u - s
        y = abs(v) + t
        q = x**2 + y*(a*y - b*x)
  
        if (q.lt.r1) exit
        if (q.gt.r2) cycle
        if((v**2).lt.(-4.0*log(u)*u**2)) exit
    enddo
  
    n = v/u

end function rng_normal

subroutine randu(randomu)
    !+ Generate an array of uniformally-distributed random deviates
    real(Float64), dimension(:), intent(out) :: randomu
        !+ Array of uniform random deviates

    integer :: i, thread_id

#ifdef _OMP
    thread_id = OMP_get_thread_num() + 1
#else
    thread_id = 1
#endif

    randomu = 0.d0
    do i=1,size(randomu)
        randomu(i) = rng_uniform(rng(thread_id))
    enddo

end subroutine randu

subroutine randn(randomn)
    !+ Generate an array of normally-distributed random deviates
    real(Float64), dimension(:), intent(out) :: randomn
        !+ Array of normal random deviates

    integer :: i, thread_id
  
#ifdef _OMP
    thread_id = OMP_get_thread_num() + 1
#else
    thread_id = 1
#endif

    randomn = 0.d0
    do i=1,size(randomn)
        randomn(i) = rng_normal(rng(thread_id))
    enddo

end subroutine randn

function search_sorted_first(x, v) result(hi)
    !+ Returns the index of the first value in `x` greater or equal to `v`.
    !+ Returns `length(x)+1` if `v` is greater then all values in `x`.
    real(Float64), dimension(:), intent(in) :: x
        !+ Monotonically increasing array
    real(Float64), intent(in)               :: v
        !+ Value to search

    integer :: hi, lo, m

    lo = 0
    hi = size(x)+1

    do while (lo.lt.(hi-1))
        m = rshift(lo+hi,1)
        if(x(m).lt.v) then
            lo = m
        else
            hi = m
        endif
    enddo

end function search_sorted_first

subroutine randind_n(n,randomi)
    !+ Generate a array of uniformally-distributed random integers in the range [1, n]
    integer, intent(in)                :: n
        !+ Largest possible value
    integer, dimension(:), intent(out) :: randomi
        !+ Array of uniform deviates

    integer :: i
    real(Float64), dimension(1) :: randomu
  
    randomi = 0 
    do i=1,size(randomi)
        call randu(randomu)
        randomi(i) = ceiling(randomu(1)*n)
    enddo

end subroutine randind_n

subroutine randind_w_1(w,randomi)
    !+ Generate an array of random indices of an 1D array distributed according to `w`
    real(Float64), dimension(:), intent(in) :: w
        !+ 1D array of index weights
    integer, dimension(:), intent(out)      :: randomi
        !+ Random indices

    integer :: i, nw
    real(Float64) :: cdf_val, t
    real(Float64), dimension(size(w)) :: cdf
    real(Float64), dimension(1) :: randomu
  
    nw = size(w)
    t = 0.d0
    do i=1, nw
        cdf(i) = t + w(i)
        t = cdf(i)
    enddo

    randomi = 0
    do i=1,size(randomi)
        call randu(randomu)
        cdf_val = randomu(1)*cdf(nw)
        randomi(i) = min(search_sorted_first(cdf,cdf_val),nw)
    enddo

end subroutine randind_w_1

subroutine ind2sub(dims,ind,subs)
    !+ Calculate the subscripts `subs` into an array with dimensions `dims`
    !+ given the corresponding linear index `ind`
    integer, dimension(:), intent(in)  :: dims
        !+ Dimensions of array
    integer, intent(in)                :: ind
        !+ Linear index
    integer, dimension(:), intent(out) :: subs
        !+ Subscripts corresponding to the linear index

    integer :: i, ndims, ind1, ind2
  
    ind1=ind
    ndims = size(dims)
    do i=1,ndims-1
        ind2 = (ind1-1)/dims(i) + 1
        subs(i) = ind1 - dims(i)*(ind2-1)
        ind1 = ind2
    enddo
    subs(ndims) = ind1

end subroutine ind2sub

subroutine randind_w_2(w,randomi)
    !+ Generate an array of random subscripts of an 2D array distributed according to `w`
    real(Float64), dimension(:,:), intent(in) :: w
        !+ 2D array of subscript weights
    integer, dimension(:,:), intent(out)      :: randomi
        !+ A 2D (ndim, :) array of random subscripts
  
    integer :: i,nw
    integer, dimension(2) :: subs
    integer, dimension(size(randomi,2)) :: randi

    randomi = 0
    nw = size(w)

    call randind_w_1(reshape(w,[nw]),randi)
    do i=1,size(randomi,2)
        call ind2sub(shape(w),randi(i),subs)
        randomi(:,i) = subs
    enddo

end subroutine randind_w_2

end module parallel_rng
