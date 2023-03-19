import pytest
from .helpers import setup_test, teardown_test, get_task


def test_cancel_task_when_not_exists(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()

    with pytest.raises(SystemExit) as err:
        new_task.cancel('test1')
    captured = capsys.readouterr()
    assert captured.out == "Task not found.\n"
    assert err.value.code == 1

    teardown_test()


def test_cancel_task_canceled(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()

    new_task.cancel('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert 'canceled_at' in task.keys()
    assert task['canceled_at'] > task['created_at']
    assert task['canceled_at'] > task['started_at'][-1]
    assert captured.out == f"Task \"{task['name']}\" canceled.\n"

    with pytest.raises(SystemExit) as err:
        new_task.cancel('test')
    captured = capsys.readouterr()
    task = get_task()
    assert err.value.code == 1
    assert captured.out == \
        "You can't cancel a task that has already canceled. \
                You need to start it again first.\n"

    teardown_test()


def test_cancel_task_unstarted(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    with pytest.raises(SystemExit) as err:
        new_task.cancel('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' not in task.keys()
    assert 'canceled_at' not in task.keys()
    assert captured.out == "You can't cancel a task that hasn't started yet. \
                You need to start it again first.\n"
    assert err.value.code == 1

    teardown_test()


def test_cancel_task_finished(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()

    new_task.finish('test')
    captured = capsys.readouterr()

    with pytest.raises(SystemExit) as err:
        new_task.cancel('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert 'finished_at' in task.keys()
    assert 'canceled_at' not in task.keys()
    assert err.value.code == 1
    assert captured.out == \
        "You can't cancel a task that has already finished. \
                You need to start it again first.\n"

    teardown_test()


def test_cancel_task(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()

    new_task.cancel('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert 'canceled_at' in task.keys()
    assert task['canceled_at'] > task['created_at']
    assert task['canceled_at'] > task['started_at'][-1]
    assert captured.out == f"Task \"{task['name']}\" canceled.\n"
