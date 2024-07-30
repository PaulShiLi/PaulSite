#!/bin/bash
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
rootDir=$(dirname $SCRIPTPATH | xargs dirname)
curDir=$(pwd)

# Read env.json file and extract ["site"]['http']["PORT"] from it

echo $rootDir

address=$(cat $rootDir/env.json | jq -r '.["site"] | .["http"] | .["ADDRESS"]')
port=$(cat $rootDir/env.json | jq -r '.["site"] | .["http"] | .["PORT"]')

echo Current address of site: $address
echo Current port of site: $port

# # Clears processes that takes up necessary ports
# bash $rootDir/cmds/start_clear.bash

cd $rootDir/assets/node
npm run tailwind-build

cd $rootDir/app/site
uvicorn paul_site.asgi:application --reload --host $address --port $port