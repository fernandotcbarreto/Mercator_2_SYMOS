import numpy as np
from netCDF4 import Dataset as dat
from scipy.interpolate import griddata, interp1d
import matplotlib.pyplot as plt
import datetime
import pandas as pd
import matplotlib.dates as dates

file=dat('golfo_2019/phys-sat_global_20190129.nc')

lat= file['latitude'][::]

lon= file['longitude'][::]

[lon,lat]=np.meshgrid(lon,lat)

u = np.ma.filled(file['uo'][::],fill_value=0)

v = np.ma.filled(file['vo'][::],fill_value=0)

sp=5

plt.quiver(lon[0:-1:sp,0:-1:sp], lat[0:-1:sp,0:-1:sp], u[0,30, 0:-1:sp,0:-1:sp], v[0,30, 0:-1:sp,0:-1:sp])
plt.show()
