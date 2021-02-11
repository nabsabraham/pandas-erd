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
        self.front_matter = f'''\n\t {self.table_name} [ label=<
        <table border="0" cellborder="1" cellspacing="0">
        <tr><td><b>{self.table_name}</b></td></tr>
        '''
        table_end = '\t\t' +  '</table>>];'
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
        except:
            print(f' table {table1_name} not found, create one with add_table method')
            return

        try:
            table2 = self.table_tracker[table2_name]
        except:
            print(f' table {table2_name} not found, create one with add_table method')
            return

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

        rel=f'''\n\t {table1.table_name}:{left_on}->{table2.table_name}:{right_on} [ 
                arrowhead={arrowhead}, arrowtail={arrowtail}];'''
        self.table_gen_code.append(rel)


    def write_to_file(self, filename='output.txt'):
        self.filename = filename
        tmp = self.table_gen_code
        tmp.append('\t}')
        self.res = '\n'.join(tmp)

        text_file = open(self.filename, "w")
        text_file.write(self.res)
        text_file.close()
        print(f'written to {self.filename}')

