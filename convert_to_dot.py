import json
import pandas as pd

table_string='{"columns":["column_name","data_type"],"index":[0,1,2,3,4,5],"data":[["PTNT_IP_ID","INT64"],["PTNT_MATCH_ID","INT64"],["GENDER","STRING"],["birth_year","INT64"],["city","STRING"],["prov","STRING"]]}'
parse = json.loads(table_string)


columns = parse['data']
table_name = 'RX_VACCINES'
align = 'left'
pad = 5
font_color = 'grey60'
table_def = []

front = f'''{table_name} [ label=<
        <table border="0" cellborder="1" cellspacing="0">
        <tr><td><i>{table_name}</i></td></tr>
        '''
end = '</table>>];'
table_def.append(front)
for col, col_type in columns:
    table_def.append('\t' + f'''<tr><td port="{col}" align="{align}" cellpadding="{pad}">{col} <font color="{font_color}">{col_type}</font></td></tr>''')

table_def.append(end)
res = '\n'.join(table_def)
#print(res)

#text_file = open("output.txt", "w")
#text_file.write(res)
#text_file.close()


class Table:
    '''
    meta_info: (df) - get df schema from BQ as pandas DataFrame
    table_info: (str) - name of the table
    filename: (str) - filename to save dot code - default is output.txt
    '''
    def __init__(self, meta_info, table_name):
        if isinstance(meta_info, str):
            # this would be the json object after printing the schema from BQ
            self.meta_info = json.loads(meta_info)

        elif isinstance(meta_info, pd.core.frame.DataFrame):
            # pass a whole dataframe
            meta = meta_info.dtypes
            meta = meta.to_frame().reset_index()
            meta.columns = ['column_name', 'data_type']
            self.meta_info = meta.values.tolist()

        else:
            print(f' {type(meta_info)} not accepted. must be a pandas dataframe')
            #self.meta_info = json.loads(meta_info.to_json(orient='split'))
        self.columns = self.meta_info['data']
        self.table_name = table_name
        self.table_def = []

        self.__construct__()

    def __construct__(self):
        self.front_matter = f'''{self.table_name} [ label=<
        <table border="0" cellborder="1" cellspacing="0">
        <tr><td><b>{self.table_name}</b></td></tr>
        '''
        self.table_end = '</table>>];'
        self.table_def.append(self.front_matter)
        for col, col_type in self.columns:
            self.table_def.append(
                '\t\t' + f'''<tr><td port="{col}" align="{align}" cellpadding="{pad}">{col} <font color="{font_color}">{col_type}</font></td></tr>''')
        self.table_def.append(end)

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

    def insert_table(self, table):
        assert isinstance(table, Table), f'The object you are trying to insert is {type(table)} but it should be a Table'
        self.table_gen_code.append(table.res)

    def print(self):
        self.table_gen_code.append('}')
        print(self.table_gen_code)

    def create_edge(self, table1, table2, **kwargs):
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

        if (isinstance(table1, Table)) and (isinstance(table2, Table)):
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

meta_string1 ='{"columns":["column_name","data_type"],"index":[0,1,2,3,4,5],"data":[["PTNT_IP_ID","INT64"],["PTNT_MATCH_ID","INT64"],["GENDER","STRING"],["birth_year","INT64"],["city","STRING"],["prov","STRING"]]}'
meta_string2 = '{"columns":["column_name","data_type"],"index":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],"data":[["PTNT_GUID","STRING"],["PTNT_MATCH_ID","INT64"],["PTNT_IP_ID","INT64"],["PTNT_NO","STRING"],["STORE_CD","STRING"],["PTNT_EFF_FROM_DT","DATE"],["PTNT_EFF_TO_DT","DATE"],["GENDER","STRING"],["PTNT_CITY","STRING"],["PTNT_PSTL_CD_FSA","STRING"],["PTNT_PROV","STRING"],["ADR_EFF_FROM_DT","DATE"],["ADR_EFF_TO_DT","DATE"],["AGE_BUCKET","STRING"],["ENTERPRISE_CD","STRING"],["DIG_PTNT_FLG","STRING"]]}'

table1 = Table(meta_string1, 'RX_VAC')
table2 = Table(meta_string2, 'PTNT_CORE')

#erd.insert_table(table1)
#erd.insert_table(table2)
erd.create_edge(table1, table2, left_on='PTNT_IP_ID', right_on='PTNT_IP_ID')
#erd.print()
erd.write_to_file()
#table2 = Table(meta_string, 'PTNT_CORE')
#table2.write_to_file()
#table.print()
#table2.print()
