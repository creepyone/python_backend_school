from sqlalchemy import MetaData
from enum import Enum, unique

from sqlalchemy import Column, Date, Enum as PgEnum, \
    ForeignKey, ForeignKeyConstraint, Integer, MetaData, String, Table


convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),

    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
    'pk': 'pk__%(table_name)s'
}
metadata = MetaData(naming_convention=convention)


@unique
class ShopUnitType(Enum):
    offer = 'OFFER'
    category = 'CATEGORY'


imports_table = Table(
    'imports',
    metadata,
    Column('import_id', Integer, primary_key=True)
)

shop_units_table = Table(
    'shop_units',
    metadata,
    Column('import_id', String, ForeignKey('imports.import_id'), primary_key=True),
    Column('unit_id', Integer, primary_key=True),
    Column('name', String, nullable=False, index=True),
    Column('date', Date, nullable=False),
    Column('parent_id', String, nullable=True),
    Column('type', PgEnum(ShopUnitType, name='type'), nullable=False),
    Column('price', Integer, nullable=True)
)

relations_table = Table(
    'relations',
    metadata,
    Column('import_id', Integer, primary_key=True),
    Column('parent_id', Integer, primary_key=True),
    Column('child_id', Integer, primary_key=True),
    ForeignKeyConstraint(
        ('import_id', 'parent_id'),
        ('citizens.import_id', 'citizens.citizen_id')
    ),
    ForeignKeyConstraint(
        ('import_id', 'child_id'),
        ('citizens.import_id', 'citizens.citizen_id')
    ),
)