import pytest
from .helpers import setup_test, teardown_test, get_task


def test_start_task_when_not_exists(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    with pytest.raises(SystemExit) as err:
        new_task.start('test1')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' not in task.keys()
    assert captured.out == "Task not found.\n"
    assert err.value.code == 1

    teardown_test()


def test_start_task_started(capsys):
    teardown_test()
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()

    with pytest.raises(SystemExit) as err:
        new_task.start('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert err.value.code == 1
    assert captured.out == "You can't start a task that has already started.\n"

    teardown_test()


def test_start_task_stoped(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()

    new_task.stop('test')
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert captured.out == f"Task \"{task['name']}\" started.\n"

    teardown_test()


def test_start_task_finished(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()

    new_task.finish('test')
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert 'finished_at' not in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert captured.out == f"Task \"{task['name']}\" started.\n"

    teardown_test()


def test_start_task_canceled(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()

    new_task.cancel('test')
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert 'canceled_at' not in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert captured.out == f"Task \"{task['name']}\" started.\n"

    teardown_test()


def test_start_task(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert captured.out == f"Task \"{task['name']}\" started.\n"

    teardown_test()
