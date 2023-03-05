import pytest
from json import load
from .helpers import setup_test, teardown_test



def test_stop_task_when_not_exists(capsys):
    new_task = setup_test(capsys)

    new_task.start('test')
    captured = capsys.readouterr()
    tasks = load(open('.tasks.json', 'r'))['tasks']
    task = [ task for task in tasks if task['name'] == 'test' ][0]
    assert 'started_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert captured.out == f"Task \"{task['name']}\" started\n"

    with pytest.raises(SystemExit) as err:
        new_task.stop('test1')
        captured = capsys.readouterr()
        assert 'started_at' in task.keys()
        assert not 'stoped_at' in task.keys()
        assert captured.out == "Task not found.\n"
        assert err.value.code == 1

    teardown_test()

def test_stop_task_when_exists(capsys):
    new_task = setup_test(capsys)

    new_task.start('test')
    captured = capsys.readouterr()
    tasks = load(open('.tasks.json', 'r'))['tasks']
    task = [ task for task in tasks if task['name'] == 'test' ][0]
    assert 'started_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert captured.out == f"Task \"{task['name']}\" started\n"

    new_task.stop('test')
    captured = capsys.readouterr()
    tasks = load(open('.tasks.json', 'r'))['tasks']
    task = [ task for task in tasks if task['name'] == 'test' ][0]
    assert 'started_at' in task.keys()
    assert 'stoped_at' in task.keys()
    assert task['stoped_at'][-1] > task['created_at']
    assert task['stoped_at'][-1] > task['started_at'][-1]
    assert captured.out == f"Task \"{task['name']}\" stoped\n"

    teardown_test()



def test_stop_task_without_start(capsys):
    new_task = setup_test(capsys)

    with pytest.raises(SystemExit) as err:
        new_task.stop('test')
        captured = capsys.readouterr()
        tasks = load(open('.tasks.json', 'r'))['tasks']
        task = [ task for task in tasks if task['name'] == 'test' ][0]
        assert 'started_at' in task.keys()
        assert not 'stoped_at' in task.keys()
        assert task['started_at'][-1] > task['created_at']
        assert captured.out == "You can't stop a task that hasn't started yet.\n"
        assert err.value.code == 1
    
    teardown_test()

def test_stop_task_with_start(capsys):
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
    assert 'started_at' in task.keys()
    assert 'stoped_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert task['stoped_at'][-1] > task['started_at'][-1]
    assert captured.out == f"Task \"{task['name']}\" stoped\n"

    teardown_test()



def test_stop_task_unstoped(capsys):
    new_task = setup_test(capsys)

    new_task.start('test')
    captured = capsys.readouterr()
    tasks = load(open('.tasks.json', 'r'))['tasks']
    task = [ task for task in tasks if task['name'] == 'test' ][0]
    assert 'started_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert captured.out == f"Task \"{task['name']}\" started\n"

    new_task.stop('test')
    captured = capsys.readouterr()
    tasks = load(open('.tasks.json', 'r'))['tasks']
    task = [ task for task in tasks if task['name'] == 'test' ][0]
    assert 'started_at' in task.keys()
    assert 'stoped_at' in task.keys()
    assert captured.out == f"Task \"{task['name']}\" stoped\n"
    assert task['started_at'][-1] > task['created_at']
    assert task['stoped_at'][-1] > task['started_at'][-1]

    teardown_test()

def test_stop_task_stoped(capsys):
    new_task = setup_test(capsys)

    new_task.start('test')
    captured = capsys.readouterr()
    tasks = load(open('.tasks.json', 'r'))['tasks']
    task = [ task for task in tasks if task['name'] == 'test' ][0]
    assert 'started_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert captured.out == f"Task \"{task['name']}\" started\n"

    new_task.stop('test')
    captured = capsys.readouterr()
    tasks = load(open('.tasks.json', 'r'))['tasks']
    task = [ task for task in tasks if task['name'] == 'test' ][0]
    assert 'started_at' in task.keys()
    assert 'stoped_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert task['stoped_at'][-1] > task['started_at'][-1]
    assert captured.out == f"Task \"{task['name']}\" stoped\n"

    with pytest.raises(SystemExit) as err:
        new_task.stop('test')
        captured = capsys.readouterr()
        tasks = load(open('.tasks.json', 'r'))['tasks']
        task = [ task for task in tasks if task['name'] == 'test' ][0]
        assert 'started_at' in task.keys()
        assert 'stoped_at' in task.keys()
        assert task['started_at'][-1] > task['created_at']
        assert task['stoped_at'][-1] > task['started_at'][-1]
        assert captured.out == "You can't stop a task that has already stoped.\n"
        assert err.value.code == 1

    teardown_test()



def test_stop_task_finished_with_stop(capsys):
    new_task = setup_test(capsys)

    new_task.start('test')
    captured = capsys.readouterr()
    tasks = load(open('.tasks.json', 'r'))['tasks']
    task = [ task for task in tasks if task['name'] == 'test' ][0]
    assert 'started_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert captured.out == f"Task \"{task['name']}\" started\n"

    new_task.stop('test')
    captured = capsys.readouterr()
    tasks = load(open('.tasks.json', 'r'))['tasks']
    task = [ task for task in tasks if task['name'] == 'test' ][0]
    assert 'started_at' in task.keys()
    assert 'stoped_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert task['stoped_at'][-1] > task['started_at'][-1]
    assert captured.out == f"Task \"{task['name']}\" stoped\n"

    new_task.finish('test')
    captured = capsys.readouterr()
    tasks = load(open('.tasks.json', 'r'))['tasks']
    task = [ task for task in tasks if task['name'] == 'test' ][0]
    assert 'started_at' in task.keys()
    assert 'finished_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert task['finished_at'] > task['started_at'][-1]
    assert task['finished_at'] > task['stoped_at'][-1]
    assert captured.out == f"Task \"{task['name']}\" finished\n"

    with pytest.raises(SystemExit) as err:
        new_task.stop('test')
        captured = capsys.readouterr()
        tasks = load(open('.tasks.json', 'r'))['tasks']
        task = [ task for task in tasks if task['name'] == 'test' ][0]

        assert 'started_at' in task.keys()
        assert 'finished_at' in task.keys()
        assert 'stoped_at' in task.keys()
        assert task['started_at'][-1] > task['created_at']
        assert task['finished_at'] > task['started_at'][-1]
        assert task['finished_at'] > task['stoped_at'][-1]
        assert err.value.code == 1
        assert captured.out == "You can't stop a task that has already finished. You need to start it again first.\n"

    teardown_test()

def test_stop_task_finished_without_stop(capsys):
    new_task = setup_test(capsys)

    new_task.start('test')
    captured = capsys.readouterr()
    tasks = load(open('.tasks.json', 'r'))['tasks']
    task = [ task for task in tasks if task['name'] == 'test' ][0]
    assert 'started_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert captured.out == f"Task \"{task['name']}\" started\n"

    new_task.finish('test')
    captured = capsys.readouterr()
    tasks = load(open('.tasks.json', 'r'))['tasks']
    task = [ task for task in tasks if task['name'] == 'test' ][0]
    assert 'started_at' in task.keys()
    assert 'finished_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert task['finished_at'] > task['started_at'][-1]
    assert captured.out == f"Task \"{task['name']}\" finished\n"

    with pytest.raises(SystemExit) as err:
        new_task.stop('test')
        captured = capsys.readouterr()
        tasks = load(open('.tasks.json', 'r'))['tasks']
        task = [ task for task in tasks if task['name'] == 'test' ][0]

        assert 'started_at' in task.keys()
        assert 'finished_at' in task.keys()
        assert not 'stoped_at' in task.keys()
        assert task['started_at'][-1] > task['created_at']
        assert task['finished_at'] > task['started_at'][-1]
        assert err.value.code == 1
        assert captured.out == "You can't stop a task that has already finished. You need to start it again first.\n"

    teardown_test()



def test_stop_task_canceled_with_stop(capsys):
    new_task = setup_test(capsys)

    new_task.start('test')
    captured = capsys.readouterr()
    tasks = load(open('.tasks.json', 'r'))['tasks']
    task = [ task for task in tasks if task['name'] == 'test' ][0]
    assert 'started_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert captured.out == f"Task \"{task['name']}\" started\n"

    new_task.stop('test')
    captured = capsys.readouterr()
    tasks = load(open('.tasks.json', 'r'))['tasks']
    task = [ task for task in tasks if task['name'] == 'test' ][0]
    assert 'started_at' in task.keys()
    assert 'stoped_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert task['stoped_at'][-1] > task['started_at'][-1]
    assert captured.out == f"Task \"{task['name']}\" stoped\n"

    new_task.cancel('test')
    captured = capsys.readouterr()
    tasks = load(open('.tasks.json', 'r'))['tasks']
    task = [ task for task in tasks if task['name'] == 'test' ][0]
    assert 'started_at' in task.keys()
    assert 'canceled_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert task['stoped_at'][-1] > task['started_at'][-1]
    assert task['canceled_at'] > task['started_at'][-1]
    assert task['canceled_at'] > task['stoped_at'][-1]
    assert captured.out == f"Task \"{task['name']}\" canceled\n"

    with pytest.raises(SystemExit) as err:
        new_task.stop('test')
        captured = capsys.readouterr()
        tasks = load(open('.tasks.json', 'r'))['tasks']
        task = [ task for task in tasks if task['name'] == 'test' ][0]

        assert 'started_at' in task.keys()
        assert 'canceled_at' in task.keys()
        assert 'stoped_at' in task.keys()
        assert task['started_at'][-1] > task['created_at']
        assert task['canceled_at'] > task['started_at'][-1]
        assert task['canceled_at'] > task['stoped_at'][-1]
        assert err.value.code == 1
        assert captured.out == "You can't stop a task that has already canceled. You need to start it again first.\n"

    teardown_test()

def test_stop_task_canceled_without_stop(capsys):
    new_task = setup_test(capsys)

    new_task.start('test')
    captured = capsys.readouterr()
    tasks = load(open('.tasks.json', 'r'))['tasks']
    task = [ task for task in tasks if task['name'] == 'test' ][0]
    assert 'started_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert captured.out == f"Task \"{task['name']}\" started\n"

    new_task.cancel('test')
    captured = capsys.readouterr()
    tasks = load(open('.tasks.json', 'r'))['tasks']
    task = [ task for task in tasks if task['name'] == 'test' ][0]
    assert 'started_at' in task.keys()
    assert 'canceled_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert task['canceled_at'] > task['started_at'][-1]
    assert captured.out == f"Task \"{task['name']}\" canceled\n"

    with pytest.raises(SystemExit) as err:
        new_task.stop('test')
        captured = capsys.readouterr()
        tasks = load(open('.tasks.json', 'r'))['tasks']
        task = [ task for task in tasks if task['name'] == 'test' ][0]

        assert 'started_at' in task.keys()
        assert 'canceled_at' in task.keys()
        assert not 'stoped_at' in task.keys()
        assert task['started_at'][-1] > task['created_at']
        assert task['canceled_at'] > task['started_at'][-1]
        assert err.value.code == 1
        assert captured.out == "You can't stop a task that has already canceled. You need to start it again first.\n"

    teardown_test()
