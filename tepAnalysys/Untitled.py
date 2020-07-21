
import pandas as pd
import os
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


ROOT_DIR = './'

df = pd.read_excel(os.path.join(ROOT_DIR, 'Копия ТЭП-50 Выгрузка2.xlsx'), sheet_name = 'ТЭП-50')
#df.info()


with_pumps = []
without_pumps = []
df.info()
pump1 = df['PSP_Pumps_801_A_S.State1']
pump2 = df['PSP_Pumps_801_A_S.State2']
#pump1.replace('Null', 0)
#pump2.replace('Null', 0)
#pump1.astype(float)
#pump2.astype(float)
x = 0
for i in pump1:
	print(i, pump2[x], i == '1', pump2[x] == '1', i == 1, pump2[x] == 1)
	if i == 1 or pump2[x] == 1:
		with_pumps.append(df.iloc[x])
	else :
		without_pumps.append(df.iloc[x])
	x += 1

pd.DataFrame(with_pumps).to_excel('С увлажнением.xlsx')
pd.DataFrame(without_pumps).to_excel('Без увлажнения.xlsx')
