from flask import Flask, redirect, url_for, request, jsonify

app = Flask(__name__)

app = Flask('app')


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/wsjf', methods=['GET'])
def wsjf():
    # print(request.args)
    # exit()
    # wsjf = 2
    # return redirect(url_for('result', wsjf=wsjf))
    try: 
        v = int(request.args.get('v'))
        t = int(request.args.get('t'))
        r = int(request.args.get('r'))
        e = int(request.args.get('e'))
        wsjf = (v + t + r) / e
        return jsonify({'wsjf_score':  wsjf})
    except Exception as e:
        return "Missing an argument or another problem. Need v, t, r, and e. Should look like /wsjf?v=1&t=2&r=3&e=5"
    #return redirect(url_for('result', wsjf=wsjf))


@app.route('/result/<wsjf>')
def result(wsjf):
    return 'wsjf score: %s' % wsjf

app.run(host='0.0.0.0', port=8080)
