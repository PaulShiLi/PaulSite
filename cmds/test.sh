#!/bin/bash


# BASH_SOURCE[1] = parent dir of this script's dir
printf 'My location: %s\n' "$( dirname "${BASH_SOURCE[1]}" )"
rootDir=$( dirname "${BASH_SOURCE[1]}" )
cd $rootDir

pwd