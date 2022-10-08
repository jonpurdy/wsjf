from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/wsjf', methods=['GET'])
def wsjf():
    # print(request.args)
    # exit()
    # wsjf = 2
    # return redirect(url_for('result', wsjf=wsjf))
    print(__name__)
    try: 
        v = int(request.args.get('v'))
        t = int(request.args.get('t'))
        r = int(request.args.get('r'))
        e = int(request.args.get('e'))
        wsjf = (v + t + r) / e
        wsjf = round(wsjf, 2)
        push("wsjf success: %s" % wsjf)
        return jsonify({'wsjf_score':  wsjf})
        
    except Exception as e:
        push("wsjf failed. args: " % str(request.args))
        return "Missing an argument or another problem. Need v, t, r, and e. Should look like /wsjf?v=1&t=2&r=3&e=5"

def push(message):
    import requests
    url = "https://api.pushover.net/1/messages.json"
    r = requests.post(url, data = {
      "token": "",
      "user": "",
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