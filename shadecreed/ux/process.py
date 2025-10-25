import re,os,json,threading,datetime
from bs4 import BeautifulSoup as bs
from shadecreed.ux.anime import wr,wrdic,wrcold,twtable,trptable
from shadecreed.core.headers.network.proxy import readCache
from shadecreed.core.utils.base import base_dir,cache_dir,stream_dir,onload_file,define_status,streamStorage,processStorage
from shadecreed.core.utils.base import cacheStorage

key_headers = ['Location', 'Set-Cookie', 'Content-Security-Policy', 'Access-Control-Allow-Origin']

def skim(target):
  if target.startswith('http'):
    try:
      host, end = target.split('.',1)
      proto, dns = host.split('//',1)
      return dns
    except Exception:
      return None
      
def processResponse(response):
  cache = readCache()
  custom_headers = cacheStorage.export_dict()
  available = dict()
  if response.status_code:
    available['[+] Status code'] = f'{response.status_code} ~ {define_status(response.status_code)}'
  if response.encoding:
    available['[+] Encoding'] = response.encoding
  if response.elapsed:
    available['[+] Elapsed time'] = response.elapsed  
  if response.url:
    available['[+] Final url'] = response.url
  if response.history:
    available['[+] Status history'] = [x.status_code for x in response.history]
  if response.cookies:
    available['[+] Cookies'] = response.cookies
  if response.content:
    available['[+] Content (byte)'] = len(response.content)
    #if len(response.content) < int(cache['content-size']):
     # wr('[+] Noticeable change in content size ✅')
      #ask = input('[+] Would you like to observe this `Yes/No`: ')
     # if ask.lower() == 'yes':
     #   content = readCache(content=True)
      #  wr(response.text[:300],ti=0.0005)
    #  else:
       # pass
  try:
    if custom_headers['host'] in response.text:
      wr(f'{cache['host']} spotted in page body')
  except Exception:
    pass
  
  for key in response.headers:
    if key in key_headers:
      available[key] = value
      
  wrdic(available)
  
def processContent(response,saveTo):
  use_cache = readCache()
  if 'html' in use_cache['content-type']:
    html = bs(response.text, 'html.parser')
   # wr(f'[+] Page content type : {use_cache['content-type']} 📜')
    if saveTo:
      with open(saveTo,'w') as save:
        save.write(html.prettify())
        save.close()
      
  else:
  #  wr(f'[+] Page content type : {use_cache['content-type']} 📜')
 # wr(f'[+] Page elapsed time : {use_cache['elapsed-time']} ⌛')
  #wr(f'[+] Page content size (byte) : {len(response.content)} 📜')
     pass
  
def is_parent_to(form, inputs):
  count = sum(1 for input_ in inputs if input_.parent == form)
  return int(count)

def hints(text):
  wr(text.strip())
  
def analyzePageContent(response):
  inputs = list()
  hidden = list()
  if response:
    responsedict = {k.lower():v for k,v in dict(response.headers).items()}
    processResponse(response)
    nice_page = bs(response.text, 'html.parser')
    HIDDEN = nice_page.find_all('input', attrs = {'type':'hidden'})
    if HIDDEN:
      for each in HIDDEN:
        hidden.append(each)
    INPUTS = nice_page.find_all('input')
    if INPUTS:
      for each in INPUTS:
        inputs.append(each)
    
    if len(hidden) >= 1:
      wr(f'Hidden input fields : {len(hidden)}',co='\x1b[1;36m')
      wr('Names : '+ ', '.join(str(e.get('name')).strip() for e in hidden if e != "None" ))
    
    if len(inputs) >= 1:
      wr(f'Visible input fields : {len(inputs)}',co='\x1b[1;36m')
      wr('Names : ' + ', '.join(str(e.get('name')).strip() for e in inputs if e != "None" ))
    print('\n')
    form = nice_page.find('form')
    if form:
      overal = inputs + hidden
      fifty = len(overal) // 2
      if is_parent_to(form,overal) >= int(fifty) - 2:
        form_method = form.get('method')
        form_action = form.get('action')
        if form_method:
          hints(f'Form method : {form_method}')
          if form_action:
            hints(f'Form action/target : {form_action}')
        if  form_method == 'get':
          content_type = responsedict.get('content-type','')
          if content_type != "":
            if 'html' in content_type and form_method == 'get':
              hints('Possible xss : reflective and DOM')
            elif form_method != 'get':
              csp = responsedict.get("content-security-policy","")
              if "'unsafe-inline'" or "'unsafe-eval'" in csp:
                hints('Possible xss : stored and DOM')
    
    url = response.url
    if url:
      domain = str(url).split('//')[-1:]
      address,*query_segments = domain[0].split('/')
      unescaped = []
      if len(query_segments) > 0:
        for query in query_segments:
          cleaned = query.strip()
          if cleaned:
            element = nice_page.find(text=cleaned)
            if element:
              unescaped.append(element)
        if unescaped:
          hints('Sql-injection via URL parameters seem possible')
          #for clue in unescaped:
           # wr(f'clue : /{clue.strip()}',co='\x1b[1;33m')
         
    connection = responsedict.get("connection","")
    if connection.strip() == "close" and form:
      scpt = form.find('script')
      if form.get('method') not in ['get','post'] and scpt:
        quest = input('\x1b[1;36mFurther observe the page\'s form, does the page reload on submission [ Yes/No ] : '+'\x1b[1;0m').strip()
        wrcold('',reverse=True if quest else False)
        if quest.lower() in ['yes','y']:
          hint('Try `sql-injection` on page inputs and headers')
        elif quest.lower() in ['no','n']:
          hints('Recommends posting data in json format')
        
    
class streamData:
  def __init__(self,data,streamed=None):
    self.data = data if isinstance(data, dict) else dict(data)
    self.streamed = streamed if streamed != None else dict()
    self.keep_alive = None
    self.process()
      
  def process(self):
    if os.path.exists(f'{base_dir}/core/middleware/process.scdb'):
      status = processStorage.export_dict()
      self.keep_alive = status['keep-alive']
    else:
       self.keep_alive = False
      
  def streaming(self):
    if isinstance(self.data, dict):
      for key, value in self.data.items():
        self.streamed[key] = value
        if self.keep_alive:
          wr('%s : %s'%(key, value))
      streamStorage.update((self.data['ip'],self.data),unique=False)
      
    