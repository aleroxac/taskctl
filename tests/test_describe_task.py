import pytest
from .helpers import setup_test, teardown_test, get_task


def test_describe_task_when_not_exists(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    with pytest.raises(SystemExit) as err:
        new_task.describe('test1')
    captured = capsys.readouterr()
    assert captured.out == "Task not found.\n"
    assert err.value.code == 1

    teardown_test()


def test_describe_task(capsys):
    new_task = setup_test()

    task = get_task()
    new_task.describe('test')
    assert 'id' in task.keys()
    assert 'name' in task.keys()
    assert 'description' in task.keys()
    assert 'created_at' in task.keys()
    assert 'owner' in task.keys()

    teardown_test()
