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

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

task1 = Task(
    name="Vacuum"
)


def add_task():
    session.add(task1)
    session.commit()

add_task()