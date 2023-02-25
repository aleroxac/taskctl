from uuid import uuid4
from datetime import datetime
from sys import argv, exit
from json import dump, dumps, load
from pathlib import Path


class Task():
    def __init__(self, name, description, owner):
        self.id = str(uuid4())
        self.name = name
        self.description = description
        self.owner = owner
        self.creation_at = str(datetime.now())


        if not Path('.tasks.json').exists():
            self.task = {
                'id': self.id,
                'name': self.name,
                'description': self.description,
                'creation_at': self.creation_at,
                'owner': self.owner
            }
        else:
            self.task = load(open('.tasks.json', 'r'))


    def create(self):
        self.store()
        return dumps(self.task, indent=2)


    def start(self):
        if 'started_at' in self.task.keys():
            self.task['started_at'].append(str(datetime.now()))
        else:
            self.task['started_at'] = []
            self.task['started_at'].append(str(datetime.now()))

        if 'stoped_at' in self.task.keys():
            count_stops = len(self.task['stoped_at'])
            count_starts = len(self.task['started_at']) 
            if not (count_starts - count_stops) < 2:
                raise Exception("You can't start a task that already started.")

        self.store()
        return dumps(self.task, indent=2)


    def stop(self):
        if not 'started_at' in self.task.keys():
            raise Exception("You can't stop a task that hasn't started yet.")
        else:
            if 'stoped_at' in self.task.keys():
                self.task['stoped_at'].append(str(datetime.now()))
            else:
                self.task['stoped_at'] = []
                self.task['stoped_at'].append(str(datetime.now()))

            count_starts = len(self.task['started_at']) 
            count_stops = len(self.task['stoped_at'])
            if count_stops > count_starts:
                raise Exception("You can't stop a task that already stoped.")

            start_datetime = datetime.strptime(self.task['started_at'][-1], "%Y-%m-%d %H:%M:%S.%f")
            stop_datetime = datetime.strptime(self.task['stoped_at'][-1], "%Y-%m-%d %H:%M:%S.%f")
            if 'duration' in self.task.keys():
                current_duration = datetime.strptime(self.task['duration'], "%H:%M:%S.%f")
                self.task['duration'] = str((stop_datetime - start_datetime) + current_duration).split(' ')[1]
            else:
                self.task['duration'] = str(stop_datetime - start_datetime)
        self.store()
        return dumps(self.task, indent=2)


    def finish(self):
        if 'finished_at' in self.task.keys():
            raise Exception("You can't finish a task that already finished.")
        elif not 'started_at' in self.task.keys():
            raise Exception("You can't finish a task that hasn't started yet.")
        else:
            self.task['finished_at'] = str(datetime.now())

            start_datetime = datetime.strptime(self.task['started_at'][0], "%Y-%m-%d %H:%M:%S.%f")
            finish_datetime = datetime.strptime(self.task['finished_at'], "%Y-%m-%d %H:%M:%S.%f")
            self.task['duration'] = str(finish_datetime - start_datetime)
        self.store()
        return dumps(self.task, indent=2)


    def store(self):
        task_content = self.task
        with open('.tasks.json', 'w+',) as task_file:
            dump(task_content, task_file, indent=2)


if __name__ == "__main__":
    if argv[1] == 'create':
        name = argv[2]
        description = argv[3]
        owner = argv[4]

        task = Task(name, description, owner)
        print(task.create())

    if argv[1] == 'start':
        name = argv[2]
        task_data = load(open('.tasks.json', 'r'))
        task = Task(task_data['name'], task_data['description'], task_data['owner'])
        print(task.start())

    if argv[1] == 'stop':
        name = argv[2]
        task_data = load(open('.tasks.json', 'r'))
        task = Task(task_data['name'], task_data['description'], task_data['owner'])
        print(task.stop())

    if argv[1] == 'finish':
        name = argv[2]
        task_data = load(open('.tasks.json', 'r'))
        task = Task(task_data['name'], task_data['description'], task_data['owner'])
        print(task.finish())