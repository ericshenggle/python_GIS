import datetime
import os

import requests


# 进行数据爬取，下载url对应的csv文件
def downloadCSV(url, path_file):
    down_res = requests.get(url)
    assert down_res.status_code == 200

    if not os.path.isdir('./data'):
        os.mkdir('./data')

    with open(path_file, 'wb') as f:
        f.write(down_res.content)


# 获取当前需要的日期对应的csv文件
def getCSVInfo(time_day, path_file):
    url = "https://quotsoft.net/air/data/china_cities_" + time_day + ".csv"
    if not os.path.exists(path_file):
        downloadCSV(url, path_file)
    with open(path_file, 'r', encoding='UTF-8') as f:
        lines = f.readlines()
        name_city = {}
        cities = lines[0].strip().split(',')[3:]
        for index in range(len(cities)):
            fields = {'AQI': [], 'AQI_24h': 0, 'PM2_5': [], 'PM2_5_24h': 0, 'PM10': [], 'PM10_24h': 0, 'SO2': [],
                      'SO2_24h': 0,
                      'NO2': [],
                      'NO2_24h': 0, 'O3': [], 'O3_24h': 0, 'O3_8h': [], 'O3_8h_24h': 0, 'CO': [], 'CO_24h': 0}
            name_city[cities[index]] = fields
        for line in lines[1:]:
            tmp = line.strip().split(',')
            if tmp[2] == 'AQI':
                j = 3
                for i in cities:
                    if not tmp[j] == '':
                        name_city[i]['AQI'].append(int(tmp[j]))
                    j += 1
            elif tmp[2] == 'PM2.5':
                j = 3
                for i in cities:
                    if not tmp[j] == '':
                        name_city[i]['PM2_5'].append(tmp[j])
                    j += 1
            elif tmp[2] == 'PM2.5_24h':
                if name_city[cities[0]]['PM2_5_24h'] != 0:
                    continue
                else:
                    j = 3
                    for i in cities:
                        name_city[i]['PM2_5_24h'] = tmp[j]
                        j += 1
            elif tmp[2] == 'PM10':
                j = 3
                for i in cities:
                    if not tmp[j] == '':
                        name_city[i]['PM10'].append(tmp[j])
                    j += 1
            elif tmp[2] == 'PM10_24h':
                if name_city[cities[0]]['PM10_24h'] != 0:
                    continue
                else:
                    j = 3
                    for i in cities:
                        name_city[i]['PM10_24h'] = tmp[j]
                        j += 1
            elif tmp[2] == 'SO2':
                j = 3
                for i in cities:
                    if not tmp[j] == '':
                        name_city[i]['SO2'].append(tmp[j])
                    j += 1
            elif tmp[2] == 'SO2_24h':
                if name_city[cities[0]]['SO2_24h'] != 0:
                    continue
                else:
                    j = 3
                    for i in cities:
                        name_city[i]['SO2_24h'] = tmp[j]
                        j += 1
            elif tmp[2] == 'NO2':
                j = 3
                for i in cities:
                    if not tmp[j] == '':
                        name_city[i]['NO2'].append(tmp[j])
                    j += 1
            elif tmp[2] == 'NO2_24h':
                if name_city[cities[0]]['NO2_24h'] != 0:
                    continue
                else:
                    j = 3
                    for i in cities:
                        name_city[i]['NO2_24h'] = tmp[j]
                        j += 1
            elif tmp[2] == 'O3':
                j = 3
                for i in cities:
                    if not tmp[j] == '':
                        name_city[i]['O3'].append(tmp[j])
                    j += 1
            elif tmp[2] == 'O3_24h':
                if name_city[cities[0]]['O3_24h'] != 0:
                    continue
                else:
                    j = 3
                    for i in cities:
                        name_city[i]['O3_24h'] = tmp[j]
                        j += 1
            elif tmp[2] == 'O3_8h':
                j = 3
                for i in cities:
                    if not tmp[j] == '':
                        name_city[i]['O3_8h'].append(tmp[j])
                    j += 1
            elif tmp[2] == 'O3_8h_24h':
                if name_city[cities[0]]['O3_8h_24h'] != 0:
                    continue
                else:
                    j = 3
                    for i in cities:
                        name_city[i]['O3_8h_24h'] = tmp[j]
                        j += 1
            elif tmp[2] == 'CO':
                j = 3
                for i in cities:
                    if not tmp[j] == '':
                        name_city[i]['CO'].append(tmp[j])
                    j += 1
            elif tmp[2] == 'CO_24h':
                if name_city[cities[0]]['CO_24h'] != 0:
                    continue
                else:
                    j = 3
                    for i in cities:
                        name_city[i]['CO_24h'] = tmp[j]
                        j += 1
        line = lines[-1]
        tmp = line.strip().split(',')
        hour = tmp[1]

    return name_city, hour

