import time

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.sql import select, and_, or_
from sqlalchemy.orm import sessionmaker


from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from db.models import Base, User, Queue, Post

# Database init
engine = create_engine('postgres+psycopg2://tweeter:tweeter@localhost:5432/tweeter')
conn = engine.connect()
Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def scheduledPublishTwitter(user_id, queue_id):
    print(user_id, queue_id)
    posts_data = s.query(Post).filter(
        Post.queue_id == queue_id
    )
    for post in posts_data:
        print("  ", post.id, post.message)



if __name__ == '__main__':


    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    #Session = sessionmaker(bind=engine)
    #s = Session()

    import db.populate

    # Scheduler init
    executors = {
        'default': ThreadPoolExecutor(1),
        'processpool': ProcessPoolExecutor(1)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 1
    }


    scheduler = BackgroundScheduler(
        executors=executors,
        job_defaults=job_defaults
    )
    scheduler.start()

    with session_scope() as s:
      while True:
        data_queues = s.query(Queue)

        for queue in data_queues:
            queue_cron = queue.cron.split(" ")

            print(queue.id, queue.name)
            scheduler.add_job(
                    scheduledPublishTwitter,
                    args=(queue.user_id, queue.id),
                    trigger='cron',
                    id=str(queue.id),
                    second=queue_cron[0],
                    minute=queue_cron[1],
                    hour=queue_cron[2],
                    replace_existing=True,
                    misfire_grace_time=5
            )


        time.sleep(10)
