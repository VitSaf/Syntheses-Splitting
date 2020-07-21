import pandas as pd
import os
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
#import plotly.plotly as py
#import plotly.graph_objs as go
#from plotly.offline import iplot

#import cufflinks
#cufflinks.go_offline()
#cufflinks.set_config_file(world_readable=True, theme='pearl', offline=True)


ROOT_DIR = './'

df = pd.read_excel(os.path.join(ROOT_DIR, 'Копия ТЭП-50 Выгрузка2.xlsx'), sheet_name = 'ТЭП-50')
#df.info()


dftmp = df[28466:]#c 1.04.20
ekons_udel = dftmp['Удельный расход, Гкал/т']
ekons_udel = ekons_udel.replace('', np.nan)
ekons_udel = ekons_udel.dropna()
ekons_udel = ekons_udel.astype(float)


steam_udel = df['Удельный расход, Гкал/т']
steam_udel =  steam_udel.replace('', np.nan)
steam_udel = steam_udel.dropna()
steam_udel = steam_udel.astype(float)


# sns.distplot(steam_udel, color='red')
# plt.show()

#fig, ax = plt.subplots()


#sns.distplot(ekons_udel, bins=np.linspace(0,3,30), hist=False, kde=True) # Через Seaborn, не работает
(n, bins, patches) = plt.hist(steam_udel, bins=np.linspace(0,3,30))  # Через mpl
(n, bins, patches) = plt.hist(ekons_udel, bins = np.linspace(0, 3, 30))
plt.show()





print('Дисперсия:',np.var(steam_udel))#наиболее типичное отклонение
print('Медиана',np.median(steam_udel))#медиана
print('среднеквадратичное отклонение',np.std(steam_udel))#среднеквадратичное отклонение
print('средее арифметическое',np.mean(steam_udel))#средее арифметическое
