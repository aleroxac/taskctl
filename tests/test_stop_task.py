import pytest
from src.main import Task
from pathlib import Path
from json import load
from time import sleep

def test_stop_task_without_start(capsys):
    if Path('.tasks.json').exists():
        Path('.tasks.json').unlink()

    new_task = Task()
    new_task.create('test', 'Testing', 'developer')
    
    sleep(0.1)
    new_task.stop('test')
    out, _ = capsys.readouterr()

    tasks = load(open('.tasks.json', 'r'))['tasks']
    task = [ task for task in tasks if task['name'] == 'test' ][0]

    assert 'stpoed_at' in task.keys()
    assert out == "STDOUT: You can't stop a task that hasn't started yet.\n"


def test_stop_task_with_start():
    if Path('.tasks.json').exists():
        Path('.tasks.json').unlink()

    new_task = Task()
    new_task.create('test', 'Testing', 'developer')
    new_task.start('test')
    new_task.stop('test')

    tasks = load(open('.tasks.json', 'r'))['tasks']
    task = [ task for task in tasks if task['name'] == 'test' ][0]
    assert 'started_at' in task.keys()
    assert 'stoped_at' in task.keys()
    assert task['stoped_at'][-1] > task['created_at']
    assert task['stoped_at'][-1] > task['started_at'][-1]
