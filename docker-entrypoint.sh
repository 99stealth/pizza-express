#!/bin/bash

npm test

if [ $? == 0 ]; then
    node server.js
fi