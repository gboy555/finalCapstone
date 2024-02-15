# Notes:
# 1. Use the following username and password to access the admin rights
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the
# program will look in your root directory for the text files.

# =====importing libraries===========
import os
from datetime import datetime, date, time
from tabulate import tabulate
import pandas as pd
import numpy as np

DATETIME_STRING_FORMAT = "%Y-%m-%d"
task_list = []

# Functions START


def read_users():
    # If no user.txt file, write one with a default account
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")

    global username_password
    # Read in user_data
    with open("user.txt", "r") as user_file:
        user_data = user_file.read().split("\n")

    # Convert to a dictionary
    username_password = {}
    for user in user_data:
        username, password = user.split(";")
        username_password[username] = password


def read_task_list():
    # Create tasks.txt if it doesn't exist
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as default_file:
            pass

    with open("tasks.txt", "r") as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    global task_list
    task_list = []
    for t_str in task_data:
        curr_t = {}

        # Split by semicolon and manually add each component
        task_components = t_str.split(";")
        curr_t["username"] = task_components[0]
        curr_t["title"] = task_components[1]
        curr_t["description"] = task_components[2]
        curr_t["due_date"] = datetime.strptime(
            task_components[3], DATETIME_STRING_FORMAT
        )
        curr_t["assigned_date"] = datetime.strptime(
            task_components[4], DATETIME_STRING_FORMAT
        )
        curr_t["completed"] = True if task_components[5] == "Yes" else False

        task_list.append(curr_t)


def reg_user():
    """Add a new user to the user.txt file"""
    # Modified - START
    # Codes to avoid duplicated username
    global username_password
    new_username_duplicated = True
    print(username_password)
    while new_username_duplicated:
        # - Request input of a new username
        new_username = input("New Username: ")
        if new_username.lower() not in username_password:
            new_username_duplicated = False
        else:
            print(
                f"{new_username} is existing user. Please provide another username for registration."
            )
    # Modified - END

    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password

        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

    # - Otherwise you present a relevant message.
    else:
        print("Passwords do no match")


def validate_date_time():
    """
    Function to ask for date input.
    """
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")
    return due_date_time


def add_task():
    """Allow a user to add a new task to task.txt file
    Prompt a user for the following:
        - A username of the person whom the task is assigned to,
        - A title of a task,
        - A description of the task and
        - the due date of the task."""
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

    due_date_time = validate_date_time()

    # Then get the current date.
    curr_date = date.today()
    """ Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete."""
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False,
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t["username"],
                t["title"],
                t["description"],
                t["due_date"].strftime(DATETIME_STRING_FORMAT),
                t["assigned_date"].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t["completed"] else "No",
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")


def view_all():
    """Reads the task from task.txt file and prints to the console in the
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling)
    """

    # Define the column headers
    headers = [
        "ID",
        "Task",
        "Assigned to",
        "Date Assigned",
        "Due Date",
        "Task Description",
        "Task Completed",
    ]

    # Create a list to store the rows of the table
    table_data = []

    # Create a list to store incomplete task
    incomplete_task = []

    # Your existing task_list loop
    for idx, t in enumerate(task_list, start=1):
        row = [
            idx,
            t["title"],
            t["username"],
            t["assigned_date"].strftime(DATETIME_STRING_FORMAT),
            t["due_date"].strftime(DATETIME_STRING_FORMAT),
            t["description"],
            "Yes" if t["completed"] else "No",
        ]
        table_data.append(row)
        # Add incomplete task into the list
        if not t["completed"]:
            incomplete_task.append(idx)

    # Using tabulate to format data as a table
    disp_str = tabulate(table_data, headers, tablefmt="pipe")
    print(disp_str)

    if len(incomplete_task) > 0:
        """
        Only allow user to edit task if there is at least 1 incomplete task
        Allow user to edit task
        """
        while True:
            try:
                idx_to_modify = int(
                    input(
                        "Please enter ID to modify a task OR -1 to return to main menu\n:"
                    )
                )
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

            if idx_to_modify == -1:
                break

            if idx_to_modify in incomplete_task:
                modify_task(idx_to_modify, table_data[idx_to_modify - 1][1])
                break
            else:
                print(
                    f"You cannot update task id : {idx_to_modify} because it is completed."
                )


def view_mine():
    """Reads the task from task.txt file and prints to the console in the
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling)
    """
    for t in task_list:
        if t["username"] == curr_user:
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += (
                f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            )
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)


def modify_task(idx, task_title):
    """
    Display menu to allow user decide what to update
    """
    while True:
        # If task is updated as "Completed", return to previous menu immediately.
        if task_list[idx - 1]["completed"]:
            print("This task is marked as 'Completed'.")
            break

        print(f"You selected task titled '{task_title}' to modify.")
        modify_task_menu = input(
            """Select one of the following options below to modify the task:
c - Make task as Completed
e - Edit the task
f - Finish modifying task
: """
        ).lower()

        if modify_task_menu == "c":
            # Update task as Yes
            modify_task_detail(idx, "completed", "Yes")
        elif modify_task_menu == "e":
            edit_task(idx, task_title)
        elif modify_task_menu == "a":
            assign_task(idx)
        elif modify_task_menu == "md":
            print("md")
        elif modify_task_menu == "f":
            break


def edit_task(idx, task_title):
    """
    Show edit menu for user to choose
    """

    if task_list[idx - 1]["completed"]:
        print(f"Task {task_title} is completed. You cannot edit this task anymore.")
        return

    while True:
        print(f"You are editing task titled '{task_title}'.")
        edit_task_menu = input(
            """Select one of the following options below to modify the task:
a - Assign task to another person
u - Update due date
f - Finish editing task
: """
        ).lower()

        if edit_task_menu == "a":
            assign_task(idx)
        elif edit_task_menu == "u":
            update_task_due_date(idx)
        elif edit_task_menu == "f":
            break


def assign_task(idx):
    """
    Function to assign task to a user
    """
    # Get Current task assignee
    task_assignee = task_list[idx - 1]["username"]

    # Show user list with id for assignment
    user_table_headers = ["Id", "Username"]
    user_table_data = []

    # Add user name into a list
    id_to_display = 1
    for username in username_password:
        if username != task_assignee:
            user_row = [
                id_to_display,
                username,
            ]
            user_table_data.append(user_row)
            id_to_display = id_to_display + 1

    print(tabulate(user_table_data, user_table_headers, tablefmt="pipe"))

    # Ask user to pick a new assignee
    while True:
        try:
            user_id_to_assign = int(
                input("Please assign the task to the user by providing the Id\n:")
            )
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

        if any(user_id == user_id_to_assign for user_id, _ in user_table_data):
            modify_task_detail(
                idx, "username", user_table_data[user_id_to_assign - 1][1]
            )
            break
        else:
            print("The id you provided cannot be found. Please try again.")


def update_task_due_date(idx):
    print("Updating due date.")
    due_date_time = validate_date_time()
    modify_task_detail(idx, "due_date", due_date_time.strftime(DATETIME_STRING_FORMAT))


def modify_task_detail(idx, attribute, value):
    """
    Modify task details by providing
    1. Task ID
    2. Attribute to be updated
    3. value to update
    """

    attribute_key_pair = {
        "username": 0,
        "title": 1,
        "description": 2,
        "due_date": 3,
        "assigned_date": 4,
        "completed": 5,
    }

    row_idx = idx - 1  # (0-based index)
    attribute_id = attribute_key_pair[attribute]

    # Open task file to update
    file_path = "tasks.txt"
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Turn lines into list with dictionary
    tasks_to_update = [line.strip().split(";") for line in lines]

    # Update value into list
    tasks_to_update[row_idx][attribute_id] = value

    # Write the updated value into txt file
    with open(file_path, "w") as file:
        for task in tasks_to_update:
            file.write(";".join(task) + "\n")
    print(f"Task {str(idx)} is updated.")

    # Refresh the task data in memory
    read_task_list()
    return


def generate_reports():
    print("Reports are being generated.")
    print("Task overview report is being generated.")
    generate_task_overview()
    print("Task overview report is ready for review.")
    print("User overview report is being generated.")
    generate_user_overview()
    print("User overview report is ready for review.")


def generate_task_overview():
    """
    Generate Task Overview report
    """
    # Ensure task_list is always the most updated
    read_task_list()
    # Perform calculation using task_list
    count_of_task = len(task_list)
    count_of_Completed_task = sum(1 for dict in task_list if dict.get("completed"))
    count_of_Uncompleted_task = count_of_task - count_of_Completed_task
    today_datetime = datetime.combine(date.today(), time.min)
    count_of_Uncompleted_overdue_task = sum(
        1
        for dict in task_list
        if dict.get("completed") is False and today_datetime > dict.get("due_date")
    )
    percentage_of_incomplete = (
        (count_of_Uncompleted_task / count_of_task) * 100 if count_of_task != 0 else 0
    )
    percentage_of_overdue = (
        (count_of_Uncompleted_overdue_task / count_of_task) * 100
        if count_of_task != 0
        else 0
    )

    # Print out result
    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write("Task Overview Report\n")
        task_overview_file.write(
            f"Generation Time : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} by {curr_user}\n"
        )
        task_overview_file.write(f"Number of all tasks : {count_of_task}\n")
        task_overview_file.write(
            f"Number of Completed tasks : {count_of_Completed_task}\n"
        )
        task_overview_file.write(
            f"Number of Uncompleted tasks : {count_of_Uncompleted_task}\n"
        )
        task_overview_file.write(
            f"Number of Uncompleted and overdue tasks : {count_of_Uncompleted_overdue_task}\n"
        )
        task_overview_file.write(
            f"Task incompletion rate : {progress_bar(percentage_of_incomplete)}\n"
        )
        task_overview_file.write(
            f"Task overdue rate : {progress_bar(percentage_of_overdue)}\n"
        )


def progress_bar(percentage):
    progress_bar_length = 20
    filled_length = int(progress_bar_length * percentage / 100)

    progress_bar = (
        "[" + "=" * filled_length + " " * (progress_bar_length - filled_length) + "]"
    )
    return f"{percentage:.2f}% {progress_bar}"


def generate_user_overview():
    """
    Generate user overview report
    """

    # Get most updated ist
    read_users()
    read_task_list()

    # Total number of user
    count_of_users = len(username_password)
    count_of_task = len(task_list)

    # Print the file
    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write("User Overview Report\n")
        user_overview_file.write(
            f"Generation Time : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} by {curr_user}\n"
        )
        user_overview_file.write(f"Number of all tasks : {count_of_task}\n")
        user_overview_file.write(f"Number of all users : {count_of_users}\n")
        user_overview_file.write(f"{task_tabulation()}")

    # print(user_tasks)


def task_tabulation():
    """
    Return tasks statistics table
    """
    # Convert task_list into data frame for calculation
    df_task = pd.DataFrame(task_list)

    # Convert username_password into data frame
    df_username_password = pd.DataFrame(
        list(username_password.items()), columns=["username", "password"]
    )

    # Merge task_list and username_password by using username as key
    df_merged = pd.merge(df_task, df_username_password, on="username", how="right")

    # Calculate the number of tasks assigned to each user and the number of complete
    user_tasks = df_merged.groupby("username")["completed"].agg(["count", "sum"])

    # Calculate the number of task assigned to each user
    user_tasks["assigned"] = round(((user_tasks["count"] / len(task_list)) * 100), 2)

    # Avoid division by zero error
    user_tasks["sum"] = user_tasks["sum"].astype(float)
    user_tasks["count"] = user_tasks["count"].astype(float)

    # Calculate completion rate
    user_tasks["completion_rate"] = (user_tasks["sum"] / user_tasks["count"]) * 100

    # Calculate the number of incomplete task but not overdue
    user_tasks["incomplete_rate"] = (
        (user_tasks["count"] - user_tasks["sum"]) / user_tasks["count"]
    ) * 100

    # Calculate the overdue tasks
    today = date.today()
    user_tasks["overdue"] = 0.0
    for user, group in df_merged.groupby("username"):
        overdue_tasks = sum(
            1
            for task in group.itertuples(index=False)
            if not task.completed and task.due_date.date() < today
        )
        user_tasks.loc[user, "overdue"] = overdue_tasks

    user_tasks["overdue_rate"] = user_tasks["overdue"] / user_tasks["count"] * 100

    # Tidy up for printing
    user_tasks["count"] = user_tasks["count"].astype("int")
    user_tasks["completion_rate"] = round(user_tasks["completion_rate"])
    user_tasks["incomplete_rate"] = round(user_tasks["incomplete_rate"])
    user_tasks["overdue_rate"] = round(user_tasks["overdue_rate"], 2)

    user_tasks["completion_rate"] = user_tasks["completion_rate"].fillna("N/A")
    user_tasks["incomplete_rate"] = user_tasks["incomplete_rate"].fillna("N/A")
    user_tasks["overdue_rate"] = user_tasks["overdue_rate"].fillna("N/A")

    user_tasks.rename(
        columns={
            "count": "Assigned",
            "assigned": "Assigned (%)",
            "completion_rate": "Completion (%)",
            "incomplete_rate": "Incomplete (%)",
            "overdue_rate": "Overdue (%)",
        },
        inplace=True,
    )

    columns_to_display = [
        "Assigned",
        "Assigned (%)",
        "Completion (%)",
        "Incomplete (%)",
        "Overdue (%)",
    ]

    return user_tasks[columns_to_display]


# Functions END

# ====Login Section====
"""This code reads usernames and password from the user.txt file to 
    allow a user to login.
"""


username_password = {}
read_users()

logged_in = False
while not logged_in:
    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


# Read contents from tasks.txt file
read_task_list()

while True:
    # presenting the menu to the user and
    # making sure that the user input is converted to lower case.
    print()
    menu = input(
        """Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: """
    ).lower()

    if menu == "r":
        reg_user()

    elif menu == "a":
        add_task()

    elif menu == "va":
        view_all()

    elif menu == "vm":
        view_mine()

    elif menu == "gr":
        generate_reports()

    elif menu == "ds" and curr_user == "admin":
        """If the user is an admin they can display statistics about number of users
            and tasks."""

        # Call read_users to get the most updated user list
        read_users()
        # Call read_task_list to get the most updated task list
        read_task_list()

        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")
        print(task_tabulation())

    elif menu == "e":
        print("Goodbye!!!")
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
