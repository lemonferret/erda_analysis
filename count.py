import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys 
import copy as copy
import math as math
from decimal import Decimal


name = str(sys.argv[1])
I = float(sys.argv[2])
data=pd.read_csv(name, delim_whitespace=True, skipinitialspace=True)

x = copy.deepcopy(data['0'])
y = copy.deepcopy(data['0.1'])


e2 = 1.4399764 #meV /fm *1e15

e = 1.602176634e-19
epsilon = 8.8541878182e-12

E = 25#*1000000

M2 = 2#*1e6 
MP = 35#*1e6

z1 = 1
z2= 17

shift = 70

#Energycalibration
calib = [0.9627374151202622,  1.3953138465680175, 600,  1900]
x = x#*(calib[1]-calib[0])/(calib[3]-calib[2]) #Mev


#sumcounts deut
cnt =  sum(y[calib[2]+shift:calib[3]])
tilt = math.sin(math.radians(30))

solidangle = (0.002*0.007)/(0.054**2) 
ions = I/(e*5)

tmp1=z1*z2*1.44/(2.0*E)
tmp2=(M2+MP)/M2
ct=math.cos(math.radians(45))
cross = (tmp1*tmp1*tmp2*tmp2)/(ct*ct*ct)

#kokonaiskonsentraatio
c = cnt*tilt*1e26/(ions*cross*solidangle)


print("{:.2E}".format(Decimal(str(round(c, -13)))))


fig = plt.figure() 
ax1 = fig.add_subplot(111) 

ax1.plot(x, y, 'k')
ax1.plot(x[calib[2]+shift:calib[3]], y[calib[2]+shift:calib[3]], 'r')
ax1.set_yscale('log')

plt.xlabel('Channels')
plt.ylabel('Counts')
plt.title('Ta D20keV ERDA')
#plt.ylabel('D consentraatio')
#ax1.plot([1, 2, 3, 4, 5], [3.60E+15, 2.93E+15, 4.20E+14, 3.70E+14, 3.70E+14], 'k')
#plt.xticks([1, 2, 3, 4, 5], ["W\n3.60E+15", "Mo\n2.93E+15", "Nb\n4.20E+14", "V\n3.70E+14", "Ta\n3.70E+14"])

plt.show()




#   | 		     |             |		|
#   | konsentraatio  | Vakansseja  |		|
#   | [mitattu ERDA)]| [SRIM]      | atomia/	|
#   | (atomia/cm2)   | (kpl)	   | vakanssi	|
#===|================|=============|============|
#W: | 3.62E+15       | 9.53E+16    |  0.0380	|
#Mo:| 2.94E+15       | 1.59E+17    |  0.0185	|
#Nb:| 4.20E+14       | 1.07E+17    |  0.0039	|
#Ta:| 3.70E+14       | 9.24E+16    |  0.0040	|
#V: | 3.70E+14       | 2.40E+17    |  0.0015	|
#-----------------------------------------------
