import datetime
import json
import os
import time

import numpy as np
from operator import itemgetter

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from pyecharts.globals import ThemeType

from gis_data import process
from gis_data.models import CityAirQualityInfo
from pyecharts import options as opts
from pyecharts.charts import Map, Grid

time_now = datetime.datetime.now()
time_today = time_now.strftime('%Y%m%d')
time_before1 = (time_now - datetime.timedelta(days=1)).strftime('%Y%m%d')
time_before2 = (time_now - datetime.timedelta(days=2)).strftime('%Y%m%d')
time_before3 = (time_now - datetime.timedelta(days=3)).strftime('%Y%m%d')
time_before4 = (time_now - datetime.timedelta(days=4)).strftime('%Y%m%d')
time_list = [time_today, time_before1, time_before2, time_before3, time_before4]


# 将返回的数据入库
def read_data(time_date):
    now_hour = str(time.localtime().tm_hour)
    path_file = os.path.join("./data", time_date + now_hour + ".csv")
    city_info, hour = process.getCSVInfo(time_date, path_file)
    for city in city_info:
        if CityAirQualityInfo.objects.filter(id=time_date + now_hour + city):
            continue
        CityAirQualityInfo.objects.filter(id__startswith=time_date, id__endswith=city).delete()
        field = city_info[city]
        aqi_list = field['AQI']
        if len(aqi_list) != 0:
            aqi_24h = int(np.mean(field['AQI']))
        else:
            aqi_24h = 0
        CityAirQualityInfo.objects.create(id=time_date + now_hour + city,
                                          name=city, date=int(time_date), hour=str(hour) + ":00",
                                          aqi=field['AQI'][-1] if len(field['AQI']) > 0 else 0, aqi_24h=aqi_24h,
                                          pm2_5=field['PM2_5'][-1] if len(field['PM2_5']) > 0 else 0, pm2_5_24h=field['PM2_5_24h'],
                                          pm10=field['PM10'][-1] if len(field['PM10']) > 0 else 0, pm10_24h=field['PM10_24h'],
                                          so2=field['SO2'][-1] if len(field['SO2']) > 0 else 0, so2_24h=field['SO2_24h'],
                                          no2=field['NO2'][-1] if len(field['NO2']) > 0 else 0, no2_24h=field['NO2_24h'],
                                          o3=field['O3'][-1] if len(field['O3']) > 0 else 0, o3_24h=field['O3_24h'],
                                          o3_8h=field['O3_8h'][-1] if len(field['O3_8h']) > 0 else 0, o3_8h_24h=field['O3_8h_24h'],
                                          co=field['CO'][-1] if len(field['CO']) > 0 else 0, co_24h=field['CO_24h'])


def airQualityInfoToday(request):
    global time_list
    if request.method == 'GET':
        now_hour = str(time.localtime().tm_hour)        # 获取当前时间
        for i in range(5):                              # GET请求初始化更新库中信息（自动将过去五日的信息爬取入库）
            if CityAirQualityInfo.objects.filter(id__startswith=time_list[i] + now_hour):           # 判断库中是否有对应数据
                continue
            read_data(time_list[i])                     # 入库
        data = list(CityAirQualityInfo.objects.all().values().filter(id__startswith=time_today))    # 获取库中当天数据
        data_dict = {'data': data}
        response = HttpResponse(json.dumps(data_dict, ensure_ascii=False))                          # 返回JSON
        response["Access-Control-Allow-Origin"] = "http://localhost:8080"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "GET,POST"
        response["Access-Control-Allow-Headers"] = "Origin,Content-Type,Cookie,Accept,Token"
        return response
    else:
        return HttpResponse("initial failed")


def airQualityInfoDetail(request):
    if request.method == 'POST':
        data = json.loads(request.body)         # 获取城市信息
        if 'date' not in data:
            try:
                city = data['name']
                data = []
                # 获取获取五日的库中信息
                for i in time_list:
                    data.extend(
                        list(CityAirQualityInfo.objects.all().values().filter(id__startswith=i, id__endswith=city)))
                data = sorted(data, key=itemgetter('date'))
                data_dict = {'data': data}
                return HttpResponse(json.dumps(data_dict, ensure_ascii=False))      # 返回JSON
            except ValueError as e:
                print(str(e))
    return HttpResponse("not receive city's name")


def date(request):
    if request.method == 'POST':
        data = json.loads(request.body)         # 获取POST中的日期
        if 'date' in data:
            date_info = data['date']
            if not CityAirQualityInfo.objects.all().values().filter(id__startswith=date_info):      # 如果库中没有则爬取并入库
                read_data(date_info)
            data_dict = CityAirQualityInfo.objects.all().values().filter(id__startswith=date_info)      # 获取对应库中信息
            city = list(i['name'] for i in data_dict)
            aqi = list(i['aqi_24h'] for i in data_dict)
            # 根据库中信息利用pyecharts绘制地图
            c = (
                Map().add("日平均AQI",
                          [list(z) for z in zip(city, aqi)],
                          "china-cities", is_map_symbol_show=False,
                          label_opts=opts.LabelOpts(is_show=False))
                    .set_global_opts(title_opts=opts.TitleOpts(title="全国" + date_info + "日平均AQI分布图",
                                                               subtitle="原始数据来源:全国城市空气质量实时发布平台",
                                                               subtitle_link="https://quotsoft.net/air/"),
                                     visualmap_opts=opts.VisualMapOpts(max_=150),
                                     )
            )
            grid_chart = Grid(init_opts=opts.InitOpts(theme=ThemeType.WHITE, page_title="全国日平均AQI分布图",
                                                      width="1500px", height="700px"))
            grid_chart.add(
                c,
                grid_opts=opts.GridOpts(pos_left="10%", pos_right="10%", pos_top="10%", pos_bottom="10%"),
            )
            grid_chart.render("./templates/map_china.html")         # 保存为HTML文件
            return HttpResponseRedirect("/show_map/")               # 重定向
    return HttpResponse()


def show_map(request):
    # 返回保存的HTML文件
    return render(request, 'map_china.html')
