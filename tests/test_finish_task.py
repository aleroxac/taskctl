import pytest
from src.main import Task
from time import sleep


def test_finish_task_already_finished():
    new_task = Task('first task', 'My fist task', 'acardoso')
    task = new_task.create()
    sleep(0.1)
    task = new_task.start()
    sleep(0.1)
    task = new_task.finish()

    with pytest.raises(Exception) as err:
        sleep(0.1)
        task = new_task.finish()
        assert 'started_at' in task.keys()
    assert str(err.value) == "You can't finish a task that already finished."


def test_finish_task_without_start():
    new_task = Task('first task', 'My fist task', 'acardoso')
    task = new_task.create()

    with pytest.raises(Exception) as err:
        sleep(0.1)
        task = new_task.finish()
        assert 'started_at' in task.keys()
    assert str(err.value) == "You can't finish a task that hasn't started yet."


def test_finish_task_with_start():
    new_task = Task('first task', 'My fist task', 'acardoso')
    task = new_task.create()
    sleep(0.1)
    task = new_task.start()
    sleep(0.1)
    task = new_task.finish()
    sleep(0.1)

    assert 'started_at' in task.keys()
    assert 'finished_at' in task.keys()
    assert task['finished_at'] > task['started_at'][-1]


def test_finish_task_without_stop():
    new_task = Task('first task', 'My fist task', 'acardoso')
    task = new_task.create()
    sleep(0.1)
    task = new_task.start()
    sleep(0.1)
    task = new_task.finish()

    assert 'started_at' in task.keys()
    assert 'finished_at' in task.keys()

    assert task['finished_at'] > task['started_at'][-1]


def test_finish_task_with_stop():
    new_task = Task('first task', 'My fist task', 'acardoso')
    task = new_task.create()
    sleep(0.1)
    task = new_task.start()
    sleep(0.1)
    task = new_task.stop()
    sleep(0.1)
    task = new_task.finish()

    assert 'started_at' in task.keys()
    assert 'finished_at' in task.keys()

    assert task['finished_at'] > task['started_at'][-1]
