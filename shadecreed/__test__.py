import sys,time,httpx
hello = 'hello'
hi = 'hello fry woman'

json={
  "name" : "shade",
  "age" : 62,
  "github" : "harkerbyte"
}

def send_json():
  response = httpx.request('POST',sys.argv[1],headers = {"content-type":"application/json"} ,json=json)
  print(response.status_code)
  print(response.json)
  
if __name__=='__main__':
  pass