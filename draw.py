# ./lue testi.LST >aaa
# python3 draw.py 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys 

name = str(sys.argv[1])

data=pd.read_csv(name, delim_whitespace=True, skipinitialspace=True)

datay = []
for i in range(0, len(data)):
	datay.extend([data.iloc[i, 0]])	  


datay.sort()

x = np.arange(0, max(datay)+1)
y = [0]*(max(datay)+1)

for i in datay:
	y[i] += 1


fig = plt.figure() 

ax1 = fig.add_subplot(111) 
ax1.plot(x, y)
ax1.set_yscale('log')

plt.show()

for i in range(0, len(y)):
	print(x[i], y[i])




