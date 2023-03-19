import pytest
from .helpers import setup_test, teardown_test, get_task


def test_list_task_when_not_exists(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.delete('test')
    captured = capsys.readouterr()

    new_task.list()
    captured = capsys.readouterr()
    assert captured.out == "No tasks found.\n"

    teardown_test()


def test_list_tasks_with_started_items(capsys):
    new_task = setup_test()
    
    new_task.start('test')
    task = get_task()
    assert 'started_at' in task.keys()

    task = new_task.list()[0]
    assert 'id' in task.keys()
    assert 'name' in task.keys()
    assert 'description' in task.keys()
    assert 'owner' in task.keys()
    assert 'created_at' in task.keys()
    assert 'status' in task.keys()
    assert task['status'] == 'doing'

    teardown_test()


def test_list_tasks_with_unstarted_items(capsys):
    new_task = setup_test()

    task = get_task()
    assert 'started_at' not in task.keys()

    task = new_task.list()[0]
    assert 'id' in task.keys()
    assert 'name' in task.keys()
    assert 'description' in task.keys()
    assert 'owner' in task.keys()
    assert 'created_at' in task.keys()
    assert 'status' in task.keys()
    assert task['status'] == 'to-do'

    teardown_test()


def test_list_tasks_with_stoped_items(capsys):
    new_task = setup_test()
    new_task.start('test')
    new_task.stop('test')

    task = get_task()
    assert 'started_at' in task.keys()
    assert 'stoped_at' in task.keys()

    task = new_task.list()[0]
    assert 'id' in task.keys()
    assert 'name' in task.keys()
    assert 'description' in task.keys()
    assert 'owner' in task.keys()
    assert 'created_at' in task.keys()
    assert 'status' in task.keys()
    assert task['status'] == 'stoped'

    teardown_test()


def test_list_tasks_with_canceled_items(capsys):
    new_task = setup_test()
    new_task.start('test')
    new_task.cancel('test')

    task = get_task()
    assert 'started_at' in task.keys()
    assert 'canceled_at' in task.keys()

    task = new_task.list()[0]
    assert 'id' in task.keys()
    assert 'name' in task.keys()
    assert 'description' in task.keys()
    assert 'owner' in task.keys()
    assert 'created_at' in task.keys()
    assert 'status' in task.keys()
    assert task['status'] == 'canceled'

    teardown_test()


def test_list_tasks_with_finished_items(capsys):
    new_task = setup_test()
    new_task.start('test')
    new_task.finish('test')

    task = get_task()
    assert 'started_at' in task.keys()
    assert 'finished_at' in task.keys()

    task = new_task.list()[0]
    assert 'id' in task.keys()
    assert 'name' in task.keys()
    assert 'description' in task.keys()
    assert 'owner' in task.keys()
    assert 'created_at' in task.keys()
    assert 'status' in task.keys()
    assert task['status'] == 'done'

    teardown_test()
