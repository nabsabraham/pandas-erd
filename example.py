import pandas as pd
from convert_to_dot import ERD


df1 = pd.DataFrame(data=[[123, 32, '1 Ottawa Street'], [123, 80, '14 Canada Road']])
df1.columns = ['PERSON', 'AGE', 'ADDRESS']
df2 = pd.DataFrame(data=[[6342, 124123124124, '1992-01-02', 'K012V4'], [3124, 154823124124, '1984-02-02', 'L4Y6S2']])
df2.columns = ['PERSON', 'CREDIT_CARD', 'DOB', 'POSTAL_CODE']

erd = ERD()
erd.add_table(df1, 'PERSON')
erd.add_table(df2, 'CREDIT_CARD')
erd.create_edge('PERSON', 'CREDIT_CARD', left_on='PERSON', right_on='PERSON', right_cardinality='*')
erd.write_to_file('output.txt')
