# Release notes

## 0.1.1

- Query fix to accept dict as parameters bug
- Allow using SQL functions for default values
- Use rowtrace func to convert row to dict
- Database.query() rows as AttrDict via AttrDictRowFactory
- Remove OperationError

## 0.1.0

- Bump version number due to breaking change

## 0.0.3

### Breaking changes

- `fetchone` has been renamed to `item`, and now raises an exception if >1 rows or fields are present

## 0.0.2

### New features

- Add `modify_table_schema`
- Custom logging


## 0.0.1

Initial release.

