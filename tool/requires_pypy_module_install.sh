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

wget https://bootstrap.pypa.io/get-pip.py
pypy get-pip.py
pypy -m pip install -r requires_python_mods.txt