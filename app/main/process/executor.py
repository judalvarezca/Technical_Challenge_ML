from time import time
from concurrent.futures import ThreadPoolExecutor
from threading import Semaphore


class Executor():
    def __init__(self, threads, queue_size, finished_message) -> None:
        self.executor = ThreadPoolExecutor(threads)
        self.semaphore = Semaphore(queue_size)
        self.futures = []
        self.finished_message = finished_message

    def set_task(self, task, *args, **kwargs):
        print("Started process for set of data")
        self.semaphore.acquire()
        future = self.executor.submit(task, *args, **kwargs)
        future.add_done_callback(self.done_callback)
        self.futures.append(future)

    def done_callback(self, future):
        self.semaphore.release()
        print(self.finished_message)
