import pytest
from src.main import Task
from pathlib import Path
from json import load


def test_create_task_from_scratch(capsys):
    if Path('.tasks.json').exists():
        Path('.tasks.json').unlink()

    new_task = Task()
    new_task.create('test', 'Testing', 'developer')
    captured = capsys.readouterr()

    tasks = load(open('.tasks.json', 'r'))['tasks']
    task = [ task for task in tasks if task['name'] == 'test' ][0]

    assert Path('.tasks.json').exists() is True
    assert captured.out == f"Task \"{task['name']}\" created\n"
    assert 'id' in task.keys()
    assert 'name' in task.keys()
    assert 'description' in task.keys()
    assert 'created_at' in task.keys()
    assert 'owner' in task.keys()


def test_create_an_already_created_task(capsys):
    if Path('.tasks.json').exists():
        Path('.tasks.json').unlink()

    new_task = Task()

    new_task.create('test', 'Testing', 'developer')
    captured = capsys.readouterr()
    tasks = load(open('.tasks.json', 'r'))['tasks']
    task = [ task for task in tasks if task['name'] == 'test' ][0]
    assert Path('.tasks.json').exists() is True
    assert captured.out == f"Task \"{task['name']}\" created\n"
    assert 'id' in task.keys()
    assert 'name' in task.keys()
    assert 'description' in task.keys()
    assert 'created_at' in task.keys()
    assert 'owner' in task.keys()

    with pytest.raises(SystemExit) as err:
        new_task.create('test', 'Testing', 'developer')
        captured = capsys.readouterr()
        assert err.value.code == 1
        assert captured.out == "This task already exists\n"