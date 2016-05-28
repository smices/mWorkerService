#!/bin/bash
#find location by shell script directory
SOURCE="$0"
while [ -h "$SOURCE"  ]; do
    DIR="$( cd -P "$( dirname "$SOURCE"  )" && pwd  )";
    SOURCE="$(readlink "$SOURCE")";
    [[ $SOURCE != /*  ]] && SOURCE="$DIR/$SOURCE";
done
workspace="$( cd -P "$( dirname "$SOURCE"  )" && pwd  )";

cd ${workspace}
sudo easy_install pip
sudo pip install -r requires_python_mods.txt