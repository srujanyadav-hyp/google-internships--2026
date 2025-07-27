import time
import os
import threading
import sys
import termios
import tty

# --- Task Class ---
class Task:
    def __init__(self, title, duration):
        self.title = title
        self.duration = duration  # in minutes

# --- Globals ---
TASK_FILE = "tasks.txt"
tasks = []
pause_flag = threading.Event()
stop_flag = threading.Event()

# --- Task File I/O ---
def load_tasks():
    if not os.path.exists(TASK_FILE):
        return
    with open(TASK_FILE, "r") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 2:
                title, duration = parts
                tasks.append(Task(title, int(duration)))

def save_task(task):
    with open(TASK_FILE, "a") as f:
        f.write(f"{task.title}|{task.duration}\n")

# --- Input Handling for Pause/Resume/Stop ---
def get_char():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def listen_for_keys():
    while True:
        char = get_char()
        if char == 'p':
            pause_flag.set()
            print("\n⏸️ Paused. Press 'r' to resume.")
        elif char == 'r':
            pause_flag.clear()
            print("\n▶️ Resumed.")
        elif char == 'q':
            stop_flag.set()
            print("\n⏹️ Timer stopped.")
            break

# --- Task Functions ---
def add_task():
    title = input("Enter task title: ")
    try:
        duration = int(input("Enter time in minutes for this task: "))
        task = Task(title, duration)
        tasks.append(task)
        save_task(task)
        print(f"✅ Task '{title}' added for {duration} minutes.\n")
    except ValueError:
        print("❌ Invalid duration. Please enter a number.\n")

def list_tasks():
    if not tasks:
        print("🚫 No tasks available.\n")
        return
    print("📝 Tasks:")
    for i, task in enumerate(tasks):
        print(f"{i+1}. {task.title} ({task.duration} minutes)")
    print()

def start_task_timer():
    if not tasks:
        print("🚫 No tasks to start.\n")
        return
    list_tasks()
    try:
        choice = int(input("Select task number to start: "))
        if 1 <= choice <= len(tasks):
            task = tasks[choice - 1]
            print(f"\n⏳ Starting timer for '{task.title}' ({task.duration} mins):")
            print("🔁 Press 'p' to pause, 'r' to resume, 'q' to quit.\n")

            total_seconds = task.duration * 60
            pause_flag.clear()
            stop_flag.clear()

            # Start listening thread
            listener = threading.Thread(target=listen_for_keys, daemon=True)
            listener.start()

            while total_seconds > 0:
                if stop_flag.is_set():
                    print(f"⏹️ Timer manually stopped at {total_seconds // 60} mins {total_seconds % 60} secs left.\n")
                    break
                if not pause_flag.is_set():
                    mins, secs = divmod(total_seconds, 60)
                    print(f"\r⏱ {mins:02d}:{secs:02d}", end="")
                    time.sleep(1)
                    total_seconds -= 1
                else:
                    time.sleep(0.2)

            if total_seconds == 0 and not stop_flag.is_set():
                print(f"\n✅ Time's up for task: {task.title}!\n")
        else:
            print("❌ Invalid choice.\n")
    except ValueError:
        print("❌ Please enter a valid number.\n")

# --- Main Menu ---
def main():
    load_tasks()
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
            print("👋 Exiting. Stay focused!")
            break
        else:
            print("❌ Invalid choice. Try again.\n")

if __name__ == "__main__":
    main()
