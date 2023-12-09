import datetime,requests,time,random,jsonpath,json
import json,execjs
import os
import sys

import pandas as pd
from os.path import exists
from os import makedirs

RESULTS_DIR_INDEX = 'buzzword_index_tmp'
exists(RESULTS_DIR_INDEX) or makedirs(RESULTS_DIR_INDEX)

RESULTS_DIR_AGE = 'buzzword_age_tmp'
exists(RESULTS_DIR_AGE) or makedirs(RESULTS_DIR_AGE)

RESULTS_DIR_INTEREST = 'buzzword_interest_tmp'
exists(RESULTS_DIR_INTEREST) or makedirs(RESULTS_DIR_INTEREST)

RESULTS_DIR_GENDER = 'buzzword_gender_tmp'
exists(RESULTS_DIR_GENDER) or makedirs(RESULTS_DIR_GENDER)

headers = {
        'Cipher-Text': '1683381603090_1683465841465_cBL6JPQcXfYJb8GTBNZ7oLh07nimUUJmt9KQ3M5o0yYJjB8ugeggt6ONlReMzjsaz+4VL/W4Q6ojWnHF6MW7LTbY5qSnyttbKOtqUwVrTFRz1G7gLwkYhVz/fBoHdlDVDW19uELBDoWcpzXcS2QCAubDcC0+sKqDdAVh3X5cBOQNFQt1sTrBu7xyjhPzexvGw8XLtEqcpMhIdo3qIIgYxR2eFvBo4uMhpIxtwdR4afc7+F3VwyoqlLCay1PAlNgumc9u4A3Fz8weOYWqpvrGt6Kfu0tjxH4p4joL2uH5A2/qpEmt3OTFrvgWcq76vRFhoyJbTBAKPMRVdikqq8xTnI4fgQ6nODO/QqIx7PHsaUx5lS7fRpnue6nHYtrwQrFDq/gczjDIto3W8ilskoNO4h//ZHl1C+YVOzk0dlULzrS/VqTVMqpvc8YG0MZyhokH',
        'Cookie': 'BIDUPSID=ECF5C00403EFB880D0471503C517D7AF; PSTM=1700366736; BAIDUID=ECF5C00403EFB880C528C0025CEEA18D:FG=1; H_PS_PSSID=39676_39678_39707_39713_39737_39766_39780_39703_39684_39661_39817_39839; BAIDUID_BFESS=ECF5C00403EFB880C528C0025CEEA18D:FG=1; ZFY=:Ak:AbSfq6CHHeUjEgZQ0YxqCdXql4eo2SVuDNZf3EuMk:C; BDUSS=E5lVTA2TlFBcW1uNVF5UHVzR1pRamQ4WWlWZnk0TDhaNnpRbVdKZTl6STE3WlJsRVFBQUFBJCQAAAAAAAAAAAEAAAA6vLKWcmFyYXJhaXIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADVgbWU1YG1lM; bdindexid=sphnl7kvh0oce0k85m87k4ark0; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1700660834,1701656714,1701666832,1701822347; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a045183479555Doj7fB7jlfWlkwrbW12A%2B3BGllCS6mjOoIjctzWmTlvaT%2Fcb9FOIAp2ITQ8wETRf6MUY6mF%2FiuwdlE%2BFGIq0BCZRYpfObfVbK%2B00oi6SBLQrBtvvmxkFglkkyajfb%2Bw0NLA526zSDfuLnXpPZQIoWeaD9lM%2FFxscYCZ3uJ%2FomOq0tMk8zYwLA9NjfPek6oKA48DG5GbT3xbtjV5p5Xg5P64FGmpaTXi3PBNO30MDRujTTNJFk3NbJ4efX9u1QbhiUjRSeaSCOZOI8QS8n3eCA%3D%3D58809109902226262366835545865897; __cas__rn__=451834795; __cas__st__212=4f766c0a63883c997d5022421f7d80c1f757cca1fafe39a914c8d1c1794868577093fdf464417cee3b35a2d4; __cas__id__212=51876559; CPTK_212=1815609448; CPID_212=51876559; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1701825779; ab_sr=1.0.1_YzZjNzdlMWE0ZjNlNDc3Njg5ZjllMzdiMDE3NDhhZjI2MDdhNDU5NmNjYjYxN2JhNTgwYzAyMjZmMWMzOWVjZjY5N2YyYjQ0NTIwYmVjYjY0NGE1ZGJmNTIzYTcxMTQ0ZmI1NjZlZWI1ZWMwYTdlNDI2NDU3YjBlNzJhMGNhZmQ2MjhmOWEyZWMwOGM3MzMzODdlYzMxMzJkYzhjZTk0NQ==; BDUSS_BFESS=E5lVTA2TlFBcW1uNVF5UHVzR1pRamQ4WWlWZnk0TDhaNnpRbVdKZTl6STE3WlJsRVFBQUFBJCQAAAAAAAAAAAEAAAA6vLKWcmFyYXJhaXIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADVgbWU1YG1lM; RT="z=1&dm=baidu.com&si=03c54861-317f-49a2-9bf3-3f1bd590a721&ss=lpt132r1&sl=i&tt=u10h&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=21m5c"',
        'Host': 'index.baidu.com',
        'Referer': 'https://index.baidu.com/v2/main/index.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
}


def buzzword_input():
    # 读取用户上传的CSV文件
    file_path = './buzzword_WordAndYear.csv'
    buzzwords_df = pd.read_csv(file_path)
    return buzzwords_df


# 获取index的搜索数据
def getData_task():
    df = buzzword_input()
    for index, row in df.iterrows():
        keyword = row['词汇']
        year = row['年份']
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        get_feedIndex_datas(0, keyword=keyword, y_start=start_date, y_end=end_date)


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
            return response
    except requests.RequestException:
        print("error occured while scraping %s", url)


#将年份传入，然后对年份进行操作
def get_feedIndex_datas(d_index,keyword,y_start,y_end):
    # 测试是能够正常请求到加密的密文 url是接口url, indexData用于存放返回包的数据
    keyword = str(keyword).replace("'", '"')
    # indexData_url = f'https://index.baidu.com/api/SearchApi/index?area={d_index}&word=[[%7B%22name%22:%22{keyword}%22,%22wordType%22:1%7D]]&startDate={y_start}-01-01&endDate={y_end}-12-31'
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
    # 获取状态码
    decData.raise_for_status()
    # 统一解密用的密钥和密文用一种编码
    decData.encoding = indexData.apparent_encoding

    # 处理返回包的json数据
    startDate = indexData.json()['data']['userIndexes'][0]['all']['startDate']
    endDate = indexData.json()['data']['userIndexes'][0]['all']['endDate']
    print(f'数据是{keyword}, {startDate}, {endDate}')

    # 遍历每一个数据，然后用key
    sources = jsonpath.jsonpath(indexData.json(), '$..all.data')
    # 密钥
    key = decData.json()['data']
    print(key)

    # dataLs可以包括起始日期的所有字符串
    dateStart = datetime.datetime.strptime(startDate, '%Y-%m-%d')
    dateEnd = datetime.datetime.strptime(endDate, '%Y-%m-%d')
    str_datastart = str(dateStart)[0:10]
    str_dataend = str(dateEnd)[0:10]
    dataLs = []
    while dateStart <= dateEnd:
        dataLs.append(str(dateStart)[0:10])
        dateStart += datetime.timedelta(days=1)

    # 这里是使用key进行解密。好的，可以解密，
    for source in sources:
        res = decrypt(key, source)
        resArr = res.split(",")
    print(resArr)
    print(len(resArr))

    try:
        # 创建dataframe 将爬取到的数据建立映射到dataframe这个数据接口中，然后保存
        df = pd.DataFrame(
            {
                'Date': dataLs,
                'DecryptedData': resArr
            }
        )
        file_name = f"{str_datastart}-{str_dataend}-{keyword}.csv"
        # 将索引列的名称修改为 "点赞"
        df.index.name = f"{keyword}"
        # 构建完整的文件路径
        file_path = os.path.join(RESULTS_DIR_INDEX, file_name)
        # 将数据保存到文件中
        df.to_csv(file_path)
        return
    except  Exception as e:
        # 打印异常信息并继续执行后续操作
        print(f"处理关键字 '{keyword}' 时发生异常: {e}")
        return  # 跳出当前函数的执行，继续后续关键词的处理

def get_baseAttr_interest_task():
    df = buzzword_input()
    for index, row in df.iterrows():
        keyword = row['词汇']
        year = row['年份']
        get_interest_datas(keyword=keyword,year=year)


def get_interest_datas(keyword, year):
    keyword = str(keyword).replace("'", '"')
    indexData_url = f'https://index.baidu.com/api/SocialApi/interest?wordlist[]={keyword}&typeid='
    indexData = get_url_res(indexData_url)
    baseArr = indexData.json()
    # 遍历整个json数据，如果该词未收录就跳过
    if not indexData or 'result' not in baseArr['data']:
        print(f'数据对于关键字 {keyword} 用户兴趣画像不存在，跳过')
        return

    # 该关键字的interest字段
    result = baseArr['data']['result'][0]['interest']
    # print(result)
    rows = []
    for interest_type in result:
        row = {
            'type': interest_type['desc'],
            'tgi': interest_type['tgi'],
            'rate': interest_type['rate']
        }
        rows.append(row)
    print(f"{keyword}-{year}-{rows}")

    # 保存到csv文件中
    try:
        interest_df = pd.DataFrame(rows)
        file_name = f"{year}-{keyword}-baseAttr-interest.csv"
        interest_df.index.name = f"{keyword}"
        file_path = os.path.join(RESULTS_DIR_INTEREST, file_name)
        interest_df.to_csv(file_path)
    except Exception as e:
        # 打印异常信息并继续执行后续操作
        print(f"处理关键字 '{keyword}' 用户兴趣分布 时发生异常: {e}")
        return  # 跳出当前函数的执行，继续后续关键词的处理


def get_baseAttr_age_task():
    df = buzzword_input()
    for index, row in df.iterrows():
        keyword = row['词汇']
        year = row['年份']
        get_age_datas(keyword=keyword,year=year)


# 用户画像中的年份，性别数据可以不要unipid,有一个cookie就可以直接请求，甚至不需要请求的年份
def get_age_datas(keyword, year):
    # 测试是能够正常请求到加密的密文 url是接口url, indexData用于存放返回包的数据
    keyword = str(keyword).replace("'", '"')
    indexData_url = f'https://index.baidu.com/api/SocialApi/baseAttributes?wordlist[]={keyword}'

    # 先写年龄后写性别
    indexData = get_url_res(indexData_url)
    baseArr = indexData.json()
    # 遍历整个json数据，如果该词未收录就跳过
    if not indexData or 'result' not in baseArr['data']:
        print(f'数据对于关键字 {keyword} 年龄用户画像不存在，跳过')
        return

    # 该关键字的age字段
    result = baseArr['data']['result'][0]['age']
    # print(result)
    rows = []
    for age_group in result:
        row = {
            # 'keyword': baseArr['data']['result'][0]['word'],
            'desc': age_group['desc'],
            'tgi': age_group['tgi'],
            'rate': age_group['rate']
        }
        rows.append(row)
    print(f"{keyword}-{year}-{rows}")

    # 保存到csv文件中
    try:
        age_df = pd.DataFrame(rows)
        file_name = f"{year}-{keyword}-baseAttr-age.csv"
        age_df.index.name = f"{keyword}"
        file_path = os.path.join(RESULTS_DIR_AGE, file_name)
        age_df.to_csv(file_path)
    except Exception as e:
        # 打印异常信息并继续执行后续操作
        print(f"处理关键字 '{keyword}' 用户年龄 时发生异常: {e}")
        return  # 跳出当前函数的执行，继续后续关键词的处理


# 对所有的流行词的性别进行分析
def get_baseAttr_gender_task():
    df = buzzword_input()
    for index, row in df.iterrows():
        keyword = row['词汇']
        year = row['年份']
        get_gender_datas(keyword=keyword,year=year)


# 用户画像中的年份，性别数据可以不要unipid,有一个cookie就可以直接请求，甚至不需要请求的年份
def get_gender_datas(keyword, year):
    # 测试是能够正常请求到加密的密文 url是接口url, indexData用于存放返回包的数据
    keyword = str(keyword).replace("'", '"')
    indexData_url = f'https://index.baidu.com/api/SocialApi/baseAttributes?wordlist[]={keyword}'

    # 性别
    indexData = get_url_res(indexData_url)
    baseArr = indexData.json()
    # 遍历整个json数据，如果该词未收录就跳过
    if not indexData or 'result' not in baseArr['data']:
        print(f'数据对于关键字 {keyword} 用户性别画像不存在，跳过')
        return

    # 该关键字的age字段
    result = baseArr['data']['result'][0]['gender']
    # print(result)
    rows = []
    for gender_group in result:
        row = {
            # 'keyword': baseArr['data']['result'][0]['word'],
            'desc': gender_group['desc'],
            'tgi': gender_group['tgi'],
            'rate': gender_group['rate']
        }
        rows.append(row)
    print(f"{keyword}-{year}-{rows}")

    # 保存到csv文件中
    try:
        age_df = pd.DataFrame(rows)
        file_name = f"{year}-{keyword}-baseAttr-gender.csv"
        age_df.index.name = f"{keyword}"
        file_path = os.path.join(RESULTS_DIR_GENDER, file_name)
        age_df.to_csv(file_path)
    except Exception as e:
        # 打印异常信息并继续执行后续操作
        print(f"处理关键字 '{keyword}' 用户年龄 时发生异常: {e}")
        return  # 跳出当前函数的执行，继续后续关键词的处理


# 将年份传入，然后对年份进行操作 。。废了，不想清洗数据了，做做人物画像得了 这个功能废了不要管了
def get_feedIndex_datas_all(d_index,keyword,y_start,y_end):
    # 测试是能够正常请求到加密的密文 url是接口url, indexData用于存放返回包的数据
    keyword = str(keyword).replace("'", '"')
    indexData_url = f'https://index.baidu.com/api/SearchApi/index?area={d_index}&word=[[%7B%22name%22:%22{keyword}%22,%22wordType%22:1%7D]]'
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
    # 获取状态码
    decData.raise_for_status()
    # 统一解密用的密钥和密文用一种编码
    decData.encoding = indexData.apparent_encoding

    # 处理返回包的json数据
    startDate = indexData.json()['data']['userIndexes'][0]['all']['startDate']
    endDate = indexData.json()['data']['userIndexes'][0]['all']['endDate']
    print(f'数据是{keyword}, {startDate}, {endDate}')

    # 遍历每一个数据，然后用key
    sources = jsonpath.jsonpath(indexData.json(), '$..all.data')
    # 密钥
    key = decData.json()['data']
    print(key)

    # dataLs可以包括起始日期的所有字符串
    dateStart = datetime.datetime.strptime(startDate, '%Y-%m-%d')
    dateEnd = datetime.datetime.strptime(endDate, '%Y-%m-%d')
    str_datastart = str(dateStart)[0:10]
    str_dataend = str(dateEnd)[0:10]
    dataLs = []
    while dateStart <= dateEnd:
        dataLs.append(str(dateStart)[0:10])
        dateStart += datetime.timedelta(days=1)

    # 这里是使用key进行解密。好的，可以解密，
    for source in sources:
        res = decrypt(key, source)
        resArr = res.split(",")

    print(resArr)
    print(dataLs)
    print("  datdaLs:  " + str(len(dataLs)) + "  resArr  " + str(len(resArr)))

    # 找到第一个非空值的索引
    first_valid_index = next((i for i, x in enumerate(resArr) if x != "" and x != "0"), None)
    print(first_valid_index)
    if first_valid_index is not None:
        # 从第一个非空元素开始映射数据 注意是切片不要忘了:
        dataLs = dataLs[first_valid_index:]
        resArr = resArr[first_valid_index:]
        try:
            # 创建dataframe 将爬取到的数据建立映射到dataframe这个数据接口中，然后保存
            df = pd.DataFrame(
                {
                    'Date': dataLs,
                    'DecryptedData': resArr
                }
            )
            file_name = f"{keyword}-{str_datastart}-{str_dataend}.csv"
            # 将索引列的名称修改为 "点赞"
            df.index.name = f"{keyword}"
            # 构建完整的文件路径
            file_path = os.path.join(RESULTS_DIR_INDEX, file_name)
            # 将数据保存到文件中
            df.to_csv(file_path)
            return
        except Exception as e:
            # 打印异常信息并继续执行后续操作
            print(f"处理关键字 '{keyword}' 时发生异常: {e}")
            return  # 跳出当前函数的执行，继续后续关键词的处理
    else:
        print(f"关键词 {keyword} 在指定时间范围内没有有效的搜索量数据")


if __name__ == '__main__':
    # getData_task()
    # get_baseAttr_age_task()
    # get_baseAttr_gender_task()
    # get_baseAttr_interest_task()

    get_feedIndex_datas(0, "chatgpt", "2023-01-01", "2023-12-09")
    get_age_datas("chatgpt", 2023)
    get_interest_datas("chatgpt", 2023)
    get_gender_datas("chatgpt", 2023)
