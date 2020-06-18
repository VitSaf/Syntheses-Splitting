import pandas as pd
import os
import xlwt
import xlrd
from xlutils.copy import copy
import join
from datetime import datetime, timedelta



ROOT_DIR = './'
MAIN_LIST = []
ERRORS_LIST = []
SYNT_START_VALUE = 30000 #753 строка 2019
MAX_SYNT_TIME = timedelta(hours = 2)
BLOCK1_START_VALUE_CATALYST = 300

#расходомер на растворителе
F_SOLVENT = 'PSP_Measures_MR201_A.FQRC2001' #D
F_CATALYST = 'PSP_Measures_MR201_A.FRCA1411' #G
#Давление
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


def getDatetimeFromSeries(series):
	tmp = str(series).split()[1] + " " + str(series).split()[2]
	tmp = tmp.split('.')[0]
	return datetime.strptime(tmp, '%Y-%m-%d %H:%M:%S')

#Проходим по столбцу с растворителем, если больше 1000, то
#считаем что синтез начался. Определяем какой реактор по росту давления. Ищем максимумы температуры и давления,
#как метки окончания синтеза(ближайшая максимальная температура с t > 70 и 
#ближайший максимум давления с p > 0.2) 
#Следующий синтез начинаем искать через 10 минут минимум (сейчас пауза = 12)


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
	if (A[row - 1] < 1) and ((A[row] > A[row - 1]) or (A[row + 1] > A[row])):
		return 'A'
	if (B[row - 1] < 1) and ((B[row] > B[row - 1]) or (B[row + 1] > B[row])):
		return 'B'
	if (C[row - 1] < 1) and ((C[row] > C[row - 1]) or (C[row + 1] > C[row])):
		return 'C'


#Возвращает столбец с температурой в реактора
def getTFromReactor(reactor):
	if reactor == 'A':
		return dframes[At]
	if reactor == 'B':
		return dframes[Bt]
	if reactor == 'C':
		return dframes[Ct]
	if reactor is None:
		return 'None?'
#Возвращает столбец с давлением реактора
def getPFromReactor(reactor):
	if reactor == 'A':
		return dframes[Ap]
	if reactor == 'B':
		return dframes[Bp]
	if reactor == 'C':
		return dframes[Cp]
	if reactor is None:
		return 'None?'


#Возвращает дату окончания синтеза по Р
def getEndByP(fromRow, reactor):
	p = getPFromReactor(reactor)
	row = fromRow + 20
	while True:
		if p[row]>0.2 and p[row]>p[row -1] and p[row]>p[row+1]:
			return getDatetimeFromSeries(dframes.iloc[[row], 0])
		else:
			row += 1

def getEndByT(fromRow, reactor):
	t = getTFromReactor(reactor)
	row = fromRow + 20
	while True:
		if t[row]>70 and t[row]>t[row -1] and t[row]>t[row+1]:
			return getDatetimeFromSeries(dframes.iloc[[row], 0])
		else:
			row += 1
#Вернет номер строки, с которой началась подача бутиллития 
def getFirstBlockStart(fromRow):
	tmp = dframes[F_CATALYST]
	while True:
		if tmp[fromRow] > BLOCK1_START_VALUE_CATALYST:
			return fromRow
		fromRow += 1

#Вернет номер строки окончания первого блока по Р
def getFirstBlockEndByP(fromRow, reactor):
	p = getPFromReactor(reactor)
	while True:
		if (p[fromRow] > p[fromRow-1]) and (p[fromRow] > p[fromRow+1]): #Если это первый максимум, то возвращаем номер строки
			return fromRow
		fromRow += 1

def getFirstBlockEndByT(fromRow, reactor):
	t = getTFromReactor(reactor)
	while True:
		if (t[fromRow] > t[fromRow-1]) and (t[fromRow] > t[fromRow+1]): #Если это первый максимум, то возвращаем номер строки
			return fromRow
		fromRow += 1



print("Start")
#dframes = pd.read_excel(os.path.join(ROOT_DIR, 'testData.xlsx'), sheet_name = '2019') #TestData
dframes = join.load()
print('dataframe загружен')
#print(str(dframes.iloc[[5],0]))#iloc[[запись], столбец]


	
x = 0
solvent_pause = 0 #Пауза между синтезами
for i in dframes[F_SOLVENT] :#Расходомер на растворителе
	print(x)
	if i > SYNT_START_VALUE and solvent_pause == 0:
		start = getDatetimeFromSeries(dframes.iloc[[x], 0])
		try:
			reactor = getReactor(x)
			if reactor is None:
				ERRORS_LIST.append({'Реактор':reactor, 'Начало синтеза':str(start)})
				x += 1
				continue
			else:
				#endByP = getEndByP(x, reactor)
				block1Start = getDatetimeFromSeries(dframes.iloc[[getFirstBlockStart(x)], 0])
				endByT = getEndByT(x, reactor)#в excel строка соответствует i+2
				block1EndByP = getDatetimeFromSeries(dframes.iloc[[getFirstBlockEndByP(x, reactor)], 0])
				block1EndByT = getDatetimeFromSeries(dframes.iloc[[getFirstBlockEndByT(x, reactor)], 0])
		except (IndexError, KeyError):#В LookupError входят IndexError и KeyError (оба эксепшена могут тут прокнуть)
			x += 1
			continue



		totalDuration = endByT - start
		block1DurationByP = block1EndByP - block1Start
		block1DurationByT = block1EndByT - block1Start

		if totalDuration < MAX_SYNT_TIME:
			MAIN_LIST.append({'Реактор':reactor, 'Начало синтеза':str(start), 'Конец синтеза': str(endByT), 'Длительность синтеза':str(totalDuration), 'Длительность первого блока по Р': str(block1DurationByP),
				'Длительность первого блок по Т':str(block1DurationByT)})
		else:
			ERRORS_LIST.append({'Реактор':reactor, 'Начало синтеза':str(start), 'Конец синтеза': str(endByT)})


		solvent_pause = 12#Избавиться
	x += 1
	if solvent_pause > 0 :
		solvent_pause -= 1


pd.DataFrame(MAIN_LIST).to_excel('output.xlsx')
pd.DataFrame(ERRORS_LIST).to_excel('errors.xlsx')
