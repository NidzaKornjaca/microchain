#!/bin/bash

x-terminal-emulator -e "FLASK_ENV=development flask run -p 5000;"
x-terminal-emulator -e "FLASK_ENV=development flask run -p 5001;"
sleep 1
cjp '{"address":"http://localhost:5001/"}' http://localhost:5000/node/introduce
cjp '{"address":"http://localhost:5000/"}' http://localhost:5001/node/introduce
