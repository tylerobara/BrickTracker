import sys #using argv
import logging #logging errors

from pathlib import Path # creating folders
import rebrick #rebrickable api

# json things
import json
from pprint import pprint as pp
import requests # request img from web
import shutil # save img locally

log_name='lego.log'

logging.basicConfig(filename=log_name, level=logging.DEBUG)
logging.FileHandler(log_name,mode='w')

if '-' not in sys.argv[1]:
    set_num = sys.argv[1] + '-1'
else:
    set_num=sys.argv[1]

#online_set_num=set_num+"-1"

print ("Adding set: " + set_num)

set_path="./static/sets/" + set_num + "/"
Path('./static/parts').mkdir(parents=True, exist_ok=True)
Path('./static/figs').mkdir(parents=True, exist_ok=True)
Path('./info').mkdir(parents=True, exist_ok=True)

with open('api','r') as f:
    api_key = f.read().replace('\n','')

rb = rebrick.init(api_key)

# if Path(set_path).is_dir():
#     print('Set exists, exitting')
#     logging.error('Set exists!')
#     #exit()

Path(set_path).mkdir(parents=True, exist_ok=True)

# Get set info
response = json.loads(rebrick.lego.get_set(set_num).read())

if Path("./info/"+set_num + ".json").is_file():

    ans = input('Set exists, would you like to add another copy (Y/N)?\n')
    if ans.lower() == 'yes' or ans.lower() == 'y':
        with open("./info/" + set_num + ".json",'r') as f:
            data = json.load(f)
            data['count'] = data['count'] + 1

            tmp = {"location": "","minifigs": "","bricks": {"missing": []}}
            
            data['unit'].append(tmp)
            pp(data)
        with open("./info/" + set_num + ".json",'w') as f:
            json.dump(data,f,indent = 4)

with open(set_path+'info.json', 'w', encoding='utf-8') as f:
    json.dump(response, f, ensure_ascii=False, indent=4)

# save set image to folder
set_img_url = response["set_img_url"]

print('Saving set image:',end='')

res = requests.get(set_img_url, stream = True)

if res.status_code == 200:
    with open(set_path+"cover.jpg",'wb') as f:
        shutil.copyfileobj(res.raw, f)
        print(' OK')
else:
    print('Image Couldn\'t be retrieved for set ' + set_num)
    logging.error('set_img_url: ' + set_num)
    print(' ERROR')

# set inventory
print('Saving set inventory')
response = json.loads(rebrick.lego.get_set_elements(set_num,page_size=20000).read())
with open(set_path+'inventory.json', 'w', encoding='utf-8') as f:
    json.dump(response, f, ensure_ascii=False, indent=4)

# get part images if not exists
print('Saving part images')
for i in response["results"]:
    try:
        if i['element_id'] == None:
            if not Path("./static/parts/p_"+i["part"]["part_id"]+".jpg").is_file():
                res = requests.get(i["part"]["part_img_url"], stream = True)
                if res.status_code == 200:
                    with open("./static/parts/p_"+i["part"]["part_id"]+".jpg",'wb') as f:
                        shutil.copyfileobj(res.raw, f)
        else:
            if not Path("./static/parts/"+i["element_id"]+".jpg").is_file():
                res = requests.get(i["part"]["part_img_url"], stream = True)

                if res.status_code == 200:
                    with open("./static/parts/"+i["element_id"]+".jpg",'wb') as f:
                        shutil.copyfileobj(res.raw, f)
            if not Path("./static/parts/"+i["element_id"]+".jpg").is_file():
                res = requests.get(i["part"]["part_img_url"], stream = True)

                if res.status_code == 200:
                    with open("./static/parts/"+i["element_id"]+".jpg",'wb') as f:
                        shutil.copyfileobj(res.raw, f)
    except Exception as e:
        print(e)
        logging.error(set_num + ": " + str(e))

# read info file with missing pieces

if Path("./info/"+set_num + ".json").is_file():
    with open("./info/" + set_num + ".json") as f:
        data = json.load(f)
else:
    shutil.copy("set_template.json", "./info/"+set_num+".json")

## Minifigs ##
print('Savings minifigs')
response = json.loads(rebrick.lego.get_set_minifigs(set_num).read())

figures = {"figs": []}

for x in response["results"]:
    print("    " + x["set_name"])
    fig = {
        "set_num": x["set_num"],
        "name": x["set_name"],
        "quantity": x["quantity"],
        "set_img_url": x["set_img_url"],
        "parts": []
    }

    res = requests.get(x["set_img_url"], stream = True)

    if res.status_code == 200:
        with open("./static/figs/"+x["set_num"]+".jpg",'wb') as f:
            shutil.copyfileobj(res.raw, f)
    else:
        print('Image Couldn\'t be retrieved for set ' + set_num)
        logging.error('set_img_url: ' + set_num)

    response = json.loads(rebrick.lego.get_minifig_elements(x["set_num"]).read())

    for i in response["results"]:
        part = {
            "name": i["part"]["name"],
            "quantity": i["quantity"],
            "color_name": i["color"]["name"],
            "part_num": i["part"]["part_num"],
            "part_img_url": i["part"]["part_img_url"]

        }
        fig["parts"].append(part)

        try:
            if i['element_id'] == None:
                if not Path("./static/figs/p_"+i["part"]["part_num"]+".jpg").is_file():
                    res = requests.get(i["part"]["part_img_url"], stream = True)

                    if res.status_code == 200:
                        with open("./static/figs/p_"+i["part"]["part_num"]+".jpg",'wb') as f:
                            shutil.copyfileobj(res.raw, f)
            else:
                if not Path("./static/figs/"+i["part"]["part_num"]+".jpg").is_file():
                    res = requests.get(i["part"]["part_img_url"], stream = True)

                    if res.status_code == 200:
                        with open("./static/figs/"+i["part"]["part_num"]+".jpg",'wb') as f:
                            shutil.copyfileobj(res.raw, f)
                if not Path("./static/figs/"+i["part"]["part_num"]+".jpg").is_file():
                    res = requests.get(i["part"]["part_img_url"], stream = True)

                    if res.status_code == 200:
                        with open("./static/figs/"+i["part"]["part_num"]+".jpg",'wb') as f:
                            shutil.copyfileobj(res.raw, f)
        except Exception as e:
            print(e)
            logging.error(set_num + ": " + str(e))

    figures["figs"].append(fig)
    part = {}
    fig = {}

with open(set_path+'minifigs.json', 'w', encoding='utf-8') as f:
    json.dump(figures, f, ensure_ascii=False, indent=4)
####

print('Done!')
