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
        #     list: A list of tasks with 'description' and 'due_date'.
        tasks = []  # List to store tasks
        try:
            with open(self.file_path, 'r') as file:  # Open the file for reading
                for line in file:  # Read each line in the file
                    description, due_date_str = line.strip().split('|')  # Split line into description and due date
                    due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d %H:%M:%S")  # Convert due date to datetime
                    tasks.append({'description': description, 'due_date': due_date})  # Add task to the list
        except FileNotFoundError:  # If the file doesn't exist
            pass  # Do nothing
        return tasks  # Return the list of tasks

    def save_tasks(self):
        # Save tasks to the file.
        with open(self.file_path, 'w') as file:  # Open the file for writing
            for task in self.tasks:  # For each task in the list
                file.write(f"{task['description']}|{task['due_date'].strftime('%Y-%m-%d %H:%M:%S')}\n")  # Write task to the file

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
