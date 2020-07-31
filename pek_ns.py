  
import pandas as pd
import os
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


ROOT_DIR = './'
MONTHS = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
YEARS = [2017, 2018, 2019, 2020]
YEAR_STR = {2017:'2017', 2018:'2018', 2019:'2019', 2020:'2020'}

#Ищет ячейку с заголовком "Действующая технологическая линия" на странице в журнале начальника смены
#Возвращает координаты ячейки вида № столбоца, № строки

def find_table(d, m, y):
	df, isExist = get_ns_journal_by_date(d,m,y)
	if(isExist):
		x = df.shape[1]#запоминаем количество столбцов в датасете
		i = 0
	#В цикле обходим все столбцы
		while i < x:
			tmp = df.iloc[:,i]#Выбираем полностью стобец номер i
			i += 1
			counter = 0
			for j in tmp:#по всем ячейкам
				if j == 'Действующая технологическая линия':#, пока не встретим ячейку со значением "Действующая технологическая линия"
					#return i -1  , counter
					column = i - 1
					row = counter
					return df.iloc[row+1:row+10,column:column+8]
				counter += 1
	else:
		print('Нет данных')

#0-8	11/1	35а/3	1 бат	112/2	41/1	37/3	11 л/л
def get_actual_tl(d, m, y):
	table = find_table(d,m,y)
	SMENA_TMP = ("0","0","0","0","0","0","0","0")
	RESULT = []
	print(table)
	for row in range(table.shape[0]):
		SMENA = list(SMENA_TMP)
		for column in range(table.shape[1]):
			data = table.iloc[row, column]
			print(data)
			if (pd.isna(data) and column != 0):
				continue
			else:
				try:
					hour = str(data).split('-')
					#08.01.2017 08:52 - даты из лимс(остаточный стирол)
					#01.01.17 0:00:00 - мес
					dt = []
					dt.append(datetime(day = d,month = m,year = y, hour = int(hour[0]), minute = 0,second = 0).strftime("%d.%m.%y %H:%M:%S"))
					if(int(hour[1]) == 24): 
						hour[1] = 0
					dt.append(datetime(day = d,month = m,year = y, hour = int(hour[1]), minute = 0,second = 0).strftime("%d.%m.%y %H:%M:%S"))
					SMENA[column] = dt
				except Exception as e:
					print(type(e))
					if column == 0:#
						tmp = RESULT[-1]
						SMENA[column] = tmp[column]
					else:
						SMENA[column] = data
		RESULT.append(SMENA)
	return RESULT

#date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
	print(table)#Выбираем подтаблицу с содержимым таблицы "Действующая технологическая линия"
	#return df_tmp, df_tmp.shape[0]#Возвращаем содержимое и количество линий в работе (соответствует количеству строк в таблице)


def parse_all():
	for y in YEARS:
		for m in MONTHS:
			for d in range(31):
				print(m, MONTHS.index(m))
				df, isExist = get_ns_journal_by_date(d,MONTHS.index(m), y)
				if (isExist):
					print(find_table(df))
					print(get_actual_tl_in_3sm(df))
				else:
					break


def get_ns_journal_by_date(d, m, y):
	m -= 1
	journal_name = MONTHS[m] + ' ' + YEAR_STR[y] + ".xlsx"
	try:
		return pd.read_excel(os.path.join(ROOT_DIR, journal_name), sheet_name = str(d + 1)), True
	except FileNotFoundError as e:
		print(e)
		return np.nan ,False


tmp = get_actual_tl(1,12,2017)
for i in tmp:
	print(i)