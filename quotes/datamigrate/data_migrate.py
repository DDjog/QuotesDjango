#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import connect
import models
import seeds

if __name__ == '__main__':

    print("___MondoDB simple app___\n")
    
    seeds.delete_data()
    seeds.put_data_to_mongo()
    seeds.copy_data_from_mongo_to_postgres()
    
           
