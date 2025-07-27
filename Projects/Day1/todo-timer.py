import tkinter as tk
from tkinter import messagebox, simpledialog
import time
import json
import threading
import os
from playsound import playsound

TASKS_FILE = "tasks.json"

class TaskTimer:
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do Timer Manager")

        self.tasks = []
        self.current_timer = None
        self.timer_running = False
        self.timer_paused = False
        self.remaining_time = 0

        # UI
        self.task_entry = tk.Entry(master, width=40)
        self.task_entry.pack(pady=5)

        self.time_entry = tk.Entry(master, width=20)
        self.time_entry.insert(0, "mm:ss")
        self.time_entry.pack(pady=5)

        self.add_button = tk.Button(master, text="Add Task", command=self.add_task)
        self.add_button.pack()

        self.listbox = tk.Listbox(master, width=50)
        self.listbox.pack(pady=10)

        self.start_button = tk.Button(master, text="Start", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = tk.Button(master, text="Pause", command=self.pause_timer)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.resume_button = tk.Button(master, text="Resume", command=self.resume_timer)
        self.resume_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(master, text="Stop", command=self.stop_timer)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(master, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(pady=5)

        self.load_tasks()

    def add_task(self):
        task_name = self.task_entry.get()
        time_str = self.time_entry.get()
        if not task_name or not time_str:
            messagebox.showwarning("Input Error", "Enter task and time (mm:ss)")
            return
        try:
            minutes, seconds = map(int, time_str.split(":"))
            total_seconds = minutes * 60 + seconds
        except:
            messagebox.showwarning("Format Error", "Use mm:ss format for time")
            return

        self.tasks.append({"name": task_name, "time": total_seconds})
        self.save_tasks()
        self.update_listbox()
        self.task_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            display_time = time.strftime('%M:%S', time.gmtime(task['time']))
            self.listbox.insert(tk.END, f"{task['name']} - {display_time}")

    def start_timer(self):
        if self.timer_running or self.timer_paused:
            return
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("No task", "Please select a task to start")
            return
        index = selection[0]
        self.current_task = self.tasks[index]
        self.remaining_time = self.current_task["time"]
        self.timer_running = True
        self.timer_paused = False
        self.timer_thread = threading.Thread(target=self.run_timer)
        self.timer_thread.start()

    def run_timer(self):
        while self.remaining_time > 0 and self.timer_running:
            if self.timer_paused:
                time.sleep(1)
                continue
            mins, secs = divmod(self.remaining_time, 60)
            self.master.title(f"{self.current_task['name']} - {mins:02}:{secs:02}")
            time.sleep(1)
            self.remaining_time -= 1

        if self.remaining_time == 0 and self.timer_running:
            self.master.title("Time's up!")
            playsound("alarm.mp3")  # Provide your own short mp3/wav file in the same folder
            messagebox.showinfo("Done", f"Task '{self.current_task['name']}' finished!")
        self.timer_running = False
        self.timer_paused = False

    def pause_timer(self):
        if self.timer_running:
            self.timer_paused = True

    def resume_timer(self):
        if self.timer_running and self.timer_paused:
            self.timer_paused = False

    def stop_timer(self):
        self.timer_running = False
        self.timer_paused = False
        self.master.title("To-Do Timer Manager")

    def delete_task(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("No task", "Select a task to delete")
            return
        index = selection[0]
        del self.tasks[index]
        self.save_tasks()
        self.update_listbox()

    def save_tasks(self):
        with open(TASKS_FILE, "w") as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r") as f:
                self.tasks = json.load(f)
                self.update_listbox()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskTimer(root)
    root.mainloop()
