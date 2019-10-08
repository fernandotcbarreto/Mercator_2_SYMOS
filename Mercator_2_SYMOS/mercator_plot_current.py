import numpy as np
from netCDF4 import Dataset as dat
from scipy.interpolate import griddata, interp1d
import matplotlib.pyplot as plt
import datetime
import pandas as pd
import matplotlib.dates as dates

file=dat('golfo_2019/phys-sat_global_20190102.nc')

input = 'golfo_2019/phys-sat_global_'

dateini='2019-01-01'
dateend='2019-01-31'

a=[dateini, dateend]

date=dates.datestr2num(a)

ntimes=len(np.arange(date[0], date[1]+1))

date = np.arange(date[0], date[1]+1)

time_oil=np.arange(ntimes)

time_oil=time_oil*24*60 

lat= np.ma.filled(file['latitude'][::],fill_value=0)

lon= np.ma.filled(file['longitude'][::],fill_value=0)

[lon,lat]=np.meshgrid(lon,lat)

u = np.ma.filled(file['uo'][::],fill_value=0)

v = np.ma.filled(file['vo'][::],fill_value=0)

utim=np.zeros([ntimes,u.shape[1], u.shape[2], u.shape[3]])
vtim=np.zeros([ntimes,v.shape[1], v.shape[2], v.shape[3]])


for i in range(ntimes):
  file=input + dates.num2date(date[i]).strftime("%Y%m%d")+'.nc'
  file = dat(file)
  u = np.ma.filled(file['uo'][::],fill_value=0)
  v = np.ma.filled(file['vo'][::],fill_value=0)
  utim[i,::] = u
  vtim[i,::] = v

u1=utim[:,0,:,:].copy()
v1=vtim[:,0,:,:].copy()

time=pd.read_csv('time_hours.txt', delim_whitespace=True).values   ###output data
time=time[:,0]*60


u_interp=np.zeros([u1.shape[1], u1.shape[2], len(time)])
v_interp=np.zeros([v1.shape[1], v1.shape[2], len(time)])

for j in np.arange(u_interp.shape[0]):
   for k in np.arange(u_interp.shape[1]):
      u_interp[j,k,:] = np.interp(time, time_oil, u1[:,j,k])



for j in range(v_interp.shape[0]):
  for k in range(v_interp.shape[1]):
     v_interp[j,k,:] = np.interp(time, time_oil, v1[:,j,k])


np.save('u1', u_interp)

np.save('v1', v_interp)
