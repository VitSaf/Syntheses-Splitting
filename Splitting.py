import pandas as pd
import join
from datetime import datetime, timedelta



MAIN_LIST = []
ERRORS_LIST = []
SYNT_START_VALUE = 30000 #753 строка 2019
MAX_SYNT_TIME = timedelta(hours = 2)
BLOCK1_START_VALUE_CATALYST = 300
BLOCK2_START_VALUE_BUTADIEN = 10000

#расходомер на растворителе
F_SOLVENT = 'PSP_Measures_MR201_A.FQRC2001' #D
F_CATALYST = 'PSP_Measures_MR201_A.FRCA1411' #G
F_BUTADIEN = 'PSP_Measures_MR201_A.FRC1061' #E
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


def getEndByT(fromRow, reactor):
	t = getTFromReactor(reactor)
	row = fromRow + 20
	while True:
		if t[row]>70 and t[row]>t[row -1] and t[row]>t[row+1]:
			#return getDatetimeFromSeries(dframes.iloc[[row], 0])
			return row
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
	fromRow += 3
	p = getPFromReactor(reactor)
	while True:
		if (p[fromRow] > p[fromRow-1]) and (p[fromRow] > p[fromRow+1]): #Если это первый максимум, то возвращаем номер строки
			return fromRow
		fromRow += 1

def getFirstBlockEndByT(fromRow, reactor):
	fromRow += 3
	t = getTFromReactor(reactor)
	while True:
		if (t[fromRow] > t[fromRow-1]) and (t[fromRow] > t[fromRow+1]): #Если это первый максимум, то возвращаем номер строки
			return fromRow
		fromRow += 1
#начало второго блока - конец подачи бутадиена (судя по трендам)
def getSecondBlockStart(fromRow):
	tmp = dframes[F_BUTADIEN]
	fromRow += 20#задержка для избежания пересечения синтезов
	while True:
		if tmp[fromRow] > BLOCK2_START_VALUE_BUTADIEN:#нашли начало слива бутадиена
			while True: #ищем конец слива бутадиена
				if tmp[fromRow] < BLOCK2_START_VALUE_BUTADIEN:#нашли конец слива бутадиена
					return fromRow
				fromRow += 1
		fromRow += 1

#Возвращает дату окончания синтеза второго блока
def getSecondBlockEnd(fromRow, reactor):
	p = getPFromReactor(reactor)
	row = fromRow + 20
	while True:
		if p[row]>0.2 and p[row]>p[row -1] and p[row]>p[row+1]:
			#return getDatetimeFromSeries(dframes.iloc[[row], 0])
			return row
		else:
			row += 1



print("Start")
dframes = join.loadTest() #TestData
#dframes = join.load()
print('dataframe загружен')
#print(str(dframes.iloc[[5],0]))#iloc[[запись], столбец]


	
x = 0
solvent_pause = 0 #Пауза между синтезами
for i in dframes[F_SOLVENT] :#Расходомер на растворителе
	#print(x)
	if i > SYNT_START_VALUE and solvent_pause == 0:
		start = getDatetimeFromSeries(dframes.iloc[[x], 0])
		try:
			reactor = getReactor(x)
			if reactor is None:
				ERRORS_LIST.append({'Реактор':reactor, 'Начало синтеза':str(start)})
				x += 1
				continue
			else:
				block1Start = getFirstBlockStart(x)
				block1StartDatetime = getDatetimeFromSeries(dframes.iloc[[block1Start], 0])
				endByT = getEndByT(x, reactor)#в excel строка соответствует i+2
				endByTDatetime = getDatetimeFromSeries(dframes.iloc[[endByT], 0])
				block1EndByP = getFirstBlockEndByP(x, reactor)
				block1EndByT = getFirstBlockEndByT(x, reactor)
				block1EndByPDatetime = getDatetimeFromSeries(dframes.iloc[[block1EndByP], 0])
				block1EndByTDatetime = getDatetimeFromSeries(dframes.iloc[[block1EndByT], 0])
				block2Start = getSecondBlockStart(x)
				block2End = getSecondBlockEnd(x, reactor)
				block2StartDatetime = getDatetimeFromSeries(dframes.iloc[[block2Start], 0])
				block2EndDatetime = getDatetimeFromSeries(dframes.iloc[[block2End], 0])
		except (IndexError, KeyError):#В LookupError входят IndexError и KeyError (оба эксепшена могут тут прокнуть)
			x += 1
			continue

		print(reactor)
		print(block2StartDatetime)
		print(block1EndByPDatetime)
		totalDuration = endByTDatetime - start
		block1DurationByP = block1EndByPDatetime - block1StartDatetime
		block1DurationByT = block1EndByTDatetime - block1StartDatetime
		block2Duration = block2EndDatetime - block2StartDatetime

		pauseBetweenBlock1AndBlock2 = block2StartDatetime - block1EndByPDatetime# ошибки из-за пересечения синтезов

		if totalDuration < MAX_SYNT_TIME:
			MAIN_LIST.append({'Реактор':reactor, 'Начало синтеза':str(start), 'Конец синтеза': str(endByTDatetime), 'Длительность синтеза':str(totalDuration), 'Длительность первого блока по Р': str(block1DurationByP),
				'Длительность первого блока по Т':str(block1DurationByT), 'Длительность второго блока': str(block2Duration), 'Пауза между 1(по Р) и 2 блоком': str(pauseBetweenBlock1AndBlock2)})
		else:
			ERRORS_LIST.append({'Реактор':reactor, 'Начало синтеза':str(start), 'Конец синтеза': str(endByT)})


		solvent_pause = 12#Избавиться
	x += 1
	if solvent_pause > 0 :
		solvent_pause -= 1


pd.DataFrame(MAIN_LIST).to_excel('output.xlsx')
pd.DataFrame(ERRORS_LIST).to_excel('errors.xlsx')
