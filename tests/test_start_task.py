import pytest
from src.main import Task
from pathlib import Path
from json import load


def test_start_task_when_not_exists(capsys):
    if Path('.tasks.json').exists():
        Path('.tasks.json').unlink()

    new_task = Task()
    new_task.create('test', 'Testing', 'developer')

    with pytest.raises(SystemExit) as err:
        new_task.start('test1')
        captured = capsys.readouterr()
        assert captured.out == "Task not found.\n"
        assert err.value.code == 1


def test_start_task_when_exists():
    if Path('.tasks.json').exists():
        Path('.tasks.json').unlink()

    new_task = Task()
    new_task.create('test', 'Testing', 'developer')
    new_task.start('test')

    tasks = load(open('.tasks.json', 'r'))['tasks']
    task = [ task for task in tasks if task['name'] == 'test' ][0]

    assert 'started_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']





def test_start_task_stoped_with_start_stop_diff_count_ok(capsys):
    pass


def test_start_task_stoped_with_start_stop_diff_count_nok(capsys):
    pass





def test_start_task_without_stop_and_start_count_ok(capsys):
    pass


def test_start_task_without_stop_and_start_count_nok(capsys):
    pass





def test_start_task_finished(capsys):
    pass


def test_start_task_canceled(capsys):
    pass