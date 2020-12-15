import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys 
import math as math 
from scipy.interpolate import interp1d
from functools import reduce 
import copy as copy
from scipy.optimize import curve_fit

def f(S, A, B): # this is your 'straight line' y=f(x)
    return A*S + B


name = str(sys.argv[1])
EP = 25 #MeV
MP = 35
theta = 45 
xfoil = 4000 #nanom

MH = 1
MD = 2

data=pd.read_csv(name, delim_whitespace=True, skipinitialspace=True)

x = data['0']
y = data['0.1']

#Theoretical max
EHmax = EP*(4*MH*MP)*math.cos(math.radians(theta))**2/((MH+MP)**2) 
EDmax = EP*(4*MD*MP)*math.cos(math.radians(theta))**2/((MD+MP)**2) 

#Stopping 
stopH=pd.read_csv("StoppingH", delim_whitespace=True, skipinitialspace=True)
stopD=pd.read_csv("StoppingD", delim_whitespace=True, skipinitialspace=True)
EstopH = copy.deepcopy(stopH['100.00'])
EstopD = copy.deepcopy(stopD['100.00'])

unit = stopH['keV']
Estops = [n*0.001 for i, n in enumerate(EstopH) if unit[i] == 'keV']
EstopH[0:len(Estops)] = Estops

unit = stopD['keV']
Estops = [n*0.001 for i, n in enumerate(EstopD) if unit[i] == 'keV']
EstopD[0:len(Estops)] = Estops

eleH = stopH['2.390E+02'] #Mev/mm
nucH = stopH['5.107E-01'] #Mev/mm
eleD = stopD['2.116E+02'] #Mev/mm
nucD = stopD['1.013E+00'] #Mev/mm


f1H = interp1d(EstopH, eleH, kind='cubic')
f2H = interp1d(EstopH, nucH, kind='cubic')
f1D = interp1d(EstopH, eleD, kind='cubic')
f2D = interp1d(EstopH, nucD, kind='cubic')
xnewH = np.linspace(min(EstopH), max(EstopH), num=100001, endpoint=True)
xnewD = np.linspace(min(EstopD), max(EstopD), num=100001, endpoint=True)

s = 0
dx = 1
SeH = 0
SnH = 0
SeD = 0
SnD = 0

while s<=xfoil:
	SeH = f1H(EHmax)
	SnN = f2H(EHmax) 
	SeD = f1D(EHmax)
	SnD = f2D(EHmax)
	s += dx #nano m
	EHmax -= SeH*dx/1e6 +SnH*dx/1000 
	EDmax -= SeD*dx/1e6 +SnD*dx/1000



Hstart = 600
Dstart = 1300


fig, axs = plt.subplots(2)
#axs[1].plot(EstopH, eleH, 'r')
#axs[0].plot(EstopH, eleH, '.',EstopH, nucH, '.', xnew, f1H(xnew), '--', xnew, f2H(xnew), '--' )
#ax1.plot(EstopH, nucH)

axs[1].plot(x, y, 'k')
axs[1].plot([Hstart, Hstart], [1,1000], 'r')
axs[1].plot([Dstart, Dstart], [1,1000], 'r')
axs[1].set_yscale('log')





popt = curve_fit(f,  [Hstart, Dstart], [EHmax, EDmax])
popt = popt[0]
axs[0].plot([0, 2000],[popt[1], popt[0]*2000+popt[1]], '-r')
axs[0].plot([Hstart, Dstart], [EHmax, EDmax], '*-k')

title = "A=" + str(popt[0]) + " B=" + str(popt[1])

fig.suptitle(title)

print(EHmax, EDmax, Hstart, Dstart)

plt.show()


