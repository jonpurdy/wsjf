from flask import Flask, request, jsonify

import requests
import os
import json

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/wsjf', methods=['GET'])
def wsjf():
    try: 
        v = int(request.args.get('v'))
        t = int(request.args.get('t'))
        r = int(request.args.get('r'))
        e = int(request.args.get('e'))
        task_id = request.args.get('taskid')
        wsjf_score = (v + t + r) / e
        wsjf_score = round(wsjf_score, 2)
        #push("wsjf success: %s" % wsjf_score)

        asana_updated = "unknown"

        if request.args.get('taskid') is not None:
            try:
                update_asana_task(task_id, wsjf_score)
                asana_updated = "yes"
                print("Asana successfully updated.")
            except:
                print("Asana not updated.")
                asana_updated = "no"
        else:   
            asana_updated = "no task_id provided in args; didn't try"

        return jsonify({'wsjf_score':  wsjf_score, 'asana_updated': asana_updated})

        
    except Exception as e:
        #push("wsjf failed.")
        return "Missing an argument or another problem. Need v, t, r, and e. Should look like /wsjf?v=1&t=2&r=3&e=5"

    
def update_asana_task(task_id, wsjf_score):
    # https://app.asana.com/api/1.0/tasks/TASK_ID

    try:
        asana_token = os.environ['ASANA_TOKEN']
    except Exception as e:
        print(e)
        asana_token = '111222'

    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer %s' % asana_token,
    }

    data2 = '{"data": {"custom_fields": { "1202941379778435": "%s" } } }' % wsjf_score

    jsondata = json.loads(data2)

    url = "https://app.asana.com/api/1.0/tasks/%s" % task_id

    response = requests.put(url, headers=headers, data=data2)
    #print(response.text)
    print("asana response: %s" % response.code)


def push(message):
    print(os.environ['TOKEN'])
    url = "https://api.pushover.net/1/messages.json"
    r = requests.post(url, data = {
      "token": os.environ['TOKEN'],
      "user": os.environ['USER'],
      "message": "%s" % message
    })
    print(r.status_code)

# {
#   "data": {
#     "custom_fields": {
#       "4578152156": "Not Started",
#     }
#   }
# }

if __name__ == '__main__':
    app.run(debug=True)