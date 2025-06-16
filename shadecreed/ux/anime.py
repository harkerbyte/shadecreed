import sys,time
from shadecreed.ux.ascii import width
green='\x1b[1;32m'
red='\x1b[1;31m'
yellow='\x1b[1;33m'
plain='\x1b[1;0m'

def wr(te,ti=0.0002,co=plain):
  sys.stdout.write(co)
  for ie in te:
    sys.stdout.write(ie)
    sys.stdout.flush()
    time.sleep(ti)
  sys.stdout.write(f'\n{plain}')
  
def wrdel(te,re,ti=0.005):
  for ie in te:
    sys.stdout.write(ie)
    sys.stdout.flush()
    time.sleep(ti)
  sys.stdout.write(f'\r')
  for e in range(len(re)):
    sys.stdout.write(f'\r{re[:e+1]}' + ' ' * (len(te)-e-1))
    sys.stdout.flush()
    time.sleep(ti)
  sys.stdout.write(f'\n')

def wrtime(te,ti=5,co=plain):
  sys.stdout.write(co)
  i=0
  while i <= ti:
    sys.stdout.write(f'{te} : {i}/{ti}\r')
    sys.stdout.flush()
    time.sleep(1)
    i+=1
  sys.stdout.write(f'{plain}\n')
  
def wrcold(te,ti=0.01,co=plain,timeout=1,reverse=False):
  sys.stdout.write(co)
  for ie in te:
    sys.stdout.write(ie)
    sys.stdout.flush()
    time.sleep(ti)
  time.sleep(timeout)
  if len(te) <= width:
    sys.stdout.write(f'\r' + ' ' * width + '\r')
    if reverse:
      sys.stdout.write(f'\x1b[1A' + ' ' * width + '\r')
  else:
    total = width // len(te)
    sys.stdout.write(f'\x1b[{total}A' + ' ' * width + '\r')
  sys.stdout.write(plain)
  
def wrloader(ti=5):
  sys.stdout.write('\r')
  for i in range(ti+1):
    sys.stdout.write(f'\r{green}' + ['.'][0] * i)
    time.sleep(1)
  sys.stdout.write(f'\r{plain}')
  
"""
def wrsplit(te,de,ti=0.003):
  for i in range(20):
    for t,d in zip(te,de):
      sys.stdout.write(f'\x1b[1;31m{t[:+i]}\x1b[1;0m' + '\n' if i == 10 else t)
      sys.stdout.write(' '+=i '|' if i == 10 + f'\x1b[1;33m{d[:+i]}\x1b[1;0m')
    
    sys.stdout.write('\n')
"""  
def wrcom(dictone, dicttwo, ti=0.005):
  if isinstance(dictone, dict) and isinstance(dicttwo, dict):
    for key in dicttwo.keys():
      if key in dictone.keys():
        val1 = dictone[key]
        val2 = dicttwo[key]
        if val1 != val2:
          sys.stdout.write(f'{key} : {yellow}{val2}{plain}')
        else:
          sys.stdout.write(f'{key} : {val2}')
      
      
      
def wrdic(dict_,co=plain,ti=0.002,mi=False):
  if isinstance(dict_,dict):
    for k, v in dict_.items():
      if mi:
        sys.stdout.write(f'{co}%s{plain} : %s\n'%(k,v[:20]))
      else:
        sys.stdout.write(f'{co}%s{plain} : %s\n'%(k,v))
      sys.stdout.flush()
      time.sleep(ti)
    sys.stdout.write(f'\n')
  else:
    wr(dict_)
if __name__=='__main__':
  wrdel('Not a standalone', 'Buzz off fam')