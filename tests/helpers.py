"""Functions to be used by unit-tests Client ."""

from pathlib import Path
from src.app.entities.task import Task
from json import load


def setup_test(clean=True):
    """Set up enviroment for tests."""
    if clean is True:
        teardown_test()

    new_task = Task()
    args = 'test', 'Testing', 'developer'
    new_task.create(args)
    return new_task


def get_task():
    """Get task data."""
    tasks = load(open('.tasks.json', 'r'))['tasks']
    task = [task for task in tasks if task['name'] == 'test'][0]
    return task


def teardown_test():
    """Teardown enviroment for tests."""
    if Path('.tasks.json').exists():
        Path('.tasks.json').unlink()
