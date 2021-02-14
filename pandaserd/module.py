import json
import pandas as pd


class Table:
    """
    Instantiates a Table object which houses information about each table/df
    :param table: (pandas DataFrame) - df/table you want to add to the diagram
    :param table_name: (str) Name of the table
    """
    def __init__(self, table, table_name, **kwargs):
        if isinstance(table, pd.core.frame.DataFrame):
            # pass a whole dataframe
            meta = table.dtypes
            meta = meta.to_frame().reset_index()
            meta.columns = ['column_name', 'data_type']
            self.table_columns = set(meta.column_name)
            self.meta_info = meta.values.tolist()

        else:
            print(f' {type(table)} not accepted. must be a pandas dataframe')

        self.table_name = table_name
        self.table_def = []

        self.pad = 5
        self.align = 'left'
        self.font_color = 'grey60'
        self.bg_color = kwargs.get('bg_color', 'grey')
        bg_colors = ['lightblue', 'skyblue', 'pink', 'lightyellow', 'grey', 'gold']
        assert self.bg_color in set(bg_colors), f"{self.bg_color} not available; color must be one of {bg_colors}"
        self.__construct__()

    def __construct__(self):
        self.front_matter = f'''\n\t {self.table_name} [ label=<
        <table border="0" cellborder="1" cellspacing="0">
        <tr><td bgcolor="{self.bg_color}"><b>{self.table_name}</b></td></tr>
        '''
        table_end = '\t\t' + '</table>>];'
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
    """
    Instantiates an ERD object whose functionality includes adding tables and connecting tables
    with multiple cardinalities or just connect tables with arrows

    """
    def __init__(self):
        self.table_tracker = {}
        self.rel_tracker = set()
        self.table_gen_code = ['''digraph G {
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

    def add_table(self, df, table_name, **kwargs):
        table = Table(table=df, table_name=table_name, **kwargs)
        self.table_tracker[table_name] = table
        self.table_gen_code.append(table.res)
        return table

    def print(self):
        self.table_gen_code.append('}')
        print(self.table_gen_code)

    def __make_edge__(self):
        if self.left_cardinality == '*':
            arrowtail = 'ocrow'
        elif self.left_cardinality == '+':
            arrowtail = 'noneotee'
        else:
            arrowtail = 'none'

        if self.right_cardinality == '*':
            arrowhead = 'ocrow'
        elif self.right_cardinality == '+':
            arrowhead = 'noneotee'
        else:
            arrowhead = 'none'

        # if you didn't set cardinalities, you can make arrows
        if self.left_cardinality is None and self.right_cardinality is None:
            if self.left_arrow and self.right_arrow is False:
                rel = f'''\n\t {self.left.table_name}:{self.left_on}->{self.right.table_name}:{self.right_on} [
                        arrowhead="none"];'''
            elif self.right_arrow and self.left_arrow is False:
                rel = f'''\n\t {self.left.table_name}:{self.left_on}->{self.right.table_name}:{self.right_on} [
                            arrowtail="none"];'''
            elif self.left_arrow and self.right_arrow:
                rel = f'''\n\t {self.left.table_name}:{self.left_on}->{self.right.table_name}:{self.right_on};'''
            else:
                rel = f'''\n\t {self.left.table_name}:{self.left_on}->{self.right.table_name}:{self.right_on};'''

        else:  # use the cardinalities
            rel = f'''\n\t {self.left.table_name}:{self.left_on}->{self.right.table_name}:{self.right_on} [ 
                        arrowhead={arrowhead}, arrowtail={arrowtail}];'''

        return rel

    def create_rel(self, left_table_name, right_table_name, left_on=None, right_on=None, on=None, **kwargs):
        """
        Generates a relationship between two tables with either cardinality or just flowchart arrows.

        :param left_table_name: (str)
        :param right_table_name: (str)
        :param left_on: (str) Column in the left table
        :param right_on: (str) Column in the right table
        :param on: (str) Common column in both tables
        :param kwargs:
            left_cardinality (str):
                '*' = zero or more
                '+' = 1 or more
                '1' = 1
            right_cardinality (str):
                '*' = zero or more
                '+' = 1 or more
                '1' = 1
            left_arrow (bool):
                True : if you want the arrow to point from right to left
            right_arrow (bool):
                True : if you want the arrow to point from left to right
        :return None
        """
        # get the tables referenced by their name
        try:
            self.left = self.table_tracker[left_table_name]
        except:
            print(f' table {left_table_name} not found, create one with add_table method')
            return

        try:
            self.right = self.table_tracker[right_table_name]
        except:
            print(f' table {right_table_name} not found, create one with add_table method')
            return

        # use the on or left_on/right_on like pandas merge
        if on is not None:
            self.left_on = on
            self.right_on = on
        else:
            self.left_on = left_on
            self.right_on = right_on

        # check that the on columns exist in the tables:
        assert self.left_on in self.left.table_columns, f'Column {self.left_on} not in left table: {self.left.table_name}'
        assert self.right_on in self.right.table_columns, f'Column {self.right_on} not in right table: {self.right.table_name}'

        self.left_cardinality = kwargs.get('left_cardinality', None)
        self.right_cardinality = kwargs.get('right_cardinality', None)
        self.left_arrow = kwargs.get('left_arrow', None)
        self.right_arrow = kwargs.get('right_arrow', None)

        rel_name = f'{left_table_name}:{self.left_on}->{right_table_name}:{self.right_on}'
        # check if the rel already exist
        if rel_name in self.rel_tracker:
            print(f' Edge {rel_name} already exists, skipping this edge creation.')
        else:
            self.rel_tracker.add(rel_name)
            rel = self.__make_edge__()
            self.table_gen_code.append(rel)


    def write_to_file(self, filename='output.txt'):
        """
        Encloses the current tables and relationships into a DiGraph object (dot code) and
        writes output dot code to a text file.
        :param filename: (str) file to output the dot code to
        """
        self.filename = filename

        # did the code already end before?
        if '\t}' in set(self.table_gen_code):
            self.table_gen_code.remove('\t}')

        self.table_gen_code.append('\t}')

        tmp = self.table_gen_code
        self.res = '\n'.join(tmp)

        text_file = open(self.filename, "w")
        text_file.write(self.res)
        text_file.close()

        url='https://edotor.net/'
        print(f'written to {self.filename}; visit {url} to render ERD')
