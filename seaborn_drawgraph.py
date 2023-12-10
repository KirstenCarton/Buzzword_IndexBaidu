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


# 绘制plot bar charts
def plot_bar_chart(data, x, y, title, xlabel, ylabel, color, rotation=0):
    plt.figure(figsize=(10, 6))
    sns.barplot(x=x, y=y, hue=x, data=data, palette=color)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=rotation)
    plt.show()


# 绘制搜索指数折线图
def plot_search_index_over_time(dataframe):
    # 将 'Date' column 转化成时间对象 datetime
    dataframe['Date'] = pd.to_datetime(dataframe['Date'])
    # Create the plot
    plt.figure(figsize=(15, 6))
    sns.lineplot(x='Date', y='DecryptedData', data=dataframe, color='purple')
    # Setting the title and labels
    plt.title('ChatGPT Search Index Over Time')
    plt.xlabel('Date')
    plt.ylabel('Search Index')
    # 格式化x轴用来显示月份
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    # Rotate the date labels for better readability
    plt.xticks(rotation=45)
    plt.show()


if __name__ == '__main__':
    file_paths = file_input('2023-chatgpt-baseAttr-gender.csv', '2023-chatgpt-baseAttr-age.csv', '2023-01-01-2023-12-09-chatgpt.csv', '2023-chatgpt-baseAttr-interest.csv')
    gender_df, age_df, search_index_df, interest_df = read_df(file_paths=file_paths)

    # Setting up the visual style 设置样式和字体，字体颜色不对也会无法显示中文
    sns.set(style="whitegrid")
    sns.set(font='SimHei')  # 或 'Microsoft YaHei'

    # Plotting 性别分布
    plot_bar_chart(
        gender_df,
        x='desc',
        y='rate',
        title='Gender Distribution for ChatGPT Interest',
        xlabel='Gender',
        ylabel='Percentage (%)',
        color='Blues'
    )

    # Plotting 年龄分布
    plot_bar_chart(
        age_df,
        x='desc',
        y='rate',
        title='Age Distribution for ChatGPT Interest',
        xlabel='Age Group',
        ylabel='Percentage (%)',
        color='Greens'
    )

    plot_search_index_over_time(search_index_df)

    # Plotting 兴趣爱好分布
    plot_bar_chart(
        interest_df,
        x='type',
        y='rate',
        title='Interest Distribution for ChatGPT Searchers',
        xlabel='Interest Type',
        ylabel='Percentage (%)',
        color='Oranges',
        rotation=45
    )