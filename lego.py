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

set_num=sys.argv[1]
online_set_num=set_num+"-1"

set_path="./sets/" + sys.argv[1] + "/"
Path('./static/parts').mkdir(parents=True, exist_ok=True)
Path('./info').mkdir(parents=True, exist_ok=True)

with open('api','r') as f:
    api_key = f.read().replace('\n','')

rb = rebrick.init(api_key)



if Path(set_path).is_dir():
    print('Set exists, exitting')
    logging.error('Set exists!')
    #exit()

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

    else:
        with open(set_path+'info.json', 'w', encoding='utf-8') as f:
            json.dump(response, f, ensure_ascii=False, indent=4)

# save set image to folder
set_img_url = response["set_img_url"]

res = requests.get(set_img_url, stream = True)

if res.status_code == 200:
    with open(set_path+"cover.jpg",'wb') as f:
        shutil.copyfileobj(res.raw, f)
else:
    print('Image Couldn\'t be retrieved for set ' + set_num)
    logging.error('set_img_url: ' + set_num)

# set inventory
response = json.loads(rebrick.lego.get_set_elements(set_num).read())
with open(set_path+'inventory.json', 'w', encoding='utf-8') as f:
    json.dump(response, f, ensure_ascii=False, indent=4)

# get part images if not exists
for i in response["results"]:
    if not Path("./static/parts/"+i["element_id"]+".jpg").is_file():
        res = requests.get(i["part"]["part_img_url"], stream = True)

        if res.status_code == 200:
            with open("./static/parts/"+i["element_id"]+".jpg",'wb') as f:
                shutil.copyfileobj(res.raw, f)
            print('image saved')
        else:
            print('Image Couldn\'t be retrieved for set ' + set_num + ": " + i["element_id"])
            logging.error(set_num + ": " + i["element_id"])

# read info file with missing pieces


if Path("./info/"+set_num + ".json").is_file():
    with open("./info/" + set_num + ".json") as f:
        data = json.load(f)
    print(data)
else:
    shutil.copy("set_template.json", "./info/"+set_num+".json")
