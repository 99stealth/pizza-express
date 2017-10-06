#!/bin/bash

npm i --production
npm test

if [ $? == 0 ]; then
    node server.js
fi