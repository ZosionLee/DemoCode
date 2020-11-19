import time

import random

from kazoo.client import KazooClient
import sys
import logging
import uuid
import threading


def logger():
    logging.basicConfig(
        level=logging.DEBUG,
        stream=sys.stdout,
        format='%(asctime)s %(pathname)s %(funcName)s%(lineno)d %(levelname)s: %(message)s'
    )
    return logging.getLogger()

class Zookeeper(object):

    @classmethod
    def crud(cls):
        zk = KazooClient(hosts='127.0.0.1:2182')
        zk.start()
        zk.delete('/crud',recursive=True)
        zk.ensure_path('/crud')
        if zk.exists('/crud'):
            print('path exists')
        zk.create('/crud/node1',b'this is a dummy data one')
        zk.create('/crud/node2', b'this is a dummy data two')

        data, stat = zk.get('/crud/node1')
        print(f'Version:{stat.version},data:{data.decode("utf-8")}')
        data, stat = zk.get('/crud/node2')
        print(f'Version:{stat.version},data:{data.decode("utf-8")}')
        children = zk.get_children('/crud')
        print(children)
        zk.stop()

    @classmethod
    def monitor(cls):

        def worker():
            zk = KazooClient(hosts='127.0.0.1:2182')
            zk.start()
            zk.ensure_path('/failure')
            zk.create('/failure/worker',value=b'value', ephemeral=True)
            for _ in range(10):
                print('I am alive')
                time.sleep(1)
            zk.stop()

        def watcher():
            zk = KazooClient(hosts='127.0.0.1:2182')
            zk.start()
            time.sleep(1)
            while True:
                if zk.exists('/failure/worker'):
                    print('Worker alive')
                else:
                    print('Worker goes down')
                    break
                time.sleep(1)
            zk.stop()

        t1 = threading.Thread(target=worker)
        t2 = threading.Thread(target=watcher)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    @classmethod
    def election(cls):

        def leader(t):

            def func():
                print(f'leader:{myid}')
                for _ in range(t):
                    print(f'{myid} is working')
                    time.sleep(1)

            myid=uuid.uuid4().hex
            zk = KazooClient(hosts='127.0.0.1:2182')
            zk.start()
            election = zk.Election('/election')
            election.run(func)
            zk.stop()

        t1 = threading.Thread(target=leader,args=(5,))
        t2 = threading.Thread(target=leader, args=(10,))
        t3 = threading.Thread(target=leader, args=(15,))
        t1.start()
        t2.start()
        t3.start()

    @classmethod
    def lock(cls):

        def task(num):
            myid = uuid.uuid4().hex
            print(f'I am {myid}')
            zk = KazooClient(hosts='127.0.0.1:2182')
            zk.start()
            lock = zk.Lock('/lock', myid)
            def do():
                print(f'{myid} is processing')
            with lock:
                for _ in range(num):
                    do()
                    time.sleep(1)
            zk.stop()

        t1 = threading.Thread(target=task, args=(1,))
        t2 = threading.Thread(target=task, args=(2,))
        t3 = threading.Thread(target=task, args=(3,))
        t1.start()
        t2.start()
        t3.start()

    @classmethod
    def watch(cls):

        def server():
            zk = KazooClient(hosts='127.0.0.1:2182')
            zk.start()
            myid=uuid.uuid4().hex
            @zk.DataWatch('/watch/config')
            def my_func(data, stat):
                if data:
                    print(f'[ID:{myid}]data is {data} and version is {stat.version}')
                else:
                    print('data is not available')

            while True:
                time.sleep(1)

        def config():
            zk = KazooClient(hosts='127.0.0.1:2182')
            zk.start()
            zk.ensure_path('/watch')
            for i in range(3):
                zk.set('/watch/config',f'config {i}'.encode())
                time.sleep(1)
            zk.stop()

        ts=[threading.Thread(target=server) for _ in range(3)]
        tc=threading.Thread(target=config)
        tc.start()
        for t in ts:
            t.start()

    @classmethod
    def queue(cls):

        def producer():
            zk = KazooClient(hosts='127.0.0.1:2182')
            zk.start()
            q=zk.Queue('/queue')
            while True:
                num=random.randint(0,100)
                print(f'put {num} in queue')
                q.put(str(num).encode())
                time.sleep(1)

        def consumer():
            zk = KazooClient(hosts='127.0.0.1:2182')
            zk.start()
            q = zk.Queue('/queue')
            while True:
                print(f'get {q.get()} from queue')
                time.sleep(1)

        t1=threading.Thread(target=producer)
        t2=threading.Thread(target=consumer)
        t1.start()
        t2.start()

    @classmethod
    def count(cls):

        def worker():
            myid=uuid.uuid4().hex
            zk = KazooClient(hosts='127.0.0.1:2182')
            zk.start()
            c= zk.Counter('/count')
            while True:
                c+=1
                print(f'[ID:{myid}]pre_value:{c.pre_value},post_value:{c.post_value}')
                time.sleep(1)

        ts=[threading.Thread(target=worker) for _ in range(3)]
        for t in ts:
            t.start()


if __name__ == '__main__':
    Zookeeper.count()