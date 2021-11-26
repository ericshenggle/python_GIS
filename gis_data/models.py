from django.db import models


# Create your models here.
class CityAirQualityInfo(models.Model):
    # 如果没有models.AutoField，默认会创建一个id的自增列
    objects = models.Manager()
    id = models.CharField('id', max_length=255, primary_key=True)
    name = models.CharField('城市名', max_length=255)
    date = models.IntegerField('日期', null=True)
    hour = models.CharField('小时', max_length=100, null=True)
    aqi = models.CharField('实时AQI', max_length=100, null=True)
    aqi_24h = models.CharField('平均AQI', max_length=100, null=True)
    pm2_5 = models.CharField('PM2.5', max_length=100, null=True)
    pm2_5_24h = models.CharField('PM2.5_24h', max_length=100, null=True)
    pm10 = models.CharField('PM10', max_length=100, null=True)
    pm10_24h = models.CharField('PM10_24h', max_length=100, null=True)
    so2 = models.CharField('SO2', max_length=100, null=True)
    so2_24h = models.CharField('SO2_24h', max_length=100, null=True)
    no2 = models.CharField('NO2', max_length=100, null=True)
    no2_24h = models.CharField('NO2_24h', max_length=100, null=True)
    o3 = models.CharField('O3', max_length=100, null=True)
    o3_24h = models.CharField('O3_24h', max_length=100, null=True)
    o3_8h = models.CharField('O3_8h', max_length=100, null=True)
    o3_8h_24h = models.CharField('O3_8h_24h', max_length=100, null=True)
    co = models.CharField('CO', max_length=100, null=True)
    co_24h = models.CharField('CO_24h', max_length=100, null=True)


class Meta:
    managed = True
