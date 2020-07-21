import pandas as pd
import os

ROOT_DIR = './'

df1 = pd.read_excel(os.path.join(ROOT_DIR, 'Сводный журнал результатов анализа за период (Лаборатория производства термоэластопластов) (1).xlsx'))
print(df1)