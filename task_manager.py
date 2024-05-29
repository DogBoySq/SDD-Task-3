import datetime

class TaskManager:
    # TaskManager class for managing tasks, including loading, saving, adding, and deleting tasks.
    def __init__(self, file_path):
        # Initialize the TaskManager.
        # Args:
        #     file_path (str): The path to the file where tasks are stored.
        self.file_path = file_path
        self.tasks = self.load_tasks()

    def load_tasks(self):
        # Load tasks from the file.
        # Returns:
        #     list: A list of tasks, where each task is a dictionary with 'description' and 'due_date' keys.
        tasks = []
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    description, due_date_str = line.strip().split('|')
                    due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d %H:%M:%S")
                    tasks.append({'description': description, 'due_date': due_date})
        except FileNotFoundError:
            pass
        return tasks

    def save_tasks(self):
        # Save tasks to the file.
        with open(self.file_path, 'w') as file:
            for task in self.tasks:
                file.write(f"{task['description']}|{task['due_date'].strftime('%Y-%m-%d %H:%M:%S')}\n")

    def add_task(self, description, due_date):
        # Add a new task.
        # Args:
        #     description (str): The task description.
        #     due_date (datetime): The task due date.
        self.tasks.append({'description': description, 'due_date': due_date})
        self.save_tasks()

    def delete_task(self, description, due_date):
        # Delete a task.
        # Args:
        #     description (str): The task description.
        #     due_date (datetime): The task due date.
        self.tasks = [task for task in self.tasks if not (task['description'] == description and task['due_date'] == due_date)]
        self.save_tasks()
