import os
from datetime import date

import django



# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Task
# Create task instances with custom creation dates
task1 = Task(
    title="Task 1",
    description="Description for Task 1",
    priority="High",
    creation_date=date(2023, 1, 15),
    completion_date=date(2023, 1, 25)
)

task2 = Task(
    title="Task 2",
    description="Description for Task 2",
    priority="Medium",
    is_completed=True,
    creation_date=date(2023, 2, 1),
    completion_date=date(2023, 2, 10)
)

task3 = Task(
    title="Task 3",
    description="Description for Task 3",
    priority="Hard",
    is_completed=True,
    creation_date=date(2023, 1, 15),
    completion_date=date(2023, 1, 20)
)

# Save the tasks to the database
task1.save()
task2.save()
task3.save()
task2.search_tasks()
Task.search_tasks()

# Now, you can run the defined methods

# 1. Get ongoing high-priority tasks
ongoing_high_priority = Task.ongoing_high_priority_tasks()
print("Ongoing High Priority Tasks:")
for task in ongoing_high_priority:
    print('- ' + task.title)

# 2. Get completed medium-priority tasks
completed_mid_priority = Task.completed_mid_priority_tasks()
print("Completed Medium Priority Tasks:")
for task in completed_mid_priority:
    print('- ' + task.title)

# 3. Search for tasks based on a query
search_results = Task.search_tasks("Task 3")
print("Search Results:")
for task in search_results:
    print('- ' + task.title)

# 4. Get recent completed tasks
recent_completed = task1.recent_completed_tasks(days=5)
print("Recent Completed Tasks:")
for task in recent_completed:
    print('- ' + task.title)
