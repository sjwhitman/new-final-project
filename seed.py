import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server


os.system('dropdb tasks')
os.system('createdb tasks')

model.connect_to_db(server.app)
model.db.create_all()

user1 = model.User(
    username="codingWizard",
    email="codingWizard@gmail.com",
    password="notSecure51"
)

user2 = model.User(
    username="testuser3",
    email="testemail3@email.com",
    password="testpassword3"
)

model.db.session.add(user1)
model.db.session.add(user2)
model.db.session.commit()

task1 = model.Task(
    task_name="Vacuum",
    task_description="Clean those floors!",
    timer_type = "task",
    duration=(3600),
    user_id=1
)

model.db.session.add(task1)
model.db.session.commit()
