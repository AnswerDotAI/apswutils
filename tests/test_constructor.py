from apswutils import Database
import apsw
import gc
import pytest
import weakref


def test_recursive_triggers():
    db = Database(memory=True)
    assert db.execute("PRAGMA recursive_triggers").fetchone()[0]


def test_recursive_triggers_off():
    db = Database(memory=True, recursive_triggers=False)
    assert not db.execute("PRAGMA recursive_triggers").fetchone()[0]


# This test is currently disabled since shared mem for sqlite is not recommended,
#   and it requires a special build.
"""
def test_memory_name():
    db1 = Database(memory_name="shared")
    db2 = Database(memory_name="shared")
    db1["dogs"].insert({"name": "Cleo"})
    assert list(db2["dogs"].rows) == [{"name": "Cleo"}]
"""


def test_sqlite_version():
    db = Database(memory=True)
    version = db.sqlite_version
    assert isinstance(version, tuple)
    as_string = ".".join(map(str, version))
    actual = next(db.query("select sqlite_version() as v"))["v"]
    assert actual == as_string


def test_table_cache_does_not_keep_database_alive():
    db = Database(memory=True)
    table = db.table("dogs")
    ref = weakref.ref(db)
    assert table is db.table("dogs")

    del table, db
    gc.collect()
    assert ref() is None


@pytest.mark.parametrize("memory", [True, False])
def test_database_close(tmpdir, memory):
    if memory:
        db = Database(memory=True)
    else:
        db = Database(str(tmpdir / "test.db"))
    assert db.execute("select 1 + 1").fetchone()[0] == 2
    db.close()
    with pytest.raises(apsw.ConnectionClosedError):
        db.execute("select 1 + 1")
