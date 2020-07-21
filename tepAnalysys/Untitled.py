#!/usr/bin/env python
# coding: utf-8

# In[89]:


import pandas as pd
import os
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


ROOT_DIR = './'

df = pd.read_excel(os.path.join(ROOT_DIR, 'Копия ТЭП-50 Выгрузка2.xlsx'), sheet_name = 'ТЭП-50')
#df.info()


steam = df['Расход пара на 2-ю ступень дегазации MS-312, Гкал/час']
polimer = df['Общая подача полимера на дегазацию, т/час']

#steam = steam.astype('float64')
steam = steam.replace(0, 0.1)
steam = steam.dropna()
#polimer = polimer.astype('float64')
polimer = polimer.replace(0, np.nan)
polimer = polimer.dropna()

df['total'] = steam / polimer


dftmp = df[28466:]#c 1.04.20
ekons_udel = dftmp['Удельный расход, Гкал/т']
ekons_udel = ekons_udel.replace('', np.nan)
ekons_udel = ekons_udel.dropna()
ekons_udel = ekons_udel.astype(float)


steam_udel = df['Удельный расход, Гкал/т']
steam_udel =  steam_udel.replace('', np.nan)
steam_udel = steam_udel.dropna()
steam_udel = steam_udel.astype(float)


print(steam_udel.shape)# sns.distplot(steam_udel, color='red')
# plt.show()

#sns.distplot(ekons_udel, bins=np.linspace(0,3,30), hist=False, kde=True) # Через Seaborn, не работает
(n, bins, patches) = plt.hist(steam_udel, bins=np.linspace(0,3,30))  # Через mpl
(n, bins, patches) = plt.hist(ekons_udel, bins = np.linspace(0, 3, 30))
plt.show()
