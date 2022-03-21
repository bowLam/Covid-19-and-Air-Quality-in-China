# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 18:00:46 2021

@author: Lam Pui King
"""

# =============================================================================
# Now we try to match all the data based on province
# =============================================================================
#Now I locate my file position
import re, os
import pandas as pd
import glob

os.chdir('C:/Users/jcgss/OneDrive/Desktop/Master of Economics/Sem1/Econ 6067 2pm to 5pm Tuesday CP4- LTA/Final Project/1023')
csv_path= os.getcwd()
csv_path
csv_files = glob.glob(os.path.join(csv_path, "*.csv"))
csv_path

#loading data consisting the checking point code and city name
import pandas as pd
site_list=pd.read_csv(csv_path+"/siteslist2021(2).csv")
site_list
site_list=site_list[["监测点编码","城市"]]
site_list.to_csv("C:/Users/instemp/Downloads/siteslist2021.csv")

#Loadinf data of chinese city and province
province=pd.read_csv("C:/Users/instemp/Downloads/city_province.csv")

prov_city = pd.read_csv(csv_path+"/match_cities_province.csv")
prov_city

#For the data containing province chinese and english from custom
prov_city_custom = pd.read_excel(csv_path+"/custom.xls")
prov_city_custom

#Do the cleaning:
empty_province=[]
for q in prov_city_custom["北京市"]:
    head, sep, tail = q.partition("市")
    empty_province.append(head)

empty_province

prov_city_custom["province"]=empty_province
prov_city_custom
    
ep=[]
for w in empty_province:
    head, sep, tail = w.partition("省")
    ep.append(head)

ep
prov_city_custom["provincee"]=ep
prov_city_custom


ep_shi=[]
for q in prov_city_custom["Beijing Shi"]:
    head, sep, tail = q.partition(" Shi")
    ep_shi.append(head)
    
ep_shi
prov_city_custom["ep_shi"]=ep_shi
prov_city_custom
    
ep_sheng=[]
for w in ep_shi:
    head, sep, tail = w.partition(" Sheng")
    ep_sheng.append(head)

ep_sheng
prov_city_custom["ep_sheng"]=ep_sheng

prov_city_custom= prov_city_custom.iloc[:,[4,6]]
prov_city_custom
prov_city_custom = prov_city_custom.rename({'provincee': '省', 'ep_sheng': 'RegionName'}, axis=1) 

#Checking stage
if "Yunnan" in prov_city_custom.values:
    print("yes")
else:
    print("no")


#For the one that match with all cities and provinces
prov_city = pd.read_csv(csv_path+"/match_cities_province.csv")
#Do the cleaning:
for i in prov_city["省"]:
    head, sep, tail = i.partition("市")
    prov_city["省"].replace({i:head}, inplace = True)

prov_city

for j in prov_city["省"]:
    head, sep, tail = j.partition("省")
    prov_city["省"].replace({j:head}, inplace = True)
    
#This is the one with 监测点编码, city, province, reformat
prov_city
prov_city_group_based_number=prov_city.groupby('监测点编码', as_index=False).first()
prov_city=prov_city.groupby('城市', as_index=False).first()
prov_city=prov_city.iloc[:,[0,2]]

#This is the one match chinese and english province name, reformat
prov_city_custom=prov_city_custom.groupby('省', as_index=False).first()
prov_city_custom

#Merging the dataset, based on prov_city (the chinese one) and the prov_city(english one)
prov_chi_eng_match = pd.merge(prov_city,prov_city_custom,on="省")
prov_chi_eng_match
#Need another round of cleaning
pcem=[]
for q in prov_chi_eng_match["RegionName"]:
    head, sep, tail = q.partition(" ")
    pcem.append(head)

prov_chi_eng_match["RegionName"]=pcem

prov_chi_eng_match["RegionName"].replace("Nei","Inner Mongolia", inplace=True)
prov_chi_eng_match["RegionName"].replace("Xizang","Tibet", inplace=True)
prov_chi_eng_match["RegionName"].replace("Ningxiahuizu","Ningxi", inplace=True)

prov_chi_eng_match

#Now open the Oxford Data:
oxford_data= pd.read_csv(csv_path+"/oxdta_yq.csv")
oxford_data

if "Heilongjiang" in oxford_data.values:
    print("yes")
else:
    print("no")

#Merge the one with englsih and chinese province with the Oxford one
oxf_prov_match = pd.merge(oxford_data,prov_chi_eng_match,on="RegionName")


#Read R data from groupmate
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import os
import pandas as pd 
from rpy2.robjects import r
from rpy2.robjects import pandas2ri
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
import rpy2.robjects as ro
pandas2ri.activate()

f1=r.load("airavg.Rdata")
## load .RData and converts to pd.DataFrame
robj = robjects.r.load('airavg.Rdata')
# iterate over datasets the file
for sets in robj:
    myRData = ro.conversion.rpy2py(r[sets])
    # convert to DataFrame
    if not isinstance(myRData, pd.DataFrame):
        myRData = pd.DataFrame(myRData)
#Now matching the air_avg data with the one with (chinese and english cities&provinces)
prov_chi_eng_match = prov_chi_eng_match.rename(columns={'城市': 'city_CH'})
airq_match = pd.merge(myRData,prov_chi_eng_match,on="city_CH")
airq_match.to_csv(csv_path+"/airq_match.csv")
airq_match
#turning float into int
Date=[]
for i in airq_match["Date"]:
    i=int(i)
    Date.append(i)
airq_match["Date"]=Date
#airq_match = airq_match.rename(columns={'date': 'Date'})

#Now we combine the oxford data with airq_match data based on dates and cities
new_df = pd.merge(oxford_data, airq_match,  how='left', left_on=["RegionName","Date"], right_on = ["RegionName","Date"])
new_df.to_csv("Combine_Covid_data_and_Air_data.csv", index=False)
pd.read_csv("Combine_Covid_data_and_Air_data.csv")