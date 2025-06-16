import sys,httpx,argparse
from bs4 import BeautifulSoup as bs
from shadecreed.ux.anime import wr,wrdic,wrdel
from shadecreed.ux.ascii import red,blue,yellow,green,plain
from shadecreed.ux.process import processResponse
from shadecreed.core.utils.build import buildConfig

assist = f"""

\033[1;44mAUTOMATE INPUT FIELDS INTERACTIONS\033[1;0m

[+] Add input fields by their placeholder text

    • Single Placeholder:
        → Type: placeholder

    • Multiple Placeholders (comma-separated):
        → Type: placeholder1, placeholder2, placeholder3

[!] Use exact placeholder text as it appears in the input \nfield
[!] Type `all` to retrieve all inputs with placeholder
[!] Type `done` to proceed further
[!] Type `{red}q{plain}` to exit.
──────────────────────────────────────────────────
"""
closed = f"""
CLOSED INPUT FIELDS AUTOMATION
"""
findsubmit=f"""
Now...Let\'s Proceed To Find The Submit Button
"""
def findInputs(document):
  retrieved = list()
  if document.find_all('input'):
    for found in document.find_all('input', attrs ={'placeholder' : True}):
      retrieved.append(found)
    
    return retrieved
  else:
    wr('There are no input field with placeholder')
  
def retrieveForm(form,target):
  elements = ['div','p','a','b','button']
  drop = list()
  for each in elements:
    drop.extend(form.find_all(each, string=target))
  wr(drop,ti=0.001)
    
    
def findSubmit(document,placeholders):
  wr(f'Retrieved inputs by placeholder : {yellow}{[item.get('placeholder') for item in placeholders]}{plain}', ti=0.0002)
  findbutton = True
  while findbutton:
    button,extracted = list(), []
    placeholders = list(placeholders)
    wr(findsubmit)
    target_form = placeholders[0].find_parent('form')
    sub_button = target_form.find('button', attrs={'type':'submit'}) or target_form.find('input', attrs={'type':'submit'})
    if sub_button:
      button.append(sub_button)
    else:
      while True:
        in_text = input('Type the submission `button` displayed text : ').strip()
        if in_text.lower() == 'q':
          button.clear()
          break
        elif in_text.lower().startswith('assist-'):
          if '-' in in_text:
            com, target = in_text.split('-')
            retrieveForm(target_form,target)
        else:
          sub_input = target_form.find('input', attrs={'value': in_text}) or target_form.find('input',attrs={'type':'submit'}) 
          if sub_input:
            button.append(sub_input)
            break
          else:
            sub_link = target_form.find('a', string=in_text)
            button.append(sub_link)
            break
    try:
      if button:
        wr(f'Type `{yellow}select{plain}` on which button submits the form \nType `{red}q{plain}` for previous')
        for extra in button:
          it_is = input(f'{str(extra.text if str(extra.text).strip() != "" else "🔍").strip()} : ').strip()
          if it_is.lower() == 'select':
            extracted.append(extra)
            buildConfig([text.get('placeholder') for text in placeholders],[str(extracted[0].text) if str(extracted[0].text).strip() != "" else "TgEnter"],str(extracted[0].parent.name))
          elif it_is.lower() == 'q':
            extracted.clear()
            findbutton = False
      else:
        wr('Submit button/link extraction... Failed')
    except Exception as error:
      print(error)
        

def runStartAssembling():
  parse = argparse.ArgumentParser(description="shadecreed toolkit : admin page custom brute force; this tool is in beta version and as of version 0.0.4 : it can only make 10 password attempts")
  parse.add_argument('-u','--url',help="<target_url> make sure that a form exists on the provided page url.")
  parse.add_argument('-r','--redirect', help="provide this flag if you intend to allow redirection.")
  args = parse.parse_args()
  
  if args.url:
    startAssembling(url=args.url,redirects=True if args.redirect is not None else False)
    
def startAssembling(document=None,parser='html.parser',url=None,redirects=None):
  if url != None:
    response = httpx.request('GET', url,follow_redirects=redirects if redirects is not None else False)
    if response.status_code != 200:
      processResponse(response)
      
      wr("provide '--redirect true' flag, if this issue persists",co='\x1b[1;31m')
      sys.exit()
    
    fdocument = response.text
  text = bs(fdocument if url is not None else document, parser)
  inputs = set()
  if text.find_all('form'):
    if text.find_all('input'):
      wr(assist)
      while True:
        placeholders = input('> ').strip()
        if placeholders.lower() == 'q':
          wr(closed)
          break
                
        elif placeholders.lower() == 'all':
          all_ = findInputs(text)
          if all_:
            for each in all_:
              wr(f'[+] Placeholder : {each.get('placeholder')}')
        elif placeholders.lower() == 'done':
          if inputs:
            findSubmit(text,inputs)
          else:
            wr('[+] You haven\'t added any inputs yet')
        else:
          if ',' in placeholders:
            for placeholder in placeholders.split(','):
              seen = text.find('input', attrs ={'placeholder' : placeholder.strip()})
              if seen:
                inputs.add(seen)
              else:
                wr(f'{placeholder.strip()} not found')
          else:
            seen = text.find('input', attrs ={'placeholder' : placeholders.strip()})
            if seen:
              inputs.add(seen)
              
            else:
              wr(f'[-] {placeholders}` not found')
  
