import pytest
from src.main import Task
from pathlib import Path
from json import load
from .helpers import setup_test, teardown_test



def test_start_task_when_not_exists(capsys):
    new_task = setup_test(capsys)

    with pytest.raises(SystemExit) as err:
        new_task.start('test1')
        captured = capsys.readouterr()
        assert captured.out == "Task not found.\n"
        assert err.value.code == 1

    teardown_test()


def test_start_task_when_exists(capsys):
    new_task = setup_test(capsys)

    new_task.start('test')
    captured = capsys.readouterr()

    tasks = load(open('.tasks.json', 'r'))['tasks']
    task = [ task for task in tasks if task['name'] == 'test' ][0]

    assert captured.out == f"Task \"{task['name']}\" started\n"
    assert 'started_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']

    teardown_test()



def test_start_task_stoped_with_start_stop_diff_count_ok(capsys):
    new_task = setup_test(capsys)

    new_task.start('test')
    captured = capsys.readouterr()
    tasks = load(open('.tasks.json', 'r'))['tasks']
    task = [ task for task in tasks if task['name'] == 'test' ][0]
    assert 'started_at' in task.keys()
    assert captured.out == f"Task \"{task['name']}\" started\n"
    assert task['started_at'][-1] > task['created_at']

    new_task.stop('test')
    captured = capsys.readouterr()
    tasks = load(open('.tasks.json', 'r'))['tasks']
    task = [ task for task in tasks if task['name'] == 'test' ][0]
    assert 'stoped_at' in task.keys()
    assert captured.out == f"Task \"{task['name']}\" stoped\n"
    assert task['stoped_at'][-1] > task['started_at'][-1]

    new_task.start('test')
    captured = capsys.readouterr()
    tasks = load(open('.tasks.json', 'r'))['tasks']
    task = [ task for task in tasks if task['name'] == 'test' ][0]
    assert 'started_at' in task.keys()
    assert captured.out == f"Task \"{task['name']}\" started\n"
    assert task['started_at'][-1] > task['stoped_at'][-1]

    teardown_test()


def test_start_task_stoped_with_start_stop_diff_count_nok(capsys):
    new_task = setup_test(capsys)

    new_task.start('test')
    captured = capsys.readouterr()
    tasks = load(open('.tasks.json', 'r'))['tasks']
    task = [ task for task in tasks if task['name'] == 'test' ][0]
    assert 'started_at' in task.keys()
    assert captured.out == f"Task \"{task['name']}\" started\n"
    assert task['started_at'][-1] > task['created_at']

    new_task.stop('test')
    captured = capsys.readouterr()
    tasks = load(open('.tasks.json', 'r'))['tasks']
    task = [ task for task in tasks if task['name'] == 'test' ][0]
    assert 'stoped_at' in task.keys()
    assert captured.out == f"Task \"{task['name']}\" stoped\n"
    assert task['stoped_at'][-1] > task['started_at'][-1]

    new_task.start('test')
    captured = capsys.readouterr()
    tasks = load(open('.tasks.json', 'r'))['tasks']
    task = [ task for task in tasks if task['name'] == 'test' ][0]
    assert 'started_at' in task.keys()
    assert captured.out == f"Task \"{task['name']}\" started\n"
    assert task['started_at'][-1] > task['stoped_at'][-1]

    with pytest.raises(SystemExit) as err:
        new_task.start('test')
        captured = capsys.readouterr()
        tasks = load(open('.tasks.json', 'r'))['tasks']
        task = [ task for task in tasks if task['name'] == 'test' ][0]
        assert 'started_at' in task.keys()
        assert err.value.code == 1
        assert captured.out == "You can't start a task that has already started.\n"

    teardown_test()





# def test_start_task_without_stop_and_start_count_ok(capsys):
#     pass


# def test_start_task_without_stop_and_start_count_nok(capsys):
#     pass





# def test_start_task_finished(capsys):
#     pass


# def test_start_task_canceled(capsys):
#     pass