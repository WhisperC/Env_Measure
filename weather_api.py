# -*- coding: utf-8 -*-
import json
import requests


# 调用和风天气的API
url = 'https://free-api.heweather.com/x3/weather?cityid=' + 'CN101190101' + '&key=c6f375ad271746668307f2297d24ef87'


resp = requests.get(url).text
# 将JSON转化为Python的数据结构
json_data = json.loads(resp)
data = json_data['HeWeather data service 3.0'][0]

# 获取PM2.5的值
pm25 = data['aqi']['city']['pm25']
# 获取空气质量
air_quality = data['aqi']['city']['qlty']

# 获取城市
city = data['basic']['city']

# 获取现在的天气、温度、体感温度、风向、风力等级
now_weather = data['now']['cond']['txt']
now_tmp = data['now']['tmp']
now_fl = data['now']['fl']
now_wind_dir = data['now']['wind']['dir']
now_wind_sc = data['now']['wind']['sc']

# 今天的天气
today = data['daily_forecast'][0]
weather_day = today['cond']['txt_d']
weather_night = today['cond']['txt_n']
tmp_high = today['tmp']['max']
tmp_low = today['tmp']['min']
wind_dir = today['wind']['dir']
wind_sc = today['wind']['sc']

# 天气建议

# 舒适度
comf = data['suggestion']['comf']['brf']
comf_txt = data['suggestion']['comf']['txt']

# 流感指数
flu = data['suggestion']['flu']['brf']
flu_txt = data['suggestion']['flu']['txt']

# 穿衣指数
drsg = data['suggestion']['drsg']['brf']
drsg_txt = data['suggestion']['drsg']['txt']

weather_forcast_txt = "%s今天白天天气%s\n夜间天气%s\n最高气温%s℃\n最低气温%s℃\n风力%s\n风向%s\n天气舒适度：%s\n%s\n流感" \
                      "指数：%s\n%s \n穿衣指数：%s %s \n现在外面的天气：%s\n当前温度:%s\n当前风力:%s" % (
                      city, weather_day, weather_night, tmp_high, tmp_low, wind_sc, wind_dir, comf, comf_txt, flu,
                      flu_txt, drsg, drsg_txt, now_weather, now_tmp, now_wind_sc)

weathernow = weather_forcast_txt
# print(weathernow)
