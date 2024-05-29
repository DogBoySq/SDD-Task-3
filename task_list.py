import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import datetime

class TaskListView(tk.Frame):
    # TaskListView class for displaying and managing the task list.
    # Inherits from tk.Frame.
    def __init__(self, master, task_manager):
        # Initialize the TaskListView frame.
        # Args:
        #     master (tk.Tk): The root window of the application.
        #     task_manager (TaskManager): The task manager instance.
        super().__init__(master)
        self.master = master
        self.task_manager = task_manager
        self.create_widgets()
        self.load_tasks()
        self.start_countdown_update()

    def create_widgets(self):
        # Create and pack the widgets for the task list view.
        self.tree = ttk.Treeview(self, columns=('Description', 'Due Date', 'Countdown', 'Remaining Seconds'), show='headings')
        self.tree.heading('Description', text='Description', command=lambda: self.sort_column('Description', False))
        self.tree.heading('Due Date', text='Due Date', command=lambda: self.sort_column('Due Date', False))
        self.tree.heading('Countdown', text='Countdown', command=lambda: self.sort_column('Countdown', False))
        self.tree.heading('Remaining Seconds', text='Remaining Seconds', command=lambda: self.sort_column('Remaining Seconds', False))
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side="bottom", fill="x", pady=10)

        self.add_button = ttk.Button(self.button_frame, text="Add Task", command=self.add_task)
        self.add_button.pack(side="left", padx=10)

        self.delete_button = ttk.Button(self.button_frame, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(side="left", padx=10)

    def load_tasks(self):
        # Load tasks from the task manager and display them in the treeview.
        self.tree.delete(*self.tree.get_children())  # Clear existing tasks
        for task in self.task_manager.tasks:
            self.add_task_to_view(task['description'], task['due_date'])

    def add_task_to_view(self, description, due_date):
        # Add a task to the treeview.
        # Args:
        #     description (str): The task description.
        #     due_date (datetime): The task due date.
        countdown = due_date - datetime.datetime.now()
        formatted_countdown, remaining_seconds = self.format_countdown(countdown)
        item_id = self.tree.insert('', 'end', values=(description, due_date.strftime("%Y-%m-%d %H:%M:%S"), formatted_countdown, remaining_seconds))
        self.tree.item(item_id, tags=('countdown',))  # Add tag to identify countdown items

    def delete_task_from_view(self, item):
        # Delete a task from the treeview.
        # Args:
        #     item (str): The item ID of the task to delete.
        self.tree.delete(item)

    def format_countdown(self, countdown):
        # Format the countdown timer to display days, hours, minutes, and remaining seconds.
        # Args:
        #     countdown (datetime.timedelta): The countdown time.
        # Returns:
        #     tuple: Formatted countdown string and remaining seconds.
        total_seconds = countdown.total_seconds()
        days = total_seconds // (24 * 3600)
        remaining_seconds = total_seconds % (24 * 3600)
        hours = remaining_seconds // 3600
        minutes = (remaining_seconds % 3600) // 60
        seconds = remaining_seconds % 60

        formatted_countdown = f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"
        return formatted_countdown, int(total_seconds)

    def sort_column(self, col, reverse):
        # Sort the treeview column in the specified order.
        # Args:
        #     col (str): The column name to sort by.
        #     reverse (bool): Whether to sort in reverse order.
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]

        if col == 'Description':
            items.sort(reverse=reverse)
        elif col == 'Due Date':
            items.sort(key=lambda x: datetime.datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S"), reverse=reverse)
        elif col == 'Countdown':
            items.sort(key=lambda x: self.parse_countdown(x[0]), reverse=reverse)
        elif col == 'Remaining Seconds':
            items.sort(key=lambda x: x[1], reverse=reverse)

        for index, (val, k) in enumerate(items):
            self.tree.move(k, '', index)

        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))

    def parse_countdown(self, countdown_str):
        # Parse the countdown string into total seconds.
        # Args:
        #     countdown_str (str): The countdown string.
        # Returns:
        #     int: Total seconds of the countdown.
        countdown_str = countdown_str.strip()
        days, hours, minutes, seconds = 0, 0, 0, 0
        if 'd' in countdown_str:
            days_part, countdown_str = countdown_str.split('d')
            days = int(days_part.strip())
        if 'h' in countdown_str:
            hours_part, countdown_str = countdown_str.split('h')
            hours = int(hours_part.strip())
        if 'm' in countdown_str:
            minutes_part, countdown_str = countdown_str.split('m')
            minutes = int(minutes_part.strip())
        if 's' in countdown_str:
            seconds_part, _ = countdown_str.split('s')
            seconds = int(seconds_part.strip())

        return days * 24 * 3600 + hours * 3600 + minutes * 60 + seconds

    def add_task(self):
        # Prompt the user to add a new task.
        description = simpledialog.askstring("Task Description", "Enter task description:")
        due_date_str = simpledialog.askstring("Due Date", "Enter due date (YYYY-MM-DD HH:MM:SS):")

        if description and due_date_str:
            try:
                due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d %H:%M:%S")
                self.task_manager.add_task(description, due_date)
                self.load_tasks()  # Reload tasks to reflect changes
            except ValueError:
                messagebox.showerror("Invalid Date Format", "Please enter the date in the format YYYY-MM-DD HH:MM:SS")

    def delete_task(self):
        # Delete the selected task after confirming with the user.
        selected_item = self.tree.selection()
        if selected_item:
            confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected task?")
            if confirm:
                item_values = self.tree.item(selected_item[0])['values']
                description = item_values[0]
                due_date = datetime.datetime.strptime(item_values[1], "%Y-%m-%d %H:%M:%S")
                self.task_manager.delete_task(description, due_date)
                self.load_tasks()  # Reload tasks to reflect changes

    def start_countdown_update(self):
        # Start the countdown update process.
        self.update_countdowns()

    def update_countdowns(self):
        # Update the countdowns displayed in the treeview.
        items = self.tree.get_children()
        for item in items:
            description, due_date_str, formatted_countdown, remaining_seconds = self.tree.item(item, 'values')
            due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d %H:%M:%S")
            countdown = due_date - datetime.datetime.now()
            formatted_countdown, remaining_seconds = self.format_countdown(countdown)
            self.tree.item(item, values=(description, due_date_str, formatted_countdown, remaining_seconds))
        self.after(1000, self.update_countdowns)
