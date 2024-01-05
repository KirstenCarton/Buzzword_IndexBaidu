from bson import json_util
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from elasticsearch import Elasticsearch
import json

# 该脚本用于对数据进行检索
app = Flask(__name__)

# Elasticsearch 客户端
es = Elasticsearch(hosts=['http://localhost:9200'])  # 新版本将将状态码在这里创建

# MongoDB 客户端
client = MongoClient('mongodb://localhost:27017')
db = client['baidu_index']  # 替换为你的数据库名

# 为每个MongoDB表创建一个Elasticsearch索引
indices = ['age_index', 'gender_index', 'search_index', 'interest_index']
for index in indices:
    if es.indices.exists(index=index):
        es.indices.delete(index=index)
    es.indices.create(index=index)


# 插入数据到elasticsearch索引（工具函数）
def index_data_to_es(es_index):
    collection = db[es_index]
    # print('11')
    for document in collection.find():
        # print(document)
        try:
            # 使用json_util处理MongoDB文档
            document['id'] = str(document['_id'])
            document.pop('_id', None)  # 安全移除 '_id' 字段
            es.index(index=es_index, id=document['id'], body=document)
        except Exception as e:
            print(f'{e}')


@app.route('/index_data', methods=['GET'])
def index_data():
    for index in indices:
        index_data_to_es(index)
    try:
        return jsonify({'message': 'Data indexed successfully'})            # 使用了 Flask 的 jsonify 函数来转换 Python 字典为 JSON 格式
    except Exception as e:
        print(f'{e}')


@app.route('/search', methods=['GET'])
def search():
    index = request.args.get('index')
    keyword = request.args.get('keyword')

    if not index or not keyword:
        return jsonify({'error': 'Index and keyword parameters are required'}), 400

    query = {
        "query": {
            "ids": {
                "values": [keyword]
            }
        }
    }

    response = es.search(index=index, body=query)
    # print(response)
    hits = response['hits']['hits']
    # return jsonify(hits if hits else [])
    results = [hit['_source'] for hit in hits]
    return render_template('search.html', results=results)


@app.route('/')
def index():
    return render_template('search.html', results=[])


if __name__ == '__main__':
    app.run(debug=True)
