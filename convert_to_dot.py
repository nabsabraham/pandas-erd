import json
import pandas as pd


class Table:
    '''
    meta_info: (df) - get df schema from BQ as pandas DataFrame
    table_info: (str) - name of the table
    filename: (str) - filename to save dot code - default is output.txt
    '''
    def __init__(self, table, table_name):
        if isinstance(table, pd.core.frame.DataFrame):
            # pass a whole dataframe
            meta = table.dtypes
            meta = meta.to_frame().reset_index()
            meta.columns = ['column_name', 'data_type']
            self.meta_info = meta.values.tolist()

        else:
            print(f' {type(table)} not accepted. must be a pandas dataframe')

        self.table_name = table_name
        self.table_def = []

        self.pad = 5
        self.align = 'left'
        self.font_color = 'grey60'

        self.__construct__()

    def __construct__(self):
        self.front_matter = f'''{self.table_name} [ label=<
        <table border="0" cellborder="1" cellspacing="0">
        <tr><td><b>{self.table_name}</b></td></tr>
        '''
        table_end = '</table>>];'
        self.table_def.append(self.front_matter)
        for col, col_type in self.meta_info:
            self.table_def.append(
                '\t\t' + f'''<tr><td port="{col}" align="{self.align}" cellpadding="{self.pad}">{col} <font color="{self.font_color}">{col_type}</font></td></tr>''')
        self.table_def.append(table_end)

        self.res = '\n'.join(self.table_def)

    def write_to_file(self, filename='output.txt'):
        self.filename = filename
        text_file = open(self.filename, "w")
        text_file.write(self.res)
        text_file.close()
        print(f'written to {self.filename}')

    def print(self):
        print(self.res)


class ERD:
    def __init__(self):
        self.table_tracker = {}
        self.table_gen_code = ['''
        digraph G {
            graph [
                nodesep=0.5;
                rankdir="LR";
                cencentrate=true;
                splines="spline";
                fontname="Helvetica";
                pad="0.2,0.2",
                label="",
                
            ];
    
        node [shape=plain, fontname="Helvetica"];
        edge [
            dir=both,
            fontsize=12,
            arrowsize=0.9,
            penwidth=1.0,
            labelangle=32,
            labeldistance=1.8,
            fontname="Helvetica"
        ];''']

    def add_table(self, df, table_name):
        table = Table(table=df, table_name=table_name)
        self.table_tracker[table_name] = table
        self.table_gen_code.append(table.res)

    def insert_table(self, table):
        assert isinstance(table, Table), f'The object you are trying to insert is {type(table)} but it should be a Table'
        self.table_gen_code.append(table.res)

    def print(self):
        self.table_gen_code.append('}')
        print(self.table_gen_code)

    def create_edge(self, table1_name, table2_name, **kwargs):
        try:
            table1 = self.table_tracker[table1_name]
        except(TableNotFoundError):
            print(f' table {table1_name} not found in tracker, create one with add_table method')

        try:
            table2 = self.table_tracker[table2_name]
        except(TableNotFoundError):
            print(f' table {table2_name} not found in tracker, create one with add_table method')

        left_on = kwargs.get('left_on', '')
        right_on = kwargs.get('right_on', '')
        left_cardinality = kwargs.get('left_cardinality', None)
        right_cardinality = kwargs.get('right_cardinality', None)

        if left_cardinality == '*':
            arrowtail = 'ocrow'
        elif left_cardinality == '+':
            arrowtail = 'noneotee'
        else:
            arrowtail = 'neneotee'

        if right_cardinality == '*':
            arrowhead = 'ocrow'
        elif right_cardinality == '+':
            arrowhead = 'noneotee'
        else:
            arrowhead = 'neneotee'

        #if (isinstance(table1, Table)) and (isinstance(table2, Table)):
        rel=f'''{table1.table_name}:{left_on}->{table2.table_name}:{right_on} [ 
                arrowhead={arrowhead}, arrowtail={arrowtail}];'''
        self.table_gen_code.append(rel)


    def write_to_file(self, filename='output.txt'):
        self.filename = filename
        tmp = self.table_gen_code
        tmp.append('}')
        self.res = '\n'.join(tmp)

        text_file = open(self.filename, "w")
        text_file.write(self.res)
        text_file.close()
        print(f'written to {self.filename}')


erd = ERD()

dummy1 = pd.DataFrame(data=[[231, 32, '1 Ottawa Street'], [123, 80, '14 Canada Road']])
dummy1.columns = ['PTNT_ID', 'STORE_CD', 'STORE_ADDRESS']
dummy2 = pd.DataFrame(data=[[6342, 23, '2020-01-02', 'L5N1X6'], [3124, 32, '2020-02-02', 'L5N1X6']])
dummy2.columns = ['PTNT_ID', 'AGE_AT_VACATION', 'DOB', 'POSTAL_CODE']

#table1 = Table(dummy1, 'RX_VAC')
#table2 = Table(dummy2, 'PTNT_CORE')

erd.add_table(dummy1, 'RX_VAC')
erd.add_table(dummy2, 'PTNT_CORE')
erd.create_edge('RX_VAC', 'PTNT_CORE', left_on='PTNT_ID', right_on='PTNT_ID', right_cardinality='*')
#erd.print()
erd.write_to_file()
#table2 = Table(meta_string, 'PTNT_CORE')
#table2.write_to_file()
#table.print()
#table2.print()
