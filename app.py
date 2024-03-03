from flask import Flask, request, jsonify, render_template
import json
from pprint import pprint as pp
from pathlib import Path
import re
app = Flask(__name__)

#tmp = '71386-10'


@app.route('/')
def index():
    pathlist = Path('./info/').rglob('*.json')
    set_list = []
    for path in pathlist:
        set_num = re.findall(r"\b\d+(?:-\d+)?\b",str(path))[0]
        with open('./static/sets/'+set_num+'/info.json') as info:
            info_file = json.loads(info.read())
        set_list.append(info_file)
    print(set_list) 
    return render_template('frontpage.html',set_list=set_list)

@app.route('/<tmp>')
def sets(tmp):
    with open('./static/sets/'+tmp+'/info.json') as info:
          info_file = json.loads(info.read())
    with open('./static/sets/'+tmp+'/inventory.json') as inventory:
          inventory_file = json.loads(inventory.read())
    with open('./info/'+tmp+'.json') as info:
          json_file = json.loads(info.read())
    pp(json_file['unit'][0]['bricks']['missing'])
    return render_template('bootstrap_table.html', tmp=tmp,title=info_file['set_num']+" - "+info_file['name'],
                           info_file=info_file,inventory_file=inventory_file,json_file=json_file)


@app.route('/<tmp>/saveNumber', methods=['POST'])
def save_number(tmp):
    data1 = request.form.get('brick.part.part_num')
    data2 = request.form.get('brick.color.name')
    data3 = request.form.get('index')
    number = request.form.get('numberInput')
    is_spare = request.form.get('is_spare')

    if number is not None:

        print(data1)
        print(data2)
        print(number)
        print(is_spare)

        with open('./info/'+tmp+'.json') as info:
            json_file = json.loads(info.read())
        print(json_file['count'])

        data = '{"brick" : {"ID":"' + data1 + '","is_spare": "' + is_spare + '","color_name": "' + data2 + '","amount":"' + number + '"}}'
        
        json_file['unit'][int(data3)]['bricks']['missing'].append(json.loads(data))

        with open('./info/'+tmp+'.json', 'w') as dump_file:
            json.dump(json_file,dump_file)
    
    return  ('', 204)

if __name__ == '__main__':
    app.run(host='192.168.10.109', debug=True, port=3333)
