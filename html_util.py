from bs4 import BeautifulSoup
import json


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


if __name__ == '__main__':
    with open('example.html', 'r', encoding='utf-8') as file:
        html = file.read()
    result = parse_html_to_arr(html)
    print(json.dumps(result, ensure_ascii=False, indent=2))
