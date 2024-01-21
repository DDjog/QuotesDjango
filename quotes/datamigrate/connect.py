#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mongoengine 
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')


url_local = "mongodb://localhost:27017/DBTest"
url = f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority"""

mongoengine.connect( host=url_local )
