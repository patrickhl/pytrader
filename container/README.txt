This folder only contains DB

How to install:
1, download package from mongodb webpage
2, unpack by >tar -zvxf xxx
3, move to /usr/local/mongodb
4, create conf file as shown in this folder
5, make dir as shown in conf file
6, start mongodb as >./mongod -f /proj/pytrader/container/mongodb.conf
7, if error happens, kill existing process, and remove lock file if necessary
   and redo 6.
