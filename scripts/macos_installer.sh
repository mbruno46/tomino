#!/bin/bash

if [ ! -z `which python` ]; then
  URL=`curl -k -s "https://api.github.com/repos/mbruno46/tomino/releases/latest" | python -c "
import sys, json; 
dat = json.load(sys.stdin)['assets']; 
for d in dat:
  if (d['name']=='tomino.app.tar.gz'):
    print d['browser_download_url']; 
    break;
"`
elif [ ! -z `which python3` ]; then
  URL=`curl -k -s "https://api.github.com/repos/mbruno46/tomino/releases/latest" | python3 -c "
import sys, json; 
dat = json.load(sys.stdin)['assets']; 
for d in dat:
  if (d['name']=='tomino.app.tar.gz'):
    print(d['browser_download_url']); 
    break;
"`
fi

echo "Downloading $URL"

curl -L -O -k $URL
NAME=`basename $URL`

tar -zxf $NAME
DEST="$HOME/Applications/tomino.app"
if [ -d $DEST ]; then rm -r $DEST; fi
mv tomino.app $DEST
xattr -dr com.apple.quarantine $DEST

rm $NAME