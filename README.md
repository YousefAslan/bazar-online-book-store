# bazar-online-book-store

## About bazar. com

bazar . com is one of a distributed operating system course project.
bazar online book store. It is a microservices builds based on the RAST API using Flask as it is online book store, and contains only four books:
|book title |topic |
|----------------|-----------------------------|
|How to get a good grade in DOS in 20 minutes a day| distributed systems  
|
|RPCs for Dummies| distributed systems  
|
|Xen and the Art of Surviving Graduate School| graduate school
|
|Cooking for the Impatient Graduate Student| graduate school
|
The project is divided into three main servers:

- front-end server which receive all the request form the user and propagate it back-end servers
- catalog server which consider as one of the back-end server
- order server and its the second back-end server

## Installation

This repository is consist of three main files, each of which represents one of the three servers.
The order server and catalog server files both contain a python scripts called server_configuration.py through which you can change the IP and the ports number of the servers; Where front-end server contains this information inside the front-end server.py file, both servers are running on localhost. If you want to change the environment to works on a different machine, just modify these files to suit the new environment.
After that make sure pipenv is installed if not apply the following command on the terminal

```
$ pip install pipenv
```

After that, open the three directors and apply these commands in each server:

```
$ pipenv shell
$ pipenv install
$ python <server name>
```

# The API
