##delft 2 oil
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

depth = np.ma.filled(file['uo'][::],fill_value=19999999)
depth = depth[0,0,:,:]
depth[depth<19999999]=1000;depth[depth==19999999]=-1000

layer =  -np.ma.filled(file['depth'][::],fill_value=0)



for i in range(ntimes):
  file=input + dates.num2date(date[i]).strftime("%Y%m%d")+'.nc'
  file = dat(file)
  u = np.ma.filled(file['uo'][::],fill_value=0)
  v = np.ma.filled(file['vo'][::],fill_value=0)
  utim[i,::] = u
  vtim[i,::] = v
   

counttimeh=np.zeros([1])
counttimeh=np.array([12*60])

with open('time_delft.txt', 'w') as f:
   np.savetxt(f, np.array(len(time_oil)).reshape(1,), fmt = '%i')
   np.savetxt(f, np.array(int(lon.shape[0])).reshape(1,), fmt = '%i')
   np.savetxt(f, np.array(int(lon.shape[1])).reshape(1,), fmt = '%i')   
   np.savetxt(f, np.array(int(u.shape[1])).reshape(1,), fmt = '%i')      
   np.savetxt(f, time_oil,fmt='%10.4f')
   np.savetxt(f, layer,fmt='%10.4f')
   np.savetxt(f, counttimeh,fmt='%10.4f')
#   np.savetxt(f, time_oil,fmt="%s")


for i in range(len(time_oil)):
  with open(str(i+1) + 'v.txt', 'w') as f:
    for j in range(v.shape[1]):
      np.savetxt(f, np.squeeze(vtim[i,j, :,:]),fmt='%10.8f')

for i in range(len(time_oil)):
  with open(str(i+1) + 'u.txt', 'w') as f:
    for j in range(u.shape[1]):
      np.savetxt(f, np.squeeze(utim[i,j, :,:]),fmt='%10.8f')


with open('lat_delft.txt', 'w') as f:
     np.savetxt(f, lat,fmt='%10.8f')


with open('lon_delft.txt', 'w') as f:
     np.savetxt(f, lon,fmt='%10.8f')


with open('depth.txt', 'w') as f:
  np.savetxt(f, depth, fmt='%10.8f')





