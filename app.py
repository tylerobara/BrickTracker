from flask import Flask, request, jsonify, render_template
import json
from pprint import pprint as pp
app = Flask(__name__)

tmp = '71386-10'

@app.route('/')
def index():
    with open('./sets/'+tmp+'/info.json') as info:
          info_file = json.loads(info.read())
    with open('./sets/'+tmp+'/inventory.json') as inventory:
          inventory_file = json.loads(inventory.read())
    with open('./info/'+tmp+'.json') as info:
          json_file = json.loads(info.read())
    pp(json_file['unit'][0]['bricks']['missing'])
    return render_template('bootstrap_table.html', title=info_file['set_num']+" - "+info_file['name'],
                           info_file=info_file,inventory_file=inventory_file,json_file=json_file)
           
    #return render_template('index.html') 

#'Welcome to the Flask App'


@app.route('/saveNumber', methods=['POST'])
def save_number():
    data1 = request.form.get('brick.part.part_num')
    data2 = request.form.get('brick.color.name')
    number = request.form.get('numberInput')

    if number is not None:

        print(data1)
        print(data2)
        print(number)

        with open('./info/'+tmp+'.json') as info:
            json_file = json.loads(info.read())
        print(json_file['count'])

        data = '{"brick" : {"ID":"' + data1 + '","color_name": "' + data2 + '","amount":"' + number + '"}}'
        print(data)
        print(json.loads(data))

        json_file['unit'][0]['bricks']['missing'].append(json.loads(data))
        print(json_file['unit'][0]['bricks'])
        # Save number to JSON file
        with open('./info/'+tmp+'.json', 'w') as dump_file:
            json.dump(json_file,dump_file)
    
    return  ('', 204)

if __name__ == '__main__':
    app.run(host='192.168.10.109', debug=True, port=3333)
