import time
from datetime import datetime

# Task class to store each task
class Task:
    def __init__(self, title, duration):
        self.title = title
        self.duration = duration  # in minutes

tasks = []

# Add new task
def add_task():
    title = input("Enter task title: ")
    duration = int(input("Enter time in minutes for this task: "))
    task = Task(title, duration)
    tasks.append(task)
    print(f"✅ Task '{title}' added for {duration} minutes.\n")

# List all tasks
def list_tasks():
    if not tasks:
        print("🚫 No tasks available.\n")
        return
    print("📝 Tasks:")
    for i, task in enumerate(tasks):
        print(f"{i+1}. {task.title} ({task.duration} minutes)")
    print()

# Start a timer for selected task
def start_task_timer():
    if not tasks:
        print("🚫 No tasks to start.\n")
        return
    list_tasks()
    try:
        choice = int(input("Select task number to start: "))
        if 1 <= choice <= len(tasks):
            task = tasks[choice - 1]
            print(f"⏳ Starting timer for '{task.title}' ({task.duration} mins):\n")
            total_seconds = task.duration * 60
            try:
                while total_seconds:
                    mins, secs = divmod(total_seconds, 60)
                    print(f"\r⏱ {mins:02d}:{secs:02d}", end="")
                    time.sleep(1)
                    total_seconds -= 1
                print(f"\n✅ Time's up for task: {task.title}!\n")
            except KeyboardInterrupt:
                print(f"\n⏹️ Timer for '{task.title}' was stopped manually.\n")
        else:
            print("❌ Invalid choice.\n")
    except ValueError:
        print("❌ Please enter a valid number.\n")

# Main menu
def main():
    while True:
        print("📋 To-Do Timer Manager")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Start Task Timer")
        print("4. Exit")
        choice = input("Select an option: ")
        if choice == '1':
            add_task()
        elif choice == '2':
            list_tasks()
        elif choice == '3':
            start_task_timer()
        elif choice == '4':
            print("👋 Exiting. Have a productive day!")
            break
        else:
            print("❌ Invalid choice. Try again.\n")

if __name__ == "__main__":
    main()
