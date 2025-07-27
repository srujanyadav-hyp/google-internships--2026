import time
from datetime import datetime

# Store tasks in a list of dicts
tasks = []

def add_task():
    title = input("Enter task title: ")
    try:
        minutes = int(input("Enter time in minutes for this task: "))
        tasks.append({"title": title, "minutes": minutes, "added": datetime.now()})
        print(f"✅ Task '{title}' added for {minutes} minutes.\n")
    except ValueError:
        print("❌ Please enter a valid number for minutes.\n")

def show_tasks():
    if not tasks:
        print("📭 No tasks available.\n")
        return
    print("\n📝 Task List:")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task['title']} - {task['minutes']} min")
    print()

def start_timer():
    show_tasks()
    try:
        choice = int(input("Enter task number to start timer: ")) - 1
        task = tasks[choice]
        minutes = task["minutes"]
        seconds = minutes * 60
        print(f"⏳ Starting timer for '{task['title']}' ({minutes} mins):\n")

        while seconds:
            mins = seconds // 60
            secs = seconds % 60
            timer = f"{mins:02d}:{secs:02d}"
            print(f"\r⏱ {timer}", end="")
            time.sleep(1)
            seconds -= 1

        print(f"\n✅ Time's up for task: {task['title']}!\n")
    except (IndexError, ValueError):
        print("❌ Invalid choice.\n")

def main():
    while True:
        print("===== TO-DO MANAGER WITH TIMER =====")
        print("1. Add Task")
        print("2. Show Tasks")
        print("3. Start Task Timer")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            add_task()
        elif choice == '2':
            show_tasks()
        elif choice == '3':
            start_timer()
        elif choice == '4':
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid input, try again.\n")

if __name__ == "__main__":
    main()
