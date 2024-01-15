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

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer(), primary_key=True)
    slug = Column(String(100), nullable=False, unique=True)
    title = Column(String(100), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    content = Column(Text)
    # author_id = Column(Integer(), ForeignKey('authors.id'))

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

article1 = Article(
    slug="clean-python",
    title="How to Write Clean Python",
    content="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
)


def add_task():
    session.add(article1)
    session.commit()

add_task()