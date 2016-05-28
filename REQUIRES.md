## SYSTEM REQUIREMENTS ##
```
ubuntu >=14.04 LTS
python >= 2.7.6
redis >= 3.2
```

## PYTHON MODULE REQUIREMENTS ##
```
see tool/requires_python_mods.txt
```

## PYTHON MODULE INSTALLATION  ##
```
cd tool
chmod a+x *.sh
```

## FOR CPYTHON ENVIRONMENT ##
```
./requires_python_module_install.sh
```

## FOR PYPY ENVIRONMENT##
```
./requires_pypy_module_install.sh
```


## UBUNTU INSTALL PYPY ##
```
sudo add-apt-repository ppa:pypy/ppa
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 251104D968854915
sudo apt-get update
sudo apt-get install pypy pypy-dev

 ----OR----

Go http://pypy.org/download.html download the new package
```
