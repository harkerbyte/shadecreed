import time,threading
from shadecreed.ux.anime import wrcold
class taskSchedule:
  def __init__(self):
    self.copied = []
    self.func_queue = []
    self.running = True
    self.queue_lock = threading.Lock()
    self.event_stop = threading.Event()
    self.worker = threading.Thread(target=self.run, daemon=True)
    self.worker.start()
    
  def add_task(self,func,*args,**kwargs):
    with self.queue_lock:
      if callable(func):
        self.func_queue.append((func,args,kwargs))
        
  def stop(self):
    self.running = False
    self.event_stop.set()
    self.worker.join()
    
  def run(self):
    while self.running:
      if self.event_stop.is_set():
        break
      task = None
      with self.queue_lock:
        if self.func_queue:
            task = self.func_queue.pop(0)
      if task:
        func, args, kwargs = task
        try:
          func(*args,**kwargs)
        except Exception as error:
          print(f'\x1b[1;33mError\x1b[1;0m Running {func.__name__} : {error}')
      else:
        time.sleep(0.5)
          
            
        
if __name__ == '__main__':
  pass