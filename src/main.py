from uuid import uuid4, UUID
from datetime import datetime
from sys import argv, exit
from json import dump, dumps, load
from pathlib import Path
from re import match


class Task():
    @classmethod
    def load(self):
        if Path('.tasks.json').exists():
            tasks = load(open('.tasks.json', 'r'))
        else:
            print("Task data file not found. Create a task and try again.")
            exit(1)
        return tasks


    @classmethod
    def store(self, task, delete=False):
        if Path('.tasks.json').exists():
            tasks = self.load()
            if delete is True:
                task_data = [ t for t in tasks['tasks'] if t['id'] == task['id'] ][0]
                index = tasks['tasks'].index(task_data)
                del tasks['tasks'][index]
            elif task['name'] in [ task['name'] for task in tasks['tasks'] ]:
                task_data = [ t for t in tasks['tasks'] if t['id'] == task['id'] ][0]
                index = tasks['tasks'].index(task_data)
                tasks['tasks'][index] = task
            else:
                tasks['tasks'].append(task)

            with open('.tasks.json', 'w+') as task_file:
                dump(tasks, task_file, indent=2)
        else:
            with open('.tasks.json', 'w+') as task_file:
                dump({"tasks":[task]}, task_file, indent=2)


    @classmethod
    def get(self, task_name):
        task_name = self.check(task_name, 'name')
        tasks = self.load()['tasks']
        for task in tasks:
            if task['name'] == task_name:
                return task


    @classmethod
    def check(self, param, type):
        if type == 'id':
            isinstance(UUID, param)
            return param
        if type == 'name':
            name_pattern = r'^[a-z][a-z0-9-_]{2,49}$'
            if match(name_pattern, param):
                return param
            else:
                print(f"Parameter '{type}' don't  match allowed pattern('alphanumeric text, with underscores and hiphens; max 50 characters').")
                exit(1)
        if type == 'description':
            description_pattern = r'^[a-zA-Z][a-zA-Z0-9-_,. ]{2,99}$'
            if match(description_pattern, param):
                return param
            else:
                print(f"Parameter '{type}' don't  match allowed pattern('alphanumeric text, with underscores, spaces and hiphens; max 100 characters').")
                exit(1)
        if type == 'owner':
            owner_pattern = r'^([a-z][a-z0-9-_]{2,29}$)|(^[a-z0-9.]+@[a-z0-9]+((\.[a-z]+)|(\.[a-z]+\.([a-z]+))))$'
            if match(owner_pattern, param):
                return param
            else:
                print(f"Parameter '{type}' don't  match allowed pattern('username or an email').")
                exit(1)
        else:
            print(f"Please, inform a value to parameter '{param}'")
            exit(1)


    def describe(self, task_name):
        task_name = self.check(task_name, 'name')
        task = dumps(self.get(task_name), indent=2)

        if task != 'null':
            print(task)
        else:
            print(f"Task '{task_name}' not found.")
            exit(1)


    def create(self, name, description, owner):
        name = self.check(name, 'name')
        description = self.check(description, 'description')
        owner = self.check(owner, 'owner')

        task = {
            'id': str(uuid4()),
            'name': name,
            'description': description,
            'created_at': str(datetime.now()),
            'owner': owner
        }

        if Path('.tasks.json').exists():
            tasks = self.load()['tasks']
            if name in [ task['name'] for task in tasks ]:
                print("This task already exists")
                exit(1)
            self.store(task)
        else:
            self.store(task)

        print(f"Task \"{task['name']}\" created")


    def start(self, task_name):
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
        print(f"Task \"{task['name']}\" started")


    def stop(self, task_name):
        task_name = self.check(task_name, 'name')
        task = self.get(task_name)

        if not task:
            print("Task not found.")
            exit(1)

        if not 'started_at' in task.keys():
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
                    print("You can't stop a task that has already canceled. You need to start it again first.")
                    exit(1)
                elif count_stops >= count_starts:
                    print("You can't stop a task that has already stoped.")
                    exit(1)
                else:
                    task['stoped_at'].append(str(datetime.now()))
            else:
                if 'finished_at' in task.keys():
                    print("You can't stop a task that has already finished. You need to start it again first.")
                    exit(1)
                elif 'canceled_at' in task.keys():
                    print("You can't stop a task that has already canceled. You need to start it again first.")
                    exit(1)
                else:
                    task['stoped_at'] = []
                    task['stoped_at'].append(str(datetime.now()))

            start_datetime = datetime.strptime(task['started_at'][-1], "%Y-%m-%d %H:%M:%S.%f")
            stop_datetime = datetime.strptime(task['stoped_at'][-1], "%Y-%m-%d %H:%M:%S.%f")
            if 'duration' in task.keys():
                current_duration = datetime.strptime(task['duration'], "%H:%M:%S.%f")
                task['duration'] = str((stop_datetime - start_datetime) + current_duration).split(' ')[1]
            else:
                task['duration'] = str(stop_datetime - start_datetime)
        self.store(task)
        print(f"Task \"{task['name']}\" stoped")


    def finish(self, task_name):
        task_name = self.check(task_name, 'name')
        task = self.get(task_name)

        if not task:
            print("Task not found.")
            exit(1)

        if 'finished_at' in task.keys():
            print("You can't finish a task that has already finished.")
            exit(1)
        elif not 'started_at' in task.keys():
            print("You can't finish a task that hasn't started yet.")
            exit(1)
        else:
            task['finished_at'] = str(datetime.now())

            start_datetime = datetime.strptime(task['started_at'][0], "%Y-%m-%d %H:%M:%S.%f")
            finish_datetime = datetime.strptime(task['finished_at'], "%Y-%m-%d %H:%M:%S.%f")
            task['duration'] = str(finish_datetime - start_datetime)
        self.store(task)
        print(f"Task \"{task['name']}\" finished")


    def cancel(self, task_name):
        task_name = self.check(task_name, 'name')
        task = self.get(task_name)

        if not task:
            print("Task not found.")
            exit(1)

        if 'canceled_at' in task.keys():
            print("You can't cancel a task that has already canceled.")
            exit(1)
        elif not 'started_at' in task.keys():
            print("You can't cancel a task that hasn't started yet.")
            exit(1)
        # elif not 'finished_at' in task.keys():
        #     print("You can't cancel a task that has finished.")
        #     exit(1)
        else:
            task['canceled_at'] = str(datetime.now())

            start_datetime = datetime.strptime(task['started_at'][0], "%Y-%m-%d %H:%M:%S.%f")
            cancel_datetime = datetime.strptime(task['canceled_at'], "%Y-%m-%d %H:%M:%S.%f")
            task['duration'] = str(cancel_datetime - start_datetime)
        self.store(task)
        print(f"Task \"{task['name']}\" canceled")


    def delete(self, task_name):
        task_name = self.check(task_name, 'name')
        task = self.get(task_name)

        if not task:
            print("Task not found.")
            exit(1)

        self.store(task, delete=True)
        print(f"Task \"{task['name']}\" deleted")


    def list(self):
        tasks = self.load()['tasks']
        if len(tasks) < 1:
            print("No tasks found.")
        else:
            print("id\tname\tdescription\towner\t\tcreated_at\t\t\tstatus")
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

                if 'stoped_at' in task.keys() and count_starts == count_stops:
                    status = 'stoped'

                if 'canceled_at' in task.keys():
                    status = 'canceled'
                
                if 'finished_at' in task.keys():
                    status = 'done'


                print(f"{id}\t{name}\t{description}\t\t{owner}\t{created_at}\t{status}")


if __name__ == "__main__":
    options = ['create', 'describe', 'start', 'stop', 'finish', 'cancel', 'delete', 'list']
    options_with_no_args = ['list']

    if len(argv) > 1:
        if argv[1] not in options:
            print(f"Option '{argv[1]}' not implemented.")
            exit(1)

        if len(argv) >= 3:
            if argv[1] == 'create':
                name = argv[2]

                if argv[3]:
                    description = argv[3]
                else:
                    print("Please, inform task description.")
                    exit(1)

                if argv[4]:
                    owner = argv[4]
                else:
                    print("Please, inform task owner.")

                task = Task()
                task.create(name, description, owner)

            if argv[1] == 'describe':
                name = argv[2]
                task = Task()
                task.describe(name)

            elif argv[1] == 'start':
                name = argv[2]
                task = Task()
                task.start(name)

            elif argv[1] == 'stop':
                name = argv[2]
                task = Task()
                task.stop(name)

            elif argv[1] == 'finish':
                name = argv[2]
                task = Task()
                task.finish(name)

            elif argv[1] == 'cancel':
                name = argv[2]
                task = Task()
                task.cancel(name)

            elif argv[1] == 'delete':
                name = argv[2]
                task = Task()
                task.delete(name)
        else:
            if argv[1] == 'list':
                task = Task()
                task.list()
            else:
                print("Please, informe the task name.")
                exit(1)
    else:
        print("Please, informe an valid option.")
        exit(1)
