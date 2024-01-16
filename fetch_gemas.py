import requests
import json
import os
from bs4 import BeautifulSoup
from time import sleep
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def fetch_gemas(page_num):
    new_dict_data = {}
    print("start to fetch gemas data")
    for i in range(0, page_num):
        print("fetching page " + str(i))
        url = f"http://gz.gemas.com.cn/portal/page?to=proUtrms&proType=housingA&pageIndex={str(i + 1)}&pkey=6&proPriceStart=200&proPriceEnd=500"
        response = requests.get(url)
        new_dict_data.update(parse_html_to_obj(response.text))
        sleep(3)
    print("finish fetching gemas data")

    old_dict_data = {}
    file_name = "gemas_data.json"
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            old_json_data = file.read()
        old_dict_data = json.loads(old_json_data)

    added_dict_data = {}
    for key in new_dict_data:
        if key not in old_dict_data:
            added_dict_data[key] = new_dict_data[key]
            old_dict_data[key] = new_dict_data[key]
    print("today added " + str(len(added_dict_data)))

    old_json_data = json.dumps(old_dict_data, ensure_ascii=False, indent=2)
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(old_json_data)
    print("finish writing data to " + file_name)

    send_email(added_dict_data)


def parse_html_to_obj(html_content):
    if not html_content:
        print('没有获取到HTML内容')
        return

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'lxml')

    # 查找所有符合条件的div标签
    div_list = soup.find_all('div', {'class': 'main mt20'})
    if not div_list:
        print('没有找到符合要求的div标签')
        return

    li_list = div_list[0].find_all('li')
    if not li_list:
        print('没有找到符合要求的li标签')
        return

    # 输出匹配的内容
    result = {}
    for li in li_list:
        # print(li)
        status = li.select_one('.img_status').text.strip()
        title = li.select_one('h5').text.strip()
        price = li.select_one('.dqj span').text.strip()
        date_range = li.find('p', class_='gpqnew').text.strip().split('至')
        start_date = date_range[0].replace("挂牌日期：", "").strip()
        end_date = date_range[1].strip().split('\r\n')[0]
        project_number = li.find('p', class_='gpqnew').find('br').next_sibling.strip().replace("项目编号：", "")
        result[project_number] = {
            'status': status,
            'title': title,
            'price': price,
            'start_date': start_date,
            'end_date': end_date,
        }
    return result


def send_email(added_dict_data):
    # 邮件配置
    sender_email = "shijiajie0090@163.com"
    receiver_email = "stone0090@qq.com"
    subject = "gemas data update " + str(len(added_dict_data))
    body = json.dumps(added_dict_data, ensure_ascii=False, indent=2)

    # SMTP服务器配置
    smtp_server = "smtp.163.com"
    smtp_port = 465
    smtp_username = "shijiajie0090@163.com"
    smtp_password = "xxx"

    # 构建邮件
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # 连接到SMTP服务器并发送邮件
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("邮件发送成功")
    except Exception as e:
        print("邮件发送失败:", e)


def test_parse_html_to_arr():
    with open('gemas_example.html', 'r', encoding='utf-8') as file:
        html = file.read()
    result = parse_html_to_obj(html)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    fetch_gemas(10)
