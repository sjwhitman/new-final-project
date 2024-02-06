from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Task(db.Model):
    __tablename__ = "tasks"

    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_name = db.Column(db.String(50), nullable=False)
    task_description = db.Column(db.String(200))
    timer_type = db.Column(db.String(10)) # 'break' or 'task'
    duration = db.Column(db.Integer) #stored in seconds
    timer_number = db.Column(db.Integer, nullable = True) # number of timer cycles for a task
    user_id = db.Column(db.Integer(), db.ForeignKey('users.user_id'))
    user = db.relationship('User', back_populates="tasks")

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    theme_preference = db.Column(db.String(10))
    work_session_time = db.Column(db.Integer)
    break_session_time = db.Column(db.Integer)
    # work_time_interval = db.Column(db.Integer)
    # break_time_interval = db.Column(db.Integer)

    tasks = db.relationship('Task', back_populates='user')



def connect_to_db(flask_app, db_uri="postgresql:///tasks", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")



if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    db.create_all()



# def calculate_timer(start_time,end_time):
#     #function to calculate start and end time as seconds
#     time_difference = end_time - start_time
#     return int(time_difference.total_seconds())

# print(calculate_timer(datetime(2022, 1, 1, 12, 0, 0),datetime(2022, 1, 1, 12, 30, 0)))
