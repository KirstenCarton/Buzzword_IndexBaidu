import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 选择包含中文字符的字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示为方块的问题


# 从文件目录中加载文件
# 2023-chatgpt-baseAttr-gender.csv
# 2023-chatgpt-baseAttr-age.csv
# 2023-01-01-2023-12-09-chatgpt.csv
# 2023-chatgpt-baseAttr-interest.csv
def file_input(gender_file, age_file, index_data, interest_file):
    file_paths = {
        "gender_data": f"./buzzword_gender_tmp/{gender_file}",
        "age_data": f"./buzzword_age_tmp/{age_file}",
        "search_index_data": f"./buzzword_index_tmp/{index_data}",
        "interest_data": f"./buzzword_interest_tmp/{interest_file}"
    }
    return file_paths


# 使用pd从每个文件中读取数据
def read_df(file_paths):
    gender_df = pd.read_csv(file_paths["gender_data"])
    age_df = pd.read_csv(file_paths["age_data"])
    search_index_df = pd.read_csv(file_paths["search_index_data"])
    interest_df = pd.read_csv(file_paths["interest_data"])

    # 展示头部的部分数据
    gender_df.head(), age_df.head(), search_index_df.head(), interest_df.head()
    return gender_df, age_df, search_index_df, interest_df


# 画一个饼状图
def create_pie_chart(data, labels, title, ax):
    ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_title(title)


if __name__ == '__main__':
    file_paths = file_input('2023-chatgpt-baseAttr-gender.csv', '2023-chatgpt-baseAttr-age.csv', '2023-01-01-2023-12-09-chatgpt.csv', '2023-chatgpt-baseAttr-interest.csv')
    gender_df, age_df, search_index_df, interest_df = read_df(file_paths=file_paths)

    # ------------
    # 创建可视化视图
    fig, axs = plt.subplots(2, 2, figsize=(14, 14))

    # 1. Search Index Trend - Line Chart 搜索指数，折线图
    search_index_df['Date'] = pd.to_datetime(search_index_df['Date'])
    axs[0, 0].plot(search_index_df['Date'], search_index_df['DecryptedData'])
    axs[0, 0].set_title('ChatGPT Search Index Over Time')
    axs[0, 0].set_xlabel('Date')
    axs[0, 0].set_ylabel('Search Index')

    # 2. Gender Distribution - Pie Chart 性别分布，饼图
    create_pie_chart(gender_df['rate'], gender_df['desc'], 'Gender Distribution', axs[0, 1])

    # 3. Age Distribution - Pie Chart   年龄分布，饼图
    create_pie_chart(age_df['rate'], age_df['desc'], 'Age Distribution', axs[1, 0])

    # 4. Interest Distribution - Pie Chart 兴趣爱好分布，饼图
    create_pie_chart(interest_df['rate'], interest_df['type'], 'Interest Distribution', axs[1, 1])

    plt.tight_layout()
    plt.show()
