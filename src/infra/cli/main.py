"""Command line tool for task management."""
from sys import exit, argv, path
from pathlib import Path
path.append(str(Path(__file__).parent.parent.parent))


def format_task(tasks, format='table', style='plain'):
    if tasks is None:
        return

    if format == 'json':
        from json import dumps
        task_list = dumps(tasks, indent=2)
    elif format == 'yaml':
        from yaml import dump
        task_list = dump(tasks)
    elif format == 'table' or 'wide':
        import tabulate

        available_table_styles = tabulate.tabulate_formats
        if style not in available_table_styles:
            print(f"Invalid table format '{style}'.")
            print(f"\nAvailable table format: \n{available_table_styles}\n")
            exit(1)

        task_cells = []
        for task in tasks:
            if format == 'wide':
                task_cel = [task['id'], task['name'], task['description'],
                            task['created_at'], task['owner'], task['status']]
                task_headers = ['ID', 'NAME', 'DESCRIPTION',
                                'CREATED_AT', 'OWNER', 'STATUS']
            else:
                task_cel = [task['name'], task['owner'], task['status']]
                task_headers = ['NAME', 'OWNER', 'STATUS']

            task_cells.append(task_cel)
            task_list = tabulate.tabulate(
                task_cells,
                task_headers,
                tablefmt=style
            )

    return task_list


def show_task(tasks):
    if tasks != 'null' and tasks is not None:
        print(tasks)


def call_action():
    from app.entities.task import Task

    """Call one of task functions."""
    if argv[1] == 'create':
        task = Task()
        args = argv[2], argv[3], argv[4]
        task.create(args)

    if argv[1] == 'list':
        task = Task()
        tasks = task.list()

        if any(item in argv for item in ['-o', '--output']):
            format_arg_index = [
                argv.index(item)
                for item in argv if item in ['-o', '--output']
            ][0] + 1
            format = argv[format_arg_index]

            if any(item in argv for item in ['-s', '--style']):
                style_arg_index = [
                    argv.index(item)
                    for item in argv if item in ['-s', '--style']
                ][0] + 1
                style = argv[style_arg_index]

                formated_tasks = format_task(tasks, format=format, style=style)
                show_task(formated_tasks)
            else:
                formated_tasks = format_task(tasks, format=format)
                show_task(formated_tasks)
        else:
            formated_tasks = format_task(tasks)
            show_task(formated_tasks)

    if argv[1] == 'describe':
        task = Task()
        args = argv[2:]
        for arg in args:
            task.describe(arg)

    if argv[1] == 'start':
        task = Task()
        args = argv[2:]
        for arg in args:
            task.start(arg)

    if argv[1] == 'stop':
        task = Task()
        args = argv[2:]
        for arg in args:
            task.stop(arg)

    if argv[1] == 'finish':
        task = Task()
        args = argv[2:]
        for arg in args:
            task.finish(arg)

    if argv[1] == 'cancel':
        task = Task()
        args = argv[2:]
        for arg in args:
            task.cancel(arg)

    if argv[1] == 'delete':
        task = Task()
        args = argv[2:]
        for arg in args:
            task.delete(arg)

    if argv[1] == 'help':
        usage()


def check_arguments():
    """Check if has passed valid arguments."""
    args = []
    if len(argv) > 3:
        for arg in argv[2:]:
            if not arg:
                print("Please, informe the task name.")
                exit(1)
        args = argv[2:]
    elif len(argv) > 2:
        args = argv[1]
    return args


def usage():
    """Show usage menu."""
    print("""
    Description: Command line utility to convert envfiles files into json.

    Usage: taskctl [option] [arguments]

    Options:
        create [name] [description] [owner]
            Create a task.
        list
            List tasks.
        describe [name]
            Describe a task.
        start [name]
            Start a task.
        stop [name]
            Stop a task.
        finish [name]
            Finish a task.
        cancel [name]
            Cancel a task.
        delete [name]
            Delete a task.
        help
            Print this help message

    Arguments:
        name
            The task name. Required by all options.
        description
            The task description. Only required by 'create' option.
        owner
            The task owner. Only required by 'create' option.

    Examples:
        taskctl create 'example-task' 'Example Task' 'someone'
        taskctl list
        taskctl describe 'example-task'
        taskctl start 'example-task'
        taskctl stop 'example-task'
        taskctl finish 'example-task'
        taskctl cancel 'example-task'
        taskctl delete 'example-task'
        taskctl help

    More:
        See more about taskctl in: github.com/aleroxac/taskctl
    """)


def check_option():
    """Check if has passed a valid option."""
    options = [
        'create', 'describe', 'start', 'stop',
        'finish', 'cancel', 'delete', 'list'
    ]

    if not len(argv) > 1:
        print('Please, informe an option.')
        usage()
        exit(1)
    else:
        if argv[1] not in options:
            print(f"Option '{argv[1]}' not implemented.")
            exit(1)


def main():
    """Call checks and actions."""
    check_option()
    check_arguments()
    call_action()


if __name__ == "__main__" or __package__ is None:
    main()
