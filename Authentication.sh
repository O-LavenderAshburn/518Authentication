#!/bin/bash

#activate Virtual envirment
cd Authentication
python -m venv auth-env
source auth-env/bin/activate

#install dependantcies
pip install bcrypt
pip install maskpass
pip install better_profanit
python3 sql_setup.py
python3 Authentication.py
