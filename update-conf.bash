curDir=$(pwd)
rootDir=$( dirname "${BASH_SOURCE[0]}" )

http_portKey="['site']['http']['PORT']"
http_addressKey="['site']['http']['ADDRESS']"

http_port=$(cat $rootDir/env.json | python -c "
import json, sys
ENV=json.loads(sys.stdin.read())
print(ENV$http_portKey)
")

http_address=$(cat $rootDir/env.json | python -c "
import json, sys
ENV=json.loads(sys.stdin.read())
print(ENV$http_addressKey)
")

echo "Updating Nginx config"

python -c "
import sys
with open('nginx.conf', 'r') as f:
    conf = f.read()
# Update the port and address of the websocket server
print(conf.replace('REPLACE_SITE_SERVER', '"$http_address"' + ':' + '"$http_port"').replace('REPLACE_WS_SERVER', '"$ws_address"' + ':' + '"$ws_port"'))
" > nginx.txt

sudo cp $rootDir/nginx.txt /etc/nginx/nginx.conf
sudo service nginx restart
echo "Nginx config has been updated in /etc/nginx/nginx.conf"
