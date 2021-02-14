import pandas as pd
from pandaserd import ERD

df1 = pd.DataFrame(data=[[123, 32, '1 Ottawa Street'], [123, 80, '14 Canada Road']])
df1.columns = ['PERSON', 'AGE', 'ADDRESS']
df2 = pd.DataFrame(data=[[6342, 124123124124, '1992-01-02', 'K012V4'], [3124, 154823124124, '1984-02-02', 'L4Y6S2']])
df2.columns = ['PERSON', 'CREDIT_CARD', 'DOB', 'POSTAL_CODE']

erd = ERD()
t1 = erd.add_table(df1, 'PERSON')
t2 = erd.add_table(df2, 'CREDIT_CARD')
erd.create_rel('PERSON', 'CREDIT_CARD', on='PERSON', left_cardinality='+', right_cardinality='*')
erd.create_rel('PERSON', 'CREDIT_CARD', left_on='AGE', right_on='DOB', right_arrow=True, left_arrow=False)

erd.write_to_file('output.txt')
