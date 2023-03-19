import pytest
from .helpers import setup_test, teardown_test, get_task


def test_delete_task_when_not_exists(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    with pytest.raises(SystemExit) as err:
        new_task.delete('test1')
    captured = capsys.readouterr()
    assert captured.out == "Task not found.\n"
    assert err.value.code == 1

    teardown_test()


def test_delete_task(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()
    task = get_task()

    new_task.delete('test')
    captured = capsys.readouterr()
    assert captured.out == f"Task \"{task['name']}\" deleted.\n"
    with pytest.raises(IndexError) as err:
        task = get_task()
    assert err.type is IndexError

    teardown_test()
