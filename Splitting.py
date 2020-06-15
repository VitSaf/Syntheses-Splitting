import pandas as pd
import os
import xlwt
import xlrd
from xlutils.copy import copy

print("Start")
def newExcel():
	wb = xlwt.Workbook()
	ws = wb.add_sheet('Results')
	ws.write(0, 0, "Реактор")
	ws.write(0, 1, "Начало синтеза")
	ws.write(0, 2, "Конец синтеза по Р")
	ws.write(0, 3, "Конец синтеза по Т")
	wb.save('res.xls')
	print('Created')

def toExcel(reactor, start, endP, endT):
	rb = xlrd.open_workbook('res.xls')
	r_sheet = rb.sheet_by_index(0)
	r = r_sheet.nrows
	wb = copy(rb)
	sheet = wb.get_sheet(0)
	sheet.write(r ,0 ,reactor)
	sheet.write(r, 1, start)
	sheet.write(r, 2, endP)
	sheet.write(r, 3, endT)
	wb.save('res.xls')

def getDatetimeFromSeries(series):
	return str(series).split()[1] + " " + str(series).split()[2]

ROOT_DIR = './'
#f-string expression
#dframes = pd.concat([pd.read_excel(os.path.join(ROOT_DIR, f'Выгрузка_2_201{x}.xlsx'), sheet_name = f'201{x}') for x in ['7', '8', '9']], axis = 0).reset_index(drop = True)
#1576803 строки и 24 столбца
dframes = pd.read_excel(os.path.join(ROOT_DIR, 'testData.xlsx'), sheet_name = '2019')
#print(str(dframes['PSP_Measures_MR201_A.FQRC2001']))
#print(str(dframes.iloc[[5],0]))#iloc[[запись], столбец]
x = 0
#newExcel()
#Проходим по столбцу с растворителем, если больше 1000, то
#считаем что синтез начался. Определяем какой реактор по росту давления. Ищем максимумы температуры и давления,
#как метки окончания синтеза(ближайшая максимальная температура с t > 70 и 
#ближайший максимум давления с p > 0.2) 
#Следующий синтез начинаем искать через 10 минут минимум (сейчас пауза = 12)
Ap = 'PSP_MR201_A.PIRSA2011' #I
Bp = 'PSP_MR201_B.PIRSA2013' #N
Cp = 'PSP_MR201_C.PIRSA2015' #S
#Температура внизу
At = 'PSP_MR201_A.TRSA2013' #K
Bt = 'PSP_MR201_B.TRSA2018' #P
Ct = 'PSP_MR201_C.TRSA2023' #U
#
def getReactor(fromRow):#Определить название реактора,
	tmp = dframes[Bp]
	z = 10
	while z > 0 :
		print(tmp[z])#Почему 0 начинается с 3 строки???
		z -= 1
#Как переходить по строкам????
pause = 0 #Пауза между синтезами
for i in dframes['PSP_Measures_MR201_A.FQRC2001'] :#Расходомер на растворителе
	if i > 1000 and pause == 0:
		print(x)
		print(i)
		print(getDatetimeFromSeries(dframes.iloc[[x], 0]))#в excel строка соответствует i+2
		pause = 12
	x += 1
	if pause > 0 :
		pause -= 1

getReactor(5)
#counter = 0
#SZ = len(dframes.index)

#while counter < SZ:
	#print(str(dframes.iloc[[counter], 3]))
#	if dframes.iloc[[counter], 3] > 1000 :
#		print(dframes.iloc[[counter], 3])
#		if counter + 11 < SZ : 
#			counter += 11
#	counter += 1

#tmp = dframes.iloc[[10], 0]
#tmp1 = str(tmp).split()[1] + " " + str(tmp).split()[2]
#print(getDatetimeFromSeries(tmp))

#print(str(dframes[1]))

#На какую метрику рассматривать как конце синтеза:максимум температуры(верх, низ, середина) или давление? Непосредственно максимум или последующее измерение?