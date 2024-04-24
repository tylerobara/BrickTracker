#!/bin/bash

wget https://cdn.rebrickable.com/media/downloads/themes.csv.gz
gzip -f -d themes.csv.gz


wget https://cdn.rebrickable.com/media/downloads/sets.csv.gz
gzip -f -d sets.csv.gz


cd static/
wget https://rebrickable.com/static/img/nil_mf.jpg
wget https://rebrickable.com/static/img/nil.png
cd ..
