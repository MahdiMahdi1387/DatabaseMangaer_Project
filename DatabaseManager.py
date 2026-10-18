import sqlite3 as sq
from string import ascii_letters, digits
from typing import Any


class DatabaseManager:
    def __init__(
            self,
            db_name: str = 'DataBase.db',
            table_name: str = 'MyTable',
            table_query: str = 'id.INTEGER.PRIMARY.KEY.AUTOINCREMENT'
        ) -> None:
        # Error handling
        if not isinstance(table_query, str):
            raise TypeError('Invalid table query, expected str, '
                            f'got {type(table_query).__name__}')
        if not isinstance(table_name, str):
            raise TypeError('Invalid table name, expected str,'
                            f' got {type(table_name).__name__}')
        if not isinstance(db_name, str):
            raise TypeError('Invalid database name, expected str,'
                            f' got {type(db_name).__name__}')
        for i in table_name:
            if i not in ascii_letters + digits + '_':
                raise ValueError('Invalid table name, expected to only contain'
                                 f' a-z A-Z 0-9 uderscore, got {table_name}')
        for i in db_name:
            if i not in ascii_letters + digits + './_':
                raise ValueError('Invalid database name, expected to only contain'
                                 f' a-z A-Z 0-9 dot slash underscore, got {db_name}')
        if len(table_query) < 5:
            raise ValueError('Expected at least 5 character query, got'
                             f' {len(table_query)}')

        # Initializing inputs
        self.db_name = db_name
        self.table_name = table_name
        self.table_query = table_query  # . = word sep and , = command sep
        
    def query_parser(self, query: str) -> str:
        '''Parses the input query into a table query.'''

        parsed_query = (f'CREATE TABLE IF NOT EXISTS {self.table_name}(\n\t' 
            + query.replace(' ', '').replace(',', ',\n\t').replace('.', ' ')
            + '\n)')

        return parsed_query

    def init(self) -> None:
        '''Initializes the database and creates a table.'''

        with sq.connect(self.db_name) as conn:
            conn.execute(self.query_parser(self.table_query))

    def add(self, *fields: Any) -> None:
        '''Adds a record in database'''

        for field in fields:
            if not isinstance(field, str):
                raise TypeError('There is an invalid field name in your inputs.')

        questions = ''
        for i in range(len(fields)):
            if i + 1 < len(fields):
                questions += '?, '
            else:
                questions += '?'

        with sq.connect(self.db_name) as conn:
            conn.execute(
                f'INSERT INTO {self.table_name} VALUES({questions})',
                fields
            )

    def remove(self, **field: Any) -> None:
        '''Removes a record in database.'''
        
        if len(field) != 1:
            raise ValueError('Invalid amount of keys, expected 1 got ' \
                           f'{len(field)}')

        for key, value in field.items():
            field_key: str = key
            field_value: Any = value
        
        for i in field_key:
            if i not in ascii_letters + digits + '_':
                raise ValueError('Invalid key name, expected to only contain' \
                                 f' a-z A-Z 0-9 underscore, got {field_key}')
        

        with sq.connect(self.db_name) as conn:
            conn.execute(
                f'DELETE FROM {self.table_name} WHERE {field_key} = ?',
                (field_value,)
            )

    def update(self, condition: dict[str, Any] = {'id' : 1}, **fields: Any) -> None:
        '''Updates records' fields.'''

        if len(condition) != 1:
            raise ValueError('Invalid amount of keys, expected 1 got ' \
                             f'{len(condition)}')

        for field_key in fields.keys():
            for i in field_key:
                if i not in ascii_letters + digits + '_':
                    raise ValueError('Invalid key name, expected to only contain' \
                                     f' a-z A-Z 0-9 underscore, got {field_key}')

        query = f'UPDATE {self.table_name} SET '
        for i, key in enumerate(fields.keys()):
            if i + 1 < len(fields.keys()):
                query += f'{key} = ?, '
            else:
                query += f'{key} = ? '
        for key in condition.keys():
            query += f'WHERE {key} = ?'

        values: list = []

        for value in fields.values():
            values.append(value)
        for value in condition.values():
            values.append(value)
        
        with sq.connect(self.db_name) as conn:
            conn.execute(query, tuple(values))

    def show(
            self,
            condition: dict[str, Any] = {'id' : 1}, 
            *fields: str
        ) -> dict[str, Any]:
        '''Returns a record by a condition.'''

        if not isinstance(condition, dict[str, Any]):
            raise TypeError('Invalid condition, expected dict[str, Any], '
                            f'got {type(condition).__name__}')
        if not fields:
            fields = ('*',)
        if fields != ('*',):
            for field in fields:
                if not isinstance(field, str):
                    raise TypeError('Invalid table query, expected dict[str, Any], '
                                    f'got {type(field).__name__}')
                for i in field:
                    if i not in ascii_letters + digits + '_':
                        raise ValueError('Invalid fields\' name, expected to only contain'
                                        f' a-z A-Z 0-9 underscore, got {fields}')

        query = 'SELECT '
        if fields[0] == '*':
            query += fields[0]
        else:
            query += ', '. join(fields)
        for key in condition.keys():
            query += f' FROM {self.table_name} WHERE {key} = ?'

        with sq.connect(self.db_name) as conn:
            conn.row_factory = sq.Row
            for value in condition.values():
                records = conn.execute(query, (value,))
            records = records.fetchall()

        return records
