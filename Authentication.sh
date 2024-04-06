#!/bin/bash

#activate Virtual envirment
cd Authentication
source auth-env/bin/activate

#install dependantcies
pip install bcrypt
pip install maskpass
pip install better_profanity

python3 Authentication.py
