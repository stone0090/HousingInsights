import requests
import json
import csv
import re
import os
from datetime import date
from bs4 import BeautifulSoup
from time import sleep


def fetch_bk_deals(custom_headers, district):
    result = []
    print("start to fetch " + district + "deal data")
    for i in range(0, 100):
        print("fetching page " + str(i))
        url = "https://gz.ke.com/chengjiao/" + district + "/pg" + str(i + 1) + "/"
        response = requests.get(url, headers=custom_headers)
        deals = parse_html_to_arr(response.text)
        print(deals)
        result.extend(deals)
        sleep(3)
    print("finish fetching " + district + " deal data")
    json_data = json.dumps(result, ensure_ascii=False, indent=2)
    file_name = "history3000_" + district + '_' + date.today().strftime('%Y-%m-%d') + '.json'
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(json_data)
    print("finish writing data to " + file_name)
    json_to_csv(file_name, 'haizhu')
    print("finish convert json to csv")


def parse_html_to_arr(html_content):
    if not html_content:
        print('没有获取到HTML内容')
        return

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'lxml')

    # 查找所有符合条件的div标签
    div_list = soup.find_all('div', {'data-component': 'list'})
    if not div_list:
        print('没有找到符合要求的div标签')
        return

    li_list = div_list[0].find_all('li', class_='VIEWDATA')
    if not li_list:
        print('没有找到符合要求的li标签')
        return

    # 输出匹配的内容
    result = []
    for li in li_list:
        print(li)
        title_list = li.select_one('.title a').text.strip().split(' ')
        xiaoqu, fangxing, mianji = '', '', ''
        for title in title_list:
            if title != '' and xiaoqu == '':
                xiaoqu = title
                continue
            if title != '' and fangxing == '':
                fangxing = title
                continue
            if title != '' and mianji == '':
                mianji = title
                continue
        chaoxiang, zhuangxiu = li.select_one('.houseInfo').text.strip().split('|')
        dealDate = li.select_one('.dealDate').text.strip()
        totalPrice = float(li.select_one('.totalPrice .number').text.strip())
        unitPrice = float(li.select_one('.unitPrice .number').text.strip())
        positionInfo = li.select_one('.flood .positionInfo').text.strip()
        dealHouseInfo = ' '.join(span.text.strip() for span in li.select('.dealHouseInfo span:not([class])'))
        dealCycleeInfo = ' '.join(span.text.strip() for span in li.select('.dealCycleeInfo span:not([class])'))
        dealInfo = {
            "xiaoqu": xiaoqu,
            "fangxing": fangxing,
            "mianji": mianji,
            "chaoxiang": chaoxiang,
            "zhuangxiu": zhuangxiu,
            "dealDate": dealDate,
            "totalPrice": totalPrice,
            "unitPrice": unitPrice,
            "positionInfo": positionInfo,
            "dealHouseInfo": dealHouseInfo,
            "dealCycleeInfo": dealCycleeInfo
        }
        result.append(dealInfo)
    return result


def json_to_csv(json_file, district):
    file_name, file_extension = os.path.splitext(json_file)
    csv_file = file_name + '.csv'
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for obj in data:
            obj["district"] = district
            match = re.search(r'(\d+(?:\.\d+)?)', obj["mianji"])
            if match:
                obj["mianji"] = float(match.group(1))
        with open(csv_file, 'w', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for item in data:
                writer.writerow(item.values())
    # 打开输入文件并读取内容
    with open(csv_file, 'r', encoding='utf-8') as input_file:
        # 读取文件内容并去除空白行
        lines = [line.strip() for line in input_file if line.strip()]
    # 打开输出文件并写入处理后的内容
    with open(csv_file, 'w', encoding='utf-8') as output_file:
        output_file.write('\n'.join(lines))


def test_parse_html_to_arr():
    with open('bk_example.html', 'r', encoding='utf-8') as file:
        html = file.read()
    result = parse_html_to_arr(html)
    print(json.dumps(result, ensure_ascii=False, indent=2))


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Host": "gz.ke.com",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
}

if __name__ == '__main__':
    # test_parse_html_to_arr()
    headers["Cookie"] = ""
    # districts = ['tianhe', 'haizhu', 'yuexiu', 'liwan', 'panyu', 'baiyun', 'huangpugz']
    fetch_bk_deals(headers, 'tianhe')
