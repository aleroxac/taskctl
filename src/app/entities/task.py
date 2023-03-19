from pathlib import Path
from uuid import uuid4, UUID
from re import match
from json import dump, dumps, load
from datetime import datetime
from sys import exit


class Task():
    """Class with Task entity functions."""

    @classmethod
    def load(cls):
        """Load task datafile content."""
        if Path('.tasks.json').exists():
            tasks = load(open('.tasks.json', 'r'))
            return tasks
        else:
            print("Task data file not found. Create a task and try again.")
            exit(1)

    @classmethod
    def store(cls, task, delete=False):
        """Store a task info task datafile."""
        if Path('.tasks.json').exists():
            tasks = cls.load()
            if delete is True:
                task_data = [
                    t for t in tasks['tasks']
                    if t['id'] == task['id']][0]
                index = tasks['tasks'].index(task_data)
                del tasks['tasks'][index]
            elif task['name'] in [task['name'] for task in tasks['tasks']]:
                task_data = [
                    t for t in tasks['tasks']
                    if t['id'] == task['id']][0]
                index = tasks['tasks'].index(task_data)
                tasks['tasks'][index] = task
            else:
                tasks['tasks'].append(task)

            with open('.tasks.json', 'w+') as task_file:
                dump(tasks, task_file, indent=2)
        else:
            with open('.tasks.json', 'w+') as task_file:
                dump({"tasks": [task]}, task_file, indent=2)

    @classmethod
    def get(cls, task_name):
        """Get task content from task datafile."""
        task_name = cls.check(task_name, 'name')
        tasks = cls.load()['tasks']
        for task in tasks:
            if task['name'] == task_name:
                return task

    @classmethod
    def check(cls, param, type):
        """Check if has passed valid task parameter."""
        if type == 'id':
            isinstance(UUID, param)
            return param
        if type == 'name':
            name_pattern = r'^[a-z][a-z0-9-_]{2,49}$'
            if match(name_pattern, param):
                return param
            else:
                print(
                    f"Parameter '{type}' don't match allowed pattern\
                        ('alphanumeric text, with underscores and hiphens; \
                            max 50 characters').")
                exit(1)
        if type == 'description':
            description_pattern = r'^[a-zA-Z][a-zA-Z0-9-_,. ]{2,99}$'
            if match(description_pattern, param):
                return param
            else:
                print(
                    f"Parameter '{type}' don't match allowed pattern\
                        ('alphanumeric text, with underscores, \
                            spaces and hiphens; max 100 characters').")
                exit(1)
        if type == 'owner':
            username = r'([a-z][a-z0-9-_]{2,29})'
            email_user = r'([a-z0-9.]+)'
            email_single_domain = r'([a-z0-9]+(\.[a-z]+))'
            email_multi_domain = r'(\.[a-z]+\.([a-z]+))'
            email_domain = f'({email_single_domain}|{email_multi_domain})'
            email = f'({email_user}@{email_domain})'
            owner = f'^({username}$|^{email})$'
            if match(owner, param):
                return param
            else:
                print(
                    f"Parameter '{type}' don't match allowed \
                        pattern('username or an email').")
                exit(1)
        else:
            print(f"Please, inform a value to parameter '{param}'")
            exit(1)

    @classmethod
    def validate(cls):
        """Check if task datafile content is valid."""
        if Path('.tasks.json').exists():
            tasks = cls.load()
            if 'tasks' in tasks.keys():
                for task in tasks['tasks']:
                    cls.check(task.id, 'id')
                    cls.check(task.name, 'name')
                    cls.check(task.description, 'description')
                    cls.check(task.owner, 'owner')
                    cls.check(task.created_at, 'created_at')
                    cls.check(task.started_at, 'started_at')
                    cls.check(task.stoped_at, 'stoped_at')
                    cls.check(task.finished_at, 'finished_at')
                    cls.check(task.canceled_at, 'canceled_at')
            else:
                print('Invalid task datafile content.')
                exit(1)
        else:
            print('Task datafile not found.')
            exit(1)

    def describe(self, task_name):
        """Describe a task."""
        task_name = self.check(task_name, 'name')
        task = dumps(self.get(task_name), indent=2)

        if task != 'null':
            print(task)
        else:
            print(f"Task not found.")
            exit(1)

    def create(self, args):
        """Create a task."""
        name = self.check(args[0], 'name')
        description = self.check(args[1], 'description')
        owner = self.check(args[2], 'owner')

        task = {
            'id': str(uuid4()),
            'name': name,
            'description': description,
            'created_at': str(datetime.now()),
            'owner': owner
        }

        if Path('.tasks.json').exists():
            tasks = self.load()['tasks']
            if name in [task['name'] for task in tasks]:
                print("This task already exists.")
                exit(1)
            else:
                self.store(task)
        else:
            self.store(task)

        print(f"Task \"{task['name']}\" created.")

    def start(self, task_name):
        """Start a task."""
        task_name = self.check(task_name, 'name')
        task = self.get(task_name)

        if not task:
            print("Task not found.")
            exit(1)

        if 'started_at' in task.keys():
            if 'stoped_at' in task.keys():
                count_starts = len(task['started_at'])
                count_stops = len(task['stoped_at'])
                if not (count_starts - count_stops) < 1:
                    print("You can't start a task that has already started.")
                    exit(1)
                else:
                    task['started_at'].append(str(datetime.now()))
            elif 'finished_at' in task.keys():
                del task['finished_at']
            elif 'canceled_at' in task.keys():
                del task['canceled_at']
            else:
                count_starts = len(task['started_at'])
                if count_starts == 1:
                    print("You can't start a task that has already started.")
                    exit(1)
                else:
                    task['started_at'].append(str(datetime.now()))
        else:
            task['started_at'] = []
            task['started_at'].append(str(datetime.now()))

        self.store(task)
        print(f"Task \"{task['name']}\" started.")

    def stop(self, task_name):
        """Stop a task."""
        task_name = self.check(task_name, 'name')
        task = self.get(task_name)

        if not task:
            print("Task not found.")
            exit(1)

        if 'started_at' not in task.keys():
            print("You can't stop a task that hasn't started yet.")
            exit(1)
        else:
            if 'stoped_at' in task.keys():
                count_starts = len(task['started_at'])
                count_stops = len(task['stoped_at'])
                if 'finished_at' in task.keys():
                    print("You can't stop a task that has already finished. You need to start it again first.")
                    exit(1)
                elif 'canceled' in task.keys():
                    print(
                        "You can't stop a task that has already canceled.You need to start it again first.")
                    exit(1)
                elif count_stops >= count_starts:
                    print("You can't stop a task that has already stoped.")
                    exit(1)
                else:
                    task['stoped_at'].append(str(datetime.now()))
            else:
                if 'finished_at' in task.keys():
                    print(
                        "You can't stop a task that has already finished. You need to start it again first.")
                    exit(1)
                elif 'canceled_at' in task.keys():
                    print(
                        "You can't stop a task that has already canceled. You need to start it again first.")
                    exit(1)
                else:
                    task['stoped_at'] = []
                    task['stoped_at'].append(str(datetime.now()))

            start_datetime = datetime.strptime(
                task['started_at'][-1], "%Y-%m-%d %H:%M:%S.%f")
            stop_datetime = datetime.strptime(
                task['stoped_at'][-1], "%Y-%m-%d %H:%M:%S.%f")
            if 'duration' in task.keys():
                current_duration = datetime.strptime(
                    task['duration'], "%H:%M:%S.%f")
                task['duration'] = str(
                    (stop_datetime - start_datetime) + current_duration
                ).split(' ')[1]
            else:
                task['duration'] = str(stop_datetime - start_datetime)
        self.store(task)
        print(f"Task \"{task['name']}\" stoped.")

    def finish(self, task_name):
        """Finish a task."""
        task_name = self.check(task_name, 'name')
        task = self.get(task_name)

        if not task:
            print("Task not found.")
            exit(1)

        if 'finished_at' in task.keys():
            print("You can't finish a task that has already finished.")
            exit(1)
        elif 'canceled_at' in task.keys():
            del task['canceled_at']
        elif 'started_at' not in task.keys():
            print("You can't finish a task that hasn't started yet.")
            exit(1)

        task['finished_at'] = str(datetime.now())
        start_datetime = datetime.strptime(
            task['started_at'][0], "%Y-%m-%d %H:%M:%S.%f")
        finish_datetime = datetime.strptime(
            task['finished_at'], "%Y-%m-%d %H:%M:%S.%f")
        task['duration'] = str(finish_datetime - start_datetime)
        self.store(task)
        print(f"Task \"{task['name']}\" finished.")

    def cancel(self, task_name):
        """Cancel a task."""
        task_name = self.check(task_name, 'name')
        task = self.get(task_name)

        if not task:
            print("Task not found.")
            exit(1)

        if 'canceled_at' in task.keys():
            print("You can't cancel a task that has already canceled. You need to start it again first.")
            exit(1)
        elif 'finished_at' in task.keys():
            print("You can't cancel a task that has already finished. You need to start it again first.")
            exit(1)
        elif 'started_at' not in task.keys():
            print("You can't cancel a task that hasn't started yet. You need to start it again first.")
            exit(1)
        else:
            task['canceled_at'] = str(datetime.now())

            start_datetime = datetime.strptime(
                task['started_at'][0], "%Y-%m-%d %H:%M:%S.%f")
            cancel_datetime = datetime.strptime(
                task['canceled_at'], "%Y-%m-%d %H:%M:%S.%f")
            task['duration'] = str(cancel_datetime - start_datetime)
        self.store(task)
        print(f"Task \"{task['name']}\" canceled.")

    def delete(self, task_name):
        """Delete a task."""
        task_name = self.check(task_name, 'name')
        task = self.get(task_name)

        if not task:
            print("Task not found.")
            exit(1)

        self.store(task, delete=True)
        print(f"Task \"{task['name']}\" deleted.")

    def list(self):
        """List all tasks."""
        tasks = self.load()['tasks']

        if len(tasks) == 0:
            print("No tasks found.")
            return
        else:
            items = []
            if len(tasks) > 0:
                for task in tasks:
                    id = task['id']
                    name = task['name']
                    description = task['description']
                    owner = task['owner']
                    created_at = task['created_at']

                    if 'started_at' in task.keys():
                        status = 'doing'
                        count_starts = len(task['started_at'])
                        if 'stoped_at' in task.keys():
                            count_stops = len(task['stoped_at'])
                        else:
                            count_stops = 0
                    else:
                        status = 'to-do'
                        count_stops = 0
                        count_starts = 0

                    if 'stoped_at' in task.keys() and \
                            count_starts == count_stops:
                        status = 'stoped'

                    if 'canceled_at' in task.keys():
                        status = 'canceled'

                    if 'finished_at' in task.keys():
                        status = 'done'

                    item = {
                        "id": id,
                        "name": name,
                        "description": description,
                        "owner": owner,
                        "created_at": created_at,
                        "status": status
                    }
                    items.append(item)
            return items
