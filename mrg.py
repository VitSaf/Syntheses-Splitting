import pandas as pd
import os
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


ROOT_DIR = './'

df_l = pd.read_excel(os.path.join(ROOT_DIR, 'полимеризат СБС Л 30-01.xlsx'), sheet_name = 'Лист1')
df_r = pd.read_excel(os.path.join(ROOT_DIR, 'полимеризат СБС Р 30-00.xlsx'), sheet_name = 'Лист1')
df = pd.read_excel(os.path.join(ROOT_DIR, 'Новая выгрузка тэп50.xlsx'), sheet_name = 'Лист1')
#df = pd.read_excel(os.path.join(ROOT_DIR, 'load_with_l.xlsx'), sheet_name = 'Sheet1')
df_l['Дата и время'] = df_l['Дата и время'].dropna()

df.info()

def prepare_dates(series):
	tmp = []
	#for i in df_l['Дата и время  отбора']:
	for i in series:
		date = datetime.strptime(str(i), '%d.%m.%Y %H:%M')
		if date.minute > 30:
			if(date.hour == 23):
				date = date.replace(minute = 0, hour = 0)
			else:
				date = date.replace(minute = 0, hour = date.hour + 1)
		else: 
			date = date.replace(minute = 0)
		tmp.append(date)
	return pd.Series(tmp)



df_l['Дата и время'] = prepare_dates(df_l['Дата и время'])
df_r['Дата и время'] = prepare_dates(df_r['Дата и время'])


df_l_tmp = pd.concat([df_l['Дата и время'], df_l['Массовая доля полимера, г']], axis = 1)
df_r_tmp = pd.concat([df_r['Дата и время'], df_r['Массовая доля полимера, г']], axis = 1)
df_r_tmp.info()

#pd.merge(df, df_l_tmp, how = 'outer', left_index=True, right_index=True,).to_excel('merge.xlsx')

def join_l():
	xi = 1
	last_row = 0
	while xi < 31129:
		xj = last_row
		while xj < 9039:
			try:
				d1 = datetime.strptime(str(df.iloc[[xi], 0]).split()[1] + ' ' + str(df.iloc[[xi], 0]).split()[2], '%Y-%m-%d %H:%M:%S')
			except(ValueError):
				str_tmp = df.iloc[[xi], 0]
				str_tmp = str(str_tmp).split()
				d1 = datetime.strptime(str_tmp[1] + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
			try:
				d2 = datetime.strptime(str(df_l_tmp.iloc[[xj], 0]).split()[1] + ' ' + str(df_l_tmp.iloc[[xj], 0]).split()[2], '%Y-%m-%d %H:%M:%S')
			except (ValueError):
				str_tmp = df_l_tmp.iloc[[xj], 0]
				str_tmp = str(str_tmp).split()
				d2 = datetime.strptime(str_tmp[1] + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
			if (d1 == d2):
				print('l', df.iloc[xi, 36], df_l_tmp.iloc[xj, 1], 'xj=', xj, 'xi= ',xi)
				df.iloc[xi, 36] = df_l_tmp.iloc[xj, 1]
				print('!!!!!!!!!!!!!!!!!!!!!!!')
				last_row = xj
				xj = 9039
			if(d1 < d2):
				xj = 9039
			xj += 1
		xi += 1
	df.to_excel('load_with_l.xlsx')


def join_r():
	xi = 1
	last_row = 0
	while xi < 31129:
		xj = last_row
		while xj < 10520:
			print()
			try:
				d1 = datetime.strptime(str(df.iloc[[xi], 0]).split()[1] + ' ' + str(df.iloc[[xi], 0]).split()[2], '%Y-%m-%d %H:%M:%S')
			except(ValueError):
				str_tmp = df.iloc[[xi], 0]
				str_tmp = str(str_tmp).split()
				d1 = datetime.strptime(str_tmp[1] + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
			try:
				d2 = datetime.strptime(str(df_r_tmp.iloc[[xj], 0]).split()[1] + ' ' + str(df_r_tmp.iloc[[xj], 0]).split()[2], '%Y-%m-%d %H:%M:%S')
			except (ValueError):
				str_tmp = df_r_tmp.iloc[[xj], 0]
				str_tmp = str(str_tmp).split()
				d2 = datetime.strptime(str_tmp[1] + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
			if (d1 == d2):
				print('r', df.iloc[xi, 36], df_r_tmp.iloc[xj, 1], 'xj=', xj, 'xi= ',xi)
				df.iloc[xi, 36] = df_r_tmp.iloc[xj, 1]
				print('!!!!!!!!!!!!!!!!!!!!!!!')
				last_row = xj
				xj = 10520
			if(d1 < d2):
				xj = 10520
			xj += 1
		xi += 1
	df.to_excel('load_with_l_and_r.xlsx')


def finalize_load():
	df_final  = pd.read_excel(os.path.join(ROOT_DIR, 'load_with_l_and_r.xlsx'), sheet_name = 'Sheet1')
	df_final['Массовая доля полимера, г'] = df_final['Массовая доля полимера, г'].replace('-', '0')
	#df_final.info()
	xf = 1
	while xf < 31128:
		print('iloc=' ,df_final.iloc[[xf], 37])
		tmp = float(str(df_final.iloc[[xf], 37]).split()[1].replace(',','.'))
		print('xf=', xf, 'tmp=', tmp, type(tmp))
		if tmp == 0:
			#print('before= ', df_final.iloc[[xf], 37])
			df_final.iloc[xf, 37] = df_final.iloc[xf - 1, 37]
			print('after= ', df_final.iloc[[xf], 37])
		xf += 1
	df_final.to_excel('final_load.xlsx')

#join_l()
#join_r()
#finalize_load()