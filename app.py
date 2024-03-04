from flask import Flask, request, redirect, jsonify, render_template
import json
from pprint import pprint as pp
from pathlib import Path
import re
app = Flask(__name__)

#tmp = '71386-10'
@app.route('/favicon.ico')

@app.route('/')
def index():
    pathlist = Path('./info/').rglob('*.json')
    set_list = []
    for path in pathlist:
        set_num = re.findall(r"\b\d+(?:-\d+)?\b",str(path))[0]
        with open('./static/sets/'+set_num+'/info.json') as info:
            info_file = json.loads(info.read())
        set_list.append(info_file)
    return render_template('frontpage.html',set_list=set_list)

@app.route('/<tmp>')
def sets(tmp):
    with open('./static/sets/'+tmp+'/info.json') as info:
          info_file = json.loads(info.read())
    with open('./static/sets/'+tmp+'/inventory.json') as inventory:
          inventory_file = json.loads(inventory.read())
    with open('./info/'+tmp+'.json') as info:
          json_file = json.loads(info.read())
    return render_template('bootstrap_table.html', tmp=tmp,title=info_file['name'],
                           info_file=info_file,inventory_file=inventory_file,json_file=json_file)


@app.route('/<tmp>/saveNumber', methods=['POST'])
def save_number(tmp):
    part_num = request.form.get('brick.part.part_num')
    color = request.form.get('brick.color.name')
    index = request.form.get('index')
    number = request.form.get('numberInput')
    is_spare = request.form.get('is_spare')

    if number is not None:

        print(part_num)
        print(color)
        print(number)
        print(is_spare)

        with open('./info/'+tmp+'.json') as info:
            json_file = json.loads(info.read())
        print(json_file['count'])

        data = '{"brick" : {"ID":"' + part_num + '","is_spare": "' + is_spare + '","color_name": "' + color + '","amount":"' + number + '"}}'
        
        if len(json_file['unit'][int(index)]['bricks']['missing']) == 0:
            json_file['unit'][int(index)]['bricks']['missing'].append(json.loads(data))
            print(json_file)
        elif number == '0' or number == '':
            for idx,i in enumerate(json_file['unit'][int(index)]['bricks']['missing']):
                if i['brick']['ID'] == part_num and i['brick']['is_spare'] == is_spare and i['brick']['color_name'] == color:
                    json_file['unit'][int(index)]['bricks']['missing'].pop(idx)
        else:
            found = False
            for idx,i in enumerate(json_file['unit'][int(index)]['bricks']['missing']):
                if not found and i['brick']['ID'] == part_num and i['brick']['is_spare'] == is_spare and i['brick']['color_name'] == color:
                    json_file['unit'][int(index)]['bricks']['missing'][idx]['brick']['amount'] = number
                    found = True
            if not found:
                json_file['unit'][int(index)]['bricks']['missing'].append(json.loads(data))

        
        with open('./info/'+tmp+'.json', 'w') as dump_file:
            json.dump(json_file,dump_file)
        
    return  redirect('/{}'.format(tmp))

if __name__ == '__main__':
    app.run(host='192.168.10.109', debug=True, port=3333)
