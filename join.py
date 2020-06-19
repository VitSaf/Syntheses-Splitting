import pandas as pd
import os


ROOT_DIR = './'
#f-string expression
def load():
	df1 = pd.concat([pd.read_excel(os.path.join(ROOT_DIR, f'Выгрузка_2_201{x}.xlsx'), sheet_name = f'201{x}') for x in ['7', '8', '9']], axis = 0).reset_index(drop = True)
	print('df1 загружен')
	df2 = pd.concat([pd.read_excel(os.path.join(ROOT_DIR, 'Выгрузка_MR201ABC_2017_18_19 копия.xlsx'), sheet_name=x) for x in ['2017','2018','2019']], axis = 0).reset_index(drop = True)
	print('df2 загружен')
	return pd.merge(df1, df2, left_index=True, right_index=True, how='left')

def loadTest():
	return pd.read_excel(os.path.join(ROOT_DIR, 'testData.xlsx'), sheet_name = '2019')


#pd.set_option('display.max_rows', df3.shape[0] + 1)

#dft1 = pd.read_excel(os.path.join(ROOT_DIR, 'Выгрузка_2_2017.xlsx'), sheet_name = '2017')
#dft2 = pd.read_excel(os.path.join(ROOT_DIR, 'Выгрузка_MR201ABC_2017_18_19 копия.xlsx'), sheet_name='2017')
#dft3 = pd.merge(dft1, dft2, left_index=True, right_index=True, how='left')
#dft3.to_excel('out_2017.xlsx')