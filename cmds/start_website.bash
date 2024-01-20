rootDir=$( dirname "${BASH_SOURCE[1]}" )

# Activate env
source $rootDir/start_env.bash

# Clears processes that takes up necessary ports
sudo bash $rootDir/start_clear.bash

cd $rootDir/..
python3 PaulWebsite