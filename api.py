"""给根本不看空气质量的人发短信"""
from urllib.request import quote

import requests


class AQIData(object):
    """空气质量数据"""

    def __init__(self, app_key):
        self._app_key = app_key

    def get(self, city_name):
        """获取当前空气质量数据"""
        url = "http://apis.haoservice.com/air/pm"
        params = {
            "city": city_name,
            "key": self._app_key
        }
        return requests.get(url=url, params=params).json()


class MsgSender(object):
    """短信发送"""

    def __init__(self, app_key):
        self._app_key = app_key

    def send(self, msg, mobile, tpl_id):
        aqi = int(msg.get("result").get("AQI"))
        pm25 = msg.get("result").get("PMTwoPointFive")
        if_wear_mask = "出门需要戴口罩"

        if aqi <= 50:
            quality = "优"
        elif aqi <= 100:
            quality = "良"
        elif aqi <= 150:
            quality = "轻度污染"
        elif aqi <= 200:
            quality = "中度污染"
        elif aqi <= 300:
            quality = "重度污染"
        elif aqi <= 500:
            quality = "严重污染"
        else:
            quality = "污染爆表"

        content = (
            "#quality#=%s&#if_wear_mask#=%s&"
            "#aqi#=%s&#pm25#=%s"
        ) % (quality, if_wear_mask, aqi, pm25)
        url = " http://apis.haoservice.com/sms/send"
        params = {
            "mobile": mobile,
            "tpl_id": tpl_id,
            "tpl_value": quote(content),
            "key": self._app_key
        }
        return requests.get(url=url, params=params).json()
