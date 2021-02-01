from sqlalchemy import Table
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import UpdateBase

class InsertFromSelect(UpdateBase):
    def __init__(self, table, select):
        self.table = table
        self.select = select

@compiles(InsertFromSelect)
def visit_insert_from_select(element, compiler, **kw):
    return "INSERT INTO %s %s" % (
        compiler.process(element.table, asfrom=True),
        compiler.process(element.select)
    )

def cloneTable(name, table, metadata):
    cols = [c.copy() for c in table.columns]
    constraints = [c.copy() for c in table.constraints]
    return Table(name, metadata, *(cols + constraints))

# test data
from sqlalchemy import MetaData, Column, Integer
from sqlalchemy.engine import create_engine
e = create_engine('sqlite://')
m = MetaData(e)
t = Table('t', m, Column('id', Integer, primary_key=True),
          Column('number', Integer))
t.create()
e.execute(t.insert().values(id=1, number=3))
e.execute(t.insert().values(id=9, number=-3))

# create temp table
temp = cloneTable('temp', t, m)
temp.create()

# copy data
ins = InsertFromSelect(temp, t.select().where(t.c.id>5))
e.execute(ins)

# print result
for r in e.execute(temp.select()):
    print(r)
