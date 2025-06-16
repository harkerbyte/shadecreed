import os,sys,json,argparse,httpx
from shadecreed.core.utils.parse import Parse
from shadecreed.core.utils.build import analyzeHeaders
from shadecreed.ux.anime import wr,wrdic
from shadecreed.ux.ascii import payloadInject,payloadInjectQuit
from shadecreed.ux.process import processResponse
from shadecreed.core.headers.network.proxy import proxyParse
from shadecreed.core.utils.base import base_dir,onload_file,cache_dir

# Optional fuzz payloads for testing header injection
fuzz_payloads = ["true", "admin", "' OR '1'='1", "1", "localhost", "evil.com"]

def mainTarget():
  with open(f'{cache_dir}/cache.json', 'r') as pin:
    target = json.load(pin)
  return target['target']
  
memory = {
  'target' : mainTarget(),
  'method' : 'GET',
  'header' : f'{base_dir}/core/headers/map.json',
  'proxy' : None,
  'redirects' : True,
}
def runHeaderEditor():
  try:
    parse = argparse.ArgumentParser(description="shadecreedcreed : toolkit; header editor (HTTPs/HTTPsV2)")
    parse.add_argument('-u','--url',help="<target_url> to open, inject payloads i.e WHERE * SELECT user='victim'",required=True)
    parse.add_argument('-m','--method',default="GET",help="<method:GET> | <method:POST> ",choices=["GET","POST","PUT","DELETE"])
    parse.add_argument('-s','--header',help="custom header directory path : <custom_header>.json")
    parse.add_argument('-p','--proxy',help="custom proxy; <format> address:port - No authentication support in version 0.0.2")
    parse.add_argument('-r','--redirect',help="Provide flag if you intend to allow redirects")
    args = parse.parse_args()
    if args.url:
      memory['target'] = args.url
      memory['method'] = args.method if args.method is not None else 'GET'
      memory['proxy'] = args.proxy if args.proxy is not None and ':' in args.proxy else None
      memory['redirects'] = True if args.redirect is not None else False
      
      if args.header:
        memory['header'] = args.header
        if os.path.exists(args.header):
          headerEditor(target=args.url,method=memory['method'],custom=onload_file(memory['header']),proxy=memory['proxy'],allow_redirects=memory['redirects'])
        else:
          wr(f'{args.header} was not found')
      else:
        headerEditor(target=args.url,method=memory['method'],custom=onload_file(memory['header']),proxy=memory['proxy'],allow_redirects=memory['redirects'])
  
  except KeyboardInterrupt:
    pass
 
def headerEditor(target=None,method=None,custom=None,proxy=None,allow_redirects=None):
  wr(payloadInject())
  while True:
    parsed_cmds = input('> ').strip()
    if parsed_cmds.lower() == 'q':
      wr(payloadInjectQuit())
      break
    elif parsed_cmds.lower() == 'headers':
      wrdic(onload_file(memory['header']),ti=0.005)
    elif parsed_cmds.lower() == 'cheaders':
      wrdic(onload_file(memory['header']))
    elif 'del' in parsed_cmds.lower():
      del_parsed = Parse(onload_file(memory['header']),parsed_cmds)
      finished_del = del_parsed.parse()
      with open(memory['header'], 'w') as deleted:
        json.dump(finished_del,deleted,indent=2)
      modRun(target=memory['target'],method=memory['method'],header=custom if custom is not None else finished_del,proxy=memory['proxy'])
    else:
      instance = Parse(onload_file(memory['header']),parsed_cmds)
      payload = instance.parse()
      save_to = memory['header']
      init_headers = onload_file(save_to)
      with open(save_to, 'w') as rewrite:
        init_headers.update(payload)
        json.dump(init_headers,rewrite,indent=2)
        
      modRun(target=memory['target'],method=memory['method'],header=custom if custom is not None else payload,proxy=memory['proxy'])
    
    
def modRun(target=None,method=None,header=None,proxy=None):
  
  response = httpx.request(method,target,headers=header,proxy=proxyParse(proxy),follow_redirects=memory['redirects'])
  analyzeHeaders(dict(response.headers))
  processResponse(response)
   
  
if __name__=='__main__':
  pass