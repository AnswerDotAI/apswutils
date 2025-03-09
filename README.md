# apswutils


<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

> [!TIP]
>
> ### Where to find the complete documentation for this library
>
> If you want to learn about everything this project can do, we
> recommend reading the Python library section of the sqlite-utils
> project
> [here](https://sqlite-utils.datasette.io/en/stable/python-api.html).
>
> This project wouldn’t exist without Simon Willison and his excellent
> [sqlite-utils](https://github.com/simonw/sqlite-utils) project. Most
> of this project is his code, with some minor changes made to it.

## Install

    pip install apswutils

## Use

First, import the apswutils library. Through the use of the **all**
attribute in our Python modules by using `import *` we only bring in the
`Database`, `Queryable`, `Table`, `View` classes. There’s no risk of
namespace pollution.

``` python
from apswutils.db import *
```

Then we create a SQLite database. For the sake of convienance we’re
doing it in-memory with the `:memory:` special string. If you wanted
something more persistent, name it something not surrounded by colons,
`data.db` is a common file name.

``` python
db = Database(":memory:")
```

Let’s drop (aka ‘delete’) any tables that might exist. These docs also
serve as a test harness, and we want to make certain we are starting
with a clean slate. This also serves as a handy sneak preview of some of
the features of this library.

``` python
for t in db.tables: t.drop()
```

User tables are a handy way to create a useful example with some
real-world meaning. To do this, we first instantiate the `users` table
object:

``` python
users = Table(db, 'Users')
users
```

    <Table Users (does not exist yet)>

The table doesn’t exist yet, so let’s add some columns via the
`Table.create` method:

``` python
users.create(columns=dict(id=int, name=str, age=int))
users
```

    <Table Users (id, name, age)>

What if we need to change the table structure?

For example User tables often include things like password field. Let’s
add that now by calling `create` again, but this time with
`transform=True`. We should now see that the `users` table now has the
`pwd:str` field added.

``` python
users.create(columns=dict(id=int, name=str, age=int, pwd=str), transform=True, pk='id')
users
```

    <Table Users (id, name, age, pwd)>

``` python
print(db.schema)
```

    CREATE TABLE "Users" (
       [id] INTEGER PRIMARY KEY,
       [name] TEXT,
       [age] INTEGER,
       [pwd] TEXT
    );

## Queries

Let’s add some users to query:

``` python
users.insert(dict(name='Raven', age=8, pwd='s3cret'))
users.insert(dict(name='Magpie', age=5, pwd='supersecret'))
users.insert(dict(name='Crow', age=12, pwd='verysecret'))
users.insert(dict(name='Pigeon', age=3, pwd='keptsecret'))
users.insert(dict(name='Eagle', age=7, pwd='s3cr3t'))
```

    <Table Users (id, name, age, pwd)>

A simple unfiltered select can be executed using `rows` property on the
table object.

``` python
users.rows
```

    <generator object Queryable.rows_where>

Let’s iterate over that generator to see the results:

``` python
[o for o in users.rows]
```

    [{'id': 1, 'name': 'Raven', 'age': 8, 'pwd': 's3cret'},
     {'id': 2, 'name': 'Magpie', 'age': 5, 'pwd': 'supersecret'},
     {'id': 3, 'name': 'Crow', 'age': 12, 'pwd': 'verysecret'},
     {'id': 4, 'name': 'Pigeon', 'age': 3, 'pwd': 'keptsecret'},
     {'id': 5, 'name': 'Eagle', 'age': 7, 'pwd': 's3cr3t'}]

Filtering can be done via the `rows_where` function:

``` python
[o for o in users.rows_where('age > 3')]
```

    [{'id': 1, 'name': 'Raven', 'age': 8, 'pwd': 's3cret'},
     {'id': 2, 'name': 'Magpie', 'age': 5, 'pwd': 'supersecret'},
     {'id': 3, 'name': 'Crow', 'age': 12, 'pwd': 'verysecret'},
     {'id': 5, 'name': 'Eagle', 'age': 7, 'pwd': 's3cr3t'}]

We can also `limit` the results:

``` python
[o for o in users.rows_where('age > 3', limit=2)]
```

    [{'id': 1, 'name': 'Raven', 'age': 8, 'pwd': 's3cret'},
     {'id': 2, 'name': 'Magpie', 'age': 5, 'pwd': 'supersecret'}]

The `offset` keyword can be combined with the `limit` keyword.

``` python
[o for o in users.rows_where('age > 3', limit=2, offset=1)]
```

    [{'id': 2, 'name': 'Magpie', 'age': 5, 'pwd': 'supersecret'},
     {'id': 3, 'name': 'Crow', 'age': 12, 'pwd': 'verysecret'}]

The `offset` must be used with `limit` or raise a `ValueError`:

``` python
try:
    [o for o in users.rows_where(offset=1)]
except ValueError as e:
    print(e)
```

    Cannot use offset without limit

## Transactions

If you have any SQL calls outside an explicit transaction, they are
committed instantly.

To group 2 or more queries together into 1 transaction, wrap them in a
BEGIN and COMMIT, executing ROLLBACK if an exception is caught:

``` python
users.get(1)
```

    {'id': 1, 'name': 'Raven', 'age': 8, 'pwd': 's3cret'}

``` python
db.begin()
try:
    users.delete([1])
    db.execute('FNOOORD')
    db.commit()
except Exception as e:
    print(e)
    db.rollback()
```

    near "FNOOORD": syntax error

Because the transaction was rolled back, the user was not deleted:

``` python
users.get(1)
```

    {'id': 1, 'name': 'Raven', 'age': 8, 'pwd': 's3cret'}

Let’s do it again, but without the DB error, to check the transaction is
successful:

``` python
db.begin()
try:
    users.delete([1])
    db.commit()
except Exception as e: db.rollback()
```

``` python
try:
    users.get(1)
    print("Delete failed!")
except: print("Delete succeeded!")
```

    Delete succeeded!

## Differences from sqlite-utils and sqlite-minutils

- WAL is the default
- Setting `Database(recursive_triggers=False)` works as expected
- Primary keys must be set on a table for it to be a target of a foreign
  key
- Errors have been changed minimally, future PRs will change them
  incrementally

## Differences in error handling

| Old/sqlite3/dbapi | New/APSW | Reason |
|----|----|----|
| IntegrityError | apsw.ConstraintError | Caused due to SQL transformation blocked on database constraints |
| sqlite3.dbapi2.OperationalError | apsw.Error | General error, OperationalError is now proxied to apsw.Error |
| sqlite3.dbapi2.OperationalError | apsw.SQLError | When an error is due to flawed SQL statements |
| sqlite3.ProgrammingError | apsw.ConnectionClosedError | Caused by an improperly closed database file |

## Handling of default values

Default values are handled as expected, including expression-based
default values:

``` python
db.execute("""
DROP TABLE IF EXISTS migrations;
CREATE TABLE IF NOT EXISTS migrations (
    id INTEGER PRIMARY KEY,
    name TEXT DEFAULT 'foo',
    cexpr TEXT DEFAULT ('abra' || 'cadabra'),
    rand INTEGER DEFAULT (random()),
    unix_epoch FLOAT DEFAULT (unixepoch('subsec')),
    json_array JSON DEFAULT (json_array(1,2,3,4)),
    inserted_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);
""")
```

    <apsw.Cursor>

``` python
migrations = Table(db, 'migrations')
migrations.default_values
```

    {'name': 'foo',
     'cexpr': SQLExpr: 'abra' || 'cadabra',
     'rand': SQLExpr: random(),
     'unix_epoch': SQLExpr: unixepoch('subsec'),
     'json_array': SQLExpr: json_array(1,2,3,4),
     'inserted_at': SQLExpr: CURRENT_TIMESTAMP}

``` python
assert all([type(x) is SQLExpr for x in list(migrations.default_values.values())[1:]])
```

``` python
migrations.insert(dict(id=0))
migrations.insert(dict(id=1))
```

    <Table migrations (id, name, cexpr, rand, unix_epoch, json_array, inserted_at)>

Default expressions are executed independently for each row on row
insertion:

``` python
rows = list(migrations.rows)
rows
```

    [{'id': 0,
      'name': 'foo',
      'cexpr': 'abracadabra',
      'rand': 8201569685582150332,
      'unix_epoch': 1741481111.188,
      'json_array': '[1,2,3,4]',
      'inserted_at': '2025-03-09 00:45:11'},
     {'id': 1,
      'name': 'foo',
      'cexpr': 'abracadabra',
      'rand': 1625289491289542947,
      'unix_epoch': 1741481111.19,
      'json_array': '[1,2,3,4]',
      'inserted_at': '2025-03-09 00:45:11'}]

``` python
assert rows[0]['rand'] != rows[1]['rand']
```
