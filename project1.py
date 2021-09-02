#!/usr/bin/env python
# coding: utf-8

# In[22]:


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
import datetime
from scipy import stats
from scipy.stats import linregress
from config import weather_api_key
#from config import g_key
from citipy import citipy
import csv as atlantic_working


# In[23]:


# Import API key
from config import weather_api_key


# In[24]:


# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy


# In[35]:


awdf = pd.read_csv('atlanticworking.csv')
#awdf['Latitude'].head()
awdf['Longitude'].head()


# In[ ]:





# In[25]:


#set "cit center" for Houston
Houston_lat = 29.756097853207656
Houston_lng = -95.3669907972107


#calculate greater Houston area by expanding lat and lng
lat = np.random.uniform(Houston_lat-1, Houston_lat+2, size=6500)
lng = np.random.uniform(Houston_lng-5, Houston_lng+2, size=6500)
city = []

#find nearest city using lat and lng
for x in range(len(lat)):
    city.append(citipy.nearest_city(lat[x], lng[x]).city_name)


# In[11]:


#turn cities into df
df_city = pd.DataFrame({
    "City":city,
    "lat":lat,
    "lng":lng,
})


# In[38]:


awdf['Latitude']=df_city['lat']
awdf['Longitude']=df_city['lng']
awdf.head()


# In[32]:


awdf.head()


# In[12]:


#check length of cities
len(list(df_city["City"].unique()))


# In[17]:


cities = list(df_city["City"].unique())
target_cities=[]

for i in cities:
    c=str(i).replace(" ","+")
    target_cities.append(c)

target_cities


# In[13]:


#set function to get today and previous 4 days' weather data
def unix_time():
    today = datetime.date.today()
    days = [1,2,3,4]
    times = [int(time.mktime(today.timetuple()))]
    for day in days:
        x=today - datetime.timedelta(days=day)
        unixtime = int(time.mktime(x.timetuple()))
        times.append(unixtime)
    return (times)


# In[14]:


base_current_url = "http://api.openweathermap.org/data/2.5/weather?"
temp=[]
wind_speed=[]
pressure=[]
city_name=[]

for city in target_cities[:4]:
    query_url=f"{base_current_url}appid={weather_api_key}&q={city},US&units=imperial"
    req = requests.get(query_url)
    response1=req.json()
    latitude=response1["coord"]["lat"]
    longitude=response1["coord"]["lon"]

    for x in unix_time():
        historical_url = f"http://api.openweathermap.org/data/2.5/onecall/timemachine?lat={latitude}&lon={longitude}&dt={x}&appid={weather_api_key}&units=imperial"
        hist_json = requests.get(historical_url).json()
        temp.append(hist_json["current"]["temp"])
        pressure.append(hist_json["current"]["pressure"])
        wind_speed.append(hist_json["current"]["wind_speed"])
        city_name.append(response1['name'])
        print(historical_url)


# In[15]:


#set base url and define function to find OpenWeather cities' based on city name from nearest place API and feed back into
#OpenWeather one call API to ensure proper lat and lng

def find_location(target_cities):
    unix_time()
    base_current_url = "http://api.openweathermap.org/data/2.5/weather?"
    temp=[]
    wind_speed=[]
    pressure=[]
    city_name=[]
    country_code=[]
    for city in target_cities[:5]:
        try: 
            query_url=f"{base_current_url}appid={weather_api_key}&q={city},Texas,USA&units=imperial"
            req = requests.get(query_url)
            response1=req.json()
            latitude=response1["coord"]["lat"]
            longitude=response1["coord"]["lon"]
#             print(response1)

        except:
            print("City not found. Skipping...")
            pass
        if response1["sys"]["country"]=="US":
            for x in unix_time():
                historical_url = f"http://api.openweathermap.org/data/2.5/onecall/timemachine?lat={latitude}&lon={longitude}&dt={x}&appid={weather_api_key}&units=imperial"
                hist_json = requests.get(historical_url).json()
                temp.append(hist_json["current"]["temp"])
                pressure.append(hist_json["current"]["pressure"])
                wind_speed.append(hist_json["current"]["wind_speed"])
                city_name.append(response1['name'])
                country_code.append(response1["sys"]["country"])
    d=dict()
    d["City Name"] = city_name
    d["Country"] = country_code
    d["Temperature"] = temp
    d["Wind_Speed"] = wind_speed
    d["Pressure"] = pressure    
    return(d)
        #print ("--"*30)


# In[16]:


df2 =pd.DataFrame(find_location(target_cities))


# In[ ]:


df2


# In[ ]:


df[df["Country"]=="US"]

