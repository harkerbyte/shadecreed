import time,threading
from shadecreed.ux.anime import wrcold
class taskSchedule:
  def __init__(self):
    self.func_queue = []
    self.queue_lock = threading.Lock()
    self.event_stop = threading.Event()
    self.worker = threading.Thread(target=self.run, daemon=True)
    
  def add_task(self,func,*args,**kwargs):
    with self.queue_lock:
      if callable(func):
        self.func_queue.append((func,args,kwargs))
        if not self.worker.is_alive():
          self.worker.start()
   
  def stop(self):
    self.event_stop.set()
    self.worker.join()
    
  def run(self):
    while True:
      while not self.event_stop.is_set():
        with self.queue_lock:
          if self.func_queue:
            task = self.func_queue.pop(0)
            if task:
              func,args,kwargs = task
              try:
                func(*args,**kwargs)
              except Exception as error:
                wrcold('Error encountered running %s -> %s'%(func.__name__,error),reverse=False)
          else:
            time.sleep(0.5)
            
        
if __name__ == '__main__':
  pass