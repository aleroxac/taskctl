import pytest
from .helpers import setup_test, teardown_test, get_task


def test_finish_task_when_not_exists(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    with pytest.raises(SystemExit) as err:
        new_task.start('test1')
        captured = capsys.readouterr()
        task = get_task()
        assert 'started_at' not in task.keys()
        assert task['started_at'][-1] > task['created_at']
        assert captured.out == "Task not found.\n"
        assert err.value.code == 1

    teardown_test()


def test_finish_task_when_exists(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert captured.out == f"Task \"{task['name']}\" started\n"

    new_task.finish('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert 'finished_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert task['finished_at'] > task['started_at'][-1]
    assert captured.out == f"Task \"{task['name']}\" finished\n"

    teardown_test()


def test_finish_task_unfinished(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert captured.out == f"Task \"{task['name']}\" started\n"

    new_task.finish('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert 'finished_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert task['finished_at'] > task['started_at'][-1]
    assert captured.out == f"Task \"{task['name']}\" finished\n"

    with pytest.raises(SystemExit) as err:
        new_task.finish('test')
        captured = capsys.readouterr()
        task = get_task()

        assert 'started_at' in task.keys()
        assert 'finished_at' in task.keys()
        assert 'stoped_at' not in task.keys()
        assert task['started_at'][-1] > task['created_at']
        assert task['finished_at'] > task['started_at'][-1]
        assert err.value.code == 1
        assert captured.out == \
            "You can't finish a task that already finished\n"

    teardown_test()


def test_finish_task_finished(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert captured.out == f"Task \"{task['name']}\" started\n"

    new_task.finish('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert 'finished_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert task['finished_at'] > task['started_at'][-1]
    assert captured.out == f"Task \"{task['name']}\" finished\n"

    with pytest.raises(SystemExit) as err:
        new_task.finish('test')
        captured = capsys.readouterr()
        task = get_task()

        assert 'started_at' in task.keys()
        assert 'finished_at' in task.keys()
        assert 'stoped_at' not in task.keys()
        assert task['started_at'][-1] > task['created_at']
        assert task['finished_at'] > task['started_at'][-1]
        assert err.value.code == 1
        assert captured.out == \
            "You can't finish a task that already finished\n"

    teardown_test()


def test_finish_task_without_start(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    with pytest.raises(SystemExit) as err:
        new_task.finish('test')
        captured = capsys.readouterr()
        task = get_task()

        assert 'started_at' not in task.keys()
        assert 'finished_at' not in task.keys()
        assert captured.out == \
            "You can't finish a task that hasn't started yet.\n"
        assert err.value.code == 1

    teardown_test()


def test_finish_task_with_start(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert captured.out == f"Task \"{task['name']}\" started\n"

    new_task.finish('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert 'finished_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert task['finished_at'] > task['started_at'][-1]
    assert captured.out == f"Task \"{task['name']}\" finished\n"

    teardown_test()


def test_finish_task_without_stop(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert captured.out == f"Task \"{task['name']}\" started\n"

    new_task.finish('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert 'finished_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert task['finished_at'] > task['started_at'][-1]
    assert captured.out == f"Task \"{task['name']}\" finished\n"

    teardown_test()


def test_finish_task_with_stop(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert captured.out == f"Task \"{task['name']}\" started\n"

    new_task.stop('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'stoped_at' in task.keys()
    assert 'started_at' in task.keys()
    assert task['stoped_at'][-1] > task['created_at']
    assert task['stoped_at'][-1] > task['started_at'][-1]
    assert captured.out == f"Task \"{task['name']}\" stoped\n"

    new_task.finish('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert 'finished_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert task['finished_at'] > task['started_at'][-1]
    assert captured.out == f"Task \"{task['name']}\" finished\n"

    teardown_test()


def test_finish_task_uncanceled(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert captured.out == f"Task \"{task['name']}\" started\n"

    new_task.finish('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert 'finished_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert task['finished_at'] > task['started_at'][-1]
    assert captured.out == f"Task \"{task['name']}\" finished\n"

    teardown_test()


def test_finish_task_canceled(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert captured.out == f"Task \"{task['name']}\" started\n"

    new_task.stop('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'stoped_at' in task.keys()
    assert 'started_at' in task.keys()
    assert task['stoped_at'][-1] > task['created_at']
    assert task['stoped_at'][-1] > task['started_at'][-1]
    assert captured.out == f"Task \"{task['name']}\" stoped\n"

    new_task.finish('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert 'finished_at' in task.keys()
    assert task['started_at'][-1] > task['created_at']
    assert task['finished_at'] > task['started_at'][-1]
    assert captured.out == f"Task \"{task['name']}\" finished\n"

    teardown_test()
