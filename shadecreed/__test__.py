import sys,time,httpx
from shadecreed.core.storage.model import shadecrypt
from shadecreed.core.utils.base import base_dir
hello = 'hello'
hi = 'hello fry woman'

json={
  "name" : "shade",
  "age" : 62,
  "github" : "harkerbyte"
}

def send_json():
  response = httpx.request('POST',sys.argv[1],headers = {"content-type":"application/json"} ,json=json)
  response = httpx.request('POST',sys.argv[1],headers = {"content-type":"application/json"} ,json=json)
  print(response.status_code)
  print(response.json)