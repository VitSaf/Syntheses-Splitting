import pandas as pd
import os
import xlwt
import xlrd
from xlutils.copy import copy
import join
from datetime import datetime

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
	tmp = str(series).split()[1] + " " + str(series).split()[2]
	tmp = tmp.split('.')[0]
	return datetime.strptime(tmp, '%Y-%m-%d %H:%M:%S')

ROOT_DIR = './'
MAIN_LIST = []
SYNT_START_VALUE = 30000 #753 строка 2019

dframes = pd.read_excel(os.path.join(ROOT_DIR, 'testData.xlsx'), sheet_name = '2019') #TestData
#dframes = join.load()

#print(str(dframes.iloc[[5],0]))#iloc[[запись], столбец]

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
#Уровень
Al = 'PSP_MR201_A.LIRSA2011' #Y
Bl = 'PSP_MR201_B.LIRSA2014' #Z
Cl = 'PSP_MR201_C.LIRSA2017' #AA


def getReactorByP(fromRow):#Определяет название реактора,
	A = dframes[Ap]
	B = dframes[Bp]
	C = dframes[Cp]
	i = fromRow + 2
	if (A[i] < 0.1) and (A[i+4] < A[i+5]): 
		return 'A'
	if (B[i] < 0.1) and (B[i+4] < B[i+5]):
		return 'B'
	if (C[i] < 0.1) and (C[i+4] < C[i+5]):
		return 'C'

def getReactor(row):
	A = dframes[Al]
	B = dframes[Bl]
	C = dframes[Cl]
	#print('A' ,A[row - 1], A[row])
	#print('B' ,B[row - 1], B[row])
	#print('C' ,C[row - 1], C[row])

	if (A[row - 1] < 1) and ((A[row] > A[row - 1]) or (A[row + 1] > A[row])):
		return 'A'
	if (B[row - 1] < 1) and ((B[row] > B[row - 1]) or (B[row + 1] > B[row])):
		return 'B'
	if (C[row - 1] < 1) and ((C[row] > C[row - 1]) or (C[row + 1] > C[row])):
		return 'C'


#Возвращает дату окончания синтеза по Р
def getEndByP(fromRow, reactor):
	if reactor == 'A':
		p = dframes[Ap]
	if reactor == 'B':
		p = dframes[Bp]
	if reactor == 'C':
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
	if reactor == 'A':
		t = dframes[At]
	if reactor == 'B':
		t = dframes[Bt]
	if reactor == 'C':
		t = dframes[Ct]
	row = fromRow + 20
	if reactor is None:
		return 'None?'
	while True:
		if t[row]>70 and t[row]>t[row -1] and t[row]>t[row+1]:
			return getDatetimeFromSeries(dframes.iloc[[row], 0])
		else:
			row += 1












#newExcel()	
x = 0
pause = 0 #Пауза между синтезами
for i in dframes['PSP_Measures_MR201_A.FQRC2001'] :#Расходомер на растворителе
	if i > SYNT_START_VALUE and pause == 0:
		start = getDatetimeFromSeries(dframes.iloc[[x], 0])
		reactor = getReactor(x)
		endByP = getEndByP(x, reactor)
		endByT = getEndByT(x, reactor)#в excel строка соответствует i+2
		try:
			duration = endByT - start
			print(duration)
		except TypeError as e:
			duration = 'ошибка'
		
		MAIN_LIST.append({'Реактор':reactor, 'Начало синтеза':str(start), 'Конец синтеза': str(endByT), 'Длительность синтеза':str(duration) })
		#toExcel(reactor, start, endP, endT)
		pause = 12
	x += 1
	if pause > 0 :
		pause -= 1


pd.DataFrame(MAIN_LIST).to_excel('output.xlsx')
