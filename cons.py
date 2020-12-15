import pandas as pd
import matplotlib.pyplot as plt
from decimal import Decimal
import numpy as np
import codecs as codecs
import itertools as it
from scipy.interpolate import interp1d
import SRIMmodule as srim
from scipy.interpolate import UnivariateSpline

s = 'Tatar'
elem = s[:-3]


if elem=='W':
	rho = 19.3
	u = 183.84
	Icoef = 7.89650
elif elem=='Mo':
	rho = 10.28 
	u = 95.95
	Icoef = 7.69807
elif elem=='Ta':
	rho = 16.69
	u = 180.94788
	Icoef = 7.99840
elif elem=='Nb':
	rho = 8.57 
	u = 92.90638
	Icoef = 7.65525	
elif elem=='V':
	rho = 6.11
	u = 50.9415
	Icoef = 7.62392

c = 1.66054e-24

lay = []
cH = []
cD = []
cX = []
coef = 1e15

c =[]
order = []
comp = []
with open(s) as f:
	for line in it.islice(f, 25, None):
		line = line.strip()
		if line[50:] == '0':
			#print(line[3:-26])
			lay.extend([float(line[3:-26])])
			comp.extend([int(line[0:1])])
		if 'H' in line:
			order.extend([1])
			c.extend([coef*float(line[30:-2])]) 
		if 'D' in line:
			order.extend([2])
			c.extend([coef*float(line[30:-2])]) 			
		if elem in line:
			order.extend([3])
			c.extend([coef*float(line[30:-2])]) 
		if 'Foil' in line:
			break

nums = 0
for i, n  in enumerate(lay):
	if comp[i] == 1:
		if order[nums]== 1:
			cH.extend([c[nums]]) 
			cD.extend([0]) 
			cX.extend([0]) 
		if order[nums]== 2:		
			cH.extend([0]) 
			cD.extend([c[nums]]) 
			cX.extend([0]) 
		if order[nums]== 3:
			cH.extend([0]) 
			cD.extend([0]) 
			cX.extend([c[nums]]) 
		nums += 1
	if comp[i] == 2:
		if order[nums]== 1 and order[nums+1]== 2:
			cH.extend([c[nums]]) 
			cD.extend([c[nums+1]]) 
			cX.extend([0]) 
		if order[nums]== 1 and order[nums+1]== 3:
			cH.extend([c[nums]]) 
			cD.extend([0]) 
			cX.extend([c[nums+1]]) 
		if order[nums]== 2 and order[nums+1]== 1:
			cH.extend([c[nums+1]]) 
			cD.extend([c[nums]]) 
			cX.extend([0]) 
		if order[nums]== 2 and order[nums+1]== 3:
			cH.extend([0]) 
			cD.extend([c[nums]]) 
			cX.extend([c[nums+1]]) 
		if order[nums]== 3 and order[nums+1]== 1:
			cH.extend([c[nums+1]]) 
			cD.extend([0]) 
			cX.extend([c[nums]]) 
		if order[nums]== 3 and order[nums+1]== 2:
			cH.extend([0]) 
			cD.extend([c[nums+1]]) 
			cX.extend([c[nums]]) 
		nums += 2
	if comp[i] == 3:
		if order[nums]== 1 and order[nums+1]== 2 and order[nums+2]== 3:
			cH.extend([c[nums]]) 
			cD.extend([c[nums+1]]) 
			cX.extend([c[nums+2]]) 
		if order[nums]== 1 and order[nums+1]== 3 and order[nums+2]== 2:
			cH.extend([c[nums]]) 
			cD.extend([c[nums+2]]) 
			cX.extend([c[nums+1]]) 
		if order[nums]== 2 and order[nums+1]== 1 and order[nums+2]== 3:
			cH.extend([c[nums+1]]) 
			cD.extend([c[nums]]) 
			cX.extend([c[nums+2]]) 
		if order[nums]== 2 and order[nums+1]== 3 and order[nums+2]== 1:		
			cH.extend([c[nums+2]]) 
			cD.extend([c[nums]]) 
			cX.extend([c[nums+1]]) 
		if order[nums]== 3 and order[nums+1]== 1 and order[nums+2]== 2:
			cH.extend([c[nums+1]]) 
			cD.extend([c[nums+2]]) 
			cX.extend([c[nums]]) 		
		if order[nums]== 3 and order[nums+1]== 2 and order[nums+2]== 1:
			cH.extend([c[nums+2]]) 
			cD.extend([c[nums+1]]) 
			cX.extend([c[nums]]) 

		nums += 3


thickness = [0]*len(lay)
for i, n in enumerate(lay):
	thickness[i] = ((sum(lay[0:i-1]))+lay[i]/2)*1e15*(10*1e7)*(u*1.66054e-24)/rho


dv, v = srim.vac(s = elem+ '20D', N=5e16, p = 0)
di, i = srim.rng(s = elem+ '20D', p = 0)
f1 = interp1d(thickness, cD, kind='slinear')
xnew = np.linspace(min(thickness), max(thickness), num=100001, endpoint=True)

#fig, axs = plt.subplots(2, 1, constrained_layout=True)

fig = plt.figure( figsize=(6.5, 10), constrained_layout=True)
gs = fig.add_gridspec(4, 1)
axs= [0, 0, 0]
axs[0] = fig.add_subplot(gs[0, :])
axs[1] = fig.add_subplot(gs[1, :])
axs[2] = fig.add_subplot(gs[2:, :])

axs[0].plot(np.asarray(thickness)/10, np.asarray(cD)*Icoef, '.b')
axs[0].plot(np.asarray(xnew)/10, np.asarray(f1(xnew))*Icoef, '--')
axs[0].set_xlim([0,400])
axs[0].set_title(elem+ "-->D  relative conc. atoms/cm2 (Simnra)" ) #Total =  {:.2E}".format(Decimal(str(sum(cD)))))
axs[0].set_xlabel('Depth nm')
axs[0].set_ylabel('Number of atoms')

#axs[0].set_yscale('log')

	
#axs[1].plot(np.asarray(di)/10, i*5e16/6957, 'r')
#axs[1].plot(np.asarray(dv)/10, np.asarray(v), 'g')
#axs[1].set_xlim([0,400])
#axs[1].set_title(elem +'-->Vacancies(g) + ion profile(r) (SRIM)')
#axs[1].set_xlabel('Depth nm')
#axs[1].set_ylabel('Number of vacancies/ions')

#axs[2].plot(np.asarray(di)/10, i*5e16/6957, 'r')
#axs[2].plot(np.asarray(dv)/10, np.asarray(v)*3, 'g')
#axs[2].plot(np.asarray(thickness)/10, np.asarray(cD)*10000, '.b')
#axs[2].plot(np.asarray(xnew)/10, np.asarray(f1(xnew))*10000, '--')
#axs[2].set_xlim([0,400])
#axs[2].set_title(elem +'-->All in one (not proportional)')
#axs[2].set_xlabel('Depth nm')
#axs[2].set_ylabel('random units')


plt.show()

	
#fig = plt.figure( figsize=(6.5, 6.5), constrained_layout=True)
#gs = fig.add_gridspec(1, 1)
#axs = fig.add_subplot(gs[0, :])
#axs.plot(np.asarray(thickness)/10, np.asarray(cD), '.b')
#axs.plot(np.asarray(xnew)/10, np.asarray(f1(xnew)), '--')
#axs.set_xlim([0,350])
#plt.show()
