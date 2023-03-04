import pytest
from pathlib import Path
from src.main import Task



def setup_test(capsys):
    if Path('.tasks.json').exists():
        Path('.tasks.json').unlink()

    new_task = Task()
    new_task.create('test', 'Testing', 'developer')
    capsys.readouterr()

    return new_task



def teardown_test():
    if Path('.tasks.json').exists():
        Path('.tasks.json').unlink()
