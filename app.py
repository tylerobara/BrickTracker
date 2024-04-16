from flask import Flask, request, redirect, jsonify, render_template, Response
import json
from pprint import pprint as pp
from pathlib import Path
import time,random,string,sqlite3
import numpy as np
import re #regex
import rebrick #rebrickable api
import requests # request img from web
import shutil # save img locally

app = Flask(__name__)

@app.route('/favicon.ico')

@app.route('/create',methods=['GET', 'POST'])
def create():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    count = 0
    if request.method == 'GET':
        print('get')

    if request.method == 'POST':
        set_num = request.form['inputField']
        add_duplicate = request.form.get('addDuplicate', False) == 'true'
        # Do something with the input value and the checkbox value
        print("Input value:", set_num)
        print("Add duplicate:", add_duplicate)
        # You can perform any further processing or redirect to another page

        if '-' not in set_num:
            set_num = set_num + '-1'

        print ("Adding set: " + set_num)
        with open('api','r') as f:
            api_key = f.read().replace('\n','')
        rb = rebrick.init(api_key)

        unique_set_id = generate_unique_set_unique()
        
        # Get Set info and add to SQL
        response = json.loads(rebrick.lego.get_set(set_num).read())
        count+=1
        print(response)

        cursor.execute('''INSERT INTO sets (
            set_num,
            name,
            year,
            theme_id,
            num_parts,
            set_img_url,
            set_url,
            last_modified_dt,
            u_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) ''', (response['set_num'], response['name'], response['year'], response['theme_id'], response['num_parts'],response['set_img_url'],response['set_url'],response['last_modified_dt'],unique_set_id))

        conn.commit()
        


        # Get set image. Saved under ./static/sets/xxx-x.jpg
        set_img_url = response["set_img_url"]

        print('Saving set image:',end='')

        res = requests.get(set_img_url, stream = True)
        count+=1
        if res.status_code == 200:
            with open("./static/sets/"+set_num+".jpg",'wb') as f:
                shutil.copyfileobj(res.raw, f)
                print(' OK')
        else:
            print('Image Couldn\'t be retrieved for set ' + set_num)
            logging.error('set_img_url: ' + set_num)
            print(' ERROR')


        # Get inventory and add to SQL
        response = json.loads(rebrick.lego.get_set_elements(set_num,page_size=20000).read())
        count+=1
        for i in response['results']:
            # Get part image. Saved under ./static/parts/xxxx.jpg
            part_img_url = i['part']['part_img_url']

            pattern = r'/([^/]+)\.(?:png|jpg)$'
            match = re.search(pattern, part_img_url)

            if match:
                part_img_url_id = match.group(1)
                print("Part number:", part_img_url_id)
            else:
                print("Part number not found in the URL.")
                print(">>> " + part_img_url)


            cursor.execute('''INSERT INTO inventory (
                set_num,
                id,
                part_num,
                name,
                part_img_url,
                part_img_url_id,
                color_id,
                color_name,
                quantity,
                is_spare,
                element_id,
                u_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (set_num, i['id'], i['part']['part_num'],i['part']['name'],i['part']['part_img_url'],part_img_url_id,i['color']['id'],i['color']['name'],i['quantity'],i['is_spare'],i['element_id'],unique_set_id))
            
            
            if not Path("./static/parts/"+part_img_url_id+".jpg").is_file():
                print('Saving part image:',end='')

                res = requests.get(part_img_url, stream = True)
                count+=1
                if res.status_code == 200:
                    with open("./static/parts/"+part_img_url_id+".jpg",'wb') as f:
                        shutil.copyfileobj(res.raw, f)
                        print(' OK')
                else:
                    print('Image Couldn\'t be retrieved for set ' + part_img_url_id)
                    logging.error('part_img_url: ' + part_img_url_id)
                    print(' ERROR')
            else: 
                print(part_img_url_id + '.jpg exists!')

        conn.commit()

        # Get minifigs
        print('Savings minifigs')
        response = json.loads(rebrick.lego.get_set_minifigs(set_num).read())
        count+=1
        print(response)

        for i in response['results']:

            # Get set image. Saved under ./static/minifigs/xxx-x.jpg
            set_img_url = i["set_img_url"]
            set_num = i['set_num']

            print('Saving set image:',end='')

            res = requests.get(set_img_url, stream = True)
            count+=1
            if res.status_code == 200:
                with open("./static/minifigs/"+set_num+".jpg",'wb') as f:
                    shutil.copyfileobj(res.raw, f)
                    print(' OK')
            else:
                print('Image Couldn\'t be retrieved for set ' + set_num)
                logging.error('set_img_url: ' + set_num)
                print(' ERROR')

            cursor.execute('''INSERT INTO minifigures (
                set_num,
                name,
                quantity,
                set_img_url,
                u_id
            ) VALUES (?, ?, ?, ?, ?) ''', (i['set_num'], i['set_name'], i['quantity'],i['set_img_url'],unique_set_id))

            conn.commit()
        
            # Get minifigs inventory
            response_minifigs = json.loads(rebrick.lego.get_minifig_elements(i['set_num']).read())
            count+=1

            for i in response_minifigs['results']:
                cursor.execute('''INSERT INTO inventory (
                    set_num,
                    id,
                    part_num,
                    name,
                    part_img_url,
                    color_id,
                    color_name,
                    quantity,
                    is_spare,
                    element_id,
                    u_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (i['set_num'], i['id'], i['part']['part_num'],i['part']['name'],i['part']['part_img_url'],i['color']['id'],i['color']['name'],i['quantity'],i['is_spare'],i['element_id'],unique_set_id))
            conn.commit()

    conn.close()

    print('Count: ' + str(count))


    return render_template('create.html')

def generate_unique_set_unique():
    timestamp = int(time.time() * 1000)  # Current timestamp in milliseconds
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))  # 8-digit alphanumeric
    return f'{timestamp}{random_chars}'

@app.route('/',methods=['GET','POST'])
def index():
    set_list = []
    theme_file = np.loadtxt("themes.csv",delimiter=",",dtype="str")

    if request.method == 'GET':
        
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * from sets;')

        results = cursor.fetchall()
        set_list = [list(i) for i in results]

        print(set_list)
        for i in set_list:
            try:
                i[3] = theme_file[theme_file[:, 0] == str(i[3])][0][1]
            except Exception as e:
                print(e)


        cursor.close()
        conn.close()
        return render_template('index.html',set_list=set_list,themes_list=theme_file)


@app.route('/<tmp>/<u_id>', methods=['GET', 'POST'])
def inventory(tmp,u_id):
    
    if request.method == 'GET':
        
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        # Get set info
        cursor.execute("SELECT * from sets where set_num == '" + tmp + "' and u_id == '" + u_id + "';")
        results = cursor.fetchall()
        set_list = [list(i) for i in results]

        # Get inventory
        cursor.execute("SELECT * from inventory where set_num == '" + tmp + "' and u_id == '" + u_id + "';")
        results = cursor.fetchall()
        inventory_list =  [list(i) for i in results]

        # Get missing parts
        cursor.execute("SELECT * from missing where set_num == '" + tmp + "' and u_id == '" + u_id + "';")
        results = cursor.fetchall()
        missing_list =  [list(i) for i in results]

        cursor.close()
        conn.close()

        return render_template('table.html', tmp=tmp,title=set_list[0][1],set_list=set_list,inventory_list=inventory_list,missing_list=missing_list)


    if request.method == 'POST':
        set_num = request.form.get('set_num')
        id = request.form.get('id')
        part_num = request.form.get('part_num')
        color_id = request.form.get('color_id')
        element_id = request.form.get('element_id')
        u_id = request.form.get('u_id')
        missing = request.form.get('missing')
            
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        # If quantity is not empty
        if missing != '' and missing != '0':
            #Check if there's an existing entry
            cursor.execute('''SELECT quantity FROM missing 
                WHERE   set_num = ? AND 
                        id = ? AND 
                        part_num = ? AND 
                        color_id = ? AND 
                        element_id = ? AND 
                        u_id = ?''',
                        (set_num, id, part_num, color_id, element_id, u_id))
            
            existing_quantity = cursor.fetchone()

            #If there's an existing entry or if entry isn't the same as the new value 
            if existing_quantity is None or existing_quantity[0] != missing:
                cursor.execute('''INSERT OR REPLACE INTO missing (
                        set_num,
                        id,
                        part_num,
                        color_id,
                        quantity,
                        element_id,
                        u_id
                    ) VALUES (?, ?, ?, ?, ?, ?, ?) ''', 
                   (set_num, id, part_num, color_id, missing, element_id, u_id))

            conn.commit()
        
        # If quantity is empty, delete the entry.
        else:
            cursor.execute('''DELETE FROM missing
                WHERE   set_num = ? AND
                        id = ? AND
                        part_num = ? AND
                        color_id = ? AND
                        element_id = ? AND
                        u_id = ?''',
                (set_num, id, part_num, color_id, element_id, u_id))

            conn.commit()

        cursor.close()
        conn.close()
        return ('', 204)

@app.route('/old', methods=['GET', 'POST'])
def frontpage():
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

@app.route('/old/<tmp>', methods=['GET', 'POST'])
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
