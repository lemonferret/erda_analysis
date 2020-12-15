import pandas as pd
import matplotlib.pyplot as plt
from decimal import Decimal
import numpy as np
import codecs as codecs


def rng(s = 'EXAMPLE'):
	s = '/home/anliski/.wine/drive_c/Program Files (x86)/SRIM/SRIM Outputs/' + s +'/RANGE_3D.txt'
	#print('\n', s,'\n')
	data=pd.read_csv(s, delim_whitespace=True, skipinitialspace=True, skiprows = 17)
	
	n = []
	d = []
	ylat = []
	zlat = []

	def titles(s):
		print('')
		with codecs.open(s, 'r', encoding='utf-8', errors='ignore') as f:
			lines = f.readlines()
		
		for line in lines:
			if "   Ion Mass=" in line:
				temp1 = line[5:9]
				print(line[:-1])
			if "Energy  =" in line:
				temp2 = line[10:-2]
				print(line[:-1])	
			if "Layer # 1 -  " in line:
				print(line[24:-2])
				title = temp1+'('+ temp2 + ') in ' +line[24:-2]
		f.close()
		return(title)
	

	for i in range(0, len(data)):
		n.extend([data.iloc[i, 0]])	  
		d.extend([data.iloc[i, 1]])
		ylat.extend([data.iloc[i, 2]])
		zlat.extend([data.iloc[i, 3]])

	print("Ions calculated", max(n))
	title = titles(s)	
	counts, bins = np.histogram(d, int(round(max(d)*0.01)))		 

	plt.ylabel('Ions')
	plt.xlabel('Depth Å')
	plt.title(title)
	plt.plot(bins[:-1], counts)
	plt.show()


def vac(s = 'EXAMPLE', N=10000):
	s = '/home/anliski/.wine/drive_c/Program Files (x86)/SRIM/SRIM Outputs/' + s +'/VACANCY.txt'
	#print('\n', s,'\n')
	data=pd.read_csv(s, delim_whitespace=True, skipinitialspace=True, engine="python" , skiprows = 28, skipfooter= 1 )
	d = []
	v1 = []
	v2 = []
	v3 = []
	
	def ioncount(s):
		print('')
		f = open(s)
		lines = f.readlines()
		for line in lines:
			if "Total Ions calculated =" in line:
				ions= round(float(line[24:]))
				print(line[7:22],'' ,ions, '--> ',N ,'\n')
			if "====== TRIM Calc.=" in line:
				tmp= line[20:30]+ "in "
			if "Atomic Percent" in line:
				title =tmp+ line[13:15] 
				print(tmp, line[13:15])	
		f.close()
		return(ions, title)
	
	ions, title = ioncount(s)
	for i in range(0, len(data)):
		d.extend([data.iloc[i, 0]])	  
		v1.extend([data.iloc[i, 1]*100*N])
		v2.extend([data.iloc[i, 2]*100*N])
		v3.extend([data.iloc[i, 1]*100*N+data.iloc[i, 2]*N*100])

	

	print("Ion Vacancies    {:.2E}".format(Decimal(str(sum(v1)))))
	print("Recoil Vacancies {:.2E}\n".format(Decimal(str(sum(v2)))))

	print("Total Vacancies  {:.2E}".format(Decimal(str(sum(v3)))))

	plt.ylabel('Vacancy')
	plt.xlabel('Depth Å')
	plt.title(title)
	plt.plot(d, v1, '.-k', label='ions')
	plt.plot(d, v2, '.-b', label='recoils')
	plt.plot(d, v3, '.-r', label='total')
	plt.legend(loc='upper right')
	plt.show()

