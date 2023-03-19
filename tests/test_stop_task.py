import pytest
from .helpers import setup_test, teardown_test, get_task


def test_stop_task_when_not_exists(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()

    with pytest.raises(SystemExit) as err:
        new_task.stop('test1')
    task = get_task()
    captured = capsys.readouterr()
    assert 'started_at' in task.keys()
    assert 'stoped_at' not in task.keys()
    assert captured.out == "Task not found.\n"
    assert err.value.code == 1

    teardown_test()


def test_stop_task_unstarted(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    with pytest.raises(SystemExit) as err:
        new_task.stop('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' not in task.keys()
    assert 'stoped_at' not in task.keys()
    assert captured.out == \
        "You can't stop a task that hasn't started yet.\n"
    assert err.value.code == 1

    teardown_test()


def test_stop_task_stoped(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()

    new_task.stop('test')
    captured = capsys.readouterr()

    with pytest.raises(SystemExit) as err:
        new_task.stop('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'stoped_at' in task.keys()
    assert captured.out == \
        "You can't stop a task that has already stoped.\n"
    assert err.value.code == 1

    teardown_test()


def test_stop_task_finished(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()

    new_task.finish('test')
    captured = capsys.readouterr()

    with pytest.raises(SystemExit) as err:
        new_task.stop('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert 'finished_at' in task.keys()
    assert 'stoped_at' not in task.keys()
    assert err.value.code == 1
    assert captured.out == "You can't stop a task that has already finished. \
                            You need to start it again first.\n"

    teardown_test()


def test_stop_task_canceled(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()

    new_task.cancel('test')
    captured = capsys.readouterr()

    with pytest.raises(SystemExit) as err:
        new_task.stop('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert 'canceled_at' in task.keys()
    assert 'stoped_at' not in task.keys()
    assert err.value.code == 1
    assert captured.out == "You can't stop a task that has already canceled. \
                            You need to start it again first.\n"

    teardown_test()


def test_stop_task(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()

    new_task.stop('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert 'stoped_at' in task.keys()
    assert task['stoped_at'][-1] > task['created_at']
    assert task['stoped_at'][-1] > task['started_at'][-1]
    assert captured.out == f"Task \"{task['name']}\" stoped.\n"

    teardown_test()
