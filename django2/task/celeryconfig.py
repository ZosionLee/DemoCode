# * coding:utf-8 *
# Author: ZosionLee

import celery
from kombu import Exchange, Queue

from django2.celery import settings

app = celery.Celery('django2.celery')
app.config_from_object('django2.celery.settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.broker_transport_options = {
    'max_retries': 3,
    'interval_start': 0,
    'interval_step': 0.2,
    'interval_max': 0.2,
}


# define exchange
default_exchange = Exchange('default',type='direct')

# define queues
default_queue = Queue('default',default_exchange,routing_key='default')
message1 = Queue('message1',default_exchange,routing_key='message1')
message2 = Queue('message2',default_exchange,routing_key='message2')
queue1 = Queue('queue1', default_exchange, routing_key='queue1')
queue2 = Queue('queue2', default_exchange, routing_key='queue2')
queue3 = Queue('queue3', default_exchange, routing_key='queue3')


app.conf.task_queues = (
    default_queue,
    queue1,
    queue2,
    queue3,
    message1,
    message2
)

class RouterConst(object):

    Name = 'report'
    Mappings = {
        0: 'queue1',
        1: 'queue2',
        2: 'queue3',
    }

class TaskRouter:
    def route_for_task(self, *args, **kwargs):
        if self ==RouterConst.Name:
            id_ = kwargs.get('id', None)
            if not id_:
                for arg in args:
                    if isinstance(arg, tuple) and arg:
                        id_ = arg[0]
                    elif isinstance(arg, dict):
                        id_ = arg.get('id', None)
                    else:
                        id_ = None
                if not id_:
                    raise ValueError('Can`t find id')
            queue_name = RouterConst.Mappings.get(hash(id_) % 3, None)
            if not queue_name:
                return None
            return {'queue': queue_name}




app.conf.task_default_queue = 'default'
app.conf.task_default_exchange = 'default'
app.conf.task_default_routing_key = 'default'
app.conf.task_routes = (TaskRouter,)

