import pandas as pd
from convert_to_dot import ERD


df1 = pd.DataFrame(data=[[231, 32, '1 Ottawa Street'], [123, 80, '14 Canada Road']])
df1.columns = ['PTNT_ID', 'STORE_CD', 'STORE_ADDRESS']
df2 = pd.DataFrame(data=[[6342, 23, '2020-01-02', 'L5N1X6'], [3124, 32, '2020-02-02', 'L5N1X6']])
df2.columns = ['PTNT_ID', 'AGE_AT_VACATION', 'DOB', 'POSTAL_CODE']

erd = ERD()
erd.add_table(df1, 'RX_VAC')
erd.add_table(df2, 'PTNT_CORE')
erd.create_edge('RX_VAC', 'PTNT_CORE', left_on='PTNT_ID', right_on='PTNT_ID', right_cardinality='*')
erd.write_to_file('example.txt')
