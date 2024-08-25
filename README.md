# sqlite-minutils


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

    pip install sqlite-minutils

## Use

First, import the sqlite-miniutils library. Through the use of the
**all** attribute in our Python modules by using `import *` we only
bring in the `Database`, `Queryable`, `Table`, `View` classes. There’s
no risk of namespace pollution.

``` python
from sqlite_minutils.db import *
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
users.create(columns=dict(name=str, age=int))
users
```

    <Table Users (name, age)>

What if we need to change the table structure?

For example User tables often include things like password field. Let’s
add that now by calling `create` again, but this time with
`transform=True`. We should now see that the `users` table now has the
`pwd:str` field added.

``` python
users.create(columns=dict(name=str, age=int, pwd=str), transform=True)
users
```

    <Table Users (name, age, pwd)>

``` python
print(db.schema)
```

    CREATE TABLE "Users" (
       [name] TEXT,
       [age] INTEGER,
       [pwd] TEXT
    );
