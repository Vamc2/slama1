import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import random
import tkinter as tk
from tkinter import simpledialog, messagebox

# Initialize an empty task list
tasks = pd.DataFrame(columns=['description', 'priority'])

# Load pre-existing tasks from a CSV file (if any)
try:
    tasks = pd.read_csv('tasks.csv')
except FileNotFoundError:
    pass

# Train the task priority classifier only if there are tasks available
if not tasks.empty and 'description' in tasks.columns and 'priority' in tasks.columns:
    vectorizer = CountVectorizer()
    clf = MultinomialNB()
    model = make_pipeline(vectorizer, clf)
    model.fit(tasks['description'], tasks['priority'])

# Function to save tasks to a CSV file
def save_tasks():
    tasks.to_csv('tasks.csv', index=False)

# Function to add a task to the list with a popup
def add_task_popup():
    global tasks
    description = simpledialog.askstring("Add Task", "Enter task description:")
    if description:
        priority = simpledialog.askstring("Add Task", "Enter task priority (Low/Medium/High):")
        if priority and priority.capitalize() in ['Low', 'Medium', 'High']:
            new_task = pd.DataFrame({'description': [description], 'priority': [priority.capitalize()]})
            tasks = pd.concat([tasks, new_task], ignore_index=True)
            save_tasks()
            messagebox.showinfo("Success", "Task added successfully.")
        else:
            messagebox.showerror("Error", "Invalid priority. Please enter Low, Medium, or High.")
    else:
        messagebox.showerror("Error", "Task description cannot be empty.")

# Function to remove a task with a popup
def remove_task_popup():
    global tasks
    description = simpledialog.askstring("Remove Task", "Enter task description to remove:")
    if description:
        tasks = tasks[tasks['description'] != description]
        save_tasks()
        messagebox.showinfo("Success", "Task removed successfully.")
    else:
        messagebox.showerror("Error", "Task description cannot be empty.")

# Function to list all tasks with a popup
def list_tasks_popup():
    if tasks.empty:
        messagebox.showinfo("Task List", "No tasks available.")
    else:
        task_list_str = tasks.to_string(index=False)
        messagebox.showinfo("Task List", task_list_str)

# Function to prioritize a task with a popup
def prioritize_task_popup():
    global tasks
    description = simpledialog.askstring("Prioritize Task", "Enter task description to prioritize:")
    if description:
        priority = simpledialog.askstring("Prioritize Task", "Enter new priority (Low/Medium/High):")
        if priority and priority.capitalize() in ['Low', 'Medium', 'High']:
            tasks.loc[tasks['description'] == description, 'priority'] = priority.capitalize()
            save_tasks()
            messagebox.showinfo("Success", "Task prioritized successfully.")
        else:
            messagebox.showerror("Error", "Invalid priority. Please enter Low, Medium, or High.")
    else:
        messagebox.showerror("Error", "Task description cannot be empty.")

# Function to recommend a task with a popup
def recommend_task_popup():
    if not tasks.empty:
        high_priority_tasks = tasks[tasks['priority'] == 'High']

        if not high_priority_tasks.empty:
            random_task = random.choice(high_priority_tasks['description'])
            messagebox.showinfo("Recommended Task", f"Recommended task: {random_task} - Priority: High")
        else:
            messagebox.showinfo("Recommendation", "No high-priority tasks available for recommendation.")
    else:
        messagebox.showinfo("Recommendation", "No tasks available for recommendations.")

# Tkinter GUI
root = tk.Tk()
root.title("Task Management App")

# Buttons for various actions
add_button = tk.Button(root, text="Add Task", command=add_task_popup)
add_button.pack()

remove_button = tk.Button(root, text="Remove Task", command=remove_task_popup)
remove_button.pack()

list_button = tk.Button(root, text="List Tasks", command=list_tasks_popup)
list_button.pack()

prioritize_button = tk.Button(root, text="Prioritize Task", command=prioritize_task_popup)
prioritize_button.pack()

recommend_button = tk.Button(root, text="Recommend Task", command=recommend_task_popup)
recommend_button.pack()

exit_button = tk.Button(root, text="Exit", command=root.destroy)
exit_button.pack()

root.mainloop()
