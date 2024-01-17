from sqlalchemy import create_engine,Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

url = URL.create(
    drivername='postgresql',
    database='tasks',
    host='localhost',
    username='dickatiel',
)

engine = create_engine(url)
connection = engine.connect()

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    task_description = Column(String(200))
    duration_in_seconds = Column(Integer)

class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(200, nullable = False))
    theme_preference = Column(String(10))
    work_session_time = Column(Integer)
    break_session_time = Column(Integer)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

task1 = Task(
    name="Vacuum"
)


def add_task(name):
    new_task = Task(name=name)
    # session.add(task1)
    session.add(new_task)
    session.commit()

def get_tasks():
    return session.query(Task).all()

def update_task(task_id, new_task_name):
    task = session.query(Task).filter_by(task_id=task_id).first()
    task.name = new_task_name
    session.commit()

def delete_task(task_id):
    task = session.query(Task).filter_by(task_id=task_id).first()
    session.delete(task)
    session.commit()

# update_task(1,"Sweep")
