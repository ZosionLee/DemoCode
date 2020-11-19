# * coding:utf-8 *
# Author: ZosionLee

from celery.schedules import crontab

from task.celeryconfig import app


@app.task(queue='message1')
def eat_fruit(fruit):
    print(f'[Eat fruit] {fruit}')

@app.task(queue='message2')
def eat_vegetable(vegetable):
    print(f'[Eat vegetable] {vegetable}')


@app.task(name='report')
def report(id,msg):
    print(f'[Report] {id}:{msg}')


@app.task(queue='default')
def periodic_one():
    print('This is periodic one')


@app.task(queue='default')
def periodic_two():
    print('This is periodic two')

app.conf.update(
    timezone='UTC',
    enable_utc=True,
    beat_schedule={
        'beat_one': {
            'task': 'task.tasks.periodic_one',
            'schedule': crontab(minute='*'),
            'options': {'routing_key': 'default'}
        },
        'beat_two': {
            'task': 'task.tasks.periodic_two',
            'schedule': crontab(minute='*/5'),
            'options': {'routing_key': 'default'}
        },
    }
)
