#!/bin/bash
rootDir=$(dirname "${BASH_SOURCE[0]}")
curDir=$(pwd)
absDir="$curDir/$rootDir"
# Read env.json file and extract ["site"]['http']["PORT"] from it

address=$(cat $absDir/env.json | jq -r '.["site"] | .["http"] | .["ADDRESS"]')
port=$(cat $absDir/env.json | jq -r '.["site"] | .["http"] | .["PORT"]')

echo Current address of site: $address
echo Current port of site: $port

# Clears processes that takes up necessary ports
bash $absDir/cmds/start_clear.bash

cd $absDir/pkgs/nodeModules
npm run tailwind-build

cd $absDir/app/site
uvicorn paul_site.asgi:application --reload --host $address --port $port