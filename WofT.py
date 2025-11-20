# -*- coding:utf-8 -*-
# !/usr/bin/python
import requests
from datetime import datetime
import xmltodict
from openai import OpenAI

def get_current_date_string():
    current_date = datetime.now().date()
    return current_date.strftime("%Y%m%d")

def get_current_hour_string():
    now = datetime.now()
    if now.minute<45: # base_time와 base_date 구하는 함수
        if now.hour==0:
            base_time = "2330"
        else:
            pre_hour = now.hour-1
            if pre_hour<10:
                base_time = "0" + str(pre_hour) + "30"
            else:
                base_time = str(pre_hour) + "30"
    else:
        if now.hour < 10:
            base_time = "0" + str(now.hour) + "30"
        else:
            base_time = str(now.hour) + "30"

    # print('기준시간: ' + base_time)
    return base_time

keys = 'Your Service Key'
url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
params ={'serviceKey' : keys, 
         'pageNo' : '1', 
         'numOfRows' : '1000', 
         'dataType' : 'XML', 
         'base_date' : get_current_date_string(), 
         'base_time' : get_current_hour_string(), 
         'nx' : '55', 
         'ny' : '127' }

def forecast():
    # 값 요청 (웹 브라우저 서버에서 요청 - url주소와 파라미터)
    res = requests.get(url, params = params)

    #XML -> 딕셔너리
    xml_data = res.text
    dict_data = xmltodict.parse(xml_data)

    #값 가져오기
    weather_data = dict()
    for item in dict_data['response']['body']['items']['item']:
        # 기온
        if item['category'] == 'T1H':
            weather_data['tmp'] = item['fcstValue']
        # 습도
        if item['category'] == 'REH':
            weather_data['hum'] = item['fcstValue']
        # 하늘상태: 맑음(1) 구름많은(3) 흐림(4)
        if item['category'] == 'SKY':
            weather_data['sky'] = item['fcstValue']
        # 강수형태: 없음(0), 비(1), 비/눈(2), 눈(3), 빗방울(5), 빗방울눈날림(6), 눈날림(7)
        if item['category'] == 'PTY':
            weather_data['sky2'] = item['fcstValue']

    return weather_data

def proc_weather():
    dict_sky = forecast()

    str_sky = "서울 "
    if dict_sky['sky'] != None or dict_sky['sky2'] != None:
        str_sky = str_sky + "날씨 : "
        if dict_sky['sky2'] == '0':
            if dict_sky['sky'] == '1':
                str_sky = str_sky + "맑음"
            elif dict_sky['sky'] == '3':
                str_sky = str_sky + "구름많음"
            elif dict_sky['sky'] == '4':
                str_sky = str_sky + "흐림"
        elif dict_sky['sky2'] == '1':
            str_sky = str_sky + "비"
        elif dict_sky['sky2'] == '2':
            str_sky = str_sky + "비와 눈"
        elif dict_sky['sky2'] == '3':
            str_sky = str_sky + "눈"
        elif dict_sky['sky2'] == '5':
            str_sky = str_sky + "빗방울이 떨어짐"
        elif dict_sky['sky2'] == '6':
            str_sky = str_sky + "빗방울과 눈이 날림"
        elif dict_sky['sky2'] == '7':
            str_sky = str_sky + "눈이 날림"
        str_sky = str_sky + "\n"
    if dict_sky['tmp'] != None:
        str_sky = str_sky + "온도 : " + dict_sky['tmp'] + 'ºC \n'
    if dict_sky['hum'] != None:
        str_sky = str_sky + "습도 : " + dict_sky['hum'] + '%'

    return str_sky
    
api_key = 'Your OpenAI API Key'

def generate_encouragement(weather):
    # prompt = f"오늘의 날씨는 {weather['날씨 정보']}입니다. 이 날씨에 맞는 응원의 한마디와 운세를 알려주세요."
    prompt = "오늘의 날씨는 " + weather + "입니다. 이 날씨에 맞는 응원의 한마디와 운세를 알려주세요."
    client = OpenAI()
    client.api_key = api_key
    # export OPENAI_API_KEY='Your OpenAI API Key'

    message = ""
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo", #"gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant designed to output JSON."},
                {
                    "role": "user",
                    "content": prompt
                },
                {
                    "role": "assistant",
                    "content": "GPT-4 Turbo is an advanced version of GPT-4, optimized for faster responses and improved accuracy. It supports a wide range of tasks, offering robust answers across various domains."}
            ]
        )

        message = completion.choices[0].message
    except Exception as e:
        message = e

    print(message)
    return message

if __name__ == "__main__":
    weather_of_today =proc_weather() 
    print(weather_of_today)
    '''
    서울 날씨 : 맑음
    온도 : 19ºC
    습도 : 95%
    '''

    encouragement_message = generate_encouragement(weather_of_today)
    print(encouragement_message)
