# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 00:59:14 2021

@author: instemp
"""

# =============================================================================
# import pandas as pd
# 
# df=pd.read_csv("https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest.csv")
# 
# df.head()
# 
# df.to_csv('//192.168.35.1/fs/Kenny Hsiao/covid_data.csv')
# 
# =============================================================================

import urllib.request
import json

api_token = "529c20e99ef5a34de69c440a9cd78045f90ba90e"

city_name = "bejing"
url = f"https://api.waqi.info/feed/{city_name}/?token={api_token}"
json_obj = urllib.request.urlopen(url)

data = json.load(json_obj)
print(data)

data_time_adm=data["data"]["time"]["s"]
data_time_adm

data_cate= data["data"]["iaqi"]
for i in data_cate:
    print(i," ",data_cate[i]["v"])









