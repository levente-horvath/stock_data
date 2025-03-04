#!/bin/bash


PYTHON=/home/lev/programming/stock_data/.venv/bin/python3.11


$PYTHON extract.py


if [ $? -ne 0 ]; then
    echo "Error running extract.py"
    exit
fi


$PYTHON transform.py


if [ $? -ne 0 ]; then
    echo "Error running transform.py"
    exit
fi


$PYTHON load.py



if [ $? -ne 0 ]; then
    echo "Error running load.py"
    exit
fi
