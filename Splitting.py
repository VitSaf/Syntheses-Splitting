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
dframes = pd.read_excel(os.path.join(ROOT_DIR, 'testData.xlsx'), sheet_name = '2019') #TestData
#print(str(dframes['PSP_Measures_MR201_A.FQRC2001']))
#print(str(dframes.iloc[[5],0]))#iloc[[запись], столбец]

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
#найти причину, по которой возвращает None
def getReactor(fromRow):#Определяет название реактора,
	A = dframes[Ap]
	B = dframes[Bp]
	C = dframes[Cp]
	i = fromRow + 2
	if (A[i] < 0.1) and (A[i+4] < A[i+5]): 
		return 'А'
	if (B[i] < 0.1) and (B[i+4] < B[i+5]):
		return 'Б'
	if (C[i] < 0.1) and (C[i+4] < C[i+5]):
		return 'В'

#Возвращает дату окончания синтеза по Р
def getEndByP(fromRow, reactor):
	if reactor == 'А':
		p = dframes[Ap]
	if reactor == 'Б':
		p = dframes[Bp]
	if reactor == 'В':
		p = dframes[Cp]
	row = fromRow + 20
	if reactor is None:
		return 'None?'
	while True:
		if p[row]>0.2 and p[row]>p[row -1] and p[row]>p[row+1]:
			return getDatetimeFromSeries(dframes.iloc[[row], 0])
		else:
			row += 1

def getEndByT(fromRow, reactor):
	if reactor == 'А':
		t = dframes[At]
	if reactor == 'Б':
		t = dframes[Bt]
	if reactor == 'В':
		t = dframes[Ct]
	row = fromRow + 20
	if reactor is None:
		return 'None?'
	while True:
		if t[row]>70 and t[row]>t[row -1] and t[row]>t[row+1]:
			return getDatetimeFromSeries(dframes.iloc[[row], 0])
		else:
			row += 1

newExcel()	
x = 0
pause = 0 #Пауза между синтезами
for i in dframes['PSP_Measures_MR201_A.FQRC2001'] :#Расходомер на растворителе
	if i > 1000 and pause == 0:
		start = getDatetimeFromSeries(dframes.iloc[[x], 0])
		reactor = getReactor(x)
		endP = getEndByP(x, reactor)
		endT = getEndByT(x, reactor)#в excel строка соответствует i+2
		toExcel(reactor, start, endP, endT)
		pause = 12
	x += 1
	if pause > 0 :
		pause -= 1
