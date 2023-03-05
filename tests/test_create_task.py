import pytest
from pathlib import Path
from .helpers import setup_test, teardown_test, get_task


def test_create_task_uncreated(capsys):
    setup_test()
    captured = capsys.readouterr()
    task = get_task()

    assert Path('.tasks.json').exists() is True
    assert captured.out == f"Task \"{task['name']}\" created.\n"
    assert 'id' in task.keys()
    assert 'name' in task.keys()
    assert 'description' in task.keys()
    assert 'created_at' in task.keys()
    assert 'owner' in task.keys()

    teardown_test()


def test_create_task_created(capsys):
    setup_test()
    captured = capsys.readouterr()
    task = get_task()

    assert Path('.tasks.json').exists() is True
    assert captured.out == f"Task \"{task['name']}\" created.\n"
    assert 'id' in task.keys()
    assert 'name' in task.keys()
    assert 'description' in task.keys()
    assert 'created_at' in task.keys()
    assert 'owner' in task.keys()

    with pytest.raises(SystemExit) as err:
        setup_test(clean=False)
        captured = capsys.readouterr()
        assert captured.out == "This task already exists.\n"
        assert err.value.code == 1

    teardown_test()
