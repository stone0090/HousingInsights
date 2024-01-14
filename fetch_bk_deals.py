from time import sleep

import requests
import json
from datetime import date

from html_util import parse_html_to_arr

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


def fetch_bk_deals(headers, district):
    result = []
    print("start to fetch " + district + "deal data")
    for i in range(0, 100):
        print("fetching page " + str(i))
        url = "https://gz.ke.com/chengjiao/" + district + "/pg" + str(i + 1) + "/"
        response = requests.get(url, headers=headers)
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


if __name__ == '__main__':
    headers["Cookie"] = ""
    # districts = ['tianhe', 'haizhu', 'yuexiu', 'liwan', 'panyu', 'baiyun', 'huangpugz']
    fetch_bk_deals(headers, 'liwan')
