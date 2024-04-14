from flask import Flask, request, redirect, jsonify, render_template, Response
import json
from pprint import pprint as pp
from pathlib import Path
import numpy as np
import re
app = Flask(__name__)

#tmp = '71386-10'
@app.route('/favicon.ico')

@app.route('/', methods=['GET', 'POST'])
def index():
    pathlist = Path('./info/').rglob('*.json')
    set_list = []
    json_file = {}
    theme_file = np.loadtxt("themes.csv", delimiter=",",dtype="str")
    if request.method == 'GET':
        for path in pathlist:
            set_num = re.findall(r"\b\d+(?:-\d+)?\b",str(path))[0]
            with open('./static/sets/'+set_num+'/info.json') as info:
                info_file = json.loads(info.read())
            try:
                info_file['theme_id'] = theme_file[theme_file[:, 0] == str(info_file['theme_id'])][0][1]
            except Exception as e:
                print(e)
            
            with open('./info/'+set_num+'.json') as info:
                json_file[set_num] = json.loads(info.read())
            
            set_list.append(info_file)

        return render_template('frontpage.html',set_list=set_list,themes_list=theme_file,json_file=json_file)
    
    if request.method == 'POST':
        set_num = request.form.get('set_num')
        index = request.form.get('index')
        minif = request.form.get('minif')
        scheck = request.form.get('scheck')
        scol = request.form.get('scol')
        
        with open('./info/'+set_num+'.json') as info:
            json_file = json.loads(info.read())
        if minif != None:
            json_file['unit'][int(index)]['Minifigs Collected'] = minif
        if scheck != None:
            json_file['unit'][int(index)]['Set Checked'] = scheck
        if scol != None:
            json_file['unit'][int(index)]['Set Collected'] = scol
       
        with open('./info/'+set_num+'.json', 'w') as dump_file:
            json.dump(json_file,dump_file)
        return ('', 204)

@app.route('/<tmp>', methods=['GET', 'POST'])
def sets(tmp):
   
    with open('./static/sets/'+tmp+'/info.json') as info:
          info_file = json.loads(info.read())
    with open('./static/sets/'+tmp+'/minifigs.json') as info:
          minifigs_file = json.loads(info.read())
    with open('./static/sets/'+tmp+'/inventory.json') as inventory:
          inventory_file = json.loads(inventory.read())
    with open('./info/'+tmp+'.json') as info:
          json_file = json.loads(info.read())

    if request.method == 'POST':
        part_num = request.form.get('brickpartpart_num')
        color = request.form.get('brickcolorname')
        index = request.form.get('index')
        number = request.form.get('numberInput')
        is_spare = request.form.get('is_spare')

        # print(part_num)
        # print(color)
        # print(index)
        # print(number)
        # print(is_spare)
        
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
            elif number == '':
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
        #return Response(status=200)
        return ('', 204)
    else:
       return render_template('bootstrap_table.html', tmp=tmp,title=info_file['name'],
                       info_file=info_file,inventory_file=inventory_file,json_file=json_file,minifigs_file=minifigs_file)



@app.route('/<tmp>/saveNumber', methods=['POST'])
def save_number(tmp):
    part_num = request.form.get('brickpartpart_num')
    color = request.form.get('brickcolorname')
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

        data = '{"brick" : {"ID":"' + part_num + '","is_spare": "' + is_spare + '","color_name": "' + color + '","amount":"' + number + '"}}'
        
        if len(json_file['unit'][int(index)]['bricks']['missing']) == 0:
            json_file['unit'][int(index)]['bricks']['missing'].append(json.loads(data))
            print(json_file)
        elif number == '':
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
        
    return Response(status=204)

if __name__ == '__main__':
    app.run(host='192.168.10.109', debug=True, port=3333)
