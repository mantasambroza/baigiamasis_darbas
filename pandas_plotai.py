import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import numpy as np

engine = create_engine('sqlite:///lazeriu_duomenys.db')
df = pd.read_sql_table('lazeriu_duomenys', engine)
df['Date'] = pd.to_datetime(df['Date'])
serial = 'K0127124'
df_dut = df[df['Serial'] == serial]
dut_idx = df.index[df['Serial'] == serial]

#col = np.where(df.index[df['Serial'] == serial], 'r', 'g')[0].strip("'")
col = ''.join(np.where(df.index[df['Serial'] == serial], 'r', 'g').tolist()).strip("'")


print(f'Pilnas stringas: {col}')

