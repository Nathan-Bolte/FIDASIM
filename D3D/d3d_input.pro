PRO d3d_input,inputs                                    

;;-----------------------------------------------------
;;				PREFIDA INPUT FILE
;;-----------------------------------------------------
shot=142114											;; Shot Number
time=1.090 		        							;; Time (s) 
runid='142114B08'   								;; runid of FIDASIM
device='D3D'										;; D3D,NSTX,AUGD,MAST
install_dir='/u/stagnerl/FIDASIM/'		   			;; Location of fidasim code and executable
result_dir='/u/stagnerl/FIDASIM/RESULTS/D3D/'  	;; Location where results will be stored result_dir/runid directory will be created
profile_dir='/u/stagnerl/GAPROFILES/'              	;; Location of profile save files. EX: profile_dir+'shot/'+'dne142353.00505'

;;----------------------------------------------------
;; Fast-ion distribution function from transp
;;----------------------------------------------------
cdf_file='/u/stagnerl/GAPROFILES/142114/142114B08_fi_1.cdf'  ;; CDF file from transp with the distribution funciton
emin=0.                                                      ;; minimum energy used from the distribution function
emax=100.        										     ;; maximum energy used from the distribution function


;;-----------------------------------------------------
;; Beam/diagnostic/equilibrium Selection
;;-----------------------------------------------------
isource=6     		    ;; Beam source index (FIDASIM only simulates one NBI source)
einj=0.                 ;; [keV] If 0, get data from MDS+
pinj=0.                 ;; [MW] If 0, get data from MDS+

fida_diag='VERTICAL'	;; Name of the FIDA diag

gfile=''                ;; If empty, use MDS+; otherwise, filename
equil='EFIT01'			;; MDS+ equilibrium runid

;;-----------------------------------------------------
;; Discharge Parameters
;;-----------------------------------------------------
btipsign=-1.d0		;; Use -1 when Bt and Ip are in the opposite direction   
ab=2.01410178d0     ;; Atomic mass of beam [u]
ai=2.01410178d0     ;; Atomic mass of hydrogenic plasma ions [u]
impurity_charge=6 	;; 5: BORON, 6: carbon, 7: Nitrogen

;;-----------------------------------------------------
;; Wavelength Grid
;;-----------------------------------------------------
lambdamin=6470.d0       						;; Minimum wavelength of wavelength grid[A] 
lambdamax=6670.d0       						;; Maximum wavelength of wavelength grid[A] 
nlambda=2000L           						;; Number of wavelengths
dlambda= (lambdamax-lambdamin)/double(nlambda)	;; Wavelength seperation

;;---------------------------------------------------
;; Define FIDASIM grid in machine coordinates(x,y,z)
;;---------------------------------------------------
nx=40				;; Number of cells in x direction
ny=60				;; Number of cells in y direction
nz=50				;; Number of cells in z direction
xdim1=-150.			;; Minimum x value
xdim2=-110.			;; Maximum x value
ydim1=80.			;; Minimum y value
ydim2=190.			;; Maximum y value
zdim1=-50.			;; Minimum z value
zdim2=50.			;; Maximum z value

;;--------------------------------------------------
;; Define number of Monte Carlo particles
;;--------------------------------------------------
nr_fida=50000   		;; FIDA
nr_ndmc=1000 			;; Beam emission
nr_halo=50000   		;; Halo contribution

;;--------------------------------------------------
;; Calculation of the weight function
;;--------------------------------------------------
nr_wght=40   				;; Number of Pitches, energyies and gyro angles 
emax_wght=100  				;; Maximum energy (keV)
ichan_wght=-1  				;; -1 for all channels, otherwise a given channel index
dwav_wght=1.   				;; Wavelength interval
wavel_start_wght=651.  		;; Minimum wavelength
wavel_end_wght=663.   		;; Maximum wavelength

;;-------------------------------------------------
;; Simulation switches
;;-------------------------------------------------
npa=[1]   					;; (0 or 1) If 0 do a simulation for NPA
no_spectra=[0]   			;; (0 or 1) If 1 then no spectra are calculated
nofida=[0]    				;; (0 or 1) If 1 then no fast-ions are simulated
f90brems=[1]                ;; (0 or 1) If 0 use the IDL bremstrahlung calculation
guidingcenter=[1]           ;; (0 or 1) Use 1 for guiding center distribution functs.
calc_wght=[0]  				;; (0 or 1) If 1 then weight functions are calculated
load_neutrals=[0]   		;; (0 or 1) If 1 then the neutral density is loaded from an existing 
							;; neutrals.bin file located in runid directory

;;------------------------------------------------
;; DO NOT MODIFY THIS PART
;;------------------------------------------------

inputs={shot:shot,time:time,runid:runid,device:strupcase(device),install_dir:install_dir,result_dir:result_dir,$
       cdf_file:cdf_file,profile_dir:profile_dir,emin:emin,emax:emax, $
       isource:isource,einj:einj,pinj:pinj,fida_diag:fida_diag,gfile:gfile,equil:equil,$
       btipsign:btipsign,ab:ab,ai:ai,impurity_charge:impurity_charge,$
       lambdamin:lambdamin,lambdamax:lambdamax,nlambda:nlambda,dlambda:dlambda,$
       nx:nx,ny:ny,nz:nz,xdim1:xdim1,xdim2:xdim2,ydim1:ydim1,ydim2:ydim2,zdim1:zdim1,zdim2:zdim2,$
       nr_fida:nr_fida,nr_ndmc:nr_ndmc,nr_halo:nr_halo,nr_wght:nr_wght,$
       emax_wght:emax_wght,ichan_wght:ichan_wght,dwav_wght:dwav_wght,wavel_start_wght:wavel_start_wght,$
	   wavel_end_wght:wavel_end_wght,npa:npa,no_spectra:no_spectra,nofida:nofida, $
       f90brems:f90brems,guidingcenter:guidingcenter,calc_wght:calc_wght,load_neutrals:load_neutrals}

END
