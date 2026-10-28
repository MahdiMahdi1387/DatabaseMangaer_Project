SQLite Database Manager

A lightweight, object-oriented Python utility for managing SQLite databases. This project provides a simple interface for creating tables, inserting records, deleting records, updating existing data, and retrieving records without manually writing SQL queries for every operation.

Features

- Automatic Database Initialization: Connects to an SQLite database and creates the specified table if it does not already exist.
- Custom Table Definitions: Define table columns and constraints using a compact, custom query syntax.
- Insert Records: Add new records using positional arguments.
- Delete Records: Remove records by specifying a field and its value.
- Update Records: Modify selected fields of existing records using conditions.
- Retrieve Records: Fetch records by conditions and optionally select specific columns.
- Parameterized Queries: Uses SQLite parameter binding for record values.
- Input Validation: Validates database names, table names, field names, and input types.
- Automatic Resource Management: Uses context managers to manage SQLite connections.

Technologies

- Python
- SQLite3
- Python Type Hints

Requirements

- Python 3.10 or later is recommended for compatibility with the type annotations used in this project.

The "sqlite3", "string", and "typing" modules are part of the Python standard library, so no external dependencies are required for the functionality shown.

Installation

Clone the repository:

git clone <repository-url>
cd <repository-directory>

No additional package installation is required.

Quick Start

1. Import the Class

from database_manager import DatabaseManager

Replace "database_manager" with the name of the Python file containing the class.

2. Initialize the Database

db = DatabaseManager(
    db_name="DataBase.db",
    table_name="Users",
    table_query="id.INTEGER.PRIMARY.KEY.AUTOINCREMENT,username.TEXT,email.TEXT"
)

db.init()

The custom table-definition syntax uses:

- "." to separate SQL keywords within a column definition.
- "," to separate column definitions.

For example:

id.INTEGER.PRIMARY.KEY.AUTOINCREMENT,username.TEXT,email.TEXT

is transformed into a SQL table definition.

3. Insert Records

db.add(1, "mahdi", "mahdi@example.com")

The "add()" method inserts the supplied values into the table.

Note: The number and order of values must match the table's columns. If the table uses an automatically generated primary key, the insertion method may need to be adjusted to omit that column.

4. Retrieve Records

Retrieve all columns from a record:

records = db.show({"id": 1})

for record in records:
    print(dict(record))

Retrieve selected columns:

records = db.show({"id": 1}, "username", "email")

for record in records:
    print(dict(record))

The "show()" method returns fetched SQLite rows, which can be accessed by column name.

5. Update Records

db.update(
    condition={"id": 1},
    username="new_username",
    email="new@example.com"
)

This updates the specified fields for records matching the given condition.

6. Delete Records

db.remove(id=1)

This removes records whose "id" matches the supplied value.

API Reference

Method| Description
"DatabaseManager(...)"| Configures the database name, table name, and table definition.
"query_parser(query)"| Converts the custom table-definition syntax into a SQL "CREATE TABLE" statement.
"init()"| Opens the database and creates the table if it does not exist.
"add(*fields)"| Inserts a record using the supplied values.
"remove(**field)"| Deletes records matching a specified field and value.
"update(condition, **fields)"| Updates selected fields for records matching a condition.
"show(condition, *fields)"| Retrieves records matching a condition, optionally selecting specific columns.

Design
- Create: Initialize the database table.
- Read: Retrieve records.
- Update: Modify existing records.
- Delete: Remove records.

The implementation uses Python's built-in "sqlite3" module to execute SQL statements and parameterized queries to bind record values.

Limitations

- The current implementation is designed to work with a single configured table per instance.
- The "add()" method expects values for the table's columns in their defined order.
- The update and retrieval methods currently support a single condition.
- The custom table-definition syntax is a simplified representation of SQL rather than a complete SQL parser.
- The current implementation does not provide transaction management beyond SQLite's connection context managers, database migrations, or a dedicated exception-handling layer.
- Table and column identifiers are interpolated into SQL statements, so identifier validation and safe query construction remain important.

Future Improvements

Potential improvements include:

- Support for inserting records without explicitly providing automatically generated IDs.
- More flexible filtering conditions.
- Better handling of SQLite errors and constraint violations.
- Support for multiple tables.
- Improved SQL identifier validation.
- Unit tests and automated testing.
- Type annotations and return types that accurately describe the returned records.

License

No license has been specified yet.
The project encapsulates database operations inside a single class, reducing repetitive connection-management code and providing a consistent interface for common CRUD operations.

CRUD stands for:
