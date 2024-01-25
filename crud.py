from model import User, Task, db, connect_to_db
from flask import Flask, current_app

# CRUD for tasks table
def add_task(task_name):
    new_task = Task(task_name=task_name)
    db.session.add(new_task)
    db.session.commit()

def get_tasks():
    return Task.query.all()

def update_task(task_id, new_task_name):
    task = Task.query.get(task_id)
    task.task_name = new_task_name
    db.session.commit()

def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()

# CRUD functionality for users table
def add_user(username, email, password, theme_preference, work_session_time, break_session_time):
    existing_user = User.query.filter_by(email=email).first()
    # if existing_user:
    #     return "User already exists in db"
    # else:
    new_user = User(username=username, email=email, password=password, theme_preference=theme_preference, work_session_time=work_session_time, break_session_time=break_session_time)
    db.session.add(new_user)
    db.session.commit()

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

# print(get_user_by_email("codingWizard@gmail.com"))
# print(add_user("sqlSorcerer", "sqlsorcerer@microsoft.com", "love2Query"))

if __name__ == "__main__":
    from server import app
    connect_to_db(app)




