import datetime, requests, jsonpath, json
import json, execjs
import os
import sys

import pandas as pd
from os.path import exists
from os import makedirs

import pymongo
from pymongo import MongoClient

# 该脚本用于爬取 关键字的 1.百度搜索指数2.年龄分布3.性别分布4.兴趣爱好分布
# 指定目录
RESULTS_DIR_INDEX = 'buzzword_index_tmp'
exists(RESULTS_DIR_INDEX) or makedirs(RESULTS_DIR_INDEX)

RESULTS_DIR_AGE = 'buzzword_age_tmp'
exists(RESULTS_DIR_AGE) or makedirs(RESULTS_DIR_AGE)

RESULTS_DIR_INTEREST = 'buzzword_interest_tmp'
exists(RESULTS_DIR_INTEREST) or makedirs(RESULTS_DIR_INTEREST)

RESULTS_DIR_GENDER = 'buzzword_gender_tmp'
exists(RESULTS_DIR_GENDER) or makedirs(RESULTS_DIR_GENDER)

# none-exist 词语
none_word = []

headers = {
        'Cipher-Text': '1683381603090_1683465841465_cBL6JPQcXfYJb8GTBNZ7oLh07nimUUJmt9KQ3M5o0yYJjB8ugeggt6ONlReMzjsaz+4VL/W4Q6ojWnHF6MW7LTbY5qSnyttbKOtqUwVrTFRz1G7gLwkYhVz/fBoHdlDVDW19uELBDoWcpzXcS2QCAubDcC0+sKqDdAVh3X5cBOQNFQt1sTrBu7xyjhPzexvGw8XLtEqcpMhIdo3qIIgYxR2eFvBo4uMhpIxtwdR4afc7+F3VwyoqlLCay1PAlNgumc9u4A3Fz8weOYWqpvrGt6Kfu0tjxH4p4joL2uH5A2/qpEmt3OTFrvgWcq76vRFhoyJbTBAKPMRVdikqq8xTnI4fgQ6nODO/QqIx7PHsaUx5lS7fRpnue6nHYtrwQrFDq/gczjDIto3W8ilskoNO4h//ZHl1C+YVOzk0dlULzrS/VqTVMqpvc8YG0MZyhokH',
        'Cookie': 'BIDUPSID=ECF5C00403EFB880D0471503C517D7AF; PSTM=1700366736; BAIDUID=ECF5C00403EFB880C528C0025CEEA18D:FG=1; BAIDUID_BFESS=ECF5C00403EFB880C528C0025CEEA18D:FG=1; BAIDU_WISE_UID=wapp_1703681768747_578; H_PS_PSSID=39938_39974_39998_40009_40083; BA_HECTOR=00a42480200l2kaka48l8hahb6igm41ip9e8s1s; ZFY=00TSAnSzWHWkI3R8z4QH9OGUHYR8Efe6nXtAUFjsYtE:C; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1702182049,1702281529,1702299068,1704249210; BDUSS=NQaDQtMEduRDF2MGw5V0VDLWgxZWFVcjdHZmt6NzU5TUJHTzVEUnpVR2tWTHhsSVFBQUFBJCQAAAAAAAAAAAEAAAA6vLKWcmFyYXJhaXIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKTHlGWkx5Rlc0; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a04542617066AE0f1hdgCs6OkLFrCMOMAsX4rztGzQ98xJzV0E%2F3zNMVG%2B2YaE0qdrjH%2BsRfr927mLutrEPaikQA7H%2BWZVWfXY5RHc4hkaGlBtax2wPjSkwy0t%2Fsy0bDISpBFZjX0Irp5RvRblEY9ES3IRxQaHt5mG%2BmWvWFMlIlqxyqqvbbxmcqDbQj5VmZuQGg1wujlvSsCuRb%2FyMiVrGKZnbtdTTSWhk5yAUrda7uNiQafyFHWyE1fVoaUionIX1%2BwCtzd6OALqTyd3Q%2FktZqq9fG9VUNCQ%3D%3D80089553286052975940582052769323; __cas__rn__=454261706; __cas__st__212=2c7ee473d5b410c496d2bdb41275e015c88786a7dd138f4276228f9ca13c1a49558d385b7ad9b391d8f956b1; __cas__id__212=51876559; CPTK_212=1385152925; CPID_212=51876559; bdindexid=4joj9v180d8iomrn5iv5s5enp5; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1704250752; ab_sr=1.0.1_ZDBjOWFkZmJmOWE1MjkxZjk4ODQ2OGZkZWJhNWE1YjFlNzQyMjBmZGRlYzRiZjRmYzg2NjRkNDVhNjNmNzMyYzEwM2ZiY2FlYzRjZDI1OTIwYmNkZGZjNTg5ZDQwOTM1M2Y0ZTVhY2UxOWQxN2VjMjJiZjcwNDQyZWE3ZjU2MDk2OGZiMjBlZjNkMmFmZTZlNzg5MmM4OWRlOThkODllNw==; RT="z=1&dm=baidu.com&si=761701a4-21cf-4444-99ec-f5508d971dbb&ss=lqx5z28z&sl=e&tt=1k2a&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=1i3y3"',
        'Host': 'index.baidu.com',
        'Referer': 'https://index.baidu.com/v2/main/index.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
}


def buzzword_input():
    # 读取用户上传的CSV文件
    file_path = './buzzword_WordAndYear.csv'
    buzzwords_df = pd.read_csv(file_path)
    return buzzwords_df


# 判断数据是否存在，再进行读数据
def check_data_exist(keyword):
    try:
        keyword = str(keyword).replace("'", '"')
        indexData_url = f'https://index.baidu.com/api/SearchApi/index?area=0&word=[[%7B%22name%22:%22{keyword}%22,%22wordType%22:1%7D]]'
        indexData = get_url_res(indexData_url)
        # 检查是否成功获取数据!!!!
        if not indexData or 'data' not in indexData.json() or 'uniqid' not in indexData.json()['data']:
            print(f'数据对于关键字 {keyword} 不存在，跳过')
            return False
        else:
            return True
    except Exception as e:
        print(f"{e}")


# 搜索指数数据解密
def decrypt(t, e):
    n = list(t)
    i = list(e)
    a = {}
    result = []
    ln = int(len(n) / 2)
    start = n[ln:]
    end = n[:ln]
    for j, k in zip(start, end):
        a.update({k: j})
    for j in e:
        result.append(a.get(j))
    return ''.join(result)


def get_ptbk(uniqid):
    url = 'http://index.baidu.com/Interface/ptbk?uniqid={}'
    resp = requests.get(url.format(uniqid), headers=headers)

    if resp.status_code != 200:
        print('获取uniqid失败')
        sys.exit(1)
    return resp.json().get('data')


# 这个是个统一的接口，用来测试url能否正常访问，然后将返回包的数据返回
def get_url_res(url):
    requests.adapters.DEFAULT_RETRIES = 5
    try:
        response = requests.get(url=url, headers=headers, timeout=30)
        if response.status_code == 200:
            # print(response)
            result = response.json()
            # print(result)
            return response
    except requests.RequestException:
        print("error occured while scraping %s", url)


# 获取index的搜索数据
def getData_task():
    df = buzzword_input()
    for index, row in df.iterrows():
        keyword = row['词汇']
        year = row['年份']
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        if check_data_exist(keyword):
            get_feedIndex_datas(0, keyword=keyword, y_start=start_date, y_end=end_date)
            get_interest_datas(keyword=keyword, year=year)
            get_age_datas(keyword=keyword, year=year)
            get_gender_datas(keyword=keyword, year=year)
        else:
            print(f"{keyword} 未被收录")
            none_word.append(keyword)
            continue


# 将年份传入，然后对年份进行操作
def get_feedIndex_datas(d_index, keyword, y_start, y_end):
    # 连接数据库
    client = MongoClient('mongodb://localhost:27017')
    db = client['baidu_index']
    collection = db['search_index']

    # 测试是能够正常请求到加密的密文 url是接口url, indexData用于存放返回包的数据
    keyword = str(keyword).replace("'", '"')
    indexData_url = f'https://index.baidu.com/api/SearchApi/index?area={d_index}&word=[[%7B%22name%22:%22{keyword}%22,%22wordType%22:1%7D]]&startDate={y_start}&endDate={y_end}'
    ptbk_url = 'https://index.baidu.com/Interface/ptbk?uniqid='

    indexData = get_url_res(indexData_url)

    # 检查是否成功获取数据!!!!
    if not indexData or 'data' not in indexData.json() or 'uniqid' not in indexData.json()['data']:
        print(f'数据对于关键字 {keyword} 不存在，跳过')
        return

    # 获取unipid用于解密数据 (是uniqid不是pid)
    uniqid = indexData.json()['data']['uniqid']
    print(f'unipid is {uniqid}')

    # 将unipid传参，ptbk是一个加解密用的url，使用unipid解密后得到decData,
    decData = get_url_res(ptbk_url + uniqid)

    try:
        # 获取状态码
        decData.raise_for_status()
    except Exception as e:
        print(f"处理interest关键字 '{keyword}' 时发生异常: {e}")
        return
    # 统一解密用的密钥和密文用一种编码
    decData.encoding = indexData.apparent_encoding

    # 处理返回包的json数据
    startDate = indexData.json()['data']['userIndexes'][0]['all']['startDate']
    endDate = indexData.json()['data']['userIndexes'][0]['all']['endDate']

    # 遍历每一个数据，然后用key
    sources = jsonpath.jsonpath(indexData.json(), '$..all.data')
    # 密钥
    key = decData.json()['data']
    # print(key)

    # dataLs可以包括起始日期的所有字符串
    dateStart = datetime.datetime.strptime(startDate, '%Y-%m-%d')
    dateEnd = datetime.datetime.strptime(endDate, '%Y-%m-%d')
    str_datastart = str(dateStart)[0:10]
    str_dataend = str(dateEnd)[0:10]
    dataLs = []
    while dateStart <= dateEnd:
        dataLs.append(str(dateStart)[0:10])
        dateStart += datetime.timedelta(days=1)

    try:
        # 解密数据
        for source in sources:
            res = decrypt(key, source)
            resArr = res.split(",")

        # 检查dataLs和resArr的长度是否一致
        if len(dataLs) != len(resArr):
            raise ValueError("日期列表和数据列表长度不一致")

        # 创建包含日期和数据的列表
        date_data_pairs = [{'date': date, 'data': data} for date, data in zip(dataLs, resArr)]
        # 构建要插入的文档
        document = {
            '_id': keyword,  # 使用keyword作为文档的主键
            'keyword': keyword,
            'data': date_data_pairs
        }

        # 将文档保存到MongoDB中
        collection.insert_one(document)
        print(f"成功插入数据到MongoDB，searchindex 关键字：{keyword}")
    except Exception as e:
        # 打印异常信息并继续执行后续操作
        print(f"处理关键字 '{keyword}' 时发生异常: {e}")


def get_baseAttr_interest_task():
    df = buzzword_input()
    for index, row in df.iterrows():
        keyword = row['词汇']
        year = row['年份']
        get_interest_datas(keyword=keyword, year=year)


def get_interest_datas(keyword, year):
    # 连接数据库
    client = MongoClient('mongodb://localhost:27017')
    db = client['baidu_index']
    collection = db['interest_index']

    # 发起请求
    keyword = str(keyword).replace("'", '"')
    indexData_url = f'https://index.baidu.com/api/SocialApi/interest?wordlist[]={keyword}&typeid='
    indexData = get_url_res(indexData_url)
    try:
        baseArr = indexData.json()
        # 遍历整个json数据，如果该词未收录就跳过
        if not indexData or 'result' not in baseArr['data']:
            print(f'数据对于关键字 {keyword} 用户兴趣画像不存在，跳过')
            return
    except Exception as e:
        print(f"处理 interest 关键字 '{keyword}' 时发生异常: {e}")
        return

    # 该关键字的interest字段
    interests = baseArr['data']['result'][0]['interest']
    interest_data = [{'type': interest['desc'], 'tgi': interest['tgi'], 'rate': interest['rate']} for interest in
                     interests]
    # 构建要插入的文档
    document = {
        '_id': keyword,  # 使用keyword作为文档的主键
        'year': year,
        'interests': interest_data
    }
    # 保存解析好的数据到mongodb中
    try:
        result = collection.insert_one(document)
        print('成功插入数据，插入文档的ID为:', result.inserted_id)
    except Exception as e:
        print(f"{keyword} interest 插入失败，报错为： {e}")

    print(f"{year}-{keyword}-interest-handled")


def get_baseAttr_age_task():
    df = buzzword_input()
    for index, row in df.iterrows():
        keyword = row['词汇']
        year = row['年份']
        get_age_datas(keyword=keyword, year=year)


# 用户画像中的年份，性别数据可以不要unipid,有一个cookie就可以直接请求，甚至不需要请求的年份
def get_age_datas(keyword, year):
    # 测试是能够正常请求到加密的密文 url是接口url, indexData用于存放返回包的数据
    keyword = str(keyword).replace("'", '"')
    indexData_url = f'https://index.baidu.com/api/SocialApi/baseAttributes?wordlist[]={keyword}'
    # 先写年龄后写性别
    indexData = get_url_res(indexData_url)
    try:
        baseArr = indexData.json()
        # 遍历整个json数据，如果该词未收录就跳过
        if not indexData or 'result' not in baseArr['data']:
            print(f'数据对于关键字 {keyword} 年龄用户画像不存在，跳过')
            return
    except Exception as e:
        print(f"处理 age 关键字 '{keyword}' 时发生异常: {e}")
        return

    # 连接数据库
    client = MongoClient('mongodb://localhost:27017')
    db = client['baidu_index']
    collection = db['age_index_a']

    # 该关键字的age字段
    ages = baseArr['data']['result'][0]['age']
    age_data = [{'desc': age_group['desc'],'tgi': age_group['tgi'],'rate': age_group['rate']} for age_group in ages]

    # 要插入的文档
    document = {
        '_id': keyword,
        'year': year,
        'age': age_data
    }
    try:
        result = collection.insert_one(document)
        print('成功插入数据，插入文档的ID为:', result.inserted_id)
    except Exception as e:
        print(f"{keyword} age 插入失败 报错为：{e}")
    print(f"{year}-{keyword}-age-handled")


# 对所有的流行词的性别进行分析
def get_baseAttr_gender_task():
    df = buzzword_input()
    for index, row in df.iterrows():
        keyword = row['词汇']
        year = row['年份']
        try:
            get_gender_datas(keyword=keyword, year=year)
        except Exception as e:
            print(f"采集失败：{e}")
            continue


# 用户画像中的年份，性别数据可以不要unipid,有一个cookie就可以直接请求，甚至不需要请求的年份
def get_gender_datas(keyword, year):
    # 测试是能够正常请求到加密的密文 url是接口url, indexData用于存放返回包的数据
    keyword = str(keyword).replace("'", '"')
    indexData_url = f'https://index.baidu.com/api/SocialApi/baseAttributes?wordlist[]={keyword}'
    try:
        # 性别
        indexData = get_url_res(indexData_url)
        baseArr = indexData.json()
        # 遍历整个json数据，如果该词未收录就跳过
        if not indexData or 'result' not in baseArr['data']:
            print(f'数据对于关键字 {keyword} 用户性别画像不存在，跳过')
            return
    except Exception as e:
        print(f"处理 gender 关键字 '{keyword}' 时发生异常: {e}")
        return

    # 连接数据库
    client = MongoClient('mongodb://localhost:27017')
    db = client['baidu_index']
    collection = db['gender_index']

    # 该关键字的age字段
    genders = baseArr['data']['result'][0]['gender']
    gender_data = [{'desc': gender_group['desc'],'tgi': gender_group['tgi'],'rate': gender_group['rate']} for gender_group in genders]
    try:
        document = {
            '_id': keyword,
            'year': year,
            'gender': gender_data
        }
        result = collection.insert_one(document)
        print('成功插入数据，插入文档的ID为:', result.inserted_id)
    except Exception as e:
        print(f"{keyword}插入失败 报错为：{e}")
    print(f"{year}-{keyword}-gender-handled")


if __name__ == '__main__':
    getData_task()
    # get_baseAttr_age_task()
    # get_baseAttr_gender_task()
    # get_baseAttr_interest_task()

    # get_feedIndex_datas(0, "chatgpt", "2023-01-01", "2023-12-09")
    # get_age_datas("chatgpt", 2023)
    # get_interest_datas("chatgpt", 2023)
    # get_gender_datas("chatgpt", 2023)
    # print("test")
