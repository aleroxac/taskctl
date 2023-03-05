import pytest
from .helpers import setup_test, teardown_test, get_task


def test_start_task_when_not_exists(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    with pytest.raises(SystemExit) as err:
        new_task.start('test1')
        captured = capsys.readouterr()
        task = get_task()
        assert 'started_at' not in task.keys()
        assert captured.out == "Task not found.\n"
        assert err.value.code == 1

    teardown_test()


def test_start_task_when_exists(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert captured.out == f"Task \"{task['name']}\" started\n"
    assert task['started_at'][-1] > task['created_at']

    teardown_test()


def test_start_task_unstarted(capsys):
    teardown_test()
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert captured.out == f"Task \"{task['name']}\" started\n"
    assert task['started_at'][-1] > task['created_at']

    teardown_test()


def test_start_task_started(capsys):
    teardown_test()
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert captured.out == f"Task \"{task['name']}\" started\n"
    assert task['started_at'][-1] > task['created_at']

    with pytest.raises(SystemExit) as err:
        new_task.start('test')
        captured = capsys.readouterr()
        task = get_task()
        assert 'started_at' in task.keys()
        assert err.value.code == 1
        assert captured.out == \
            "You can't start a task that has already started.\n"

    teardown_test()


def test_start_task_stoped_with_diff_start_count_ok(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert captured.out == f"Task \"{task['name']}\" started\n"
    assert task['started_at'][-1] > task['created_at']

    new_task.stop('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'stoped_at' in task.keys()
    assert captured.out == f"Task \"{task['name']}\" stoped\n"
    assert task['stoped_at'][-1] > task['started_at'][-1]

    new_task.start('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert captured.out == f"Task \"{task['name']}\" started\n"
    assert task['started_at'][-1] > task['stoped_at'][-1]

    teardown_test()


def test_start_task_stoped_with_diff_start_count_nok(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert captured.out == f"Task \"{task['name']}\" started\n"
    assert task['started_at'][-1] > task['created_at']

    new_task.stop('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'stoped_at' in task.keys()
    assert captured.out == f"Task \"{task['name']}\" stoped\n"
    assert task['stoped_at'][-1] > task['started_at'][-1]

    new_task.start('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert captured.out == f"Task \"{task['name']}\" started\n"
    assert task['started_at'][-1] > task['stoped_at'][-1]

    with pytest.raises(SystemExit) as err:
        new_task.start('test')
        captured = capsys.readouterr()
        task = get_task()
        assert 'started_at' in task.keys()
        assert err.value.code == 1
        assert captured.out == \
            "You can't start a task that has already started.\n"

    teardown_test()


def test_start_task_unstoped_and_start_count_ok(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert captured.out == f"Task \"{task['name']}\" started\n"
    assert task['started_at'][-1] > task['created_at']

    teardown_test()


def test_start_task_stoped_and_start_count_nok(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert captured.out == f"Task \"{task['name']}\" started\n"
    assert task['started_at'][-1] > task['created_at']

    with pytest.raises(SystemExit) as err:
        new_task.start('test')
        captured = capsys.readouterr()
        task = get_task()
        assert 'started_at' in task.keys()
        assert err.value.code == 1
        assert captured.out == \
            "You can't start a task that has already started.\n"

    teardown_test()


def test_start_task_finished(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert captured.out == f"Task \"{task['name']}\" started\n"
    assert task['started_at'][-1] > task['created_at']

    new_task.finish('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'finished_at' in task.keys()
    assert captured.out == f"Task \"{task['name']}\" finished\n"
    assert task['finished_at'] > task['started_at'][-1]

    new_task.start('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert 'finished_at' not in task.keys()

    teardown_test()


def test_start_task_canceled(capsys):
    new_task = setup_test()
    captured = capsys.readouterr()

    new_task.start('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert captured.out == f"Task \"{task['name']}\" started\n"
    assert task['started_at'][-1] > task['created_at']

    new_task.cancel('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert 'canceled_at' in task.keys()
    assert captured.out == f"Task \"{task['name']}\" canceled\n"
    assert task['canceled_at'] > task['started_at'][-1]

    new_task.start('test')
    captured = capsys.readouterr()
    task = get_task()
    assert 'started_at' in task.keys()
    assert 'canceled_at' not in task.keys()

    teardown_test()
