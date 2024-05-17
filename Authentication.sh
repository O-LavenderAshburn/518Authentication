#!/bin/bash
#activate Virtual envirment
cd Authentication
python3 -m venv auth-env
source auth-env/bin/activate

#install dependantcies
pip install better_profanity
pip install bcrypt
pip install maskpass
python3 sql_setup.py
python3 Authentication.py