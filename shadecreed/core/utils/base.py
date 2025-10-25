import os,sys,json,argparse
from pathlib import Path
from shadecreed.ux.anime import wr,wrdic
from shadeDB.core import shadeDB
from shadecreed.core.middleware.schedule import taskSchedule

required_modules = [
  'beautifulsoup4',
  'jinja2',
  'httpx',
  'html5lib'
  ]
schedule = taskSchedule()

#Fixed dirs
navigate = Path.home()
home = navigate / ".shadecreed"
stream = home / "logs" / "xss"
home_dir = f"{navigate}/.shadecreed"
stream_dir = f"{home_dir}/logs/xss"

#Temp dirs
base_dir = Path(__file__).resolve().parents[2]
cache_dir = base_dir / 'cache'
password_dir = base_dir / 'path'

#Storage instances
cacheStorage = shadeDB(f'{cache_dir}/cache.scdb',write=True,silent=True)
mapStorage = shadeDB(f'{base_dir}/core/headers/map.scdb',write=True,silent=True)  
recordStorage = shadeDB(f'{home_dir}/logs/statistics.scdb',write=True,silent=True)
processStorage = shadeDB(f'{base_dir}/core/middleware/process.scdb',write=True,silent=True)
streamStorage = shadeDB(f'{stream_dir}/streamed.scdb',write=True,silent=True)

def onload_file(onload):
  if os.path.isfile(onload):
    if '/' in onload:
      target = onload.split('/')[-1:]
      file = target[0]
    name, ext = os.path.splitext(file)
    if ext == '.json':
      with open(onload, 'r') as loaded:
        try:
          return json.load(loaded)
        except Exception as error:
          print(error)
          return dict()
    else:
      wr(f'{file.split('/')[-1:]} carries an invalid extension for a json document')
      sys.exit()
  else:
    raise FileNotFoundError(f'{onload} was not found')

  
"""    
def readXssLog():
  parse = argparse.ArgumentParser(description="Read xss captured datas")
  parse.add_argument('-r','--read',help="Provide the number of recent datas to display - LIFO")
  args = parse.parse_args()
  
  if os.path.exists(stream_dir / 'streamed.json'):
    retrieved = onload_file(stream_dir / 'streamed.json')
    if args.read and args.read >= 1:
      Lifo = retrieved.items()[-args.read:]
    else:
      Lifo = retrieved.items()[-5:]
      
    wrdic(Lifo)
  else:
    wr(f'There are no existing log')
"""

def define_status(code):
  statusBox = {
    100: "Continue",
    101: "Switching Protocols",
    102: "Processing",
    200: "OK",
    201: "Created",
    202: "Accepted",
    203: "Non-Authoritative Information",
    204: "No Content",
    205: "Reset Content",
    206: "Partial Content",
    207: "Multi-Status",
    300: "Multiple Choices",
    301: "Moved Permanently",
    302: "Found",
    303: "See Other",
    304: "Not Modified",
    305: "Use Proxy",
    307: "Temporary Redirect",
    308: "Permanent Redirect",
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required",
    408: "Request Timeout",
    409: "Conflict",
    410: "Gone",
    411: "Length Required",
    412: "Precondition Failed",
    413: "Payload Too Large",
    414: "URI Too Long",
    415: "Unsupported Media Type",
    416: "Range Not Satisfiable",
    417: "Expectation Failed",
    418: "I'm a teapot",
    422: "Unprocessable Entity",
    425: "Too Early",
    426: "Upgrade Required",
    428: "Precondition Required",
    429: "Too Many Requests",
    431: "Request Header Fields Too Large",
    451: "Unavailable For Legal Reasons",
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
    505: "HTTP Version Not Supported",
    506: "Variant Also Negotiates",
    507: "Insufficient Storage",
    508: "Loop Detected",
    510: "Not Extended",
    511: "Network Authentication Required"
  }
  return statusBox.get(code, 'Not defined')
      
      
def calculate_age(cache):
  for each in cache.split(','):
    each = each.strip()
    if 'max-age' in each:
      key,value = each.split('=')
      return int(value) // 60
 
def write_statistics():
  if not os.path.exists(f"{home_dir}/logs/statistics.scdb"):
    format_ = {
      'scans' : 0,
      'header_injections' : 0,
      'sql_executed' : 0,
      'payloads_deployed' : 0
    }
    recordStorage.import_dict(format_)
    
def record(scan=None,header=None,sql=None,payload=None):
  if os.path.exists(f'{home_dir}/logs/statistics.scdb'):
    record = recordStorage.export_dict()
    if scan:
      record['scans'] = int(record.get('scans',0)) + 1
    if header:
      record['header_injections'] = int(record.get('header_injections',0)) + 1
    if sql:
      record['sql_executed'] = int(record.get('sql_executed',0)) + 1
    if payload:
      record['payloads_deployed'] = int(record.get('payloads_deployed',0)) + 1
      
    recordStorage.import_dict(record,overwrite=True)
  else:
    write_statistics()
    
def statistics():
  wrdic(recordStorage.export_dict(),co='\x1b[1;32m')

if __name__ == "__main__":
  pass