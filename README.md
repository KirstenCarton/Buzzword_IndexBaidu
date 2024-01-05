## IndexBaidu Buzzword Collection

Reference Project：

[1] https://github.com/longxiaofei/spider-BaiduIndex

[2] https://github.com/Kit139/baidu_index_scraper



task方法用来读取文件然后一条条爬取；测试单个方法的时候可指定关键字，有的指数未被收录，可能数据不存在

包括：搜索指数、用户年龄分布、用户性别分布、用户兴趣领域分布



### 使用指南

index_baidu_buzzword.py有全部的工具函数，为了方便将header写死在了里面，使用该脚本的时候需要手动从浏览器中复制原始的cookie替换header中的cookie，将发送的请求转换成json格式输出即可检测脚本能够正常使用



### 修改记录

240105新增Elasticsearch+MongoDB+Flask简单检索页面

新增的文件放在/searching目录下，用于尝试学习使用Elasticsearch

- app.py是Flask的启动文件，静态页面放在templates模版下的
- index_baidu_buzzword-search.py 是爬虫文件，将爬取的文件存储在本地的MongoDB数据库中