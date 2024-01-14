import json
import csv
import re


def json_to_csv(json_file, csv_file, district):
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


if __name__ == '__main__':
    json_to_csv('history3000_haizhu_2024-01-13.json', 'history3000_haizhu_2024-01-13.csv', 'haizhu')
    json_to_csv('history3000_liwan_2024-01-13.json', 'history3000_liwan_2024-01-13.csv', 'liwan')
    json_to_csv('history3000_tianhe_2024-01-13.json', 'history3000_tianhe_2024-01-13.csv', 'tianhe')
    json_to_csv('history3000_yuexiu_2024-01-13.json', 'history3000_yuexiu_2024-01-13.csv', 'yuexiu')
