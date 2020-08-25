import time

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker


from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from db.models import Base, User, Queue, Post


engine = create_engine('postgres+psycopg2://tweeter:tweeter@localhost:5432/tweeter')

Session = sessionmaker(bind=engine)
s = Session()

user = User(
    username='germain'
)
s.add(user)
queue = Queue(
    name='My First queue',
    cron='* * * * *',
    user_id=1
)
s.add(queue)
queue = Queue(
    name='Another queue',
    cron='*/3 * * * *',
    user_id=1
)
s.add(queue)
post = Post(
    title='My first post',
    message='Message in the bottle',
    queue_id=1
)
s.add(post)
post = Post(
    title='Another post',
    message='Another message in the bottle',
    queue_id=1
)
s.add(post)
s.commit()

