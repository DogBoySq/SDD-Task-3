import tkinter as tk
from tkinter import ttk
from task_manager import TaskManager
from task_list import TaskListView

class App(tk.Tk):
    # Main application class for the productivity app.
    # Inherits from tk.Tk.
    def __init__(self):
        # Initialize the main application window.
        super().__init__()
        self.title("Productivity App")
        self.geometry("600x400")
        self.task_manager = TaskManager("tasks.txt")  # Initialize the TaskManager with the path to the tasks file
        self._frame = None
        self.create_styles()
        self.switch_frame(TaskListView)  # Start with the TaskListView frame

    def create_styles(self):
        # Create and configure styles for the ttk widgets.
        style = ttk.Style(self)
        style.configure("Treeview", font=("Helvetica", 10), rowheight=25)
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        style.configure("TButton", font=("Helvetica", 10), padding=5)

    def switch_frame(self, frame_class):
        # Destroy the current frame and replace it with a new one.
        # Args:
        #     frame_class (tk.Frame): The new frame class to switch to.
        new_frame = frame_class(self, self.task_manager)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill='both', expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()
